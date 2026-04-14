<!-- title: Scraper de Anúncios de Imóveis | url: https://outline.seazone.com.br/doc/scraper-de-anuncios-de-imoveis-syoChChV3e | area: Tecnologia -->

# Scraper de Anúncios de Imóveis

### Scraper de Anúncios de Imóveis da OLX

O scraper coleta dados de anúncios de imóveis publicados na OLX Brasil, extraindo informações como preço, localização, características do imóvel e metadados do anúncio. Opera via parsing de `__NEXT_DATA__` (Server-Side Rendering do Next.js), substituindo o scraper anterior que utilizava a API `nga.olx.com.br` (descontinuada).

#### Fonte dos Dados

Os dados são extraídos do JSON embutido na tag `<script id="__NEXT_DATA__">` presente em cada página de listagem da OLX. Esse JSON contém os mesmos dados que a página renderiza, incluindo a lista de anúncios, total de resultados e metadados de paginação.

**URL de exemplo:** `https://www.olx.com.br/imoveis/venda/estado-sp?o=1`

Para acessar o `__NEXT_DATA__`, basta abrir o código-fonte da página (Ctrl+U) e buscar por `__NEXT_DATA__`.

 ![Página de listagem da OLX com a estrutura do __NEXT_DATA__ em destaque](/api/attachments.redirect?id=9784c697-32b3-4476-9256-b824bef7dbbb)

#### Categorias Coletadas

| Código | Categoria | Tipo |
|----|----|----|
| 1001 | Venda | Residencial |
| 1002 | Aluguel | Residencial |
| 1080 | Temporada | Residencial |
| 1100 | Terrenos | Não-residencial |
| 1120 | Comércio e Indústria | Não-residencial |
| 1140 | Lançamentos | Residencial |

#### Arquitetura

```
Refiller (CLI)          Busca estados/regiões na API OLX
       │                Cria mensagens: estado × região × categoria
       ▼
  SQS Input Queue       FIFO, com deduplicação
       │
       ▼
  OlxScraper            N workers concorrentes (ECS Fargate)
   ├─ totalOfAds > 5700?
   │   SIM → subdivide query (quartos/banheiros/preço) e re-enqueue
   │   NÃO → pagina e coleta ads (dual-pass com retry)
       │
       ▼
  Kinesis Firehose       Cross-account via STS assume_role
       │
       ▼
  Data Lake RAW          Parquet no S3
```


1. **Refiller**: Consulta a API de filtros da OLX (`/api/filters/v1`) para obter a lista de estados e regiões disponíveis. Gera uma mensagem SQS para cada combinação `estado × região × categoria` (6 categorias), alimentando a fila de input.
2. **Scraper Principal**: Workers concorrentes consomem da fila SQS. Para cada mensagem, o scraper acessa a URL da listagem, extrai o `__NEXT_DATA__` e verifica o `totalOfAds`. Se exceder 5.700 (limite de paginação do OLX — 100 páginas × 57 ads), a query é subdividida e re-enfileirada. Caso contrário, pagina todas as páginas e coleta os anúncios.
3. **Envio ao Data Lake**: Os ads coletados são enviados em batches via Kinesis Firehose (cross-account) para o Data Lake RAW como arquivos Parquet.

#### Subdivisão Adaptativa

Quando uma query retorna mais de **5.700 ads**, o scraper subdivide automaticamente em sub-queries mais específicas e as re-enfileira na fila SQS. A estratégia varia por tipo de imóvel:

**Imóveis residenciais** (venda, aluguel, temporada, lançamentos):

| Depth | Estratégia | Branches |
|----|----|----|
| 0 | Quartos (0–5) | 6 |
| 1 | Banheiros (0–5) | 6 |
| 2 | Faixas de preço fixas | 6 |
| 3 | Subdivisão da faixa em 4 partes | 4 |
| 4–7 | Bisseção da faixa | 2 |
| 8 | Limite — coleta o que conseguir | — |

**Imóveis não-residenciais** (terrenos, comércio/indústria):

| Depth | Estratégia | Branches |
|----|----|----|
| 0 | Faixas de preço fixas | 6 |
| 1–2 | Subdivisão da faixa em 4 partes | 4 |
| 3–7 | Bisseção da faixa | 2 |
| 8 | Limite — coleta o que conseguir | — |

O objetivo é que cada sub-query retorne menos de 5.700 ads, garantindo que todos os anúncios sejam alcançáveis via paginação.

#### Resiliência de Paginação

O scraper implementa um mecanismo robusto de resiliência durante a paginação:

* **Checkpoint pattern**: mensagens SQS rastreiam `pending_pages` — se o worker falha no meio, a mensagem re-enfileirada contém apenas as páginas restantes
* **Dual-pass**: primeira tentativa em todas as páginas, segunda tentativa nas que falharam
* **Flush parcial**: ads coletados até o momento são enviados ao Firehose antes de re-enfileirar (evita perda de dados já coletados)
* **Retry com backoff**: erros 429/403 → retenta com delays progressivos (1s, 2s, 5s)
* **Rotação de IP**: recria a sessão HTTP após 5 erros consecutivos

#### Schema de Saída (RAW)

| Campo | Tipo | Exemplo | |-------|------|---------|| | `listing_id` | int | 1234567890 | | `listing_title` | str | "Apartamento 2 quartos" | | `listing_category` | str | "Apartamentos" | | `listing_type` | str | "Venda" | | `listing_url` | str | URL completa do anúncio | | `listing_price` | int | 450000 | | `listing_currency` | str | "R$" | | `is_professional_ad` | bool | true/false | | `listing_created` | int | Timestamp (epoch seconds) | | `state` | str | "SP" | | `region` | str | "sao-paulo-e-regiao" | | `zone` | str | Slug extraído da URL | | `municipality` | str | "São Paulo" | | `neighbourhood` | str | "Vila Mariana" | | `ddd` | str | "11" | | `listing_condominium` | str | Valor do condomínio | | `listing_iptu` | str | Valor do IPTU | | `listing_size` | str | Área em m² | | `listing_rooms` | str | Nº de quartos | | `listing_bathrooms` | str | Nº de banheiros | | `listing_garage_spaces` | str | Nº de vagas | | `listing_re_features` | str | Features do imóvel | | `listing_re_complex_features` | str | Features do condomínio | | `aquisition_date` | str | "2026-03-17 12:30:00" |

#### Frequência de Execução

Diária, orquestrada via AWS Step Functions com trigger no EventBridge.

#### Estrutura do Código

```
olx/
├── olx.py             # Classe OlxScraper — lógica principal
├── refiller.py        # Classe Refiller — seed da fila SQS
├── parser.py          # Extração de __NEXT_DATA__ e mapeamento de campos
├── session.py         # Sessão HTTP com cloudscraper e rotação de IP
├── subdivision.py     # Subdivisão adaptativa de queries
├── constants.py       # Configurações, limites e categorias
└── tests/             # 82 testes (unit + integration)
```

#### Principais Serviços e Componentes

**Conta seazone-technology (452791833956):**

* [S3 — .env do scraper](https://452791833956-ayfnvwew.us-west-2.console.aws.amazon.com/s3/object/pipe-essential-files?region=us-west-2&prefix=Pipe-scrapers/external/environment/olx_scraper.env): Variáveis de ambiente do scraper
* [SQS — Fila de Input](https://452791833956-ayfnvwew.us-west-2.console.aws.amazon.com/sqs/v3/home?region=us-west-2#/queues/https%3A%2F%2Fsqs.us-west-2.amazonaws.com%2F452791833956%2Folx-scraper-input.fifo): Fila principal de mensagens para o scraper
* [SQS — Fila de Falhas](https://452791833956-ayfnvwew.us-west-2.console.aws.amazon.com/sqs/v3/home?region=us-west-2#/queues/https%3A%2F%2Fsqs.us-west-2.amazonaws.com%2F452791833956%2Folx-scraper-failure.fifo): Dead-letter queue do scraper
* [SQS — Fila de Output (dados)](https://452791833956-ayfnvwew.us-west-2.console.aws.amazon.com/sqs/v3/home?region=us-west-2#/queues/https%3A%2F%2Fsqs.us-west-2.amazonaws.com%2F452791833956%2Folx-scraper-output.fifo): Fila de saída para envio ao Firehose
* [SQS — Fila de Falhas (dados)](https://452791833956-ayfnvwew.us-west-2.console.aws.amazon.com/sqs/v3/home?region=us-west-2#/queues/https%3A%2F%2Fsqs.us-west-2.amazonaws.com%2F452791833956%2Folx-scraper-data-failure.fifo): Dead-letter queue do envio de dados
* [ECS — Scraper Principal](https://452791833956-ayfnvwew.us-west-2.console.aws.amazon.com/ecs/v2/clusters/galadriel/services/pipe-olx-scraper?region=us-west-2): Serviço ECS que roda o scraper
* [ECS — Scraper de Dados](https://452791833956-ayfnvwew.us-west-2.console.aws.amazon.com/ecs/v2/clusters/galadriel/services/pipe-olx-scraper-data?region=us-west-2): Serviço ECS que envia dados ao Firehose
* [Step Functions](https://452791833956-ayfnvwew.us-west-2.console.aws.amazon.com/states/home?region=us-west-2#/statemachines/view/arn%3Aaws%3Astates%3Aus-west-2%3A452791833956%3AstateMachine%3Ascraper_olx): Orquestração do pipeline
* [EventBridge Schedule](https://452791833956-ayfnvwew.us-west-2.console.aws.amazon.com/scheduler/home?region=us-west-2#schedules/default/scraper_olx): Trigger diário

**Conta PRD-Lake (011528361483):**

* [Kinesis Data Firehose](https://011528361483-sjvx345v.us-west-2.console.aws.amazon.com/firehose/home?region=us-west-2#/details/brlink-olx_listings-PUT-S3-6eSBZ/monitoring): Processamento e envio de dados ao S3
* [S3 — Data Lake RAW](https://011528361483-sjvx345v.us-west-2.console.aws.amazon.com/s3/buckets/brlink-seazone-raw-data?region=us-west-2&prefix=olx_listings/&showversions=false): Dados brutos particionados por ano/mes/dia