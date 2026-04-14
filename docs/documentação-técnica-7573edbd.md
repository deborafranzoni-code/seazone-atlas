<!-- title: Documentação Técnica | url: https://outline.seazone.com.br/doc/documentacao-tecnica-B0QQbQVNIE | area: Tecnologia -->

# Documentação Técnica

1. ### **Visão Geral**

   
   1. **Problema:** O time de Revenue Management (RM) identifica variações diárias no número de concorrentes ativos, mas não possui uma ferramenta para diagnosticar de forma rápida e automatizada a causa dessas mudanças.\n
   2. **Objetivo do projeto:** Implementar uma solução de diagnóstico que possibilite ao time de RM analisar e auditar a variação no número de concorrentes entre duas datas. O objetivo é transformar a investigação manual em um diagnóstico automatizado e instantâneo, respondendo de forma clara e rápida à pergunta: "Quais concorrentes mudaram de status e por quê?". Com isso espera-se reduzir o tempo de investigação, acelerar a resolução de problemas de dados e aumentar a confiança nas métricas de mercado.

      \
   3. **Solução:** Pipeline que obtém os dados de imóveis concorrentes, dada uma determinada data inicial e uma data final, permitindo diagnosticar a causa da variação e visualização dos dados através de um dashboard no Looker.

      \
2. ### **Arquitetura**

   
   1. **Função Cloud Run (GCP):** A função *calculate-competitors-category* reúne a lógica relacionada a ativação/inativação de concorrentes. Nela são feitas consultas em diferentes fontes de dados, sendo elas:

| Fonte | Tabela/Arquivo |
|----|----|
| Aws Athena | brlink_seazone_enriched_data.details_last_aquisitiondetails |
| Aws Athena | brlink_seazone_enriched_data.daily_fat |
| Aws Athena | brlink_seazone_enriched_data.monthly_fat |
| Aws Athena | brlink_seazone_clean_data.seazone_listings_historic |
| Aws Athena | {INPUT_DATABASE}.setup_groups |
| Aws Athena | {SAPRON_DATA}.listing_status |
| BigQuery | competitors.competitors_polygons |
| BigQuery | competitors.competitors_inactive |
| BigQuery | competitors.strata |
| PostgreSQL (via DB_CREDENTIALS) | listing |
| PostgreSQL (via DB_CREDENTIALS) | strata |
| PostgreSQL (via DB_CREDENTIALS) | manual_category |
| Google Cloud Storage (Parquet em gs://{BUCKET_OUTPUT}) | parameters_review/df.parquet<br> |
| Google Cloud Storage (Parquet em gs://{BUCKET_OUTPUT}) | parameters_min_fat/df.parquet |
| Google Cloud Storage (Parquet em gs://{BUCKET_OUTPUT}) | backup_polygons/df.parquet (colunas: polygon, polygon_backup) |
| Google Cloud Storage (Parquet em gs://{BUCKET_OUTPUT}) | gs://{bucket}/backup_categories/df.parquet (colunas: category, down_strata_up_room, up_strata_down_room, equivalence) |

   b. **Table functions:** Há table functions criadas no bigquery para que dada uma data inicial e uma data final escolhida, sejam obtidos os dados desejados.
   * ==competitors_kpis:== 
     * Table function criada no bigquery para que dada uma data inicial e uma data final seja possível obter dados para KPIS como: o número total de concorrentes na data inicial, o número total de concorrentes na data final, concorrentes ganhos no período, concorrentes perdidos no período e o resultado dessa variação, sendo possível identificar se foi uma variação positiva com mais imóveis ganhos do que perdidos, ou uma variação negativa, com mais imóveis perdidos do que ganhos.
   * ==competitors_changes:==
     * Table function criada no bigquery para que seja obtido um detalhamento de causa da variação para o imóvel e categoria. Ela classifica as mudanças (se foi uma perda ou um ganho) e aponta os motivos da mudança. Os motivos de mudança podem ser:

| Motivo de mudança | Detalhamento |
|----|----|
| **Passou nos filtros (reviews/fat)** | 'passed_the_filters' virou true. |
| **Mudou de categoria** | mesmo airbnb_listing_id trocou de 'category'. |
| **Falhou nos filtros (reviews/fat)** | passed_the_filters virou false. |
| **Ganhou categoria válida** | is_competitor virou true. |
| **Sem categoria válida** | is_competitor virou false. |
| **Morto** | is_dead virou true. |
| **Ativado por regra is_active** | mudança em is_active (quando passa a ser considerado ativo porque estava abaixo do limite 15 manuais). |
| **Desativado** **por regra is_active** | quando excede o limite (>15) de manuais e é forçado para inativo. |
| **Voltou a ficar vivo** | is_dead virou false. |


c. **Dashboard no Looker:** Foi estruturado um dashboard para que seja possível visualizar de forma intuitiva e detalhada os motivos das variações de mudança. Ele está dividido em três partes: 

* Visualização dos KPIS
* Tabela detalhada com os campos: Id, Categoria, Status Inicial, Status Final, Tipo de Mudança e Motivo da Mudança.
* Gráfico com a distribuição de motivos da mudança. 

d. **Scheduler Google Apps Script:** Gatilho para executar a função cloud run 1x ao dia e obter os dados atualizados de variação. Esse scheduler não existe na GCP mas existe na planilha de SETUP do ambiente de produção, e lá já está configurado para a cloud function na GCP ser executada diariamente por volta das 06h da manhã. Esse script pode ser atualizado mais de uma vez no dia, basta a pessoa clicar no botão de "Atualizar polígonos/backups" da aba Grupos da planilha de SETUP Groups.\n


3. ### Variáveis de Ambiente

As variáveis devem ser configuradas no ambiente GCP:

| Variável de Ambiente | Detalhamento |
|----|----|
| AWS_ACCESS_KEY_ID | Chave de acesso da AWS usada para autenticação. |
| AWS_SECRET_ACCESS_KEY | Senha/segredo associado ao AWS_ACCESS_KEY_ID. |
| PROJECT_ID | ID do projeto no Google Cloud Platform (ex: data-resources-448418). Usado pelo cliente BigQuery e outras libs GCP. |
| DB_CREDENTIALS | Credenciais do banco PostgreSQL (que guarda listing, strata e manual_category). |
| BUCKET_OUTPUT | Bucket no **Google Cloud Storage** onde ficam os parâmetros (parameters_review, parameters_min_fat) e backups (backup_polygons, backup_categories). |
| INPUT_DATABASE | Database do athena usado para leitura da tabela setup_groups |
| COMPETITORS_DATA | Nome do database do Athena onde as partições são registradas para outputs (competitors_output, competitors_no_strata). |
| SAPRON_DATA |  Nome do database Athena que contém a tabela listing_status. |
| BUCKET_COMPETITORS | bucket **S3** onde os outputs finais são gravados (competitors_output, competitors_no_strata, historic/current). |
| WEBHOOK_URL | Notificação de erros no Slack. |

### \n4. **Artefato de Saída**

Há duas tabelas que são geradas: a competitors_category (que possui dados 'current') e a competitors_category_historic (que armazena dados históricos). Ambas as tabelas possuem o mesmo schema.

Formato: parquet

Schema:

| Coluna  | Tipo |
|----|----|
| airbnb_listing_id | string |
| category | string |
| polygon | string |
| listing_type | string |
| strata | string |
| number_of_bedrooms | int64 |
| star_rating | float64 |
| last_90_fat | float64 |
| current_month_fat | float64 |
| alive | bool |
| superhost | bool |
| guest_favorite | bool |
| passed_the_filters | bool |
| category_backup | string |
| is_active | bool |
| is_competitor | bool |
| acquisition_date | timestamp |



5. ### Dependências

   Arquivo requirements.txt:

```javascript
functions-framework==3.*
pyarrow==12.*
pandas==2.0.0
psycopg2-binary==2.9.*
numpy==1.26.*
google-cloud-bigquery==3.27.*
google-cloud-bigquery-storage==2.32.*
awswrangler==3.1.*
fsspec==2024.12.*
gcsfs==2024.12.*
db-dtypes==1.4.*
requests==2.32.*
```



6. ### Monitoramento e Notificações:

* **Webhook (Slack):** Notificação de erros com traceback detalhado.
* **Logs GCP:** Execuções monitoradas pelo console do Cloud Run.