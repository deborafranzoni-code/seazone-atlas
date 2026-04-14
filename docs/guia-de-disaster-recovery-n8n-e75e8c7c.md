<!-- title: Guia de Disaster Recovery  n8n | url: https://outline.seazone.com.br/doc/guia-de-disaster-recovery-n8n-0z3a5uySGi | area: Tecnologia -->

# Guia de Disaster Recovery  n8n

**Cluster:** `cluster-tools-prod-gke` | **Namespace:** `dev-n8n`


---

## Cenário 1 — Perda do PVC do Postgres

**Sintoma:** `data-n8n-postgres-0` não existe ou está em erro. Postgres não sobe.

```mermaidjs
flowchart TD
    A[PVC perdido] --> B{VolumeSnapshot\ndisponível?}
    B -- Sim --> C[Recriar PVC\na partir do snapshot]
    B -- Não --> D{PV com\nretain policy?}
    D -- Sim --> E[Recriar PVC\napontando para PV existente]
    D -- Não --> F[Restore via\nBackup GCS — Cenário 2]
    C --> G[Scale up Postgres]
    E --> G
    F --> G
    G --> H[Scale up demais deployments]
```

```nu
# 1. Confirmar que o PV sobreviveu (deve estar Released)
kubectl get pv | grep dev-n8n

# 2. Recriar PVC a partir do snapshot mais recente
kubectl apply -f - <<EOF
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: data-n8n-postgres-0
  namespace: dev-n8n
spec:
  accessModes: [ReadWriteOnce]
  resources:
    requests:
      storage: 20Gi
  storageClassName: standard-rwo
  dataSource:
    name: <nome-do-snapshot>
    kind: VolumeSnapshot
    apiGroup: snapshot.storage.k8s.io
EOF

# 3. Subir o Postgres (PVC faz Bound ao ser consumido)
kubectl scale statefulset n8n-postgres -n dev-n8n --replicas=1
kubectl wait pod/n8n-postgres-0 -n dev-n8n --for=condition=Ready --timeout=120s

# 4. Subir o restante
kubectl scale deployment n8n-editor n8n-workers n8n-webhooks n8n-mcp -n dev-n8n --replicas=1
```

**Sem snapshot disponível?** Ver Cenário 2.

⚠️ Antes de qualquer delete, sempre verificar se o PV tem reclaim policy `Retain`:

```nu
kubectl get pv | grep dev-n8n
```


---

## Cenário 2 — Restore via Backup GCS (sem snapshot)

**Usar quando:** não há VolumeSnapshot disponível. RPO de até 24h.

```nu
# 1. Subir Postgres zerado
kubectl scale statefulset n8n-postgres -n dev-n8n --replicas=1

# 2. Baixar backup mais recente
gcloud storage cp $"gs://szn-n8n-dev-backup/credentials/credentials-backup-(date now | format date '%Y-%m-%d').json" /tmp/credentials-backup.json
gcloud storage cp $"gs://szn-n8n-dev-backup/workflows/workflows-backup-(date now | format date '%Y-%m-%d').json" /tmp/workflows-backup.json

# 3. Copiar para o pod e importar
kubectl cp /tmp/credentials-backup.json dev-n8n/$(kubectl get pod -n dev-n8n -l app.kubernetes.io/component=editor -o jsonpath='{.items[0].metadata.name}'):/tmp/ -c n8n-editor
kubectl cp /tmp/workflows-backup.json dev-n8n/$(kubectl get pod -n dev-n8n -l app.kubernetes.io/component=editor -o jsonpath='{.items[0].metadata.name}'):/tmp/ -c n8n-editor

kubectl exec -n dev-n8n deploy/n8n-editor -c n8n-editor -- n8n import:credentials --input=/tmp/credentials-backup.json
kubectl exec -n dev-n8n deploy/n8n-editor -c n8n-editor -- n8n import:workflow --input=/tmp/workflows-backup.json
```

⚠️ Workflows são importados **desativados** - reativar manualmente na UI após restore.

⚠️ Execution history **não é recuperado** por este método.


---

## Cenário 3 — Deploy com Imagem Inválida

**Sintoma:** pod em `ImagePullBackOff` ou `ErrImagePull` após deploy. Serviço continua funcionando (RollingUpdate).

```nu
# Rollback imediato
kubectl rollout undo deployment/<nome-do-deployment> -n dev-n8n
kubectl rollout status deployment/<nome-do-deployment> -n dev-n8n
```

**Deployments disponíveis:** `n8n-editor`, `n8n-workers`, `n8n-webhooks`, `n8n-mcp`


---

## Cenário 4 — Falha do Redis

**Sintoma:** `n8n-redis` em erro ou ausente. Workers com falha de conexão.

Nenhuma ação necessária , o Deployment recria o pod automaticamente em \~1 min. Aguardar e monitorar:

```nu
kubectl get pod -n dev-n8n -l app.kubernetes.io/name=redis -w
```

⚠️ Execuções em andamento no momento da falha podem ser perdidas ou reprocessadas.


---

## Cenário 5 — Secret Deletado ou Corrompido no K8s

**Sintoma:** pods com erro de variável de ambiente ou falha de autenticação.

```mermaidjs
flowchart LR
    SSM[AWS Parameter Store\n/sre/n8n/dev/]
    ESO[External Secrets\nOperator]
    SEC[n8n-secrets\nno K8s]
    PODS[Pods]

    SSM -- "sync a cada 1min" --> ESO
    ESO -- "cria/atualiza" --> SEC
    SEC -- "montado como env" --> PODS

    style SSM fill:#f90,color:#000
    style ESO fill:#4a90d9,color:#fff
    style SEC fill:#2ecc71,color:#fff
```

O External Secrets Operator recria o secret automaticamente em até **1 minuto** a partir do AWS Parameter Store (`/sre/n8n/dev/`). Aguardar e forçar restart se necessário:

```nu
kubectl rollout restart deployment/n8n-editor deployment/n8n-workers deployment/n8n-webhooks deployment/n8n-mcp -n dev-n8n
kubectl rollout restart statefulset/n8n-postgres -n dev-n8n
```

⚠️ Se o problema estiver na **fonte (AWS SSM)**, o operador propagará os valores errados. Verificar o Parameter Store antes de reiniciar.


---

## Checklist Pré-Ação Destrutiva

Antes de qualquer operação de risco no ambiente:

- [ ] PV com reclaim policy `Retain` — `kubectl get pv | grep dev-n8n`
- [ ] VolumeSnapshot recente criado — `kubectl get volumesnapshot -n dev-n8n`
- [ ] Backup GCS do dia validado — `gcloud storage ls gs://szn-n8n-dev-backup/`
- [ ] Aplicação com scale down — `kubectl scale deployment ... --replicas=0`


---

## Referências

| Recurso | Localização |
|----|----|
| Backup GCS | `gs://szn-n8n-dev-backup/` |
| Secrets | AWS Parameter Store `/sre/n8n/dev/` |
| VolumeSnapshotClass | `csi-gce-pd-vsc` |
| Relatórios de DR | @[Casos de Teste](mention://4c7c9bb5-1981-4c32-bb53-603a485e2942/document/e3d0b6cc-888b-4c82-8b30-97c4bc6dc305) |