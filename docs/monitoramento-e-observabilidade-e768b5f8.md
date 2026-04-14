<!-- title: Monitoramento e Observabilidade | url: https://outline.seazone.com.br/doc/monitoramento-e-observabilidade-7nar0soFPu | area: Tecnologia -->

# Monitoramento e Observabilidade

## Descrição:

Itens relacionados à visibilidade do ambiente e saúde da infraestrutura. Inclui métricas essenciais, queries úteis, dashboards, alertas configurados e boas práticas de observabilidade. Ajuda a detectar anomalias antes que causem impacto em produção.


***

### Template

```none
📊 [Tema Monitorado] - [Ferramenta ou Serviço] - [Data]

🎯 Objetivo

O que estamos tentando monitorar ou detectar?

📉 Métricas Relevantes

- Métrica 1  
- Métrica 2

🧪 Alertas Configurados

Descreva os thresholds, intervalos, e ações esperadas.

📊 Dashboards / Queries

Links ou trechos úteis:

Ex:
sum by(namespace) (kube_pod_container_status_terminated_reason{reason="Evicted"})

📝 Observações

Cobertura esperada, exceções conhecidas, limitações atuais.

🏷️ Tags

#observabilidade #grafana #prometheus #alertas
```