<!-- title: Workloads do cluster | url: https://outline.seazone.com.br/doc/workloads-do-cluster-2p5UEeTbhb | area: Tecnologia -->

# Workloads do cluster

| Namespace | Workload | Descrição | Resource Usage |
|----|----|----|----|
| `karpenter` | **karpenter** | Componente responsável pelo auto-scaling de nós dentro do cluster Kubernetes. | low |
| `traefik` | **traefik** | Ingress Controller responsável pelo roteamento de tráfego externo para os serviços internos do cluster. | medium |
| `tools` | **Outline** | Ferramenta de documentação e wiki. | high |
|    | **Outline-redis** | Redis utilizado pelo Outline para caching e sessões. | high |
|    | **Metabase** | Plataforma de BI e análise de dados. | high |
|    | **Opensearch-nodes** | Nós da instância OpenSearch, utilizado para armazenamento e busca de dados. | high |
|    | **Opensearch-masters** | Master nodes do OpenSearch para gerenciamento do cluster. | high |
|    | **Opensearch-dashboards** | Interface de visualização para o OpenSearch. | medium |
|    | **Opensearch-operator** | Operador responsável pela gestão dos recursos do OpenSearch. | low |
| `apps` | **worker-seazone-reservas** | Worker responsável pelo processamento de reservas da Seazone. | high |
|    | **worker-user-seazone-reservas** | Worker focado no processamento de usuários ligados às reservas da Seazone. | high |
|    | **api-seazone-reservas** | API central para gerenciamento das reservas. | high |
|    | **scheduler-seazone-reservas** | Componente responsável pelo agendamento de tarefas relacionadas às reservas. | low |
|    | **wallet** | Serviço principal da carteira digital. | low |
|    | **wallet-bff** | Backend-for-Frontend (BFF) para interação com a Wallet. | low |
| ```javascript
kube-system
``` | **aws-node** | Componente responsável pela integração dos nós do cluster com a AWS. | low |
|    | **coredns** | Serviço de resolução de nomes dentro do cluster Kubernetes. | low |
|    | **ebs-csi-controller** | Controlador do driver CSI do Amazon EBS. | low |
|    | **ebs-csi-node** | Componente de nós do driver CSI do Amazon EBS. | low |
|    | **efs-csi-controller** | Controlador do driver CSI do Amazon EFS. | low |
|    | **efs-csi-node** | Componente de nós do driver CSI do Amazon EFS. | low |
|    | **kube-proxy** | Mantém regras de rede nos nós e permite a comunicação entre pods e serviços. | low |
|    | **metrics-server** | Coleta métricas de uso de recursos no cluster Kubernetes. | low |
|    | **eks-pod-identity-agent** | Gerencia identidades de pods no Amazon EKS. | low |
| ```javascript
monitoramento
``` | **prometheus-operator** | Operador para gerenciar instâncias do Prometheus no cluster. | low |
|    | **OpenTelemetry-collector** | Coletor de métricas e traces OpenTelemetry. | medium |
|    | **prometheus-agent** | Agente Prometheus para coleta de métricas. | medium |
|    | **Grafana** | Plataforma de visualização de métricas e dashboards. | low |
|    | **kube-state-metrics** | Exporta métricas detalhadas sobre o estado dos recursos do Kubernetes. | low |
|    | grafana-tempo-ingester | Componente responsável por ingerir traces no Grafana Tempo. | high |
|    | grafana-tempo-compactor | Componente que compacta os dados armazenados no Grafana Tempo. | high |
|    | grafana-tempo-distributor | Distribuidor de traces no sistema Grafana Tempo. | medium |
|    | grafana-tempo-querier | Componente responsável por consultas no Grafana Tempo. | high |
|    | grafana-tempo-query-frontend | Interface de frontend para consultas no Grafana Tempo. | high |
|    | grafana-tempo-metrics-generator | Gerador de métricas baseado nos dados do Grafana Tempo. | medium |
|    | loki-ingester | Componente responsável por ingerir logs no Loki. | high |
|    | loki-compactor | Componente que compacta os dados armazenados no Loki. | high |
|    | loki-distributor | Distribuidor de logs no sistema Loki. | medium |
|    | loki-querier | Componente responsável por consultas no Loki. | high |
|    | loki-query-frontend | Interface de frontend para consultas no Loki. | high |
|    | loki-metrics-gateway | Gateway nginx  | low |
|    | loki-distributed-query-scheduler | Scheduler para consultas distribuídas no Loki. | low |
|    | grafana-mimir-ingester | Componente responsável por ingerir métricas no Grafana Mimir. | high |
|    | grafana-mimir-compactor | Componente que compacta os dados armazenados no Grafana Mimir. | high |
|    | grafana-mimir-distributor | Distribuidor de métricas no sistema Grafana Mimir. | medium |
|    | grafana-mimir-querier | Componente responsável por consultas no Grafana Mimir. | high |
|    | grafana-mimir-query-frontend | Interface de frontend para consultas no Grafana Mimir. | high |
|    | grafana-mimir-nginx | Servidor Nginx para balanceamento de carga no Grafana Mimir. | low |
|    | grafana-mimir-overrides-exporter | Exportador de overrides no Grafana Mimir. | low |
|    | grafana-mimir-store-gateway | Gateway de armazenamento no Grafana Mimir. | high |
|    | grafana-mimir-query-scheduler | Scheduler para consultas distribuídas no Grafana Mimir. | low |
|    | grafana-mimir-alertmanager | Componente de gerenciamento de alertas do Grafana Mimir. | low |

##