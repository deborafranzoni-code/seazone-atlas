<!-- title: Documentação Técnica | url: https://outline.seazone.com.br/doc/documentacao-tecnica-Frk7AxgNkg | area: Tecnologia -->

# Documentação Técnica

## V**isão Geral da Solução**

A solução é uma **Cloud Function HTTP** (Functions Framework) que, ao ser executada:

**Extrai dados do Athena (AWS)**:

* Concorrentes categorizados (`competitors_output`)
* Concorrentes sem strata (`competitors_no_strata`)
* Série de preços por imóvel (`daily_revenue_competitors`)
* Categorias internas (Seazone) (`setup_groups`)

**Calcula métricas de saúde por categoria**, incluindo:

* Outliers de preço por categoria via IQR
* Frequência de incompatibilidade por imóvel e agregação por categoria
* Scores (quantidade, estratificação, frequência)
* Health score final e status (verde/amarelo/vermelho)

**Grava resultados no BigQuery** (tabelas "today" e "historic")

Para categorias críticas (**amarelo/vermelho**), gera **candidatos a concorrentes** por:

* Regras usando clusters do modelo (strata com prefixo `A_`) com expansão controlada
* Regras usando base `competitors_no_strata` com expansão controlada
* "Lookalike" por **similaridade vetorial** (cosine) filtrando por **climate_type**

**Consolida** todos os candidatos e grava no BigQuery.

## !) Variáveis de ambiente

* `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`: acesso ao Athena/S3 via boto3
* `PROJECT_ID`: projeto GCP para o BigQuery Client
* `INPUT_DATABASE`: database Athena com `setup_groups`
* `COMPETITORS_DATA`: database Athena com `competitors_*` e `daily_revenue_competitors`
* `WEBHOOK_URL`: webhook (Slack) para notificação de erro

## 2) Bibliotecas

* AWS: `boto3`, `awswrangler (wr)`
* Dados: `pandas`, `numpy`
* GCP: `google-cloud-bigquery`
* Runtime: `functions_framework`
* Observabilidade: `traceback`, `requests`

## 3) Fontes de dados (Athena)

### 3.1 `competitors_output` (state=current, alive, passed_the_filters)

Campos usados:

* `airbnb_listing_id`, `polygon`, `listing_type`, `strata`, `number_of_bedrooms`
* `mode`, `last_90_fat`, `acquisition_date`, `number_of_reviews`, `star_rating`

Separação feita no código:

* **ML**: `strata.startswith('A_')` → `df_competitors_clusters_ml`
* **Não-ML**: demais → `df_competitors_clusters`

### 3.2 `setup_groups` (internos)

Filtro:

* `group_type='Categoria'` e `state='current'`

Campos:

* `id_seazone`, `group_name AS categoria`

### 3.3 `daily_revenue_competitors` (preço)

Janela dinâmica:

* `data_inicio = hoje - 60 dias`
* `data_fim = hoje + 120 dias`

Filtro:

* `blocked=false`, `price>0`

Agregação:

* `AVG(price)` por imóvel e mês (`date_trunc('month', date)`)

### 3.4 `competitors_no_strata`

Mesma estrutura base (com strata podendo estar ausente / não confiável), usada na estratégia "sem_strata".

## 4) Construção das categorias

Para concorrentes **não-ML** (`df_competitors_clusters`), a categoria é construída como:

`categoria = polygon + "-" + listing_type + "-" + strata + "-" + number_of_bedrooms + "Q"`

Exemplo:\n`Florianopolis-UFSC-casa-TOP-4Q`

Essa string é usada como chave de:

* Contagem de concorrentes por categoria
* Cálculo de outliers e scores
* Seleção de categorias críticas
* Join com detalhes de imóveis e candidatos

## 5) Cálculo de saúde (pipeline)

### 5.1 Definição de categorias relevantes

* `concorrentes_por_categoria`: count de concorrentes por categoria
* `compensacao_por_categoria`: count de concorrentes onde `mode != "Automática"`
* `imoveis_por_categoria`: count de internos por categoria (`setup_groups`)
* `categorias_relevantes`: `inner join` entre concorrentes e internos (garante que a categoria existe nos dois universos)

### 5.2 Merge com pricing mensal

* Filtra concorrentes para `categorias_relevantes`
* Faz merge do pricing mensal com concorrentes filtrados
* Remove:
  * linhas sem `strata`
  * duplicados (ignorando a coluna `mode`)

### 5.3 Outliers por IQR (por categoria)

Funções:

* `calcular_iqr_por_categoria(df, 'preco_medio')`:
  * Q1, Q3, IQR
  * limites: `[max(0, Q1-1.5*IQR), Q3+1.5*IQR]`
* `marcar_outliers(df, iqr_info)`:
  * adiciona `preco_incompativel` boolean

### 5.4 Estratificação (outliers por categoria)

Agrega por `categoria`:

* `qtd_total_registros`
* `qtd_registros_outliers`
* `perc_preco_incompativel = outliers/total * 100`

### 5.5 Frequência de incompatibilidade por imóvel

Agrega por imóvel (e atributos de cluster):

* `qtd_meses_incompativeis = sum(preco_incompativel)`
* `n_meses = count(preco_medio)`
* `qtd_total_meses = min(n_meses, 7)` *(cap para não privilegiar séries muito longas)*
* `percentual_freq_incompatibilidade = qtd_meses_incompativeis / qtd_total_meses`

Resultado: `df_flags`

## 6) Persistência BigQuery (Saúde)

### Tabelas geradas


1. **Detalhamento de imóveis**

* `competitors.test_listings_health_details_today` (TRUNCATE)
* `competitors.test_listings_health_details_historic` (APPEND + particionada por `data_particao`)

Campos principais:

* id, strata, mode, listing_type, polygon, number_of_bedrooms
* qtd_meses_incompativeis, qtd_total_meses, percentual_freq_incompatibilidade
* categoria, data_particao


2. **Saúde por categoria**

* `competitors.test_competitors_health_score_today` (TRUNCATE)
* `competitors.test_competitors_health_score_historic` (APPEND + particionada por `data_particao`)

Campos principais:

* qtd_total_registros, qtd_registros_outliers, perc_preco_incompativel
* freq_incompatibilidade
* qtd_concorrentes, qtd_compensacao
* score_quantidade, score_estratificacao, score_frequencia
* health_score, status, data_particao


3. **Histórico diário de concorrentes**

* `competitors.daily_competitors` (TRUNCATE)

Campos principais: 

* airbnb_listing_id, date, price, available, occupied, blocked, acquisition_date

### Views geradas


1. **Saúde e diagnóstico dos clusters**

* `competitors.vw_health_clusters`: Consolida informações de saúde da categoria, métricas estatísticas de faturamento, dados individuais dos concorrentes e status de quarentena.

  \
  *Campos principais:*
  * categoria, health_score, status
  * score_quantidade, score_frequencia, score_estratificacao
  * qtd_concorrentes, qtd_compensacao, tipos_compensacao
  * airbnb_listing_id, strata, polygon, mode
  * percentual_freq_incompatibilidade
  * origem, potencial, last_90_fat, url
  * star_rating, number_of_reviews
  * month_fat, median_fat, avg_fat, p60_fat, std_fat
  * avg_daily_category
  * current_month_fat, daily_price, occupancy_rate
  * em_quarentena, inativado_meta, status_quarentena, regras_quarentena

  \


2. Detalhamento diário de concorrentes:

* `competitors.vw_competitors_category_daily`: Fornece o histórico diário de preço e disponibilidade dos concorrentes por categoria.

  \
  *Campos principais:*
* airbnb_listing_id, categoria, date
* price
* available, occupied, blocked
* status
* acquisition_date

### 6.1 Cálculo de scores e status

* `score_quantidade`:
  * usa quantil 0.95 de `qtd_concorrentes` como máximo
  * `clip` e normalização
* `score_estratificacao = 1 - perc_preco_incompativel/100`
* `score_frequencia = 1 - freq_incompatibilidade`

`health_score = 0.3*quantidade + 0.4*estratificacao + 0.3*frequencia`

Status:

* `verde` se `health_score >= 0.7`, senão `amarelo`
* Regra crítica:
  * se `qtd_concorrentes < 7` → `vermelho` e `health_score = 0`

Categorias críticas:

* `categorias_criticas = status in ('amarelo','vermelho')`

## 7) Geração de candidatos a concorrentes (categorias críticas)

O pipeline monta uma tabela final `competitors.test_competitors_candidates` (TRUNCATE) com colunas:

* `airbnb_listing_id`, `url`, `mode`, `strata`, `listing_type`, `number_of_bedrooms`, `polygon`
* `number_of_reviews`, `last_90_fat`, `star_rating`
* `categoria`, `data`, `potencial`, `origem`

### 7.1 Estratégia 1 — Machine Learning (strata `A_`)

Base: `df_competitors_clusters_ml`

Objetivo: para cada categoria crítica, sugerir IDs que:

* pertençam ao mesmo contexto geográfico/estrutural
* mas diferenciem-se do par (listing_type + strata) do anchor

Expansão controlada (em cascata) até atingir `MIN_CANDIDATOS_POR_CATEGORIA`:


1. **Exato**: mesmo `polygon` e mesmos `quartos`
2. **Expandido quartos**: mesmo `polygon`, `quartos` em `q-1,q,q+1`
3. **Expandido polígono**: "vizinhos" por similaridade textual (macro prefixo) com `quartos` exatos
4. **Expandido quartos + polígono**: vizinhos + quartos adjacentes

A origem vira:

* `machine_learning`
* `machine_learning_expandido_quartos`
* `machine_learning_expandido_poligono`
* `machine_learning_expandido_quartos_poligono`

*(dedup por* `*airbnb_listing_id*` *para evitar repetição)*

### 7.2 Estratégia 2 — Sem strata

Base: `competitors_data_no_strata`

Mesmo algoritmo de expansão, porém sem usar `strata_anchor` como critério (somente difere por `listing_type`).

Origens:

* `sem_strata`
* `sem_strata_expandido_quartos`
* `sem_strata_expandido_poligono`
* `sem_strata_expandido_quartos_poligono`

### 7.3 Estratégia 3 — Similaridade ("Lookalike")

Objetivo: sugerir candidatos com perfil semelhante ao anchor, usando features derivadas de:

* preços mensais (média, desvio, min, max, contagem de meses)
* `last_90_fat` (log)
* normalizações por categoria e polígono
* reputação: combinação normalizada de `star_rating` e `number_of_reviews`

#### 7.3.1 Enriquecimento com clima

* Lê parquet no S3:
  * `s3://.../inputs/min_stay_calendar/state=current/`
* Constrói `polygon_climate` = mapa 1:1 de `polygon -> climate_type` via moda:
  * `df_min_stay` + `setup_groups` (join por `id_seazone`)
  * extrai polygon da categoria interna (`extract_polygon_from_categoria`)
* Merge do clima nos concorrentes: `df_competitors_with_climate`

**Compatibilidade necessária do pipeline**:

* se a coluna `season` não existir em `df_competitors_with_climate`, o código cria:
  * `df_competitors_with_climate["season"] = None`\n(para manter o contrato da função `build_lookalike_features`)

#### 7.3.2 Criação de features e matching

* `build_lookalike_features(...)`:
  * agrega por `airbnb_listing_id`
  * cria features e versões normalizadas (z-score)
* `compute_lookalike_candidates_with_climate(...)`:
  * define anchors = imóveis cuja `categoria` está em `categorias_criticas`
  * filtra pool por `climate_type` igual ao do anchor
  * calcula similaridade (cosine) após normalização L2
  * seleciona top_k com score >= `min_score`
  * retorna pares (anchor, candidate, similarity_score)

Resultado final gravado com:

* `origem = "similaridade"`
* `categoria = anchor_categoria` (categoria crítica que motivou o candidato)


---

## 8) Consolidação final e classificação de potencial

Consolidação:

* concatena `df_resultado` (ML), `df_resultado_sem_strata` e `df_lookalike_final` (similaridade)

Tratamentos finais:

* `strata` null → `"Não Estratificado"`
* `data = hoje`
* `star_rating`, `number_of_reviews` null → 0
* `classificar_potencial`:
  * calcula quantis 0.7 e 0.4 para `star_rating` e `number_of_reviews`
  * atribui:
    * **A**: >= q70 em ambos
    * **B**: >= q40 em ambos
    * **C**: demais ou nulos

Grava em:

* `competitors.test_competitors_candidates` (TRUNCATE)


---

## 9) Tratamento de erros e observabilidade

* O `main` está envolvido em `try/except`.
* Em erro, envia mensagem para `WEBHOOK_URL` com:
  * mensagem do erro
  * traceback completo em bloco de código
* Retorna HTTP 500 com `str(e)`.


## 10) Melhorias futuras

* Expandir o lookalike para bases adicionais, por exemplo, em 'competitors_no_strata'. Aplicando a lógica de similaridade também para imóveis sem strata, podem criar uma origem do tipo 'similaridade_sem_strata'.
* Aprender clima e/ou sazonalidade a partir dos dados: criar "perfis sazonais" aprendidos do histórico (ex.: séries mensais de preço/ocupação), e usar esse perfil como filtro/feature no lookalike.
* Testar outros modelos de lookalike: Similaridade com **ponderação por importância** (pesos ajustáveis por feature) e melhorar features.