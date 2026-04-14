<!-- title: Versionamento e Backup de Workflows no Kestra OSS | url: https://outline.seazone.com.br/doc/versionamento-e-backup-de-workflows-no-kestra-oss-hfENzjMwOS | area: Tecnologia -->

# Versionamento e Backup de Workflows no Kestra OSS

Ambiente atual: **Kestra OSS 1.2.2** no GKE, PostgreSQL (Cloud SQL), GCS storage.


---

## TL;DR

| Mecanismo | Disponível no OSS | O que faz |
|----|----|----|
| Revisions (built-in) | ✅ | Versionamento automático de flows, comparação e rollback |
| `io.kestra.plugin.git.SyncFlows` | ✅ | Sincroniza flows de um repo Git → Kestra (GitOps) |
| `io.kestra.plugin.git.PushFlows` | ✅ | Edita no UI e faz commit automático para Git |
| Revision History para todos os recursos | ❌ | Enterprise only |
| Integração nativa Git como source of truth (painel centralizado) | ❌ | Enterprise only |


---

## 1. Revisions — Versionamento Automático (Built-in)

 ![](/api/attachments.redirect?id=61f4e725-a2a0-4dfa-88e2-a2fdabefd19c " =1472x842")

O Kestra cria uma nova revisão automaticamente toda vez que um flow é salvo. Isso está ativo por padrão, sem configuração necessária.

### O que dá para fazer

* **Ver histórico completo** de todas as versões do flow na aba `Revisions`
* **Comparar versões** lado a lado (diff linha por linha) — você escolhe as duas versões no dropdown
* **Rollback instantâneo** — botão `Restore` para voltar para qualquer versão anterior

### Limitação no OSS

Revisions só funcionam para **flows**. No Enterprise, o histórico é estendido para todos os recursos (namespaces, namespace files, etc.).


---

## 2. Git Sync via SyncFlows — GitOps

Para ter o Git como source of truth e sincronizar automaticamente para o Kestra, é possível usar task `io.kestra.plugin.git.SyncFlows`. Ele está disponível no OSS.

### Como funciona

```
Repo Git (main) ──► SyncFlows (cron ou webhook) ──► Flows no Kestra (namespace)
```

* A cada execução, o task clona o repo e compara os flows do diretório configurado com os que existem no namespace
* Flows novos ou alterados são criados/atualizados
* Se `delete: true`, flows que não existem mais no Git são removidos do Kestra


---

## 3. PushFlows — Editar no UI e Versionar no Git

<https://kestra.io/docs/how-to-guides/pushflows>

 ![](/api/attachments.redirect?id=510eea83-68d0-4518-839f-d880aa24a09f " =980x616")

O padrão inverso: Edita o flow pela UI do Kestra, e ele faz commit automático no repo Git.

> **Nota:** PushFlows e SyncFlows não são para usar juntos no mesmo namespace.


---

## 4. Estratégia para o Ambiente Atual

| Camada | Mecanismo | Função |
|----|----|----|
| Versionamento diário | **Revisions** (built-in) | Histórico automático, rollback rápido no UI |
| Sincronização | **PushFlows**  | Puxa mudanças do Kestra para o Git automaticamente |


---

## Fontes

* [Flow Revisions — Kestra Docs](https://kestra.io/docs/concepts/revision)
* [SyncFlows Plugin](https://kestra.io/plugins/plugin-git/tasks/io.kestra.plugin.git.syncflows)
* [Version Control with Git](https://kestra.io/docs/version-control-cicd/git)
* [OSS vs Enterprise](https://kestra.io/docs/oss-vs-paid)