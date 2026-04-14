<!-- title: Kestra 1.2.2 OSS — Features Self-Hosted (Comparativo) | url: https://outline.seazone.com.br/doc/kestra-122-oss-features-self-hosted-comparativo-CpmOMyehNC | area: Tecnologia -->

# Kestra 1.2.2 OSS — Features Self-Hosted (Comparativo)

Baseado na documentação oficial + nos problemas encontrados durante o teste do ambiente. Ambiente atual: **Kestra OSS 1.2.2** no GKE, PostgreSQL (Cloud SQL), GCS storage, DinD habilitado.


---

## Legenda

| Cor/símbolo | Significa |
|----|----|
| ==✅== | Disponível no OSS |
| ==❌== | Enterprise only |
| ==⚠️== | Disponível mas com limitações / workaround necessário |
| ==🔧== | Funciona, mas precisou de workaround no nosso ambiente |


---

## 1. Autenticação & Usuários

| Feature | Status | Detalhes |
|----|----|----|
| ==Basic Auth (usuário/senha)== | ✅ | Usuários armazenados no PostgreSQL (`settings` table). Senha: SHA-512 de `salt\|password` |
| ==Múltplos usuários== | ❌ | Enterprise only |
| ==SSO / OIDC== | ❌ | Enterprise only |
| ==RBAC (Role-Based Access Control)== | ❌ | Enterprise only |
| ==Service Accounts / API Tokens== | ❌ | Enterprise only |


---

## 2. Secrets & Configuração

| Feature | Status | Detalhes |
|----|----|----|
| ==Secret nos flows== | ==🔧== | Funciona via env vars com prefixo `SECRET_`. Valor deve ser base64. Como K8s faz decode automático do Secret, precisamos de **double base64.** É possível importar com boto, existe um plugin de aws CLI… |
| ==Namespace Variables== | ❌ | Enterprise only |
| ==Namespace-level Plugin Defaults== | ❌ | Enterprise only |
| ==Secrets via K8s Secret + extraEnv (workaround)== | ==🔧== | Isso é o que estamos usando. Funciona mas é manual |


---

## 3. Task Runners (execução de scripts)

| Feature | Status | Detalhes |
|----|----|----|
| ==Process Runner== | ==✅== | Executa diretamente no worker pod |
| ==Docker Runner== | ==🔧== | Disponível no OSS, mas precisou habilitar **DinD** (`dind: enabled: true`) no Helm porque o GKE usa containerd |
| ==Kubernetes Runner== | ==❌== | Enterprise only (`io.kestra.plugin.ee.kubernetes.runner.Kubernetes`) |
| ==AWS Batch Runner== | ==❌== | Enterprise only |
| ==Google Batch / Cloud Run Runner== | ==❌== | Enterprise only |


---

## 4. Flows & Orquestração

| Feature | Status | Detalhes |
|----|----|----|
| ==Flows YAML declarativos== | ==✅== |    |
| ==Tarefas sequenciais== | ==✅== |    |
| ==Tarefas paralelas== | ==✅== |    |
| ==Loops== | ==✅== |    |
| ==Branching / Switch== | ==✅== |    |
| ==Triggers (Schedule, Event, etc.)== | ==✅== | Usado `cron` no nosso flow |
| ==Error handlers== (`errors:`) | ==✅== | Funciona, mas `{{ task.error }}` não resolve no contexto do error handler — usar `{{ error }}` ou logar via outro mecanismo |
| ==outputFiles entre tasks== | ==✅== | Usado entre `fetch_posthog_views` → `calculate_ranking` |
| ==pluginDefaults (retry, etc.)== | ==✅== | Configurado no flow com retry `constant`, 3 tentativas |
| ==Custom Blueprints== | ==❌== | Enterprise only |


---

## 5. Linguagens & Scripts

| Feature | Status | Detalhes |
|----|----|----|
| ==Python== | ✅ | Usado via `io.kestra.plugin.scripts.python.Script` |
| ==Shell / Bash== | ✅ |    |
| ==Node.js== | ✅ |    |
| ==R== | ✅ |    |
| ==Ruby== | ✅ |    |
| ==PowerShell== | ✅ |    |
| ==Julia== | ✅ |    |
| ==dbt== | ✅ | Plugin separado |


---

## 6. Armazenamento & Backend

| Feature | Status | Detalhes |
|----|----|----|
| ==PostgreSQL como backend (queue + repository)== | ✅ | Usado no ambiente atual (Cloud SQL) |
| ==GCS como storage== | ✅ | Bucket `kestra-storage-tools-440117` |
|    |    |    |
| ==S3 como storage== | ✅ | Suportado como alternativa |
| ==Kafka como backend== | ❌ | Enterprise only (necessário para HA) |
| ==Elasticsearch== | ❌ | Enterprise only (logs + search) |


---

## 7. Escalabilidade & Alta Disponibilidade

| Feature | Status | Detalhes |
|----|----|----|
| ==Deploy com Helm no K8s== | ✅ | Chart `kestra-1.0.31` |
| ==Múltiplos pods (webserver, worker, etc.)== | ✅ | replicaCount configurável |
| ==High Availability (sem single point of failure)== | ❌ | Enterprise only (usa Kafka/ES) |
| ==Worker Groups== | ❌ | Enterprise only |
| ==Horizontal scaling automático== | ❌ | Enterprise only |
| ==Backup & Restore== | ❌ | Enterprise only |


---

## 8. Monitoramento & Observabilidade

| Feature | Status | Detalhes |
|----|----|----|
| ==Logs das execuções no UI== | ✅ | Armazenados no PostgreSQL (`logs` table) |
| ==Audit Logs== | ❌ | Enterprise only |
| ==Log Shipper (Datadog, Elasticsearch)== | ❌ | Enterprise only |
| ==Métricas Prometheus (básicas)== | ✅ | Exposto pelo webserver |


---

## 9. UI & Experiência do Usuário

| Feature | Status | Detalhes |    |
|----|----|----|----|
| ==UI Web (flows, execuções, logs)== | ✅ |    |    |
| ==Multi-Panel Editor== | ✅ |    |    |
| ==No-Code Forms== | ✅ |    |    |
| ==Full-text search nas execuções== | ❌ | Enterprise only (requer Elasticsearch) |    |
| ==Apps (interfaces customizáveis)== | ❌ | Enterprise only |    |
| ==Unit Tests para flows== | ❌ | Enterprise only |    |
| ==Revision History== | ✅ | Automático no OSS. Enterprise estende para todos os recursosLiberado |    |


---

## 10. Plugins & Integrações

| Feature | Status | Detalhes |
|----|----|----|
| ==900+ plugins disponíveis== | ✅ | Registrados no webserver |
| ==Plugins custom via Docker== | ✅ |    |
| ==Key-Value Store== | ✅ | Adicionado no OSS desde 0.18 |
| ==Namespaces== | ✅ | Usado: `production` |
| ==Integração nativa com git== | ❌ | Enterprise only |


---

## Resumo: O que NÃO temos e pode ser problema no futuro

| Risco | Impacto | Alternativa atual |
|----|----|----|
| ==Sem Secrets Manager externo== | Secrets são env vars manuais via K8s Secret | Double base64 + `extraEnv` no Helm |
| ==Sem Kubernetes Runner== | Scripts só rodam via Docker (DinD) | DinD habilitado no worker |
| ==Sem RBAC== | Todos os usuários têm mesmo acesso | Usar um único usuário compartilhado |
| ==Sem Audit Logs== | Não há rastreamento de quem mudou o quê | Controle via Git se os flows forem versionados |


---

*Fontes: [Kestra OSS vs Enterprise](https://kestra.io/docs/oss-vs-paid) · [Task Runner Types](https://kestra.io/docs/task-runners/types) · [Enterprise Features](https://kestra.io/docs/enterprise/overview/enterprise-edition) · [Pricing](https://kestra.io/pricing)*