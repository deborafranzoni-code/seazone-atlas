<!-- title: Análise de Anomalias em Preço dos Imóveis | url: https://outline.seazone.com.br/doc/analise-de-anomalias-em-preco-dos-imoveis-lOh3gt25CP | area: Tecnologia -->

# Análise de Anomalias em Preço dos Imóveis

Link do épico no jira é: **[Detecção de Anomalias de Faturamento 1 - Preços Anomalos](https://seazone.atlassian.net/browse/DS-485)**

Link do canal criado no Slack: [data-alerts-anomalias-lake](https://seazone-fund.slack.com/archives/C094D7W3JSW)

Link do processo DataOps: 

# Explicação dos Alertas

Essa seção tem o foco de explicar em detalhes os alertas que estão indo pro Slack.

## MAPE Mudança de Preço PriceAV

Este aviso compara a aquisição de preço de **hoje** com a **última**. Normalmente, o preço dos anúncios do **Airbnb não muda**, então esse aviso calcula o MAPE da última aquisição com a de hoje, esse valor normalmente fica em torno de 1%, se subir para acima de 3% isso significa um possível problema nos scrappers e alguém precisa verificar os dados.

 ![](/api/attachments.redirect?id=f1760a5f-e5e7-4fbb-a3f4-af6111cd7bdf " =411x184")**Regras e Filtros:**

* **Aquisição de Hoje:** Todas as diárias com tag 'price_correct' da price_av de hoje.
* **Última Aquisição:** Última aquisição com tag 'price_correct' da price_av dentre 5 dias atrás e ontem.
* **Erro Percentual Absoluto:** Dentre as datas presentes nas duas aquisição acima, é calculado o erro percentual absoluto - abs(preço_hj  - último_preço)/último_preço

**Alerta:**

* **Nº Diárias**: Número de diárias consideradas no Warning.
* **Nº Diárias Diferentes**: Número de diárias que o preço mudou da última aquisição para hoje.
* **Média**: Média do MAPE (um valor próximo de 1% está okey)
* **P50**: P50 do MAPE (um valor de 0% está okey)
* **P75**: P75 do MAPE (um valor próximo de 0% está okey)
* **P90**: P90 do MAPE (um valor de até uns 3% está okey)

## **Anomalias nas Aquisições de Preço**

Este aviso conta o número de diárias que deveríamos estar scrappando dentre hoje e 180 dias no futuro, mas que por algum motivo não estamos scrappando. Se esse número de diárias ficar grande significa um possível problema nos scrappers e alguém precisa verificar os dados.

 ![](/api/attachments.redirect?id=1b295adb-ab30-493e-b9cf-b4dc55381a35 " =374x165")

A tabela **lake_anomalies.anomaly_price_antecedence** da conta PRD-Lake mostra todas as diárias não scrappadas.

 ![](/api/attachments.redirect?id=d14d97de-9ff0-4cec-b662-fb0678078d89 " =486x164")

**Regras e Filtros:**

* **Lista de IDs:** Imóveis Seazone, concorrentes ou imóveis com review >= 10 (mesma lista de ids que os scrappers usam)
* **Intervalo:** Todas as diárias da daily_fat dentre ontem e 175 dias no futuro.
  * Como a daily_fat roda praticamente 1 dia depois de scrapparmos o preço é por isso que também é utilizado ontem
  * Como os imóveis concorrentes são scrappados 180 dias de 5 em 5 dias é utilizadfo 175 dias como o máximo da janela do futuro, apenas para garantir que todas as datas do intervalo precisam estar sendo scrappadas.
* **Diárias não Scrappadas:** Datas consecutivas que estão disponíveis e são maiores que a min_stay, mas que nunca scrappamos ou faz mais de 7 dias que scrappamos. Também é filtrado bloqueios.
* **Total de diárias:** Número de diárias do intervalo daquela lista de ids. Não é feito nenhum outro filtro.

**Possíveis problemas:**

* Não está sendo considerando bloqueios de checkin/checkout. As vezes pode acontecer do imóvel ter esse bloqueio e ser impossível scrapparmos a data, como não está sendo levado em conta os números reais que devíamos estar scrappando serão menor que o número apresentado no aviso.
* Os imóveis do airbnb_price a gente scrapa 1 ano deles, por enquanto não estamos levando isso em consideração, é pego apenas até 175 dias no futuro, então os dias que não scrappamos é um pouco maior do que aquele que o aviso aponta.
* Tem alguns imóveis que morreram, mas ainda não morreram na details (o que também reduziria o número real de linhas que não scrappamos corretamente)

**Alerta:**

* **Nº Diárias Não Scrappadas**: Número de diárias não scrappadas.
* **Nº de IDs**: Número de ids que tiveram pelo menos 1 diárias não scrappada.
* **Nº Diárias Não Scrappadas Por ID**:  É calculado os percentils de diárias não scrappadas por ID.