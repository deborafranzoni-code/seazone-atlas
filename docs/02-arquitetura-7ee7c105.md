<!-- title: 02-Arquitetura | url: https://outline.seazone.com.br/doc/02-arquitetura-bihbtWLXrg | area: Tecnologia -->

# 02-Arquitetura

## Diagrama de Componentes

 ![](/api/attachments.redirect?id=e475f265-b19c-4d83-af38-cd3d5df4c24c " =1408x768")

## Componentes e suas responsabilidades

### n8n-editor

* Serve a UI Vue.js e a API REST
* Recebe requisições de usuários e armazena workflows/credentials no PostgreSQL
* **Não executa workflows** — apenas enfileira jobs no Redis quando um workflow é disparado manualmente
* 1 réplica fixa (não escala horizontalmente; monitorar memória — alerta em 80% do limite)

### n8n-webhooks

* Processo exclusivo para receber requisições de webhook externas
* Ao receber um webhook, enfileira o job no Bull (Redis) e aguarda o worker processar
* Escalonamento automático (HPA): dev 1–3, prd 2–6 réplicas (CPU 70%, memória 80%)

### n8n-workers

* Consomem jobs da fila Bull e executam os workflows
* Cada worker processa no máximo **10 execuções em paralelo** (`EXECUTIONS_CONCURRENCY_ACTIVE`)
* Com 6 workers, limite de **60 execuções simultâneas** — alerta configurado quando mantido por >3 min
* Cada worker tem um **sidecar task-runner** (`n8nio/runners`) para Code Nodes (JS/Python)
* Escalonamento automático (HPA): dev 1–3, prd 2–6 réplicas

### n8n-mcp

* Servidor MCP (Model Context Protocol) para integração com agentes AI
* Exposto em `/mcp` no host de webhooks com Middleware `n8n-nogzip` (remove `Content-Encoding` para compatibilidade com clientes MCP)
* 1 réplica fixa

### Task Runner (sidecar `n8nio/runners`)

* Roda ao lado de cada worker em **external mode** (`N8N_RUNNERS_MODE=external`)
* Executa Code Nodes (JavaScript e Python) em processo isolado
* Conecta ao broker (porta `5679` do worker) via WebSocket autenticado por `N8N_RUNNERS_AUTH_TOKEN`
* A versão da imagem **deve ser sempre igual** à do `n8nio/n8n`

## Namespace Kubernetes

| Recurso | dev-n8n | prd-n8n |
|----|----|----|
| Deployments | editor, webhooks, workers, mcp, hooks-server | editor, webhooks, workers, mcp |
| StatefulSets | n8n-postgres | — |
| CronJobs | n8n-backup | n8n-backup |
| Services | ClusterIP para cada deployment | ClusterIP para cada deployment |
| IngressRoutes | editor, webhooks, mcp, hooks | editor, webhooks, mcp |
| Middlewares | n8n-nogzip | n8n-nogzip |
| ExternalSecrets | n8n-external-secrets | n8n-external-secrets |
| PodMonitoring | n8n-pod-monitoring | n8n-pod-monitoring |
| ServiceAccounts | n8n-sa (Workload Identity) | n8n-sa (Workload Identity) |

## Dependências externas

### Banco de dados (PostgreSQL)

|    | dev | prd |
|----|----|----|
| Tipo | In-cluster StatefulSet | GCP Cloud SQL |
| Banco | `db_n8n_dev` | via secret `DB_POSTGRESDB_DATABASE` |
| Host | `n8n-postgres` (Service K8s) | via secret `DB_POSTGRESDB_HOST` |
| Porta | `5432` | via secret `DB_POSTGRESDB_PORT` |
| Credenciais | `n8n-secrets` (ExternalSecret) | `n8n-secrets` (ExternalSecret) |
| Storage | PVC 20Gi `standard-rwo` (zonal) | Gerenciado pelo GCP |



:::warning
Atenção (dev): standard-rwo é zonal — se o nó for movido para outra zona, o PVC não acompanha. O StatefulSet deve ser schedulado na mesma zona do PV.Redis (fila Bull)

:::

### Redis (fila Bull)

|    | dev | prd |
|----|----|----|
| Tipo | In-cluster Deployment | GCP Memorystore (HA) |
| Host | `n8n-redis` (Service K8s) | `10.23.1.3` |
| Porta | `6379` | `6379` |
| DB index | `1` | `1` |
| Auth | Desabilitada | Desabilitada |

### Secrets Manager (AWS Parameter Store)

* **ClusterSecretStore:** `aws-parameter-store-global`
* **Path dev:** `/sre/n8n/dev/*` → Secret `n8n-secrets` em `dev-n8n`
* **Path prd:** `/sre/n8n/prd/*` → Secret `n8n-secrets` em `prd-n8n`
* **Refresh:** 1 minuto (policy `Periodic`)
* **Deletion policy:** `Retain` — Secret não é deletado mesmo se o ExternalSecret for removido

Chaves obrigatórias no SSM:

```
DB_TYPE
DB_POSTGRESDB_DATABASE
DB_POSTGRESDB_HOST
DB_POSTGRESDB_PORT
DB_POSTGRESDB_USER
DB_POSTGRESDB_PASSWORD
N8N_ENCRYPTION_KEY          ← crítica: perda = credentials ilegíveis
N8N_RUNNERS_AUTH_TOKEN
N8N_SMTP_USER
N8N_SMTP_PASS
```

### GCS (Backup)

|    | dev | prd |
|----|----|----|
| Bucket | `gs://szn-n8n-dev-backup` | `gs://szn-n8n-prd-backup` |
| GCP Project | `tools-440117` | `tools-440117` |
| GCP SA | `n8n-dev-sa@tools-440117.iam.gserviceaccount.com` | `n8n-prd-sa@tools-440117.iam.gserviceaccount.com` |
| K8s SA | `n8n-sa` (namespace `dev-n8n`) | `n8n-sa` (namespace `prd-n8n`) |
| IAM binding | `roles/iam.workloadIdentityUser` + `objectAdmin` | idem |

## Ingress e DNS (Traefik)

| Rota | Componente | Entrypoint | Observação |
|----|----|----|----|
| `Host(dev-automation.seazone.com.br)` | n8n-editor | `web` |    |
| `Host(dev-webhook-automation.seazone.com.br)` | n8n-webhooks | `web` |    |
| `Host(...) && PathPrefix(/mcp)` | n8n-mcp | `web` | Middleware `n8n-nogzip` |
| `Host(...) && PathPrefix(/hooks/)` | hooks-server nginx | `web` | Priority 200, dev only |
| `Host(automation.seazone.com.br)` | n8n-editor | `web` | prd |
| `Host(webhook-automation.seazone.com.br)` | n8n-webhooks | `web` | prd |
| `Host(...) && PathPrefix(/mcp)` | n8n-mcp | `web` | Middleware `n8n-nogzip`, prd |


:::info
O n8n-nogzip Middleware limpa o header Content-Encoding na resposta — necessário para compatibilidade com clientes MCP que não suportam gzip.

:::

## Recursos (CPU/Memória)

### dev-n8n

| Componente | CPU Request | CPU Limit | Mem Request | Mem Limit |
|----|----|----|----|----|
| editor | 250m | 500m | 256Mi | 512Mi |
| workers | 250m | 500m | 256Mi | 512Mi |
| webhooks | 250m | 500m | 256Mi | 512Mi |
| mcp | 250m | 500m | 512Mi | 1024Mi |
| hooks-server | 10m | 100m | 32Mi | 64Mi |
| postgres | 250m | 1000m | 512Mi | 2Gi |
| redis | 50m | 250m | 128Mi | 512Mi |

### prd-n8n

| Componente | CPU Request | CPU Limit | Mem Request | Mem Limit |
|----|----|----|----|----|
| editor | 250m | 1000m | 256Mi | 2048Mi |
| workers | 250m | 500m | 256Mi | 1024Mi |
| webhooks | 250m | 500m | 256Mi | 1024Mi |
| mcp | 250m | 500m | 512Mi | 1024Mi |