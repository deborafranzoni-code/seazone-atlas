<!-- title: Levantamento de Métricas de Suporte | url: https://outline.seazone.com.br/doc/levantamento-de-metricas-de-suporte-qXxdym2Uij | area: Tecnologia -->

# Levantamento de Métricas de Suporte

## 1. Métricas Temporais Fundamentais

* **First Response Time (FRT):** tempo entre criação do ticket no Jira e primeira interação humana

  **Fonte:** timestamps de criação e transição `BACKLOG → FIRST CALL` no Jira
* **Resolution Time:** tempo entre criação do ticket e conclusão em DONE

  **Fonte:** Jira (criação → DONE)
* **Active Work Time:** tempo efetivo de trabalho (excluindo espera)

  **Fonte:** Jira (intervalos em `TODO`, `WIP`, `REVIEW`)

## 2. Métricas de Volume e Distribuição

* **Tickets Created/Day:** volume diário de entrada

  **Fonte:** Jira (quantidade de tickets que chegam em x data)
* **Tickets Resolved/Day:** tickets concluídos por dia

  **Fonte:** Jira (status DONE por dia)
* **Throughput:** tickets processados por período

  **Fonte:** Jira (issues finalizadas por semana)
* **Distribuição por Categoria:**
  * Complexidade
  * Impacto
  * Tipo (incidente/requisição/projeto)

    **Fonte:** tags/metadados obrigatórios definidos no Jira

## 3. Métricas de Qualidade e Eficiência

* **SLA Compliance:** % de tickets dentro dos tempos definidos

  **Fonte:** combinação Jira (tempo real) vs SLAs acordados


---

## Proposta de SLAs Baseados em Dados

### Metodologia para Definição


1. **Coleta baseline** das métricas propostas
2. **Análise estatística** dos tempos atuais
3. **Definição de targets** baseados em capacidade demonstrada + margem de melhoria

## Métricas Não Prioritárias/Arquivadas

* **Escalation Time:** tempo entre identificação de escalação e transferência de board (Suporte → Delivery/Upstream)
* **Backlog Loss Rate:** variação de crescimento de tickets em BACKLOG

  **Fonte:** Jira (contagem semanal do status BACKLOG)
* **Internal Queue Time:** tempo em cada status (BACKLOG, TODO, WIP, REVIEW)

  **Fonte:** Jira (histórico de status)

  **Fonte:** Jira (logs de transferência entre boards)
* **First Contact Resolution Rate:** % de tickets resolvidos sem transferência

  **Fonte:** Jira (tickets resolvidos dentro do board Suporte)
* **Customer Satisfaction Score:** feedback qualitativo do solicitante

  **Fonte:** Slack (resposta de confirmação ou comentários do solicitante)