<!-- title: Documentação Técnica | url: https://outline.seazone.com.br/doc/documentacao-tecnica-DCVFlWntFO | area: Tecnologia -->

# Documentação Técnica

# **Cloud Function** `get-current-vivareal`

Este documento detalha o funcionamento e a arquitetura do processo de extração de dados `get-current-vivareal`. O objetivo principal deste processo é consultar dados de imóveis na plataforma Viva Real, que estão armazenados em um Data Lake na AWS, e disponibilizá-los para análise no Google Cloud Platform (GCP).

## **Visão Geral do Processo**

O código é executado como uma **Google Cloud Function** e serve como um pipeline de dados (ETL - Extract, Transform, Load) que realiza as seguintes etapas:


1. **Extração (Extract):** Conecta-se ao serviço AWS Athena para executar uma consulta SQL em um Data Lake, extraindo dados específicos sobre imóveis.
2. **Carga (Load):** Salva o resultado da consulta em um arquivo no formato **Parquet** dentro de um bucket do Google Cloud Storage (GCS).
3. **Disponibilização:** Os dados no GCS são posteriormente carregados na tabela `vivareal-current` no BigQuery.
4. **Visualização:** A tabela no BigQuery serve como fonte de dados para um painel de visualização no **Looker (Google Looker Studio)**.

## **Arquitetura do Fluxo de Dados**

O fluxo de dados segue a arquitetura descrita abaixo:


1. **Gatilho (Trigger):** A Cloud Function é acionada por uma requisição HTTP, podendo ser automatizada por um serviço como o Google Cloud Scheduler.
2. **Execução na Cloud Function:**
   * O código Python é executado no ambiente serverless do GCP.
   * Ele utiliza credenciais de acesso da AWS (armazenadas como variáveis de ambiente) para se autenticar.
   * Executa uma consulta na base `datalake` do AWS Athena.
3. **Armazenamento em GCS:**
   * O resultado da consulta é convertido em um DataFrame e salvo como um arquivo chamado `vivareal.parquet`.
   * Este arquivo é depositado no bucket `seazone-info`, no diretório `gcp-current-vivareal/`. O processo garante que qualquer arquivo existente seja removido antes de salvar o novo, garantindo que os dados estejam sempre atualizados.
4. **Integração com BigQuery:**
   * O arquivo Parquet no GCS é usado para popular a tabela `data-resources-448418.SEAZONE_INFO.vivareal-current` no BigQuery. Esta etapa pode ser realizada por um processo de carregamento do BigQuery ou usando uma tabela externa que aponta para o arquivo no GCS.
5. **Análise no Looker:**
   * O dashboard do Viva Real no Looker Studio conecta-se diretamente à tabela `vivareal-current` no BigQuery para exibir métricas e análises atualizadas. 

## **Análise Detalhada do Código**

O script Python utiliza bibliotecas especializadas para interagir com os serviços de nuvem da AWS e do GCP.

#### **Principais Bibliotecas**

* `awswrangler`: Simplifica a interação com serviços da AWS, especialmente para executar consultas no Athena e manipular os resultados.
* `functions_framework`: Biblioteca padrão do Google para criar e implantar Cloud Functions em Python.
* `gcsfs`: Permite interagir com o Google Cloud Storage como se fosse um sistema de arquivos local.
* `boto3`: SDK oficial da AWS para Python, usado para criar a sessão de autenticação.
* `requests`: Utilizado para enviar notificações de erro para um webhook.

#### **Estrutura do Código**

O código é encapsulado na função `main(request)`, que é o ponto de entrada padrão para uma Cloud Function acionada por HTTP.


1. **Configuração e Autenticação:**
   * As credenciais da AWS (`AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`) e a URL do webhook de erro (`DEV_WEBHOOK_URL`) são carregadas a partir de variáveis de ambiente para garantir a segurança.
   * Uma sessão `boto3` é iniciada para autenticar as chamadas para a AWS.
2. **Consulta SQL no Athena:**
   * Uma consulta SQL é definida para extrair dados da tabela `datalake.brlink_seazone_clean_data.vivareal`.
   * A consulta possui filtros específicos: `ano = '2025'`, `mes = '07'` e `usable_area >= 12`. **Atenção:** Estes valores são fixos no código e podem precisar de atualização para buscar dados de outros períodos.
   * A função `wr.athena.read_sql_query` executa a consulta e retorna os dados em um DataFrame do Pandas.

   \
   ```python
   query = '''
       SELECT * FROM datalake."brlink_seazone_clean_data".vivareal
       WHERE ano = '2025' AND mes = '07' AND usable_area >= 12
   '''
   
   query_result = wr.athena.read_sql_query(...)
   ```
3. **Armazenamento no Google Cloud Storage (GCS):**
   * O código primeiro tenta remover o diretório de destino (`gs://seazone-info/gcp-current-vivareal/`) usando `fs.rm()`. Isso garante que a execução seja **idempotente**, ou seja, o resultado final é sempre o mesmo, independentemente de quantas vezes o processo seja executado.
   * Em seguida, o DataFrame com os resultados da consulta é salvo no formato Parquet no GCS usando o método `to_parquet()`. O formato Parquet é otimizado para armazenamento colunar e performance em sistemas analíticos como o BigQuery.

     \

   ```python
   # Remove o diretório antigo para garantir dados novos
   fs.rm(PREFIX, recursive=True)
   
   # Salva o novo arquivo parquet
   query_result.to_parquet(f"gs://{PREFIX}/vivareal.parquet", ...)
   ```
4. **Tratamento de Erros:**
   * O código está envolto em um bloco `try...except`.
   * Se qualquer erro ocorrer durante a execução, uma notificação detalhada é enviada para o webhook definido na variável `DEV_WEBHOOK_URL`.
   * A notificação inclui a mensagem de erro e o *traceback* completo, facilitando a depuração. 

## **Dependências e Ambiente de Execução**

* **Plataforma:** Google Cloud Function.
* **Variáveis de Ambiente Obrigatórias:**
  * `AWS_ACCESS_KEY_ID`: Chave de acesso da AWS.
  * `AWS_SECRET_ACCESS_KEY`: Chave secreta da AWS.
  * `DEV_WEBHOOK_URL`: URL para notificação de erros (Slack).
* **Permissões Necessárias:**
  * A conta de serviço da Cloud Function precisa de permissão de **Leitura e Escrita (Storage Object Admin)** no bucket do GCS.
  * As credenciais da AWS precisam de permissão para executar consultas no Athena e ler os dados do Data Lake no S3.