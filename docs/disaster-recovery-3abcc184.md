<!-- title: Disaster Recovery | url: https://outline.seazone.com.br/doc/disaster-recovery-DykeHeekJT | area: Tecnologia -->

# Disaster Recovery

**Data:** 2026-03-10 **Namespace:** `clickhouse` **Cluster:** EKS sa-east-1


---

## 1. Arquitetura de Volumes

| Componente | Réplicas | Storage | StorageClass (YAML) | StorageClass (Real) | ReclaimPolicy |
|----|----|----|----|----|----|
| ClickHouse Data | 3 | 50Gi cada | `szn-ebs-gp3-retained` | `szn-ebs-gp3-retained` | **Retain** |
| ClickHouse Keeper | 3 | 10Gi cada | `szn-ebs-gp3-retained` | `gp3` | ~~Delete~~ → **Retain** (corrigido) |

### PVs — ClickHouse Data

| PV | PVC | Capacidade |
|----|----|----|
| `pvc-c5ca4a5a-da2f-410b-b295-438a0cf99150` | `data-volume-chi-clickhouse-cluster-production-0-0-0` | 50Gi |
| `pvc-b295f172-f55b-46f2-838d-b682cdcf0c88` | `data-volume-chi-clickhouse-cluster-production-0-1-0` | 50Gi |
| `pvc-53e7b7e6-e79c-41d0-9be5-ab43bd3c0f9a` | `data-volume-chi-clickhouse-cluster-production-0-2-0` | 50Gi |

### PVs — ClickHouse Keeper

| PV | PVC | Capacidade |
|----|----|----|
| `pvc-3ded20ca-3536-4477-96bd-90071610ad99` | `data-clickhouse-keeper-0` | 10Gi |
| `pvc-113b4218-95be-441e-9045-2a63869d12b8` | `data-clickhouse-keeper-1` | 10Gi |
| `pvc-2f6dac76-1de7-4b58-9174-5bd666ef6cad` | `data-clickhouse-keeper-2` | 10Gi |

### Mapa PV → EBS Volume ID

| Componente | PV | EBS Volume ID |
|----|----|----|
| CH Data réplica 0 | `pvc-c5ca4a5a-...` | `vol-090ca80d6864bb533` |
| CH Data réplica 1 | `pvc-b295f172-...` | `vol-027c7681063014b64` |
| CH Data réplica 2 | `pvc-53e7b7e6-...` | `vol-05f158c3e7da2fd30` |
| Keeper 0 | `pvc-3ded20ca-...` | `vol-00c932cece3603b41` |
| Keeper 1 | `pvc-113b4218-...` | `vol-0cd8d1b0cc7af206b` |
| Keeper 2 | `pvc-2f6dac76-...` | `vol-04c45d82d83eb5528` |


---

## 2. Problema Identificado

Os PVCs do **ClickHouse Keeper** foram provisionados com a StorageClass `gp3`, que possui ReclaimPolicy **Delete**. Isso significa que, caso os PVCs fossem deletados (por exemplo, durante uma recriação do StatefulSet), os PersistentVolumes e os discos EBS associados seriam **destruídos permanentemente**.

O manifesto `clickhouse-keeper.yaml` já especifica `storageClassName: szn-ebs-gp3-retained`, mas como os PVCs foram criados antes dessa configuração ser adicionada ao YAML, os volumes existentes permaneceram com a classe `gp3`.

> **Nota:** A StorageClass de um PVC não pode ser alterada após a criação. A correção definitiva exigiria recriar os PVCs, o que envolve downtime do Keeper.


---

## 3. Correção Aplicada

**Ação:** Alterada a ReclaimPolicy dos 3 PVs do Keeper de `Delete` para `Retain` via patch direto.

```bash

kubectl patch pv pvc-3ded20ca-3536-4477-96bd-90071610ad99 -p '{"spec":{"persistentVolumeReclaimPolicy":"Retain"}}'
kubectl patch pv pvc-113b4218-95be-441e-9045-2a63869d12b8 -p '{"spec":{"persistentVolumeReclaimPolicy":"Retain"}}'
kubectl patch pv pvc-2f6dac76-1de7-4b58-9174-5bd666ef6cad -p '{"spec":{"persistentVolumeReclaimPolicy":"Retain"}}'
```

**Resultado:** Todos os 6 PVs do cluster ClickHouse agora possuem ReclaimPolicy **Retain**.

**Impacto:** Zero downtime. A alteração afeta apenas o comportamento em caso de deleção do PVC — o PV (e o disco EBS) será preservado em vez de deletado.


---

## 4. Estado Pós-Correção

```
NAME                                       CAPACITY   RECLAIM   STATUS   CLAIM                                               STORAGECLASS

pvc-3ded20ca-...   10Gi   Retain   Bound   data-clickhouse-keeper-0                            gp3

pvc-113b4218-...   10Gi   Retain   Bound   data-clickhouse-keeper-1                            gp3

pvc-2f6dac76-...   10Gi   Retain   Bound   data-clickhouse-keeper-2                            gp3

pvc-c5ca4a5a-...   50Gi   Retain   Bound   data-volume-chi-clickhouse-cluster-production-0-0-0 szn-ebs-gp3-retained

pvc-b295f172-...   50Gi   Retain   Bound   data-volume-chi-clickhouse-cluster-production-0-1-0 szn-ebs-gp3-retained

pvc-53e7b7e6-...   50Gi   Retain   Bound   data-volume-chi-clickhouse-cluster-production-0-2-0 szn-ebs-gp3-retained
```


---

## 5. Observações Adicionais

### ClickHouse Operator — Política de Cleanup

A configuração do operator (`clickhouse-operator-files` ConfigMap) contém:

```yaml

reconcile:
  host:
    drop:
      replicas:
        active: false
        onDelete: true      # operator PODE deletar PVCs ao remover o CHI
        onLostVolume: true
```

**Implicação:** Ao deletar o recurso `ClickHouseInstallation`, o operator pode deletar os PVCs dos dados do ClickHouse como parte do cleanup. Porém, com ReclaimPolicy **Retain**, os PVs e discos EBS sobrevivem independentemente.

### Outros PVs no namespace (não fazem parte do cluster principal)

| PV | PVC | StorageClass | ReclaimPolicy |
|----|----|----|----|
| `pvc-7914c76b-...` | `clickhouse-data-op-ch-0` (5Gi) | `gp3` | **Delete** |
| `pvc-bc9d0174-...` | `clickhouse-logs-op-ch-0` (5Gi) | `gp3` | **Delete** |
| `pvc-ea8c4ad3-...` | `clickhouse-data-clickhouse-0` (100Gi) | `gp3` | **Delete** |

Esses volumes parecem pertencer a instalações anteriores ou ao operator. Recomenda-se investigar se ainda estão em uso e, caso positivo, aplicar a mesma correção de ReclaimPolicy.

### Sync Policy do ArgoCD

A Application do ClickHouse possui `prune: true` e `selfHeal: true`. Isso significa que se um manifesto for removido do Git acidentalmente, o ArgoCD irá deletar o recurso correspondente no cluster. Com a ReclaimPolicy `Retain`, os discos EBS sobreviveriam, mas o serviço ficaria indisponível até a restauração.

### Application não está em App-of-Apps

A Application `clickhouse-operator` **não é gerenciada** por nenhum app-of-apps (`cluster-services.yaml`, `monitoring.yaml`, `tools.yaml`). Isso significa que, se a Application for deletada, ela **não será recriada automaticamente** pelo ArgoCD. A reaplicação deve ser feita manualmente.


---

## 6. Procedimento de Disaster Recovery

### Cenário: PVCs deletados (por remoção do CHI, erro humano, etc.)

Quando um PVC é deletado e o PV tem ReclaimPolicy `Retain`:

* O PV muda de status `Bound` → `Released`
* O disco EBS **continua existindo** na AWS
* O PV mantém o `claimRef` do PVC antigo (impede novo bind automático)

### Passo 1 — Localizar os PVs órfãos

```bash
# Listar PVs Released do ClickHouse

kubectl get pv | grep Released

# Verificar disco EBS associado a um PV específico

kubectl get pv <pv-name> -o jsonpath='{.spec.csi.volumeHandle}'

# Verificar na AWS diretamente

aws ec2 describe-volumes --volume-ids vol-090ca80d6864bb533 --query 'Volumes[].{ID:VolumeId,State:State,Size:Size,AZ:AvailabilityZone}'
```

### Passo 2 — Limpar o claimRef dos PVs

O PV Released ainda guarda referência ao PVC antigo. É necessário limpar para permitir novo bind:

```bash
# ClickHouse Data

kubectl patch pv pvc-c5ca4a5a-da2f-410b-b295-438a0cf99150 -p '{"spec":{"claimRef":null}}'
kubectl patch pv pvc-b295f172-f55b-46f2-838d-b682cdcf0c88 -p '{"spec":{"claimRef":null}}'
kubectl patch pv pvc-53e7b7e6-e79c-41d0-9be5-ab43bd3c0f9a -p '{"spec":{"claimRef":null}}'

# ClickHouse Keeper

kubectl patch pv pvc-3ded20ca-3536-4477-96bd-90071610ad99 -p '{"spec":{"claimRef":null}}'
kubectl patch pv pvc-113b4218-95be-441e-9045-2a63869d12b8 -p '{"spec":{"claimRef":null}}'
kubectl patch pv pvc-2f6dac76-1de7-4b58-9174-5bd666ef6cad -p '{"spec":{"claimRef":null}}'
```

### Passo 3 — Recriar PVCs apontando para os PVs existentes

Criar PVCs com o **mesmo nome** que os StatefulSets esperam, referenciando o PV específico:

**ClickHouse Data (repetir para cada réplica, ajustando nome e PV):**

```yaml

apiVersion: v1

kind: PersistentVolumeClaim

metadata:
  name: data-volume-chi-clickhouse-cluster-production-0-0-0
  namespace: clickhouse

spec:
  accessModes: ["ReadWriteOnce"]
  storageClassName: ""   # vazio para evitar provisioning dinâmico
  volumeName: pvc-c5ca4a5a-da2f-410b-b295-438a0cf99150
  resources:
    requests:
      storage: 50Gi
```

**ClickHouse Keeper (repetir para cada réplica):**

```yaml

apiVersion: v1

kind: PersistentVolumeClaim

metadata:
  name: data-clickhouse-keeper-0
  namespace: clickhouse

spec:
  accessModes: ["ReadWriteOnce"]
  storageClassName: ""
  volumeName: pvc-3ded20ca-3536-4477-96bd-90071610ad99
  resources:
    requests:
      storage: 10Gi
```

**Mapeamento completo para referência:**

| PVC Name | PV Name | Storage |
|----|----|----|
| `data-volume-chi-clickhouse-cluster-production-0-0-0` | `pvc-c5ca4a5a-da2f-410b-b295-438a0cf99150` | 50Gi |
| `data-volume-chi-clickhouse-cluster-production-0-1-0` | `pvc-b295f172-f55b-46f2-838d-b682cdcf0c88` | 50Gi |
| `data-volume-chi-clickhouse-cluster-production-0-2-0` | `pvc-53e7b7e6-e79c-41d0-9be5-ab43bd3c0f9a` | 50Gi |
| `data-clickhouse-keeper-0` | `pvc-3ded20ca-3536-4477-96bd-90071610ad99` | 10Gi |
| `data-clickhouse-keeper-1` | `pvc-113b4218-95be-441e-9045-2a63869d12b8` | 10Gi |
| `data-clickhouse-keeper-2` | `pvc-2f6dac76-1de7-4b58-9174-5bd666ef6cad` | 10Gi |

### Passo 4 — Reaplicar a Application do ArgoCD

```bash

kubectl apply -f argocd/applications/databases/clickhouse/application.yaml
```

O ArgoCD irá recriar todos os recursos (operator, CHI, Keeper StatefulSet, etc.). Os StatefulSets encontrarão os PVCs já existentes com os nomes corretos e montarão os mesmos discos EBS.

### Passo 5 — Validar integridade

```bash
# Verificar que os pods estão Running

kubectl get pods -n clickhouse

# Verificar que PVCs estão Bound

kubectl get pvc -n clickhouse

# Verificar dados no ClickHouse

kubectl exec -n clickhouse chi-clickhouse-cluster-production-0-0-0 -- \
  clickhouse-client --query "SELECT count() FROM system.tables"
```


---

## 7. Teste de Persistência — Executado em 2026-03-10

### Resultado: PASSOU

### Etapas executadas

**1. Inserção de dados de teste**

```sql

CREATE TABLE default.persistence_test ON CLUSTER 'production' (
    id UInt32, message String, created_at DateTime DEFAULT now()
) ENGINE = ReplicatedMergeTree('/clickhouse/tables/{shard}/persistence_test', '{replica}')
ORDER BY id;

INSERT INTO default.persistence_test (id, message) VALUES
(1, 'teste-persistencia-2026-03-10'),
(2, 'dados-devem-sobreviver-delete'),
(3, 'disaster-recovery-validation');
```

Dados confirmados replicados nas 3 réplicas antes da destruição.

**2. Destruição — Deleção da Application ArgoCD**

```bash

kubectl delete application clickhouse-operator -n argocd
```

* A Application possuía finalizer `resources-finalizer.argocd.argoproj.io`
* O finalizer ficou travado porque o `ClickHouseInstallation` entrou em `Terminating` (operator já havia sido removido e não conseguia processar o finalizer do CHI)
* Foi necessário remover manualmente os finalizers:

```bash
# Remover finalizer da Application (destravar deleção do ArgoCD)
kubectl patch application clickhouse-operator -n argocd --type json \
  -p '[{"op": "remove", "path": "/metadata/finalizers"}]'

# Remover finalizer do CHI (destravar Terminating)
kubectl patch chi clickhouse-cluster -n clickhouse --type json \
  -p '[{"op": "remove", "path": "/metadata/finalizers"}]'
```

**3. Estado pós-destruição**

| Recurso | Status |
|----|----|
| Application | Deletada |
| ClickHouseInstallation | Deletada |
| Pods (6) | Todos removidos |
| StatefulSets (4) | Todos removidos |
| Services | Todos removidos |
| Deployment (operator) | Removido |
| **PVCs (6)** | **Sobreviveram — Bound** |
| **PVs (6)** | **Sobreviveram — Retain + Bound** |

> **Descoberta importante:** Os PVCs NÃO são gerenciados diretamente pelo ArgoCD (não aparecem em `.status.resources`). O ArgoCD mostra PVCs na UI como filhos dos StatefulSets, mas não os inclui no prune. O ClickHouse Operator também não deletou os PVCs ao remover o CHI (apesar da config `onDelete: true`), provavelmente porque o operator foi removido antes do CHI ser processado.

**4. Restauração**

```bash

kubectl apply -f argocd/applications/databases/clickhouse/application.yaml
```

* ArgoCD recriou todos os recursos automaticamente (sync policy `automated`)
* Os StatefulSets encontraram os PVCs existentes e montaram os mesmos discos EBS
* Todos os 7 pods voltaram a `Running` em \~10 minutos

**5. Validação dos dados**

```
=== Réplica 0 ===
   ┌─id─┬─message───────────────────────┬──────────created_at─┐
1. │  1 │ teste-persistencia-2026-03-10 │ 2026-03-10 21:20:03 │
2. │  2 │ dados-devem-sobreviver-delete │ 2026-03-10 21:20:03 │
3. │  3 │ disaster-recovery-validation  │ 2026-03-10 21:20:03 │
   └────┴───────────────────────────────┴─────────────────────┘
=== Réplica 1 === (idêntico)
=== Réplica 2 === (idêntico)
```

**3 registros intactos nas 3 réplicas após destruição total e restauração.**

### Lições aprendidas


1. **PVCs sobrevivem à deleção da Application** — não são recursos gerenciados pelo ArgoCD
2. **Finalizers podem travar** — se o operator é removido antes do CHI, o finalizer `finalizer.clickhouseinstallation.altinity.com` não é processado e o recurso fica em `Terminating`
3. **Recovery sem procedimento manual** — como os PVCs se mantiveram, bastou reaplicar a Application e o ArgoCD restaurou tudo automaticamente
4. **ReclaimPolicy Retain é a última linha de defesa** — mesmo se PVCs forem deletados, os PVs e discos EBS sobrevivem