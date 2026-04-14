<!-- title: Diagnóstico de Qualidade e Fortalecimento de Clusters de Concorrentes | url: https://outline.seazone.com.br/doc/diagnostico-de-qualidade-e-fortalecimento-de-clusters-de-concorrentes-f5RDUqVqlO | area: Tecnologia -->

# 📉 Diagnóstico de Qualidade e Fortalecimento de Clusters de Concorrentes

## **Objetivo Geral**

A solução tem como objetivo fornecer ao time de Revenue Management uma ferramenta robusta para diagnosticar a qualidade de clusters de concorrentes e reforçar automaticamente aqueles considerados fracos. O projeto entrega três principais funcionalidades:

* Cálculo e armazenamento do *Health Score* por cluster.
* Geração de flag para diagnósticos detalhados por imóvel.
* Identificação automática de candidatos a concorrentes para clusters críticos.

## **Funções presentes no projeto**

|   **Nome da função** | **O que a função realiza** |
|----|----|
| ## `get_competitors_data(session, client)`: | Extrai dados dos concorrentes atuais da tabela competitors_output no Athena.  **Campos retornados:*** airbnb_listing_id
* polygon
* listing_type
* strata
* number_of_bedrooms
* mode
* last_90_fat
* acquisition_date
* number_of_reviews
* star_rating  **Critérios de filtro na consulta:*** state = 'current'
* alive = true
* passed_the_filters = true |
| ## `get_internals_data(session, client)`: | Obtém dados de agrupamento dos imóveis internos da tabela setup_groups.  **Campos retornados:*** id_seazone
* categoria (formada por: polígono - tipo - strata - quartos)  **Critérios de filtro:*** group_type in ('Polígono', 'Quartos', 'Strata')
* state = 'current' |
| ## `get_pricing_data(session, client)`: | Obtém dados da tabela daily_revenue_competitors e calcula a média de preços por mês dos concorrentes.  **Período:** 60 dias anteriores até 120 dias à frente da data atual.  **Agrupamento:*** Por airbnb_listing_id e mês  **Filtragem:** * blocked = false
* price > 0 |
| ## `get_competitors_data_no_strata(session, client)`: | Obter dados dos concorrentes da tabela competitors_no_strata que estão vivos (alive = true) e possuem estado atual (state = 'current'), mas que ainda **não têm uma** strata. Ou seja, ainda não fazem parte de nenhum cluster oficial de concorrência com estratificação definida.  **Critérios de Filtro:*** state = 'current': garante que apenas os dados mais recentes sejam utilizados.
* alive = true: considera apenas imóveis ativos na plataforma.**Campos retornados:*** airbnb_listing_id
* polygon
* listing_type
* strata
* number_of_bedrooms
* mode
* last_90_fat
* acquisition_date
* number_of_reviews
* star_rating |
| ## `calcular_iqr_por_categoria(df, coluna_valor='preco_medio')`: | Calcula os quartis (Q1,Q3) e o intervalo interquartil (IQR) de preços para cada categoria.  **Output:*** categoria
* q1
* q3
* iqr
* limite_inferior
* limite_superior |
| ## `marcar_outliers(df, iqr_info)`: | Identificar se os preços de cada registro estão fora do intervalo IQR de sua categoria.  **Output:*** Coluna booleana preco_incompativel |
| ## `classificar(score):` | Classificar o cluster com base no health score.  **Regras:*** Score < 0.7 → "amarelo"
* Score >= 0.7 → "verde"
* Clusters com menos de 7 concorrentes são forçados como "vermelho". |
| ## `classificar_potencial(df):` | Atribuir nota de potencial (A,B,C) aos candidatos a concorrentes com base em star_rating e number_of_reviews.   **Regras:*** **Potencial A: >= 70º percentil**
* **Potencial B: >= 40º percentil**
* **Potencial C: abaixo disso ou valores nulos.** |

O script do projeto se encontra em: <https://console.cloud.google.com/run/detail/us-central1/health-status-clusters/source?cloudshell=true&hl=pt-br&inv=1&invt=Ab4kTw&project=data-resources-448418>

## **Tabelas Geradas**

### **competitors.competitors_health_score**

| Nome do campo | Tipo |
|----|----|
| `categoria` | `STRING` |
| `qtd_total_registros` | `INTEGER` |
| `qtd_registros_outliers` | `INTEGER` |
| `perc_preco_incompativel` | `FLOAT` |
| `freq_incompatibilidade` | `FLOAT` |
| `qtd_concorrentes` | `INTEGER` |
| `score_quantidade` | `FLOAT` |
| `score_frequencia` | `FLOAT` |
| `health_score` | `FLOAT` |
| `status` | `STRING` |
| `data_particao` | `DATETIME` |

### **competitors.listings_health_details**

| Nome do campo | Tipo |
|----|----|
| `airbnb_listing_id` | `STRING` |
| `strata` | `STRING` |
| `mode` | `STRING` |
| `listing_type` | `STRING` |
| `polygon` | `STRING` |
| `number_of_bedrooms` | `INTEGER` |
| `qtd_meses_incompativeis` | `INTEGER` |
| `qtd_total_meses` | `INTEGER` |
| `percentual_freq_incompatibilidade` | `FLOAT` |
| `categoria` | `STRING` |
| `data_particao` | `DATETIME` |


### **competitors.competitors_candidates**

| Nome do campo | Tipo |
|----|----|
| `airbnb_listing_id` | `STRING` |
| `url` | `STRING` |
| `mode` | `STRING` |
| `strata` | `STRING` |
| `listing_type` | `STRING` |
| `number_of_bedrooms` | `INTEGER` |
| `polygon` | `STRING` |
| `number_of_reviews` | `INTEGER` |
| `last_90_fat` | `FLOAT` |
| `star_rating` | `FLOAT` |
| `categoria` | `STRING` |
| `data` | `DATETIME` |
| `potencial` | `STRING` |


## **Funcionalidades e Regras de Negócio**

* **Health Score por Cluster**

  **Objetivo:**  identificar rapidamente os clusters mais problemáticos e priorizar ações de melhoria.

  \
  * **Health Score calculado por categoria no padrão:** Polígono-ListingType-Strata-QuartosQ.

    \
  * **Métricas consideradas:** 
    * Quantidade de concorrentes 
    * % de preços incompatíveis (outliers) 
    * Frequência de incompatibilidade dos imóveis

  \
  * **Scores são normalizados e ponderados:** 
    * 30% Score Quantidade - Quanto mais concorrentes, mais confiável é a análise da categoria, pois há mais dados para comparação. No entanto, esse valor é limitado ao percentil 95 para evitar que categorias com concorrentes em excesso tenham uma vantagem desproporcional sobre as demais.

      \
    * 40% Score Estratificação - A porcentagem de preços fora do padrão (outliers) indica inconsistência na estratificação. Este componente recebe o maior peso, pois é diretamente ligado à precisão da clusterização de imóveis.

      \
    * 30% Score Frequência de incompatibilidade - Mede com que frequência, ao longo dos meses, os preços de um imóvel estão fora dos limites definidos. Esse componente avalia a persistência do problema ao longo do tempo.

      \
    * A ponderação 0.3 / 0.4 / 0.3 foi escolhida para priorizar a **consistência de precificação (estratificação)**, sem negligenciar o **volume de dados disponíveis (quantidade)** e a **recorrência dos problemas (frequência)**. Esses três pilares fornecem uma visão robusta e equilibrada da saúde de uma categoria.
    * **Como cada score esta sendo calculado:** 

| Score | Cálculo |
|----|----|
| score_quantidade - \[0 a 1\] | Reflete se a categoria tem muitos concorrentes.`max_concorrentes = df_health['qtd_concorrentes'].quantile(0.95)``score_quantidade = qtd_concorrentes / max_concorrentes`  Se uma categoria tem mais concorrentes que 95% das outras, ela ainda recebe no máximo score 1.  Isso evita que categorias muito grandes distorçam a pontuação.  Porque mais concorrentes significa dados mais confiáveis. Mas categorias superpopulosas poderiam dominar o ranking, o uso do percentil 95 evita isso. |
| score_frequencia - \[0 a 1\] | Mede com que frequência os imóveis têm preços incompatíveis ao longo dos meses:`score_frequencia = 1 - freq_incompatibilidade`  freq_incompatibilidade => É um número entre 0 e 1 que representa a fração de meses em que o imóvel teve **preços fora do intervalo considerado compatível**, em relação ao total de meses observados.  Por exemplo, se os problemas acontecem só em 1 ou 2 meses dos 7 observados, o score é maior.  Isso ajuda a entender se o problema de preço fora do padrão é *pontual ou recorrente*. |
| score_estratificacao - \[0 a 1\] | Mede a compatibilidade de preços (quanto menos outliers, melhor):`score_estratificacao = 1 - (perc_preco_incompativel / 100)`  perc_preco_incompativel = % de registros da categoria com preço fora do intervalo IQR.  Quanto maior a % de preços compatíveis, maior o score.  Se os preços estão coerentes dentro da categoria, é sinal de que a estratificação (agrupamento de imóveis semelhantes) está funcionando bem. |

      \
  * **Classificação visual:** 
    * Verde: Score ≥ 0.7
    * Amarelo: Score < 0.7
    * Vermelho: <7 concorrentes ou score nulo

  \
  **Output:** Tabela competitors.competitors_health_score no BigQuery, particionada e clusterizada por data. 

  \
* **Diagnóstico Detalhado por Imóvel**

**Objetivo:**  Ver uma lista detalhada de imóveis com flag de problema para identificar e entender as causas da baixa qualidade do cluster.

* \
  * **Flags aplicadas por imóvel:**
    * preço_incompativel (fora do IQR por mês) 
    * Frequência de incompatibilidade (% de meses com preço fora do IQR) 

      \
  * **Regras de agrupamento para cálculo:**
    * No máximo 7 meses com a observação de preço por imóvel
    * Frequência = meses incompatíveis / meses totais 

\nOBS: **Cada imóvel está vinculado à sua categoria**

**Output:** Tabela competitors.listings_health_details, particionada e clusterizada por data.


* **Recrutamento de candidatos para clusters críticos**
* **Clusters amarelos/vermelhos são alvos de busca de concorrentes.**
  * **Dois grupos de candidatos:**
    * Com strata gerada pelo machine learning (strata começa com A_)
    * Sem strata atribuída (tabela competitors_no_strata)
  * **Filtros aplicados para considerar um imóvel candidato a concorrente:**
    * Mesmo polígono e número de quartos
    * listing_type e strata diferentes dos concorrentes atuais

      \
  * **Para cada candidato são exibidos:** airbnb_listing_id, url, mode, strata, listing_type, quartos, polygon, reviews, last_90_fat, star_rating, potencial
  * **O potencial é classificado:**
    * A: 70+ percentil em star_rating e número de reviews
    * B: 40–70%
    * C: abaixo de 40% ou dados ausentes

**Output:** Tabela competitors.competitors_candidates, sobrescrita a cada execução, sem armazenamento de dados.


## **Execução e Deploy**

* Script executado via Google Cloud Function (link)
* O script é executado diariamente às 8h através de um job no cloud scheduler
* Logs de erro são enviados via webhook para canal Slack (via variável WEBHOOK_URL).

## **Painel Visual**

O painel visual foi estruturado no looker: <https://lookerstudio.google.com/reporting/6de103de-51ad-40e1-ac2d-7327cebc169a/page/MpySF> 

O painel possui uma tabela de saúde e diagnóstico do cluster:

 ![](/api/attachments.redirect?id=b204017c-e65e-4b8d-ae2e-e7be78fdeb95 " =496.5x108")O painel possui uma tabela de detalhamento dos imóveis para uma ou mais categorias selecionadas:

 ![](/api/attachments.redirect?id=8b9f5206-2376-47ae-b989-57611b0ecff3 " =363.5x99")O painel possui uma tabela de possíveis candidatos a concorrentes para uma ou mais categorias selecionadas:

 ![](/api/attachments.redirect?id=6719fbf7-05cc-44c5-aefc-7ca84ad65075 " =493x118.5")O painel possui um gráfico mostrando a distribuição dos status para entender a quantidade de clusters saudáveis(verde), para atenção(amarelo) e críticos(vermelho):

 ![](/api/attachments.redirect?id=9bd398c2-dd39-4172-b544-fbfe4aeb0bdc " =127.5x101")