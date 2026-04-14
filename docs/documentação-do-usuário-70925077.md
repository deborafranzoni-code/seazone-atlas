<!-- title: Documentação do Usuário | url: https://outline.seazone.com.br/doc/documentacao-do-usuario-7aOwfYISbK | area: Tecnologia -->

# Documentação do Usuário

## **Guia do Usuário: Alertas Inteligentes de Anomalia de Preços**

Para ajudar na nossa estratégia de precificação e garantir que estamos sempre um passo à frente, desenvolvemos um assistente automático que monitora os preços dos nossos imóveis 24/7. O objetivo dele é simples: encontrar oportunidades de melhoria e nos alertar sobre possíveis desalinhamentos com o mercado.

Este guia explica os alertas que você receberá e como interpretá-los para tomar as melhores decisões.


### **Como e Quando os Alertas são Enviados?**

Todos os dias, pontualmente às **9h da manhã**, nosso sistema enviará uma mensagem automática para o canal de Slack:

**#data-alerts-rm-precos-anomalos**

Cada mensagem conterá um resumo e um arquivo em formato .csv com os detalhes das anomalias encontradas. Existem dois tipos de alertas que você pode receber:


### **Alerta 1: Preços ALTOS para Datas PRÓXIMAS (Risco de Vaga Ociosa)**

* **O que significa?** Este alerta aponta imóveis que, para os próximos 14 dias, estão com um preço visivelmente mais alto que o da concorrência. Quando isso acontece, corremos o risco de "espantar" clientes em busca de uma reserva de última hora, o que pode levar a diárias não vendidas.
* **Qual é a ação recomendada?** Abra o arquivo CSV anexado (high_price_earlier.csv), verifique os imóveis e os preços dos concorrentes listados. Considere fazer um ajuste no preço para baixo para tornar a propriedade mais atrativa e aumentar as chances de garantir aquela reserva de última hora.

### **Alerta 2: Preços BAIXOS para Datas DISTANTES (Risco de Perda de Receita)**

* **O que significa?** Aqui, o sistema identifica imóveis que, para datas futuras (de 1 a 6 meses à frente), estão com preços muito baixos, especialmente para períodos de alta demanda como feriados ou férias. Isso pode significar que estamos "vendendo barato" demais e com muita antecedência, perdendo a chance de maximizar nosso lucro.
* **Qual é a ação recomendada?** Analise a lista de imóveis no arquivo CSV (low_price_late.csv). Avalie os períodos e, se fizer sentido para a estratégia, considere aumentar o preço para aproveitar melhor a alta demanda esperada para essas datas no futuro

### **[Planilha de Preços Anomalos](https://docs.google.com/spreadsheets/d/15aVijlOSPIk9CpoYn2Aslzr6RTpQryInboBBeSTB-LM/edit?gid=2010477181#gid=2010477181)**

A planilha auxilia no processo de verificação se os preços são de fato anomalias ou falsos positivos.