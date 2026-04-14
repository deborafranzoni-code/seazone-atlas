<!-- title: Documentação Técnica | url: https://outline.seazone.com.br/doc/documentacao-tecnica-T2v1HnwiTE | area: Tecnologia -->

# Documentação Técnica

# Resumo técnico do projeto

O projeto é uma aplicação **Streamlit** empacotada em Docker e executada como um serviço no **Cloud Run** que mostra um **mapa interativo** de polígonos (regiões) e destaca discrepâncias internas dentro de cada polígono, comparando **grupos** definidos pela junção de dois componentes: 

* Strata
* Número de Quartos 

==A aplicação oferece três "frentes de análise" (camadas), cada uma com uma métrica principal:==

* **Preço ofertado**: preço anunciado (por imóvel) agregado por grupo
* **Reservas**: valor reservado (por imóvel) agregado por grupo
* **Demanda**: volume de registros de reserva (por imóvel) agregado por grupo

*==OBS:==* ==Explicando mais detalhadamente a parte do 'agregado por grupo'==

Agregar aqui significa pegar **vários imóveis** que pertencem ao mesmo grupo e resumir eles em **um único número representativo.**

Exemplo prático (Preço Ofertado):

* Grupo: JR2Q
* Imóveis no grupo:
  * Imóvel A: avg_offered_price = 200
  * Imóvel B: avg_offered_price = 220
  * Imóvel C: avg_offered_price = 210
* Diante disso, a mediana desses valores (que nesse caso resulta em 210). Então: "O preço típico do grupo Standard 2Q nesse polígono é 210".
* Esse raciocínio também se aplica a Reservas (usa avg_reserved_fat) e Demanda (usa n_reservation_records).

  \

==Para cada polígono, é calculado:==

* **Referência do polígono** (média ponderada das medianas dos grupos)
* **Discrepância por grupo** (quanto cada grupo está acima/abaixo da referência)
* **Score do polígono** (um resumo numérico do "quão discrepante" o polígono é por dentro)
* **Grupo mais crítico** (o grupo com maior discrepância)

Além do mapa por polígono, existe um modo opcional de **análise por imóvel (pins)** dentro de um polígono selecionado, onde cada imóvel recebe cor por quantis e tooltip com comparações versus a referência do polígono.

# Tecnologias e componentes do sistema

**(A) Aplicação (Streamlit) em Cloud Run**

* Container Docker com a aplicação Python (`main.py`)
* Renderiza UI (sidebar, mapa, tabelas) e executa queries no BigQuery
* Usa cache para reduzir custo e melhorar performance

**(B) Pipeline de atualização de tabelas em BigQuery**

* Uma Cloud Run separada chamada: `**atualiza_tabelas_mapa_de_calor**`
* Responsável por atualizar diariamente as tabelas:
  * `location_latest`
  * `competitors_prices_window`

**(C) Agendamento (Cloud Scheduler)**

* Um Cloud Scheduler também chamado: `**atualiza_tabelas_mapa_de_calor**`
* Executa **1x por dia às 09h** (diariamente)
* Faz chamada HTTP para a Cloud Run de atualização (chama URL da cloud run)

# Arquitetura do projeto

### 3.1 Visão geral (fluxo de dados)


1. **Cloud Scheduler (09h diária)**\n↓ chama
2. **Cloud Run** `**atualiza_tabelas_mapa_de_calor**`\n↓ atualiza no
3. **BigQuery** (tabelas `location_latest` e `competitors_prices_window`)\n↓
4. **Cloud Run (Streamlit: Mapa de Calor)**\n↓ consulta BigQuery, calcula métricas e renderiza
5. **Usuário final (browser)** interage com mapa + filtros + tabelas

### 3.2 Por que essa arquitetura faz sentido?

* **Separar "atualização" do "app"** é saudável:
  * O app fica focado em exibir e calcular (rápido e estável)
  * A atualização roda como um job independente (mais controlável, com logs próprios)
* O **Scheduler** garante rotina diária sem depender de alguém rodar manualmente
* **BigQuery** vira a "fonte única" de dados processados para o app (consistência)


# Dependências /  Empacotamento (Docker + requirements) 

### 4.1 Dockerfile (conceito)

A imagem Docker:


1. Parte de uma base Python
2. Copia `requirements.txt` e instala dependências
3. Copia o código do app
4. Expõe a porta 8080 e roda Streamlit

**Por que Docker?**

* Garante que o ambiente do app em produção seja **igual** ao testado localmente
* Facilita deploy no Cloud Run (Cloud Run trabalha muito bem com containers)

### 4.2 requirements.txt (visão técnica das libs principais)

A aplicação usa principalmente:

* **Streamlit**: UI (sidebar, tabelas, controles)
* **PyDeck**: mapa/camadas
* **GeoPandas + Shapely + PyProj**: manipulação geográfica
* **Pandas + NumPy**: agregações e cálculo de métricas
* **google-cloud-bigquery** e **db-dtypes**: queries e tipos BigQuery → pandas
* **pyarrow**: performance de DataFrame e integração com BigQuery

> Observação prática: bibliotecas geográficas (GeoPandas/Shapely/Fiona/PyProj) costumam ser as mais "sensíveis" em container (dependem de libs do sistema). Por isso a versão e compatibilidade no Docker é importante.


# Bibliotecas utilizadas

### 5.1 Manipulação de texto / utilidades

* `re`\nUsado para limpar strings com regex (ex.: remover caracteres inválidos, múltiplos espaços/traços).
* `unicodedata`\nUsado para remover acentos e normalizar nomes (ex.: "São" → "Sao").
* `json`\nUsado para transformar GeoDataFrame em GeoJSON (`gdf.to_json()` → `json.loads(...)`) para passar ao PyDeck.
* `html`\nUsado para texto em tooltips HTML (evita quebrar HTML e melhora segurança/UI).
* `typing` (`Optional`, `Dict`, `Tuple`, `Any`)\nAjuda a documentar tipos de funções e deixar mais claro (entrada/saída).

### 5.2 Cálculo e dados tabulares

* `numpy as np`\nOperações vetorizadas, `np.where`, cálculo de percentis, etc.
* `pandas as pd`\nDataFrames, `merge`, `groupby`, limpeza de tipos, etc.

### 5.3 Geoespacial e visualização

* `geopandas as gpd`\nGeoDataFrame, CRS, áreas, centróides, spatial join, conversão para GeoJSON.
* `pydeck as pdk`\nRenderiza camadas (GeoJsonLayer e ScatterplotLayer) no mapa.
* `shapely.wkt as shapely_wkt`\nConverte geometria do BigQuery (WKT) em objetos geométricos (polígonos).

### 5.4 UI e app

* `streamlit as st`\nUI do app, cache, widgets, layout.

### 5.5 BigQuery

* `google.cloud.bigquery`\nCliente BigQuery e execução de queries.


# Fontes de dados e schemas

### 6.1 Visão geral: tabelas usadas na aplicação 


1. `competitors.competitors_polygons`
2. `mapa_de_calor_poligonos.location_latest`
3. `competitors.competitors_category`
4. `mapa_de_calor_poligonos.competitors_prices_window`
5. `competitors.polygons`

*OBS: Essas tabelas estão no Bigquery*

A Cloud Run de atualização (pipeline) atualiza especificamente:

* `location_latest`
* `competitors_prices_window`

*OBS: Essas são tabelas que vem da AWS* 

### 6.2 Schemas

#### 6.2.1 `competitors.competitors_polygons`

Query do app busca:

* `polygon` (STRING)
* `airbnb_listing_id` (STRING)

Uso no app:

* Faz a relação **imóvel → polígono**
* Serve para "saber quais imóveis pertencem a quais polígonos"

#### 6.2.2 `mapa_de_calor_poligonos.location_latest`

Campos usados:

* `airbnb_listing_id` (STRING)
* `state` (STRING)
* `city` (STRING)
* `suburb` (STRING)
* `latitude` (FLOAT64)
* `longitude` (FLOAT64)

Uso no app:

* Preencher filtros de **Estado/Cidade**
* Centralizar mapa
* Colocar pins (modo micro)

#### 6.2.3 `competitors.competitors_category` (latest por acquisition_date)

Campos usados:

* `airbnb_listing_id` (STRING)
* `polygon` (STRING)
* `strata` (STRING)
* `number_of_bedrooms` (FLOAT64 → convertido/round para Int)
* `alive` (BOOL)
* `passed_the_filters` (BOOL)
* `is_active` (BOOL)
* `last_90_fat` (FLOAT64)
* `current_month_fat` (FLOAT64)
* `acquisition_date` (usado para pegar o MAX)

Uso no app:

* Base "cadastro" do imóvel em grupos (strata/quartos)
* "flags" de qualidade (alive/passed/is_active)
* Métricas de faturamento (fat) para referência adicional

#### 6.2.4 `mapa_de_calor_poligonos.competitors_prices_window`

Campos usados:

* `airbnb_listing_id` (STRING)
* `n_price_records` (INT64)
* `avg_offered_price` (FLOAT64)
* `std_offered_price` (FLOAT64)
* `n_reservation_records` (INT64)
* `avg_reserved_fat` (FLOAT64)
* `std_reserved_fat` (FLOAT64)

Uso no app:

* Métrica principal de **Preço ofertado** e **Reservas**
* Métrica de **Demanda** deriva do volume de reservas (`n_reservation_records`)
* Também determina "qualidade" do imóvel (se tem amostra suficiente)

#### 6.2.5 `competitors.polygons`

Campos usados:

* `polygon` (STRING)
* `geometry` (GEOGRAPHY)

O app lê:

* `ST_AsText(geometry) AS wkt`

Uso no app:

* Render do mapa (polígonos)
* Cálculo de área/centróide e detecção de "expandidos"


# Estratégia de cache

O app usa dois tipos de cache do Streamlit:

### 7.1 `@st.cache_resource` (para o BigQuery client)

* Cria o `bigquery.Client` uma vez e reaproveita
* Bom porque criar cliente repetidas vezes é desnecessário

### 7.2 `@st.cache_data` (para dados e transformações)

* TTL de 24h: `CACHE_TTL_SECONDS = 24 * 3600`
* Aplica em:
  * queries ao BigQuery
  * funções de transformação (build_base, build_view, city map, etc.)

**Intuição do cache:**

* O app faz muitas agregações e merges pesados
* O usuário muda filtros (Estado/Cidade/Score) e isso pode reprocessar bastante
* Cache evita recalcular tudo o tempo todo e reduz custo de BigQuery

**Por que TTL 24h faz sentido aqui?**

* Porque existe uma atualização diária às 09h
* Então cache diário combina com "batch diário"
* Isso evita cenário em que o app "vive mudando" ao longo do dia de forma inesperada


# Lógica matemática do projeto

### 8.1 Conceitos principais

**Entidade base:** imóvel (`airbnb_listing_id`)\n**Polígono:** região (campo `polygon`)\n**Grupo dentro do polígono:** `(strata + number_of_bedrooms)`

Para cada polígono se busca responder:

=="Dentro desse polígono, os grupos estão **coerentes** entre si, ou tem grupo muito diferente do 'normal' do polígono?"==

Isso é útil porque:

* Se um grupo está muito acima/abaixo, pode indicar:
  * problema de precificação
  * problema de amostragem
  * mistura de sub-regiões
  * mudança real de mercado

### 8.2 Peso 1/k (evitar "imóvel contar duas vezes")

#### Problema

Um imóvel pode aparecer em **mais de um polígono** (por sobreposição, borda, etc.).\nSe você simplesmente contar ele inteiro em cada polígono, você **duplica influência** desse imóvel no sistema.

#### Solução usada

Para cada imóvel, calcule:

* `k = número de polígonos em que ele aparece`
* `listing_weight = 1 / k`

Então cada imóvel "distribui seu peso" entre polígonos.

#### Por que faz sentido?

Você preserva a contribuição total do imóvel como 1 (no conjunto), sem inflar.

#### Exemplo prático

* Imóvel A pertence a 2 polígonos (k=2)\n→ em cada polígono, ele vale 0,5
* Imóvel B pertence a 1 polígono (k=1)\n→ vale 1,0

Isso evita distorção quando muitos imóveis "duplicados" existirem.

### 8.3 Agregação por grupo: mediana por grupo

O app agrupa por:

* `polygon`
* `strata`
* `number_of_bedrooms`

E calcula, por exemplo no preço:

* `median_offered_price` (mediana do `avg_offered_price` dos imóveis do grupo)

#### Por que "mediana"?

A mediana é mais robusta que média quando há outliers.

#### Exemplo:

Imóveis de um grupo:

* 180
* 190
* 200
* 210
* 220
* 350

**Usando a média** → Soma = 1.350; Quantidade = 6; Resultado: 1350/6 = 225 

A média "puxa" para cima por causa de um único imóvel.

**Usando a mediana** → Com os valores ordenados, Resultado: (200 + 210) / 2 = 205

Muito mais próxima da realidade do grupo, é mais representativa.

### 8.4 Referência do polígono: média ponderada das medianas dos grupos

Depois de ter uma mediana por grupo, o app cria a **referência do polígono**.

#### Ideia

A referência é um "valor típico do polígono", levando em conta que grupos com mais imóveis devem pesar mais.

#### Modo de calcular

A referência do polígono é calculada somando, para cada grupo, o valor do grupo multiplicado pelo número de imóveis do grupo, e dividindo pela soma do número de imóveis de todos os grupos.

*Vg = valor do grupo. (ex.: mediana do preço do grupo)*

*Wg (ex.: n_listings que é a soma de listing_weight)*

*RefPolígono =* *Soma por cada grupo g (Wg \* Vg) / Soma de cada grupo g (Wg)*

#### Por que ponderar por `n_listings`?

Porque um grupo com muitos imóveis é mais representativo do polígono do que um grupo raríssimo.

#### Exemplo:

Polígono X:

* grupo A (JR2Q): valor da mediana de preço do grupo = 200, w (número de imóveis) = 50
* grupo B (TOP3Q): valor da mediana de preço do grupo = 800, w (número de imóveis) = 5

Referência:

(50\*200 + 5 \* 800) / (50 + 5) \~= 254,55

Sem ponderar, a média simples daria 500, o que seria enganoso (porque quase ninguém é TOP3Q).

### 8.5 Discrepância por grupo: comparação relativa com a referência

Depois, o app mede o quanto cada grupo difere da referência:

#### Modo de calcular

A discrepância de um grupo é calculada dividindo o valor do grupo pela referência do polígono e subtraindo 1. 

*Discrepância g = Vg / Refpolígono - 1*

* Se der **+0,20** → grupo está **20% acima**
* Se der **-0,10** → grupo está **10% abaixo**

#### Por que usar razão (divisão) e não diferença absoluta (subtração)?

Porque preço e fat variam de escala.

Exemplo:

* Diferença 50 reais
  * Em preço 200 → +25%
  * Em preço 1000 → +5%\nA discrepância relativa captura "impacto proporcional".

### 8.6 Discrepância mínima

O usuário escolhe no sidebar uma discrepância mínima (0 a 1).

O app marca um grupo como "anômalo" se o valor absoluto da discrepância de um determinado grupo for maior ou igual que a discrepância mínima. 

**Isso tem dois papéis:**


1. Filtrar polígonos para mostrar "só os relevantes"
2. Contar quantos grupos "discrepantes" existem (`n_anomalous_groups_*`)

Exemplo:

* discrepância mínima = 0,20
  * grupo +18% → não conta
  * grupo -25% → conta

### 8.7 Score do polígono: média ponderada da discrepância absoluta

O score resume: "o quão inconsistente esse polígono é por dentro".

O score do polígono é calculado somando, para cada grupo, o valor absoluto da discrepância do grupo multiplicado pelo número de imóveis do grupo, e dividindo pela soma do número de imóveis de todos os grupos.

* score 0: grupos alinhados com a referência
* score alto: muitos grupos muito diferentes do "normal"

#### Por que usar valor absoluto?

Porque tanto + quanto - são "desvios" do padrão.\nO score mede **tamanho da divergência**, não direção.

#### Exemplo prático

Polígono:

* Grupo A: discrepância +20%, peso 50
* Grupo B: discrepância -10%, peso 50

Score:

(50\*0,2 + 50 \* 0,1) / 50 + 50 = 0,15

### 8.8 Grupo mais crítico

O app pega o grupo com maior valor absoluto de discrepância no polígono e mostra no tooltip e na tabela:

* label (strata + quartos)
* discrepância formatada em %

Isso é importante porque o score sozinho é um resumo; o grupo crítico dá direção: "onde olhar primeiro".

# Deploy

Para fazer o deploy, foram adicionados os arquivos atualizados no ambiente do cloud shell, e em seguida foram dados os seguintes comandos:

1- Dar o build e push da imagem novamente (pois arquivos foram mudados):

```javascript
PROJECT=data-resources-448418
REGION=us-central1
REPO=mapa-calor-poligonos-repo
IMAGE=mapa-de-calor-poligonos
TAG="$REGION-docker.pkg.dev/$PROJECT/$REPO/$IMAGE:latest"

gcloud builds submit --tag "$TAG" --project "$PROJECT"
```

*OBS: Algo que é importante alterar é a tag para distinguir que versão será usado.*

2-  Deploy no Cloud Run:

```javascript
gcloud run deploy mapa-de-calor-poligonos \
  --region us-central1 \
  --project data-resources-448418 \
  --image us-central1-docker.pkg.dev/data-resources-448418/mapa-calor-poligonos-repo/mapa-de-calor-poligonos:latest \
  --platform managed \
  --service-account data-resources-function-sa@data-resources-448418.iam.gserviceaccount.com \
  --memory 2Gi \
  --cpu 2 \
  --timeout 300 \
  --no-allow-unauthenticated
```