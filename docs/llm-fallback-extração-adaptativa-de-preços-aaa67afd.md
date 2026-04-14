<!-- title: LLM Fallback - Extração Adaptativa de Preços | url: https://outline.seazone.com.br/doc/llm-fallback-extracao-adaptativa-de-precos-9CUJtHKkWn | area: Tecnologia -->

# LLM Fallback - Extração Adaptativa de Preços

## TL;DR

* **Qual problema resolve?** Os scrapers de preço dependem de caminhos fixos no JSON da API do Airbnb. Quando o Airbnb muda a estrutura, 200+ tasks ECS falham ao mesmo tempo e precisam de correção manual.
* **Onde a IA ajuda?** Quando o caminho fixo falha, uma LLM recebe o JSON bruto e descobre onde o preço está na nova estrutura. O novo caminho é validado estruturalmente e salvo no S3 para as outras 199 tasks usarem direto. Na operação normal, a LLM não é chamada. Custo zero.
* **Qual IA?** Gemini 2.5 Flash (Google) — 8s por chamada, 1 vez por mudança de API, não por listing.
* **Números:** 16/16 listings extraídos com sucesso, scraper 1.09s/listing, fallback 1.15s/listing, com LLM 9.61s/listing, delta de preço R$0.25 médio.

**Repositório:** [seazone-tech/priceav-scraper-ai-fallback](https://github.com/seazone-tech/priceav-scraper-ai-fallback)


---

## Arquitetura

### Visão Geral

O módulo `llm_fallback` é um pacote Python independente que fornece extração resiliente de preços da API do Airbnb. Ele é projetado para ser integrado ao [Pipe-scrapers](https://github.com/seazone-tech/Pipe-scrapers) como **git submodule**.

### Estratégia de Fallback em 3 Camadas

```mermaidjs
flowchart TD
    A[Request API Airbnb] --> B{1. Parser Tradicional}
    B -->|OK| Z[Dados extraídos]
    B -->|FALHA| C{2. Cache S3}
    C -->|Path encontrado| D[Parser com path do S3]
    D -->|OK| Z
    D -->|FALHA| E{3. LLM Gemini}
    C -->|Cache vazio| E
    E -->|Path válido| F[Validar estrutura]
    F -->|OK| G[Salvar path no S3]
    G --> Z
    F -->|FALHA| H[Retry com feedback]
    H --> E
    E -->|NOT_FOUND| I[Retorna None]
```

| Camada | O que faz | Latência | Custo |
|----|----|----|----|
| 1. Parser tradicional | Extrai pelo JSON path fixo conhecido | \~1.1s | Zero |
| 2. Cache S3 | Busca paths descobertos por outras tasks | \~1.2s | Zero |
| 3. LLM (Gemini) | Descobre o novo path no JSON bruto | \~9.6s | 1 API call |

### Componentes do Módulo

```
llm_fallback/
  __init__.py        → extract_price() - orquestrador público
  config.py          → Configuração via variáveis de ambiente
  parser.py          → Parser tradicional + validação estrutural
  llm_discovery.py   → Descoberta de paths via LLM com retry
  s3_cache.py        → Cache de paths no S3 com proteção contra race condition
```

#### `__init__.py` — Orquestrador

Exporta `extract_price()`, a função principal que coordena as 3 camadas de fallback. Retorna `None` quando todas as camadas falham, espelhando o comportamento padrão do Pipe-scrapers (que envia `price: None` para o Firehose).

#### `parser.py` — Parsers e Validação

| Função | Descrição |
|----|----|
| `parse_traditional()` | Extrai pelo path fixo: `data.presentation.stayCheckout.sections.temporaryQuickPayData.bootstrapPayments.productPriceBreakdown.priceBreakdown` |
| `parse_from_path()` | Extrai por um path dinâmico (dot-notation) |
| `extract_from_breakdown()` | Extrai dados de um node `priceBreakdown` |
| `validate_breakdown_structure()` | Valida que um node tem a estrutura esperada |
| `navigate_json_path()` | Navega dict por dot-notation com busca recursiva |

**Schema esperado do node** `**priceBreakdown**`**:**

```json
{
  "total": {
    "total": {
      "amountFormatted": "R$482,80",
      "amountMicros": 48280000000,
      "currency": "BRL"
    }
  },
  "priceItems": [
    {
      "localizedTitle": "2 noites x R$258,50",
      "total": { "amountFormatted": "R$517,00" },
      "nestedPriceItems": [...]
    }
  ]
}
```

#### `llm_discovery.py` — Descoberta via LLM

* Usa **Gemini 2.5 Flash** via SDK `google-genai`
* **Prompt estruturado**: mostra o schema JSON exato esperado, não apenas "encontre preços"
* **Validação antes de aceitar**: navega até o node e verifica a estrutura com `validate_breakdown_structure()`
* **Retry com feedback**: se o LLM retorna um path inválido, envia de volta as keys encontradas e pede para tentar de novo (até 2 tentativas)
* **Sentinel NOT_FOUND**: LLM retorna explicitamente quando não encontra a estrutura
* **Truncamento**: JSONs >80KB são podados preservando a estrutura para caber no context window

#### `s3_cache.py` — Cache Compartilhado

* **Localização:** `s3://pipe-essential-files/Pipe-scrapers/fallback-paths/airbnb/{scraper}/paths.json`
* **Leitura:** `get_cached_paths()` retorna lista de paths ou lista vazia
* **Escrita:** `save_path_to_s3()` com read-verify-retry para proteger contra race condition entre 200+ tasks concorrentes
* Paths inválidos **nunca** são salvos no S3

### Cenário: API Muda com 200 Tasks Rodando


1. Todas as 200 tasks falham no parser tradicional
2. Todas consultam o S3 — está vazio (primeira vez)
3. A **primeira task** chama o LLM (\~8s), descobre o novo path, valida, salva no S3
4. As **outras 199 tasks** encontram o path no S3 e usam direto — **sem chamar o LLM**
5. Resultado: **1 call ao LLM** em vez de 200

### Segurança

* Paths são **validados estruturalmente** antes de aceitar ou salvar no S3
* Paths do S3 são **re-validados** antes do uso (protege contra paths stale)
* Escrita no S3 usa **read-verify-retry** para mitigar race conditions
* Paths inválidos nunca poluem o cache


---

## Formato de Saída

```python
{
    "items": [
        {
            "title": "2 noites x R$258,50",
            "total": "R$517,00",
            "nested": [
                {"title": "2 noites - 5 a 7 de jul.", "total": "R$517,00"}
            ]
        },
        {
            "title": "Desconto para reservas antecipadas",
            "total": "-R$34,20",
            "nested": [...]
        }
    ],
    "total": "R$482,80",
    "total_micros": 48280000000,
    "currency": "BRL"
}
```


---

## Testes

### Estrutura dos testes

```
tests/
  test_full_flow.py              → 10 listings via checkout API + parser tradicional
  test_llm_vs_scraper.py         → 6 listings cross-check scraper vs checkout API
  test_scraper_vs_llm_benchmark.py → 16 listings benchmark completo (3 modos)
```

### Master Benchmark (`test_scraper_vs_llm_benchmark.py`)

Compara 3 modos de extração lado a lado para **16 listings reais**:


1. **Scraper** — `StaysPdpSections` API (mesmo que o Pipe-scrapers usa em produção)
2. **Fallback** — `stayCheckout` API + parser tradicional (sem LLM)
3. **LLM forçado** — `stayCheckout` API + chamada Gemini (para medir overhead)

O LLM forçado roda em **subprocess separado** para evitar conflitos entre `eventlet.monkey_patch()` e o SDK `google-genai`.

#### Resultados (16 listings)

| Listing | N | Scraper | Time | Fallback | Time | Delta |
|----|----|----|----|----|----|----|
| 1312949509621922876 | 2 | R$613 | 1.32s | R$632,40 | 1.18s | R$19.40 (taxa serviço) |
| 1580533510841386501 | 2 | R$572 | 1.09s | R$571,92 | 0.97s | R$0.08 |
| 1521846334742031022 | 2 | R$615 | 0.92s | R$614,16 | 1.24s | R$0.84 |
| 1486959815291020761 | 2 | R$712 | 1.25s | R$711,88 | 1.04s | R$0.12 |
| 918143400027469545 | 2 | R$1.241 | 1.35s | R$1.240,56 | 1.27s | R$0.44 |
| 1110220274163244963 | 2 | R$490 | 0.89s | R$490,00 | 1.11s | **R$0.00** |
| 46502581 | 4 | R$1.142 | 1.11s | R$1.160,70 | 1.35s | R$18.70 |
| 51067926 | 4 | R$676 | 1.01s | R$676,00 | 1.18s | **R$0.00** |
| 41213741 | 4 | R$457 | 1.09s | R$464,28 | 1.19s | R$7.28 |
| 37526401 | 4 | R$685 | 0.92s | R$696,43 | 1.18s | R$11.43 |
| 832048531904142816 | 4 | R$2.853 | 1.09s | R$2.901,75 | 1.19s | R$48.75 |
| 1373191610513309191 | 4 | R$1.950 | 1.09s | R$1.934,89 | 0.98s | R$15.11 |
| 5414746 | 4 | R$8.364 | 1.00s | R$8.506,79 | 1.11s | R$142.79 |
| 1298813049360030201 | 4 | R$841 | 1.10s | R$835,71 | 1.12s | R$5.29 |
| 1277129408849139616 | 4 | R$1.212 | 1.13s | R$1.201,32 | 1.18s | R$10.68 |
| 1158616773138927166 | 4 | R$989 | 0.99s | R$974,99 | 1.06s | R$14.01 |

#### Latências

| Modo | Avg Latência | O que mede |
|----|----|----|
| Scraper | **1.09s** | StaysPdpSections API + fixed-path parser |
| Fallback | **1.15s** | stayCheckout API + traditional parser (sem LLM) |
| LLM forçado | **9.61s** | stayCheckout API + Gemini call + parse |
| Gemini apenas | **8.0s** | Overhead puro da chamada LLM |

#### Sobre os deltas de preço

* Deltas < R$1: **arredondamento** (scraper arredonda para inteiro, checkout tem centavos)
* Deltas R$5-R$142: **taxa de serviço do Airbnb** (\~1.5-3.2%) inclusa no endpoint `stayCheckout` mas não no `StaysPdpSections`
* Delta médio excluindo taxa de serviço: **R$0.25**

### Teste do LLM com Listing Problemático

O listing `1486959815291020761` teve comportamento intermitente — em algumas chamadas o `bootstrapPayments` vem `null` (data não disponível para checkin). Investigação mostrou que **Sep 26 está bloqueado** nesse listing. Mudando para Sep 27, funciona perfeitamente.

Quando `bootstrapPayments` é null, o `validate_breakdown_structure()` rejeita corretamente e o LLM retorna `NOT_FOUND`. **Nenhum path inválido é salvo no S3.**

### Teste de Simulação de Mudança de API

Renomeamos 4 chaves no JSON para simular uma atualização do Airbnb:

| Original | Simulado |
|----|----|
| `temporaryQuickPayData` | `checkoutPaymentContext` |
| `bootstrapPayments` | `paymentBootstrap` |
| `productPriceBreakdown` | `pricingSummary` |
| `priceBreakdown` | `breakdown` |

Resultado: Parser tradicional falhou (esperado), LLM encontrou o novo path e extraiu o preço correto — **match exato** com o valor original.


---

## Integração com Pipe-scrapers

### 1. Adicionar como submodule

```bash
cd Pipe-scrapers
git submodule add https://github.com/seazone-tech/priceav-scraper-ai-fallback.git airbnb/llm_fallback_repo
git submodule update --init
```

Estrutura resultante:

```
Pipe-scrapers/
  airbnb/
    price.py                    ← scraper existente
    session.py                  ← sessão Airbnb existente
    llm_fallback_repo/          ← submodule
      llm_fallback/
        __init__.py
        config.py
        parser.py
        llm_discovery.py
        s3_cache.py
```

### 2. Importar no scraper

Em `airbnb/price.py`:

```python
from airbnb.llm_fallback_repo.llm_fallback import extract_price as llm_extract_price
```

#### Opção A: Fallback no `_new_extract_price` (recomendado)

```python
def _new_extract_price(self, request_data, checkin, checkout):
    # ... código existente de extração ...

    # Se não conseguiu extrair preço, tentar fallback LLM
    if not price_str:
        log.warning("Extraction failed, trying LLM fallback for %s",
                     self.listing['id_airbnb'])
        llm_result = llm_extract_price(request_data,
                                        scraper_name="stayCheckout",
                                        use_s3_cache=True)
        if llm_result:
            nights = self._extract_nights_from_qualifier(
                checkin, checkout, qualifier, selected_dates_title)
            if nights <= 0:
                nights = 1
            nightly = llm_result["total_micros"] / (nights * 1_000_000)
            price_str = f"R${nightly:,.2f}".replace(",", "X") \\
                        .replace(".", ",").replace("X", ".")

    return price_str
```

#### Opção B: Fallback no `handle_message` (safety net)

Usar como camada extra ao redor de todo o fluxo existente, sem modificar a lógica interna do `PriceScraper`.

### 3. Adicionar dependência

No `requirements.txt`:

```
google-genai
```

### 4. Variáveis de ambiente

Na ECS task definition ou `.env`:

```bash
# Obrigatória
GEMINI_API_KEY=<api-key-do-gemini>

# Opcionais (têm defaults)
GEMINI_MODEL_NAME=gemini-2.5-flash
FALLBACK_PATHS_BUCKET=pipe-essential-files
FALLBACK_PATHS_PREFIX=Pipe-scrapers/fallback-paths/airbnb
```

### 5. Atualizar o submodule

Quando houver atualizações:

```bash
cd Pipe-scrapers
git submodule update --remote airbnb/llm_fallback_repo
git add airbnb/llm_fallback_repo
git commit -m "Update llm_fallback submodule"
```

### Monitoramento

CloudWatch Metric Filters sugeridos:

```
# Quando LLM é acionado (API pode ter mudado)
{ $.message = "*calling LLM*" }

# Quando tudo falha
{ $.message = "*LLM did not return a valid path*" }
```


---

## Variáveis de Ambiente

| Variável | Default | Descrição |
|----|----|----|
| `GEMINI_API_KEY` | — | API key do Google Gemini (obrigatória) |
| `GEMINI_MODEL_NAME` | `gemini-2.5-flash` | Modelo a usar |
| `FALLBACK_PATHS_BUCKET` | `pipe-essential-files` | Bucket S3 para cache |
| `FALLBACK_PATHS_PREFIX` | `Pipe-scrapers/fallback-paths/airbnb` | Prefixo S3 |

## Dependências

```
boto3
botocore
google-genai
```

## Decisões Técnicas

| Decisão | Motivo |
|----|----|
| LLM Fallback ao invés de Midscene.js | Midscene: 40s/listing, 4/6 campos, inviável para 30k/dia. LLM: 2s normal, 10s com fallback, 6/6 campos |
| `gemini-2.5-flash` | Equilíbrio entre velocidade (8s) e qualidade. `gemini-3.1-pro` funciona mas leva \~30s |
| Validação estrutural antes do S3 | Sem validação, LLM retornava paths para nodes "próximos" mas sem a estrutura certa. Esses paths poluiriam o cache das 200 tasks |
| Retry com feedback | Na 1ª tentativa o LLM frequentemente acha um node "próximo". Com feedback das keys encontradas, a 2ª tentativa acerta |
| Read-verify-retry no S3 | Com 200 tasks escrevendo concorrentemente, a última escrita vence. O verify garante que o path não foi sobrescrito |
| Git submodule ao invés de PyPI | Projeto interno, fortemente acoplado ao Pipe-scrapers. Submodule é mais simples que versionamento PyPI |
| `google-genai` ao invés de `google-generativeai` | O SDK antigo foi descontinuado |
| Retornar `None` ao invés de crash | Espelha o comportamento atual do Pipe-scrapers que envia `price: None` ao Firehose |

## Links

* **Repositório:** [seazone-tech/priceav-scraper-ai-fallback](https://github.com/seazone-tech/priceav-scraper-ai-fallback)
* **Pipe-scrapers:** [seazone-tech/Pipe-scrapers](https://github.com/seazone-tech/Pipe-scrapers/tree/Pipe-scrapers)
* **Cache S3:** `s3://pipe-essential-files/Pipe-scrapers/fallback-paths/airbnb/stayCheckout/paths.json`
* **Jira:** [DOP-541](https://seazone.atlassian.net/browse/DOP-541), [DOP-542](https://seazone.atlassian.net/browse/DOP-542), [DOP-543](https://seazone.atlassian.net/browse/DOP-543), [DOP-544](https://seazone.atlassian.net/browse/DOP-544)