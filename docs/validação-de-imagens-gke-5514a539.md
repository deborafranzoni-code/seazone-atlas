<!-- title: Validação de Imagens GKE | url: https://outline.seazone.com.br/doc/validacao-de-imagens-gke-L7CxVfV2xG | area: Tecnologia -->

# Validação de Imagens GKE

Realizei um levantamento de todas as imagens em uso nos pods do cluster GKE verificando se estão sendo puxadas do Artifact Registry gerenciado pelo Google ou de registries externos.


---

## Imagens no Artifact Registry (GKE-managed) ✅

Todos os componentes internos do GKE estão usando `us-central1-artifactregistry.gcr.io/gke-release`:

* `calico/cni`, `calico/node`, `calico/typha`
* `kube-proxy-amd64`, `k8s-dns-*`, `metrics-server`
* `fluent-bit`, `fluent-bit-gke-exporter`, `event-exporter`
* `gcp-compute-persistent-disk-csi-driver`, `csi-node-driver-registrar`
* `gke-metrics-agent`, `gke-metrics-collector`, `gke-metadata-server`
* `prometheus-engine/prometheus`, `prometheus-engine/operator`, `prometheus-engine/config-reloader`
* `netd`, `netd-init`, `ip-masq-agent`, `proxy-agent`
* `cluster-proportional-autoscaler`, `ingress-gce-404-server-with-metrics`


---

## Imagens fora do Artifact Registry ❌

Todas as aplicações do cluster estão usando imagens de registries externos. Não há nenhuma imagem de aplicação espelhada em registry próprio (ECR ou Artifact Registry privado).

### docker.io — 13 imagens

| Imagem | Namespace |
|----|----|
| `baserow/backend:1.35.1`, `baserow/web-frontend:1.35.1` | baserow |
| `traefik:v3.3.6` | traefik-system |
| `n8nio/n8n:2.6.3`, `n8nio/n8n:2.8.3` | n8n-poc, dev-n8n, prd-n8n |
| `n8nio/runners:2.6.3`, `n8nio/runners:2.8.3` | n8n-poc, dev-n8n, prd-n8n |
| `nginx:1.27-alpine`, `nginx:alpine` | dev-n8n, n8n-poc |
| `postgres:14-alpine`, `postgres:17` | n8n, n8n-poc, dev-n8n |
| `redis:7-alpine`, `redis:7.4-alpine` | n8n, n8n-poc, dev-n8n |
| `google/cloud-sdk:alpine` | dev-n8n, prd-n8n |
| `outlinewiki/outline:0.87.1` | outline |
| `verdaccio/verdaccio:5.32.1` | verdaccio |
| `kestra/kestra:v1.2.2` | kestra-poc |
| `docker:dind-rootless` | *(sem namespace identificado)* |
| `busybox:1.36` | *(sem namespace identificado)* |

### ghcr.io — 1 imagem

| Imagem | Namespace |
|----|----|
| `external-secrets/external-secrets:v2.0.0` | external-secrets |

### docker.n8n.io — 1 imagem

| Imagem | Namespace |
|----|----|
| `n8nio/n8n:1.109.2` | n8n |


---

**Total: \~15 imagens distintas fora de registry próprio**, todas sendo aplicações. O cluster GKE (`tools-prod`) não possui nenhuma imagem de aplicação espelhada em Artifact Registry privado ou ECR  tudo vem diretamente de registries públicos externos.