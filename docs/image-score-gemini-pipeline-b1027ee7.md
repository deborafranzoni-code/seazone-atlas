<!-- title: Image Score Gemini Pipeline | url: https://outline.seazone.com.br/doc/image-score-gemini-pipeline-bHc3oZz8VD | area: Tecnologia -->

# Image Score Gemini Pipeline

# Pipeline de Pontuação de Imagens com Gemini

Este projeto implementa um pipeline robusto e assíncrono para analisar e pontuar imagens de anúncios de propriedades (ex: Airbnb) utilizando o modelo multimodal `Gemini` da Google, através da plataforma Vertex AI. O objetivo é extrair características visuais das imagens e atribuir pontuações para diversas categorias (como acabamentos, decoração, iluminação), processando apenas os anúncios que ainda não foram analisados.

## Arquitetura e Fluxo de Trabalho

O pipeline é projetado para ser resiliente e eficiente, operando de forma incremental. Ele identifica novos anúncios, processa-os em lotes, salva os resultados periodicamente e registra falhas para análise posterior.

O fluxo de trabalho é o seguinte:


1. **Inicialização e Alertas**:
   * O `main.py` inicia o processo e configura o `CloudFunctionAlertSender`, um sistema de monitoramento que envia alertas críticos para uma Cloud Function em caso de falhas fatais no pipeline.
2. **Setup Inteligente**:
   * A `CategorizationPipeline` é inicializada.
   * **Seleção de Dados Incrementais**: Em vez de processar todos os dados, o pipeline consulta o BigQuery para selecionar apenas os metadados de anúncios que ainda **não** possuem resultados na tabela de features (`dataset_features`). Isso é feito através de um `LEFT JOIN`.
   * Os dados são carregados de forma iterativa (usando `to_dataframe_iterable()`) para otimizar o uso de memória, ideal para grandes volumes de dados.
   * Os prompts necessários são baixados do Google Cloud Storage (GCS).
3. **Inicialização do Modelo Gemini**:
   * O serviço Vertex AI é inicializado com o projeto e localização corretos.
   * Um modelo generativo (ex: `gemini-2.0-flash`) é carregado com uma instrução de sistema (prompt) que o orienta a analisar as imagens e retornar um JSON estruturado com as pontuações.
   * As configurações de segurança são ajustadas para `BLOCK_NONE` para evitar bloqueios desnecessários, e o `response_mime_type` é definido como `"application/json"` para garantir saídas válidas.
4. **Processamento Assíncrono em Lotes**:
   * O pipeline itera sobre os dados do BigQuery em páginas.
   * Dentro de cada página, os dados são agrupados por `airbnb_listing_id` e processados em "chunks" (lotes) de tamanho configurável.
   * Para cada anúncio, todas as suas imagens são enviadas em uma única requisição concorrente para o modelo Gemini usando `asyncio.gather`.
5. **Error Handling e Retries**:
   * **Robustez da API**: A função `generate_vertex_async` implementa um mecanismo de **retry com backoff exponencial** para lidar com erros transitórios da API, como `ServiceUnavailable`, `FailedPrecondition` e `ResourceExhausted`.
   * **Tratamento de Falhas**: Falhas permanentes (ex: imagem não encontrada (`NotFound`), JSON inválido, bloqueio por filtros de segurança) são capturadas. As informações da requisição e o erro são armazenados em uma lista de falhas.
6. **Salvamento Incremental e Finalização**:
   * **Buffer de Sucesso**: Os resultados bem-sucedidos são acumulados em um buffer.
   * **Salvamento em Lotes**: Quando o buffer atinge um tamanho pré-definido (`save_chunk_size`), os resultados são processados e salvos como um arquivo Parquet no GCS. Isso garante que o progresso seja salvo periodicamente, evitando perda de dados em caso de falha.
   * **Salvamento de Falhas**: Ao final da execução, a lista de requisições com falha é salva em um arquivo Parquet separado no GCS (`dataset_tables/logs/`), permitindo depuração e reprocessamento.
   * Os arquivos de resultado e de log são nomeados com um timestamp para garantir a unicidade.

## Estrutura do Projeto

```
image_score_gemini_pipeline/
├── app/
│   ├── __init__.py
│   ├── pipeline.py       # (CORE) Classe CategorizationPipeline com a lógica principal.
│   └── util.py           # Funções utilitárias para GCS e sistema de arquivos.
├── prompts/
│   └── prompt_score_por_tipo.txt # Instrução de sistema para o modelo Gemini.
├── main.py               # Ponto de entrada para executar o pipeline.
├── cloud_function_alert_sender.py # Cliente para enviar alertas de monitoramento.
├── gemini.py             # Script de rascunho/versão anterior para testes.
├── sandbox-*.json        # Arquivo de credenciais do Service Account (NÃO VERSIONAR).
└── README.md             # Esta documentação.
```

## Componentes Principais

### `main.py`

O orquestrador do pipeline. Suas responsabilidades são:

* Instanciar o `CloudFunctionAlertSender` para monitoramento.
* Envolver a execução do pipeline em um bloco `try...except` para capturar exceções fatais e enviar um alerta crítico.
* Instanciar e executar a `CategorizationPipeline` na sequência correta: `setup`, `get_vertex_model`, `process_in_chunks`, e `save_failures`.

### `app/pipeline.py`

O coração do projeto. A classe `CategorizationPipeline` encapsula toda a lógica:

* `**__init__**`: Configura os parâmetros do GCP, inicializa o cliente BigQuery e os buffers para resultados e falhas.
* `**setup()**`: Prepara o ambiente, baixando prompts e, crucialmente, criando um iterador de metadados a partir de uma consulta ao BigQuery que seleciona apenas os dados pendentes.
* `**get_vertex_model()**`: Configura e retorna uma instância do modelo generativo do Vertex AI.
* `**generate_vertex_async()**`: Função assíncrona que envia as imagens para a API do Gemini. Inclui a lógica de retentativas, tratamento de exceções específicas da API (NotFound, InvalidArgument, etc.), e validação da resposta (JSON, bloqueios de segurança).
* `**process_in_chunks()**`: Gerencia o processamento concorrente dos anúncios em lotes, separa sucessos de falhas e aciona o salvamento incremental.
* `**_save_chunk()**`: Salva um lote de resultados do buffer para um arquivo Parquet no GCS, processando os dados e limpando o buffer em seguida.
* `**save_failures()**`: Salva todas as falhas registradas durante a execução em um arquivo Parquet dedicado no GCS para análise.

### `cloud_function_alert_sender.py`

Uma classe utilitária para enviar alertas para uma Cloud Function via requisição HTTP POST.

* Gera um token de identidade (ID Token) usando um Service Account para autenticar a requisição de forma segura.
* Formata a carga útil do alerta com informações como `execution_id`, `app_name`, severidade, mensagem e detalhes do erro.

### `prompts/prompt_score_por_tipo.txt`

Arquivo de texto contendo a instrução de sistema para o Gemini. Define o papel do modelo, as categorias a serem pontuadas, a escala de pontuação e o formato de saída JSON esperado, incluindo como lidar com imagens irrelevantes (`BadImage`).

## Como Executar


1. **Configurar o Ambiente**:
   * Certifique-se de ter o Python 3.10+ instalado.
   * Instale as dependências:

     ```bash
     pip install pandas google-cloud-aiplatform google-cloud-storage google-cloud-bigquery python-dotenv requests google-auth
     ```
   * Autentique-se no Google Cloud CLI:

     ```bash
     gcloud auth application-default login
     ```
2. **Configurar Credenciais e Variáveis**:
   * **Service Account**: Coloque o arquivo JSON do seu Service Account na raiz do projeto (ex: `sandbox-439302-e5ebce1seus-dados.json`). Este arquivo é referenciado em `main.py` e `cloud_function_alert_sender.py`.
   * **URL da Cloud Function**: Verifique se a URL no `main.py` para o `CloudFunctionAlertSender` está correta.
3. **Verificar Pré-requisitos no GCP**:
   * **BigQuery**: As tabelas `categorizacao.metadata` e `categorizacao.dataset_features` devem existir no projeto configurado.
   * **Cloud Storage**: O bucket (`categorizacao_pipeline`) deve existir. Ele deve conter os prompts no caminho `prompts/`. As imagens dos anúncios também devem estar no bucket, seguindo a estrutura de caminho esperada (`gs://<bucket>/<id_anuncio>/images/<id_imagem>.jpg`).
   * **APIs**: As APIs do Vertex AI, BigQuery e Cloud Storage devem estar ativadas no seu projeto GCP.
4. **Executar o Pipeline**:
   * O pipeline é iniciado executando o `main.py`:

     ```bash
     python main.py
     ```
   * Acompanhe os logs no console para ver o progresso. As mensagens indicarão o setup, o processamento das páginas do BigQuery, o processamento dos lotes do Gemini e o salvamento incremental dos resultados e falhas no GCS.