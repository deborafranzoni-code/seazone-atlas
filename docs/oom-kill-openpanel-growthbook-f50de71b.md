<!-- title: OOM Kill Openpanel & Growthbook | url: https://outline.seazone.com.br/doc/oom-kill-openpanel-growthbook-2IQyCaBM2A | area: Tecnologia -->

# OOM Kill Openpanel & Growthbook

# Relatório de Incidente — Alertas OOM Kill

| Campo | Valor |
|----|----|
| **Data do Incidente** | 2026-03-10 \~21:30 UTC (\~18:30 BRT) |
| **Severidade** | P1 — Critical |
| **Alertas Disparados** | `OpenPanel - OOM Kill Detected`, `GrowthBook - OOM Kill Detected` |
| **Duração** | \~1 hora (21:30 – 22:30 UTC) |
| **Impacto** | OpenPanel API indisponível; GrowthBook com reagendamento de pods |
| **Autor** | SRE / Governança |


---

## 1. Resumo Executivo

Os alertas **"OpenPanel - OOM Kill Detected"** e **"GrowthBook - OOM Kill Detected"** dispararam na noite de 10/03/2026. A investigação revelou que **não houve OOM real (Out of Memory) em nenhum dos dois serviços**. A causa raiz foi uma **indisponibilidade temporária do ClickHouse** que provocou crash loops em cascata no OpenPanel API, e a **rotação de nodes do Karpenter** que afetou pods do GrowthBook.


---

## 2. Cronologia do Incidente

| Horário (UTC) | Evento |
|----|----|
| \~21:20 | ClickHouse fica temporariamente inacessível via DNS interno |
| \~21:30 | Todos os 10 pods do `op-api` começam a falhar com `ENOTFOUND clickhouse-clickhouse-cluster.clickhouse.svc.cluster.local` |
| \~21:30-21:40 | Pods `op-api` acumulam 3-4 restarts cada (exit code 137 — SIGKILL por probe failure) |
| \~21:30 | Alerta `OpenPanel - OOM Kill Detected` dispara (falso positivo) |
| \~21:30 | Alerta `GrowthBook - OOM Kill Detected` dispara durante reagendamento de pods por rotação de node |
| \~22:30 | ClickHouse volta ao normal, pods `op-api` se estabilizam |
| \~22:30 | Alertas resolvem automaticamente |


---

## 3. Análise de Causa Raiz

### 3.1 OpenPanel — Crash Loop por ClickHouse Indisponível

**O que aconteceu:**

Os logs do pod `op-api-b48dc5bfd-76m28` (e todos os demais pods API) mostram repetidamente:

```
error Query: HTTP request error.
  hostname: clickhouse-clickhouse-cluster.clickhouse.svc.cluster.local
  code: ENOTFOUND
  syscall: getaddrinfo
```

Quando o ClickHouse ficou inacessível, a API não possui circuit breaker nem retry com backoff — ela simplesmente crasha. O Kubernetes reinicia o pod, que crasha novamente, gerando o crash loop.

**Evidências que comprovam que NÃO foi OOM:**

| Métrica | Valor | Esperado se fosse OOM |
|----|----|----|
| `container_oom_events_total` | **0** (todos os pods) | > 0 |
| `kube_pod_container_status_last_terminated_reason` | **Error** | OOMKilled |
| Pico de memória `op-api` | **310-536 Mi** | Próximo de 2Gi (limite) |
| % de uso da memória | **16-26%** do limite | >95% |

**Por que o alerta disparou:** O exit code 137 (SIGKILL) enviado pelo kubelet quando a liveness probe falha pode incrementar `container_oom_events_total` em algumas versões do cAdvisor, mesmo quando o kill não é por OOM. O alerta usa a query `increase(container_oom_events_total{namespace="openpanel"}[5m]) > 0`, que não distingue a razão real da terminação.

### 3.2 GrowthBook — Reagendamento por Rotação de Nodes

**O que aconteceu:**

Pods do GrowthBook backend foram reagendados para novos nodes criados pelo Karpenter (rotação normal de spot instances):

| Pod | Criado em | Node | Node Criado em |
|----|----|----|----|
| backend-48r5v | 11/03 11:00 | ip-10-0-45-220 | 11/03 10:35 |
| backend-mgwf8 | 11/03 11:00 | ip-10-0-45-220 | 11/03 10:35 |
| backend-z65f9 | 12/03 08:07 | ip-10-0-59-52 | 11/03 15:17 |
| backend-jjtc2 | 12/03 11:34 | ip-10-0-21-69 | 12/03 11:20 |

**Evidências que comprovam que NÃO foi OOM:**

| Métrica | Valor |
|----|----|
| Restarts em todos os pods | **0** |
| `container_oom_events_total` | **0** |
| Memória backend | \~280Mi / 2Gi (**14%**) |
| Memória frontend | \~170Mi / 512Mi (**33%**) |
| CPU utilização | **1%** |


---

## 4. Problemas Estruturais Encontrados

### 4.1 OpenPanel API sem resiliência ao ClickHouse

A API do OpenPanel não possui circuit breaker, retry com backoff, ou graceful degradation. Qualquer indisponibilidade do ClickHouse derruba **100% das instâncias** simultaneamente.

### 4.2 Ausência de PodDisruptionBudgets (PDB)

Nenhum dos serviços (OpenPanel, GrowthBook, ClickHouse) possui PDB configurado. Isso permite que operações de manutenção (rotação de nodes, upgrades) derrubem todos os pods simultaneamente.

### 4.3 Ausência de Pod Anti-Affinity

Nenhum dos serviços tem `podAntiAffinity` configurado. No caso do ClickHouse, **5 de 6 pods** (3 data + 2 keepers) estão no **mesmo node** (`ip-10-0-11-227`), criando um ponto único de falha.

### 4.4 Redis do OpenPanel com política de evição incorreta

Os logs mostram repetidamente:

```
IMPORTANT! Eviction policy is volatile-lru. It should be "noeviction"
```

### 4.5 Alerta OOM Kill com falsos positivos

O alerta `container_oom_events_total > 0` não distingue OOM real de SIGKILL por outras razões.


---

## 5. Plano de Ações

### 5.1 Ações Essenciais (Aplicadas)

As seguintes ações foram implementadas na branch `fix/ha-openpanel-growthbook-clickhouse`:

#### OpenPanel — Pod Anti-Affinity

Adicionado `podAntiAffinity` preferencial para distribuir replicas de API, Dashboard e Worker em nodes diferentes, evitando que uma falha de node derrube todas as instâncias.

#### ClickHouse — Pod Anti-Affinity

Adicionado `podAntiAffinity` no template do ClickHouseInstallation e no StatefulSet do Keeper para forçar a distribuição dos pods em nodes distintos, eliminando o ponto único de falha atual.

#### GrowthBook — Redução de minReplicas do Backend

Reduzido `minReplicas` do backend de 8 para 4. Com CPU a 1% e memória a 14%, 8 réplicas mínimas é overprovisioning. O HPA continua habilitado e escalará se necessário.

#### GrowthBook — Pod Anti-Affinity

Adicionado `podAntiAffinity` preferencial para distribuir pods do backend e frontend entre nodes diferentes.


---

### 5.2 Ações Pendentes (Nice to Have)

As seguintes ações requerem trabalho adicional e devem ser planejadas em sprints futuras:

- [ ] **OpenPanel — Circuit breaker no código da API**: A API precisa de retry com exponential backoff para conexão ao ClickHouse. Requer mudança no código-fonte da aplicação, não apenas infra.
- [ ] **OpenPanel — PodDisruptionBudgets**: Adicionar PDBs com `minAvailable: 50%` para API e Worker. Requer validação de que o Helm chart (`seazone-tech/helm-charts/openpanel`) suporta o campo `pdb` nos values. Se não suportar, criar os PDBs como manifests extras no ArgoCD.
- [ ] **GrowthBook — PodDisruptionBudgets**: Adicionar PDBs com `minAvailable: 1` para backend e frontend. Requer validação de que o chart oficial (`ghcr.io/growthbook/charts`) suporta PDB nos values.
- [ ] **ClickHouse — PodDisruptionBudgets**: Criar PDBs para o cluster e keeper garantindo quórum (2/3 nodes disponíveis). Como o ClickHouse usa CRD do operator Altinity, o PDB deve ser criado como manifest separado.
- [ ] **Redis — Corrigir eviction policy**: Alterar a política de evição do ElastiCache de `volatile-lru` para `noeviction` conforme requerido pelo OpenPanel. Requer mudança no Terraform/console AWS do ElastiCache.
- [ ] **Alertas — Refinar regra de OOM Kill**: Alterar os alertas no Grafana para usar uma combinação que evite falsos positivos:

  ```promql
  (increase(container_oom_events_total{namespace="openpanel"}[5m]) > 0)
  AND ON (namespace, pod)
  (kube_pod_container_status_last_terminated_reason{reason="OOMKilled"} == 1)
  ```
- [ ] **Probes — Adicionar health checks**: Configurar `livenessProbe` e `readinessProbe` para OpenPanel e GrowthBook com `initialDelaySeconds` adequado para evitar kills prematuros durante startup.
- [ ] **TopologySpreadConstraints**: Adicionar constraints para distribuir pods entre Availability Zones, não apenas entre nodes.


---

## 6. Estado Atual dos Serviços (pós-incidente)

### OpenPanel (namespace: `openpanel`)

| Componente | Pods | Status | Restarts | Memória Atual | Limite | % Uso |
|----|----|----|----|----|----|----|
| API | 4 | Running | 0\* | \~335Mi | 2Gi | 16% |
| Dashboard | 2 | Running | 0 | \~100Mi | 2Gi | 5% |
| Worker | 2 | Running | 0 | \~290Mi | 2Gi | 14% |

*\*Pod* `*op-api-b48dc5bfd-76m28*` *tem 4 restarts do incidente de 10/03, mas está estável desde então.*

### GrowthBook (namespace: `tools`)

| Componente | Pods | Status | Restarts | Memória Atual | Limite | % Uso |
|----|----|----|----|----|----|----|
| Backend | 8 | Running | 0 | \~280Mi | 2Gi | 14% |
| Frontend | 2 | Running | 0 | \~170Mi | 512Mi | 33% |

### ClickHouse (namespace: `clickhouse`)

| Componente | Pods | Status | Memória Atual | Limite |
|----|----|----|----|----|
| Data (3 replicas) | 3 | Running | \~7.5Gi | 4Gi\* |
| Keeper (3 replicas) | 3 | Running | N/A | 1Gi |

*\*Os data nodes estão rodando com limites diferentes do que consta no repo (16Gi no cluster real vs 4Gi no manifest). Essa discrepância deve ser investigada.*


---

## 7. Lições Aprendidas


1. **Alertas devem ser precisos**: `container_oom_events_total` sozinho não é suficiente para determinar OOM real. Combinar com `kube_pod_container_status_last_terminated_reason{reason="OOMKilled"}`.
2. **Aplicações devem tolerar falhas de dependências**: Um serviço não deve crashar porque uma dependência ficou indisponível por alguns minutos. Circuit breakers e retries são essenciais.
3. **Anti-affinity é fundamental para HA**: Ter 5 pods de um banco de dados no mesmo node anula qualquer benefício de ter réplicas.
4. **PDBs são obrigatórios em produção**: Sem PDBs, operações rotineiras de cluster (rotação de nodes, upgrades) podem causar indisponibilidade total.


---

## 8. Referências

* Dashboard GrowthBook: <https://monitoring.seazone.com.br/d/growthbook-overview/growthbook-overview>
* Dashboard OpenPanel: <https://monitoring.seazone.com.br/d/openpanel-overview/openpanel-overview>
* Branch com correções: `fix/ha-openpanel-growthbook-clickhouse`