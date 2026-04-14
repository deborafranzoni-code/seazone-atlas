<!-- title: Documentação Técnica | url: https://outline.seazone.com.br/doc/documentacao-tecnica-xYCsyOYfqr | area: Tecnologia -->

# Documentação Técnica

# 📘 Documentação Técnica: Sistema de Quarentena e Governança de Competidores

## 1. Visão Geral e Arquitetura

O sistema opera em uma arquitetura **Híbrida (AWS + GCP)**. A AWS é responsável pelo processamento pesado e aplicação das regras de detecção diária. A GCP atua como camada de governança, integrando os resultados com o BigQuery e a interface do usuário (Google Sheets), além de aplicar regras estatísticas mensais (IQR).

### Diagrama de Fluxo de Dados


 ![](/api/attachments.redirect?id=aab28f4d-4191-4702-9eb4-85a7d81404cb " =1108x805")

## 2. Camada de Detecção (AWS)

**Orquestrador:** AWS Step Functions (`fetchcompetitors`) **Horário de Execução:** Diariamente, 06:00 - 07:00 AM.

### 2.1. Preparação dos Dados

* **Lambda:** `LambdaDailyRevenueCompetitors`
* **Função:** Cria um snapshot dos dados diários (`daily_revenue_competitors_temp`) e limpa tabelas temporárias.
* **Fail-safe:** Aborta se a tabela `dead_alive` tiver < 400k IDs ativos ou integridade duvidosa.

### 2.2. Motor de Regras (Paralelo)

Quatro Lambdas executam simultaneamente para identificar anomalias. Se um listing é detectado, ele é salvo em `blocked_listings_dates_temp` com uma tag específica (`rule`).\n

| Regra | Nome Técnico | Gatilho Lógico (Resumo) | Tag |
|----|----|----|----|
| **A** | `Rule A` | Alta ocupação (>1.3x média) sem reviews recentes ou imóveis novos sem reviews. | `6m_ocup` |
| **B** | `Rule B` | Preço diário > 3x mediana móvel (30d) e > 3x média da categoria. Ignora feriados. | `day_fat_acima` |
| **C** | `Rule C` | Ocupação e Preço consistentemente acima da categoria (Outliers históricos). | `ocup_alta` |
| **D** | `Rule D` | Taxa de indisponibilidade futura (bloqueado + ocupado) ≥ 90% nos próximos 90 dias. | `futuro_bloqueado` |

#### 2.2.1. Detalhamento da Regra D (Indisponibilidade Futura)

**Objetivo:** Detectar listings que possuem o calendário quase totalmente indisponível nos próximos 90 dias, o que indica possível bloqueio manual pelo host ou uso pessoal do imóvel, distorcendo métricas de ocupação e oferta.

**Fonte de Dados:**

* Tabela `daily_revenue_competitors_temp`, filtrando datas de hoje até hoje + 90 dias.

**Lógica de Detecção:**


1. Calcula o campo derivado `unavailable = blocked OR occupied` para cada dia/listing.
2. Agrupa por `airbnb_listing_id` e calcula a `future_unavailability_rate_90d` (média de `unavailable`).
3. Filtra os listings cuja taxa de indisponibilidade seja **≥ 90%**.

**Geração das Datas de Bloqueio:**

* Para cada listing detectado, consulta a `max_date` (última data disponível no calendário).
* Gera um range de datas de bloqueio de **hoje** até a `max_date` do listing.
* Cada par `(airbnb_listing_id, date)` é salvo como uma linha individual.

**Gestão de Estado (Incremental):**

* A regra mantém um estado próprio em `s3://{BUCKET_OUTPUT}/rule_d_dates_to_block/`.
* A cada execução, o histórico de datas **passadas** (anteriores a hoje) do estado anterior é preservado e combinado com os novos suspeitos, evitando perda de rastreabilidade.
* O estado corrente é sobrescrito em `state=current/` e uma cópia é adicionada em `state=historic/` particionada por `acquisition_date`.

**Saída:**

* Grava os resultados em `blocked_listings_dates_temp` (modo `append`), integrando-se ao mesmo pipeline das demais regras.

### 2.3. Aplicação dos Bloqueios

* **Lambda:** `LambdaApplyRulesDailyRevenueCompetitors`
* **Ação:** Consolida todas as regras geradas (A, B, C e D). Reescreve a tabela `daily_revenue_competitors` no S3.
* **Efeito:**
  * `available` = `false`
  * `occupied` = `false`
  * `blocked` = `true`
  * `block_reason` = Concatenação das regras (ex: `['6m_ocup', 'futuro_bloqueado']`).

## 3. Camada de Governança (GCP)

Esta camada conecta a detecção técnica com a decisão humana.

**Componente Principal:** Cloud Function `competitors-quarantine-blocked` **Gatilho:** Webhook (HTTP) acionado pelo Scheduler ou pela Planilha.

### 3.1. Entradas de Dados

A função recebe dados de duas fontes:


1. **AWS Athena:** Lê a tabela `blocked_listings_dates_temp` para saber quem foi bloqueado hoje pelo robô.
2. **Google Sheets (Payload JSON):** Recebe as listas de IDs que o usuário decidiu manipular:
   * `remove_quarantine`: Listings a serem liberados.
   * `meta_inactive`: Listings a serem removidos da meta permanentemente.

### 3.2. Regra Adicional: IQR (Interquartile Range)

Esta regra roda **apenas na GCP** e somente a partir do **dia 20 de cada mês**.

* **Objetivo:** Identificar outliers estatísticos de faturamento que passaram pelas regras diárias.
* **Lógica:** Calcula o faturamento acumulado do mês. Se `Faturamento > Q3 + 2 * IQR` da categoria.
* **Tag:** `IQR`.

### 3.3. Saídas e Armazenamento (GCS & BigQuery)

A função processa as entradas e salva arquivos Parquet no Google Cloud Storage (GCS), que alimentam External Tables no BigQuery.

#### A. Listings em Quarentena (`competitors-quarantine-blocked`)

* **Conteúdo:** União dos bloqueios da AWS (Regras A–D) + Regra IQR, **filtrando** (removendo) os IDs que o usuário já tratou (liberou ou inativou).
* **Destino GCS:** `gs://seazone-competitors/competitors-quarantine-blocked/state=current` (e `historic`).
* **Tabela BigQuery:** `data-resources-448418.competitors.competitors_quarantine`.
* **Uso:** Alimenta a aba "Listings em Quarentena" da planilha.

#### B. Listings Inativados (`competitors-quarantine-inactive`)

* **Conteúdo:** IDs que o usuário marcou como "Inativar da Meta" na planilha.
* **Destino GCS:** `gs://seazone-competitors/competitors-quarantine-inactive/state=current`.
* **Tabela BigQuery:** `competitors_inative` (sugerido).
* **Impacto no Negócio:** Estes dados são consumidos pela função `calculates-competitors-category` para remover o listing do cálculo de oferta/demanda.

#### C. Histórico de Remoção (`competitors-quarantine-remove`)

* **Conteúdo:** IDs que o usuário marcou como "Liberar da Meta".
* **Função:** Mantém log de auditoria para saber o que foi liberado manualmente.

## 4. Integração com Google Sheets (Interface do Usuário)

A planilha atua como o "Front-end" do sistema.


1. **Leitura:** O Apps Script da planilha consulta o BigQuery (`competitors_quarantine`) para preencher a aba "Listings em Quarentena" toda manhã.
2. **Ação do Usuário:**
   * Seleciona Status: "Inativar da Meta" ou "Liberar da Meta".
   * Clica em **Check**.
3. **Escrita (Trigger):** O botão Check dispara um script que monta um JSON com as decisões e envia um POST para a Cloud Function `competitors-quarantine-blocked`.
4. **Feedback:** A Cloud Function reprocessa os arquivos no GCS, removendo os itens tratados da visualização de "Quarentena" e movendo-os para as pastas de "Inativos" ou "Removidos".

## 5. Dicionário de Tags de Bloqueio

Estas tags aparecem na coluna `rule` na planilha e no BigQuery:

| Tag | Origem | Descrição para Analista | Ação Sugerida |
|----|----|----|----|
| `6m_ocup` | AWS | Imóvel com muita ocupação e sem review. | Verificar calendário no Airbnb. Provável bloqueio manual do host. |
| `day_fat_acima` | AWS | Preço de um dia específico muito alto. | Geralmente erro de digitação ou trava de preço. Inativar se frequente. |
| `ocup_alta` | AWS | Desempenho muito acima da categoria (Outlier). | Analisar se é um concorrente real ou nicho específico. |
| `futuro_bloqueado` | AWS | Calendário ≥ 90% indisponível nos próximos 90 dias. | Provável bloqueio manual ou uso pessoal. Verificar calendário no Airbnb e inativar se confirmado. |
| `IQR` | GCP | Faturamento total do mês muito alto (Estatístico). | Validar se o faturamento é real. |

## 6. Monitoramento e Troubleshooting

* **Erros na AWS:**
  * Capturados pelo SNS Topic (`SNS_ERROR_TOPIC`).
  * Causa comum: Falha na query do Athena ou Timeout no Lambda.
* **Erros na GCP:**
  * Capturados no bloco `except` da Cloud Function.
  * **Ação:** Envia notificação formatada para o **Slack** (Webhook).
  * Logs disponíveis no Google Cloud Logging.
* **Logs de Auditoria:**
  * Todo arquivo salvo no GCS possui partição `state=historic` com a data `day_alert`, permitindo reconstruir o cenário de qualquer dia passado.
  * A Regra D mantém histórico próprio em `rule_d_dates_to_block/state=historic/`, particionado por `acquisition_date`.