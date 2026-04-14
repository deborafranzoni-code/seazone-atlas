<!-- title: Métrica de SLA | url: https://outline.seazone.com.br/doc/metrica-de-sla-AjeH2PS4nX | area: Tecnologia -->

# Métrica de SLA

# Suporte Wallet 

Considerando suportes ***==criados==*** nos últimos 30 dias e atualmente estão ***==Concluídos==***

Nosso SLA definido é:

* P0 (**Crítico**) - Highest - 1 a 4 horas
* P1 (**Alto**) - High           - 1 dia
* P2 (**Médio**) - Medium - 1 a 3 dias
* P3 (**Baixo**) - Low         - 5 a 7 dias
* P4 (**Mínimo**) - Lowest - mais de 15 dias


## Resultados (**SLI - Service Level Indicator - Indicador de Nível de Serviço)**

Numero de cards (por prioridade) e  media de Priorização nos últimos 30 dias, disponível nesse [dashboard](https://app.pipefy.com/pipes/305658493/dashboards/157580), foi de:


 ![](/api/attachments.redirect?id=1ad247dc-1922-4400-ac50-7290521c8892 " =591x305")



| **Prioridade** | **Priorização** |
|----|----|
| P0-Highest | 2.9120320713888889 |
| P1-High | 63.98229725574652776910 |
| P2-Medium | 85.6430726072395833 |
| P3-Low | 21.1171983088888889 |
| P4-Lowest | 43.1932962827777778 |


## Analise dos Resultados



| **Prioridade** | **Resolução** | **Priorização** |
|----|----|----|
| * P0 (**Crítico**) - Highest - | *  1 a 4 horas | 2.9120320713888889 |
| * P1 (**Alto**) - High           -  | * 1 dia | 63.98229725574652776910 |
| * P2 (**Médio**) - Medium -  | * 1 a 3 dias | 85.6430726072395833 |
| * P3 (**Baixo**) - Low         -  | * 5 a 7 dias | 21.1171983088888889 |
| * P4 (**Mínimo**) - Lowest -  | * mais de 15 dias | 43.1932962827777778 |


* **P0 (Crítico):** Priorização ágil em **menos de 3 horas**.  **✅**
* **P1 (Alto):** Demora de **64 horas** (\~2.5 dias úteis) para serem priorizados. **(Ponto de Atenção) ⚠️**
* **P2 (Médio):** O mais lento, com **85 horas** (\~3.5 dias úteis). **(Ponto de Atenção) ⚠️**
* **P3 (Baixo) e P4 (Mínimo):** Priorizados mais rápido que P1 e P2, com **21 e 43 horas**, respectivamente. **👀**


* **Inconsistência na Priorização (P1 vs. P3):** 
  * **O que os dados mostram:** Um ticket de prioridade Alta (P1) leva 3 vezes mais tempo para ser priorizado do que um de prioridade Baixa (P3). 
  * **Hipótese:** Isso pode indicar que os tickets P1 chegam com informações insuficientes, exigindo mais análise antes da priorização, ou que a equipe foca em resolver tickets mais simples (P3) primeiro para "limpar a fila".

    \
    \
    ![](/api/attachments.redirect?id=68b25cc6-8684-46fd-84e6-6fb6dbf3286d " =810x319")

    \
* **O Grande Gargalo (P2 - Prioridade Média):** 
  * **O que os dados mostram:** Tickets de prioridade Média são os mais lentos, levando em média 85.6 horas (mais de 3.5 dias úteis) para serem priorizados. 
  * **Hipótese:** Esses tickets podem ser complexos demais para uma decisão rápida, mas não urgentes o suficiente para receberem atenção imediata. Eles acabam "esquecidos" na caixa de entrada enquanto a equipe lida com os extremos (P0 e P3/P4).


## Próximos Passos


1. **Investigar o Fluxo de P1 e P2:** Realizar uma análise qualitativa (revisar os cards) para entender por que tickets P1 e P2 demoram tanto. Eles são mais complexos? Faltam informações no formulário inicial?

   \
2. **Revisar o Processo de Triagem:** Implementar uma rotina diária (ou mais frequente) de triagem focada especificamente em analisar e mover os tickets P1 e P2 da "Caixa de Entrada", evitando que fiquem parados.

   \
3. **Definir SLOs Claros para Priorização:** 

   **SLO (Service Level Objective - Objetivo de Nível de Serviço)**

   Garantir que 99% dos card sejam priorizados dentro de:
   * **P0:** < 1 horas
   * **P1:** < 3 horas
   * **P2:** < 24 horas

     \
4. **Monitorar a Métrica Semanalmente:** Criar um Dashboard Semanal no Pipefy
5. Medir o SLA ate a conclusão


Dados obtidos da semana 19/08 ate 26/08, considerando cards "concluídos"

| P1-High | 45.00762929060185183148 |
|----|----|
| P2-Medium | 55.1742275147863248 |

Houve uma **melhora expressiva** no tempo médio para priorização de tickets P1 e P2 nos últimos 7 dias. As ações focadas em agilizar a triagem inicial surtiram um efeito notável, reduzindo o tempo de espera em mais de 30% para ambas as categorias.

**Tabela Comparativa de Desempenho:**

| **Prioridade** | **Tempo Anterior (h)** | **Tempo Atual (h)** | **Redução (h)** | **Melhoria Percentual** |
|----|----|----|----|----|
| **P1 - Alta** | 64.0 | **45.0** | -19.0 horas | **↓ 30%** |
| **P2 - Média** | 85.6 | **55.2** | -30.4 horas | **↓ 35%** |


# Suporte Sapron


\
# Suporte Website