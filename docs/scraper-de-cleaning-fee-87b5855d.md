<!-- title: Scraper de Cleaning Fee | url: https://outline.seazone.com.br/doc/scraper-de-cleaning-fee-lVSaVBfgLd | area: Tecnologia -->

# Scraper de Cleaning Fee

## Scraper de Cleaning Fee do Airbnb

O scraper infere a **taxa de limpeza (cleaning fee)** de listings do Airbnb. O Airbnb não expõe a cleaning fee como campo separado nas APIs públicas — ela está embutida no preço total da reserva. Para isolá-la, o scraper utiliza um sistema de equações lineares baseado em 3 reservas sobrepostas.

### Por que inferir a Cleaning Fee?

A cleaning fee é cobrada **uma vez por reserva**, independentemente da duração da estadia. Sabendo disso, ao comparar o custo de duas reservas separadas com o custo de uma reserva que engloba ambas, a cleaning fee extra se revela:

* **r1** = preço total da primeira reserva (diárias + cleaning_fee)
* **r2** = preço total da segunda reserva (diárias + cleaning_fee)
* **r3** = preço total da reserva combinada (diárias + cleaning_fee)

Como r1 e r2 cobram cleaning_fee duas vezes, e r3 cobra apenas uma vez:

```
cleaning_fee = r1 + r2 - r3
```

### Por que dois valores de Cleaning Fee (small_stays e big_stays)?

O Airbnb permite que anfitriões configurem **taxas de limpeza diferentes** para reservas abaixo e acima de 3 noites. Por isso o scraper calcula dois valores:

* `**cleaning_fee_small_stays**` — usando combinações de estadias curtas (<3 noites cada)
* `**cleaning_fee_big_stays**` — usando estadias de 3+ noites cada

Na maioria dos listings (\~88%) os dois valores são iguais, mas nos demais \~12% podem diferir.

### Fórmula especial para min_stay = 2

Para imóveis com estadia mínima de 2 noites, as small_stays acabam tendo estadias individuais de 2 dias (combinação > 2 dias). Nesse caso, a fórmula padrão mistura os dois tipos de cleaning fee. Uma fórmula ajustada é aplicada quando `cleaning_fee_big_stays` já foi calculado:

```
cleaning_fee_small_stays = (r1 + r2 - r3 + cleaning_fee_big_stays) / 2
```

Condições para aplicar: ambos os valores já calculados, `followed_stay_pattern_small_stays == False`, e ambas as estadias individuais ≤ 2 dias.

### Fonte dos Dados (API)

Os dados são extraídos da **API GraphQL V3 de checkout** do Airbnb:

* **Endpoint:** `POST /api/v3/stayCheckout/`
* **Domínio:** `www.airbnb.com.br` (com rotação entre 47 TLDs do Airbnb)
* **Autenticação:** API key pública `d306zoyjsyarp7ifhu67rjxn52tv0t20`

**De onde vem essa API:** É a mesma API que o site do Airbnb chama quando um hóspede acessa a tela de checkout de uma reserva. Pode ser observada pelo DevTools do browser (Network tab) ao selecionar datas e clicar em "Reservar" em qualquer listing do Airbnb.

**Dados extraídos do response:**

O scraper navega até `data.presentation.stayCheckout.sections.temporaryQuickPayData.bootstrapPayments.productPriceBreakdown.priceBreakdown.priceItems[0].nestedPriceItems` e extrai:

* O item com `amountMicros > 0` → **preço total da reserva** (base de acomodação, sem descontos)
* A presença/ausência de "Taxa de serviço do Airbnb" → **is_professional** (hosts profissionais não têm essa taxa)

O scraper utiliza apenas `priceItems[0]` (tipo `ACCOMMODATION`), ignorando itens de desconto como `PRICING_RULE_EARLY_BIRD_DISCOUNT` em `priceItems[1]`.

### Arquitetura

```
Refiller                Consulta IDs de listings para scrapar
       │                Cria mensagens na fila SQS
       ▼
  SQS Input Queue       FIFO, com deduplicação
       │
       ▼
  CleaningFeeScraper     N workers concorrentes (ECS Fargate)
   ├─ Scrapa small_stays (3 requests por grupo)
   ├─ Scrapa big_stays (3 requests por grupo)
   ├─ Calcula cleaning_fee = r1 + r2 - r3
   ├─ Aplica fórmula especial se necessário
       │
       ▼
  Kinesis Firehose       Cross-account via STS assume_role
       │
       ▼
  Data Lake RAW          JSON no S3
```


1. **Refiller**: Alimenta a fila SQS com IDs de listings a serem scrapados. Utiliza a query `professional_ids_from_last_month` por padrão. Roda como ECS Task (`pipe-airbnb-refiller`) com comando `python3 airbnb.py refiller_cleaning_fee`.
2. **Workers**: N workers concorrentes (ECS Service `pipe-airbnb-scraper-cleaning-fee`, concurrency=4) consomem da fila. Para cada listing, fazem até 6 requests à API (3 para small_stays + 3 para big_stays), calculam a cleaning_fee e enviam ao Firehose.
3. **Firehose**: Entrega os dados cross-account para o Data Lake RAW.

Existem **duas Step Functions** que orquestram o pipeline, uma para cada tipo de listing:

* `scraper_airbnb_cleaning_fee_professional` — listings profissionais
* `scraper_airbnb_cleaning_fee_non_professional` — listings não-profissionais

### Fluxo detalhado de scraping por listing

Para cada listing, o scraper:


1. Tenta scrapar **small_stays** primeiro (estadias curtas)
2. Calcula `cleaning_fee_small_stays` se bem-sucedido
3. Se as small_stays tiverem ambas estadias ≥3 noites, **reutiliza** como big_stays (evita requests redundantes)
4. Se big_stays ainda não foi calculado, scrapa **big_stays** (estadias longas)
5. Calcula `cleaning_fee_big_stays` se bem-sucedido
6. Aplica a **fórmula especial** para min_stay=2 se aplicável
7. Envia resultado ao Firehose

### Resiliência

* **13 retries** por mensagem na fila SQS
* **2 tentativas** por stay_group antes de mover para `failed_stays`
* **Rate limit:** 5 requests/segundo
* **Detecção de IP block:** monitora erros 401, 405, 420, 429 com threshold de 10 erros
* **Rotação de IP:** sessão HTTP com rotação entre 47 TLDs do Airbnb
* **Checkpoint parcial:** dados scrapados com sucesso são enviados ao Firehose mesmo em caso de falha parcial

### Validações da Cleaning Fee

O scraper rejeita valores calculados que são claramente inválidos:

* `cleaning_fee < 0` → `InvalidCleaningFee`
* `cleaning_fee >= preço de alguma estadia` → `InvalidCleaningFee`
* `abs(cleaning_fee) <= 3` → arredondado para 0 (margem de erro)

### Schema de Saída (RAW)

| Campo | Tipo | Exemplo |
|----|----|----|
| `airbnb_listing_id` | str | "1000518870833890664" |
| `cleaning_fee_small_stays` | float | 120.0 |
| `cleaning_fee_big_stays` | float | 120.0 |
| `followed_stay_pattern_small_stays` | bool | true |
| `is_professional` | bool | false |
| `aquisition_date` | str | "2026-03-27 10:30:45" |

* `followed_stay_pattern_small_stays`: `true` se a combinação de estadias curtas teve soma ≤ 2 dias (padrão ideal). `false` indica que a fórmula especial pode ter sido aplicada.

### Frequência de Execução

Executado via ciclo do **Mesh**, rodando a cada \~15 dias. Orquestrado via AWS Step Functions com triggers no EventBridge.

### Estrutura do Código

```
airbnb/
├── cleaning_fee.py    # Classe CleaningFeeScraper — lógica principal (587 linhas)
├── session.py         # Sessão HTTP com rotação de IP entre TLDs do Airbnb
airbnb.py              # Entry point CLI (python airbnb.py cleaning_fee)
sqs.py                 # SQSConsumer — consumo concorrente de filas
util.py                # Graceful shutdown, helpers
```

### Limitações conhecidas

#### Reservas mensais

Estadias de 28+ noites (mensais) não são suportadas. O Airbnb aplica pricing diferenciado para reservas mensais que não é compatível com a fórmula. Esses casos levantam `MonthlyStayError` e são ignorados.

#### Desconto semanal embutido nas diárias (Investigação DOP-565)

Listings com **desconto semanal** configurado pelo anfitrião (para estadias ≥7 noites) podem produzir cleaning_fees infladas quando as estadias individuais (r1, r2) são <7 noites mas a combinada (r3) é ≥7 noites. O desconto é embutido silenciosamente nas diárias pela API V3, sem aparecer como item separado no breakdown de preço. Detalhes completos da investigação no card [DOP-565](https://seazone.atlassian.net/browse/DOP-565).

### Principais Serviços e Componentes

**Conta seazone-technology (452791833956):**

* [S3 — .env dos scrapers Airbnb](https://452791833956-ayfnvwew.us-west-2.console.aws.amazon.com/s3/object/pipe-essential-files?region=us-west-2&prefix=Pipe-scrapers/external/environment/airbnb_scrapers.env): Variáveis de ambiente (`airbnb_scrapers.env`)
* [SQS — Fila de Input (](https://452791833956-ayfnvwew.us-west-2.console.aws.amazon.com/sqs/v3/home?region=us-west-2#/queues/https%3A%2F%2Fsqs.us-west-2.amazonaws.com%2F452791833956%2Fairbnb-listings-cleaning-fee-input.fifo)`[airbnb-listings-cleaning-fee-input.fifo](https://452791833956-ayfnvwew.us-west-2.console.aws.amazon.com/sqs/v3/home?region=us-west-2#/queues/https%3A%2F%2Fsqs.us-west-2.amazonaws.com%2F452791833956%2Fairbnb-listings-cleaning-fee-input.fifo)`[)](https://452791833956-ayfnvwew.us-west-2.console.aws.amazon.com/sqs/v3/home?region=us-west-2#/queues/https%3A%2F%2Fsqs.us-west-2.amazonaws.com%2F452791833956%2Fairbnb-listings-cleaning-fee-input.fifo): Fila FIFO de mensagens para o scraper
* [SQS — Fila de Falhas (](https://452791833956-ayfnvwew.us-west-2.console.aws.amazon.com/sqs/v3/home?region=us-west-2#/queues/https%3A%2F%2Fsqs.us-west-2.amazonaws.com%2F452791833956%2Fairbnb-listings-cleaning-fee-failure.fifo)`[airbnb-listings-cleaning-fee-failure.fifo](https://452791833956-ayfnvwew.us-west-2.console.aws.amazon.com/sqs/v3/home?region=us-west-2#/queues/https%3A%2F%2Fsqs.us-west-2.amazonaws.com%2F452791833956%2Fairbnb-listings-cleaning-fee-failure.fifo)`[)](https://452791833956-ayfnvwew.us-west-2.console.aws.amazon.com/sqs/v3/home?region=us-west-2#/queues/https%3A%2F%2Fsqs.us-west-2.amazonaws.com%2F452791833956%2Fairbnb-listings-cleaning-fee-failure.fifo): Dead-letter queue
* [ECS — Service ](https://452791833956-ayfnvwew.us-west-2.console.aws.amazon.com/ecs/v2/clusters/galadriel/services/pipe-airbnb-scraper-cleaning-fee?region=us-west-2)`[pipe-airbnb-scraper-cleaning-fee](https://452791833956-ayfnvwew.us-west-2.console.aws.amazon.com/ecs/v2/clusters/galadriel/services/pipe-airbnb-scraper-cleaning-fee?region=us-west-2)`: Serviço ECS do scraper (cluster galadriel)
* [ECS — Task Definition ](https://452791833956-ayfnvwew.us-west-2.console.aws.amazon.com/ecs/v2/task-definitions/pipe-airbnb-refiller?region=us-west-2)`[pipe-airbnb-refiller](https://452791833956-ayfnvwew.us-west-2.console.aws.amazon.com/ecs/v2/task-definitions/pipe-airbnb-refiller?region=us-west-2)`: Task definition usada pelo refiller
* [Step Function — Professional](https://452791833956-ayfnvwew.us-west-2.console.aws.amazon.com/states/home?region=us-west-2#/statemachines/view/arn%3Aaws%3Astates%3Aus-west-2%3A452791833956%3AstateMachine%3Ascraper_airbnb_cleaning_fee_professional): Orquestração para listings profissionais
* [Step Function — Non-Professional](https://452791833956-ayfnvwew.us-west-2.console.aws.amazon.com/states/home?region=us-west-2#/statemachines/view/arn%3Aaws%3Astates%3Aus-west-2%3A452791833956%3AstateMachine%3Ascraper_airbnb_cleaning_fee_non_professional): Orquestração para listings não-profissionais
* [EventBridge — Schedule Professional](https://452791833956-ayfnvwew.us-west-2.console.aws.amazon.com/scheduler/home?region=us-west-2#schedules/default/scraper_airbnb_cleaning_fee_professional): Trigger para profissionais
* [EventBridge — Schedule Non-Professional](https://452791833956-ayfnvwew.us-west-2.console.aws.amazon.com/scheduler/home?region=us-west-2#schedules/default/scraper_airbnb_cleaning_fee_non_professional): Trigger para não-profissionais

**Conta PRD-Lake (011528361483):**

* [Kinesis Data Firehose (](https://011528361483-sjvx345v.us-west-2.console.aws.amazon.com/firehose/home?region=us-west-2#/details/airbnb_cleaning_fee-KDS-S3-4Tnb5/monitoring)`[airbnb_cleaning_fee-KDS-S3-4Tnb5](https://011528361483-sjvx345v.us-west-2.console.aws.amazon.com/firehose/home?region=us-west-2#/details/airbnb_cleaning_fee-KDS-S3-4Tnb5/monitoring)`[)](https://011528361483-sjvx345v.us-west-2.console.aws.amazon.com/firehose/home?region=us-west-2#/details/airbnb_cleaning_fee-KDS-S3-4Tnb5/monitoring): Stream de entrega dos dados ao S3
* [S3 — Data Lake RAW (](https://011528361483-sjvx345v.us-west-2.console.aws.amazon.com/s3/buckets/brlink-seazone-raw-data?region=us-west-2&prefix=airbnb_cleaning_fee/&showversions=false)`[airbnb_cleaning_fee/](https://011528361483-sjvx345v.us-west-2.console.aws.amazon.com/s3/buckets/brlink-seazone-raw-data?region=us-west-2&prefix=airbnb_cleaning_fee/&showversions=false)`[)](https://011528361483-sjvx345v.us-west-2.console.aws.amazon.com/s3/buckets/brlink-seazone-raw-data?region=us-west-2&prefix=airbnb_cleaning_fee/&showversions=false): Dados brutos particionados

**Repositório:**

* [Pipe-scrapers](https://github.com/seazone-tech/Pipe-scrapers) — branch principal, diretório `airbnb/cleaning_fee.py`

### Jira

* [DOP-522](https://seazone.atlassian.net/browse/DOP-522) — Épico: Scraper PriceAv (CleanFee)
* [DOP-565](https://seazone.atlassian.net/browse/DOP-565) — Investigação: Inconsistência no cálculo de cleaning_fee em certos listings