<!-- title: Migração GKE | url: https://outline.seazone.com.br/doc/migracao-gke-hLlRSqgrOH | area: Tecnologia -->

# Migração GKE

**Projeto:** Descomissionamento do cluster GKE `cluster-tools-prod-gke` (us-central1-a) **Destino:** Cluster EKS `general-cluster` (sa-east-1) **Responsável:** Time SRE + Claude Code **Status:** Em planejamento **Duração estimada:** 1 semana de trabalho


---

## Contexto

O cluster GKE em `us-central1-a` e instâncias GCP hospedam aplicações internas da Seazone (n8n, Baserow, Passbolt, Outline, Uptime Kuma, VPN, Vault) e infraestrutura de suporte (Traefik, Loki, External Secrets). O objetivo é consolidar tudo no EKS `general-cluster` (sa-east-1) e instâncias AWS, eliminando custos e complexidade multi-cloud.

O ArgoCD já roda no EKS e gerencia o repositório `gitops-governanca`. Toda a migração segue padrões GitOps existentes: multi-source applications, ExternalSecret via AWS SSM, Traefik como ingress.


---

## Como Usar Claude Code Nesta Migração

**O que Claude Code faz:**

* Executa `kubectl`, `helm`, `aws cli`, `pg_dump`, `pg_restore` e `git` diretamente
* Gera todos os manifests YAML (Applications, ExternalSecrets, IngressRoutes, values.yaml) ao vivo
* Aplica configurações no ArgoCD imediatamente após geração
* Diagnostica erros em tempo real e corrige sem overhead de troubleshooting manual

**O que o engenheiro faz:**

* Valida cada etapa antes de prosseguir
* Toma decisões de negócio (janelas, comunicação com usuários)
* Aprova ações destrutivas (delete de Applications, exclusão do cluster)

**Gargalos reais (não mudam com Claude Code):**

* Propagação DNS: \~5 min (Cloudflare TTL)
* ArgoCD sync após push: \~2–3 min
* Pods subindo: \~1–2 min
* Estabilização pós-migração: \~24h por app (monitoramento)


---

## Inventário de Aplicações e Ações

| # | Aplicação | Origem | Ação | Destino | Complexidade | Dia |
|----|----|----|----|----|----|----|
| 1 | **Outline** | GKE `outline` | Desligar | — | Baixa | Segunda |
| 2 | **Uptime Kuma** | Instância GCP | Migrar | EKS `monitoring` (já existe) | Baixa | Segunda |
| 3 | **N8N PRD** | GKE `prd-n8n` + `n8n` | Migrar | EKS `prd-n8n` | Média | Terça |
| 4 | **VPN** | Instância GCP | Migrar | Instância EC2 AWS | Média | Terça |
| 5 | **Baserow** | GKE `baserow` | Migrar | EKS `tools` | Média | Quarta |
| 6 | **Passbolt** | GKE `passbolt` | Migrar | EKS `tools` | Baixa | Quinta |
| 7 | **Vault** | Instância GCP | Descomissionar | — (substituído pelo Passbolt) | Baixa | Quinta |
| 8 | **Loki GKE** | GKE `monitoring` | Remover | — | Baixa | Quinta |
| 9 | **External Secrets GKE** | GKE `external-secrets` | Remover | — | Baixa | Quinta |
| 10 | **Traefik GKE** | GKE `traefik-system` | Remover | — | Baixa | Quinta |
| 11 | **incident-agent GKE** | GKE `incident-agent` | Remover | — | Baixa | Quinta |
| 12 | **Cluster GKE + Instâncias GCP** | — | Descomissionar | — | Baixa | Sexta |


---

## Infraestrutura de Destino

**RDS disponível no EKS:**

| Instância | Classe | Disponível |
|----|----|----|
| `tools-postgres` | db.t4g.small | ✅ Schemas dedicados: `n8n_prd`, `baserow`, `passbolt` |
| `reservas-prd-postgres` | db.t4g.medium | ❌ Em uso   |
| `sapron-prd-postgres` | db.t4g.medium | ❌ Em uso |

**Redis:** `redis-n8n-prd` já existe no EKS. Baserow e Passbolt usam Redis in-cluster simples.

**Storage:** Baserow usa S3 `tools-baserow` (sa-east-1) — já configurado.


---

## Timeline — 1 Semana

### Segunda — Outline + Uptime Kuma + Preparação

| Horário | Atividade | Executor |
|----|----|----|
| Manhã | Comunicar usuários do Outline (Slack #geral) | Engenheiro |
| Manhã | Criar schemas e usuários no `tools-postgres` para N8N, Baserow, Passbolt | Claude Code |
| Manhã | Criar/validar secrets no AWS SSM para as 3 apps | Claude Code |
| Tarde | Exportar documentos do Outline via API | Claude Code |
| Tarde | Importar docs para Notion/Canvas | Engenheiro |
| Tarde | Desligar Outline no ArgoCD (GKE) | Claude Code |
| Tarde | **Uptime Kuma:** exportar monitors da instância GCP (`Settings > Backup`) | Claude Code |
| Tarde | **Uptime Kuma:** importar backup no EKS `uptime-kuma-0` (monitoring namespace) | Claude Code |
| Tarde | **Uptime Kuma:** atualizar DNS para apontar para EKS | Claude Code |
| Tarde | Validar todos os monitors no Uptime Kuma EKS | Engenheiro |

> Outline é prioridade 0 pois depende de ação humana (importação de docs). Iniciar na Segunda garante tempo para o time validar o conteúdo migrado antes do final da semana.
>
> Uptime Kuma já roda no EKS (`monitoring/uptime-kuma-0`) — migração é somente importar o backup e cortar o DNS.


---

### Terça — Migração N8N PRD + VPN

**N8N PRD — Janela de manutenção:** 02h00–02h45 (Brasília) — `runbook: 01-n8n-prd.md`

| T+ | Atividade | Executor |
|----|----|----|
| T+00 | Escalar deployments `prd-n8n` e `n8n` para 0 | Claude Code |
| T+02 | `pg_dump` do `postgres-n8n` StatefulSet (GKE) | Claude Code |
| T+10 | `pg_restore` no `tools-postgres` schema `n8n_prd` (EKS) | Claude Code |
| T+20 | Gerar e aplicar Application ArgoCD → EKS + values.yaml (Redis, RDS) | Claude Code |
| T+25 | ArgoCD sync + pods subindo | Automático |
| T+30 | Atualizar DNS Cloudflare | Claude Code |
| T+35 | Validar: login, workflows, webhooks | Engenheiro |
| T+45 | Manter GKE em standby por 24h | — |

**VPN — Durante o dia (sem janela de manutenção crítica):**

| Atividade | Executor |
|----|----|
| Provisionar instância EC2 (mesma region sa-east-1, mesmo SG ou equivalente) | Claude Code |
| Instalar e configurar WireGuard/OpenVPN na EC2 | Claude Code |
| Exportar configurações de clientes da instância GCP | Engenheiro |
| Gerar configs de cliente apontando para nova EC2 | Claude Code |
| Distribuir novas configs para usuários (Slack) | Engenheiro |
| Validar conectividade com pelo menos 2 usuários | Engenheiro |
| Desligar instância GCP após confirmação | Engenheiro |


---

### Quarta — Migração Baserow

**Janela de manutenção:** 02h00–02h30 (Brasília) — `runbook: 02-baserow.md`

| T+ | Atividade | Executor |
|----|----|----|
| T+00 | Escalar Baserow para 0 réplicas (GKE) | Claude Code |
| T+02 | `pg_dump` do postgres externo GKE | Claude Code |
| T+10 | `pg_restore` no `tools-postgres` schema `baserow` (EKS) | Claude Code |
| T+20 | Gerar Application ArgoCD EKS + values.yaml (RDS, Redis, S3) | Claude Code |
| T+25 | ArgoCD sync + pods subindo | Automático |
| T+30 | Atualizar DNS Cloudflare | Claude Code |
| T+35 | Validar: tabelas, uploads S3, WebSocket | Engenheiro |
| T+40 | Manter GKE em standby por 24h | — |


---

### Quinta — Migração Passbolt + Limpeza GKE

**Passbolt — Janela:** 02h00–02h45 (Brasília) — `runbook: 03-passbolt.md`

| T+ | Atividade | Executor |
|----|----|----|
| T+00 | Escalar Passbolt para 0 (GKE) | Claude Code |
| T+02 | `pg_dump` do postgres externo GKE | Claude Code |
| T+10 | `pg_restore` no `tools-postgres` schema `passbolt` (EKS) | Claude Code |
| T+20 | Gerar ExternalSecrets (env, gpg, jwt) + Application EKS | Claude Code |
| T+25 | ArgoCD sync + pod subindo | Automático |
| T+30 | Atualizar DNS Cloudflare | Claude Code |
| T+35 | **Validar GPG:** login + recuperar senha de teste | Engenheiro |
| T+45 | Manter GKE em standby até Sexta | — |

**Vault — após confirmação do Passbolt no EKS:**

| Atividade | Executor |
|----|----|
| Confirmar que todos os secrets do Vault foram migrados para o Passbolt | Engenheiro |
| Confirmar que nenhuma app ainda consome secrets diretamente do Vault | Claude Code |
| Desligar instância GCP do Vault | Engenheiro |

**Limpeza GKE — após validação do Passbolt (Quinta tarde):**

| Ordem | Ação | Pré-requisito |
|----|----|----|
| 1 | Remover Loki (Application + namespace) | Nenhuma app ativa no GKE |
| 2 | Remover External Secrets (Application + namespace) | Nenhum ExternalSecret ativo |
| 3 | Remover Traefik (Application + namespace) | Nenhum IngressRoute ativo |
| 4 | Remover incident-agent (namespace) | — |


---

### Sexta — Descomissionamento do Cluster

| Atividade | Executor |
|----|----|
| Verificar checklist completo (ver abaixo) | Claude Code + Engenheiro |
| Confirmar N8N, Baserow, Passbolt estáveis há 24h+ | Engenheiro |
| Confirmar Uptime Kuma e VPN funcionando na AWS | Engenheiro |
| Remover cluster GKE do ArgoCD (Settings > Clusters) | Engenheiro |
| Confirmar e executar delete do cluster | Engenheiro |
| Verificar recursos GCP residuais (discos, LBs, IPs estáticos, instâncias) | Claude Code |
| Confirmar custo GKE + instâncias GCP zerado no GCP Billing | Engenheiro |

```bash

gcloud container clusters delete cluster-tools-prod-gke \
  --zone=us-central1-a \
  --project=tools-440117
```


---

## Checklist de Descomissionamento

Todos os itens devem estar ✅ antes de deletar o cluster:

- [ ] Nenhuma Application ArgoCD com `destination.server: https://34.60.64.40`
- [ ] N8N PRD respondendo normalmente via EKS por 24h+
- [ ] Baserow acessível e funcional via EKS por 24h+
- [ ] Passbolt com login e credenciais validados via EKS por 24h+
- [ ] Outline desligado e conteúdo confirmado pelos usuários
- [ ] Uptime Kuma monitors funcionando via EKS e instância GCP desligada
- [ ] VPN migrada para EC2 e usuários reconectados à nova instância
- [ ] Vault desligado — todos os secrets confirmados no Passbolt
- [ ] Backups RDS executados e validados para N8N, Baserow e Passbolt
- [ ] Monitoramento (alertas, dashboards Grafana) funcionando para apps migradas
- [ ] Repositório `gitops-governanca` sem manifests apontando para o GKE
- [ ] Namespaces GKE removidos: `outline`, `prd-n8n`, `n8n`, `baserow`, `passbolt`, `external-secrets`, `traefik-system`, `incident-agent`
- [ ] Instâncias GCP desligadas: Uptime Kuma, VPN, Vault
- [ ] Cluster removido do ArgoCD
- [ ] Custo GKE zerado confirmado no GCP Billing
- [ ] Custo instâncias GCP zerado confirmado no GCP Billing


---

## Riscos e Mitigações

| Risco | Prob. | Impacto | Mitigação |
|----|----|----|----|
| Perda de dados N8N durante migração | Baixa | Alto | Backup duplo (pg_dump + cronjob GCS). Claude Code valida contagem de registros. GKE ativo 24h após migração para rollback. |
| Workflows N8N quebrando por mudança de credenciais | Média | Alto | Manter `N8N_ENCRYPTION_KEY` idêntica. Testar workflows críticos antes de redirecionar DNS. |
| Passbolt com GPG inválido após migração | Baixa | Alto | Claude Code valida fingerprint GPG antes de redirecionar DNS. Rollback imediato se login falhar. |
| Outline com docs não migrados | Média | Médio | Exportar tudo na Segunda antes de desligar. Engenheiro confirma conteúdo antes do delete. |
| `tools-postgres` sobrecarregado após consolidação | Média | Médio | Monitorar CloudWatch na Quarta. Escalar para db.t4g.medium em minutos via RDS se necessário. |
| N8N initContainer com Workload Identity GCP | Alta | Médio | Substituir `npm-wrapper` no EKS por initContainer sem dependência de `metadata.google.internal`. Ver `01-n8n-prd.md`. |
| VPN: usuários ficam sem acesso durante cutover | Média | Alto | Preparar novas configs antes de desligar GCP. Distribuir no Slack com antecedência. Manter GCP ativa até 100% dos usuários confirmarem. |
| Vault: secrets não documentados no Passbolt | Média | Médio | Auditar todos os secrets do Vault antes de desligar. Engenheiro confirma que nada foi esquecido. |
| Uptime Kuma: monitors com configurações customizadas perdidas | Baixa | Baixo | Usar export/import nativo do Uptime Kuma. Validar contagem de monitors antes e depois. |


---

## Runbooks Detalhados

| Documento | Conteúdo |
|----|----|
| [01-n8n-prd.md](./01-n8n-prd.md) | Migração N8N PRD — pg_dump/restore, ArgoCD, DNS, rollback |
| [02-baserow.md](./02-baserow.md) | Migração Baserow — postgres, Redis, S3, ArgoCD |
| [03-passbolt.md](./03-passbolt.md) | Migração Passbolt — GPG/JWT keys, postgres, ArgoCD |
| [04-outline-canvas.md](./04-outline-canvas.md) | Desligamento Outline — export API, import Notion/Canvas |
| [05-infra-decommission.md](./05-infra-decommission.md) | Remoção Loki, Traefik, External Secrets, cluster GKE |