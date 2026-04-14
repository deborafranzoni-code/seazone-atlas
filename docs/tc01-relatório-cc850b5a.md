<!-- title: TC01 -Relatório | url: https://outline.seazone.com.br/doc/tc01-relatorio-3b4Nvs91jG | area: Tecnologia -->

# TC01 -Relatório

**Data:** 2026-02-23 **Ambiente:** `dev-n8n` — cluster GKE `cluster-tools-prod-gke` 


---


## ==(SE APLICA APENAS A N8N-DEV)==

## Objetivo

Validar o processo completo de Disaster Recovery do ambiente `n8n-dev`, cobrindo:

* Configuração de VolumeSnapshot nativo do K8s para o Postgres
* Simulação de desastre com deleção do PVC
* Restauração completa a partir do snapshot
* Registro de tempos, comportamentos e pontos de atenção


---

## Componentes Avaliados

| Componente | Tipo | Tamanho | Storage Class | Estado crítico |
|----|----|----|----|----|
| `data-n8n-postgres-0` | PVC / StatefulSet | 20Gi | `standard-rwo` | Sim |
| `n8n-redis` | PVC / Deployment | 5Gi | `standard-rwo` | Não (cache) |


---

## Execução por Fase

### Fase 0 - Validação do Backup GCS

* Backup existente via CronJob exportando credentials e workflows em JSON para `gs://szn-n8n-dev-backup/`
* Backup manual forçado via `kubectl create job --from=cronjob/n8n-backup n8n-backup-manual` ✅
* Arquivos validados com conteúdo não-vazio

**Resultado:** Backup GCS validado como fallback disponível


---

### Fase 1 - Configuração do VolumeSnapshot

**Problema encontrado:** A `VolumeSnapshotClass` `csi-gce-pd-vsc` não havia sido criada, apenas os CRDs estavam presentes. O snapshot inicial entrou em erro imediato:

```
Failed to get snapshot class with error volumesnapshotclass.snapshot.storage.k8s.io "csi-gce-pd-vsc" not found
```

**Resolução:**


1. Criada a `VolumeSnapshotClass` com driver `pd.csi.storage.gke.io` e `deletionPolicy: Retain`
2. Snapshot com erro deletado e recriado

**Snapshot final:**

* Nome: `postgres-snapshot-dr-test`
* Namespace: `dev-n8n`
* Status: `readyToUse: true`
* Restore size: `20Gi`
* Criado em: `2026-02-23T16:51:34Z`

**Resultado:** ✅ Snapshot criado com sucesso após correção da SnapshotClass


---

### Fase 2 — Proteção do PV e Parada da Aplicação

**Reclaim policy alterada para** `**Retain**`**:**

* PV original: `pvc-be96d753-6adc-4580-914c-0c504131fa48`
* Alterado de `Delete` → `Retain` ✅

**Estado anotado antes do desastre:**

| Tipo | Count |
|----|----|
| workflows | 11 |
| credentials | 48 |

**Scale down:**

* Deployments parados: `n8n-editor`, `n8n-workers`, `n8n-webhooks`, `n8n-mcp`
* StatefulSet parado: `n8n-postgres`
* Apenas `n8n-redis` permaneceu em execução (sem estado crítico)

**Health check durante downtime:**

* Endpoint `https://dev-automation.seazone.com.br/healthz` retornou erro de conexão (esperado)
* HPA emitiu `FailedGetResourceMetric` por ausência de pods (esperado)

**Resultado:** ✅ Aplicação parada de forma controlada, PV protegido


---

### Fase 3 — Simulação do Desastre

**Hora do delete:** `2026-02-23 ~16:57`

**Ação:** `kubectl delete pvc data-n8n-postgres-0 -n dev-n8n`

**Estado do cluster após delete:**

| Recurso | Estado |
|----|----|
| PVC `data-n8n-postgres-0` | Deletado |
| PV `pvc-be96d753` | `Released` — disco GCE preservado ✅ |
| Pods da aplicação | Todos parados |
| `n8n-redis` | `Running` (inalterado) |

**Resultado:** ✅ PV sobreviveu ao delete do PVC — reclaim policy `Retain` funcionou conforme esperado


---

### Fase 4 — Restauração a partir do VolumeSnapshot

**Hora de início da restauração:** `2026-02-23 ~17:18`

**PVC recriado a partir do snapshot:**

```yaml
dataSource:
  name: postgres-snapshot-dr-test
  kind: VolumeSnapshot
  apiGroup: snapshot.storage.k8s.io
```

**Comportamento observado:**

* PVC ficou em `Pending` até o pod do Postgres ser schedulado
* Causa: `standard-rwo` usa `WaitForFirstConsumer` — o volume só é provisionado quando há um pod consumidor
* O `kubectl wait --for=jsonpath='{.status.phase}'=Bound` travou por esse motivo
* Solução: subir o StatefulSet diretamente com `kubectl scale statefulset n8n-postgres --replicas=1`

**Novo PV provisionado:** `pvc-9dcd395d-0547-49b5-81fa-e2baeadca46d` (20Gi, `Bound`) ✅

**Resultado:** ✅ PVC restaurado a partir do snapshot com sucesso


---

### Fase 5 — Reativação e Validação

**Postgres:**

* `n8n-postgres-0` — `Running` ✅

**Dados validados pós-restauração:**

| Tipo | Count (antes) | Count (após) |
|----|----|----|
| workflows | 11 | 11 ✅ |
| credentials | 48 | 48 ✅ |

**Demais componentes:**

| Pod | Status |
|----|----|
| `n8n-editor` | Running 2/2 ✅ |
| `n8n-mcp` | Running 1/1 ✅ |
| `n8n-webhooks` (x3) | Running 1/1 ✅ |
| `n8n-workers` (x2) | Running 2/2 ✅ |
| `n8n-postgres-0` | Running 1/1 ✅ |
| `n8n-redis` | Running 1/1 ✅ |

**Observação — workers em Pending:** O pod `n8n-workers-65b49c89cc-d95l8` ficou em `Pending` temporariamente por insuficiência de CPU nos nós disponíveis. O cluster autoscaler foi acionado e provisionou um novo nó (`14→15` instâncias no node pool `tools-prod-pool`). **Não relacionado ao DR.**

**Health check final:**

```
HTTP Status: 200
```

✅ Aplicação respondendo normalmente


---

### Fase 6 — Limpeza

| Ação | Status |
|----|----|
| Snapshot `postgres-snapshot-dr-test` deletado | ✅ |
| PV antigo `pvc-be96d753` deletado | ✅ |
| PV atual com reclaim policy `Delete` (padrão) | ✅ (já estava correto) |


---

## Resumo de Tempos

| Fase | Atividade | Tempo real |
|----|----|----|
| 0 | Validar backup GCS | \~5 min |
| 1 | Configurar SnapshotClass + tirar snapshot | \~10 min (inclui troubleshooting) |
| 2 | Proteger PV + parar aplicação | \~5 min |
| 3 | Deletar PVC + observar | \~1 min |
| 4 | Restaurar PVC do snapshot | \~6 min |
| 5 | Subir app + validar dados | \~10 min (inclui autoscaler) |
| 6 | Limpeza | \~2 min |
| **Total** |    | **\~39 min** |

> Estimativa original do plano era \~26 min. Diferença de \~13 min devido ao troubleshooting da SnapshotClass ausente e ao autoscaler do cluster.


---

## Pontos de Atenção Identificados

### ⚠️ VolumeSnapshotClass não existia no cluster

A `VolumeSnapshotClass` precisa ser criada previamente como pré-requisito. Os CRDs estavam instalados mas a classe não. **Ação recomendada:** incluir a criação da SnapshotClass no processo de bootstrap do cluster ou via IaC (Terraform/Helm).

### ⚠️ WaitForFirstConsumer no standard-rwo

O `kubectl wait` para `Bound` no PVC não funciona como gate nesse storage class. O correto é subir o StatefulSet e aguardar o pod ficar `Ready`. Atualizar o runbook com essa observação.

### ℹ️ Reclaim policy Delete no PV original

O PV do Postgres estava com `Delete` por padrão. Se a Fase 2.1 fosse pulada, o disco GCE seria destruído junto com o PVC — sem recuperação possível. A alteração para `Retain` antes de qualquer ação destrutiva é etapa obrigatória.

### ℹ️ Redis não restaurado

Comportamento esperado — Redis é cache apenas. Os pods subiram limpos sem impacto funcional.

### ℹ️ Backup GCS como fallback

O backup via CronJob (credentials + workflows em JSON) é válido como fallback mas **não inclui execution history**. Para restauração completa do estado, o VolumeSnapshot é obrigatório.


---

## Conclusão

O teste de DR foi concluído com sucesso. O ambiente `n8n-dev` foi completamente destruído (PVC deletado) e restaurado a partir de um VolumeSnapshot com **100% dos dados íntegros** (11 workflows, 48 credentials). A aplicação voltou a responder com HTTP 200 e todos os pods em estado `Running`.

O mecanismo de VolumeSnapshot via `csi-gce-pd-vsc` está validado e operacional para o cluster GKE `cluster-tools-prod-gke`.

**RTO observado (downtime até restauração completa): \~22 min** **RPO: zero (snapshot tirado imediatamente antes do desastre simulado)**


---

##