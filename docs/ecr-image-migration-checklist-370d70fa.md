<!-- title: ECR Image Migration Checklist | url: https://outline.seazone.com.br/doc/ecr-image-migration-checklist-fxpEyerUFw | area: Tecnologia -->

# ECR Image Migration Checklist

## EKS

### docker.io

- [ ] `clickhouse/clickhouse-server:latest` — clickhouse
- [ ] `traefik:v3.4.4` — traefik **(pending)**
- [ ] `alpine/socat`, `alpine/socat:latest` — prd-apps, stg-apps
- [ ] `busybox:1.36`, `docker.io/busybox:latest` — prd-apps, stg-apps, openpanel
- [ ] `grafana:12.1.0` — monitoring
- [ ] `loki:3.5.3`, `loki-canary:3.5.3` — monitoring
- [ ] `promtail:3.5.1` — monitoring
- [ ] `tempo:2.8.2` — monitoring
- [ ] `memcached:1.6.33-alpine`, `memcached:1.6.38-alpine` — monitoring **(pending)**
- [ ] `memcached-exporter:v0.14.4`, `memcached-exporter:v0.15.3` — monitoring **(pending)**
- [ ] `nginx-unprivileged:1.27-alpine`, `nginx-unprivileged:1.29-alpine` — monitoring **(pending)**
- [ ] `kiwigrid/k8s-sidecar:1.30.7` — monitoring
- [ ] `louislam/uptime-kuma:2.1.1` — monitoring
- [ ] `otel/opentelemetry-collector-contrib:0.131.0` — monitoring
- [ ] `google/cloud-sdk:alpine` — tools
- [ ] `growthbook/growthbook:3.5.0` — tools
- [ ] `mongo:8.0` — tools
- [ ] `percona/mongodb_exporter:0.40.0` — tools
- [ ] `opensourceelectrolux/aws-cost-exporter:v1.1.1` — finops

### quay.io

- [ ] `argoproj/argocd:v3.0.6` — argocd
- [ ] `argoproj/argocli:v3.7.7`, `argoexec:v3.7.7`, `workflow-controller:v3.7.7` — argo-workflows, prd-apps
- [ ] `jetstack/cert-manager-controller/cainjector/webhook:v1.13.5` — cert-manager
- [ ] `prometheus/prometheus:v3.5.0`, `alertmanager:v0.28.1`, `node-exporter:v1.9.1` — monitoring
- [ ] `prometheus-operator:v0.84.1`, `prometheus-config-reloader:v0.84.1` — monitoring

### ghcr.io

- [ ] `kedacore/keda:2.18.1`, `keda-admission-webhooks:2.18.1`, `keda-metrics-apiserver:2.18.1` — keda
- [ ] `dexidp/dex:v2.43.1` — argocd

### icr.io

- [ ] `kubecost/cost-model:3.0.4`, `frontend:3.0.4`, `cluster-controller:v0.16.29`, `modeling:v0.1.33`, `network-costs:v0.18.0` — kubecost
- [ ] `ibm-finops/agent:v1.0.3` — kubecost

### outros

- [ ] `external-secrets:v0.18.2` — external-secrets (oci.external-secrets.io)
- [ ] `kube-rbac-proxy:v0.15.0` — opensearch-operator (gcr.io)
- [ ] `kube-state-metrics:v2.16.0` — monitoring (registry.k8s.io)
- [ ] `metrics-server:v0.8.0` — kube-system (registry.k8s.io)


---

## GKE

### docker.io

- [ ] `traefik:v3.3.6` — traefik-system
- [ ] `outlinewiki/outline:0.87.1` — outline
- [ ] `kestra/kestra:v1.2.2` — kestra-poc
- [ ] `docker:dind-rootless` — (sem namespace identificado)

### ghcr.io

- [ ] `external-secrets/external-secrets:v2.0.0` — external-secrets
- [ ] \