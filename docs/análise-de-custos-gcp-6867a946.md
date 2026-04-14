<!-- title: Análise de Custos GCP | url: https://outline.seazone.com.br/doc/analise-de-custos-gcp-UPgjSmSdNX | area: Tecnologia -->

# Análise de Custos GCP

**Data da analise:** 12 de marco de 2026 **Billing Account:** 012829-B5239B-729286 (Conta de Faturamento) **Moeda:** BRL **Periodo analisado:** Dezembro/2025 a Marco/2026 (parcial) **Fonte de dados:** BigQuery Billing Export (`platform-finops-483715.billing_export`)


---

## 1. Sumario Executivo

O custo total da infraestrutura GCP apresentou uma **tendencia de alta real** quando normalizado pela migracao de projetos ocorrida entre Dez/2025 e Fev/2026. A projecao para Marco/2026 indica um custo de aproximadamente **R$ 15.300**, representando um aumento de **21% em relacao a Fevereiro** (R$ 12.618).

Os principais vetores de aumento sao:

| Servico | Fev/2026 | Projecao Mar/2026 | Variacao |
|----|----|----|----|
| **Compute Engine** | R$ 6.032 | R$ 7.759 | +28,6% |
| **Gemini API** | R$ 810 | R$ 1.717 | +112,0% |
| **Cloud SQL** | R$ 1.445 | R$ 1.747 | +20,9% |
| **Cloud Memorystore** | R$ 389 | R$ 550 | +41,4% |
| **Cloud Run** | R$ 54 | R$ 152 | +181,1% |

**Acao imediata recomendada:** Revisao de dimensionamento de Compute Engine (maior custo absoluto) e governanca do uso de Gemini API (maior taxa de crescimento).


---

## 2. Visao Geral - Evolucao Mensal

### 2.1 Custo Total por Mes

| Mes | Custo Total (BRL) | Variacao |
|----|----|----|
| Dezembro/2025 | R$ 23.006,14 | — |
| Janeiro/2026 | R$ 17.006,14 | -26,1% |
| Fevereiro/2026 | R$ 12.617,94 | -25,8% |
| **Marco/2026 (projecao)** | **R$ 15.267** | **+21,0%** |

### 2.2 Custo Diario - Tendencia (Fev-Mar/2026)

```
Fev 01-07:  media R$ 403/dia

Fev 08-14:  media R$ 413/dia

Fev 15-21:  media R$ 469/dia

Fev 22-28:  media R$ 523/dia

Mar 01-07:  media R$ 497/dia

Mar 08-11:  media R$ 601/dia  ← pico de R$ 885 em 10/Mar (Gemini API)
```

A tendencia diaria mostra **crescimento consistente** de \~R$ 400/dia no inicio de Fevereiro para \~R$ 500-600/dia em Marco, com picos associados a uso intensivo de Gemini API.


---

## 3. Analise por Servico - Ultimos 3 Meses

### 3.1 Ranking de Servicos por Custo

| # | Servico | Dez/2025 | Jan/2026 | Fev/2026 | Projecao Mar/2026 | Tendencia |
|----|----|----|----|----|----|----|
| 1 | Compute Engine | R$ 4.916 | R$ 5.036 | R$ 6.032 | R$ 7.759 | ↑ Alta |
| 2 | Cloud SQL | R$ 8.543 | R$ 2.900 | R$ 1.445 | R$ 1.747 | ↑ Subindo |
| 3 | Gemini API | R$ 1.433 | R$ 1.654 | R$ 810 | R$ 1.717 | ↑↑ Alta forte |
| 4 | Networking | R$ 1.037 | R$ 996 | R$ 1.049 | R$ 1.177 | → Estavel |
| 5 | BigQuery | R$ 644 | R$ 828 | R$ 817 | R$ 848 | → Estavel |
| 6 | Cloud Memorystore | R$ 1.087 | R$ 463 | R$ 389 | R$ 550 | ↑ Subindo |
| 7 | Support | R$ 2.634 | R$ 2.098 | R$ 467 | R$ 0 | ↓ Encerrado |
| 8 | Kubernetes Engine | R$ 455 | R$ 472 | R$ 397 | R$ 397 | → Estavel |
| 9 | Cloud Logging | R$ 218 | R$ 305 | R$ 295 | R$ 210 | → Estavel |
| 10 | Vertex AI | R$ 247 | R$ 280 | R$ 240 | R$ 203 | → Estavel |
| 11 | Cloud Monitoring | R$ 284 | R$ 305 | R$ 230 | R$ 193 | → Estavel |
| 12 | Cloud Run | R$ 351 | R$ 501 | R$ 54 | R$ 152 | ↑ Subindo |
| 13 | Cloud Run Functions | R$ 129 | R$ 134 | R$ 113 | R$ 116 | → Estavel |
| 14 | Cloud Storage | R$ 704 | R$ 684 | R$ 58 | R$ 51 | → Estavel |
| 15 | Maps API | R$ 149 | R$ 274 | R$ 91 | R$ 6 | ↓ Queda |
| 16 | Backup for GKE | R$ 0 | R$ 0 | R$ 24 | R$ 48 | ↑ Novo |

### 3.2 Distribuicao de Custo (Fev/2026)

```
Compute Engine   ██████████████████████████████████████████████  47,8%
Cloud SQL        █████████████                                   11,5%
Networking       █████████                                        8,3%
Gemini API       ███████                                          6,4%
BigQuery         ██████                                           6,5%
Support          ████                                             3,7%
Kubernetes       ███                                              3,1%
Memorystore      ███                                              3,1%
Cloud Logging    ██                                               2,3%
Vertex AI        ██                                               1,9%
Monitoring       ██                                               1,8%
Outros           ███                                              3,6%
```


---

## 4. Analise por Projeto - Ultimos 3 Meses

| # | Projeto | Fev/2026 | Projecao Mar/2026 | Variacao | Tendencia |
|----|----|----|----|----|----|
| 1 | sz-shared-seazoneTools | R$ 8.669 | R$ 10.344 | +19,3% | ↑ Alta |
| 2 | sz-dados-prd | R$ 2.075 | R$ 2.097 | +1,1% | → Estavel |
| 3 | sz-shared-tecnologia | R$ 359 | R$ 1.210 | +237,0% | ↑↑ Alta forte |
| 4 | sz-shared-sia | R$ 0 | R$ 579 | Novo | ↑ Novo |
| 5 | sz-comercial-bizops | R$ 290 | R$ 311 | +7,3% | → Estavel |
| 6 | sz-comercial-investimentos | R$ 294 | R$ 269 | -8,3% | → Estavel |
| 7 | Sandbox | R$ 212 | R$ 191 | -9,7% | → Estavel |
| 8 | sz-comercial-branding | R$ 101 | R$ 127 | +25,4% | ↑ Leve alta |
| 9 | sz-hospedagem-geradorDeCodigos | R$ 24 | R$ 81 | +237,1% | ↑ Alta |

### Destaques por Projeto

**sz-shared-seazoneTools (68% do custo total)**

* Principal projeto de infraestrutura compartilhada
* Compute Engine e2-instances sao o maior custo (R$ 5.880/mes)
* Hospeda GKE, Cloud SQL PostgreSQL, Redis, Load Balancers
* Crescimento de storage PD (+35%) indica acumulo de discos

**sz-shared-tecnologia (crescimento de 237%)**

* Aumento inteiramente causado por Gemini API (modelo `gemini-3-pro-long`)
* Saiu de R$ 359 em Fev para projecao de R$ 1.210 em Mar
* Input tokens cached + long context indicam uso de RAG ou processamento de documentos grandes

**sz-shared-sia (projeto novo)**

* Novo projeto aparecendo em Marco com Cloud SQL + Redis
* Projecao de R$ 579/mes apenas com infraestrutura base
* Necessita governanca desde o inicio


---

## 5. Projecao Marco/2026 vs Fevereiro/2026 - Analise Detalhada

### 5.1 Metodologia de Projecao

A projecao foi calculada usando a media diaria dos primeiros 11 dias completos de Marco (01-11), extrapolada para 31 dias. O dia 12/Mar foi excluido por conter dados parciais. Essa abordagem linear e conservadora - custos baseados em uso (como Gemini API) podem variar significativamente.

### 5.2 Top 15 SKUs com Maior Aumento Projetado (Mar vs Fev)

| # | Servico | Projeto | SKU | Fev/2026 | Projecao Mar | Delta |
|----|----|----|----|----|----|----|
| 1 | Compute Engine | sz-shared-seazoneTools | E2 Instance Core (Americas) | R$ 2.673 | R$ 3.932 | +R$ 1.259 |
| 2 | Compute Engine | sz-shared-seazoneTools | E2 Instance RAM (Americas) | R$ 1.433 | R$ 2.108 | +R$ 675 |
| 3 | Gemini API | sz-shared-tecnologia | gemini-3-pro (long input) | R$ 31 | R$ 475 | +R$ 444 |
| 4 | Gemini API | sz-shared-tecnologia | gemini-3-pro (cached long input) | R$ 31 | R$ 379 | +R$ 349 |
| 5 | Cloud SQL | sz-shared-sia | PostgreSQL Storage (Americas) | R$ 0 | R$ 187 | +R$ 187 |
| 6 | Memorystore | sz-shared-sia | Redis M1 (Iowa) | R$ 0 | R$ 161 | +R$ 161 |
| 7 | Cloud SQL | sz-shared-sia | PostgreSQL vCPU (Americas) | R$ 0 | R$ 141 | +R$ 141 |
| 8 | Compute Engine | sz-shared-seazoneTools | Internet Data Transfer Out (SP) | R$ 27 | R$ 155 | +R$ 127 |
| 9 | Compute Engine | sz-shared-seazoneTools | Storage PD Capacity | R$ 312 | R$ 423 | +R$ 111 |
| 10 | Cloud SQL | sz-shared-sia | PostgreSQL RAM (Americas) | R$ 0 | R$ 90 | +R$ 90 |
| 11 | BigQuery | sz-dados-prd | Analysis (us-central1) | R$ 35 | R$ 96 | +R$ 61 |
| 12 | Cloud Run | sz-dados-prd | Services CPU (Request-based) | R$ 29 | R$ 75 | +R$ 46 |
| 13 | Gemini API | sz-shared-tecnologia | gemini-3-pro (long output) | R$ 4 | R$ 48 | +R$ 44 |
| 14 | BigQuery | sz-dados-prd | Cross-cloud AWS→GCP transfer | R$ 430 | R$ 473 | +R$ 43 |
| 15 | Backup for GKE | sz-shared-seazoneTools | Backup management V2 (Iowa) | R$ 0 | R$ 42 | +R$ 42 |

### 5.3 Analise de Tendencias e Motivacoes

#### Tendencia 1: Crescimento de Compute Engine (+R$ 1.727/mes projetado)

**O que esta acontecendo:**

* Instancias E2 no `sz-shared-seazoneTools` cresceram consistentemente desde Janeiro
* Storage PD e Balanced PD tambem estao crescendo, indicando provisionamento de novos discos
* Trafego de saida (Data Transfer Out) de Sao Paulo aumentou 5x

**Possiveis motivacoes:**

* Escalonamento do cluster GKE (mais nodes ou nodes maiores)
* Novas aplicacoes deployadas na infraestrutura compartilhada
* Workloads que antes estavam nos projetos antigos agora concentrados em um unico projeto
* Spot instances nao estao sendo utilizadas na proporcao ideal (apenas \~R$ 735 de \~R$ 6.000 em Compute)

**Risco:** Se mantida a tendencia de crescimento linear, Compute Engine atingira R$ 10.000/mes ate Junho/2026.

#### Tendencia 2: Explosao de Gemini API (+112% projetado)

**O que esta acontecendo:**

* `sz-shared-tecnologia`: uso massivo de `gemini-3-pro-long` com cached inputs (R$ 475/mes projetado)
* `sz-comercial-bizops`: pico de uso com `gemini-2.5-flash` e migracao para `gemini-3-pro`
* Picos extremos em dias especificos (R$ 362 em 10/Mar, R$ 121 em 05/Mar)
* Novos projetos adotando (sz-hospedagem-geradorDeCodigos, sz-comercial-branding com Veo3)

**Possiveis motivacoes:**

* Novos produtos/features usando IA generativa em producao
* Migracao de modelos (Flash → Pro) aumentando custo por token
* Ausencia de rate limiting ou quotas por projeto
* Uso de `long context` sugere processamento de documentos extensos (contratos, manuais)
* Geracao de video com Veo3 no branding (R$ 73/mes projetado)

**Risco:** Sem governanca, Gemini API pode facilmente ultrapassar R$ 3.000/mes no proximo trimestre.

#### Tendencia 3: Novos projetos sem otimizacao (sz-shared-sia)

**O que esta acontecendo:**

* Projeto novo aparecendo em Marco com Cloud SQL Zonal + Redis
* Projecao de R$ 579/mes apenas de infraestrutura base
* Sem uso de HA (Zonal, nao Regional), mas tambem sem otimizacao de custos

**Possiveis motivacoes:**

* Deploy de nova aplicacao (SIA) replicando padrao de infraestrutura existente
* Provisioned sem rightsizing adequado

#### Tendencia 4: Data Transfer cross-cloud crescente

**O que esta acontecendo:**

* BigQuery cross-cloud transfer AWS→GCP: R$ 430/mes em Fev, projecao R$ 473 em Mar
* Trafego de saida de Sao Paulo crescendo significativamente

**Possiveis motivacoes:**

* Pipeline de dados entre AWS e GCP transferindo volumes cada vez maiores
* Queries federadas cross-cloud sem otimizacao de particionamento


---

## 6. Analise por Projeto - Custo Detalhado

### 6.1 sz-shared-seazoneTools (Projecao: R$ 10.344/mes)

| Servico | Fev/2026 | Projecao Mar/2026 |
|----|----|----|
| Compute Engine (E2 instances) | R$ 4.107 | R$ 6.040 |
| Compute Engine (Spot E2) | R$ 735 | R$ 477\* |
| Compute Engine (Storage PD/Balanced) | R$ 569 | R$ 680 |
| Compute Engine (outros) | R$ 470 | R$ 562 |
| Cloud SQL PostgreSQL | R$ 871 | R$ 893 |
| Cloud Memorystore Redis | R$ 389 | R$ 389 |
| Kubernetes Engine | R$ 397 | R$ 397 |
| Cloud Logging | R$ 295 | R$ 210 |
| Networking | R$ 555 | R$ 689 |
| Cloud Monitoring | R$ 168 | R$ 184 |
| Outros | R$ 113 | R$ 124 |

\*Spot instances apresentam variacao por natureza (preemptible).

### 6.2 sz-dados-prd (Projecao: R$ 2.097/mes)

| Servico | Fev/2026 | Projecao Mar/2026 |
|----|----|----|
| BigQuery (cross-cloud + analysis) | R$ 674 | R$ 676 |
| Cloud SQL PostgreSQL | R$ 268 | R$ 268 |
| Cloud Run Functions | R$ 96 | R$ 96 |
| Networking (Cloud Armor + LB) | R$ 362 | R$ 393 |
| Vertex AI (Colab Storage) | R$ 181 | R$ 181 |
| Cloud Run | R$ 29 | R$ 75 |
| Outros | R$ 465 | R$ 408 |


---

## 7. Recomendacoes FinOps

As recomendacoes abaixo seguem o framework da **FinOps Foundation** e estao organizadas pelos dominios de **Inform, Optimize e Operate**.

### 7.1 INFORM - Visibilidade e Alocacao

#### R01: Implementar politica de labels obrigatorias

**Impacto:** Medio | **Esforco:** Baixo | **Prazo:** 1-2 semanas

Padronizar labels em todos os recursos para permitir alocacao de custos por equipe, ambiente e produto:

```yaml

labels:
  team: "dados" | "comercial" | "tecnologia" | "hospedagem"
  environment: "production" | "staging" | "development"
  product: "sia" | "investimentos" | "bizops" | "branding"
  cost-center: "<codigo-centro-custo>"
```

**Pratica FinOps:** *Tagging & Labeling Strategy* - Sem labels adequados, e impossivel fazer showback/chargeback e responsabilizar equipes pelos custos. Implementar via Organization Policy ou Terraform validation.

#### R02: Criar alertas de budget por projeto

**Impacto:** Alto | **Esforco:** Baixo | **Prazo:** 1 semana

Configurar alertas de orcamento no GCP Billing para cada projeto:

| Projeto | Budget Mensal Sugerido | Alerta 80% | Alerta 100% |
|----|----|----|----|
| sz-shared-seazoneTools | R$ 10.000 | R$ 8.000 | R$ 10.000 |
| sz-dados-prd | R$ 2.500 | R$ 2.000 | R$ 2.500 |
| sz-shared-tecnologia | R$ 800 | R$ 640 | R$ 800 |
| sz-shared-sia | R$ 600 | R$ 480 | R$ 600 |

**Pratica FinOps:** *Budget Management* - Budgets nao impedem gastos, mas criam accountability. Integrar alertas com Slack para visibilidade em tempo real.

#### R03: Configurar dashboard FinOps em Looker Studio

**Impacto:** Medio | **Esforco:** Medio | **Prazo:** 2-3 semanas

Criar um dashboard conectado ao BigQuery billing export com:

* Custo diario/mensal por projeto e servico
* Tendencias e anomalias automaticas
* Comparativo mes-a-mes
* Projecao de custo ao final do mes (burn rate)

**Pratica FinOps:** *Data-Driven Decision Making* - Transformar dados de billing em insights acionaveis para toda a organizacao.


---

### 7.2 OPTIMIZE - Reducao de Custos

#### R04: Committed Use Discounts (CUDs) para Compute Engine

**Impacto:** Alto | **Esforco:** Baixo | **Prazo:** 1 semana **Economia estimada:** R$ 1.200 a R$ 3.400/mes

O Compute Engine consome \~R$ 6.000/mes em instancias E2 on-demand. CUDs oferecem:

| Tipo de CUD | Desconto | Economia Estimada/Mes | Compromisso |
|----|----|----|----|
| 1 ano (spend-based) | 20% | R$ 1.200 | Gasto mensal minimo |
| 3 anos (spend-based) | 35% | R$ 2.100 | Gasto mensal minimo |
| 1 ano (resource-based) | 37% | R$ 2.220 | vCPU + RAM especificos |
| 3 anos (resource-based) | 57% | R$ 3.420 | vCPU + RAM especificos |

**Recomendacao:** Iniciar com CUD spend-based de 1 ano para cobrir o baseline de \~R$ 4.000/mes em E2 instances. Isso oferece flexibilidade (nao precisa especificar machine type) com desconto significativo.

**Pratica FinOps:** *Rate Optimization* - CUDs sao a alavanca de maior impacto para workloads estaveis. O GCP Recommender ja deve ter sugestoes - verificar em `gcloud recommender recommendations list`.

#### R05: Migrar workloads para Spot VMs onde possivel

**Impacto:** Alto | **Esforco:** Medio | **Prazo:** 2-4 semanas **Economia estimada:** R$ 600 a R$ 1.800/mes

Atualmente apenas \~12% do Compute Engine usa Spot instances (R$ 735 de R$ 6.040). Para workloads tolerantes a interrupcao (batch jobs, CI/CD, workers):

* Spot VMs oferecem **60-91% de desconto** vs on-demand
* GKE node pools podem ser configurados como Spot com `--spot`
* Ideal para: jobs de processamento de dados, pipelines de ML, builds

**Acao:** Identificar node pools do GKE que rodam workloads stateless e migrar para Spot node pools com fallback para on-demand.

**Pratica FinOps:** *Rate Optimization + Architecture Optimization* - Spot VMs sao a forma mais agressiva de reducao de custo em compute. Combinar com Pod Disruption Budgets no GKE para resiliencia.

#### R06: Rightsizing de VMs e Cloud SQL

**Impacto:** Medio | **Esforco:** Medio | **Prazo:** 2-3 semanas **Economia estimada:** R$ 300 a R$ 900/mes

Verificar recomendacoes de rightsizing do GCP:

```bash
# Verificar recomendacoes de rightsizing

gcloud recommender recommendations list \
  --project=tools-440117 \
  --location=us-central1-a \
  --recommender=google.compute.instance.MachineTypeRecommender
```

Para Cloud SQL:

* Verificar se as instancias PostgreSQL estao com CPU/RAM superdimensionados
* Considerar Cloud SQL Enterprise edition vs Enterprise Plus
* Avaliar se replicas de leitura sao necessarias

**Pratica FinOps:** *Usage Optimization* - Rightsizing e uma pratica continua, nao pontual. Ideal integrar ao ciclo de revisao mensal.

#### R07: Governanca de Gemini API

**Impacto:** Alto | **Esforco:** Medio | **Prazo:** 1-2 semanas **Economia estimada:** R$ 400 a R$ 1.000/mes

O uso de Gemini API esta crescendo sem governanca:

| Acao | Descricao | Impacto |
|----|----|----|
| Quotas por projeto | Limitar tokens/dia por projeto via API quotas | Previne gastos descontrolados |
| Downgrade de modelo | Usar `gemini-3-flash` ao inves de `gemini-3-pro` onde qualidade permite | 3-5x mais barato |
| Cache de respostas | Implementar cache aplicacional para prompts repetitivos | Reducao proporcional ao hit rate |
| Revisao de long context | Otimizar inputs longos - resumir antes de enviar ao modelo | Reducao direta de tokens |
| Rate limiting | Implementar throttling nos servicos que consomem a API | Previne picos |

**Pratica FinOps:** *Usage Optimization + Governance* - APIs de IA generativa sao o novo "cloud spend" descontrolado. Tratar com a mesma disciplina que se trata compute e storage.

#### R08: Otimizar BigQuery cross-cloud transfer

**Impacto:** Medio | **Esforco:** Medio | **Prazo:** 2-4 semanas **Economia estimada:** R$ 150 a R$ 300/mes

O cross-cloud data transfer AWS→GCP custa R$ 473/mes projetado:

* Avaliar se os dados podem ser replicados em batch (diario) ao inves de query-time
* Usar BigQuery BI Engine ou materialized views para dados frequentemente acessados
* Otimizar particionamento e clustering nas tabelas de destino
* Considerar mover a fonte de dados para GCP se o volume justificar

**Pratica FinOps:** *Architecture Optimization* - Data gravity e um dos maiores custos ocultos em ambientes multi-cloud.

#### R09: Limpar discos persistentes ociosos

**Impacto:** Baixo-Medio | **Esforco:** Baixo | **Prazo:** 1 semana **Economia estimada:** R$ 100 a R$ 300/mes

Storage PD e Balanced PD totalizam R$ 680/mes projetado com tendencia de crescimento:

```bash
# Listar discos nao attached

gcloud compute disks list \
  --filter="-users:*" \
  --format="table(name,zone,sizeGb,type,status)"
```

**Pratica FinOps:** *Waste Elimination* - Discos orfaos sao um dos desperdicios mais comuns em cloud. Automatizar deteccao com Cloud Asset Inventory.

#### R10: Desabilitar Network Intelligence Center (se nao utilizado)

**Impacto:** Baixo | **Esforco:** Baixo | **Prazo:** Imediato **Economia estimada:** R$ 248/mes

Network Intelligence Center consome R$ 248/mes (Topology + Analyzer + Internet Performance):

* Verificar se alguma equipe utiliza ativamente os dashboards
* Se nao, desabilitar via Console > Network Intelligence Center > Settings

**Pratica FinOps:** *Waste Elimination* - Servicos habilitados "por padrao" ou "para teste" que nunca sao desativados sao desperdicios recorrentes.


---

### 7.3 OPERATE - Governanca Continua

#### R11: Estabelecer ciclo de revisao FinOps mensal

**Impacto:** Alto | **Esforco:** Medio | **Prazo:** Continuo

Implementar uma reuniao mensal de revisao de custos (FinOps Review):

**Agenda sugerida (30 min):**


1. Custo total vs budget (5 min)
2. Top 5 servicos com maior variacao (10 min)
3. Novos projetos/recursos provisionados (5 min)
4. Status das acoes de otimizacao (5 min)
5. Decisoes e proximos passos (5 min)

**Participantes:** FinOps lead, Tech leads dos squads com maior custo, Infra/Platform

**Pratica FinOps:** *FinOps Culture* - A pratica de revisao continua e o que diferencia organizacoes que controlam custos daquelas que apenas reagem a surpresas na fatura.

#### R12: Implementar politicas preventivas

**Impacto:** Alto | **Esforco:** Medio | **Prazo:** 2-4 semanas

| Politica | Implementacao | Objetivo |
|----|----|----|
| Quota de Gemini API por projeto | API Quotas no Console | Prevenir gastos descontrolados de IA |
| Restricao de machine types | Organization Policy | Evitar provisionamento de VMs caras |
| Lifecycle de discos | Label + automation | Deletar discos sem uso apos 30 dias |
| Ambiente dev/staging auto-shutdown | Cloud Scheduler + Cloud Functions | Desligar recursos fora do horario comercial |
| Revisao de PR para Terraform | PR review com custo estimado (Infracost) | Awareness de custo antes do deploy |

**Pratica FinOps:** *Policy & Governance* - Prevenir e sempre mais barato que remediar. Integrar custo ao pipeline de desenvolvimento.

#### R13: Avaliar Sustained Use Discounts (SUDs) e Flex CUDs

**Impacto:** Medio | **Esforco:** Baixo | **Prazo:** Continuo

* SUDs sao aplicados automaticamente para VMs que rodam >25% do mes
* Verificar se os SUDs estao sendo aplicados corretamente
* Para workloads com variacao sazonal, avaliar Flex CUDs (compromisso de 1 mes)

**Pratica FinOps:** *Rate Optimization* - Combinar SUDs (automatico) + CUDs (comprometido) + Spot (oportunistico) para criar uma estrategia de pricing em camadas.


---

## 8. Plano de Acao Priorizado

### Acoes Imediatas (proximas 2 semanas)

| Prioridade | Acao | Economia Estimada/Mes | Esforco |
|----|----|----|----|
| P0 | R10: Desabilitar Network Intelligence Center | R$ 248 | 1 hora |
| P0 | R02: Criar alertas de budget | Prevencao | 2 horas |
| P1 | R07: Implementar quotas de Gemini API | R$ 400-1.000 | 1-2 dias |
| P1 | R09: Limpar discos ociosos | R$ 100-300 | 2 horas |
| P1 | R04: Contratar CUD spend-based 1 ano | R$ 1.200 | 1 hora |

### Acoes de Curto Prazo (proximo mes)

| Prioridade | Acao | Economia Estimada/Mes | Esforco |
|----|----|----|----|
| P1 | R05: Migrar node pools GKE para Spot | R$ 600-1.800 | 1-2 semanas |
| P1 | R06: Rightsizing de VMs e Cloud SQL | R$ 300-900 | 1-2 semanas |
| P2 | R01: Implementar politica de labels | Governanca | 1-2 semanas |
| P2 | R08: Otimizar BigQuery cross-cloud | R$ 150-300 | 2-3 semanas |

### Acoes de Medio Prazo (proximo trimestre)

| Prioridade | Acao | Economia Estimada/Mes | Esforco |
|----|----|----|----|
| P2 | R03: Dashboard FinOps em Looker Studio | Visibilidade | 2-3 semanas |
| P2 | R12: Politicas preventivas (Org Policy) | Prevencao | 2-4 semanas |
| P3 | R11: Ciclo de revisao FinOps mensal | Cultura | Continuo |
| P3 | R13: Avaliar Flex CUDs | Variavel | Continuo |

### Economia Total Estimada

| Cenario | Economia Mensal | Economia Anual |
|----|----|----|
| Conservador (apenas P0+P1 imediatos) | R$ 1.948 - R$ 2.748 | R$ 23.376 - R$ 32.976 |
| Moderado (todos P0+P1) | R$ 2.848 - R$ 5.448 | R$ 34.176 - R$ 65.376 |
| Agressivo (todas as acoes) | R$ 3.000 - R$ 6.248 | R$ 36.000 - R$ 74.976 |

Considerando o custo projetado de \~R$ 15.300/mes, as acoes combinadas podem representar uma reducao de **19% a 41%** na fatura mensal.


---

## 9. Apendice

### 9.1 Queries Utilizadas

As consultas BigQuery utilizadas nesta analise estao no dataset:

```
platform-finops-483715.billing_export.gcp_billing_export_v1_012829_B5239B_729286
```

### 9.2 Limitacoes da Analise

* **Projecao linear:** A projecao de Marco assume que o padrao dos primeiros 11 dias se manterra. Servicos baseados em uso (Gemini API, BigQuery) podem variar significativamente.
* **Creditos e descontos:** Creditos promocionais ou SUDs automaticos podem alterar os valores finais.
* **Migracao de projetos:** A comparacao historica (Dez→Jan) e afetada pela migracao entre projetos. A analise mais confiavel e Fev→Mar.
* **Dados parciais de Marco/12:** O ultimo dia do dataset (12/Mar) contem dados parciais e foi incluido na media, podendo subestimar levemente a projecao.

### 9.3 Glossario FinOps

| Termo | Descricao |
|----|----|
| **CUD** | Committed Use Discount - desconto por compromisso de uso (1 ou 3 anos) |
| **SUD** | Sustained Use Discount - desconto automatico para uso >25% do mes |
| **Spot VM** | VM com preco reduzido (60-91%) que pode ser preemptada pelo GCP |
| **Rightsizing** | Ajustar recursos (CPU/RAM) ao uso real da aplicacao |
| **Showback/Chargeback** | Pratica de alocar custos de cloud a equipes/centros de custo |
| **Burn Rate** | Taxa de consumo diaria projetada para estimar custo ao final do mes |
| **Data Gravity** | Tendencia de dados atrairem servicos e custos de transferencia |

### 9.4 Referencias

* [FinOps Foundation Framework](https://www.finops.org/framework/)
* [GCP Cost Optimization Best Practices](https://cloud.google.com/architecture/cost-optimization)
* [GCP Committed Use Discounts](https://cloud.google.com/compute/docs/instances/committed-use-discounts-overview)
* [GCP Active Assist Recommenders](https://cloud.google.com/recommender/docs/recommenders)


---

*Documento gerado automaticamente via analise do BigQuery Billing Export em 12/03/2026.*



---

## 10. Análise do Cluster GKE — Plano de Remoção

> **Data da análise:** 02 de abril de 2026 **Fonte:** kubectl + relatório de billing acima **Contexto:** Workloads confirmados para remoção: n8n, Outline, Baserow. Objetivo final: remoção completa do cluster.


---

### 10.1 Estado Atual do Cluster `cluster-tools`

**Node Pools:**

| Pool | Tipo | Qtd | vCPU | RAM |
|----|----|----|----|----|
| `tools-prod-pool` | e2-standard-2 | 19 | 38 | 152 GB |
| `ingress-prod-pool` | e2-standard-2 | 3 | 6 | 24 GB |
| **Total** |    | **22** | **44** | **176 GB** |

Utilização observada: 60–66% de CPU na maioria dos nodes — explicado pelo Baserow (10 réplicas celery + 10 wsgi) e N8N (6 webhooks + 6 workers).


---

### 10.2 Inventário de Workloads

| Namespace | Workload | Status | Decisão |
|----|----|----|----|
| `prd-n8n` | n8n-editor, mcp, webhooks (×6), workers (×6) | Running | **REMOVER** |
| `outline` | outline (×5 réplicas) | Running | **REMOVER** |
| `baserow` | asgi (×2), celery (×10), frontend (×2), wsgi (×10) | Running | **REMOVER** |
| `kestra-poc` | — | Namespace vazio | Deletar namespace |
| `incident-agent` | incident-agent | **ImagePullBackOff** (quebrado, 4d) | Deletar |
| `passbolt` | passbolt-depl-srv | Running | Migrar antes de remover o cluster |
| `monitoring` | Loki stack (12+ pods, 80 GB PVCs) | Running | Migrar para Cloud Logging nativo |
| `external-secrets` | operator + cert + webhook | Running | Remove junto com o cluster |
| `traefik-system` | traefik + LB externo (`35.225.201.214`) | Running | Remove junto com o cluster |
| `ecr-token-refresher` | — | Running | Remove junto com o cluster |


---

### 10.3 Custo Atual Atribuível ao Cluster GKE

Com base nos dados de billing de março/2026 (projeto `sz-shared-seazoneTools`):

| Item | Custo/mês |
|----|----|
| Compute Engine E2 on-demand (22 nodes) | R$ 6.040 |
| Compute Engine Spot E2 | R$ 477 |
| Kubernetes Engine (management fee) | R$ 397 |
| Storage PD (PVCs Loki + Traefik = 81 GB) | R$ 680 |
| Load Balancer Traefik (NLB + IP externo) | \~R$ 150 |
| Backup for GKE | R$ 48 |
| Cloud Logging (atribuído ao GKE) | \~R$ 100 |
| **Subtotal GKE direto** | **\~R$ 7.892** |
| Cloud SQL (DBs de n8n / outline / baserow) | \~R$ 400 |
| Memorystore Redis (n8n / baserow) | \~R$ 200 |
| **Total removível com o cluster** | **\~R$ 8.492/mês** |

Representa **\~55% do custo total projetado de R$ 15.267/mês**.


---

### 10.4 Plano de Remoção em 3 Fases

#### Fase 1 — Remover workloads confirmados

**Ação:** Deletar namespaces de n8n, Outline e Baserow (e os já inativos kestra-poc e incident-agent).

**Efeito esperado:** O cluster recua de 22 para \~3–4 nodes. Economia imediata de **\~R$ 5.500–6.000/mês** em compute.

Junto com a remoção dos namespaces, deletar os recursos Cloud SQL e Redis associados:

* Cloud SQL: databases de outline, n8n e baserow
* Memorystore Redis: instâncias de n8n e baserow

#### Fase 2 — Resolver dependências remanescentes

**Passbolt (gerenciador de senhas):**

Opções para migração antes de remover o cluster:

* **Opção A (recomendada):** Migrar para SaaS — Bitwarden Teams ou 1Password (\~R$ 80–150/mês para o time, sem infra)
* **Opção B:** Mover para VM e2-micro isolada fora do GKE (\~R$ 50/mês)
* **Opção C:** Mover para o cluster EKS (se houver capacidade disponível)

**Loki Stack (observabilidade):**

O GCP já cobra R$ 210/mês em Cloud Logging nativo. Migrar os logs para Cloud Logging elimina o Loki e economiza R$ 680/mês em PVCs + compute dos pods.

* Alternativa externa: Grafana Cloud (free tier cobre até 50 GB/mês de logs)

#### Fase 3 — Remoção completa do cluster

Após Passbolt e Loki migrados:


1. Deletar todos os namespaces remanescentes
2. Deletar o cluster GKE (`cluster-tools`)
3. Limpar discos persistentes órfãos
4. Remover IP externo do Traefik
5. Atualizar/remover registros DNS que apontam para `35.225.201.214`


---

### 10.5 Pré-requisitos antes de iniciar

| # | Pré-requisito | Responsável |
|----|----|----|
| 1 | Backup dos dados de N8N (workflows, credentials) | — |
| 2 | Backup dos documentos do Outline | — |
| 3 | Backup dos dados do Baserow | — |
| 4 | Snapshot final dos Cloud SQL antes de deletar | — |
| 5 | Confirmar usuários do Passbolt e escolher destino | — |
| 6 | Definir estratégia de observabilidade pós-Loki | — |
| 7 | Atualizar registros DNS (`35.225.201.214`) | — |
| 8 | Verificar se algum ExternalSecret do cluster é compartilhado com outros sistemas | — |


---

### 10.6 Projeção de Economia

| Cenário | Economia/mês | % do custo total |
|----|----|----|
| Apenas remover n8n + Outline + Baserow | \~R$ 5.500 | \~36% |
| Remover cluster inteiro (sem resolver Passbolt/Loki) | \~R$ 7.892 | \~52% |
| Remover cluster + SQL/Redis dos apps removidos | **\~R$ 8.492** | **\~55%** |

**Fatura GCP estimada pós-remoção completa: \~R$ 6.800/mês** (vs. R$ 15.267 atual)

Custo residual permanente (não relacionado ao cluster):

* Gemini API: R$ 1.717
* Networking: R$ 1.177
* BigQuery: R$ 848
* Cloud SQL (outros projetos): \~R$ 493
* Cloud Run + Functions: R$ 268
* Memorystore remanescente: \~R$ 189
* Outros: \~R$ 883

\n


---

## 11. Auditoria de Recursos Ociosos — Todos os Projetos

> **Data:** 02/04/2026 | **Fonte:** gcloud CLI — varredura direta nos projetos com billing ativo


---

### 11.1 tools-440117 — sz-shared-seazoneTools

#### VMs Standalone (fora do GKE)

| VM | Tipo | Zona | Custo Est./mês | Observação |
|----|----|----|----|----|
| `vault` | e2-medium | us-central1-a | \~R$ 130 | Vault rodando como VM standalone |
| `uptime-kuma-instance` | e2-small | us-central1-c | \~R$ 65 | Monitoramento — avaliar migrar para Cloud Run |
| `vpn-k8s5` | e2-standard-2 | southamerica-east1-a | \~R$ 200 | **Criada em 30/03/2026 (3 dias)** — confirmar necessidade |

**Ação:** Confirmar propósito de `vpn-k8s5` (nova, custo relevante de \~R$ 200/mês). Avaliar migrar `uptime-kuma` para Cloud Run (paga só por requisição).

#### Discos Persistentes Órfãos

| Disco | Tamanho | Custo Est./mês | Observação |
|----|----|----|----|
| `pvc-9dcd395d-...` | 20 GB pd-balanced | \~R$ 8 | PVC desanexado — **remover** |
| `pvc-d4529db7-...` | 1 GB pd-balanced | \~R$ 0,40 | PVC do Traefik — remover com cluster |

#### Redis Instances

| Nome | Custo Est./mês | Observação |
|----|----|----|
| `baserow` (1 GB BASIC) | \~R$ 100 | Remover com Baserow (Fase 1, Semana 4) |
| `redis-tools` (1 GB BASIC) | \~R$ 100 | **Verificar uso** — nome genérico, qual app usa? |

#### Snapshots — Candidatos à Limpeza

| Grupo | Qtd | Disco Declarado | Storage Real | Ação |
|----|----|----|----|----|
| Pritunl Mongo (Dez/2025) | 14 | 1.400 GB | \~0 bytes comprimido | **Remover** — Pritunl desativado, dados vazios |
| Pritunl legacy (Jan/2025) | 2 | 200 GB | \~6 MB | **Remover** — mais de 1 ano de idade |
| N8N incidente/backup (Fev–Mar/2026) | 5 | \~157 GB | \~11 GB comprimido | Remover após Fase 1 do cluster |
| VPN Pritunl config disk (Fev/2026) | 1 | 20 GB | 5,9 GB | **Remover** — VPN migrada para `vpn-k8s5` |
| Snapshots pré-migração (Mar/2026) | 2 | 100 GB | \~3 GB | Remover após validar migração concluída |
| Uptime Kuma rolling (3 dias) | 3 | 30 GB | \~4 GB | Manter — backup ativo, retention ok |
| Vault rolling (3 dias) | 3 | 30 GB | \~1,5 GB | Manter — backup ativo |
| Mongo Pritunl VPN rolling (2 dias) | 2 | 200 GB | \~8,3 GB | Revisar retention — 100 GB/snap/dia é custoso |

**Economia estimada removendo snapshots obsoletos:** \~R$ 50–150/mês.


---

### 11.2 seazone-sia — sz-shared-sia

| Recurso | Custo Est./mês | Observação |
|----|----|----|
| Cloud SQL `postgres-sia` (PostgreSQL 18, Zonal) | \~R$ 418 | Projeto novo, sem rightsizing. Aguardar 30 dias de métricas para ajustar. |
| Redis `redis-sia` (BASIC, 1 GB) | \~R$ 161 | Ok para início — reavaliar após 30 dias |


---

### 11.3 data-resources-448418 — sz-dados-prd

#### IP Estático Global Suspeito

| Recurso | IP | Custo Est./mês | Observação |
|----|----|----|----|
| `ip-mapa-terrenos` | 34.160.157.188 (global) | \~R$ 35 | Verificar se está em uso — IP global sem LB visível associado no projeto |

#### Cloud Run Services com Prefixo "test-" (candidatos a remoção)

* `test-calculate-competitors-category`
* `test-data-alerts-kpis`
* `test-health-status-clusters`
* `test-min-stay-kpi`
* `hackaton-marcio-dashboard`
* `system-price-backtest`

**Cloud Run não cobra em repouso**, mas storage de imagens no Artifact Registry tem custo. Auditar tráfego dos últimos 30 dias e deletar os sem requisições.

#### Cloud Functions Gen1 Duplicadas

Existem \~40 Cloud Functions Gen1 com nomes idênticos aos Cloud Run services Gen2. Indica migração Gen1 → Gen2 incompleta. As Gen1 devem ser desativadas após confirmar que o tráfego está nas versões Gen2.

**Economia estimada:** R$ 30–80/mês em storage + execuções residuais.


---

### 11.4 sandbox-439302 — Sandbox

#### Load Balancer Global em Ambiente Sandbox

| Recurso | IP | Custo Est./mês | Observação |
|----|----|----|----|
| `lb-mapa-terrenos` (HTTPS Global LB) | 34.8.15.36 | \~R$ 80–100 | **LB global pago em Sandbox** — paga mesmo sem tráfego |

**Ação:** Avaliar migrar o mapa de terrenos para usar Cloud Run diretamente (sem LB dedicado) ou mover para ambiente de produção com LB compartilhado.

#### Cloud Run de Teste/Hackathon (candidatos a remoção)

* `hello`, `scraper-test`, `function-1` — testes iniciais sem uso
* `bizops-defense-system-mario-edition` — hackathon
* `cfo-innovation-hub` — POC
* `maria` — sem contexto
* `seazone-yield` — possível duplicata do projeto principal

**Ação:** Auditar últimas 4 semanas de tráfego. Deletar os sem requisições.


---

### 11.5 seazone-investimentos — sz-comercial-investimentos

| Recurso | Custo Est./mês | Observação |
|----|----|----|
| Cloud SQL `investimento-mysql` (MySQL, Zonal) | \~R$ 200–250 | Projeto com custo caindo (-8,3%). **Confirmar se produto ainda usa ativamente.** |

**Ação:** Se o produto de investimentos não usa mais este banco, candidato a desligamento ou downgrade de tier significativo.


---

### 11.6 seazone-bizops — sz-comercial-bizops

#### Cloud Run — Múltiplas Versões do Sistema de Comissionamento

7 serviços relacionados ao mesmo domínio coexistindo — provável acúmulo de versões:

* `comiss-opro-sistema-de-comissionamento`
* `comissionamento-comercial`
* `copy-of-guia-oficial-de-comiss-es-seazone`
* `guia-oficial-de-comiss-es-seazone`
* `seazone-commission-guide`
* `sistema-de-comissionamento-comercial`
* `sistema-de-comissionamento-teste`

**Ação:** Consolidar para 1–2 serviços ativos. Deletar versões antigas e cópias.


---

### 11.7 Resumo — Economia Adicional Identificada (excluindo cluster)

| Item | Projeto | Economia Est./mês |
|----|----|----|
| Network Intelligence Center | sz-shared | R$ 248 |
| Snapshots Pritunl antigos (16+ snaps) | tools-440117 | R$ 30–80 |
| Snapshots N8N/incidente (pós Fase 1) | tools-440117 | R$ 20–50 |
| Disco orfão `pvc-9dcd395d` (20 GB) | tools-440117 | R$ 8 |
| VM `vpn-k8s5` (confirmar necessidade) | tools-440117 | R$ 0–200 |
| Redis `redis-tools` (verificar uso) | tools-440117 | R$ 0–100 |
| LB global Sandbox | sandbox-439302 | R$ 80–100 |
| IP estático `ip-mapa-terrenos` (verificar) | data-resources-448418 | R$ 0–35 |
| Cloud Functions Gen1 duplicadas | data-resources-448418 | R$ 30–80 |
| Cloud Run de teste/hackathon | múltiplos | R$ 20–50 |
| Cloud SQL MySQL investimentos (verificar) | seazone-investimentos | R$ 0–250 |
| **Total adicional** |    | **R$ 436 – R$ 1.201/mês** |


---

### 11.8 Plano de Ações Ordenado — Visão Completa

| # | Ação | Economia/mês | Esforço | Quando |
|----|----|----|----|----|
| 1 | Desabilitar Network Intelligence Center | R$ 248 | 1h | **Imediato** |
| 2 | Deletar snapshots Pritunl antigos (16 snaps) | R$ 30–80 | 1h | **Imediato** |
| 3 | Deletar disco orfão `pvc-9dcd395d` | R$ 8 | 15min | **Imediato** |
| 4 | Confirmar/justificar VM `vpn-k8s5` (3 dias de vida) | R$ 0–200 | 1h | **Urgente** |
| 5 | Verificar uso de `redis-tools` | R$ 0–100 | 1h | Semana 1–2 |
| 6 | Desativar Cloud Functions Gen1 duplicadas | R$ 30–80 | 2h | Semana 1–2 |
| 7 | Auditar e deletar Cloud Run inativos (Sandbox + bizops) | R$ 20–50 | 2h | Semana 1–2 |
| 8 | Avaliar LB global do Sandbox | R$ 80–100 | 4h | Semana 2–3 |
| 9 | Verificar IP estático `ip-mapa-terrenos` | R$ 0–35 | 30min | Semana 2 |
| 10 | Verificar Cloud SQL MySQL (investimentos) | R$ 0–250 | 2h | Semana 2–3 |
| 11 | **\[CLUSTER\] Fase 1: Remover n8n + Outline + Baserow** | R$ 5.500–6.000 | 1 dia | **Semana 4** |
| 12 | \[CLUSTER\] Migrar Passbolt para SaaS/VM | — | 2–3 dias | Semana 5–6 |
| 13 | \[CLUSTER\] Migrar Loki → Cloud Logging nativo | R$ 680 (PVCs) | 1 semana | Semana 5–6 |
| 14 | \[CLUSTER\] Deletar snapshots N8N pós-remoção | R$ 20–50 | 30min | Semana 4+ |
| 15 | **\[CLUSTER\] Fase 3: Deletar cluster GKE completo** | R$ 7.892 total | 2h | Semana 7+ |


---

### 11.9 Projeção de Economia Total Combinada

| Cenário | Economia/mês | Fatura Estimada Pós-Ação |
|----|----|----|
| Ações imediatas (itens 1–4) | R$ 286 – R$ 536 | \~R$ 14.700 |
| Semanas 1–3 (itens 1–10) | R$ 436 – R$ 1.201 | \~R$ 14.100 |
| Semana 4 + Fase 1 cluster | R$ 5.936 – R$ 7.201 | \~R$ 8.100 |
| Semana 7+ + Remoção completa | **R$ 8.928 – R$ 9.685** | **\~R$ 5.600 – R$ 6.300** |

## **Redução total esperada: 58–63% da fatura atual** ao concluir todas as ações.

## 12. Panorama de Custos Real — Março/2026

> **Fonte:** BigQuery Billing Export — dados reais **Total real março/2026: R$ 18.472** (projeção do relatório de 12/03 era R$ 15.267 — 21% abaixo do real)

### 12.1 Evolução Mensal 2026

| Mês | Custo Real |
|----|----|
| Janeiro | R$ 17.006 |
| Fevereiro | R$ 12.617 |
| **Março** | **R$ 18.472** |
| Abril (1 dia) | R$ 1.063/dia |

### 12.2 Custo por Serviço — Março Real

| Serviço | R$/mês | % |
|----|----|----|
| Compute Engine | R$ 8.639 | 46,8% |
| Gemini API | R$ 2.068 | 11,2% |
| Cloud SQL | R$ 1.999 | 10,8% |
| Networking | R$ 1.332 | 7,2% |
| Cloud Logging | R$ 1.008 | 5,5% |
| BigQuery | R$ 988 | 5,3% |
| Cloud Memorystore Redis | R$ 628 | 3,4% |
| Kubernetes Engine | R$ 436 | 2,4% |
| Cloud Run | R$ 324 | 1,8% |
| Cloud Monitoring | R$ 312 | 1,7% |
| Vertex AI | R$ 222 | 1,2% |
| Maps API | R$ 147 | 0,8% |
| Cloud Run Functions | R$ 137 | 0,7% |
| Backup for GKE | R$ 53 | 0,3% |
| Outros | R$ 179 | 1,0% |
| **TOTAL** | **R$ 18.472** |    |

### 12.3 Custo por Projeto — Março Real

| Projeto | R$/mês | Principal driver |
|----|----|----|
| sz-shared-seazoneTools | R$ 12.403 | GKE cluster (22 nodes) |
| sz-dados-prd | R$ 2.400 | BigQuery + Cloud Run |
| sz-shared-sia | R$ 716 | Cloud SQL + Redis (novo) |
| sz-shared-tecnologia | R$ 569 | Gemini API |
| sz-comercial-branding | R$ 481 | Gemini API (Veo3) |
| Sandbox | R$ 426 | Cloud Run + Networking |
| sz-comercial-investimentos | R$ 296 | Cloud SQL MySQL |
| sz-comercial-bizops | R$ 284 | Gemini API + Cloud Run |
| sz-shared-financeiro | R$ 210 | Gemini API |
| sz-reservas-site | R$ 135 | Maps API |
| Outros | R$ 272 | — |
| **TOTAL** | **R$ 18.472** |    |

### 12.4 Detalhamento sz-shared-seazoneTools (67% do gasto total)

| Item | R$/mês | Remove com cluster? |
|----|----|----|
| GKE nodes E2 core (19 nodes) | R$ 4.270 | ✅ |
| GKE nodes E2 RAM (19 nodes) | R$ 2.289 | ✅ |
| Cloud Logging — logs do cluster | R$ 1.008 | ✅ |
| Cloud SQL (DBs dos apps) | R$ 861 | ✅ maioria |
| Networking (NAT, NLB, NIC, transfer) | R$ 779 | ✅ parcial |
| Kubernetes Engine — management fee | R$ 436 | ✅ |
| Redis — baserow + redis-tools | R$ 427 | ✅ |
| Cloud Monitoring — Prometheus | R$ 312 | ✅ parcial |
| Spot E2 core + RAM | R$ 378 | ✅ |
| VMs standalone (vault, uptime-kuma, vpn) | R$ 241 | ❌ ficam |
| Storage PD / Balanced PD | R$ 372 | ✅ maioria |
| Backup for GKE | R$ 53 | ✅ |
| Outros | R$ 277 | ✅ parcial |
| **Total** | **R$ 12.403** |    |


---

## 13. Plano de Execução e Redução de Custos

> **Ponto de partida:** R$ 18.472/mês | **Meta:** \~R$ 6.000/mês em 7 semanas

### 13.1 Fases de Execução

| Fase | Quando | O que fazer | Economia | Fatura Estimada |
|----|----|----|----|----|
| **0 — Imediato** | Semanas 1–3 | Desabilitar Network Intelligence Center, deletar disco órfão `pvc-9dcd395d`, limpar snapshots Pritunl antigos | **-R$ 421** | R$ 18.051 |
| **1 — Remover apps** | Semana 4 | Deletar namespaces n8n + Outline + Baserow + kestra-poc + incident-agent. Deletar Cloud SQL e Redis associados | **-R$ 7.800** | R$ 10.251 |
| **2 — Migrar dependências** | Semanas 5–6 | Migrar Passbolt para SaaS. Migrar Loki para Cloud Logging nativo | **-R$ 700** | R$ 9.551 |
| **3 — Deletar cluster** | Semana 7+ | Remover cluster GKE completo. Limpar PVCs, IPs e LB residuais | **-R$ 2.700** | R$ 6.851 |
| **4 — Otimizações** | Mês 3+ | Governança Gemini API, remover LB Sandbox, desativar Cloud Functions Gen1 | **-R$ 780** | \~R$ 6.071 |

### 13.2 O Que Permanece Após Remoção do Cluster

| Item | R$/mês |
|----|----|
| sz-dados-prd (BigQuery, Cloud Run, SQL, Vertex AI) | R$ 2.400 |
| Gemini API — todos os projetos | R$ 2.068 |
| sz-shared-sia (Cloud SQL + Redis) | R$ 716 |
| sz-comercial-branding (Veo3 + outros) | R$ 481 |
| Sandbox (Cloud Run + Networking) | R$ 426 |
| sz-comercial-investimentos (Cloud SQL MySQL) | R$ 296 |
| sz-comercial-bizops (Cloud Run + Gemini) | R$ 284 |
| sz-shared-financeiro | R$ 210 |
| sz-reservas-site (Maps API) | R$ 135 |
| VMs standalone tools (vault + uptime-kuma + vpn) | R$ 395 |
| Cloud SQL residual tools | R$ 260 |
| Networking residual tools | R$ 280 |
| Cloud Logging + Monitoring residual | R$ 197 |
| Outros | R$ 195 |
| **Total residual** | **\~R$ 8.343** |

Com governança de Gemini (–40% = –R$ 800): **\~R$ 7.500/mês**

### 13.3 Visão de Redução

```
Mar/26:  R$ 18.472  ██████████████████████████████████████████
Sem 1-3: R$ 18.051  █████████████████████████████████████████  (-R$   421)
Sem 4:   R$ 10.251  ████████████████████████  (-R$ 7.800 — maior impacto)
Sem 5-6: R$  9.551  ██████████████████████  (-R$   700)
Sem 7+:  R$  6.851  ████████████████  (-R$ 2.700 — cluster deletado)
Mês 3+:  R$  6.071  ██████████████  (-R$   780 — otimizações)
```

### 13.4 Resumo Executivo

|    |    |
|----|----|
| Custo atual (março/2026) | R$ 18.472/mês |
| Meta após plano completo | **\~R$ 6.071/mês** |
| Redução total | **R$ 12.401/mês (–67%)** |
| Economia anual | **\~R$ 148.800** |
| Maior alavanca única | Semana 4: remover n8n + Outline + Baserow (–R$ 7.800 em 1 dia) |
| Principal fonte de gasto residual | BigQuery + Cloud Run em sz-dados-prd (R$ 2.400 — necessários) |