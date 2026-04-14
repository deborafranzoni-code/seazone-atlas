<!-- title: Image Score Classifier Pipeline | url: https://outline.seazone.com.br/doc/image-score-classifier-pipeline-FdWu8Lo6b7 | area: Tecnologia -->

# Image Score Classifier Pipeline

# Pipeline de Classificação de Anúncios por Pontuação de Imagem

Este projeto implementa um pipeline de Machine Learning de ponta a ponta para classificar anúncios do Airbnb em estratos de qualidade (`SIM`, `JR`, `SUP`, `TOP`, `MASTER`). O modelo utiliza uma combinação rica de dados, incluindo pontuações de qualidade de imagem, metadados dos anúncios, dados de performance (faturamento, ocupação) e informações geoespaciais.

O pipeline é projetado para ser robusto e resiliente, com logging detalhado, tratamento de erros e um sistema de alertas para monitorar a execução.

## Arquitetura e Fluxo de Trabalho

O pipeline é orquestrado pelo script `main.py` e segue uma sequência de etapas modulares. A lógica de tratamento de erros `safe_run` garante que falhas em etapas não críticas não interrompam todo o processo, registrando os erros para análise posterior.

O fluxo de trabalho é o seguinte:


1. **Setup Inicial e Configuração**:
   * **Logging**: Configura um sistema de logging duplo que grava os eventos em um arquivo (`logs/expansion_YYYYMMDD_HHMMSS.log`) e os exibe no console.
   * **Download de Ativos**: Baixa arquivos essenciais do Google Cloud Storage (GCS), como o KML com polígonos de corpos d'água (`water_brazil.kml`), que é crucial para a engenharia de features geoespaciais.
2. **Ingestão e Integração de Dados**:
   * **Features de Anúncios (AWS Athena)**: Carrega dados detalhados dos anúncios, incluindo localização, tipo, número de quartos, reviews, e dados de performance (preço médio, ocupação) da tabela `brlink_seazone_enriched_data.details_last_aquisitiondetails` e outras tabelas relacionadas no Athena.
   * **Polígonos de Competidores (Google BigQuery)**: Carrega polígonos geográficos associados a anúncios da tabela `competitors.competitors_polygons` no BigQuery.
   * **Dados Seazone (AWS Athena)**: Carrega categorias e estratos de anúncios gerenciados pela Seazone da tabela `sirius."inputdata-kdatqapgmwx1".setup_groups` para enriquecer os dados.
   * **Merge Inicial**: Os dados de diferentes fontes são mesclados para criar uma base unificada, enriquecendo anúncios com informações de polígono e estrato.
3. **Engenharia de Features**:
   * **Amenities (**`**get_amenities**`**)**: Processa a coluna `amenities`, que pode estar em formato de string ou JSON, para extrair features booleanas como `piscina`, `churrasqueira`, `vista_para_o_mar`, etc.
   * **Filtragem de Candidatos**: Seleciona um subconjunto de anúncios ("candidatos à expansão") com base em critérios de negócio, como tipo de imóvel (`apartamento`, `casa`), número de quartos (<= 2) e performance (reviews, faturamento).
   * **Dados de Sazonalidade**: Carrega o histórico de ocupação e faturamento dos anúncios candidatos para análise de sazonalidade, usando a tabela `brlink_seazone_enriched_data.fato_block_occupancy`.
   * **Features de Imagem (BigQuery)**: Carrega as pontuações de imagem (`Finishes`, `Electronics`, `Furniture`, etc.), geradas por um pipeline externo, da tabela `categorizacao.dataset_features`.
   * **Distância para a Água**: Calcula a distância mínima de cada anúncio para o corpo d'água mais próximo usando GeoPandas e o arquivo KML baixado.
   * **Criação de Novas Features**: Gera features derivadas, como `avg_price_by_room` (preço médio por quarto), `fat_by_room` (faturamento por quarto) e `fat_by_room_water_normal` (faturamento por quarto normalizado pela distância da água).
4. **Preparação para Modelagem (**`**get_fit_validation**`**)**:
   * O dataset é estrategicamente dividido em três partes:
     * `df_fit`: Anúncios de competidores com estrato conhecido, usados para **treinamento**.
     * `df_validation`: Anúncios da Seazone com estrato conhecido, usados para **validação** do modelo.
     * `df_no_strata`: Anúncios sem estrato definido, para os quais o modelo fará a **predição**.
5. **Treinamento, Avaliação e Predição (**`**train_evaluate_and_predict**`**)**:
   * **Gerenciamento de Modelo**: O pipeline primeiro verifica no GCS se um modelo treinado (`logistic_regression-model-final_model.joblib`) já existe.
     * **Se existe**: O modelo é baixado e o treinamento é pulado.
     * **Se não existe**: Um novo modelo é treinado.
   * **Treinamento**: Um pipeline do Scikit-learn é criado, contendo um `StandardScaler` e um modelo de `LogisticRegression` (configurado com `class_weight='balanced'`). O modelo é treinado com o conjunto `df_fit`. O modelo treinado é salvo localmente e enviado para o GCS.
   * **Avaliação**: O desempenho do modelo é avaliado no conjunto de validação (`df_validation`), e métricas detalhadas (Acurácia, F1-Score, MAE, etc.) são geradas e logadas.
   * **Predição em Lotes (**`**predict_and_save_in_batches**`**)**: Para otimizar o uso de memória, as predições para `df_no_strata` são feitas em lotes. Cada lote de predições é salvo como um arquivo Parquet diretamente no GCS, evitando o armazenamento de um grande arquivo de resultados localmente.
6. **Finalização e Alertas**:
   * Um resumo dos erros não fatais coletados durante a execução é salvo em um arquivo JSON (`logs/pipeline_errors_*.json`).
   * Se ocorreram erros, um alerta de `warning` é enviado para uma Cloud Function de monitoramento usando a classe `CloudFunctionAlertSender`, que notifica as partes interessadas (ex: via Slack).
   * Se a execução for bem-sucedida, uma mensagem de sucesso é logada.

## Estrutura do Projeto

```
Image_score_classifcator_pipeline/
├── src/
│   ├── __init__.py
│   ├── cloud_function_alert_sender.py # Classe para enviar alertas para uma Cloud Function.
│   ├── file_download.py               # Lógica para setup inicial e download de arquivos.
│   ├── model.py                       # Funções para modelagem, avaliação e engenharia de features.
│   ├── query.py                       # Funções para carregar dados do AWS Athena e BigQuery.
│   └── util.py                        # Funções utilitárias (upload/download de blobs, etc.).
├── main.py                            # Script principal que orquestra todo o pipeline.
├── logs/                              # Diretório para arquivos de log e resumos de erro (criado em tempo de execução).
├── data/                              # Diretório para dados brutos e intermediários.
├── results/                           # Diretório para resultados finais (predições, validação, etc.).
├── models/                            # Diretório para modelos treinados.
└── README.md                          # Esta documentação.
```

## Componentes Principais

### `main.py`

O cérebro do pipeline. Ele define a sequência de operações, desde a configuração até o salvamento dos resultados. Utiliza a função `safe_run` para encapsular chamadas, permitindo que o pipeline continue mesmo que uma etapa falhe, enquanto registra o erro para análise posterior.

### `src/query.py`

Centraliza todas as consultas a fontes de dados externas. As funções aqui são responsáveis por se conectar ao AWS Athena (via `awswrangler`) e ao Google BigQuery para buscar os dados brutos necessários para o pipeline.

### `src/model.py`

Contém a lógica de negócio para a modelagem e transformação de dados:

* `get_amenities`: Realiza a extração e limpeza das features de comodidades.
* `load_data`: Carrega as features de imagem e as integra com os dados dos anúncios.
* `get_fit_validation`: Implementa a estratégia de divisão de dados para treino, validação e predição.
* `create_pipeline`: Constrói o pipeline de modelo do Scikit-learn.
* `get_metrics`: Calcula e formata as métricas de avaliação de desempenho do classificador.
* `train_evaluate_and_predict`: Orquestra o ciclo de vida do modelo, incluindo verificação de existência, treinamento, avaliação e disparo das predições.

### `src/cloud_function_alert_sender.py`

Uma classe utilitária para enviar alertas estruturados e autenticados para uma Google Cloud Function. Isso permite um monitoramento proativo do status do pipeline.

## Fontes de Dados

* **AWS Athena**:
  * `brlink_seazone_enriched_data.details_last_aquisitiondetails`: Metadados principais dos anúncios.
  * `brlink_seazone_enriched_data.fato_block_occupancy`: Dados históricos de ocupação e faturamento.
  * `brlink_seazone_clean_data.seazone_listings_historic`: Mapeamento de anúncios para IDs Seazone.
  * `Sirius."competitorsdata-ytphkan8jhr0".competitors_output`: Estratos de competidores.
  * `sirius."inputdata-kdatqapgmwx1".setup_groups`: Categorias de anúncios Seazone.
* **Google BigQuery**:
  * `data-resources-448418.categorizacao.dataset_features`: Pontuações de qualidade de imagem.
  * `data-resources-448418.competitors.competitors_polygons`: Polígonos geográficos.
  * `data-resources-448418.categorizacao.prediction`: Tabela de predições existentes (para evitar reprocessamento).
* **Google Cloud Storage**:
  * `gs://categorizacao_pipeline/expansion/water_brazil.kml`: Arquivo KML com polígonos de corpos d'água.
  * `gs://categorizacao_pipeline/models/logistic_regression-model-final_model.joblib`: Armazenamento do modelo treinado.
  * `gs://categorizacao_pipeline/results/`: Destino para os arquivos Parquet com as predições em lotes.

## Como Executar


1. **Configurar o Ambiente**:
   * Certifique-se de ter o Python 3.9+ instalado.
   * Instale as dependências a partir do `requirements.txt` (se disponível) ou manualmente:

     ```bash
     pip install pandas geopandas awswrangler google-cloud-bigquery google-cloud-storage scikit-learn xgboost joblib fiona shapely
     ```
   * **Credenciais AWS**: Configure as credenciais de acesso para a AWS. A forma mais comum é através de variáveis de ambiente ou do arquivo `~/.aws/credentials`. O código espera as variáveis `AWS_ACCESS_KEY_ID` e `AWS_SECRET_ACCESS_KEY`.
   * **Credenciais Google Cloud**: Autentique-se no Google Cloud. Para desenvolvimento local, o mais simples é usar a CLI:

     ```bash
     gcloud auth application-default login
     ```

     Para produção, utilize um Service Account, garantindo que o caminho para o arquivo JSON da credencial esteja na variável de ambiente `GOOGLE_APPLICATION_CREDENTIALS`.
2. **Verificar Pré-requisitos**:
   * As tabelas de origem no AWS Athena e Google BigQuery devem estar acessíveis com as credenciais configuradas.
   * O arquivo `water_brazil.kml` deve estar disponível no bucket `categorizacao_pipeline` do GCS, no caminho `expansion/`.
3. **Executar o Pipeline**:
   * O pipeline é iniciado executando o script `main.py` a partir da raiz do projeto:

     ```bash
     python main.py
     ```
   * Acompanhe os logs no console e no arquivo gerado em `logs/` para ver o progresso de cada etapa. Ao final da execução:
     * O modelo treinado (`logistic_regression-model-final_model.joblib`) estará salvo no diretório `models/` e no GCS.
     * Os resultados da validação (`df_validation_with_predictions.parquet`) estarão em `results/expansion/`.
     * As predições para novos anúncios serão salvas em múltiplos arquivos Parquet no GCS, no bucket `categorizacao_pipeline` sob o prefixo `results/`.
     * Um resumo de erros (se houver) estará em `logs/`.