<!-- title: Telemetria dos Scrapers | url: https://outline.seazone.com.br/doc/telemetria-dos-scrapers-9YHg7AbiVa | area: Tecnologia -->

# Telemetria dos Scrapers

## Visão geral

A telemetria dos scrapers é um sistema de **logs estruturados** emitidos pelos workers de scraping durante sua execução. Esses logs capturam métricas operacionais — como quantidade de mensagens processadas, erros por tipo, listings mortos e retries — em formato JSON padronizado.

Cada scraper mantém contadores thread-safe que acumulam métricas ao longo de sua vida útil e emitem um log consolidado no momento do shutdown.


---

## Motivação

Antes da telemetria estruturada, diagnosticar problemas nos scrapers dependia de buscar logs textuais dispersos no CloudWatch. Isso tornava difícil responder perguntas básicas como:

* Quantas mensagens o scraper processou antes de parar?
* Qual a taxa de erro? Quais tipos de erro predominam?
* Existem listings problemáticos causando retries excessivos?

Com a telemetria estruturada, conseguimos:

* **Visibilidade operacional** — dashboards no Grafana mostram o estado de cada scraper em tempo real
* **Detecção rápida de problemas** — thresholds visuais no Grafana sinalizam taxa de erro, dead listings ou queda de throughput
* **Diagnóstico facilitado** — campos padronizados permitem filtrar e correlacionar eventos
* **Histórico comparável** — logs com schema estável permitem análise temporal


---

## Arquitetura e fluxo de dados

### Fluxo principal

```none
                                    ┌─────────────────────────────┐
                                    │        ECS Task             │
                                    │  ┌───────────────────────┐  │
┌──────────────┐                    │  │      Scraper          │  │
│  SQS Queue   │───── mensagens ───▶│  │     (worker)          │  │
│              │                    │  │         │              │  │
└──────────────┘                    │  │         ▼              │  │
                                    │  │  ScraperTelemetry      │  │
                                    │  │  (contadores em        │  │
┌──────────────┐                    │  │   memória, thread-safe)│  │
│  SQS Failure │◀── msg c/ retry ──│  │         │              │  │
│    Queue     │     esgotado       │  │         │              │  │
└──────────────┘                    │  └─────────┼──────────────┘  │
                                    └────────────┼────────────────┘
                                                 │
                                        SIGTERM / SIGINT
                                                 │
                                                 ▼
                                    ┌─────────────────────────────┐
                                    │  emit_scraper_telemetry()   │
                                    │  → serializa contadores     │
                                    │  → emite log JSON           │
                                    └────────────┬────────────────┘
                                                 │
                                                 ▼
                                    ┌─────────────────────────────┐
                                    │       CloudWatch Logs       │
                                    │  log group:                 │
                                    │  /ecs/pipe-airbnb-scraper-* │
                                    └────────────┬────────────────┘
                                                 │
                                      CloudWatch Logs Insights
                                      filter: type =
                                      "scraper_telemetry"
                                                 │
                                                 ▼
                                    ┌─────────────────────────────┐
                                    │          Grafana            │
                                    │  (dashboards + thresholds   │
                                    │   visuais)                  │
                                    └─────────────────────────────┘
```

### Etapas do fluxo


1. O scraper consome mensagens de uma fila SQS via `SQSConsumer`
2. A cada mensagem processada, os contadores do `ScraperTelemetry` são incrementados
3. Mensagens que esgotam retries são enviadas para a **SQS Failure Queue**
4. No **shutdown graceful** (SIGTERM/SIGINT), a função `emit_scraper_telemetry()` serializa os contadores em JSON e emite via logger
5. O log chega ao **CloudWatch Logs**
6. O **Grafana** consulta o CloudWatch via **Logs Insights**, filtrando pelo campo `type: "scraper_telemetry"`

### Componentes principais

| Componente | Arquivo | Responsabilidade |
|----|----|----|
| `ScraperTelemetry` | `scrapers_telemetry/telemetry.py` | Contadores thread-safe, serialização JSON |
| `SQSConsumer` | `sqs.py` | Consumo concorrente de filas SQS com retry e rate limiting |
| `signal_graceful_shutdown` | `util.py` | Captura sinais do sistema e aciona shutdown com emissão de telemetria |
| `emit_scraper_telemetry` | Definida em cada scraper | Função que chama `metrics.log(logger)` para emitir o log |


---

## Estrutura dos logs

Todos os logs de telemetria são objetos JSON com o campo obrigatório `"type": "scraper_telemetry"`. Este campo é usado como **tag de identificação** por sistemas externos (Grafana).

### Exemplo de log

```json
{
  "type": "scraper_telemetry",
  "scraper": "details_scraper",
  "task_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
  "uptime_seconds": 372.5,
  "total_received_messages": 146,
  "scraped_messages": 134,
  "dead_listings": 0,
  "total_errors": 12,
  "failure_queue_messages": 3,
  "errors_by_type": {
    "405": 7,
    "403": 2,
    "errors": 3
  },
  "top_problematic_ids": [
    {"id": "12345678", "attempts": 8},
    {"id": "87654321", "attempts": 5}
  ]
}
```

### Campos

| Campo | Tipo | Descrição |
|----|----|----|
| `type` | string | Sempre `"scraper_telemetry"`. Tag obrigatória para identificação. |
| `scraper` | string | Nome do scraper (ex: `"details_scraper"`, `"reviews_scraper"`) |
| `task_id` | string (UUID) | Identificador único da execução do scraper |
| `uptime_seconds` | float | Tempo total de execução em segundos |
| `total_received_messages` | int | Total de mensagens recebidas da fila SQS |
| `scraped_messages` | int | Mensagens processadas com sucesso |
| `dead_listings` | int | Listings identificados como inativos/removidos |
| `total_errors` | int | Total acumulado de erros |
| `failure_queue_messages` | int | Mensagens enviadas para a fila de falha (após esgotar retries) |
| `errors_by_type` | object | Contagem de erros agrupados por tipo (ex: `"403"`, `"405"`, `"Timeout"`) |
| `top_problematic_ids` | array | Top 5 listings com mais retries |


---

## Dashboards no Grafana

Os logs de telemetria são consumidos pelo Grafana via **CloudWatch Logs Insights**. A tag `"scraper_telemetry"` no campo `type` é o filtro primário usado nas queries.

* **Datasource**: CloudWatch Logs
* **Log Group**: `/ecs/pipe-airbnb-scraper-details` (conta `452791833956`, região `us-west-2`)
* **Query Language**: CloudWatch Logs Insights (CWLI)

### Exemplo de query CloudWatch Insights

```
fields @timestamp, scraper, scraped_messages, total_errors, uptime_seconds
| filter type = "scraper_telemetry"
| sort @timestamp desc
| limit 50
```

### Dashboard: Scraper Details

O dashboard principal de telemetria está organizado em 4 seções com 13 painéis de dados.

#### Overview

| Painel | Tipo | O que mostra |
|----|----|----|
| Average Success Rate | gauge | `scraped_messages / total_received_messages * 100`. Thresholds: <60% vermelho, 60-70% amarelo, 70-85% amarelo, ≥85% verde |
| Total Instances | stat | Quantidade distinta de `task_id` (scrapers executados) |
| Total Received | stat | Soma de `total_received_messages` de todas as instâncias |
| Total Scraped | stat | Soma de `scraped_messages` de todas as instâncias |
| Total Errors | stat | Soma de `total_errors`. Thresholds: 0 verde, ≥10 amarelo, ≥50 vermelho |

#### Throughput & Performance

| Painel | Tipo | O que mostra |
|----|----|----|
| Throughput Over Time | timeseries | Received vs Scraped agrupados em bins de 5 minutos |
| Success Rate by Scraper (%) | barchart | Taxa de sucesso por scraper. Thresholds: <60% vermelho, 60-70% laranja, 70-85% amarelo, ≥85% verde |
| Scraper Uptime | stat | Uptime convertido em minutos (mín/méd/máx). Thresholds: <2min vermelho, 2-3min amarelo, 3-5min laranja, ≥5min verde |
| Processing Rate by Scraper (msg/min) | barchart | `scraped_messages / (uptime_seconds / 60)` por scraper. Threshold ideal: ≥35 msg/min |

#### Errors & Failures

| Painel | Tipo | O que mostra |
|----|----|----|
| Error Trend Over Time | barchart | Total de erros agrupados em bins de 10 minutos |
| Error Distribution | piechart | Distribuição de erros por tipo (extraídos do campo `errors_by_type`) |
| Error Rate by Scraper (%) | barchart | `total_errors / total_received_messages * 100` por scraper |

#### Data Quality & Health

| Painel | Tipo | O que mostra |
|----|----|----|
| Dead Listings by Scraper | barchart | Dead listings agrupados por scraper em bins de 5 minutos |
| Message Loss | bargauge | `failure_queue_messages` — mostra total, máximo, média e mínimo de mensagens perdidas |
| Scraper Health Summary | table | Tabela consolidada com todas as métricas por scraper: success rate, erros, dead listings, uptime |

### Métricas calculadas

| Métrica | Fórmula | Unidade |
|----|----|----|
| Taxa de sucesso | `scraped_messages / total_received_messages * 100` | % |
| Taxa de erro | `total_errors / total_received_messages * 100` | % |
| Throughput | `scraped_messages / (uptime_seconds / 60)` | msg/min |
| Dead listings | `dead_listings` (tendência ao longo do tempo) | contagem |
| Distribuição de erros | extraída do campo JSON `errors_by_type` | contagem por tipo |
| Message loss | `failure_queue_messages` | contagem |

### Thresholds visuais

Os dashboards utilizam thresholds visuais (cores) para sinalizar problemas. Não há alertas automáticos configurados — os thresholds servem como indicadores visuais:

| Métrica | Verde | Amarelo/Laranja | Vermelho |
|----|----|----|----|
| Success Rate | ≥85% | 60-85% | <60% |
| Total Errors | 0 | ≥10 | ≥50 |
| Uptime | ≥5 min | 2-5 min | <2 min |
| Error Rate | — | — | >50% |


---

## Guia de implementação para novos scrapers

### 1. Inicialize a telemetria no topo do módulo

```python
from scrapers_telemetry.telemetry import ScraperTelemetry

telemetry = ScraperTelemetry(scraper_name="meu_scraper")
```

### 2. Registre o shutdown graceful com emissão de telemetria

```python
from util import signal_graceful_shutdown

def emit_scraper_telemetry(metrics):
    metrics.log(log)

signal_graceful_shutdown(
    scraper,
    log=log,
    on_shutdown=lambda: emit_scraper_telemetry(telemetry)
)
```

Isso garante que, ao receber um sinal de término (SIGTERM/SIGINT), o scraper emita os contadores antes de encerrar.

### 3. Incremente os contadores nos pontos corretos

```python
# Ao receber uma mensagem da fila
telemetry.inc_received_message()

# Ao processar com sucesso
telemetry.inc_scraped_message()

# Ao detectar listing morto
telemetry.inc_dead_listing(listing_id)

# Ao encontrar um erro (categorize por tipo)
telemetry.inc_error("403")
telemetry.inc_error("Timeout")

# Ao enviar mensagem para fila de falha
telemetry.inc_failure_queue_message()

# Ao detectar retry
telemetry.inc_retry(listing_id, attempt_number)
```

### 4. Categorize erros de forma consistente

Use categorias de erro padronizadas para facilitar agregação no Grafana:

| Categoria | Quando usar |
|----|----|
| `"403"` | Forbidden — possível bloqueio de IP |
| `"405"` | Method Not Allowed |
| `"429"` | Too Many Requests — rate limiting |
| `"Timeout"` | Timeout na requisição |
| `"Nonetype"` | Resposta inesperada (campo ausente) |
| `"blocked"` | Bloqueio explícito pela plataforma |
| `"errors"` | Erros genéricos não categorizados |

### 5. Regras de estabilidade do schema

Os logs de telemetria são **consumidos por sistemas externos**. Para manter compatibilidade:

* **Não renomeie** campos existentes
* **Não altere** o tipo de campos (ex: numérico para string)
* **Não remova** campos existentes
* Novos campos devem ser **opcionais** (sistemas antigos devem continuar funcionando sem eles)


---