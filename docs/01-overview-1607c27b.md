<!-- title: 01-Overview | url: https://outline.seazone.com.br/doc/01-overview-uj179UO6yQ | area: Tecnologia -->

# 01-Overview

## O que é este serviço

O n8n é a plataforma de automação de workflows da Seazone, utilizada para integrar sistemas, processar dados e orquestrar processos internos. Roda em modo self-hosted no cluster GKE `cluster-tools-prod-gke`.

## Stack técnica

| Camada | Tecnologia | Papel |
|----|----|----|
| Orquestração | ArgoCD (multi-source) | GitOps — sincroniza manifests do repositório para o cluster |
| Runtime | GKE (Google Kubernetes Engine) | Cluster Kubernetes gerenciado |
| Charts Helm | `seazone-tech/helm-charts` | Templates dos deployments de n8n, Redis e PostgreSQL |
| Segredos | AWS Parameter Store + External Secrets Operator | Pull automático de credenciais para Secrets K8s |
| Ingress | Traefik | Roteamento HTTP/HTTPS para os componentes do n8n |
| Banco de dados | PostgreSQL (dev: in-cluster; prd: GCP Cloud SQL) | Persistência de workflows, credentials e execuções |
| Queue / Cache | Redis (dev: in-cluster; prd: GCP Memorystore) | Fila Bull para distribuição de jobs entre workers |
| Backup | GCS + Workload Identity | Export diário de workflows e credentials em JSON |
| Monitoramento | Google Managed Prometheus (PodMonitoring) | Métricas de execução e performance |

## Ambientes

| Ambiente | Namespace K8s | URL Editor | URL Webhooks |
|----|----|----|----|
| Desenvolvimento | `dev-n8n` | `dev-automation.seazone.com.br` | `dev-webhook-automation.seazone.com.br` |
| Produção | `prd-n8n` | `automation.seazone.com.br` | `webhook-automation.seazone.com.br` |

## Decisões arquiteturais relevantes

* **Queue mode** (vs. single-process): escolhido para permitir escalonamento independente de workers e webhooks, isolando a UI da carga de execução.
* **Task runners externos** (`n8nio/runners`): sidecar separado para execução de Code Nodes, seguindo recomendação de segurança da v2.0+ do n8n.
* **Redis gerenciado em prd**: o GCP Memorystore (HA) é usado em produção para evitar perda de jobs na fila em caso de falha do nó.
* **Backup via CLI + GCS**: escolhido como camada de fallback para o VolumeSnapshot — permite restaurar workflows e credentials sem snapshot de disco.
* `**prune: false**` **no ArgoCD**: protege contra deleção acidental de recursos em produção. Toda remoção requer sync explícito com `--prune`.

## Repositórios envolvidos

| Repositório | Uso |
|----|----|
| `seazone-tech/gitops-governanca` | Este repo — manifests ArgoCD, values Helm, ExternalSecrets, IngressRoutes |
| `seazone-tech/helm-charts` | Charts Helm de n8n, Redis e PostgreSQL (consumidos pelo ArgoCD) |