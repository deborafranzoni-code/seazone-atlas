<!-- title: GCP | url: https://outline.seazone.com.br/doc/gcp-IUSdoPzwYw | area: Tecnologia -->

# GCP

# Plano de Implantacao — Stack de Logs no GKE

**Epico:** SRE-4961 — Melhorias no monitoramento dos workloads **Deadline:** 13/03/2026 manha **Executores:** 2 analistas com Claude Code **Grafana:** Existente no EKS (`monitoring.seazone.com.br`) — nao sera redeployado


---

## 1. Arquitetura

```
                          EKS (sa-east-1)                          GKE (us-central1)
                    +----------------------+              +---------------------------+
                    |                      |              |                           |
                    |  Grafana ------------|- HTTPS ----->| Traefik (35.225.201.214)  |
                    |  (monitoring.        |  cross       |     |                     |
                    |   seazone.com.br)    |  cluster     |     v                     |
                    |                      |              |  Loki Gateway             |
                    +----------------------+              |     ^                     |
                                                         |     |                     |
                                                         |  Promtail (DaemonSet)     |
                                                         |  coleta logs de:          |
                                                         |  n8n, baserow, kestra...  |
                                                         +---------------------------+
```

### Estrategia de conectividade: Grafana (EKS) -> Loki (GKE)

O Loki no GKE sera exposto via **Traefik IngressRoute** (ja existe no GKE com IP `35.225.201.214`). O Grafana no EKS acessara via URL externa (ex: `https://loki-gke.seazone.com.br`).

**Opcoes de seguranca (escolher uma):**


1. **Header auth** — IngressRoute com middleware que valida um header secreto (ex: `X-Loki-Token`)
2. **IP allowlist** — middleware Traefik que so aceita o IP de saida do EKS
3. **Ambos** — header + IP allowlist (recomendado)


---

## 2. O que muda em relacao ao setup AWS

| Item | AWS (atual) | GKE (target) |
|----|----|----|
| Storage backend | S3 (`sa-east-1`) | GCS bucket (`us-central1`) |
| Auth | IRSA (IAM Role) | Workload Identity (GCP SA) |
| StorageClass | `szn-ebs-gp3-retained` | `standard-rwo` (default GKE) |
| Node Selector | `node-pool: general-karpenter-system` | `node_pool: tools-prod-pool` |
| Tolerations | `workload-type: monitoring` | Remover (nao ha taints no GKE) |
| Registry | ECR (`711387131913.dkr.ecr...`) | Imagens publicas Grafana |
| Secrets | AWS Secrets Manager | AWS Parameter Store (`aws-parameter-store-global` ja existe no GKE) |
| ArgoCD destination | `https://kubernetes.default.svc` | `https://34.60.64.40` |
| Datasource Loki | `loki-gateway.monitoring.svc.cluster.local` | `https://loki-gke.seazone.com.br` (via Traefik) |
| DNS | N/A | Criar `loki-gke.seazone.com.br` -> `35.225.201.214` |


---

## 3. Infraestrutura do cluster GKE

**Cluster:** `cluster-tools-prod-gke` (`us-central1-a`) **Projeto GCP:** `tools-440117`

### Node pools disponiveis

| Pool | Nodes | Tipo | Spot |
|----|----|----|----|
| `tools-prod-pool` | 21 | `e2-standard-4` | Nao |
| `nodepool-default-spot` | 1 | `e2-standard-2` | Sim |
| `ingress-prod-pool` | 3 | `e2-standard-2` | Nao |

**Pool alvo para monitoring:** `tools-prod-pool`

### Namespaces existentes

baserow, default, dev-n8n, ecr-token-refresher, external-secrets, kestra-poc, n8n, n8n-poc, outline, prd-n8n, tools, traefik-system

### Storage classes

| Nome | Provisioner | Default |
|----|----|----|
| `standard-rwo` | `pd.csi.storage.gke.io` | Sim |
| `premium-rwo` | `pd.csi.storage.gke.io` | Nao |
| `standard` | `kubernetes.io/gce-pd` | Nao |

### Secret stores

| Nome | Tipo | Status |
|----|----|----|
| `aws-parameter-store-global` | ClusterSecretStore | Valid |


---

## 4. Estrutura de diretorios

```
argocd/applications/monitoring-gke/
├── PLANO_IMPLANTACAO.md      # Este documento
├── loki/
│   ├── application.yaml      # ArgoCD Application
│   └── values.yaml           # Helm values (storage GCS, Workload Identity)
└── promtail/
    ├── application.yaml      # ArgoCD Application
    └── values.yaml           # Helm values (DaemonSet, coleta de logs)
```

IngressRoute e middleware do Loki ficam dentro do `values.yaml` do Loki como extra manifests.


---

## 5. Capacidade do cluster — Analise pre-deploy

### Estado atual (12/03/2026)

| Metrica | Valor | Observacao |
|----|----|----|
| Nodes total | 23 | 20 tools-prod + 3 ingress + 1 spot |
| Max pods por node | **30** | Limite do GKE (configurado no node pool) |
| Pods running | 313 | Media \~14 pods/node (max atual: 16) |
| CPU requests | 75%-99% | **13 nodes com >90% de CPU alocada** |
| Memoria uso real | 26%-80% | Alguns nodes >70% |

### Impacto da stack de monitoring

| Componente | Pods novos | CPU request (total) | Memoria request (total) |
|----|----|----|----|
| Loki backend (2) | 2 | 300m | 400Mi |
| Loki read (2) | 2 | 800m | 2Gi |
| Loki write (2) | 2 | 200m | 1.8Gi |
| Loki gateway (1) | 1 | 100m | 128Mi |
| Memcached (3 caches) | 3 | \~300m | \~1.5Gi |
| Promtail (DaemonSet) | 23 | 2300m (100m x23) | 1.5Gi (64Mi x23) |
| **Total** | **\~33 pods** | **\~4000m** | **\~7.3Gi** |

### Risco: Pods Pending por falta de CPU schedulavel

13 dos 23 nodes tem >90% de CPU requests alocado. Os pods do Loki (especialmente read com 400m request cada) podem nao conseguir

ser agendados, ficando em estado `Pending`.

### Acao requerida: Aumentar node pool ANTES do deploy

**Aumentar** `**tools-prod-pool**` **em +3 nodes** (de 20 para 23). Isso adiciona \~6 vCPUs e \~24Gi de memoria schedulavel, garantindo margem

para o Loki e absorcao do Promtail DaemonSet.

> Alternativa: Reduzir CPU requests do Loki abaixo do planejado, mas nao recomendado — pode causar throttling.


---

## 6. Divisao de trabalho

> **Principio:** A e B trabalham 100% independentes nas Fases 1 e 2. Convergem apenas na Fase 3 (integracao), quando ambas as pecas ja estao deployed.

### Mapa de dependencias

```
FASE 0 — PRE-REQUISITO (antes de tudo)
  [A] Scale up node pool tools-prod-pool +3 nodes

FASE 1 — PARALELA (configs + infra)
  [A] Infra GCP + Loki configs ──────────────────┐
  [B] Promtail configs + Grafana datasource prep ─┤
                                                   │
FASE 2 — PARALELA (deploy)                        │
  [A] Deploy Loki + IngressRoute + DNS ───────────┤
  [B] Deploy Promtail + Grafana datasource ────── ┤  (B nao depende de A aqui:
                                                   │   Promtail reconecta sozinho,
                                                   │   datasource pode ser adicionado
                                                   │   antes do Loki estar UP)
                                                   │
FASE 3 — CONVERGENCIA (validacao)                  │
  [A+B] Validar pipeline end-to-end ◄─────────────┘
```

**Unica dependencia real:** A validacao end-to-end (Fase 3) requer que Loki, Promtail, IngressRoute, DNS e datasource estejam todos UP. Tudo antes disso

pode ser feito em paralelo porque:

* Promtail tenta reconectar ao Loki automaticamente (retry loop)
* O datasource no Grafana pode ser adicionado apontando para a URL mesmo antes dela estar acessivel — so vai dar erro no Explore ate o Loki subir


---

### Analista A — Infraestrutura GCP + Loki + Exposicao

#### Fase 0: Scale up do node pool (15min)

**0.1** Aumentar `tools-prod-pool` de 20 para 23 nodes:

```bash

gcloud container clusters resize cluster-tools-prod-gke \
  --node-pool tools-prod-pool \
  --num-nodes 23 \
  --zone us-central1-a \
  --project tools-440117
```

**0.2** Aguardar nodes `Ready`:

```bash

kubectl get nodes -l node_pool=tools-prod-pool --watch
```

#### Fase 1: Infra GCP + Configs Loki (1h)

**1.1** Criar namespace `monitoring` no GKE

```bash

kubectl create namespace monitoring
```

**1.2** Criar bucket GCS para o Loki

* Nome: `cluster-tools-gke-loki-logs`
* Regiao: `us-central1`
* Lifecycle: delete apos 28 dias (igual retencao do Loki)

**1.3** Criar GCP Service Account + Workload Identity

* SA: `loki-monitoring@tools-440117.iam.gserviceaccount.com`
* Role: `roles/storage.objectAdmin` no bucket
* Binding Workload Identity: `monitoring/loki` <-> GCP SA

**1.4** Criar `monitoring-gke/loki/application.yaml`

* destination: `https://34.60.64.40`, namespace: `monitoring`
* Chart: `loki` v6.35.1 do `https://grafana.github.io/helm-charts`

**1.5** Criar `monitoring-gke/loki/values.yaml` adaptando o existente:

* **Storage**: GCS ao inves de S3

  ```yaml
  storage:
    type: gcs
    gcs:
      bucketName: cluster-tools-gke-loki-logs
  ```
* **ServiceAccount**: Workload Identity ao inves de IRSA

  ```yaml
  serviceAccount:
    annotations:
      iam.gke.io/gcp-service-account: loki-monitoring@tools-440117.iam.gserviceaccount.com
  ```
* **Escala reduzida** (cluster menor que EKS):
  * Backend: 2 replicas
  * Read: 2 replicas
  * Write: 2 replicas
  * Gateway: 1 replica
* **Node selector**: `node_pool: tools-prod-pool`
* **StorageClass**: `standard-rwo`
* **Imagens**: publicas (sem ECR) — `memcached:1.6.38-alpine`
* **Remover**: tolerations de monitoring, afinidade de spot/karpenter

**1.6** Incluir IngressRoute + Middleware no values do Loki (extraObjects):

```yaml

apiVersion: traefik.io/v1alpha1

kind: IngressRoute

metadata:
  name: loki-gateway-external
  namespace: monitoring

spec:
  entryPoints:
    - websecure
  routes:
    - match: Host(`loki-gke.seazone.com.br`)
      kind: Rule
      services:
        - name: loki-gateway
          port: 80
      middlewares:
        - name: loki-ip-allowlist
        - name: loki-header-auth
```

#### Fase 2: Deploy + DNS (45min)

**2.1** Push branch -> ArgoCD sync -> validar Loki pods running

**2.2** Criar registro DNS `loki-gke.seazone.com.br` -> `35.225.201.214`

**2.3** Validar que IngressRoute responde externamente:

```bash

curl -H "Host: loki-gke.seazone.com.br" https://35.225.201.214/ready
```


---

### Analista B — Promtail + Preparacao Grafana

#### Fase 1: Configs Promtail + Grafana datasource (1h)

**1.1** Criar `monitoring-gke/promtail/application.yaml`

* destination: `https://34.60.64.40`, namespace: `monitoring`
* Chart: `promtail` v6.17.0 do `https://grafana.github.io/helm-charts`

**1.2** Criar `monitoring-gke/promtail/values.yaml` adaptando o existente:

* **Client URL**: `http://loki-gateway.monitoring.svc.cluster.local/loki/api/v1/push`
* **Volume mounts**: `/var/log/pods` (compativel com GKE/containerd)
* **Tolerations**: `operator: Exists` (DaemonSet em todos os nodes)
* **Priority class**: `system-node-critical`
* **Resources**: 100m-200m CPU, 64Mi-128Mi RAM
* **Remover**: afinidade de spot/karpenter, node-pool karpenter

**1.3** Preparar datasource `Loki-GKE` no Grafana existente

Editar `argocd/applications/monitoring/grafana/values.yaml`:

```yaml
# Adicionar ao array datasources existente:
- name: Loki-GKE
  type: loki
  access: proxy
  url: https://loki-gke.seazone.com.br
  jsonData:
    maxLines: 1000
    timeout: 180s
    httpHeaderName1: X-Scope-OrgID
    httpHeaderName2: X-Loki-Token
  secureJsonData:
    httpHeaderValue1: "1"
    httpHeaderValue2: "<token-secreto>"
  isDefault: false
  editable: true
```

#### Fase 2: Deploy Promtail + Sync Grafana (30min)

**2.1** Push branch -> ArgoCD sync -> validar Promtail DaemonSet (24+ pods)

> Promtail vai ficar em retry ate o Loki subir — isso e normal e esperado.

**2.2** Push alteracao do Grafana -> ArgoCD sync no EKS

> O datasource Loki-GKE vai aparecer no Grafana mas vai dar erro ate Loki + IngressRoute + DNS estarem prontos. Isso e esperado.

**2.3** Validar que Promtail esta running em todos os nodes:

```bash

kubectl get pods -n monitoring -l app.kubernetes.io/name=promtail -o wide
```


---

### Convergencia (A + B juntos) — Validacao end-to-end (30min)

> **Pre-condicao:** Ambos terminaram suas Fases 1 e 2.

**3.1** Validar Loki pods healthy:

```bash

kubectl get pods -n monitoring -l app.kubernetes.io/name=loki
```

**3.2** Validar Promtail conectado ao Loki (logs sem erros de conexao):

```bash

kubectl logs -n monitoring -l app.kubernetes.io/name=promtail --tail=20
```

**3.3** Validar IngressRoute externamente:

```bash

curl -s https://loki-gke.seazone.com.br/ready
```

**3.4** Testar query via CLI:

```bash

curl -s -H "X-Scope-OrgID: 1" \
  "https://loki-gke.seazone.com.br/loki/api/v1/query?query={namespace=\"n8n\"}&limit=5"
```

**3.5** Testar no Grafana Explore:

* Abrir `monitoring.seazone.com.br`
* Selecionar datasource `Loki-GKE`
* Query: `{namespace="n8n"}`
* Verificar que logs dos workers, editor e webhook aparecem

**3.6** Se tudo OK, atualizar tasks no Jira (SRE-4961)


---

## 7. Timeline

```
12/03 (hoje a tarde)
                    Analista A                          Analista B
                    ──────────                          ──────────
FASE 0 (pre-requisito)
14:00 ─────────── Scale up node pool +3 nodes ───── (aguardando ou ja iniciando

14:15 ─────────── Aguardar nodes Ready                configs em paralelo)

FASE 1 (paralela)
14:15 ─────────── Criar namespace monitoring ─────── Criar promtail/application.yaml

14:20 ─────────── Criar bucket GCS ──────────────── Criar promtail/values.yaml

14:30 ─────────── Criar SA + Workload Identity ──── Preparar datasource Loki-GKE

14:40 ─────────── Criar loki/application.yaml         no grafana/values.yaml

14:50 ─────────── Criar loki/values.yaml ─────────── (configs prontos)
15:10 ─────────── Incluir IngressRoute no values

FASE 2 (paralela)
15:10 ─────────── Push + deploy Loki ────────────── Push + deploy Promtail

15:25 ─────────── Aguardar pods running ─────────── Push + sync Grafana datasource

15:40 ─────────── Criar DNS ─────────────────────── Validar Promtail DaemonSet

15:50 ─────────── Validar IngressRoute ──────────── (aguardando convergencia)

FASE 3 (juntos)
16:00 ─────────── [A+B] Validacao end-to-end

16:15 ─────────── [A+B] Teste no Grafana Explore

16:30 ─────────── [A+B] Ajustes finais se necessario

13/03 (manha)
09:00 ─────────── [A+B] Smoke test final

09:30 ─────────── [A+B] Update tasks Jira SRE-4961
```


---

## 8. Checklist de validacao (Definition of Done)

- [ ] Node pool `tools-prod-pool` escalado para 23 nodes (todos Ready)
- [ ] Namespace `monitoring` existe no GKE
- [ ] Bucket GCS criado com Workload Identity funcional
- [ ] Loki pods (backend, read, write, gateway) `Running`
- [ ] Promtail DaemonSet rodando em todos os 24+ nodes
- [ ] IngressRoute `loki-gke.seazone.com.br` respondendo
- [ ] DNS `loki-gke.seazone.com.br` -> `35.225.201.214` propagado
- [ ] Datasource `Loki-GKE` adicionado no Grafana do EKS
- [ ] Query `{namespace="n8n"}` retorna logs no Grafana Explore
- [ ] ArgoCD Applications `Synced` + `Healthy`


---

## 9. Riscos e mitigacoes

| Risco | Mitigacao |
|----|----|
| Latencia cross-cluster (EKS sa-east-1 -> GKE us-central1) | Queries serao mais lentas (\~200ms extra). Aceitavel para logs. Se critico, considerar Grafana local no futuro |
| Seguranca do endpoint Loki exposto | Middleware Traefik com IP allowlist + header token |
| Workload Identity demorar para propagar | Alternativa: HMAC keys do GCS como k8s secret temporario |
| DNS nao propagar a tempo | Testar com IP direto `https://35.225.201.214` + header Host |
| Node pool sem capacity | 21 nodes on-demand, monitoring e leve |
| Promtail nao coletar logs (path diferente) | GKE com containerd usa `/var/log/pods` — mesmo path do EKS |
| ArgoCD nao alcancar cluster GKE | Ja tem apps deployando (external-secrets-gcp aponta para `34.60.64.40`) |


---

## 10. Referencia — Configs AWS existentes

Os valores de referencia para adaptacao estao em:

| Componente | Arquivo |
|----|----|
| Loki (AWS) | `argocd/applications/monitoring/loki/values.yaml` |
| Promtail (AWS) | `argocd/applications/monitoring/promtail/values.yaml` |
| Grafana (AWS) | `argocd/applications/monitoring/grafana/values.yaml` |

### Resumo do Loki AWS (para referencia de adaptacao)

* **Chart:** `loki` v6.35.1 (SimpleScalable)
* **Backend:** 5-10 replicas, Read: 5-12, Write: 5-10, Gateway: 2
* **Storage:** S3 `general-cluster-loki-logs-sa-east-1`
* **IRSA:** `arn:aws:iam::711387131913:role/general-cluster-monitoring-loki-role`
* **Schema:** TSDB v13, index period 24h
* **Retencao:** 672h (28 dias)
* **Cache:** Memcached (results 4Gi, chunks 6Gi, index 1Gi)

### Resumo do Promtail AWS (para referencia de adaptacao)

* **Chart:** `promtail` v6.17.0 (DaemonSet)
* **Client:** `http://loki-gateway.monitoring.svc.cluster.local/loki/api/v1/push`
* **Volumes:** `/var/log/pods` (RO), `/var/lib/docker/containers` (RO)
* **Scrape:** kubernetes-pods + kubernetes-services
* **Priority:** `system-node-critical`