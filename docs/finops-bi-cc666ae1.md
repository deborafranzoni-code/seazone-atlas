<!-- title: Finops BI | url: https://outline.seazone.com.br/doc/finops-bi-rgGgYqZKyB | area: Tecnologia -->

# Finops BI

Essa documentação foi criada com o objetivo de explicar como estamos fazendo a ingestão de dados de billing no BI centralizado de finops : <https://lookerstudio.google.com/reporting/2dee62a4-7d08-49d4-b580-ead1ec373d20>


---

# Documentação Técnica de Implementação de FinOps

## Objetivo

Esta implementação tem como objetivo integrar dados de custo provenientes da AWS, GCP (Google Cloud Platform) e do Kubecost, unificando-os em um dashboard do Looker para análise de custos. O processo abrange dados de contas, serviços, unidades de negócios (BU) e produtos, com uma atualização diária e automatizada.


---

## **Arquitetura da Implementação**

A implementação é composta por diversas etapas que envolvem a coleta de dados de diferentes fontes, transformação e carregamento em tabelas do BigQuery. Além disso, a automação do processo é realizada por workflows no GitHub e transfers do BigQuery.


---

### **1. Dados Comuns (AWS)**

#### **Fonte de Dados**:

* Dados normais da AWS, incluindo custos por conta e serviço.
* Os dados são exportados pela AWS usando o *Data Export* no formato Parquet.

#### **Processo**:


1. **Geração do Data Export**:
   * O Data Export é gerado com granularidade diária e é armazenado no bucket da AWS `s3://bigquery-billing-export-connection/parquet-standard-daily/`.
2. **Transferência para BigQuery**:
   * Foi configurado um *BigQuery Data Transfer* que se conecta ao bucket S3 da AWS e puxa automaticamente os dados do dia anterior às 7 AM todos os dias.
   * Link de referência: [BigQuery Data Transfer](https://docs.cloud.google.com/bigquery/docs/working-with-transfers)
3. **Armazenamento e Transformação**:
   * Os dados são carregados em uma tabela no BigQuery chamada `aws_daily`.
   * Uma *view* chamada `aws_daily_clean` é criada para realizar cálculos necessários e remover colunas desnecessárias. A *view* mantém apenas as colunas de data, custo, serviço e conta.


---

### **2. Dados de Unidades de Negócio (BU) e Produto**

#### **Fontes de Dados**:

* **Cost Categories** (AWS) – Dados que segmentam os custos por Unidade de Negócio (BU) e Produto.
* **Kubecost** – Sistema de gestão de custos de Kubernetes que também segmenta custos por BU e Produto.

#### **Processo**:


1. **Script Python para Coleta e Agregação de Dados**:
   * Dois scripts Python são desenvolvidos para coletar e processar dados:
     * **Script BU**: Acessa os dados do *Cost Categories* filtrando por BU e agrega os custos.
     * **Script Produto**: Acessa os dados do *Cost Categories* e Kubecost filtrando por Produto e agrega os custos.
     * Para ambos os casos, os recursos compartilhados são divididos percentualmente de acordo com as recomendações do *Cost Categories*.
2. **Armazenamento dos Dados**:
   * Os dados processados são exportados para buckets no GCP:
     * O formato dos dados para *BU* é `(data, BU, custo)`.
     * O formato dos dados para *Produto* é `(data, produto, custo)`.
3. **Automação e Workflow**:
   * Um workflow no GitHub é configurado para disparar a execução desses scripts diariamente às 6 AM. O workflow também permite a entrada de uma data específica para rodar o processo para um dia específico.
   * Após a execução, os dados processados são armazenados nos buckets do GCP.
4. **Transferência para BigQuery**:
   * Um *BigQuery Data Transfer* é configurado para rodar às 7 AM diariamente e atualizar as tabelas `aws_daily_bu` e `aws_daily_product` com os dados provenientes dos buckets do GCP.


---

### **3. Dados Comuns (GCP)**

#### **Fonte de Dados**:

* Dados normais de custo do GCP, incluindo custos por conta e serviço.
* Os dados são exportados usando a funcionalidade de *Billing Export* do GCP, que gera arquivos em formato Parquet.

#### **Processo**:


1. **Geração do Export de Billing**:
   * O export de Billing é gerado com granularidade diária e os dados são armazenados em um bucket no GCP.
2. **Transferência para BigQuery**:
   * Foi configurado um *BigQuery Data Transfer* para conectar ao bucket do GCP onde os dados de billing são exportados.
   * O transfer ocorre diariamente, trazendo os dados de custo do GCP para o BigQuery, mantendo-os atualizados automaticamente.
3. **Armazenamento e Transformação**:
   * Os dados de custo são carregados em uma tabela no BigQuery chamada `gcp_daily`.
   * Uma *view* chamada `gcp_daily_clean` é criada para aplicar os mesmos cálculos necessários e remover colunas desnecessárias. A *view* mantém apenas as colunas de data, custo, serviço e conta, similar ao processo realizado para os dados da AWS.


---

## **Automação e Sincronização**

* **GitHub Workflow**:
  * O processo de execução dos scripts Python para BU e Produto é automatizado por um workflow no GitHub, disparado às 6 AM diariamente. Este workflow garante que os dados sejam atualizados antes da execução do BigQuery Data Transfer.
* **BigQuery Data Transfer**:
  * O BigQuery Data Transfer é configurado para importar os dados da AWS e GCP para as tabelas no BigQuery às 7 AM diariamente, garantindo que as tabelas do BigQuery estejam sempre atualizadas.


---

## **Tabelas e Views no BigQuery**

### **1. aws_daily**:

* Tabela onde os dados de custo da AWS são carregados.

### **2. aws_daily_clean**:

* *View* que transforma os dados brutos da `aws_daily`, removendo colunas desnecessárias e realizando cálculos, mantendo apenas as colunas essenciais: data, custo, serviço e conta.

### **3. aws_daily_bu**:

* Tabela que contém os dados agregados por Unidade de Negócio (BU) da AWS, importados do bucket GCP.

### **4. aws_daily_product**:

* Tabela que contém os dados agregados por Produto da AWS, importados do bucket GCP.

### **5. gcp_daily**:

* Tabela onde os dados de custo do GCP são carregados, provenientes do *Billing Export*.

### **6. gcp_daily_clean**:

* *View* que transforma os dados brutos da `gcp_daily`, removendo colunas desnecessárias e realizando cálculos, mantendo apenas as colunas essenciais: data, custo, serviço e conta.


---

## **Fluxo de Dados**


1. **Coleta de Dados da AWS**:
   * Dados exportados da AWS são armazenados em um bucket S3 da AWS e transferidos para o BigQuery.
2. **Coleta de Dados do GCP**:
   * Dados de billing do GCP são exportados para um bucket do GCP e transferidos para o BigQuery.
3. **Coleta de Dados de BU e Produto**:
   * Dados são coletados dos serviços *Cost Categories* e Kubecost, processados por scripts Python e armazenados em buckets do GCP.
4. **Transferência de Dados para BigQuery**:
   * O BigQuery Data Transfer é configurado para sincronizar os dados da AWS e GCP para as tabelas no BigQuery às 7 AM diariamente.


---

## **Benefícios e Resultados Esperados**

* **Unificação de Dados**: A integração de dados provenientes da AWS, GCP e Kubecost em uma única plataforma facilita a análise e visibilidade dos custos.
* **Atualização Diária Automática**: A automação do processo de coleta e transferência de dados garante dados atualizados de forma eficiente e sem intervenção manual.
* **Análise Facilitada no Looker**: Com os dados organizados e disponíveis no BigQuery, o dashboard do Looker pode ser atualizado automaticamente para fornecer insights sobre os custos por serviço, conta, BU e produto.


---

```mermaidjs
flowchart TB

%% ======================
%% AWS – Dados Comuns
%% ======================
AWS[AWS Billing<br/>Custos por Conta e Serviço]
AWS_EXPORT[Data Export<br/>Parquet Diário]
AWS_S3[(S3 Bucket<br/>parquet-standard-daily)]
BQ_TRANSFER_AWS[BigQuery Data Transfer<br/>07:00]
BQ_AWS_RAW[BigQuery<br/>aws_daily]
BQ_AWS_VIEW[View<br/>aws_daily_clean]

AWS --> AWS_EXPORT
AWS_EXPORT --> AWS_S3
AWS_S3 --> BQ_TRANSFER_AWS
BQ_TRANSFER_AWS --> BQ_AWS_RAW
BQ_AWS_RAW --> BQ_AWS_VIEW

%% ======================
%% BU e Produto (AWS + Kubecost)
%% ======================
COST_CAT[AWS Cost Categories<br/>BU / Produto]
KUBECOST[Kubecost<br/>Custos Kubernetes]
GITHUB[GitHub Workflow<br/>06:00]
PY_BU[Python Script<br/>Agregação BU]
PY_PROD[Python Script<br/>Agregação Produto]
GCP_BUCKET_BU[(GCP Bucket<br/>BU)]
GCP_BUCKET_PROD[(GCP Bucket<br/>Produto)]
BQ_TRANSFER_BU[BigQuery Data Transfer<br/>07:00]
BQ_TRANSFER_PROD[BigQuery Data Transfer<br/>07:00]
BQ_AWS_BU[BigQuery<br/>aws_daily_bu]
BQ_AWS_PROD[BigQuery<br/>aws_daily_product]

COST_CAT --> PY_BU
COST_CAT --> PY_PROD
KUBECOST --> PY_PROD

GITHUB --> PY_BU
GITHUB --> PY_PROD

PY_BU --> GCP_BUCKET_BU
PY_PROD --> GCP_BUCKET_PROD

GCP_BUCKET_BU --> BQ_TRANSFER_BU
GCP_BUCKET_PROD --> BQ_TRANSFER_PROD

BQ_TRANSFER_BU --> BQ_AWS_BU
BQ_TRANSFER_PROD --> BQ_AWS_PROD

%% ======================
%% GCP – Dados Comuns
%% ======================
GCP[GCP Billing]
GCP_EXPORT[Billing Export<br/>Parquet Diário]
GCP_BUCKET[(GCP Bucket<br/>Billing)]
BQ_TRANSFER_GCP[BigQuery Data Transfer]
BQ_GCP_RAW[BigQuery<br/>gcp_daily]
BQ_GCP_VIEW[View<br/>gcp_daily_clean]

GCP --> GCP_EXPORT
GCP_EXPORT --> GCP_BUCKET
GCP_BUCKET --> BQ_TRANSFER_GCP
BQ_TRANSFER_GCP --> BQ_GCP_RAW
BQ_GCP_RAW --> BQ_GCP_VIEW

%% ======================
%% Consumo
%% ======================
LOOKER[Looker Dashboard<br/>FinOps]

BQ_AWS_VIEW --> LOOKER
BQ_AWS_BU --> LOOKER
BQ_AWS_PROD --> LOOKER
BQ_GCP_VIEW --> LOOKER
```


\