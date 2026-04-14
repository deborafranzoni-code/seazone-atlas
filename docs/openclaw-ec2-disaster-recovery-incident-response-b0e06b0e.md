<!-- title: OpenClaw EC2 — Disaster Recovery & Incident Response | url: https://outline.seazone.com.br/doc/openclaw-ec2-disaster-recovery-incident-response-xJ8PI7cabz | area: Tecnologia -->

# OpenClaw EC2 — Disaster Recovery & Incident Response

> **Instância:** `i-05a410435fcca3183` (m7g.xlarge, sa-east-1a) **AMI Golden:** `ami-06f9d017cf2445a86` (01/04/2026) **Dashboard:** [monitoring.seazone.com.br/d/openclaw-ec2](https://monitoring.seazone.com.br/d/openclaw-ec2) **Responsável:** SRE — Governança Tech


---

## Arquitetura de Resiliência Atual

```mermaidjs
graph TB
  subgraph Internet
    CF["☁️ CloudFront<br/>alfredo.seazone.com.br<br/>garra.seazone.com.br"]
  end

  subgraph AWS sa-east-1a
    subgraph EC2["EC2 m7g.xlarge<br/>i-05a410435fcca3183"]
      Docker["🐳 openclaw-gateway<br/>restart: unless-stopped"]
      CWAgent["📊 CloudWatch Agent<br/>/var/log/secure"]
      Rsyslog["📝 rsyslog<br/>journald → secure"]
    end
    EBS["💾 EBS gp3 50GB<br/>encrypted<br/>vol-08c233420d03989c8"]
    DLM["📸 DLM Snapshots<br/>diários, 3 retenções"]
    AMI["🖼️ AMI Golden<br/>ami-06f9d017cf2445a86"]
    CWAlarm["⚡ Auto-Recovery Alarm<br/>StatusCheckFailed → recover"]
  end

  subgraph Observabilidade
    CWLogs["📋 CloudWatch Logs<br/>/ec2/openclaw<br/>/ec2/openclaw/auth<br/>/aws/cloudtrail"]
    Grafana["📈 Grafana Dashboard<br/>openclaw-ec2"]
    Alerts["🔔 Alertas Slack<br/>container parado<br/>EC2 fora do ar<br/>SG 0.0.0.0/0"]
  end

  subgraph Secrets
    SSM["🔐 SSM Parameter Store<br/>/sre/openclaw/*"]
  end

  CF --> Docker
  Docker --> EBS
  EBS --> DLM
  EC2 --> CWAlarm
  CWAgent --> CWLogs
  CWLogs --> Grafana
  Grafana --> Alerts
  SSM -.->|popula .env| Docker

  style CF fill:#1a73e8,color:#fff
  style Docker fill:#0db7ed,color:#fff
  style EBS fill:#e8710a,color:#fff
  style DLM fill:#e8710a,color:#fff
  style AMI fill:#4caf50,color:#fff
  style CWAlarm fill:#ff5722,color:#fff
  style SSM fill:#7b1fa2,color:#fff
  style Grafana fill:#f46800,color:#fff
  style Alerts fill:#d32f2f,color:#fff
```


---

## Mecanismos de Proteção

| Mecanismo | O que protege | RPO | RTO |
|----|----|----|----|
| `restart: unless-stopped` | Crash do container | 0 | \~30s |
| Auto-Recovery Alarm | Falha de hardware EC2 | 0 | \~2min |
| DLM Snapshots (diários) | Perda do volume EBS | até 24h | \~15min |
| AMI Golden | Reconstrução total da EC2 | 0 (SO+software) | \~5min |
| SSM Parameter Store | Perda de secrets | 0 | \~2min |
| CloudWatch Logs (14d) | Auditoria e investigação | 0 | imediato |
| CloudTrail | Rastreamento de quem fez o quê | 0 | imediato |


---

## Cenários de Incidente

### 1. Container parou (docker stop / crash)

**Sintomas:** garra.seazone.com.br fora, bots Slack offline **Alerta:** "Container OpenClaw PARADO na EC2" no Slack **Causa provável:** alguém executou `docker stop`, crash por token inválido, OOM kill

```mermaidjs
flowchart LR
  A["🔔 Alerta recebido"] --> B{"Container reiniciou<br/>sozinho?"}
  B -->|Sim, restart policy| C["✅ Verificar logs<br/>do crash"]
  B -->|Não, stop manual| D["Investigar quem parou<br/>Dashboard → Acesso SSM"]
  D --> E["Reiniciar manualmente"]
  C --> F["Corrigir causa raiz<br/>token inválido? OOM?"]
  E --> F

  style A fill:#d32f2f,color:#fff
  style C fill:#4caf50,color:#fff
  style E fill:#ff9800,color:#fff
```

**Recovery:**

```bash
# 1. Verificar status
aws ssm send-command --instance-ids i-05a410435fcca3183 \
  --document-name AWS-RunShellScript \
  --parameters 'commands=["docker ps -a --filter name=openclaw"]' \
  --profile apps --region sa-east-1

# 2. Reiniciar
aws ssm send-command --instance-ids i-05a410435fcca3183 \
  --document-name AWS-RunShellScript \
  --parameters 'commands=["cd /opt/openclaw && docker compose up -d"]' \
  --profile apps --region sa-east-1

# 3. Verificar quem parou (se docker stop manual)
# Dashboard Grafana → seção "Acesso SSH / SSM — Quem entrou"
```

**Prevenção:** não executar `docker stop` diretamente. O `restart: unless-stopped` não reinicia após stop manual.


---

### 2. EC2 fora do ar (falha de hardware / instância parada)

**Sintomas:** todos os serviços offline, healthz não responde, métricas EC2 param **Alerta:** "EC2 do OpenClaw FORA DO AR" no Slack

```mermaidjs
flowchart TD
  A["🔔 StatusCheck Failed"] --> B{"Auto-Recovery<br/>resolveu?"}
  B -->|Sim ~2min| C["✅ Verificar container<br/>subiu com restart policy"]
  B -->|Não / instância stopped| D{"Instância existe?"}
  D -->|Sim, stopped| E["aws ec2 start-instances"]
  D -->|Não, terminated| F["🔴 Rebuild completo<br/>ver seção Rebuild"]

  style A fill:#d32f2f,color:#fff
  style C fill:#4caf50,color:#fff
  style F fill:#b71c1c,color:#fff
```

**Recovery:**

```bash
# 1. Verificar status da instância
aws ec2 describe-instance-status \
  --instance-ids i-05a410435fcca3183 \
  --profile apps --region sa-east-1

# 2. Se stopped, iniciar
aws ec2 start-instances \
  --instance-ids i-05a410435fcca3183 \
  --profile apps --region sa-east-1

# 3. Verificar quem parou
aws logs start-query --log-group-name "/aws/cloudtrail" \
  --start-time $(date -d '2 hours ago' +%s) --end-time $(date +%s) \
  --query-string "filter eventName='StopInstances' | display @timestamp, userIdentity.arn, sourceIPAddress" \
  --region sa-east-1 --profile apps
```


---

### 3. Volume EBS corrompido / deletado

**Sintomas:** container em crash loop com erro de I/O, dados inacessíveis **RPO:** até 24h (último snapshot DLM)

**Recovery:**

```bash
# 1. Identificar último snapshot
aws ec2 describe-snapshots \
  --filters Name=volume-id,Values=vol-08c233420d03989c8 \
  --query 'Snapshots | sort_by(@, &StartTime) | [-1]' \
  --profile apps --region sa-east-1

# 2. Criar volume a partir do snapshot
aws ec2 create-volume \
  --snapshot-id snap-XXXXXXXXXXXX \
  --volume-type gp3 \
  --encrypted \
  --availability-zone sa-east-1a \
  --profile apps --region sa-east-1

# 3. Parar instância, trocar volume, iniciar
aws ec2 stop-instances --instance-ids i-05a410435fcca3183 --profile apps --region sa-east-1
# Aguardar stopped, then:
aws ec2 detach-volume --volume-id vol-ANTIGO --profile apps --region sa-east-1
aws ec2 attach-volume --volume-id vol-NOVO --instance-id i-05a410435fcca3183 \
  --device /dev/xvda --profile apps --region sa-east-1
aws ec2 start-instances --instance-ids i-05a410435fcca3183 --profile apps --region sa-east-1
```


---

### 4. Instância terminada / rebuild completo

**Sintomas:** instância não existe mais, precisa recriar do zero **RTO:** \~10 minutos com AMI + snapshot

```mermaidjs
flowchart TD
  A["🔴 Instância perdida"] --> B["Lançar EC2 da AMI Golden<br/>ami-06f9d017cf2445a86"]
  B --> C["Restaurar EBS do<br/>último snapshot DLM"]
  C --> D["Montar volume como<br/>/dev/xvda"]
  D --> E["Recriar .env<br/>a partir do SSM"]
  E --> F["docker compose up -d"]
  F --> G["Atualizar CloudFront<br/>origin IP se mudou"]
  G --> H["Verificar healthz<br/>e bots Slack"]
  H --> I["✅ Serviço restaurado"]

  style A fill:#b71c1c,color:#fff
  style I fill:#4caf50,color:#fff
  style B fill:#1a73e8,color:#fff
  style E fill:#7b1fa2,color:#fff
```

**Recovery completo:**

```none
# 1. Lançar nova EC2 da AMI
aws ec2 run-instances \
  --image-id ami-06f9d017cf2445a86 \
  --instance-type m7g.xlarge \
  --subnet-id subnet-0738d4978d18db909 \
  --security-group-ids sg-06dab2b93c1e82409 \
  --iam-instance-profile Name=openclaw-ec2-profile \
  --block-device-mappings '[{"DeviceName":"/dev/xvda","Ebs":{"VolumeSize":50,"VolumeType":"gp3","Encrypted":true}}]' \
  --tag-specifications 'ResourceType=instance,Tags=[{Key=Name,Value=openclaw-ec2}]' \
  --profile apps --region sa-east-1

# 2. Restaurar dados do snapshot (ver cenário 3)

# 3. Recriar .env a partir do SSM
aws ssm get-parameters-by-path --path /sre/openclaw/ --with-decryption \
  --profile apps --region sa-east-1 \
  --query 'Parameters[*].[Name,Value]' --output text | \
  awk -F'\t' '{
    name=$1; gsub(/.*\//, "", name);
    gsub(/-/, "_", name);
    print toupper(name) "=" $2
  }' > .env

# 4. Subir serviço
cd /opt/openclaw && docker compose up -d

# 5. Atualizar CloudFront se IP privado mudou
# (verificar origin no CloudFront distribution)

# 6. Atualizar auto-recovery alarm com novo instance ID
```


---

### 5. Token Slack inválido derrubou o gateway (crash loop)

**Sintomas:** container reiniciando em loop, logs mostram `account_inactive` ou `invalid_auth` **Causa:** alguém adicionou um Slack account com token inválido ou variável de ambiente não definida

**Recovery:**

```bash
# 1. Identificar o account problemático
aws ssm send-command --instance-ids i-05a410435fcca3183 \
  --document-name AWS-RunShellScript \
  --parameters 'commands=["docker logs openclaw-gateway --tail 20 2>&1 | grep -i error"]' \
  --profile apps --region sa-east-1

# 2. Desabilitar o account (funciona mesmo com container em crash)
aws ssm send-command --instance-ids i-05a410435fcca3183 \
  --document-name AWS-RunShellScript \
  --parameters 'commands=["python3 -c \"import json; f=\\\"var/lib/docker/volumes/openclaw-data/_data/openclaw.json\\\"; d=json.load(open(f)); d[\\\"channels\\\"][\\\"slack\\\"][\\\"accounts\\\"][\\\"ACCOUNT_PROBLEMÁTICO\\\"][\\\"enabled\\\"]=False; open(f,\\\"w\\\").write(json.dumps(d,indent=2))\"", "docker restart openclaw-gateway"]' \
  --profile apps --region sa-east-1
```

**Prevenção:** o Agent Creator foi atualizado para sempre criar accounts com `enabled: false` e validar tokens antes de ativar.


---

### 6. Security Group aberto para 0.0.0.0/0

**Sintomas:** alerta Grafana "Security Group abriu porta para o mundo" **Risco:** exposição direta da EC2 à internet

**Recovery:**

```bash
# 1. Identificar a regra
aws ec2 describe-security-groups \
  --group-ids sg-06dab2b93c1e82409 \
  --query 'SecurityGroups[0].IpPermissions[?IpRanges[?CidrIp==`0.0.0.0/0`]]' \
  --profile apps --region sa-east-1

# 2. Revogar imediatamente
aws ec2 revoke-security-group-ingress \
  --group-id sg-06dab2b93c1e82409 \
  --protocol tcp --port PORTA \
  --cidr 0.0.0.0/0 \
  --profile apps --region sa-east-1

# 3. Investigar quem fez no CloudTrail
# Dashboard Grafana → seção "Acesso SSH / SSM"
```


---

### 7. Secrets comprometidos (token vazado)

**Sintomas:** atividade suspeita nos bots Slack, uso anormal de API **Risco:** acesso não autorizado aos agentes e ferramentas

**Recovery:**

```bash
# 1. Revogar tokens Slack imediatamente
# Acessar api.slack.com → cada app → OAuth → Revoke

# 2. Rotacionar OpenRouter API key
# Acessar openrouter.ai → API Keys → Revoke + Create new

# 3. Rotacionar GitHub token
# Acessar github.com → Settings → Tokens → Revoke + Create new

# 4. Atualizar SSM Parameter Store com novos valores
aws ssm put-parameter --name /sre/openclaw/slack-bot-token \
  --value "xoxb-NOVO-TOKEN" --type SecureString --overwrite \
  --profile apps --region sa-east-1

# 5. Atualizar .env na EC2 e reiniciar
aws ssm send-command --instance-ids i-05a410435fcca3183 \
  --document-name AWS-RunShellScript \
  --parameters 'commands=["cd /opt/openclaw && docker compose down && docker compose up -d"]' \
  --profile apps --region sa-east-1
```


---

## Inventário de Recursos

### Compute

| Recurso | ID | Detalhe |
|----|----|----|
| EC2 | `i-05a410435fcca3183` | m7g.xlarge, sa-east-1a |
| AMI Golden | `ami-06f9d017cf2445a86` | 01/04/2026 |
| Security Group | `sg-06dab2b93c1e82409` | Portas: 18789 (VPC only) |
| IAM Role | `openclaw-ec2-role` | SSM + CloudWatch Agent |
| Subnet | `subnet-0738d4978d18db909` | Private, sa-east-1a |

### Storage

| Recurso | ID | Detalhe |
|----|----|----|
| EBS Volume | `vol-08c233420d03989c8` | 50GB gp3, encrypted |
| DLM Policy | `policy-052f222beabb51608` | Diário, 3 retenções |
| Docker Volume | `openclaw-data` | Workspaces, config, sessions |

### Observabilidade

| Recurso | Detalhe |
|----|----|
| Log Group Gateway | `/ec2/openclaw` (14 dias) |
| Log Group Auth | `/ec2/openclaw/auth` (14 dias) |
| Log Group SSM | `/aws/ssm/sessions` (14 dias) |
| Log Group CloudTrail | `/aws/cloudtrail` (14 dias) |
| CloudTrail | `seazone-audit-trail` (multi-region) |
| S3 CloudTrail | `seazone-cloudtrail-711387131913` (14 dias lifecycle) |
| Grafana Dashboard | UID: `openclaw-ec2` |
| Auto-Recovery | `openclaw-ec2-auto-recovery` (CloudWatch Alarm) |

### Alertas Grafana

| Alerta | Trigger | Destino |
|----|----|----|
| Container parado | SIGTERM nos logs | Slack |
| EC2 fora do ar | StatusCheckFailed | Slack |
| SG abriu 0.0.0.0/0 | CloudTrail AuthorizeSecurityGroupIngress | Slack |

### Secrets (SSM Parameter Store)

| Parâmetro | Uso |
|----|----|
| `/sre/openclaw/gateway-token` | Auth do gateway |
| `/sre/openclaw/openrouter-api-key` | LLM API |
| `/sre/openclaw/slack-bot-token` | Garra bot |
| `/sre/openclaw/slack-app-token` | Garra socket mode |
| `/sre/openclaw/slack-bot-token-sherlog` | Sherlog bot |
| `/sre/openclaw/slack-app-token-sherlog` | Sherlog socket mode |
| `/sre/openclaw/github-token` | GitHub integration |

|    | Quem | Quando |
|----|----|----|


---

Checklist de Manutenção

- [ ] **Mensal:** atualizar AMI Golden com `aws ec2 create-image`
- [ ] **Após mudanças:** sincronizar `openclaw.json` com o git (main)
- [ ] **Após novos agentes:** verificar tokens no SSM Parameter Store