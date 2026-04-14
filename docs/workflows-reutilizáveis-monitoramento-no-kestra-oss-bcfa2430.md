<!-- title: Workflows Reutilizáveis & Monitoramento no Kestra OSS | url: https://outline.seazone.com.br/doc/workflows-reutilizaveis-monitoramento-no-kestra-oss-U1b6GqRcdV | area: Tecnologia -->

# Workflows Reutilizáveis & Monitoramento no Kestra OSS

Ambiente atual: **Kestra OSS 1.2.2** no GKE.


---

# Parte 1 — Workflows Reutilizáveis

O mecanismo principal de reutilização no Kestra são os **Subflows**. Templates foram deprecados na versão 0.11 (2023), subflows são a única abordagem atual.


---

## Como funcionam Subflows

Um subflow é uma execução separada de um flow chamado por outro flow. Funciona como uma chamada de função: você passa inputs, aguarda o resultado, e recebe outputs.

```
Parent Flow
  └── task: Subflow (chama outro flow)
        └── executa como execução independente
              └── retorna outputs para o parent
```

Cada subflow cria uma **execução própria** no Kestra. Isso significa que:

* Logs e histórico são separados
* Falha no subflow não travou as tarefas anteriores do parent
* Performance do parent não é afetada pelo volume de tasks do subflow


---

## Quando usar Subflows na prática

| Situação | Usar Subflow? |
|----|----|
| ==Flow com mais de 100 tasks== | ✅ Sim — quebra em subflows para evitar degradação de performance |
| ==Lógica reusada por múltiplos flows (ex: notificação, autenticação)== | ✅ Sim |
| ==Flow pequeno e simples (< 10 tasks, usado só uma vez)== | ❌ Não necessário |
| ==Flow que precisa chamar a si mesmo== | ❌ Não permitido — sem recursão |


---

## Limitações

* **Restart do parent** reinicia todos os subflows que já foram executados 


---

# Parte 2 — Monitoramento

Três camadas de monitoramento disponíveis no OSS: **UI do Kestra**, **Prometheus + Grafana**, e **alertas via Flow Trigger**.


---

## 1. UI do Kestra — Monitoramento básico

A UI expõe por padrão:

* **Execuções** — lista com status, duração, namespace e labels
* **Logs por task** — saída completa de cada task em tempo real
* **Timeline** — visualização do progresso da execução
* **Outputs** — arquivos gerados pela execução

Para filtrar execuções, é possível usar as **labels** nos flows (ver [governanca-usuario-unico.md).](https://outline.seazone.com.br/doc/governanca-usuario-unico-idsix9IYrQ)


---

## 2. Prometheus + Grafana — Métricas do cluster

O Kestra expõe métricas Prometheus na porta **8081** no endpoint `/prometheus`.

### Métricas-chave

| Métrica | Tipo | O que mede |
|----|----|----|
| `kestra_executor_execution_started_count_total` | counter | Total de execuções iniciadas |
| `kestra_executor_execution_end_count_total` | counter | Total de execuções finalizadas |
| `kestra_executor_execution_duration_seconds` | summary | Duração das execuções |
| `kestra_executor_taskrun_ended_count_total` | counter | Total de tasks finalizados |
| `kestra_worker_job_pending` | gauge | Tasks esperando execução |
| `kestra_worker_job_running` | gauge | Tasks em execução agora |
| `kestra_scheduler_trigger_count_total` | counter | Triggers avaliados pelo scheduler |


---

## 3. Alertas — Flow Trigger centralizado

Em vez de adicionar lógica de alerta em cada flow, cria um único flow que **escuta falhas em qualquer flow de um namespace** e notifica.

### Como o Flow Trigger funciona

* **Não precisa editar** nenhum outro flow, ele escuta automaticamente
* Pode criar um alerta por namespace ou um único para todo o ambiente
* Funciona no OSS sem necessidade de plugins adicionais


---

## Fontes

* [Subflows — Docs](https://kestra.io/docs/workflow-components/subflows)
* [Flow Best Practices](https://kestra.io/docs/best-practices/flows)
* [Prometheus Metrics](https://kestra.io/docs/administrator-guide/prometheus-metrics)
* [Alerting & Monitoring](https://kestra.io/docs/administrator-guide/monitoring)
* [Grafana + Prometheus Setup](https://kestra.io/docs/how-to-guides/monitoring)