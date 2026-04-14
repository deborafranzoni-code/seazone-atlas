<!-- title: Análise FinOps: Compute Engine GCP — CUD, Spot Migration e Rightsizing | url: https://outline.seazone.com.br/doc/analise-finops-compute-engine-gcp-cud-spot-migration-e-rightsizing-B8Jeai6oRn | area: Tecnologia -->

# Análise FinOps: Compute Engine GCP — CUD, Spot Migration e Rightsizing

> **Ref:** [SRE-5048](https://seazone.atlassian.net/browse/SRE-5048) | Análise realizada em 2026-03-17 com dados reais de utilização do cluster GKE e instâncias standalone.


---

## 1. Visão Geral do Ambiente

### 1.1 Cluster GKE — `cluster-tools-prod-gke` (projeto `tools-440117`)

| Node Pool | Machine Type | Nodes | Provisionamento | Custo est./mês |
|----|----|----|----|----|
| `tools-prod-pool` | e2-standard-2 (2 vCPU, 8 GB) | 18 | **ON-DEMAND** | \~$881 |
| `ingress-prod-pool` | e2-standard-2 (2 vCPU, 8 GB) | 3 | **ON-DEMAND** | \~$147 |
| `nodepool-default-spot` | e2-standard-4 (4 vCPU, 16 GB) | 1 | SPOT | \~$29 |
|    |    | **22 nodes** |    | **\~$1.057** |

### 1.2 VMs Standalone

| VM | Machine Type | Zona | Provisionamento | Custo est./mês |
|----|----|----|----|----|
| `vault` | e2-medium (1 vCPU, 4 GB) | us-central1-a | ON-DEMAND | \~$24 |
| `uptime-kuma-instance` | e2-small (0.5 vCPU, 2 GB) | us-central1-c | ON-DEMAND | \~$12 |
| `vpn-pqdt` | e2-medium (1 vCPU, 4 GB) | southamerica-east1-a | ON-DEMAND | \~$24 |

### 1.3 Outros projetos

| Projeto | Recurso | Custo est./mês |
|----|----|----|
| `data-resources-448418` | 1x e2-micro (proxy-relay) | \~$6 |

> **Total Compute on-demand: \~$1.088/mês**


---

## 2. Mapeamento de Aplicações por Node Pool

Todas as aplicações abaixo rodam em nodes **on-demand**, exceto onde indicado.

### 2.1 Baserow (24 pods — **maior consumidor do cluster**)

| Componente | Réplicas | Pool | CPU Request | MEM Request | CPU Real | MEM Real | HPA |
|----|----|----|----|----|----|----|----|
| `baserow-asgi` | **12** | ON-DEMAND | 100m cada | 1Gi cada | **\~10m cada** | **\~830Mi cada** | max 12, **atingiu max** (mem 81%) |
| `baserow-wsgi` | **10** | ON-DEMAND | 100m cada | 750Mi cada | **\~3m cada** | **\~647Mi cada** | max 10, **quase max** (mem 86%) |
| `baserow-frontend` | 2 | ON-DEMAND | 1000m cada | 1Gi cada | \~335m cada | \~540Mi cada | max 10 |
| `baserow-celery` | 1 | **SPOT** | 3x1000m | 3x1800Mi | 711m total | 786Mi total | max 10 |

> **Total Baserow on-demand: 24 pods = \~10 GB MEM request + \~22 GB MEM request = \~19.5 GB de MEM consumindo \~21 nodes**

### 2.2 N8N — 3 ambientes (32 pods no total, **todos on-demand**)

| Namespace | Componente | Réplicas | CPU Real | MEM Real | HPA |
|----|----|----|----|----|----|
| `n8n` | editor | 1 | 21m | 474Mi | — |
| `n8n` | webhooks | 2 | \~4m cada | \~268Mi cada | — |
| `n8n` | workers | **6** | \~20m cada | \~442Mi cada | max 8 (mem 87%) |
| `n8n` | postgres + redis | 2 | 14m total | 30Mi total | — |
| `prd-n8n` | editor | 1 | 97m | 520Mi | — |
| `prd-n8n` | mcp | 1 | 2m | 169Mi | — |
| `prd-n8n` | webhooks | **6** | \~2m cada | \~279Mi cada | max 6, **atingiu max** (mem 104%) |
| `prd-n8n` | workers | **6** | \~30m cada | \~522Mi cada | max 6, **atingiu max** (mem 101%) |
| `dev-n8n` | editor + mcp + hooks | 3 | \~10m total | 370Mi total | — |
| `dev-n8n` | webhooks | 3 | \~2m cada | \~205Mi cada | max 3, **atingiu max** |
| `dev-n8n` | workers | 2 | \~10m cada | \~214Mi cada | max 3 |
| `dev-n8n` | postgres + redis | 2 | 17m total | 43Mi total | — |

### 2.3 Monitoring — Loki (17 pods, **todos on-demand**)

| Componente | Réplicas | CPU Real | MEM Real | MEM Request |
|----|----|----|----|----|
| `loki-write` | 4 | \~78m cada | \~343Mi cada | 900Mi cada |
| `loki-backend` | 4 | \~18m cada | \~203Mi cada | 200Mi cada |
| `loki-read` | 4 | \~42m cada | \~383Mi cada | 1Gi cada |
| `loki-chunks-cache` | 1 | 6m | 2071Mi | 2458Mi |
| `loki-results-cache` | 1 | 5m | 38Mi | 1229Mi |
| `loki-gateway` | 1 | 22m | 13Mi | 128Mi |
| `promtail` (DaemonSet) | 21 | \~100m cada | \~64Mi cada | — |

### 2.4 Outline (4 pods, **todos on-demand**)

| Componente | Réplicas | CPU Real | MEM Real | MEM Request |
|----|----|----|----|----|
| `outline` | 4 | **\~5m cada** | \~938Mi cada | 600Mi cada |

> Outline é stateless e tolerante a interrupção. Não precisa de on-demand.

### 2.5 Kestra POC (5 pods, **todos on-demand, SEM resource requests**)

| Componente | Réplicas | CPU Real | MEM Real | MEM Request |
|----|----|----|----|----|
| `kestra-executor` | 1 | 19m | 937Mi | **nenhum** |
| `kestra-indexer` | 1 | 7m | 883Mi | **nenhum** |
| `kestra-scheduler` | 1 | 18m | 904Mi | **nenhum** |
| `kestra-webserver` | 1 | 7m | 881Mi | **nenhum** |
| `kestra-worker` | 1 | 10m | 1179Mi | **nenhum** |

> Kestra consome \~4.8 GB de MEM sem declarar requests. Isso impede o scheduler de contabilizar e pode causar evictions. É um POC e deveria rodar em Spot.

### 2.6 Outros (on-demand)

| App | Réplicas | CPU Real | MEM Real |
|----|----|----|----|
| `passbolt` | 2 | \~5m | \~270Mi |
| `external-secrets` | 3 | \~1m | \~50Mi |
| `traefik` | 1 | \~5m | \~50Mi |
| `ecr-token-refresher` | 1 | \~1m | \~5Mi |


---

## 3. Oportunidades Identificadas

### 3.1 Migração para Spot — Apps que **não precisam** de on-demand

As seguintes aplicações são stateless e/ou tolerantes a interrupção. Podem rodar em Spot VMs com economia de **60-91%**:

| App | Pods | MEM total em uso | Motivo para Spot |
|----|----|----|----|
| `dev-n8n` (todos) | 12 | \~1.5 GB | Ambiente de desenvolvimento |
| `outline` | 4 | \~3.8 GB | Ferramenta de docs interna, stateless |
| `kestra-poc` | 5 | \~4.8 GB | POC, não é produção |
| `baserow-asgi` | 12 | \~10 GB | Stateless (websocket server) |
| `baserow-wsgi` | 10 | \~6.5 GB | Stateless (HTTP server) |
| `baserow-frontend` | 2 | \~1.1 GB | Stateless (frontend) |

> **Impacto estimado:** Se essas apps migrarem para Spot, liberamos nodes on-demand. A economia depende de quantos nodes o autoscaler conseguir desligar.

### 3.2 Rightsizing do Baserow — Valores sugeridos

O Baserow é o principal responsável pelo excesso de nodes. Os HPAs estão escalando ao máximo por **pressão de memória**, enquanto o CPU real é desprezível.

**Problema raiz:** o memory request está muito próximo do uso real, fazendo o HPA ver >80% de utilização e escalar indefinidamente.

#### `baserow-asgi` — Atual vs Sugerido

|    | Atual | Sugerido |
|----|----|----|
| CPU request | 100m | 100m |
| CPU limit | 2 | 500m |
| MEM request | **1Gi** | **1.5Gi** |
| MEM limit | 2Gi | 2Gi |
| HPA min | 2 | 2 |
| HPA max | **12** | **6** |
| HPA target memory | 80% | 80% |

**Justificativa:** Uso real é \~830Mi por pod. Com request de 1Gi, o HPA vê 81% (>80%) e escala ao máximo. Com request de 1.5Gi, o HPA verá \~55%, estabilizando em **3-4 réplicas** ao invés de 12.

**Resultado esperado:** de 12 pods → 4 pods, liberando \~8Gi de MEM request

#### `baserow-wsgi` — Atual vs Sugerido

|    | Atual | Sugerido |
|----|----|----|
| CPU request | 100m | 50m |
| CPU limit | 1 | 500m |
| MEM request | **750Mi** | **1Gi** |
| MEM limit | 1Gi | 1.5Gi |
| HPA min | 1 | 1 |
| HPA max | **10** | **4** |
| HPA target memory | 80% | 80% |

**Justificativa:** Uso real é \~647Mi por pod. Com request de 750Mi, o HPA vê 86% (>80%) e escala. Com request de 1Gi, o HPA verá \~65%, estabilizando em **2-3 réplicas** ao invés de 10.

**Resultado esperado:** de 10 pods → 3 pods, liberando \~5Gi de MEM request

#### `baserow-frontend` — Atual vs Sugerido

|    | Atual | Sugerido |
|----|----|----|
| CPU request | **1000m** | **500m** |
| CPU limit | 1 | 1 |
| MEM request | 1Gi | **768Mi** |
| MEM limit | 1Gi | 1Gi |

**Justificativa:** CPU real é 222-449m (média \~335m). Request de 1000m está 3x acima. MEM real \~540Mi com request de 1Gi.

#### `baserow-celery` — Atual vs Sugerido

|    | Atual (3 containers) | Sugerido |
|----|----|----|
| CPU request | **3x 1000m = 3000m** | **3x 300m = 900m** |
| CPU limit | 3x 1200m | 3x 500m |
| MEM request | **3x 1800Mi = 5.4Gi** | **3x 512Mi = 1.5Gi** |
| MEM limit | 3x 2Gi | 3x 1Gi |

**Justificativa:** Uso real total é 711m CPU e 786Mi MEM. Os requests atuais estão 4x (CPU) e 7x (MEM) acima do uso real. Já roda em Spot, então o impacto é menor, mas libera espaço no node Spot para receber mais workloads.

#### Resumo do impacto do rightsizing Baserow

| Componente | Pods antes | Pods depois | MEM request antes | MEM request depois |
|----|----|----|----|----|
| asgi | 12 | \~4 | 12 Gi | 6 Gi |
| wsgi | 10 | \~3 | 7.5 Gi | 3 Gi |
| frontend | 2 | 2 | 2 Gi | 1.5 Gi |
| celery (spot) | 1 | 1 | 5.4 Gi | 1.5 Gi |
| **Total** | **25** | **\~10** | **26.9 Gi** | **12 Gi** |

> **Economia estimada só com rightsizing Baserow: \~5-8 nodes on-demand = \~$245-390/mês**

### 3.3 Loki — `results-cache` over-provisioned

| Cache | MEM Request | MEM Real | Desperdício |
|----|----|----|----|
| `loki-results-cache` | **1229Mi** | **38Mi** | 97% ocioso |
| `loki-chunks-cache` | 2458Mi | 2071Mi | OK (84% uso) |

> Sugestão: reduzir `results-cache` request de 1229Mi para 256Mi.

### 3.4 Outline — Reduzir réplicas

|    | Atual | Sugerido |
|----|----|----|
| Réplicas | 4 | 2 |
| Pool | ON-DEMAND | **SPOT** |
| MEM request | 600Mi | 1Gi (uso real \~938Mi) |

> 4 réplicas com 5m de CPU cada é excessivo para uma wiki interna. 2 réplicas em Spot são suficientes.

### 3.5 Kestra POC — Definir requests e mover para Spot

Atualmente sem resource requests (5 pods consumindo \~4.8 GB invisíveis ao scheduler). Sugestão:

| Container | CPU Request | MEM Request | Pool |
|----|----|----|----|
| executor | 50m | 1Gi | **SPOT** |
| indexer | 50m | 1Gi | **SPOT** |
| scheduler | 50m | 1Gi | **SPOT** |
| webserver | 50m | 1Gi | **SPOT** |
| worker | 50m | 1.5Gi | **SPOT** |


---

## 4. CUD Spend-Based — O que é e quando contratar

### O que é CUD Spend-Based?

É um compromisso de gasto mínimo mensal em Compute Engine por 1 ou 3 anos, em troca de desconto automático. Diferente do resource-based (que exige definir vCPU e RAM específicos), o spend-based é flexível — ele se aplica a qualquer machine type da família, qualquer região. Se o workload mudar de tipo de VM ou escalar, o desconto continua valendo.

* **1 ano:** 20% de desconto
* **3 anos:** 35% de desconto

### Por que spend-based e não resource-based?

* **Resource-based** dá 37% de desconto (1 ano), mas exige especificar vCPU e RAM fixos — se mudarmos de e2-standard-2 para e2-standard-4, perde-se o desconto
* Estamos planejando rightsizing e migração para Spot, o que vai mudar o número de nodes on-demand
* **Spend-based é mais seguro nesse momento:** o desconto é menor (20%), mas se adapta a qualquer mudança

### Quando contratar?

> **Recomendação: contratar o CUD somente APÓS executar as otimizações das seções 3.1 a 3.5.**

Motivo: se contratarmos CUD sobre o baseline atual ($1.088/mês) e depois reduzirmos o compute com rightsizing + Spot, pagaremos o valor mínimo do commit sem usar. A ordem correta é:


1. Rightsizing Baserow (seção 3.2)
2. Migrar apps para Spot (seção 3.1)
3. Reduzir réplicas Outline + configurar Kestra (seções 3.4 e 3.5)
4. **Aguardar 2-4 semanas** para o novo baseline estabilizar
5. **Contratar CUD** sobre o novo baseline (estimado em \~$500-700/mês on-demand)

### Projeção de CUD pós-otimização

| Cenário | Baseline on-demand | Commit (80%) | Desconto 20% | Economia/ano |
|----|----|----|----|----|
| Sem otimização (atual) | \~$1.088/mês | \~$870/mês | \~$174/mês | **\~$2.088** |
| Pós-otimização (estimado) | \~$600/mês | \~$480/mês | \~$96/mês | **\~$1.152** |
| **Total (otimização + CUD)** |    |    |    | **\~$6.000-8.000/ano** |

> A economia principal vem da **redução de nodes** (rightsizing + Spot), não do CUD. O CUD é o passo final para extrair mais 20% do que sobra em on-demand.


---

## 5. Plano de Execução Sugerido

| Prioridade | Ação | Economia est./mês | Esforço | Risco |
|----|----|----|----|----|
| 1 | Rightsizing Baserow (alterar values) | **$245-390** | 1-2 dias | Médio — monitorar após deploy |
| 2 | Migrar dev-n8n, outline, kestra-poc para Spot | **$100-200** | 1 dia | Baixo — apps não-críticas |
| 3 | Migrar baserow (asgi/wsgi/frontend) para Spot | **$100-200** | 1 dia | Médio — validar comportamento em preemption |
| 4 | Reduzir Outline de 4→2 réplicas, ajustar MEM | **$0-50** | 30 min | Baixo |
| 5 | Definir requests no Kestra e reduzir loki-results-cache | **$0-50** | 1 hora | Baixo |
| 6 | Validar se `n8n` e `prd-n8n` são ambos necessários | **$100-200** | investigação | — |
| 7 | Contratar CUD spend-based (após baseline estabilizar) | **$96-174** | 1 hora | Baixo |
|    | **Total** | **\~$640-1.260/mês (\~$7.700-15.100/ano)** |    |    |