<!-- title: Métricas [rascunho] | url: https://outline.seazone.com.br/doc/metricas-rascunho-A43MinsnmE | area: Tecnologia -->

# Métricas [rascunho]

# Grafana

### Alertas de Disponibilidade (SLA)

* **Métrica**: `http_requests_total{job="my_app", code=~"5.."} / http_requests_total{job="my_app"}`
* **Criticidade**: Crítica
* **Regra**: A taxa de erros HTTP (códigos 5xx) é maior que 5% nos últimos 5 minutos.
* **Métrica**: `histogram_quantile(0.99, sum(rate(http_request_duration_seconds_bucket[5m])) by (le))`
* **Criticidade**: Aviso/Crítica
* **Regra**: O P99 da latência das requisições é maior que 2 segundos.
* **Métrica**: `kube_pod_container_status_running{container="my_app"}`
* **Criticidade**: Crítica
* **Regra**: O valor da métrica é 0, indicando que o container não está em execução.


---

### Alertas de Recurso

* **Métrica**: `sum(rate(container_cpu_usage_seconds_total{namespace="my_app_namespace"}[5m]))`
* **Criticidade**: Aviso
* **Regra**: O uso de CPU da aplicação é maior que 80% do limite configurado.
* **Métrica**: `sum(container_memory_usage_bytes{namespace="my_app_namespace"})`
* **Criticidade**: Aviso/Crítica
* **Regra**: O uso de memória da aplicação é maior que 85% do limite configurado.
* **Métrica**: `node_filesystem_free_bytes{job="node-exporter"} / node_filesystem_size_bytes{job="node-exporter"}`
* **Criticidade**: Crítica
* **Regra**: O espaço livre em disco de um nó é menor que 10% do total.


---

### Alertas de Estado do Kubernetes

* **Métrica**: `kube_pod_status_phase{phase="Running", job="kube-state-metrics"}`
* **Criticidade**: Crítica
* **Regra**: Um Pod não está em estado `Ready` por mais de 5 minutos.
* **Métrica**: `kube_deployment_status_replicas_available{job="kube-state-metrics"}`
* **Criticidade**: Crítica
* **Regra**: O número de réplicas disponíveis é diferente do número de réplicas desejado no deployment.

### Visualizando Alertas por Ambiente

* **Filtros úteis em Alert rules**:
  * Filtrar por `environment=production`
  * Filtrar por `environment=staging`
  * Filtrar por `severity=critical`

### Silenciando Alertas por Ambiente


1. Vá em **Alerting** → **Silences**# Tutorial COMPLETO: Configurando Alertas Grafana com Slack