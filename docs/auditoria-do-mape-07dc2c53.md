<!-- title: Auditoria do MAPE | url: https://outline.seazone.com.br/doc/auditoria-do-mape-V2aEpmeVBe | area: Tecnologia -->

# Auditoria do MAPE

Projeto que visa tornar mais fácil o processo de auditoria do MAPE, disponibilizando tabelas com os dados necessários para análises profundas e superficiais em cima dos dados necessários para a identificação de problemas no MAPE de faturamento de imóveis.


## Arquitetura

O processamento e armazenamento de dados do MAPE ocorrem em GCP no projeto Data Resources e os dados são coletados do Data Lake e do Sirius em AWS.

O processo começa com um trigger diário no Cloud Scheduler que ativa a Cloud Run Function mape-audit. A function faz queries às fontes de dados necessárias na AWS por meio de credenciais AWS com permissão suficiente armazenadas no Secret Manager. A partir dos dados queriados, é feito uma série de processos de tratamento de dados até que eles estejam adequados para uso, momento em que são inseridos nas tabelas mape_history, mape_granularity_analysis e mape_ranked_properties do BQ.


 ![](/api/attachments.redirect?id=b40df842-d8e2-4d7f-940e-1e69e3fb01eb " =651x449")


## Tabelas

### mape_history

Tabela principal de auditoria. Contém os dados importantes para a análise do MAPE com a menor granularidade possível (diária). Ela é atualizada por meio de um esquema de "upsert", em que os dados de MAPE dos últimos 61 dias são inseridos no BQ de tal forma que, as linhas na tabela que já existem (airbnb_listing_id e date já existentes) são atualizadas (created_at continua o mesmo e as demais linhas são sobreescritas) e as linhas novas (airbnb_listing_id e date novos) são inseridas por completo. Para a realização do "upsert" é utilizado uma tabela axiliar "mape_history_temp".

Essa é a tabela base do processo de mape-audit e as demais tabelas são montadas a partir de dados contidos nela.

**Schema:**

| Coluna | Tipo | Descrição | Fonte |
|----|----|----|----|
| **airbnb_listing_id** | STRING(20) | ID Airbnb do imóvel | `"brlink_seazone_clean_data"."seazone_listings_historic"` |
| **id_seazone** | STRING(15) | ID Seazone do imóvel | `"brlink_seazone_clean_data"."seazone_listings_historic"` |
| **date** | DATE | Data alvo | `"datalake_observability"."listing_revenue_comparison"` |
| **actual_revenue** | FLOAT | Faturamento real do dia | `"datalake_observability"."listing_revenue_comparison"` |
| **estimated_revenue** | FLOAT | Faturamento previsto | `"datalake_observability"."listing_revenue_comparison"` |
| **price** | FLOAT | Preço scrapado da diária | `"brlink_seazone_enriched_data"."daily_fat"` |
| **error** | FLOAT | Valor do Erro do imóvel no dia | Criado na function |
| **blocked** | BOOLEAN | Bloqueio especulado | `"brlink_seazone_enriched_data"."daily_fat"` |
| **block_reason** | LIST(STRING) | Lista de razões de bloqueio | `"brlink_seazone_enriched_data"."daily_fat"` |
| **occupied** | BOOLEAN | Ocupação especulada | `"brlink_seazone_enriched_data"."daily_fat"` |
| **cleaning_fee** | FLOAT | Taxa de limpeza scrapada | `"brlink_seazone_enriched_data"."daily_fat"` |
| **price_source** | STRING(15) | Origem do preço (fill_price, correct_price) | `"brlink_seazone_enriched_data"."daily_fat"` |
| **strata** | STRING(10) | Strata do imóvel (TOP, MASTER, etc.) | `"sirius"."inputdata-kdatqapgmwx1"."setup_groups"` |
| **state** | STRING | Estado do imóvel | `"brlink_seazone_clean_data"."location"` |
| **city** | STRING | Cidade do imóvel | `"brlink_seazone_clean_data"."location"` |
| **listing_type** | STRING | Tipo do imóvel (apartamento, casa, etc.) | `"brlink_seazone_enriched_data"."details_last_aquisitiondetails"` |
| **number_of_bedrooms** | INTEGER | Número de quartos | `"brlink_seazone_enriched_data"."details_last_aquisitiondetails"` |
| **created_at** | TIMESTAMP | Data de criação do registro | Criado na function |
| **updated_at** | TIMESTAMP | Data de atualização do registro | Criado na function |
| **is_inf** | BOOLEAN | Se o erro é ou não infinito (não tem infinito na tipagem FLOAT do BQ, então é posto nulo em error e True em is_inf) | Criado na function |

**Particionamento:** updated_at (DAY)


### mape_granularity_analysis

Tabela de análise de granularidades. Ela contém o MAPE agrupado para as principais granularidades: state (Paraná, São Paulo, etc.), strata (SUP, TOP, etc.), period (7 dias, 15 dias, etc.) e number of bedrooms (0-1 bedrooms, 2-3 bedrooms, etc.). Com exceção da granularidade "period", os MAPEs são referentes ao MAPE de 15 dias.

Schema:

| Coluna | Tipo | Descrição |
|----|----|----|
| **mape_value** | FLOAT | MAPE para esta granularidade |
| **granularity_type** | STRING | Tipo de granularidade (state, strata, etc.) |
| **granularity_value** | STRING | Valor da granularidade (São Paulo, TOP, etc.) |
| **comparison_to_base_mape** | FLOAT | Comparação percentual com o MAPE global de 15 dias |
| **is_critical** | BOOLEAN | Se é uma granularidade crítica (atualmente a regra é **comparison_to_base_mape** >= 0.5) |
| **count_airbnb_id** | INTEGER | Contagem de IDs distintos usados para o MAPE da granularidade |
| **count_inf** | INTEGER | Contagem de infs na granularidade |
| **period_start** | DATE | Data inicial do período analisado |
| **period_end** | DATE | Data final do período analisado |
| **created_at** | TIMESTAMP | Data de criação do registro |

**Particionamento:** created_at (DAY)


### mape_ranked_properties

Tabela de ranqueamento de imóveis pelo valor do MAPE. Agrupa o MAPE de 15 dias por ID, ranqueia eles por MAPE e adiciona colunas de porcentagem do valor do MAPE por fator diferente.

Schema:

| Coluna | Tipo | Descrição |
|----|----|----|
| **airbnb_listing_id** | STRING | ID Airbnb do imóvel |
| **mape_value** | FLOAT | MAPE de 15 dias do imóvel |
| **impact_score** | INTEGER | Score de impacto no MAPE global (1 = imóvel de maior MAPE, 2 = segundo maior, etc.) |
| **estimated_revenue** | FLOAT | Faturamento previsto para o período de 15 dias |
| **actual_revenue** | FLOAT | Faturamento real para o período de 15 dias |
| **count_inf** | INTEGER | Contagem de diárias com erro infinito no período |
| **block_mape_ratio** | FLOAT | Parcela do erro atribuida à erros de bloqueio |
| **occupancy_mape_ratio** | FLOAT | Parcela do erro atribuida à erros de ocupação |
| **price_mape_ratio** | FLOAT | Parcela do erro atribuida à erros de preço |
| **main_factor** | STRING | Maior parcela do erro (block, occupancy ou price) |
| **is_inf** | BOOLEAN | Se o mape_value é ou não infinito (mesmo esquema de mape_history) |
| **created_at** | TIMESTAMP | Data de criação do registro |

**Particionamento:** created_at (DAY)


## Endereços importantes

* **Tabelas:** Todas estão na GCP, no projeto Data Resources, dentro de lake_observability no BQ.
* **Trigger da Cloud Function:** [link](https://console.cloud.google.com/cloudscheduler/jobs/edit/us-central1/lake-observability-mape-audit?authuser=1&project=data-resources-448418)
* **Cloud Function:** [link](https://console.cloud.google.com/run/detail/us-central1/lake-observability-mape-audit/source?authuser=1&project=data-resources-448418)
* **Código fonte da Cloud Function no GitHub:** [link](https://github.com/seazone-tech/gcp-data-resources/tree/main/cloud-functions)