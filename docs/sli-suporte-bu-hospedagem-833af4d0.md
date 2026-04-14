<!-- title: SLI - SUPORTE BU-HOSPEDAGEM | url: https://outline.seazone.com.br/doc/sli-suporte-bu-hospedagem-oCaIwitv2d | area: Tecnologia -->

# SLI - SUPORTE BU-HOSPEDAGEM

Resumo dos dados de SLI dos Suportes no `#suporte-hosting`

Os dados obtidos pertencem aos últimos 30 dias separados por semana, que é o tempo que atua cada OnCall, os dados ficam neste [painel do pipefy](https://app.pipefy.com/pipes/305658493/dashboards/169333)


### Intervalo de Tempo: 

As semanas consideradas nesta analise são desde a Semana 2 do ano 2026

* Semana 2 - Jan 5, 2026
* Semana 3 - Jan 12, 2026
* Semana 4 - Jan 19, 2026
* Semana 5 - Jan 26, 2026
* Semana 6 - Feb 2, 2026\*


### 1. Saiu de Priorização (Em Dias)

*Tempo médio que o ticket leva para ser triado e priorizado.*

| **Criado em** | **Lead time (Dias) - média** |
|----|----|
| **Jan 5, 2026** | **7,26 dias** |
| **Jan 12, 2026** | **3,07 dias** |
| **Jan 19, 2026** | **2,70 dias** |
| **Jan 26, 2026** | **2,80 dias** |
| **Feb 2, 2026**\* | *0,78 dias* |


### 2. Tempo em Atendimento (Em Dias)

| **Criado em** | **Lead time (Dias)** |
|----|----|
| **Jan 5, 2026** | **9,61 dias** |
| **Jan 12, 2026** | **3,02 dias** |
| **Jan 19, 2026** | **3,25 dias** |
| **Jan 26, 2026** | **2,29 dias** |
| **Feb 2, 2026**\* | **0,79 dias** |


### 2. P1 - Concluídos/Jira (Em Dias) - SLA 1 dia

*Tempo médio para resolver chamados de prioridade alta.*

| **Criado em** | **Lead time (Dias) - média** |
|----|----|
| **Jan 5, 2026** | **7,13 dias** |
| **Jan 12, 2026** | **3,90 dias** |
| **Jan 19, 2026** | **0,89 dias** (Menos de 24h) |
| **Jan 26, 2026** | **3,34 dias** |
| **Feb 2, 2026**\* | *0,00 dias* (Sem conclusões até o momento) |


### 3. P2 - Concluídos/Jira (Em Dias) - SLA 5 dias

*Tempo médio para resolver chamados de prioridade média/normal.*

| **Criado em** | **Lead time (Dias) - média** |
|----|----|
| **Jan 5, 2026** | **0,00 dias** (Sem registros) |
| **Jan 12, 2026** | **7,69 dias** |
| **Jan 19, 2026** | **6,58 dias** |
| **Jan 26, 2026** | **5,63 dias** |
| **Feb 2, 2026**\* | *1,09 dias* |

\**Nota: Os dados de Feb 2 são parciais (semana em andamento).*


### **RESUMO:**


1. **Priorização:** Estacionou na casa dos **2,7 a 2,8 dias**.
2. **Em Atendimento:** Na primeira semana de janeiro, um ticket ficava em atendimento por quase **10 dias**. Na última semana cheia (26 de jan), esse tempo caiu para **2,29 dias**.
3. P0: Não tivemos P0 registrados nos últimos 30 dias
4. **P1:** Teve um excelente resultado em 19/Jan (**0,8 dia**), mas piorou para **3,3 dias** na última semana cheia.
5. **P2:** Vem melhorando semanalmente, caindo de **7,6** para **5,6 dias**.
6. **Priorização com Atendimento:** Note que na semana de 26 de Jan, o **Tempo em Atendimento (2,29 dias)** foi menor que o tempo de **Priorização (2,80 dias)**. Isso reforça que o gargalo atual não é a velocidade da execução técnica, mas sim a demora em tirar o ticket da fila

**Observações e itens de ação:**


1. Hoje não medimos o tempo de primeira resposta -> Definir um SLA para a triagem que inclui a priorização.
2. Não estamos cumprindo nosso SLA dos suportes P1 -> A ação 1 pode ter impacto de melhora nesse ponto.


\