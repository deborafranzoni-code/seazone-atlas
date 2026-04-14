<!-- title: APIs consultáveis na AWS e GCP relacionadas a dados de concorrentes | url: https://outline.seazone.com.br/doc/apis-consultaveis-na-aws-e-gcp-relacionadas-a-dados-de-concorrentes-RTLmAhOWbj | area: Tecnologia -->

# 🔎 APIs consultáveis na AWS e GCP relacionadas a dados de concorrentes

Foi feito um mapeamento das APIs relacionadas a concorrentes na AWS e na GCP que possuem uma estrutura que aponta que elas são disponíveis para consumo. Todas as APIs listadas abaixo foram testadas.


---

## Legenda

| Classificação | Descrição |
|----|----|
| ✅ Consultável | Retorna dados diretamente |
| ⚠️ Legada | Descontinuada mas ainda ativa |
| 🔴 Sem dados ativos | API funcional mas sem dados para retornar |
| 🏘️ Concorrentes de precificação | Concorrentes selecionados para calcular metas e preços de cada imóvel |
| 🌐 Concorrentes de mercado | Todos os imóveis Airbnb da região — usados para análise de potencial e benchmarking |


---

## AWS — Autenticação

As APIs da AWS utilizam **API Key** no header da requisição:

```bash
-H "x-api-key: {api_key}"
```

As URLs e chaves de autenticação devem ser obtidas no **API Gateway** do console AWS. Estão omitidas neste documento por segurança.


---

## GCP — Autenticação

As APIs da GCP utilizam **Google Identity Token**, gerado via `gcloud`:

```bash
gcloud auth login
TOKEN=$(gcloud auth print-identity-token)
```

O token tem validade de **1 hora**. Se expirar, basta regerá-lo com `TOKEN=$(gcloud auth print-identity-token)`.

As URLs de cada Cloud Run devem ser obtidas no **GCP Console → Cloud Run → selecione a função → copie a URL** exibida no topo da página.


---

## APIs AWS

### 1. fat_predict

**Status:** ✅ Consultável | ⚠️ Legada | 🏘️ Concorrentes de precificação | ✔️ Testada e funcionando

**Descrição:** Consulta dados históricos de concorrentes no Athena (tabelas `competitors_output` e `monthly_fat`). Calcula previsão de preço, taxa de ocupação (TO) e faturamento (FAT) por categoria e percentil. Retorna também a lista individual de concorrentes com dados mensais.

**Parâmetros:**

| Parâmetro | Descrição |
|----|----|
| `polygon` | Nome do polígono/região |
| `type` | Tipo de imóvel (ex: apartamento) |
| `strata` | Estrato do imóvel (ex: JR) |
| `rooms` | Número de quartos |
| `percentile` | Percentil de referência (ex: 0.5) |

**Exemplo de chamada:**

```bash
curl -X POST "{base_url}/fat-prediction" \
  -H "Content-Type: application/json" \
  -H "x-api-key: {api_key}" \
  -d '{
    "polygon": "Aguas_Claras-Geral",
    "type": "apartamento",
    "strata": "JR",
    "rooms": 2,
    "percentile": 0.5
  }'
```


---

### 2. fat_goal — get-specific-date

**Status:** ✅ Consultável | ⚠️ Legada | 🏘️ Concorrentes de precificação | ✔️ Testada e funcionando

**Descrição:** Usa o imóvel como chave de entrada para identificar o grupo de concorrentes associado a ele. Retorna os dados dos concorrentes desse grupo comparando dois momentos no tempo: FAT, taxa de ocupação (TO) e dias bloqueados por concorrente (`airbnb_listing_id`). Acessa tabelas `seazone_data` e `daily_fat_goal` via Athena.

**Parâmetros:**

| Parâmetro | Descrição |
|----|----|
| `listing` | ID do imóvel |
| `month` | Ano e mês de referência no formato `YYYY-MM` (ex: 2025-07) |
| `start_date` | Data inicial (ex: 2025-07-01) |
| `end_date` | Data final (ex: 2025-07-30) |

**Exemplo de chamada:**

```bash
curl -X GET "{base_url}/fat-goal-audit/get_specific_date?listing={id_imovel}&month=2025-07&start_date=2025-07-01&end_date=2025-07-30" \
  -H "x-api-key: {api_key}"
```


---

### 3. fat_goal — diff

**Status:** ✅ Consultável | ⚠️ Legada | 🏘️ Concorrentes de precificação | ✔️ Testada e funcionando

**Descrição:** Retorna comparativo de métricas da meta (FAT real, FAT concorrente, nº de concorrentes, meta, imóveis bloqueados) entre duas datas para todos os imóveis de um mês. Útil para auditoria e análise de variação. Acessa tabelas `seazone_data` e `daily_fat_goal` via Athena.

**Parâmetros:**

| Parâmetro | Descrição |
|----|----|
| `month` | Ano e mês de referência no formato `YYYY-MM` (ex: 2025-07) |
| `start_date` | Data inicial (ex: 2025-07-01) |
| `end_date` | Data final (ex: 2025-07-30) |

**Exemplo de chamada:**

```bash
curl -X GET "{base_url}/fat-goal-audit/diff?month=2025-07&start_date=2025-07-01&end_date=2025-07-30" \
  -H "x-api-key: {api_key}"
```


---

### 4. competitors_by_user

**Status:** ✅ Consultável | ⚠️ Legada | 🔴 Sem dados ativos | ✔️ Testada

**Descrição:** Retorna a lista de imóveis (`id_seazone`) que usam precificação por concorrentes, filtrados pelo usuário responsável. Na prática retorna sempre `[]` — o campo `by_competitors` está `False` em todos os registros, tanto no estado atual quanto em registros históricos. O processo que populava esse campo provavelmente foi descontinuado junto com o restante do fluxo legado.

**Parâmetros:**

| Parâmetro | Descrição |
|----|----|
| `user` | E-mail ou identificador do usuário responsável |

**Exemplo de chamada:**

```bash
curl -X POST "{base_url}/pricing/competitors-by-user" \
  -H "Content-Type: application/json" \
  -H "x-api-key: {api_key}" \
  -d '{
    "user": "email@empresa.com"
  }'
```


---

### Observações gerais — AWS

* As APIs `fat_predict`, `fat_goal — get-specific-date` e `fat_goal — diff` são legadas — estão ativas mas descontinuadas, portanto devem ser utilizadas apenas para consulta e não recebem mais manutenção ativa.
* As APIs `fat_goal — get-specific-date` e `fat_goal — diff` utilizam método **GET via query string**.
* A API `fat_predict` utiliza método **POST com body JSON**.
* URLs e chaves de autenticação omitidas neste documento por segurança — consultar o **API Gateway** no console AWS.
* Em caso de retorno `HTTP 202 — No message`, a API está ativa mas sem dados na fila (não é erro).


---

## APIs GCP

### 5. get-meta-data

**Status:** ✅ Consultável | 🏘️ Concorrentes de precificação

**Descrição:** Endpoint GET que retorna dados de meta mensal ou trimestral do BigQuery. Por imóvel retorna: faturamento real, grupo de concorrentes, meta calculada (P25/P50/P75 dos concorrentes de precificação), resultado (bateu/não bateu), número de concorrentes e taxa de ocupação dos concorrentes. É a API mais direta para consulta de dados dos concorrentes de precificação no GCP.

**Parâmetros (use apenas um por chamada):**

| Parâmetro | Descrição |
|----|----|
| `month` | Mês de referência no formato `YYYY-MM` (ex: 2025-01) |
| `quarter` | Trimestre no formato `YYYY-QN` (ex: 2025-Q1) |
| `quarter_confirmed` | Trimestre confirmado no formato `YYYY-QN` (ex: 2025-Q1) |

**Exemplo de chamada:**

```bash
curl -s -H "Authorization: Bearer $TOKEN" \
  "https://get-meta-data-352882589845.us-central1.run.app?month=2025-01"
```


---

### 6. dados-imoveis-airbnb

**Status:** ✅ Consultável | 🌐 Concorrentes de mercado | ✔️ Testada e funcionando

**Descrição:** Retorna o faturamento médio anual do bairro (`fat_bairro`) e o faturamento mediano P50 dos concorrentes Airbnb para o tipo e número de quartos informados (`predict`). Consulta os últimos 12 meses, filtrando imóveis com nota ≥ 4.5 e ≥ 5 avaliações. Requer no mínimo 12 meses de dados disponíveis para o bairro e para a combinação de tipo e quartos informados.

**Parâmetros:**

| Parâmetro | Descrição |
|----|----|
| `estado` | Nome do estado (ex: Santa Catarina) |
| `cidade` | Nome da cidade (ex: Florianópolis) |
| `bairro` | Nome do bairro (ex: Jurerê) |
| `tipo` | Tipo do imóvel: `apartamento`, `casa` ou `hotel` |
| `quartos` | Número de quartos (inteiro) |

**Exemplo de chamada:**

```bash
curl -s -X POST "{base_url}" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "estado": "Santa Catarina",
    "cidade": "Florianópolis",
    "bairro": "Jurerê",
    "tipo": "apartamento",
    "quartos": 2
  }'
```


---

### 7. api-fat-lovable

**Status:** ✅ Consultável | 🌐 Concorrentes de mercado | ✔️ Testada e funcionando

**Descrição:** Retorna análise de mercado Airbnb com percentis de faturamento anual (P25/P50/P75), taxa de ocupação média, ADR (diária média) e pontos georreferenciados para mapa. Cruza dados de concorrentes do mercado com dados internos da Seazone (bloco `seazoneStats`). Requer no mínimo 10 imóveis para retornar resultado — se insuficiente, retorna `INSUFFICIENT_DATA`.

**Parâmetros:**

| Parâmetro | Descrição |
|----|----|
| `state` | Nome do estado (ex: Santa Catarina) |
| `city` | Nome da cidade (ex: Florianópolis) |
| `suburb` | Lista de bairros (ex: `["Jurerê", "Canasvieiras"]`) |
| `type` | Tipo do imóvel (ex: apartamento) |
| `bedrooms` | Número de quartos (inteiro) |

**Exemplo de chamada:**

```bash
curl -s -X POST "{base_url}" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "state": "Santa Catarina",
    "city": "Florianópolis",
    "suburb": ["Jurerê"],
    "type": "apartamento",
    "bedrooms": 2
  }'
```


---

### 8. api-analise-fat-lovable → /competitors_analysis

**Status:** ✅ Consultável | 🌐 Concorrentes de mercado | ✔️ Testada e funcionando

**Descrição:** Retorna análise detalhada de concorrentes Airbnb por localização e período. Para cada imóvel retorna faturamento, ocupação e ADR mês a mês em colunas separadas por período (ex: `fat_2024_1`, `occ_2024_1`, `adr_2024_1`), totais anuais e uma flag indicando se o imóvel pertence à Seazone. Aceita siglas de estado (ex: `SC`) ou nome completo.

**Parâmetros:**

| Parâmetro | Descrição |
|----|----|
| `state` | Sigla (ex: `SC`) ou nome completo do estado |
| `city` | Nome da cidade |
| `suburb` | Bairros separados por vírgula (ex: `"Jurerê,Canasvieiras"`) |
| `year` | Ano (ex: `"2024"`) ou `"12 últimos meses"` |

**Exemplo de chamada:**

```bash
curl -s -X POST "https://us-central1-data-resources-448418.cloudfunctions.net/api_analise_fat_lovable" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "state": "SC",
    "city": "Florianópolis",
    "suburb": "Jurerê,Canasvieiras",
    "year": "2024"
  }'
```

> ℹ️ `suburb` nesta API é uma **string** com vírgulas, diferente da `api-fat-lovable` que recebe uma lista.


---

### 9. analise-fat-api → /analyze_revenue

**Status:** ✅ Consultável | 🌐 Concorrentes de mercado | ✔️ Testada e funcionando

**Descrição:** A mais completa para análise granular de mercado. Executa 4 consultas em paralelo e retorna: análise anual com percentis P25/P50/P75 de faturamento, taxa de ocupação e ADR; séries mensais; dados dos últimos 12 meses; e lista de imóveis individuais com coordenadas geográficas, URL do Airbnb e classificação de performance (alta/média/baixa).

**Parâmetros:**

| Parâmetro | Descrição |
|----|----|
| `state` | Sigla do estado (ex: `SC`) |
| `city` | Nome da cidade |
| `neighborhood` | Nome do bairro (pode ser vazio) |
| `year` | Ano de análise (inteiro, ex: `2024`) |
| `category` | Faixa de quartos: `1_room`, `2_room`, `3_room`, `4+_room` |
| `listing_type` | Tipo do imóvel: `apartamento`, `casa`, `hotel` ou `todos` |

**Exemplo de chamada:**

```bash
curl -s -X POST "{base_url}/analyze_revenue" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "state": "SC",
    "city": "Florianópolis",
    "neighborhood": "Jurerê",
    "year": 2024,
    "category": "2_room",
    "listing_type": "apartamento"
  }'
```

> ℹ️ O endpoint é `/analyze_revenue` — deve ser incluído ao final da URL base da Cloud Run.


---

### 10. backend-analise-faturamento-api → /api/revenue

**Status:** ✅ Consultável | 🌐 Concorrentes de mercado | ✔️ Testada e funcionando

**Descrição:** Retorna simulação de rentabilidade por localização, consultando dados de concorrentes Airbnb e dados internos da Seazone. Possui também o endpoint `/api/filters` que retorna as opções disponíveis de Estado, Cidade e Bairro — recomendado como primeiro passo para descobrir valores válidos antes de consultar o `/api/revenue`. Voltado para a ferramenta `analisefaturamento.seazone.com.br`.

**Parâmetros —** `**/api/revenue**` **(GET, query string):**

| Parâmetro | Descrição |
|----|----|
| `state` | Nome do estado (ex: Santa Catarina) |
| `city` | Nome da cidade |
| `type` | Tipo do imóvel (ex: apartamento) |
| `bedrooms` | Número de quartos (inteiro) |
| `suburb` | Bairro(s) — pode ser repetido para múltiplos |

**Exemplos de chamada:**

```bash
# Filtros disponíveis (sem parâmetros — bom ponto de partida):
curl -s -H "Authorization: Bearer $TOKEN" \
  "https://backend-analise-faturamento-api-352882589845.us-central1.run.app/api/filters"

# Simulação de rentabilidade:
curl -G -s -H "Authorization: Bearer $TOKEN" \
  --data-urlencode "state=Santa Catarina" \
  --data-urlencode "city=Florianópolis" \
  --data-urlencode "type=apartamento" \
  --data-urlencode "bedrooms=2" \
  --data-urlencode "suburb=Jurerê" \
  "https://backend-analise-faturamento-api-352882589845.us-central1.run.app/api/revenue"
```


---

### Observações gerais — GCP

* As APIs do **Grupo Concorrentes de precificação** dependem dos pipelines internos de seleção e cálculo de meta estarem atualizados — se esses processos não tiverem rodado recentemente, os dados podem estar desatualizados.
* As APIs do **Grupo Concorrentes de mercado** podem retornar erro se o bairro ou cidade informado tiver menos de 12 meses de dados ou menos de 10 imóveis disponíveis na base.
* A `backend-analise-faturamento-api` possui o endpoint `/api/filters` — recomendado como primeiro teste para confirmar que a autenticação está funcionando e para descobrir valores válidos de localização.