<!-- title: API análise fat lovable | url: https://outline.seazone.com.br/doc/api-analise-fat-lovable-whivfDkRm9 | area: Tecnologia -->

# API análise fat lovable

# API Análise de Faturamento - Documentação Usuário

## Visão Geral

A API de Análise de Faturamento retorna dados unificados de imóveis listados no Airbnb para uma determinada região, incluindo faturamento bruto, taxa de ocupação e diária média — tudo mês a mês e com totais/médias do período.

**Base URL**

```
https://api-analise-fat-lovable-gateway-4i416kyd.uc.gateway.dev
```

**Endpoint**

```
POST /api_analise_fat_lovable
```


---

## Autenticação

Todas as requisições exigem uma API Key enviada no header:

| Header | Valor |
|----|----|
| `x-api-key` | Sua chave de API |


---

## Request

**Method:** `POST` **Content-Type:** `application/json` **Timeout recomendado:** 200 segundos

### Parâmetros (Body JSON)

| Campo | Tipo | Obrigatório | Descrição |
|----|----|----|----|
| `state` | string | Sim | Estado. Aceita sigla (`SC`) ou nome completo (`Santa Catarina`). |
| `city` | string | Sim | Nome da cidade (ex: `Florianópolis`). |
| `suburb` | string | Sim | Bairros separados por vírgula (ex: `Canasvieiras,Jurerê,Ingleses`). |
| `year` | string | Sim | Período da consulta. Valores aceitos: `12 últimos meses`, `2022`, `2023`, `2024`, `2025`. |

### Exemplo de Request

```json
{
  "state": "SC",
  "city": "Florianópolis",
  "suburb": "Canasvieiras,Jurerê,Ingleses",
  "year": "12 últimos meses"
}
```

```bash

curl -X POST \
  "https://api-analise-fat-lovable-gateway-4i416kyd.uc.gateway.dev/api_analise_fat_lovable" \
  -H "Content-Type: application/json" \
  -H "x-api-key: SUA_API_KEY" \
  -d '{
    "state": "SC",
    "city": "Florianópolis",
    "suburb": "Canasvieiras,Jurerê",
    "year": "12 últimos meses"
  }'
```


---

## Response

### Sucesso (200)

Retorna um objeto JSON com o total de listings e os dados no formato **pandas split**.

```json
{
  "total_listings": 1830,
  "data": {
    "columns": ["id_listing", "link_airbnb", "state", "city", "suburb", "..."],
    "data": [
      [12345, "https://www.airbnb.com.br/rooms/12345", "Santa Catarina", "Florianópolis", "Canasvieiras", "..."],
      ["..."]
    ]
  }
}
```

### Estrutura das Colunas

As colunas retornadas seguem a ordem abaixo. As colunas mensais usam o padrão `prefixo_ANO_MES` (ex: `fat_2025_3` para março de 2025).

**Dados do Imóvel**

| Coluna | Tipo | Descrição |
|----|----|----|
| `id_listing` | int | ID do anúncio no Airbnb |
| `link_airbnb` | string | Link direto para o anúncio |
| `state` | string | Estado do imóvel |
| `city` | string | Cidade do imóvel |
| `suburb` | string | Bairro do imóvel |
| `listing_type` | string | Tipo do anúncio (apartamento ou casa) |
| `number_of_bedrooms` | int | Quantidade de quartos |

**Faturamento Bruto (mensal + total)**

| Coluna | Tipo | Descrição |
|----|----|----|
| `fat_YYYY_M` | float | Faturamento bruto do mês (vazio se zero) |
| `fat_total` | float | Soma do faturamento no período selecionado |

**Taxa de Ocupação (mensal + média)**

| Coluna | Tipo | Descrição |
|----|----|----|
| `occ_YYYY_M` | float | Taxa de ocupação do mês (0 a 1, vazio se zero) |
| `occ_media` | float | Média da ocupação nos meses com dado (ignora meses zerados) |

**Diária Média (mensal + média)**

| Coluna | Tipo | Descrição |
|----|----|----|
| `adp_YYYY_M` | float | Diária média do mês (vazio se zero) |
| `adp_media` | float | Média da diária nos meses com dado (ignora meses zerados) |

**Informações Extras**

| Coluna | Tipo | Descrição |
|----|----|----|
| `id_seazone` | string | Se o imóvel é gerido pela Seazone (`Sim`/`Não`) |
| `latitude` | float | Latitude do imóvel |
| `longitude` | float | Longitude do imóvel |


---

## Erros

| Status | Cenário | Exemplo de resposta |
|----|----|----|
| 200 | Nenhum dado encontrado | `{"error": "Nenhum dado encontrado para os filtros informados."}` |
| 400 | Campos obrigatórios faltando | `{"error": "Campos obrigatórios faltando: state, city"}` |
| 405 | Método HTTP não permitido | `{"error": "Method not allowed"}` |
| 500 | Falha na query Athena | `{"error": "Athena query failed: ..."}` |
| 500 | Falha no processamento | `{"error": "Erro ao processar dados: ..."}` |


---

## Notas Importantes

**Normalização de texto:** tanto o input quanto os dados no banco são normalizados (sem acentos, minúsculo, apenas alfanuméricos) antes da comparação. Isso significa que `Jurerê`, `jurere` e `JURERÊ` são equivalentes.

**Siglas de estado:** o campo `state` aceita tanto a sigla (`SC`, `RJ`, `SP`) quanto o nome completo (`Santa Catarina`, `Rio de Janeiro`, `São Paulo`). A conversão é automática.

**Meses sem dado:** quando um imóvel não possui faturamento, ocupação ou diária em determinado mês, o valor retornado é uma string vazia (`""`) em vez de `0`. Isso facilita a diferenciação entre "não teve dado" e "valor foi zero".

**Período "12 últimos meses":** considera os 12 meses anteriores ao mês atual. Por exemplo, se a consulta é feita em março/2026, o período vai de março/2025 a fevereiro/2026.

**Reconstrução do DataFrame em Python:**

```python

import pandas as pd

result = response.json()
data = result["data"]
df = pd.DataFrame(data["data"], columns=data["columns"])
```


---

## Exemplo Completo em Python

```python

import requests

import pandas as pd

URL = "https://api-analise-fat-lovable-gateway-4i416kyd.uc.gateway.dev/api_analise_fat_lovable"

response = requests.post(
    URL,
    headers={
        "Content-Type": "application/json",
        "x-api-key": "SUA_API_KEY",
    },
    json={
        "state": "SC",
        "city": "Florianópolis",
        "suburb": "Canasvieiras,Jurerê,Ingleses",
        "year": "12 últimos meses",
    },
    timeout=200,
)

result = response.json()
data = result["data"]
df = pd.DataFrame(data["data"], columns=data["columns"])

print(f"Total: {result['total_listings']} listings")
print(df.head())
```