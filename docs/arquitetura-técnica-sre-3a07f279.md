<!-- title: Arquitetura Técnica (SRE) | url: https://outline.seazone.com.br/doc/arquitetura-tecnica-sre-2NsWrT0oFm | area: Tecnologia -->

# Arquitetura Técnica (SRE)

## Stack atual

| Componente | Detalhe |
|---:|----|
| **Passbolt CE** | 5.10.0-1-ce · chart oficial `passbolt/passbolt` v2.1.0 · 1 réplica |
| **Banco de dados** | Cloud SQL Postgres 17 · instância `tools` · 10.23.0.3:5432 |
| **Ingress** | Traefik IngressRoute + ServersTransport (HTTPS backend, insecureSkipVerify) |
| **SSL** | Cloudflare Proxy (A → 35.225.201.214) → Traefik → Passbolt nginx TLS |
| **SMTP** | AWS SES (sa-east-1) · `cofre-no-reply@seazone.com.br` |
| **Secrets** | AWS SSM Parameter Store → 3 ExternalSecrets (env, gpg, jwt) |
| **Chaves criptográficas** | GPG + JWT · SSM Advanced tier · montadas via `gpgExistingSecret` / `jwtExistingSecret` |
| **Sessão** | PHP file-based (1 réplica obrigatória sem Redis) |
| **Backup** | CronJob diário 03h · pg_dump → GCS `szn-postgres-tools-backups/passbolt/` · retenção 14 dias |
| **Helm chart** | `passbolt/passbolt` v2.1.0 (oficial) · values em `argocd/applications/passbolt/values.yaml` |
| **ArgoCD** | Application `passbolt` · auto-sync + self-heal |


---

## Arquitetura

```mermaidjs
flowchart TB
    subgraph user[" "]
        direction LR
        U["👤 Usuário"]
        Ext["🔌 Extensão Browser\nGPG local"]
    end

    subgraph cf["☁️ Cloudflare"]
        CFDNS["DNS Proxy\ncofre.seazone.com.br\n→ 35.225.201.214"]
    end

    subgraph gke["GKE · cluster-tools-prod-gke · us-central1-a"]
        direction TB
        TK["🔀 Traefik\nServersTransport HTTPS"]
        subgraph ns["namespace: passbolt"]
            direction LR
            APP["📦 Passbolt CE 5.10.0\nnginx TLS + PHP-FPM\n1 réplica"]
            ES["🔄 3 ExternalSecrets\nenv · gpg · jwt"]
            SEC["🗝️ K8s Secrets\npassbolt-env\npassbolt-gpg\npassbolt-jwt"]
            BK["⏱️ CronJob\nbackup 03h"]
        end
    end

    subgraph aws["AWS · sa-east-1"]
        SSM["📋 SSM Parameter Store\n/sre/passbolt/production/\n16 parâmetros"]
        SES["📧 AWS SES\nSMTP 587"]
    end

    subgraph gcp["GCP · us-central1"]
        SQL["🗄️ Cloud SQL Postgres 17\ninstância tools · 10.23.0.3"]
        GCS["🪣 GCS\nszn-postgres-tools-backups\n/passbolt/ · 14 dias"]
    end

    U <-->|HTTPS| Ext
    Ext -->|HTTPS| CFDNS
    U -->|HTTPS| CFDNS
    CFDNS --> TK
    TK -->|HTTPS :443| APP
    APP -->|5432| SQL
    APP -->|SMTP 587| SES
    ES -->|pull| SSM
    ES -->|cria/atualiza| SEC
    SEC -->|envFrom + volume mount| APP
    BK -->|pg_dump| SQL
    BK -->|gsutil cp| GCS

    style user fill:#1e293b,stroke:#334155
    style cf fill:#f6821f22,stroke:#f6821f
    style gke fill:#4285f422,stroke:#4285f4
    style aws fill:#ff990022,stroke:#ff9900
    style gcp fill:#34a85322,stroke:#34a853
    style ns fill:#1e40af22,stroke:#3b82f6
```


---

## Fluxo de criptografia GPG

O servidor **nunca vê senhas em texto claro**. Todo o processo acontece na extensão do browser.

```mermaidjs
sequenceDiagram
    actor Alice
    participant Ext as Extensão (browser)
    participant API as Passbolt API
    participant DB as Cloud SQL
    actor Bob

    Note over Alice,DB: Criar e compartilhar uma senha

    Alice->>Ext: Salva senha "AWS Console"
    Ext->>Ext: Encripta com chave pública de Alice
    Ext->>API: POST /resources (ciphertext)
    API->>DB: INSERT secrets

    Alice->>Ext: Compartilhar com Bob
    Ext->>API: GET /users/bob → chave pública GPG
    API-->>Ext: Bob's public key
    Ext->>Ext: Re-encripta com chave pública de Bob
    Ext->>API: POST /share
    API->>DB: INSERT secret para Bob

    Note over Bob,DB: Bob acessa o cofre
    Bob->>Ext: Abre cofre.seazone.com.br
    Ext->>API: GET /resources
    API-->>Ext: ciphertext
    Ext->>Ext: Decripta com chave privada local de Bob
    Ext-->>Bob: "AWS Console" → plaintext
```


---

## Secrets no AWS SSM

Caminho: `/sre/passbolt/production/` — 16 parâmetros ativos

### ExternalSecret: passbolt-env

| Parâmetro | Descrição |
|----|----|
| `DATASOURCES_DEFAULT_HOST` | 10.23.0.3 (Cloud SQL) |
| `DATASOURCES_DEFAULT_PORT` | 5432 |
| `DATASOURCES_DEFAULT_USERNAME` | passbolt |
| `DATASOURCES_DEFAULT_PASSWORD` | senha do usuário Postgres |
| `DATASOURCES_DEFAULT_DATABASE` | passbolt |
| `PASSBOLT_GPG_SERVER_KEY_FINGERPRINT` | Fingerprint da GPG key do servidor |
| `EMAIL_TRANSPORT_DEFAULT_HOST` | email-smtp.sa-east-1.amazonaws.com |
| `EMAIL_TRANSPORT_DEFAULT_USERNAME` | IAM access key (passbolt-ses-smtp) |
| `EMAIL_TRANSPORT_DEFAULT_PASSWORD` | SMTP password derivada da secret key |
| `EMAIL_TRANSPORT_DEFAULT_PORT` | 587 |
| `EMAIL_TRANSPORT_DEFAULT_TLS` | true |
| `EMAIL_DEFAULT_FROM` | cofre-no-reply@seazone.com.br |

### ExternalSecret: passbolt-gpg

| Parâmetro | Tier | Descrição |
|----|----|----|
| `serverkey.asc` | Standard | Chave pública GPG do servidor |
| `serverkey_private.asc` | **Advanced** | Chave privada GPG do servidor |

### ExternalSecret: passbolt-jwt

| Parâmetro | Tier | Descrição |
|----|----|----|
| `jwt.key` | **Advanced** | Chave privada JWT |
| `jwt.pem` | **Advanced** | Chave pública JWT |


---

## Limitação: 1 réplica obrigatória

O Passbolt CE usa sessões PHP baseadas em arquivo (`SESSION_DEFAULTS: php`). Com múltiplas réplicas, requests são balanceados entre pods e a sessão se perde (login funciona mas a home fica branca).

Para escalar horizontalmente, seria necessário:

* Habilitar Redis para sessões compartilhadas, ou
* Configurar session affinity (sticky sessions) no IngressRoute


---

## Comandos Úteis

```bash
# Ver pods
kubectl get pods -n passbolt --context gke_tools-440117_us-central1-a_cluster-tools-prod-gke

# Healthcheck
curl -s https://cofre.seazone.com.br/healthcheck/status.json | jq

# Listar usuários
kubectl exec -n passbolt deploy/passbolt-depl-srv -- \
  su -s /bin/bash -c "bin/cake passbolt users_index" www-data

# Criar usuário via CLI
kubectl exec -n passbolt deploy/passbolt-depl-srv -- \
  su -s /bin/bash -c "bin/cake passbolt register_user \
  -u email@seazone.com.br -f Nome -l Sobrenome -r admin" www-data

# Gerar link de recovery
kubectl exec -n passbolt deploy/passbolt-depl-srv -- \
  su -s /bin/bash -c "bin/cake passbolt recover_user -u email@seazone.com.br --create" www-data

# Verificar backups no GCS
gsutil ls -lh gs://szn-postgres-tools-backups/passbolt/

# Restore de backup (emergência)
PGPASSWORD='...' pg_restore -h 10.23.0.3 -U passbolt -d passbolt passbolt-db.dump

# Helm rollback (emergência)
helm rollback passbolt <revision> -n passbolt \
  --kube-context gke_tools-440117_us-central1-a_cluster-tools-prod-gke
```


---

## Troubleshooting

| Problema | Causa | Solução |
|----|----|----|
| Setup link mostra "requer convite" | Extensão não instalada | Instalar a extensão antes de abrir o link |
| Home branca após login | Múltiplas réplicas + sessão PHP file-based | Verificar que `replicaCount: 1` no values.yaml |
| Pod em CrashLoopBackOff | ExternalSecret não sincronizou | `kubectl describe externalsecret -n passbolt` + verificar SSM |
| Internal Server Error | Traefik mandando HTTP pro backend HTTPS | Verificar que IngressRoute usa porta 443 + ServersTransport |
| Email não chega | SES credentials incorretas | Verificar IAM user `passbolt-ses-smtp` + params SMTP no SSM |
| Migrations falharam | Encoding ou permissão de schema | `GRANT ALL ON SCHEMA public TO passbolt` no Cloud SQL |