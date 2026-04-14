<!-- title: Passbolt | url: https://outline.seazone.com.br/doc/passbolt-NuLsEAFwau | area: Tecnologia -->

# Passbolt

**Status:** Planejamento **Data alvo:** A definir — requer janela de manutenção agendada **Responsável:** SRE / GovernancaTech **Criticidade:** ALTA — gerenciador de senhas da empresa, impacto direto em toda a equipe

> **ATENCAO:** Passbolt é o cofre de senhas da Seazone. Uma migração mal executada pode resultar em perda permanente de acesso a credenciais críticas da empresa. Esta migração EXIGE teste completo em ambiente de validação antes de qualquer execução em produção.

> **Claude Code executa todos os comandos** (kubectl, aws cli, pg_dump/restore, helm). O engenheiro valida o GPG fingerprint e confirma o login após a migração. Nenhuma preparação manual é necessária antes da janela — tudo é feito ao vivo.


---

## Sumário Executivo

O Passbolt está em `https://cofre.seazone.com.br`, rodando no GKE com:

* 1 pod `passbolt-depl-srv`
* CronJob de processamento de e-mails (`passbolt-cron-proc-email`)
* 3 ExternalSecrets já no AWS SSM: `passbolt-env`, `passbolt-gpg`, `passbolt-jwt`
* PostgreSQL externo (sem banco local no namespace)
* Helm chart (`passbolt/passbolt v2.1.0`), image `passbolt/passbolt:5.10.0-1-ce`

Os dados críticos que NÃO PODEM ser perdidos:


1. **Banco PostgreSQL** — todas as senhas, usuários, grupos e metadados
2. **Chave GPG privada do servidor** — necessária para decriptar dados armazenados
3. **Fingerprint GPG** — deve corresponder exatamente à chave no banco
4. **Chaves JWT** (`.key` e `.pem`) — necessárias para autenticação mobile/API


---

## 1. Arquitetura Atual (GKE)

### Topologia

```
Internet
    │
Traefik (GKE)
    └─ cofre.seazone.com.br → IngressRoute → Service: passbolt:443
                                                   │
                                              Pod: passbolt-depl-srv
                                           (passbolt/passbolt:5.10.0-1-ce)
                                                   │
                               ┌───────────────────┤
                          PostgreSQL             ExternalSecrets (AWS SSM)
                       (banco externo,          ┌─ passbolt-env (DB + SMTP + GPG fingerprint)
                        host via SSM)           ├─ passbolt-gpg (serverkey.asc + serverkey_private.asc)
                                                └─ passbolt-jwt (jwt.key + jwt.pem)

CronJob: passbolt-cron-proc-email → executa `bin/cake EmailQueue.sender`
```

### Estado dos Pods

| Recurso | Qtd | Observação |
|----|----|----|
| Deployment `passbolt-depl-srv` | 1 réplica | Sessões PHP em arquivo — não pode escalar sem Redis |
| CronJob `passbolt-cron-proc-email` | Frequente | Processa fila de e-mails |
| PVCs | Nenhum | Sem armazenamento local |
| ExternalSecrets | 3 | `passbolt-env`, `passbolt-gpg`, `passbolt-jwt` |

### Configurações Críticas no values.yaml

```yaml

app:
  image:
    repository: passbolt/passbolt
    tag: "5.10.0-1-ce"
  replicaCount: 1
  database:
    kind: postgresql
  cache:
    redis:
      enabled: false          # Sessões PHP em arquivo local (sem Redis)

gpgExistingSecret: "passbolt-gpg"
jwtExistingSecret: "passbolt-jwt"

passboltEnv:
  secretName: "passbolt-env"
  plain:
    APP_FULL_BASE_URL: "https://cofre.seazone.com.br"
    SESSION_DEFAULTS: php
    CACHE_DEFAULT_CLASSNAME: File
```

### ExternalSecrets no AWS SSM (ClusterSecretStore: `aws-parameter-store-global`)

| Secret K8s | Chave SSM | Conteúdo |
|----|----|----|
| `passbolt-env` → `DATASOURCES_DEFAULT_HOST` | `/sre/passbolt/production/DATASOURCES_DEFAULT_HOST` | Host do banco |
| `passbolt-env` → `DATASOURCES_DEFAULT_PORT` | `/sre/passbolt/production/DATASOURCES_DEFAULT_PORT` | Porta do banco |
| `passbolt-env` → `DATASOURCES_DEFAULT_USERNAME` | `/sre/passbolt/production/DATASOURCES_DEFAULT_USERNAME` | Usuário do banco |
| `passbolt-env` → `DATASOURCES_DEFAULT_PASSWORD` | `/sre/passbolt/production/DATASOURCES_DEFAULT_PASSWORD` | Senha do banco |
| `passbolt-env` → `DATASOURCES_DEFAULT_DATABASE` | `/sre/passbolt/production/DATASOURCES_DEFAULT_DATABASE` | Nome do banco |
| `passbolt-env` → `PASSBOLT_GPG_SERVER_KEY_FINGERPRINT` | `/sre/passbolt/production/PASSBOLT_GPG_SERVER_KEY_FINGERPRINT` | Fingerprint GPG |
| `passbolt-env` → `EMAIL_TRANSPORT_DEFAULT_*` | `/sre/passbolt/production/EMAIL_TRANSPORT_DEFAULT_*` | Config SMTP |
| `passbolt-gpg` → `serverkey.asc` | `/sre/passbolt/production/serverkey.asc` | Chave pública GPG |
| `passbolt-gpg` → `serverkey_private.asc` | `/sre/passbolt/production/serverkey_private.asc` | **CHAVE PRIVADA GPG** |
| `passbolt-jwt` → `jwt.key` | `/sre/passbolt/production/jwt.key` | Chave privada JWT |
| `passbolt-jwt` → `jwt.pem` | `/sre/passbolt/production/jwt.pem` | Certificado JWT |

> Todos esses parâmetros já estão no AWS SSM. O ExternalSecretStore no EKS (`aws-secrets-manager-ssm`) pode acessar os mesmos parâmetros desde que os caminhos (`/sre/passbolt/production/...`) existam e o IAM role do EKS tenha permissão.


---

## 2. Arquitetura Destino (EKS)

### Topologia

```
Internet
    │
Traefik NLB (EKS, sg-0a3cb448a1d444487)
    └─ cofre.seazone.com.br → IngressRoute → Service: passbolt:443
                                                    │
                                            Pod: passbolt
                                      (passbolt/passbolt:5.10.0-1-ce)
                                                    │
                               ┌────────────────────┤
                          RDS PostgreSQL        ExternalSecrets (AWS SSM)
                       (tools-postgres,        ┌─ passbolt-env
                        schema: passbolt)       ├─ passbolt-gpg
                                                └─ passbolt-jwt

CronJob: passbolt-cron-proc-email (mantido, mesma configuração)
PodDisruptionBudget: minAvailable=1 (mantido)
```

### Decisões de Infraestrutura

| Componente | Decisão | Justificativa |
|----|----|----|
| PostgreSQL | RDS `tools-postgres` — novo schema `passbolt` | Consolida bancos na AWS, sem custo adicional |
| Redis | Não necessário | Sessões PHP em arquivo (`SESSION_DEFAULTS: php`) |
| GPG/JWT | Reusar os mesmos do SSM | Chaves já estão no SSM, não gerar novas |
| ExternalSecretStore | `aws-secrets-manager-ssm` (EKS) | Mesmo store já configurado no EKS |
| NodePool | `general-karpenter-system` | Tool interna |
| Réplicas | 1 (mantido) | Sessões PHP em arquivo não são compartilháveis |


---

## 3. Sobre as Chaves GPG e JWT — Aspectos Críticos

### Por que são críticas

O Passbolt usa criptografia assimétrica (OpenPGP):

* Cada senha armazenada é **encriptada com a chave pública GPG do servidor**
* A **chave privada GPG** é necessária para decriptar ao servir senhas aos usuários
* Se a chave privada mudar ou for perdida: **todos os dados encriptados são irrecuperáveis**
* O fingerprint no banco de dados deve corresponder **exatamente** à chave em uso

As chaves JWT (`.key` e `.pem`) são usadas para autenticação:

* Mobile app e API REST usam JWT para autenticação
* Se as chaves mudarem, todos os usuários com sessões JWT ativas precisarão re-autenticar

### Premissa da Migração

**As chaves GPG e JWT JA ESTAO no AWS SSM** (`/sre/passbolt/production/serverkey.asc`, etc.). Isso significa:

* Não é necessário exportar as chaves do GKE — elas já estão seguras no SSM
* O EKS lerá as mesmas chaves via ExternalSecrets
* A única ação necessária é garantir que o ClusterSecretStore correto está sendo usado

### Verificação Pré-migração das Chaves

Claude Code executa os comandos abaixo e apresenta o resultado. O engenheiro **valida visualmente o fingerprint GPG** — esta é a única etapa que exige julgamento humano.

```bash
# 1. Confirmar que os parâmetros existem no SSM

aws ssm get-parameter --name "/sre/passbolt/production/serverkey.asc" --region sa-east-1 --query "Parameter.Value" --with-decryption | head -5

aws ssm get-parameter --name "/sre/passbolt/production/serverkey_private.asc" --region sa-east-1 --with-decryption --query "Parameter.Value" | head -5

aws ssm get-parameter --name "/sre/passbolt/production/PASSBOLT_GPG_SERVER_KEY_FINGERPRINT" --region sa-east-1 --query "Parameter.Value"

# 2. Confirmar que o fingerprint no SSM corresponde à chave pública
# Extrair fingerprint da chave pública no SSM

aws ssm get-parameter --name "/sre/passbolt/production/serverkey.asc" --with-decryption --query "Parameter.Value" --output text | \
  gpg --import --batch 2>&1 | grep fingerprint

# 3. Confirmar chaves JWT

aws ssm get-parameter --name "/sre/passbolt/production/jwt.key" --with-decryption --region sa-east-1 --query "Parameter.Value" | head -3

aws ssm get-parameter --name "/sre/passbolt/production/jwt.pem" --with-decryption --region sa-east-1 --query "Parameter.Value" | head -3

# 4. Cross-check: buscar o fingerprint diretamente no banco de dados GKE

kubectl exec -n passbolt deploy/passbolt-depl-srv -- \
  su -s /bin/bash www-data -c "bin/cake passbolt show_fingerprint"
```

### Validação Pós-migração das Chaves GPG

Claude Code executa os checks automaticamente. O engenheiro **confirma o login e recupera uma senha existente na interface** — validação que não pode ser automatizada.

```bash
# 1. Verificar que o pod subiu sem erros GPG

kubectl logs -n passbolt deploy/passbolt -c passbolt | grep -i gpg

# 2. Testar healthcheck

curl -k https://cofre.seazone.com.br/healthcheck/status.json

# 3. Verificar fingerprint carregado pelo servidor

kubectl exec -n passbolt deploy/passbolt -- \
  gpg --list-keys --keyid-format LONG

# 4. Testar decriptação — fazer login e recuperar uma senha existente na interface
# Se a senha aparecer corretamente → chave GPG funcionando
```


---

## 4. Arquivos de Configuração EKS

### 4.1 Application ArgoCD (`argocd/applications/passbolt/application.yaml`)

Claude Code escreve e commita o arquivo ao vivo durante a janela. Alterar `destination.server` de GKE para EKS:

```yaml

apiVersion: argoproj.io/v1alpha1

kind: Application

metadata:
  name: passbolt
  namespace: argocd
  finalizers:
    - resources-finalizer.argocd.argoproj.io

spec:
  project: default
  revisionHistoryLimit: 2
  sources:
    - repoURL: 'https://download.passbolt.com/charts/passbolt'
      chart: passbolt
      targetRevision: 2.1.0
      helm:
        valueFiles:
          - $values/argocd/applications/passbolt/values.yaml
    - repoURL: 'https://github.com/seazone-tech/gitops-governanca.git'
      targetRevision: HEAD
      ref: values
    - repoURL: 'https://github.com/seazone-tech/gitops-governanca.git'
      targetRevision: HEAD
      path: argocd/applications/passbolt
      directory:
        include: '{external-secret.yaml,ingressroute.yaml,pdb.yaml}'
  destination:
    server: 'https://kubernetes.default.svc'   # EKS general-cluster
    namespace: 'passbolt'
  syncPolicy:
    automated:
      prune: true
      selfHeal: true
    syncOptions:
      - CreateNamespace=true
```

### 4.2 Values EKS — Mudanças no `values.yaml`

```yaml
# Adicionar nodeSelector/tolerations para EKS Karpenter

app:
  image:
    repository: passbolt/passbolt
    tag: "5.10.0-1-ce"
  replicaCount: 1
  database:
    kind: postgresql
  databaseInitContainer:
    enabled: true
  cache:
    redis:
      enabled: false
  resources:
    requests:
      cpu: 250m
      memory: 512Mi
    limits:
      cpu: 1000m
      memory: 1Gi
  # Adicionar para EKS:
  nodeSelector:
    karpenter.sh/nodepool: general-karpenter-system
  tolerations:
    - key: "NodeType"
      operator: "Equal"
      value: "ClusterServices"
      effect: "NoSchedule"

# Manter configurações de chaves (sem alteração)
gpgExistingSecret: "passbolt-gpg"
jwtExistingSecret: "passbolt-jwt"

ingress:
  enabled: false

passboltEnv:
  secretName: "passbolt-env"
  plain:
    APP_FULL_BASE_URL: "https://cofre.seazone.com.br"
    PASSBOLT_EMAIL_VALIDATE_MX: "true"
    PASSBOLT_PLUGINS_SELF_REGISTRATION_ENABLED: "true"
    SESSION_DEFAULTS: php
    CACHE_DEFAULT_CLASSNAME: File
    CACHE_CAKEMODEL_CLASSNAME: File
    CACHE_CAKECORE_CLASSNAME: File
```

### 4.3 ExternalSecrets — Ajuste do ClusterSecretStore

O arquivo `external-secret.yaml` usa `aws-parameter-store-global` (nome do store no GKE). No EKS, o store é `aws-secrets-manager-ssm`. **Verificar se os paths** `**/sre/passbolt/production/...**` **existem no SSM acessível pelo store do EKS.**

Se os paths forem os mesmos, apenas atualizar `secretStoreRef.name`:

```yaml
# Em todos os 3 ExternalSecrets, mudar:
secretStoreRef:
  name: aws-secrets-manager-ssm   # era: aws-parameter-store-global
  kind: ClusterSecretStore
```

> **Importante:** Se os parâmetros SSM forem path `/sre/passbolt/...` e o ClusterSecretStore `aws-secrets-manager-ssm` do EKS usar um prefixo diferente ou outra conta, será necessário ajustar os `remoteRef.key` também. Confirmar com o time de infra qual o store correto e os paths acessíveis.

### 4.4 IngressRoute EKS (`argocd/applications/passbolt/ingressroute.yaml`)

O arquivo existente pode ser reutilizado sem alterações — o Traefik já roda no EKS e a configuração é idêntica:

```yaml
# ingressroute.yaml existente — sem mudanças
# cofre.seazone.com.br → Service passbolt:443 com insecureSkipVerify:true
```


---

## 5. Migração do Banco de Dados

### 5.1 Criar Schema no RDS tools-postgres

```sql
-- Executar como admin no RDS tools-postgres

CREATE USER passbolt WITH PASSWORD '<senha-nova-forte>';
CREATE DATABASE passbolt OWNER passbolt;
GRANT ALL PRIVILEGES ON DATABASE passbolt TO passbolt;

-- Atualizar o parâmetro SSM com o novo host/usuário/senha
```

### 5.2 Atualizar Parâmetros SSM

Após criar o usuário no RDS, Claude Code atualiza os parâmetros no SSM:

```bash
# Novo host do banco (RDS EKS)
aws ssm put-parameter \
  --name "/sre/passbolt/production/DATASOURCES_DEFAULT_HOST" \
  --value "<tools-postgres-endpoint>.sa-east-1.rds.amazonaws.com" \
  --type "SecureString" \
  --overwrite \
  --region sa-east-1

aws ssm put-parameter \
  --name "/sre/passbolt/production/DATASOURCES_DEFAULT_USERNAME" \
  --value "passbolt" \
  --type "SecureString" \
  --overwrite \
  --region sa-east-1

aws ssm put-parameter \
  --name "/sre/passbolt/production/DATASOURCES_DEFAULT_PASSWORD" \
  --value "<senha-nova>" \
  --type "SecureString" \
  --overwrite \
  --region sa-east-1

aws ssm put-parameter \
  --name "/sre/passbolt/production/DATASOURCES_DEFAULT_DATABASE" \
  --value "passbolt" \
  --type "SecureString" \
  --overwrite \
  --region sa-east-1
```

> **ATENCAO:** Atualizar os parâmetros SSM afeta o GKE imediatamente (refresh interval: 1m no ExternalSecret). Fazer isso apenas durante a janela de manutenção, com o GKE já em modo de manutenção (réplicas 0 ou DNS apontando para manutenção).

### 5.3 Dump do Banco no GKE

**Passo crítico — Claude Code executa antes de alterar qualquer coisa:**

```bash
# 1. Identificar o pod atual

kubectl get pods -n passbolt

# 2. Verificar o host do banco que está sendo usado

kubectl exec -n passbolt deploy/passbolt-depl-srv -- \
  env | grep DATASOURCES_DEFAULT_HOST

# 3. Executar dump via pod (o pod já tem acesso ao banco)
kubectl exec -n passbolt deploy/passbolt-depl-srv -- \
  bash -c "PGPASSWORD=\$DATASOURCES_DEFAULT_PASSWORD pg_dump \
    -h \$DATASOURCES_DEFAULT_HOST \
    -p \$DATASOURCES_DEFAULT_PORT \
    -U \$DATASOURCES_DEFAULT_USERNAME \
    -d \$DATASOURCES_DEFAULT_DATABASE \
    -Fc -v -f /tmp/passbolt_dump.dump"

# 4. Copiar o dump para a máquina local

kubectl cp passbolt/<nome-do-pod>:/tmp/passbolt_dump.dump ./passbolt_dump.dump

# 5. Verificar integridade do dump

pg_restore --list ./passbolt_dump.dump | head -30
```

### 5.4 Export via CLI do Passbolt (alternativa/complemento)

O Passbolt possui CLI para exportar senhas em formato legível. Usar como backup adicional, não como fonte de restauração:

```bash
# Export de todas as senhas (formato CSV ou JSON)
kubectl exec -n passbolt deploy/passbolt-depl-srv -- \
  su -s /bin/bash www-data -c \
  "bin/cake export --format=csv --file=/tmp/passbolt_export.csv"

kubectl cp passbolt/<pod>:/tmp/passbolt_export.csv ./passbolt_export.csv

# ATENCAO: Este arquivo contém todas as senhas em texto claro após decriptação.
# Armazenar com máximo cuidado e deletar após confirmação de migração bem-sucedida.
```

### 5.5 Restaurar no RDS tools-postgres

```bash
# Restaurar dump no RDS

pg_restore \
  -h <tools-postgres-endpoint>.sa-east-1.rds.amazonaws.com \
  -U passbolt \
  -d passbolt \
  -v \
  --no-owner \
  --no-acl \
  ./passbolt_dump.dump

# Verificar restauração

psql -h <endpoint> -U passbolt -d passbolt \
  -c "SELECT COUNT(*) FROM users; SELECT COUNT(*) FROM resources; SELECT COUNT(*) FROM secrets;"
```

### 5.6 Verificar Integridade dos Dados

```bash
# Comparar contagem de tabelas críticas entre GKE e EKS
# No GKE (antes da migração):
kubectl exec -n passbolt deploy/passbolt-depl-srv -- \
  bash -c "PGPASSWORD=\$DATASOURCES_DEFAULT_PASSWORD psql \
    -h \$DATASOURCES_DEFAULT_HOST \
    -U \$DATASOURCES_DEFAULT_USERNAME \
    -d \$DATASOURCES_DEFAULT_DATABASE \
    -c 'SELECT COUNT(*) as users FROM users; SELECT COUNT(*) as secrets FROM secrets; SELECT COUNT(*) as resources FROM resources;'"

# No RDS após restauração (deve ser idêntico):
psql -h <endpoint> -U passbolt -d passbolt \
  -c "SELECT COUNT(*) as users FROM users; SELECT COUNT(*) as secrets FROM secrets; SELECT COUNT(*) as resources FROM resources;"
```


---

## 6. Configuração do CronJob de E-mail no EKS

O CronJob `passbolt-cron-proc-email` é criado automaticamente pelo chart Helm. Verificar que está funcionando após o deploy:

```bash
# Verificar CronJob criado

kubectl get cronjob -n passbolt

# Verificar último job executado

kubectl get jobs -n passbolt

# Verificar logs do último job

kubectl logs -n passbolt \
  $(kubectl get pods -n passbolt -l job-name --sort-by=.metadata.creationTimestamp -o name | tail -1)
```

O chart do Passbolt cria o CronJob automaticamente — não é necessário criar manualmente. A configuração SMTP vem dos ExternalSecrets (`passbolt-env`), que já contém `EMAIL_TRANSPORT_DEFAULT_*`.


---

## 7. Janela de Manutenção

**Duração estimada:** 30 a 45 minutos **Horário recomendado:** Sábado à noite ou domingo de madrugada (uso mínimo) **Impacto:** Acesso ao cofre de senhas indisponível durante a migração

> **Claude Code executa todos os comandos ao vivo.** As janelas reais são dominadas por: propagação DNS (\~5 min), sincronização ArgoCD (\~3 min) e startup do pod (\~2 min). Não há trabalho de preparação manual — tudo é feito durante a janela com o engenheiro acompanhando.

### Comunicação Pré-Manutenção

* Avisar com pelo menos **1 a 2 dias de antecedência** no canal #geral ou equivalente — o Passbolt é ferramenta interna e um downtime de 30 minutos é gerenciável com aviso curto
* Pedir que o time salve credenciais críticas localmente antes da janela
* Confirmar janela com liderança de Engineering

### Execução da Janela

| Horário | Ação | Responsável |
|----|----|----|
| T-60min | Comunicar início iminente no Slack | SRE |
| T+00 | Página de manutenção no DNS (ou mensagem no Traefik) | SRE |
| T+05 | Escalar réplicas do GKE para 0 (Claude Code executa) | SRE valida |
| T+08 | Dump do banco PostgreSQL no GKE (Claude Code executa) | SRE valida |
| T+12 | Restaurar dump no RDS tools-postgres (Claude Code executa) | SRE valida |
| T+16 | Verificar integridade: contagem de tabelas GKE vs RDS (Claude Code compara) | SRE valida |
| T+18 | Atualizar parâmetros SSM com novo host do banco (Claude Code executa) | SRE valida |
| T+20 | Commit do `application.yaml` apontando para EKS (Claude Code escreve e commita) | SRE valida |
| T+23 | ArgoCD sincroniza — aguardar pods Running (\~3 min) | SRE acompanha |
| T+26 | Validar ExternalSecrets sincronizados (Claude Code verifica) | SRE valida |
| T+28 | **Testar login no Passbolt** | **Engenheiro valida** |
| T+30 | **Recuperar 2-3 senhas existentes e verificar que decriptam corretamente** | **Engenheiro + usuário de referência** |
| T+33 | Atualizar DNS Cloudflare para NLB do EKS (Claude Code executa) | SRE valida |
| T+38 | Aguardar propagação DNS (\~5 min) e testar acesso externo | SRE acompanha |
| T+40 | Confirmar CronJob de e-mail funcionando (Claude Code verifica logs) | SRE valida |
| T+43 | Declarar migração concluída no Slack | SRE |


---

## 8. Plano de Rollback Detalhado

### Cenário 1: Falha antes de alterar o DNS (até T+32)

Rollback é simples — usuários ainda acessam o GKE:

```bash
# 1. Identificar o problema (logs, ExternalSecrets, banco)
kubectl logs -n passbolt deploy/passbolt -c passbolt

# 2. Se necessário, reverter os parâmetros SSM para o banco GKE original

aws ssm put-parameter \
  --name "/sre/passbolt/production/DATASOURCES_DEFAULT_HOST" \
  --value "<host-original-gke>" \
  --type "SecureString" \
  --overwrite \
  --region sa-east-1

# 3. Reescalar no GKE

kubectl scale deployment passbolt-depl-srv -n passbolt --replicas=1 \
  --context=gke_<project>_us-central1-a_cluster-tools-prod-gke

# 4. Serviço restaurado — DNS não foi alterado
```

### Cenário 2: Falha após mudança de DNS

```bash
# 1. Reverter DNS no Cloudflare imediatamente
#    cofre.seazone.com.br → IP/CNAME original do GKE
#    TTL baixo (60s) para propagação rápida

# 2. Reverter parâmetros SSM para banco GKE (se já foram alterados)
aws ssm put-parameter \
  --name "/sre/passbolt/production/DATASOURCES_DEFAULT_HOST" \
  --value "<host-original-gke>" \
  --overwrite ...

# 3. Reescalar GKE

kubectl scale deployment passbolt-depl-srv -n passbolt --replicas=1 \
  --context=gke_<project>_...

# 4. Aguardar propagação DNS (até 5 minutos com TTL 60s)
# 5. Testar acesso via GKE
# 6. Comunicar usuários sobre restauração
```

### Cenário 3: Dados corrompidos após migração

**Este é o cenário mais grave.** Se os dados no RDS estiverem corrompidos mas o banco GKE ainda existir:

```bash
# 1. O banco GKE deve ser preservado por pelo menos 7 dias pós-migração
# 2. Reverter para banco GKE (via parâmetros SSM)
# 3. Investigar causa da corrupção
# 4. Reexecutar dump/restore com validação mais detalhada
```

### Checklist de Decisão de Rollback

- [ ] Pod em `CrashLoopBackOff` após 10 minutos → Rollback
- [ ] Erro de autenticação GPG nos logs → Rollback imediato (chave incorreta)
- [ ] ExternalSecret não sincroniza após 5 minutos → Investigar IAM/SSM, rollback se > 15min
- [ ] Login funciona mas senhas não decriptam → **Rollback imediato** (problema de chave GPG)
- [ ] Banco inacessível ou dados inconsistentes → Rollback imediato
- [ ] CronJob de e-mail falhando → Não é bloqueante, pode ser corrigido após migração


---

## 9. Checklist de Validação

### Pré-migração

- [ ] Confirmar todos os 11 parâmetros SSM existem e têm valor não-vazio
- [ ] Confirmar que o ClusterSecretStore `aws-secrets-manager-ssm` no EKS tem acesso ao prefixo `/sre/passbolt/production/`
- [ ] Criar schema e usuário `passbolt` no RDS tools-postgres
- [ ] Confirmar que o RDS está acessível a partir do EKS (security groups, VPC peering)
- [ ] **Engenheiro valida o fingerprint GPG** (Claude Code exibe o valor do SSM e do banco GKE lado a lado)
- [ ] Fazer backup adicional: `kubectl exec ... -- bin/cake export`
- [ ] Arquivar o fingerprint GPG atual: `aws ssm get-parameter --name /sre/passbolt/production/PASSBOLT_GPG_SERVER_KEY_FINGERPRINT`
- [ ] Comunicar manutenção aos usuários com 1-2 dias de antecedência

### Durante a Migração

- [ ] Réplicas GKE zeradas antes de alterar banco
- [ ] Contagem de tabelas idêntica entre GKE e RDS
- [ ] Parâmetros SSM atualizados com novo host RDS
- [ ] `application.yaml` commitado apontando para EKS

### Pós-migração (EKS)

- [ ] Pod `passbolt` em estado `Running`
- [ ] ExternalSecrets sincronizados (`kubectl get externalsecret -n passbolt`)
  * `passbolt-env` → `SecretSynced: True`
  * `passbolt-gpg` → `SecretSynced: True`
  * `passbolt-jwt` → `SecretSynced: True`
- [ ] Logs sem erros GPG (`kubectl logs -n passbolt deploy/passbolt | grep -i "gpg\|error\|fatal"`)
- [ ] Healthcheck retornando 200: `curl -k https://cofre.seazone.com.br/healthcheck/status.json`
- [ ] **Engenheiro confirma login bem-sucedido com conta de teste**
- [ ] **Engenheiro recupera pelo menos 3 senhas existentes e verifica que o conteúdo está correto**
- [ ] Criar nova entrada de senha e verificar que aparece para outros usuários
- [ ] CronJob `passbolt-cron-proc-email` existindo no namespace
- [ ] Envio de e-mail de teste funcionando (convidar um usuário fictício e verificar envio)
- [ ] PodDisruptionBudget criado (`kubectl get pdb -n passbolt`)
- [ ] IngressRoute ativo e DNS apontando para EKS
- [ ] Sem alertas ativos no Alertmanager para o namespace `passbolt`

### Pós-migração (D+7)

- [ ] Monitoramento sem erros por 7 dias
- [ ] Todos os usuários reportaram acesso normal
- [ ] Snapshot do banco GKE arquivado antes de descomissionar
- [ ] Deployments do GKE escalados para 0 (não deletar por mais 7 dias)
- [ ] Após confirmação total: remover recursos do GKE e descomissionar cluster


---

## 10. Referências e Contatos

| Recurso | Detalhe |
|----|----|
| URL produção | <https://cofre.seazone.com.br> |
| Helm chart | `https://download.passbolt.com/charts/passbolt` v2.1.0 |
| Documentação Passbolt CLI | <https://www.passbolt.com/docs/admin/cli-reference> |
| ArgoCD | <https://argocd.seazone.com.br> (app: `passbolt`) |
| Grafana | <https://monitoring.seazone.com.br> |
| Slack notificações | #tech-argocd |
| AWS Account | 711387131913 (sa-east-1) |
| SSM Path prefix | `/sre/passbolt/production/` |