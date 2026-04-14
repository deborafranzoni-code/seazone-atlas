<!-- title: Processo DataOps | url: https://outline.seazone.com.br/doc/processo-dataops-hvXyxNUNuv | area: Tecnologia -->

# Processo DataOps

Para que nenhum incidente crítico seja perdido e a responsabilidade pela investigação seja formalmente atribuída e rastreada, foi estabelecido o processo abaixo para o time de Data Ops com a implementação de um mecanismo para monitorar os alertas do canal #data-alerts-anomalias-lake.

### Criação do Mecanismo:

\nFoi decidido manter o processo de criação de card manual, para evitar que cards sejam criados desnecessariamente. Porém, foi implementado um mecanismo para monitorar os alertas de preço.

Nesse [card](https://seazone.atlassian.net/browse/DOP-370 "https://seazone.atlassian.net/browse/DOP-370"), o Hideki definiu os critérios para gerar uma investigação:

Para o **MAPE Mudança de Preço PriceAV** ficou definido**:**

* Nº Diárias Diferentes > 30%
* Média de mudança de preço > 3%

Para o **Anomalias nas Aquisições de Preço** ficou definido:

* Nº Diárias Não Scrappadas > 5%
* Nº de IDs não scrapados > 30%

  \

Quando essas métricas apresentarem acima desses valores definidos, o time de Data Ops será marcado no slack, para investigar o ocorrido.

### Processo de criação do card:

Após o squad-data-ops ser marcado no canal, um membro do time deve verificar os valores acima do estabelecido e investigar o que ocorreu e criar um card no Jira e o título do ticket deve identificar claramente o tipo de alerta e a data (ex: "Anomalia de Preço - Diárias Não Scrappadas - 2025-07-17"). Além disso, a descrição do ticket deve ser pré-populada com todas as métricas e informações contidas no alerta original do Slack.