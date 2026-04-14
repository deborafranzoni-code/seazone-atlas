<!-- title: Validação de Imagens  EKS | url: https://outline.seazone.com.br/doc/validacao-de-imagens-eks-of08wzbR5t | area: Tecnologia -->

# Validação de Imagens  EKS

Realizei um levantamento de todas as imagens em uso nos pods do cluster EKS, verificando se estão sendo puxadas do ECR ou de registries externos.


---

## Imagens no ECR ✅

Todas as aplicações de produto estão corretamente usando ECR:

* `reservas-api`, `reservas-frontend`
* `sapron-api`, `sapron-frontend`
* `wallet-api`, `wallet-frontend`
* `openpanel-api/dashboard/worker`
* `metabase`, `clickhouse-keeper`, `clickhouse-operator`, `metrics-exporter`
* `metrics-daemon`
* Componentes AWS gerenciados (`kube-proxy`, `aws-node`, `ebs-csi`, `efs-csi`, etc.) via ECR da AWS (`602401143452.dkr.ecr.sa-east-1.amazonaws.com`)
* Karpenter e AWS Load Balancer Controller via `public.ecr.aws`


---

## Imagens fora do ECR ❌

### docker.io — 29 imagens

| Imagem | Namespace |
|----|----|
| `clickhouse/clickhouse-server:latest` | clickhouse |
| `traefik:v3.4.4` | traefik |
| `alpine/socat`, `alpine/socat:latest` | prd-apps, stg-apps |
| `docker.io/busybox:latest`, `busybox:1.36` | prd-apps, stg-apps, openpanel |
| `opensearch:2.11.1`, `opensearch-dashboards:2.11.1` | prd-apps, stg-apps |
| `opensearch-operator:2.8.0` | opensearch-operator |
| `grafana:12.1.0`, `loki:3.5.3`, `loki-canary:3.5.3`, `promtail:3.5.1`, `tempo:2.8.2` | monitoring |
| `memcached:1.6.33-alpine`, `memcached:1.6.38-alpine`, `memcached-exporter:v0.14.4/v0.15.3` | monitoring |
| `nginx-unprivileged:1.27-alpine`, `nginx-unprivileged:1.29-alpine` | monitoring |
| `otel/opentelemetry-collector-contrib:0.131.0` | monitoring |
| `kiwigrid/k8s-sidecar:1.30.7` | monitoring |
| `louislam/uptime-kuma:2.1.1` | monitoring |
| `mongo:8.0` | tools |
| `google/cloud-sdk:alpine` | tools |
| `growthbook/growthbook:3.5.0` | tools |
| `percona/mongodb_exporter:0.40.0` | tools |
| `opensourceelectrolux/aws-cost-exporter:v1.1.1` | finops |

### quay.io — 12 imagens

| Imagem | Namespace |
|----|----|
| `argoproj/argocd:v3.0.6` | argocd |
| `argoproj/argocli:v3.7.7`, `argoexec:v3.7.7`, `workflow-controller:v3.7.7` | argo-workflows, prd-apps |
| `jetstack/cert-manager-controller/cainjector/webhook:v1.13.5` | cert-manager |
| `prometheus/prometheus:v3.5.0`, `alertmanager:v0.28.1`, `node-exporter:v1.9.1` | monitoring |
| `prometheus-operator/prometheus-operator:v0.84.1`, `prometheus-config-reloader:v0.84.1` | monitoring |

### ghcr.io — 4 imagens

| Imagem | Namespace |
|----|----|
| `kedacore/keda:2.18.1`, `keda-admission-webhooks:2.18.1`, `keda-metrics-apiserver:2.18.1` | keda |
| `dexidp/dex:v2.43.1` | argocd |

### icr.io (IBM) — 6 imagens

| Imagem | Namespace |
|----|----|
| `kubecost/cost-model:3.0.4`, `frontend:3.0.4`, `cluster-controller:v0.16.29`, `modeling:v0.1.33`, `network-costs:v0.18.0` | kubecost |
| `ibm-finops/agent:v1.0.3` | kubecost |

### Outros registries

| Imagem | Registry | Namespace |
|----|----|----|
| `external-secrets:v0.18.2` | oci.external-secrets.io | external-secrets |
| `kube-rbac-proxy:v0.15.0` | gcr.io | opensearch-operator |
| `kube-state-metrics:v2.16.0` | registry.k8s.io | monitoring |
| `metrics-server:v0.8.0` | registry.k8s.io | kube-system |


---

**Total: \~53 imagens distintas fora do ECR**, distribuídas principalmente nos namespaces `monitoring`, `prd-apps`, `stg-apps`, `argocd`, `keda`, `clickhouse`, `kubecost` e `tools`.