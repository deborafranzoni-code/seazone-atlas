<!-- title: baserow | url: https://outline.seazone.com.br/doc/baserow-e6ClywlEZN | area: Tecnologia -->

# baserow

> **Esta migração é executada ao vivo com Claude Code. Todos os manifests, ExternalSecrets e configurações são gerados e aplicados durante a janela de manutenção. O engenheiro valida e aprova cada passo; Claude Code executa.**

**Status:** Planejamento **Data alvo:** A definir **Responsável:** SRE / GovernancaTech **Criticidade:** Media (ferramenta interna de dados, sem SLA externo)


---

## Sumário Executivo

O Baserow está atualmente rodando no cluster GKE (`cluster-tools-prod-gke`, `us-central1-a`) e será migrado para o cluster EKS (`general-cluster`, `sa-east-1`). A migração é relativamente direta pois:

* Não há PVCs locais — dados em banco externo (PostgreSQL via Cloud SQL / RDS) e storage de arquivos no S3 (`tools-baserow`, `sa-east-1`)
* Imagens públicas do Docker Hub (`baserow/backend:1.35.1`, `baserow/web-frontend:1.35.1`)
* O Helm chart e values.yaml já existem neste repositório, apontando para o cluster GKE
* As credenciais já estão no AWS SSM Parameter Store, acessíveis via ExternalSecrets


---

## 1. Arquitetura Atual (GKE)

### Topologia

```
Internet
    │
Traefik (GKE)
    ├─ baserow.seazone.com.br       → Service: baserow-frontend     (port 3000)
    └─ api-baserow.seazone.com.br   → Service: baserow-asgi         (port 8000)
                                                    │
                                           baserow-wsgi (port 8000)
                                           baserow-celery (workers)
                                                    │
                                    ┌───────────────┼───────────────┐
                               PostgreSQL       Redis          S3 Bucket
                           (Cloud SQL GKE   (10.23.1.19,    (tools-baserow,
                            10.23.0.3:5432)  port 6379)      sa-east-1)
```

### Deployments no GKE

| Componente | Replicas (GKE) | Imagem | HPA |
|----|----|----|----|
| `baserow-frontend` | 2 | `baserow/web-frontend:1.35.1` | min:1 max:10 CPU/Mem 80% |
| `baserow-asgi` | 3 | `baserow/backend:1.35.1` | min:2 max:10 CPU/Mem 80% |
| `baserow-wsgi` | 10 | `baserow/backend:1.35.1` | min:1 max:4 CPU/Mem 80% |
| `baserow-celery` | 10 | `baserow/backend:1.35.1` | min:1 max:10 CPU/Mem 80% |

> Nota: As réplicas altas no GKE (10x wsgi, 10x celery) sugerem carga real de uso. Dimensionar EKS com minReplicas conservadoras inicialmente e deixar o HPA escalar.

### Dependências de Banco

* **PostgreSQL**: Cloud SQL GKE, IP `10.23.0.3`, porta `5432`, banco `baserow`
  * Este IP é interno ao GKE e **não acessível do EKS**
  * A migração deve apontar para o RDS `tools-postgres` na AWS (sa-east-1)
* **Redis**: IP `10.23.1.19`, porta `6379`, sem autenticação
  * Necessário provisionar Redis no EKS ou usar ElastiCache

### Storage de Arquivos

* **S3 Bucket**: `tools-baserow` em `sa-east-1` (já na AWS)
* **Custom domain**: `tools-baserow.s3.sa-east-1.amazonaws.com`
* **Endpoint**: `https://s3.sa-east-1.amazonaws.com`
* Acesso via credenciais IAM (`baserow-aws-credentials`)

### Segredos no AWS SSM

| Segredo Kubernetes | Chave SSM |
|----|----|
| `baserow-database-credentials` → `username` | `/governancatech/baserow/database_user` |
| `baserow-database-credentials` → `password` | `/governancatech/baserow/database_password` |
| `baserow-smtp-credentials` → `email-password` | `/governancatech/baserow/smtp_password` |
| `baserow-app-secrets` → `secret-key` | `/governancatech/baserow/secret_key` |
| `baserow-app-secrets` → `jwt-signing-key` | `/governancatech/baserow/jwt_signing_key` |
| `baserow-aws-credentials` → `access-key-id` | `/governancatech/baserow/s3_access_key_id` |
| `baserow-aws-credentials` → `secret-access-key` | `/governancatech/baserow/s3_secret_access_key` |

### Application ArgoCD Atual (GKE)

```yaml

destination:
  server: 'https://34.60.64.40'   # GKE cluster
  namespace: baserow
```


---

## 2. Arquitetura Destino (EKS)

### Topologia

```
Internet
    │
Traefik NLB (EKS, sg-0a3cb448a1d444487)
    ├─ baserow.seazone.com.br       → IngressRoute → Service: baserow-frontend  (port 3000)
    └─ api-baserow.seazone.com.br   → IngressRoute → Service: baserow-asgi      (port 8000)
                                                               │
                                                     baserow-wsgi (port 8000)
                                                     baserow-celery (workers)
                                                               │
                                            ┌──────────────────┼──────────────────┐
                                        RDS PostgreSQL     Redis               S3 Bucket
                                     (tools-postgres,    (ElastiCache ou     (tools-baserow,
                                      sa-east-1)          Redis in-cluster)   sa-east-1, inalterado)
```

### Decisões de Infraestrutura

| Componente | Decisão | Justificativa |
|----|----|----|
| PostgreSQL | RDS `tools-postgres` (db.t4g.small) — novo schema `baserow` | Instância compartilhada disponível, evita custo adicional |
| Redis | Novo Deployment Redis no namespace `baserow` | Baserow não requer Redis persistente (cache/queue temporário) |
| Storage | S3 `tools-baserow` (mantido, já em sa-east-1) | Sem migração necessária |
| NodePool | `general-karpenter-system` com toleration `NodeType=ClusterServices` | Tool interna, não é app de produto |

### Réplicas Alvo no EKS (Inicial)

| Componente | minReplicas | maxReplicas | Observação |
|----|----|----|----|
| `baserow-frontend` | 1 | 5 | Deixar HPA escalar conforme demanda |
| `baserow-asgi` | 2 | 8 | ASGI para WebSocket precisa de mínimo 2 |
| `baserow-wsgi` | 2 | 8 | Gunicorn HTTP workers |
| `baserow-celery` | 2 | 10 | Workers de background |


---

## 3. Arquivos de Configuração EKS

### 3.1 Application ArgoCD (`argocd/applications/baserow/application.yaml`)

Alterar o `destination.server` de GKE para EKS:

```yaml

apiVersion: argoproj.io/v1alpha1

kind: Application

metadata:
  name: baserow
  namespace: argocd
  finalizers:
    - resources-finalizer.argocd.argoproj.io

spec:
  project: default
  revisionHistoryLimit: 2
  sources:
    - repoURL: 'https://charts.christianhuth.de'
      chart: baserow
      targetRevision: 5.1.0
      helm:
        valueFiles:
          - $values/argocd/applications/baserow/values.yaml
    - repoURL: 'https://github.com/seazone-tech/gitops-governanca.git'
      targetRevision: HEAD
      ref: values
    # Manifests extras: ExternalSecrets, IngressRoutes
    - repoURL: 'https://github.com/seazone-tech/gitops-governanca.git'
      targetRevision: HEAD
      path: argocd/applications/baserow
      directory:
        include: '{external-secret.yaml,ingress.yaml}'
  destination:
    server: 'https://kubernetes.default.svc'   # EKS general-cluster
    namespace: baserow
  syncPolicy:
    automated:
      prune: true
      selfHeal: true
    syncOptions:
      - CreateNamespace=true
      - ServerSideApply=true
```

### 3.2 Values EKS (`argocd/applications/baserow/values.yaml`) — Mudanças Principais

```yaml
# Remover tolerations GKE e adicionar EKS Karpenter

frontend:
  tolerations: []
  affinity: {}
  nodeSelector:
    karpenter.sh/nodepool: general-karpenter-system
  tolerations:
    - key: "NodeType"
      operator: "Equal"
      value: "ClusterServices"
      effect: "NoSchedule"

backend:
  celery:
    tolerations: []
    affinity: {}
    # idem nodeSelector acima

# PostgreSQL: apontar para RDS tools-postgres na AWS

externalPostgresql:
  auth:
    enabled: true
    database: baserow
    existingSecret: "baserow-database-credentials"
    userPasswordKey: "password"
    userUsernameKey: "username"
  hostname: "<RDS_TOOLS_POSTGRES_ENDPOINT>"   # ex: tools-postgres.xxxx.sa-east-1.rds.amazonaws.com
  port: 5432

# Redis: serviço interno no namespace baserow

externalRedis:
  enabled: true
  auth:
    enabled: false
  hostname: "baserow-redis"   # Service name do Redis local
  port: 6379

# Manter S3 inalterado (já está na AWS)
backend:
  config:
    aws:
      accessKeyId: "baserow"
      bucketName: "tools-baserow"
      existingSecret: "baserow-aws-credentials"
      s3CustomDomain: "tools-baserow.s3.sa-east-1.amazonaws.com"
      s3EndpointUrl: "https://s3.sa-east-1.amazonaws.com"
      s3RegionName: "sa-east-1"
```

### 3.3 ExternalSecrets (`argocd/applications/baserow/external-secret.yaml`)

Claude Code gera e aplica o arquivo com os 4 segredos via ExternalSecrets no EKS:

```yaml

apiVersion: external-secrets.io/v1

kind: ExternalSecret

metadata:
  name: baserow-database-credentials
  namespace: baserow

spec:
  refreshInterval: "1h"
  secretStoreRef:
    name: aws-secrets-manager-ssm
    kind: ClusterSecretStore
  target:
    name: baserow-database-credentials
    creationPolicy: Owner
    deletionPolicy: Retain
  data:
    - secretKey: username
      remoteRef:
        key: /governancatech/baserow/database_user
    - secretKey: password
      remoteRef:
        key: /governancatech/baserow/database_password
---
apiVersion: external-secrets.io/v1

kind: ExternalSecret

metadata:
  name: baserow-smtp-credentials
  namespace: baserow

spec:
  refreshInterval: "1h"
  secretStoreRef:
    name: aws-secrets-manager-ssm
    kind: ClusterSecretStore
  target:
    name: baserow-smtp-credentials
    creationPolicy: Owner
    deletionPolicy: Retain
  data:
    - secretKey: email-password
      remoteRef:
        key: /governancatech/baserow/smtp_password
---
apiVersion: external-secrets.io/v1

kind: ExternalSecret

metadata:
  name: baserow-app-secrets
  namespace: baserow

spec:
  refreshInterval: "1h"
  secretStoreRef:
    name: aws-secrets-manager-ssm
    kind: ClusterSecretStore
  target:
    name: baserow-app-secrets
    creationPolicy: Owner
    deletionPolicy: Retain
  data:
    - secretKey: secret-key
      remoteRef:
        key: /governancatech/baserow/secret_key
    - secretKey: jwt-signing-key
      remoteRef:
        key: /governancatech/baserow/jwt_signing_key
---
apiVersion: external-secrets.io/v1

kind: ExternalSecret

metadata:
  name: baserow-aws-credentials
  namespace: baserow

spec:
  refreshInterval: "1h"
  secretStoreRef:
    name: aws-secrets-manager-ssm
    kind: ClusterSecretStore
  target:
    name: baserow-aws-credentials
    creationPolicy: Owner
    deletionPolicy: Retain
  data:
    - secretKey: access-key-id
      remoteRef:
        key: /governancatech/baserow/s3_access_key_id
    - secretKey: secret-access-key
      remoteRef:
        key: /governancatech/baserow/s3_secret_access_key
```

### 3.4 IngressRoutes (`argocd/applications/baserow/ingress.yaml`)

O arquivo já existe e pode ser reutilizado sem alterações (Traefik já roda no EKS):

```yaml
# Existente — sem mudanças necessárias
# baserow-front → baserow.seazone.com.br → service baserow-frontend:3000
# baserow-back  → api-baserow.seazone.com.br → service baserow-asgi:8000
```


---

## 4. Migração de Dados do Banco

### 4.1 Investigação do Banco Atual

Antes da migração, Claude Code confirma o banco atual no GKE:

```bash
# Conectar no pod do backend e verificar configuração

kubectl exec -it -n baserow deployment/baserow-wsgi -- \
  env | grep -E 'DATABASE|POSTGRES'

# Verificar se o host 10.23.0.3 é Cloud SQL Proxy local ou remoto

kubectl get service -n baserow

kubectl get pods -n baserow
```

### 4.2 Criar Schema no RDS tools-postgres

```sql
-- Executar no RDS tools-postgres como usuário administrador

CREATE USER baserow WITH PASSWORD '<senha-forte>';
CREATE DATABASE baserow OWNER baserow;
GRANT ALL PRIVILEGES ON DATABASE baserow TO baserow;

-- Verificar
\l baserow
```

### 4.3 Dump do Banco GKE (Cloud SQL)

**Opção A — pg_dump via pod no GKE (recomendado):**

```bash
# No cluster GKE

kubectl exec -it -n baserow deployment/baserow-wsgi -- \
  bash -c "pg_dump -h 10.23.0.3 -U <usuario> -d baserow -Fc -f /tmp/baserow_dump.dump"

# Copiar o dump para local

kubectl cp baserow/<pod-wsgi>:/tmp/baserow_dump.dump ./baserow_dump.dump
```

**Opção B — Backup direto do Cloud SQL (se for Cloud SQL gerenciado):**

```bash
# Via gcloud

gcloud sql export sql <INSTANCE_NAME> gs://<bucket>/baserow_dump.sql \
  --database=baserow \
  --project=<gcp-project>
```

### 4.4 Restaurar no RDS tools-postgres

```bash
# Opção A: restaurar via pg_restore (arquivo dump Fc)
pg_restore \
  -h <tools-postgres-endpoint>.sa-east-1.rds.amazonaws.com \
  -U baserow \
  -d baserow \
  -v \
  ./baserow_dump.dump

# Opção B: restaurar via psql (arquivo SQL)
psql \
  -h <tools-postgres-endpoint>.sa-east-1.rds.amazonaws.com \
  -U baserow \
  -d baserow \
  -f ./baserow_dump.sql

# Verificar contagem de registros após restauração

psql -h <endpoint> -U baserow -d baserow \
  -c "SELECT schemaname, tablename, n_live_tup FROM pg_stat_user_tables ORDER BY n_live_tup DESC LIMIT 20;"
```

### 4.5 Migrações Django pós-restauração

```bash
# Após o deploy no EKS, verificar se as migrações estão OK
# O chart roda migrate automaticamente (backend.config.migrateOnStartup: "true")
# Monitorar logs do pod wsgi na inicialização:
kubectl logs -f -n baserow deployment/baserow-wsgi | grep -i migrat
```


---

## 5. Provisionar Redis no EKS

O Baserow precisa de Redis para queue de tarefas Celery e cache. Claude Code gera e aplica o manifest durante a janela:

```yaml
# argocd/applications/baserow/redis.yaml

apiVersion: apps/v1

kind: Deployment

metadata:
  name: baserow-redis
  namespace: baserow

spec:
  replicas: 1
  selector:
    matchLabels:
      app: baserow-redis
  template:
    metadata:
      labels:
        app: baserow-redis
    spec:
      containers:
        - name: redis
          image: redis:7-alpine
          ports:
            - containerPort: 6379
          resources:
            requests:
              cpu: 50m
              memory: 64Mi
            limits:
              cpu: 200m
              memory: 256Mi
---
apiVersion: v1

kind: Service

metadata:
  name: baserow-redis
  namespace: baserow

spec:
  selector:
    app: baserow-redis
  ports:
    - port: 6379
      targetPort: 6379
```


---

## 6. Atualizar DNS

Após validar o Baserow no EKS:

```bash
# Obter o endereço do NLB do Traefik no EKS

kubectl get svc -n traefik traefik -o jsonpath='{.status.loadBalancer.ingress[0].hostname}'

# Atualizar no Cloudflare:
# baserow.seazone.com.br     → CNAME → <NLB hostname>
# api-baserow.seazone.com.br → CNAME → <NLB hostname>
```


---

## 7. Plano de Execução

### Janela de Migração (Dia D)

| Horário | Ação |
|----|----|
| T+00 | Anunciar manutenção em canal interno (#tech-tools ou similar) |
| T+02 | Claude Code investiga banco atual no GKE (env vars, serviços) |
| T+05 | Claude Code escala réplicas do GKE para 0 (freeze de escrita) |
| T+07 | Claude Code executa dump do banco no GKE — \~5min |
| T+12 | Claude Code cria usuário/banco no RDS e restaura dump — \~5-10min |
| T+20 | Validar contagem de registros no RDS vs GKE |
| T+22 | Claude Code gera e aplica ExternalSecrets, redis.yaml, atualiza values.yaml e application.yaml |
| T+24 | Claude Code commita e ArgoCD sincroniza — \~3min |
| T+27 | Validar pods Running no EKS — \~2min |
| T+29 | Testar login e acesso a tabelas no Baserow |
| T+32 | Claude Code atualiza DNS Cloudflare |
| T+37 | Validar acesso externo via novo DNS (\~5min propagação) |
| T+40 | Confirmar encerramento da manutenção |

### Pós-migração (D+1)

- [ ] Monitorar erros nos logs por 24h (`kubectl logs -n baserow ...`)
- [ ] Verificar que jobs Celery estão processando (envio de e-mails, etc.)
- [ ] Escalar down os deployments no GKE (não deletar ainda — aguardar D+7)
- [ ] Criar snapshot do banco GKE antes de deletar


---

## 8. Plano de Rollback

Em caso de problemas durante ou após a migração:

### Rollback Imediato (dentro da janela de manutenção)

```bash
# 1. Reverter application.yaml para destination GKE

git revert HEAD

git push

# 2. Escalar Baserow de volta no GKE

kubectl scale deployment baserow-wsgi baserow-asgi baserow-celery baserow-frontend \
  -n baserow --replicas=<replicas-originais> \
  --context=gke_<project>_us-central1-a_cluster-tools-prod-gke

# 3. O DNS ainda aponta para GKE (não houve mudança) — serviço restaurado
```

### Rollback Tardio (após mudança de DNS)

```bash
# 1. Reverter DNS no Cloudflare para os IPs do GKE
# 2. Aguardar propagação do DNS (TTL)
# 3. Reverter application.yaml no git
# 4. Anunciar resolução
```

### Checklist de Decisão de Rollback

- [ ] Pods em CrashLoopBackOff após 10 minutos → Rollback
- [ ] Erros 500 em mais de 10% das requisições → Rollback
- [ ] Celery workers não processando tasks → Investigar, rollback se > 30min
- [ ] Dados inconsistentes no banco (registros faltando) → Rollback imediato


---

## 9. Checklist de Validação

### Infraestrutura

- [ ] Todos os pods em estado `Running`
- [ ] ExternalSecrets sincronizados (`kubectl get externalsecret -n baserow`)
- [ ] HPA criado para todos os componentes
- [ ] Redis respondendo (`kubectl exec -n baserow deploy/baserow-redis -- redis-cli ping`)
- [ ] Conexão com RDS OK (checar logs do pod wsgi na inicialização)
- [ ] Conexão com S3 OK (testar upload de arquivo no Baserow)

### Funcional

- [ ] Login na interface `https://baserow.seazone.com.br`
- [ ] Listar tabelas e dados existentes (conferir com dados pré-migração)
- [ ] Criar nova linha em tabela existente
- [ ] Upload de arquivo (imagem) — valida conexão S3
- [ ] WebSocket funcionando (edição em tempo real — valida ASGI)
- [ ] Envio de e-mail de convite (valida SMTP + Celery)
- [ ] API REST respondendo em `https://api-baserow.seazone.com.br/api/_health/`

### Monitoramento

- [ ] ServiceMonitor ou logs visíveis no Grafana
- [ ] Sem alertas ativos no Alertmanager relacionados ao namespace `baserow`