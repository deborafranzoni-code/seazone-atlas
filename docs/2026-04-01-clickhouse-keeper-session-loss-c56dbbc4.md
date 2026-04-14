<!-- title: 2026-04-01 — ClickHouse Keeper Session Loss | url: https://outline.seazone.com.br/doc/2026-04-01-clickhouse-keeper-session-loss-WItxecN579 | area: Tecnologia -->

# 2026-04-01 — ClickHouse Keeper Session Loss

# Incidente — ClickHouse Keeper Session Loss

**Data:** 2026-04-01 **Severidade:** P1 **Status:** Resolvido **Responsável:** Guilherme Santos


---

## Alerta recebido

```
Only X of 3 ClickHouse replicas connected to Keeper
Not all ClickHouse replicas have active Keeper sessions.
This means replication is degraded and data consistency is at risk.
Expected: 3 sessions (one per replica).
```

Métrica: `chi_clickhouse_metric_ZooKeeperSession < 3`


---

## O que foi encontrado

### Confirmação do incidente

A réplica `chi-clickhouse-cluster-production-0-2-0` apresentou `ZooKeeperSessionExpired = 1`, confirmando a expiração de sessão. As demais réplicas estavam saudáveis. O cluster se recuperou sozinho antes da intervenção.

### Root cause

O `clickhouse-keeper-0` (líder do Raft) estava alocado no mesmo node que cargas pesadas de I/O:

```
ip-10-0-30-90 (r6g.2xlarge, 8 vCPU / 64GB)
├── clickhouse-keeper-0         ← Keeper líder
├── chi-clickhouse-...-2-0      ← ClickHouse réplica 2
├── opensearch-...-data-0/1/2   ← 3 data nodes OpenSearch
├── opensearch-...-masters-1/2  ← 2 master nodes OpenSearch
└── mongodb-tools-0             ← MongoDB
```

A contenção de EBS I/O entre todos esses StatefulSets causava lentidão no processamento de requests do Keeper. Sob picos de I/O do OpenSearch e MongoDB, o tempo de resposta do Keeper se aproximava do `operation_timeout_ms` (10s). Quando isso se sustentou, a sessão da réplica 2 expirou (`session_timeout_ms = 30s`).

O Keeper em si estava saudável internamente (latência Raft interna < 40ms, quorum 2/3 OK) — o problema era exclusivamente a disputa de I/O no node.

### Por que o co-location aconteceu

O cluster OpenSearch `opensearch-reservas-api-prd` está incorretamente configurado para usar o nodepool `general-karpenter-data`, o mesmo usado pelo ClickHouse e Keeper. Não havia nenhuma regra impedindo que o Karpenter alocasse pods do OpenSearch e do Keeper no mesmo node.


---

## O que foi feito

### Fix aplicado

**Branch:** `fix/clickhouse-keeper-node-affinity` **Arquivo:** `argocd/applications/databases/clickhouse/clickhouse-keeper.yaml`

Adicionada `podAntiAffinity` preferred (weight 100) no StatefulSet do Keeper para evitar nodes que hospedam pods do OpenSearch (identificados pelo label `opster.io/opensearch-cluster`):

```yaml
preferredDuringSchedulingIgnoredDuringExecution:
- weight: 100
  podAffinityTerm:
    labelSelector:
      matchExpressions:
      - key: opster.io/opensearch-cluster
        operator: Exists
    topologyKey: kubernetes.io/hostname
```

### Por que é seguro

* `preferred` (não `required`): não bloqueia scheduling se não houver alternativa disponível
* Rolling restart automático pelo ArgoCD após merge: 1 pod por vez, quorum Raft mantido em 2/3 durante todo o processo
* Sem novo node provisionado: o `keeper-0` será realocado para `ip-10-0-24-150` (m6g.large com apenas CH-replica-0, \~1.4 vCPU e \~5.5Gi livres)


---

## Resultado esperado após merge

```
ip-10-0-24-150: CH-replica-0 + Keeper-0  ← Keeper-0 sai do node sobrecarregado
ip-10-0-30-90:  CH-replica-2 + OpenSearch x5 + MongoDB
ip-10-0-12-33:  CH-replica-1 + Keeper-2
ip-10-0-56-0:   Keeper-1
```


---

## Recomendações pendentes

| Prioridade | Ação | Motivo |
|----|----|----|
| P2 | Aumentar `session_timeout_ms` 30s → 60s | Margem extra contra picos transitórios de I/O |
| P2 | Investigar nodepool do `opensearch-reservas-api-prd` | Deveria ter nodepool dedicado — é a causa raiz do co-location |
| P3 | Adicionar readiness probe no Keeper | Pod aparece Ready antes do Raft estabilizar |
| P3 | PodDisruptionBudget para o Keeper | Previne que Karpenter drene 2 pods simultaneamente |