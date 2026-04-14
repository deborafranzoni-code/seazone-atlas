<!-- title: BI de Observabilidade | url: https://outline.seazone.com.br/doc/bi-de-observabilidade-G11EwYsF1Q | area: Tecnologia -->

# BI de Observabilidade

### 1. Contexto

O BI de Observabilidade é um dashboard que permite o monitoramento de métricas importantes. Ele foi desenvolvido no Power BI com dados da AWS (S3 e Athena) e oferece visibilidade para o time de DataOps, permitindo monitorar a execução dos scrapers, verificar a consistência das inserções de dados, avaliar métricas de preço, disponibilidade e faturamento (MAPE) e identificar possíveis problemas ou anomalias nos dados. 

Buscando a modernização da infraestrutura do BI, melhor integração com o ecossistema Google Cloud Plataform, redução de custos operacionais e a necessidade de corrigir e aprimorar métricas existentes, foi feita essa migração para a GCP. 

### 2. Objetivo

* Centralizar as fontes de dados no BigQuery;
* Padronizar o processo de atualização e histórico dos dados utilizados nos painéis;
* Reduzir custos e complexidade operacional, mantendo uma arquitetura mais simples;
* Garantir integridade e histórico completo, transferindo os dados anteriores da AWS para o BigQuery;
* Atualizar a visualização no Looker Studio, substituindo o Power BI como ferramenta principal.

### 3. Arquitetura no Google Cloud

#### 3.1 Ambiente

`Projeto: DataResources`\n`Dataset: lake_observability`

`Cloud Storage: bi_observability/insert_report`

#### 3.2 Componentes Utilizados

| Componente | Função |
|----|----|
| **BigQuery** | Utilizado para armazenar as tabelas com as métricas relevantes |
| **Cloud Storage** | Utilizado para armazenar o insert_report.json, necessário para a contagem de linhas diferentes |
| **AWS Lambda** | Executa queries no Athena, processa métricas e envia mensagens para o Slack. |
| **AWS Athena** | Contém as tabelas que serão consultadas pelos Lambdas. |

#### 3.3 Estrutura das tabelas no BigQuery

As tabelas foram criadas no projeto Data Resources, dentro do dataset lake_observability, e incluem os principais conjuntos de dados utilizados pelo BI de Observabilidade:

* anomaly_mape_report
* anomaly_price_metrics
* priceav_mape_report
* revenue_mape_monthly_big_errors
* revenue_mape_monthly_last_years
* revenue_mape_report_last_days
* scrapers_health

#### 3.4 Processo de Migração

* **Lambdas atualizados (PRD_Lake)**

  Foram adicionadas aos Lambdas funções e bibliotecas responsáveis por estabelecer a conexão com o Google Cloud, permitindo que as métricas sejam inseridas diretamente no BigQuery. Para viabilizar essa integração entre nuvens (AWS ↔ GCP), foi criada uma conta de serviço na GCP, dentro do projeto Data Resources, com permissão de Editor no BigQuery. As credenciais dessa conta de serviço foram armazenadas de forma segura no AWS Systems Manager Parameter Store, garantindo que as funções Lambda tenham acesso controlado e seguro ao BigQuery.

  \
  * RevenueMapeReport (mape_daily.py e mape_monthly.py)
  * AnomalyPriceAntecedence
  * AnomalyMapeReport
  * PriceAvMapeReport\n
* **Processo da Insert_report (Seazone Technology)**\nA insert_report é executada por meio de uma Step Function que orquestra, diariamente, uma ECS Task responsável por inserir no S3 os dados históricos e atualizar o arquivo insert_report.json (utilizado para comparar o número de linhas atuais com a quantidade registrada no dia anterior). 

  Durante o processo de migração, foram adicionados trechos de código que inserem no BigQuery (tabela scrapers_health) as métricas que anteriormente eram enviadas apenas para o histórico no S3 (insert_report_historic).\nAlém disso, o fluxo foi ajustado para que o arquivo `insert_report.json` passasse a ser lido diretamente do Cloud Storage, substituindo a dependência do S3.

  Para viabilizar essa integração com o Google Cloud, foram incluídas bibliotecas da Google Cloud no código da `insert_report` e criado um Parameter Store específico para armazenar com segurança as credenciais da conta de serviço responsável pela autenticação no BigQuery.\n

### 4. Fluxo do processo

 ![](/api/attachments.redirect?id=b29374b1-abb7-4cee-a954-c506cb56f588 " =1202x789")


### 5. Observações Importantes

O código da insert_report.py está alimentando, atualmente, o S3 e o BigQuery. Isso ocorre porque o BI de Observabilidade ainda precisa dos dados que estão no Bucket. É necessário, assim que o Looker Studio for criado, apagar a função que alimenta o S3 e garantir que os dados estejam apenas no BigQuery. 

### 6. Links Importantes

Lambdas:

* [AnomalyMapeReport](https://us-west-2.console.aws.amazon.com/lambda/home?region=us-west-2#/functions/DataLake-ReportsStack-ME5DT6NZ3D-AnomalyMapeReport-PCwdzG5XCYjw?tab=code)
* [AnomalyPriceAntecedence](https://us-west-2.console.aws.amazon.com/lambda/home?region=us-west-2#/functions/DataLake-ReportsStack-ME5D-AnomalyPriceAntecedence-watwnuRtkShO?tab=code)
* [RevenueMapeReport](https://us-west-2.console.aws.amazon.com/lambda/home?region=us-west-2#/functions/DataLake-ReportsStack-ME5DT6NZ3D-RevenueMapeReport-EUej1I6qJVaT?tab=code)
* [PriceAvMapeReport](https://us-west-2.console.aws.amazon.com/lambda/home?region=us-west-2#/functions/DataLake-ReportsStack-ME5DT6NZ3D-PriceavMapeReport-tfN6Qm1bJ0pX?tab=code)\n

Cloud Storage:

* [bi_observability](https://console.cloud.google.com/storage/browser/bi_observability;tab=objects?inv=1&invt=Ab214g&project=data-resources-448418&prefix=&forceOnObjectsSortingFiltering=false)

BigQuery:

* [anomaly_mape_report](https://console.cloud.google.com/bigquery?inv=1&invt=Ab214g&project=data-resources-448418&ws=!1m10!1m4!4m3!1sdata-resources-448418!2slake_observability!3sscrapers_health!1m4!4m3!1sdata-resources-448418!2slake_observability!3sanomaly_mape_report)
* [anomaly_price_antecedence](https://console.cloud.google.com/bigquery?inv=1&invt=Ab214g&project=data-resources-448418&ws=!1m10!1m4!4m3!1sdata-resources-448418!2slake_observability!3sscrapers_health!1m4!4m3!1sdata-resources-448418!2slake_observability!3sanomaly_mape_report)
* [priceav_mape_report](https://console.cloud.google.com/bigquery?inv=1&invt=Ab214g&project=data-resources-448418&ws=!1m10!1m4!4m3!1sdata-resources-448418!2slake_observability!3sscrapers_health!1m4!4m3!1sdata-resources-448418!2slake_observability!3spriceav_mape_report)
* [revenue_mape_report_last_years](https://console.cloud.google.com/bigquery?inv=1&invt=Ab214g&project=data-resources-448418&ws=!1m10!1m4!4m3!1sdata-resources-448418!2slake_observability!3sscrapers_health!1m4!4m3!1sdata-resources-448418!2slake_observability!3srevenue_mape_monthly_last_years)
* [revenue_mape_report_last_days](https://console.cloud.google.com/bigquery?inv=1&invt=Ab214g&project=data-resources-448418&ws=!1m10!1m4!4m3!1sdata-resources-448418!2slake_observability!3sscrapers_health!1m4!4m3!1sdata-resources-448418!2slake_observability!3srevenue_mape_report_last_days)
* [revenue_mape_report_big_errors](https://console.cloud.google.com/bigquery?inv=1&invt=Ab214g&project=data-resources-448418&ws=!1m10!1m4!4m3!1sdata-resources-448418!2slake_observability!3sscrapers_health!1m4!4m3!1sdata-resources-448418!2slake_observability!3srevenue_mape_monthly_big_errors)
* [scrapers_health](https://console.cloud.google.com/bigquery?inv=1&invt=Ab214g&project=data-resources-448418&ws=!1m10!1m4!4m3!1sdata-resources-448418!2slake_observability!3sscrapers_health!1m4!4m3!1sdata-resources-448418!2slake_observability!3srevenue_mape_report_last_days)