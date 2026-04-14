<!-- title: 03-Deploy GitOps | url: https://outline.seazone.com.br/doc/03-deploy-gitops-qkWsFJsbhO | area: Tecnologia -->

# 03-Deploy GitOps

## Visão geral do fluxo

 ![](/api/attachments.redirect?id=ba4c94f9-20f0-412e-8cb9-c17b036b8e86 " =1408x768")

## ArgoCD Multi-Source

Cada ambiente é uma ArgoCD `Application` com múltiplas fontes. O campo `$values` é uma referência ao próprio repositório `gitops-governanca` que age como source de values files:

```yaml
sources:
  # Fonte 1: Helm chart do n8n
  - repoURL: 'https://github.com/seazone-tech/helm-charts.git'
    targetRevision: HEAD
    path: n8n
    helm:
      releaseName: n8n
      valueFiles:
        - $values/argocd/applications/n8n/prd/values-n8n.yaml

  # Fonte 2: ref de values (este repo como $values)
  - repoURL: 'https://github.com/seazone-tech/gitops-governanca.git'
    targetRevision: HEAD
    ref: values

  # Fonte 3: manifests raw deste repo
  - repoURL: 'https://github.com/seazone-tech/gitops-governanca.git'
    targetRevision: HEAD
    path: argocd/applications/n8n/prd
    directory:
      include: '{external-secret.yaml,ingressroute.yaml,...}'
```


:::tip
O mesmo padrão se aplica para Redis e PostgreSQL (apenas em dev), cada um com seu próprio `releaseName`.

:::

## Sync Policy

| Configuração | Valor | Implicação |
|----|----|----|
| `automated.prune` | `false` | Recursos removidos do repo **não** são deletados automaticamente |
| `automated.selfHeal` | `false` | Drift entre cluster e repo **não** é auto-corrigido |
| `revisionHistoryLimit` | `2` | Mantém apenas os 2 últimos históricos de revisão |


:::info
**Por que prune e selfHeal estão desabilitados?** Proteção contra deleção acidental em produção. Toda remoção de recurso requer intent explícito.

:::

### Comandos ArgoCD

```bash
# Verificar status das applications

argocd app list

# Ver diff entre repo e cluster

argocd app diff dev-n8n

argocd app diff prd-n8n

# Sync sem prune (default)
argocd app sync dev-n8n

argocd app sync prd-n8n

# Sync com prune (para remover recursos deletados do repo)
argocd app sync prd-n8n --prune

# Forçar sync mesmo sem mudança de hash

argocd app sync dev-n8n --force

# Ver histórico de syncs

argocd app history dev-n8n
```


:::tip
**Regra**: nunca usar `--prune` em prd sem revisar o diff antes.

:::

## Gestão de Segredos

### Fluxo completo

 ![](/api/attachments.redirect?id=aa6fa801-29f0-4118-846c-e6dd516df7d8 " =1408x768")

### Adicionar um novo segredo


1. Criar o parâmetro no AWS SSM:

   ```
   /sre/n8n/dev/NOME_DA_VAR  ← para dev
   /sre/n8n/prd/NOME_DA_VAR  ← para prd
   ```
2. Adicionar a variável no `config:` de `values-n8n.yaml` com `value: ""`:

   ```yaml
   config:
     - name: NOME_DA_VAR
       value: ""   # valor vem do existingSecret
   ```
3. Aguardar o refresh do ExternalSecret (até 1 min) ou forçar:

   ```bash
   kubectl annotate externalsecret n8n-external-secrets \
     force-sync=$(date +%s) -n {env}-n8n --overwrite
   ```
4. Reiniciar os pods para carregar a nova variável:

   ```bash
   kubectl rollout restart deployment/n8n-editor deployment/n8n-workers \
     deployment/n8n-webhooks deployment/n8n-mcp -n {env}-n8n
   ```

### Verificar se o Secret está atualizado

```bash
# Ver todas as chaves do secret (sem valores)
kubectl get secret n8n-secrets -n prd-n8n -o json | jq '.data | keys'

# Ver status do ExternalSecret

kubectl get externalsecret n8n-external-secrets -n prd-n8n

kubectl describe externalsecret n8n-external-secrets -n prd-n8n
```

## Adicionar um novo componente ao deploy

Para incluir um novo manifest que seja aplicado pelo ArgoCD, adicionar o nome do arquivo no campo `directory.include` em `application.yaml`:

```yaml

directory:
  include: '{external-secret.yaml,ingressroute.yaml,cronjob-backup-n8n.yaml,podmonitoring.yaml,novo-recurso.yaml}'
```

## Rollback via ArgoCD

```bash
# Ver histórico

argocd app history prd-n8n

# Rollback para revisão anterior

argocd app rollback prd-n8n <revision-id>
```


:::tip
Alternativa rápida para rollback de imagem: atualizar `image.tag` no `values-n8n.yaml` para a versão anterior e commitar.

:::

## Rollback via kubectl (emergência)

Se o ArgoCD não estiver disponível ou o sync estiver travado:

```bash
# Rollback de deployment específico

kubectl rollout undo deployment/n8n-editor -n prd-n8n

kubectl rollout undo deployment/n8n-workers -n prd-n8n

kubectl rollout undo deployment/n8n-webhooks -n prd-n8n

# Verificar status

kubectl rollout status deployment/n8n-editor -n prd-n8n
```


:::tip
Após rollback via kubectl, o ArgoCD vai mostrar drift. Fazer sync para reconciliar.

:::