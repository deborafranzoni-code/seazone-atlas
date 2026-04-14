<!-- title: Documentação do Pipeline: Panorama MKT | url: https://outline.seazone.com.br/doc/documentacao-do-pipeline-panorama-mkt-MyVpDphJdf | area: Tecnologia -->

# Documentação do Pipeline: Panorama MKT

## 1. Visão Geral

* Este projeto consiste em um pipeline de dados (ETL e Machine Learning) projetado para processar, enriquecer, treinar modelos e gerar predições sobre o mercado de aluguel por temporada (ex: Airbnb).
* O objetivo final é fornecer dados históricos consolidados e predições de métricas chave (Faturamento, Ocupação, Diária Média) para diferentes cidades e estados.
* O pipeline utiliza **Google Cloud Platform (GCS, BigQuery)** para armazenamento e processamento, e **AWS Athena** para consulta de IDs ativos.

## 2. Arquitetura de Dados

* O fluxo de dados segue uma estrutura sequencial dividida em módulos.
* Os dados são armazenados no GCS (Google Cloud Storage) seguindo uma estrutura de diretórios particionada (Hive-style partitioning).

### Fluxo Simplificado

* **Dataprep / Faturamento_real**
  * (Upstream) Preparam os dados brutos e calculam os fatos reais.
* **Expand_ids**
  * Cruza os dados reais com a base total de IDs ativos para garantir que todos os imóveis (mesmo sem reservas no mês) existam na base histórica.
* **Treinamento**
  * Treina modelos de Machine Learning (CatBoost) usando os dados reais (`fato_real`) e detalhes do imóvel.
* **Predict**
  * Utiliza os modelos treinados para preencher lacunas (valores nulos) na base expandida (`full_fato`), gerando a base final de predições.

## 3. Detalhamento dos Módulos

### A. Dataprep & Faturamento_real

* **Função**
  * Responsáveis pela ingestão, limpeza inicial e cálculo das métricas reais (Faturamento, Dias Ocupados, etc.) a partir das fontes de dados brutas (ex: AirDNA, Pipe, Scrapers).
* **Saída Esperada**
  * Arquivos Parquet salvos no GCS sob o prefixo `splitversion/fato_real/`.

### B. Expand_ids

* Este módulo garante a completude da série histórica.
* **Objetivo**
  * Para cada cidade, identificar todos os `airbnb_listing_id` ativos (via AWS Athena) e cruzar com os dados de `fato_real`.
  * Se um imóvel estava ativo em um mês mas não teve faturamento (não existe no fato real), ele é criado com valores nulos/zerados para ser preenchido posteriormente.
* **Entrada**
  * `splitversion/fato_real/{state}/{city}/` (GCS)
  * Tabela de IDs ativos no AWS Athena.
* **Processamento**
  * Multithreading por cidade.
  * Verifica partições existentes para evitar reprocessamento desnecessário.
  * Gera range de datas de 2016 até o ano futuro.
* **Saída**
  * `splitversion/full_fato/{state}/{city}/year=YYYY/month=MM/data.parquet`

### C. Treinamento

* Módulo responsável por criar os modelos preditivos.
* **Objetivo**
  * Treinar modelos de regressão (CatBoost) para prever métricas de performance baseadas nas características do imóvel.
* **Entrada**
  * `splitversion/fato_real/{state}/{city}/` (Dados históricos reais).
  * `splitversion/details/{state}/{city}_details.parquet` (Características estáticas do imóvel: quartos, amenidades, etc.).
* **Targets (Alvos)**
  * `faturamento`
  * `avg_price`
  * `days_in_month`
  * `available_dates`
  * `blocked_dates`
  * `occupied_dates`
* **Processamento**
  * Otimização de memória (downcasting de tipos numéricos).
  * Treinamento iterativo por target (Multi-output logic via lista de modelos).
  * Suporte a GPU/CPU configurável.
* **Saída**
  * Modelo salvo: `splitversion/models/{state}/{city}_multi_output_catboost_model.joblib`.
  * Métricas de performance (RMSE, MAE, R2) salvas no **BigQuery** (`panorama_de_mercado.model_training_metrics`).

### D. Predict

* Módulo responsável pela inferência e preenchimento de dados.
* **Objetivo**
  * Ler a base expandida (`full_fato`), identificar registros com métricas faltantes (NaN) e utilizar o modelo treinado para estimar esses valores.
* **Entrada**
  * `splitversion/full_fato/` (Base com lacunas).
  * `splitversion/details/` (Detalhes para features).
  * Modelos `.joblib` salvos pelo módulo de Treinamento.
* **Processamento**
  * Lógica incremental: processa mês atual, próximos 12 meses e histórico faltante.
  * Marca registros preditos com a flag `is_predicted = 1`.
  * Merge incremental com predições já existentes para evitar sobrescrita total.
* **Saída**
  * `splitversion/predictions/{state}/{city}_predictions.parquet`.

## 4. Estrutura de Diretórios no GCS (Bucket: `panorama-marketing`)

* O projeto segue uma estrutura hierárquica baseada em `splitversion`:
* `splitversion/`
  * `fato_real/`
    * Dados reais processados (Input do Treinamento/Expand)
    * `{state}/{city}/*.parquet`
  * `full_fato/`
    * Dados expandidos com IDs ativos (Input do Predict)
    * `{state}/{city}/year={YYYY}/month={MM}/data.parquet`
  * `details/`
    * Características dos imóveis
    * `{state}/{city}_details.parquet`
  * `models/`
    * Modelos treinados (Joblib/Catboost)
    * `{state}/{city}_multi_output_catboost_model.joblib`
  * `predictions/`
    * Resultado final consolidado
    * `{state}/{city}_predictions.parquet`

## 5. Configuração e Dependências

### Variáveis de Ambiente (.env)

* Para executar os scripts, as seguintes variáveis são necessárias:
  * `gcp_credentials`
    * JSON contendo as credenciais da Service Account do Google Cloud.
  * `ATHENA_DATABASE`
    * Nome do banco de dados no AWS Athena (usado no `Expand_ids`).
  * `MAX_WORKERS`
    * Número de threads para processamento paralelo (Padrão: 4).
  * `USE_GPU`
    * (Opcional, no Treinamento) `true` ou `false`.
  * `CATBOOST_THREAD_COUNT`
    * (Opcional) Controle de threads do CatBoost.

### Planilha de Controle

* A lista de cidades e estados a serem processados é obtida dinamicamente de uma planilha Google Sheets:
  * Colunas obrigatórias:
    * `state`
    * `city`

    \

### Bibliotecas Principais

* `pandas`, `numpy`
  * Manipulação de dados.
* `google-cloud-storage`, `google-cloud-bigquery`
  * Integração GCP.
* `catboost`
  * Algoritmo de Machine Learning.
* `joblib`
  * Serialização de modelos e paralelismo.
* `awswrangler` / `boto3`
  * (Implícito no módulo `athena`) Integração AWS.
* `gspread`
  * Leitura da planilha de parâmetros.