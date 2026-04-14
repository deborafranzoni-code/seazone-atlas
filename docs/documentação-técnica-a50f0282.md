<!-- title: Documentação Técnica | url: https://outline.seazone.com.br/doc/documentacao-tecnica-j3oZ31kjD6 | area: Tecnologia -->

# 💻 Documentação Técnica

# **1. Visão Geral da Solução**

A solução consiste em um **pipeline analítico de dados** responsável por consolidar, tratar e disponibilizar informações de mercado para consumo no **BI para Apresentações Comerciais**. Executa diariamente às 5h (horário de Brasília).

## 1.1. Extração de dados do Athena (AWS)

A solução realiza a extração de dados a partir do **Athena**, utilizando bases analíticas consolidadas que descrevem tanto o desempenho operacional dos imóveis quanto suas características cadastrais e geográficas. São extraídas as seguintes informações:

* **Desempenho mensal de imóveis de curta temporada**, a partir da base `fato_block_occupancy`, incluindo métricas como faturamento, dias ocupados, dias bloqueados, diária média e taxa de ocupação.
* **Informações cadastrais dos listings**, obtidas da base `details_and_location_last_aquisition`, como tipo de imóvel, número de quartos e identificadores do imóvel.
* **Dados geográficos**, incluindo estado, cidade e bairro, utilizados para segmentação e agregações territoriais.
* **Informações de hosts**, com identificação do proprietário e cálculo da quantidade de listings por host, permitindo a classificação de hosts profissionais.
* **Amenities dos imóveis**, extraídas da base `details`, utilizadas para análises comparativas e construção de quebras de objeção (ex.: presença de piscina ou garagem).

  \

## 1.2. Processa e consolida métricas de mercado

* Faturamento médio, bruto e líquido;
* Taxa média de ocupação;
* Diária média;
* Quantidade total de listings ativos;
* Percentis de performance (P75 e P90);
* Métricas de crescimento e variação ao longo do tempo;
* Identificação de hosts profissionais (Pro Hosts).


## 1.3. Disponibiliza os dados no BigQuery

Os dados processados são disponibilizados no **BigQuery**, no projeto **data-resources**, dataset **Apresentacoes Comerciais**, para consumo direto pelo BI.


# 2. Variáveis de Ambiente

A solução depende de variáveis de ambiente para acesso às fontes de dados e ao ambiente de consumo analítico:

* `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`: acesso ao Athena/S3 via boto3
* `PROJECT_ID`: projeto GCP para o BigQuery Client


# 3. Bibliotecas

* AWS: `boto3`, `awswrangler (wr)`
* Dados: `pandas`, `numpy`, `re`
* GCP: `google.cloud.bigquery`, `google.auth.transport.requests`

  \

# 4. Fonte de Dados (Athena)

## 4.1. `fato_block_occupancy`

Base principal de **desempenho mensal** dos imóveis do airbnb. Campos utilizados:

`airbnb_listing_id`, `ano`, `mes`,`avg_price`,`faturamento`,`occupied_dates`,`blocked_dates`,`days_in_month`

## 4.2. `details_and_location_last_aquisition`

Base consolidada de **características e informações geográficas** dos listings.

`airbnb_listing_id`,`state`, `city`, `suburb`,`listing_type`,`number_of_bedrooms`

## 4.3. `details`

Base histórica utilizada para **contagem de listings por host** e para análise de amenities.

`airbnb_listing_id`, `owner_id`, `amenities`


# 5. Tabelas Geradas

O pipeline consolida e persiste os dados processados no **BigQuery**, no dataset `apresentacoes_comerciais`. As tabelas geradas são utilizadas diretamente pelo BI para suportar análises comerciais, rankings e visualizações temporais.

## 5.1. `apresentacoes_comerciais.monthly_metrics`

Tabela principal do BI, contendo métricas agregadas mensais por localização e tipologia do imóvel.

**Granularidade**

* Mensal
* Por: estado, cidade, bairro, tipo de imóvel e número de quartos.

**Campos principais**

* `data`: referência temporal (primeiro dia do mês);
* `state`, `city`, `suburb`: localização do imóvel;
* `listing_type`: tipo do imóvel;
* `number_of_bedrooms`: número de quartos;
* `sum_diaria`: soma das diárias médias;
* `sum_fat`: soma do faturamento mensal;
* `count_fat`: quantidade de imóveis com faturamento válido;
* `sum_occupied_dates`: total de diárias ocupadas;
* `sum_days_in_month`: total de dias disponíveis no período;
* `sum_blocked_dates`: total de datas bloqueadas;
* `total_listings`: número total de imóveis ativos;
* `total_hosts`: total de hosts distintos;
* `total_pro_hosts`: total de hosts profissionais.

**Métricas derivadas armazenadas**

* `top10_faturamento_city_real`;
* `top10_faturamento_suburb_real`;
* `p75_faturamento_city_real`;
* `p75_faturamento_suburb_real`;
* `p90_faturamento_city_real`;
* `p90_faturamento_suburb_real`.

## 5.2. `apresentacoes_comerciais.listing_monthly_fat`

Tabela em nível de imóvel, utilizada para análises detalhadas e cruzamento com amenities.

**Granularidade**

* Mensal.
* Por imóvel (`airbnb_listing_id`).

**Campos principais**

* `data`;
* `airbnb_listing_id`;
* `state`, `city`, `suburb`;
* `listing_type`;
* `number_of_bedrooms`;
* `avg_price`;
* `faturamento`;
* `taxa_ocupacao`;
* `owner_id`.


## 5.3. View: `vw_monthly_metrics`

View analítica utilizada para **padronizar dimensões**, **calcular métricas mensais agregadas** e **viabilizar comparações em 12 meses** no BI.

### 5.3.1. Principais transformações

* Discretização do número de quartos em faixas: `0-1 Quartos`, `2 Quartos`, `3 Quartos`, `4+ Quartos`
* Manutenção da granularidade mensal por: estado, cidade, bairro, tipo de imóvel e faixa de quartos.

### 5.3.2. Métricas calculadas

* **Total de listings (cidade):** soma de listings ativos no mês por cidade.
* **Total de listings (bairro):** soma de listings ativos no mês por bairro.
* **Diária média (cidade):** razão entre soma das diárias e quantidade de registros com faturamento.
* **Diária média (bairro):** mesma lógica aplicada ao nível de bairro.

  \

## 5.4. View: `vw_avg_top10_faturamento`

View responsável por **consolidar o faturamento médio dos Top 10% de studios** por cidade e bairro, garantindo que o valor agregado por cidade não seja duplicado na visualização.

### 5.4.1. Principais cálculos

* **Faturamento médio Top 10% (cidade):**\nMédia do `top10_faturamento_city_real` por: data, estado, cidade, tipo de imóvel e faixa de quartos.
* **Faturamento médio Top 10% (bairro):**\nMédia do `top10_faturamento_suburb_real` por: data, estado, cidade, bairro, tipo de imóvel e faixa de quartos.

### 5.4.2. Tratamento de duplicidade

* Utiliza `ROW_NUMBER()` para:
  * Exibir o valor agregado da **cidade apenas uma vez** por combinação de dimensões, evitando repetição do mesmo valor em múltiplos bairros.


\