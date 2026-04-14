<!-- title: Analytics Stack — OpenPanel + GrowthBook + ClickHouse | url: https://outline.seazone.com.br/doc/analytics-stack-openpanel-growthbook-clickhouse-PcNoFRdwcQ | area: Tecnologia -->

# Analytics Stack — OpenPanel + GrowthBook + ClickHouse

> EKS `general-cluster` | sa-east-1 | Atualizado em 2026-03-11

## O que faz cada peça

A stack resolve dois problemas distintos: **entender o comportamento dos usuários** (OpenPanel + ClickHouse) e **controlar o que os usuários veem** (GrowthBook). O ClickHouse é o denominador comum — serve como engine OLAP para queries analíticas do OpenPanel.

```mermaidjs
flowchart LR
    subgraph " "
        direction LR
        OP["OpenPanel\nProduct Analytics"]
        GB["GrowthBook\nFeature Flags & A/B"]
        CH[("ClickHouse\nEngine OLAP")]
    end

    OP -- "lê e escreve\neventos" --> CH
    GB -. "pode usar como\ndatasource de métricas" .-> CH

    style OP fill:#1e6091,stroke:#14456b,color:#fff
    style GB fill:#6a40bf,stroke:#4a2d87,color:#fff
    style CH fill:#d4a017,stroke:#a67c00,color:#1a1a2e
```


---

## Como o tráfego chega

Todo request externo passa pelo mesmo caminho: **Cloudflare DNS → AWS NLB → Traefik → Service**.

```mermaidjs
flowchart LR
    CF["Cloudflare\nDNS"] --> NLB["AWS NLB"] --> TFK["Traefik\n3 replicas"]

    TFK -->|"openpanel.seazone.com.br"| OP_D["op-dashboard\n:3000"]
    TFK -->|"openpanel.../api/*"| OP_A["op-api\n:3000"]
    TFK -->|"ff.seazone.com.br"| GB_F["gb-frontend\n:3000"]
    TFK -->|"api-ff.seazone.com.br"| GB_B["gb-backend\n:3100"]
    TFK -->|"clickhouse.seazone.com.br"| CH["clickhouse\n:8123"]

    style CF fill:#f39c12,color:#1a1a2e
    style NLB fill:#7b2cbf,color:#fff
    style TFK fill:#7b2cbf,color:#fff
```

> O path `/api` do OpenPanel passa por um middleware `strip-api-prefix` antes de chegar no `op-api`.


---

## OpenPanel — Product Analytics

Captura eventos de produto via SDK e exibe dashboards analíticos. São 3 deployments com HPA independente.

```mermaidjs
flowchart LR
    SDK["SDK / Browser"] -->|"POST /api/event"| API["op-api"]
    API -->|"enfileira"| REDIS[("ElastiCache\nValkey")]
    REDIS -->|"consome"| WKR["op-worker"]
    WKR -->|"INSERT batch"| CH[("ClickHouse")]

    DASH["op-dashboard"] -->|"GET /api/reports"| API
    API -->|"SELECT"| CH
    API -->|"metadados"| PG[("RDS\nPostgreSQL")]

    style REDIS fill:#d63031,color:#fff
    style CH fill:#d4a017,color:#1a1a2e
    style PG fill:#0984e3,color:#fff
```

**Backends externos:**

| Recurso | Onde |
|:---|:---|
| PostgreSQL (metadados) | RDS — `tools-postgres...rds.amazonaws.com:5432` |
| Redis/Valkey (filas) | ElastiCache — `openpanel-valkey-prd...cache:6379` |
| ClickHouse (analytics) | In-cluster — `clickhouse-clickhouse-cluster...svc:8123` |

**Scaling atual** (snapshot `kubectl`, 2026-03-11):

| Deploy | Pods | CPU real | Mem real | HPA range |
|:---|:---|:---|:---|:---|
| op-api | 4 | \~4m cada | \~335Mi | 2 → 10 |
| op-dashboard | 2 | \~2m | \~124Mi | 2 → 6 |
| op-worker | 2 | \~9m | \~287Mi | 2 → 10 |


---

## GrowthBook — Feature Flags & Experimentation

Plataforma de feature flags e experimentos A/B. O frontend é a UI de gestão; o backend avalia flags em tempo real e serve como SDK endpoint para todas as aplicações.

```mermaidjs
flowchart LR
    UI["gb-frontend"] -->|"API_HOST"| BK["gb-backend"]
    APPS["Apps / SDKs"] -->|"/api/features"| CDN["CloudFront\nCDN cache"]
    CDN --> BK
    BK --> MONGO[("MongoDB\nAtlas")]
    BK --> S3[("S3\nUploads")]

    style CDN fill:#ff9900,color:#1a1a2e
    style MONGO fill:#00b894,color:#1a1a2e
    style S3 fill:#ff9900,color:#1a1a2e
```

O backend roda com **8 replicas mínimas** — reflete a criticidade como serviço que todas as aplicações consultam para avaliar feature flags. As respostas passam por CloudFront com cache agressivo (30s fresh, 1h stale-while-revalidate, 10h stale-if-error).

**Scaling atual:**

| Deploy | Pods | CPU real | Mem real | HPA range |
|:---|:---|:---|:---|:---|
| gb-backend | 8 | \~3m cada | \~270Mi | 8 → 16 |
| gb-frontend | 2 | \~4m | \~170Mi | 2 → 4 |


---

## ClickHouse Cluster — Engine OLAP

O coração analítico da stack. Gerenciado pelo **Altinity ClickHouse Operator** com coordenação via **ClickHouse Keeper** (substituto leve do ZooKeeper, baseado em RAFT).

### Topologia

```mermaidjs
flowchart TB
    subgraph cluster["Cluster 'production' — 1 shard"]
        direction LR
        R0["Replica 0\n50Gi GP3"]
        R1["Replica 1\n50Gi GP3"]
        R2["Replica 2\n50Gi GP3"]
        R0 <-- ":9009" --> R1
        R1 <-- ":9009" --> R2
    end

    subgraph keeper["ClickHouse Keeper — RAFT"]
        direction LR
        K0["Keeper 0\n10Gi"]
        K1["Keeper 1\n10Gi"]
        K2["Keeper 2\n10Gi"]
        K0 <-- ":9234" --> K1
        K1 <-- ":9234" --> K2
    end

    R0 & R1 & R2 -- ":9181" --> keeper

    OP["Altinity Operator\nv0.26.0"] -. "reconcile" .-> cluster

    style R0 fill:#1e6091,color:#fff
    style R1 fill:#1e6091,color:#fff
    style R2 fill:#1e6091,color:#fff
    style K0 fill:#2d6a4f,color:#fff
    style K1 fill:#2d6a4f,color:#fff
    style K2 fill:#2d6a4f,color:#fff
    style OP fill:#6c757d,color:#fff
```

* **1 shard, 3 réplicas** — todas as réplicas contêm os mesmos dados (HA, não sharding horizontal)
* Tabelas usam `ReplicatedMergeTree` — replicação gerenciada pelo Keeper via RAFT consensus
* Duas credenciais: `openpanel` (app) e `admin` (DBA), ambas via ExternalSecret

### Consumo real (snapshot)

| Componente | Pods | CPU real | Mem real |
|:---|:---|:---|:---|
| ClickHouse Server | 3 | **\~1.7 cores** cada | \~2.6-3.0Gi |
| ClickHouse Keeper | 3 | \~3m cada | \~84Mi |
| Operator | 1 | \~27m | \~56Mi |

> Os servidores ClickHouse estão consumindo **\~85-90% do limite de CPU** (2 cores). Pode precisar de revisão se a carga crescer.


---

## Infraestrutura de suporte

### Secrets — AWS Parameter Store → ESO → K8s Secrets

```mermaidjs
flowchart LR
    SSM["AWS Parameter Store\n/sre/*"] -->|"OIDC JWT\nsync 1min"| ESO["External Secrets\nOperator"]
    ESO --> S1["openpanel-secrets"]
    ESO --> S2["growthbook-secrets"]
    ESO --> S3["clickhouse-secrets"]

    style SSM fill:#ff9900,color:#1a1a2e
    style ESO fill:#326ce5,color:#fff
```

Todos os secrets sincronizam a cada **1 minuto** — paths SSM em `/sre/openpanel/*`, `/sre/growthbook/production/*` e `/sre/databases/clickhouse/*`.

### Imagens — ECR Privado

Todas as imagens vivem no ECR `711387131913.dkr.ecr.sa-east-1.amazonaws.com/sre/`. Isso evita rate limits do Docker Hub e garante controle de supply chain.

### Node Pools (Karpenter)

| Pool | Nodes | Workloads | Toleration |
|:---|:---|:---|:---|
| `general-karpenter-system` | 10 | OpenPanel, GrowthBook, Traefik, Operator | — |
| `general-karpenter-data` | 2 | ClickHouse Server + Keeper | `workload=stateful` |

### Deploy — ArgoCD GitOps

```mermaidjs
flowchart LR
    GH["GitHub\ngitops-governanca"] --> ARGO["ArgoCD"]
    ARGO -->|"auto-sync\nprune + self-heal"| EKS["EKS Cluster"]

    style GH fill:#24292e,color:#fff
    style ARGO fill:#e8563f,color:#fff
    style EKS fill:#326ce5,color:#fff
```

Cada aplicação é um `Application` ArgoCD multi-source (Helm chart + values customizados + manifests extras). Sync automático com prune e self-heal garante que o cluster sempre reflete o estado do Git.


---

## Referência rápida de arquivos

```
argocd/applications/
├── openpanel/
│   ├── application.yaml          # ArgoCD App (chart: seazone-tech/helm-charts)
│   ├── values-openpanel.yaml     # Helm values
│   ├── external-secret.yaml      # 10 secrets do SSM
│   └── ingressroute.yaml         # Traefik routes
├── growthbook/
│   ├── application.yaml          # ArgoCD App (chart: ghcr.io OCI v4.1.0)
│   ├── values.yaml               # Helm values
│   ├── external-secret.yaml      # path-based discovery /sre/growthbook/production/*
│   └── ingressroute.yaml         # Traefik routes
└── databases/clickhouse/
    ├── application.yaml          # ArgoCD App (altinity-operator v0.26.0)
    ├── values.yaml               # Operator values
    ├── clickhouse-cluster.yaml   # ClickHouseInstallation CRD
    ├── clickhouse-keeper.yaml    # Keeper StatefulSet (3 nodes)
    ├── external-secret.yaml      # admin + openpanel passwords
    └── ingressroute.yaml         # Traefik route
```

<https://github.com/seazone-tech/gitops-governanca>