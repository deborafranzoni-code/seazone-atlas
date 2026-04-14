<!-- title: TC02 - Relatório Restauração via Backup GCS | url: https://outline.seazone.com.br/doc/tc02-relatorio-restauracao-via-backup-gcs-fto4w3eUhu | area: Tecnologia -->

# TC02 - Relatório Restauração via Backup GCS

**Data:** 2026-02-24 **Ambiente:** `dev-n8n` — cluster GKE `cluster-tools-prod-gke` 

Team **Status final:** ✅ Sucesso


---

## Objetivo

Validar que workflows e credentials podem ser restaurados via backup JSON armazenado no GCS (`gs://szn-n8n-dev-backup/`), sem depender de VolumeSnapshot. Este é o cenário de **fallback** quando não há snapshot disponível.


---

## Modalidade do Teste

Teste não-destrtutivo, import executado sobre banco com dados existentes para validar o processo de restauração sem necessidade de destruir o ambiente.


---

## Fase 0 - Validação dos Backups Disponíveis

 ![](/api/attachments.redirect?id=70fc9d5a-f5dc-44a8-9ad9-4e1588b8e15b " =1431x603")

**Backup do dia validado:**

 ![](/api/attachments.redirect?id=f3e7f800-6fd0-473a-a1c6-a8b76288d2a4 " =1900x85")

✅ Critério atendido: arquivos existem e têm conteúdo


---

## Fase 1 — Download e Cópia para o Pod mportação via n8n CLI

```bash
# Cópia para dentro do pod n8n-editor
kubectl cp /tmp/credentials-backup.json dev-n8n/n8n-editor-7698dc6f96-dmvms:/tmp/credentials-backup.json -c n8n-editor
kubectl cp /tmp/workflows-backup.json dev-n8n/n8n-editor-7698dc6f96-dmvms:/tmp/workflows-backup.json -c n8n-editor
### Credentials
kubectl exec -n dev-n8n n8n-editor-7698dc6f96-dmvms -c n8n-editor -- \
  n8n import:credentials --input=/tmp/credentials-backup.json
```

 ![](/api/attachments.redirect?id=737fc752-7ce8-4d27-8d96-f6e0479816b8 " =1359x403")

✅ Arquivos

 copiados sem erro

### Workflows

```bash
kubectl exec -n dev-n8n n8n-editor-7698dc6f96-dmvms -c n8n-editor -- \
  n8n import:workflow --input=/tmp/workflows-backup.json
```

**Output:**

 ![](/api/attachments.redirect?id=a1dbe034-8a2f-4a22-b694-00abb502044a " =1317x112")

Workflows recuperados com sucesso

## Fase 3 — Validação no Banco

```bash
kubectl exec -n dev-n8n n8n-postgres-0 -- psql -U postgres -d db_n8n_dev \
  -c "SELECT 'workflows' as tipo, COUNT(*) FROM workflow_entity UNION ALL SELECT 'credentials', COUNT(*) FROM credentials_entity;"
```

**Resultado:**

 ![](/api/attachments.redirect?id=029118cd-ea15-4c7a-8d9d-ed6d8ae2ec26 " =1756x221")

| Tipo | Count |
|----|----|
| workflows | 13 |
| credentials | 48 |

✅ Dados confirmados no banco


---

## Observações

### Workflows desativados após import

O n8n desativa workflows automaticamente durante o import. Em uma restauração real, os workflows precisam ser **reativados manualmente** na UI ou via CLI após a importação.

### Execution history não recuperado

O backup GCS exporta apenas workflows e credentials. Histórico de execuções não é incluído e não pode ser recuperado por este método.


---

## Resumo

| Métrica | Valor |
|----|----|
| Tempo total do teste | \~15 min |
| Credentials restauradas | 48 / 48 ✅ |
| Workflows restaurados | 13 / 13 ✅ |