<!-- title: Stack de analytics | url: https://outline.seazone.com.br/doc/stack-de-analytics-fNyvsyaTgt | area: Tecnologia -->

# Stack de analytics

# Alertas de Monitoramento — ClickHouse, OpenPanel e GrowthBook

## Visão Geral

Foram criados **13 alertas** no Grafana distribuídos em 3 aplicações, todos notificando via contact point **"Alerta do grafana"** (Slack). Os alertas estão organizados em grupos por severidade (`critical` e `warning`).

| Aplicação | Alertas Critical | Alertas Warning | Total |
|----|----|----|----|
| ClickHouse | 3 | 3 | 6 |
| OpenPanel | 2 | 2 | 4 |
| GrowthBook | 2 | 1 | 3 |

**Dashboards relacionados:**

* [ClickHouse Cluster Overview](https://monitoring.seazone.com.br/d/clickhouse-cluster-overview/clickhouse-cluster-overview)
* [OpenPanel Overview](https://monitoring.seazone.com.br/d/openpanel-overview/openpanel-overview)
* [GrowthBook Overview](https://monitoring.seazone.com.br/d/growthbook-overview/growthbook-overview)


---

## ClickHouse (Pasta: Governança)

Cluster de produção: 1 shard, 3 réplicas, ClickHouse Keeper com 3 nós. Métricas coletadas via metrics-exporter do Altinity Operator (porta 8888).

### Critical — Grupo: `clickhouse-critical`

#### 1. Readonly Replica Detected

* **Condição:** `chi_clickhouse_metric_ReadonlyReplica > 0`
* **Pendência:** 2 minutos
* **noDataState:** OK
* **O que significa:** Uma réplica entrou em modo somente leitura. Isso ocorre quando a réplica perde conexão com o Keeper ou detecta corrupção de dados.
* **Impacto:** A réplica não aceita inserts. Se mais de uma réplica ficar readonly, o cluster perde capacidade de escrita.
* **Ação:** Verificar conexão com o Keeper, logs do ClickHouse e status do StatefulSet.

#### 2. Max Parts Per Partition Too High

* **Condição:** `max(chi_clickhouse_metric_MaxPartCountForPartition) > 200`
* **Pendência:** 5 minutos
* **noDataState:** OK
* **O que significa:** O número de parts em uma partition está crescendo além do normal. O ClickHouse throttla inserts em 300 parts e rejeita completamente em 600.
* **Impacto:** Degradação de performance de escrita; em caso extremo (>300), inserts serão atrasados/rejeitados.
* **Ação:** Verificar se merges estão rodando (`chi_clickhouse_metric_Merge`), se há recursos suficientes e se não há mutations bloqueando.

#### 3. Keeper Sessions Lost

* **Condição:** `sum(chi_clickhouse_metric_ZooKeeperSession) < 3`
* **Pendência:** 3 minutos
* **noDataState:** Alerting (se parar de receber dados, também alerta)
* **O que significa:** Nem todas as 3 réplicas estão conectadas ao Keeper. Sem sessão no Keeper, a réplica não participa da replicação.
* **Impacto:** Replicação degradada, risco de inconsistência de dados.
* **Ação:** Verificar status dos pods do Keeper (`kubectl get pods -n clickhouse -l app.kubernetes.io/name=clickhouse-keeper`), logs e rede.

### Warning — Grupo: `clickhouse-warning`

#### 4. High Failed Query Rate

* **Condição:** `sum(rate(chi_clickhouse_event_FailedQuery[5m])) > 0.5`
* **Pendência:** 5 minutos
* **O que significa:** Mais de 0.5 queries/segundo estão falhando de forma sustentada. Pode ser erro de aplicação, schema incorreto ou resource exhaustion.
* **Ação:** Verificar `system.query_log` no ClickHouse para identificar as queries falhando.

#### 5. Replication Queue Backlog

* **Condição:** `max(chi_clickhouse_metric_ReplicasSumQueueSize) > 50`
* **Pendência:** 10 minutos
* **O que significa:** A fila de replicação está acumulando tarefas. Dados entre réplicas estão divergindo.
* **Ação:** Verificar se merges e fetches estão progredindo. Investigar Keeper e rede inter-réplica.

#### 6. High Memory Usage

* **Condição:** `chi_clickhouse_metric_MemoryTracking > 3Gi` (limit configurado: 4Gi)
* **Pendência:** 5 minutos
* **O que significa:** O ClickHouse está usando mais de 75% da memória disponível. Risco de OOM kill.
* **Ação:** Identificar queries pesadas em `system.processes`, considerar aumentar limits ou otimizar queries.


---

## OpenPanel (Pasta: Governança)

Plataforma de analytics com 3 componentes: API (2-10 réplicas), Dashboard (2-6), Worker (2-10). Namespace: `openpanel`. Não expõe métricas Prometheus nativas — alertas baseados em métricas de infraestrutura (cAdvisor + kube-state-metrics).

### Critical — Grupo: `openpanel-critical`

#### 1. Pods Unavailable

* **Condição:** `kube_deployment_status_replicas_unavailable{namespace="openpanel"} > 0`
* **Pendência:** 5 minutos
* **O que significa:** Um ou mais pods dos deployments `op-api`, `op-dashboard` ou `op-worker` estão indisponíveis.
* **Impacto:** Perda de coleta de eventos analytics se API indisponível; perda de processamento se Worker indisponível.
* **Ação:** `kubectl get pods -n openpanel`, verificar logs e eventos.

#### 2. OOM Kill Detected

* **Condição:** `increase(container_oom_events_total{namespace="openpanel"}[5m]) > 0`
* **Pendência:** Imediato (0s)
* **O que significa:** Um container foi morto pelo kernel por exceder o limite de memória (2Gi).
* **Impacto:** Pod reinicia automaticamente mas perde dados em processamento.
* **Ação:** Verificar memory leak (gráfico "Memory RSS" no dashboard), considerar aumentar limits.

### Warning — Grupo: `openpanel-warning`

#### 3. Pod CrashLooping

* **Condição:** `increase(kube_pod_container_status_restarts_total{namespace="openpanel"}[1h]) > 3`
* **Pendência:** 5 minutos
* **O que significa:** Um pod reiniciou mais de 3 vezes em 1 hora, indicando CrashLoopBackOff.
* **Ação:** `kubectl logs -n openpanel <pod> --previous` para ver o log da execução anterior.

#### 4. HPA at Maximum Capacity

* **Condição:** `kube_horizontalpodautoscaler_status_current_replicas / kube_horizontalpodautoscaler_spec_max_replicas >= 1`
* **Pendência:** 15 minutos
* **O que significa:** O autoscaler atingiu o número máximo de réplicas e não consegue escalar mais.
* **Impacto:** Se a demanda continuar crescendo, haverá degradação de performance.
* **Ação:** Avaliar se é pico temporário ou crescimento orgânico. Aumentar `maxReplicas` no `values-openpanel.yaml` se necessário.


---

## GrowthBook (Pasta: GrowthBook)

Plataforma de feature flags com 2 componentes: Backend (8-16 réplicas) e Frontend (2-4). Namespace: `tools`. Não expõe métricas Prometheus nativas.

### Critical — Grupo: `growthbook-critical`

#### 1. Pods Unavailable

* **Condição:** `kube_deployment_status_replicas_unavailable{namespace="tools",deployment=~"growthbook-backend|growthbook-frontend"} > 0`
* **Pendência:** 5 minutos
* **O que significa:** Réplicas do backend ou frontend estão indisponíveis.
* **Impacto:** Feature flag delivery degradado; se backend indisponível, SDKs dos clientes não conseguem buscar configurações atualizadas.
* **Ação:** `kubectl get pods -n tools -l app.kubernetes.io/name=growthbook`, verificar logs e eventos.

#### 2. OOM Kill Detected

* **Condição:** `increase(container_oom_events_total{namespace="tools",pod=~"growthbook.*"}[5m]) > 0`
* **Pendência:** Imediato (0s)
* **O que significa:** Um container GrowthBook foi morto por exceder o limite de memória (backend: 2Gi, frontend: 512Mi).
* **Ação:** Verificar tendência de memória no dashboard, buscar memory leaks no Node.js.

### Warning — Grupo: `growthbook-warning`

#### 3. Pod CrashLooping

* **Condição:** `increase(kube_pod_container_status_restarts_total{namespace="tools",pod=~"growthbook.*"}[1h]) > 3`
* **Pendência:** 5 minutos
* **O que significa:** Um pod reiniciou mais de 3 vezes em 1 hora.
* **Ação:** `kubectl logs -n tools <pod> --previous` para diagnóstico.


---

## Configuração Técnica

| Parâmetro | Valor |
|----|----|
| **Contact Point** | Alerta do grafana (Slack) |
| **Datasource** | Prometheus (`PBFA97CFB590B2093`) |
| **Evaluation interval** | 1 minuto (padrão do Grafana) |
| **Provisionamento** | Via API Grafana (`/api/v1/provisioning/alert-rules`) |

### Critérios de Design

* **Critical:** Condições que indicam perda de disponibilidade ou risco iminente de perda de dados. Pendência curta (0-5min).
* **Warning:** Condições que indicam degradação ou risco futuro. Pendência mais longa (5-15min) para evitar ruído.
* **noDataState: OK** para a maioria dos alertas (ausência de dados não é alerta). Exceção: Keeper Sessions usa `Alerting` porque perda de dados do Keeper é em si um problema.