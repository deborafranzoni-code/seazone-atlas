<!-- title: Documentação do Usuário | url: https://outline.seazone.com.br/doc/documentacao-do-usuario-AwDR1XD2yr | area: Tecnologia -->

# Documentação do Usuário

# Introdução

Este documento tem como objetivo orientar o uso do **BI de Auditoria do MAPE**, desenvolvido com objetivo de tornar a auditoria ágil das variações do MAPE de faturamento, identificando ofensores por granularidade, decomposição de erro e impacto por imóvel.

Link do dashboard: <https://lookerstudio.google.com/reporting/59bed237-fbc1-4006-81e3-50fc8964ba93/page/x0SkF>

# Estrutura do Dashboard

O dashboard é composto por apenas uma página que foi dividida em cinco seções:


1. KPIs Macro
2. Alertas de Granularidade
3. Decomposição do Erro
4. Gráficos Temporais de Ocupação, Bloqueio e Concordância de Modelos
5. Tabela com Top Imóveis Impactadores\n

## Seção 1: KPIs Macro

Essa seção tem como objetivo mostrar os principais KPIs do MAPE em que é possível comparar um período antes (Intervalo A) com um período depois (Intervalo B).

### Período

 ![](/api/attachments.redirect?id=9ad57bba-fdc2-450f-9adf-8de13b4be15c " =1222x141")

Os períodos variam de 0 a 60 dias, ou seja, variam entre o intervalo de tempo que possuímos dados do MAPE. Portanto, caso você queira comparar os dados do MAPE de 30 dias com o de 15 dias, basta selecionar **30 no período A** e **15 no período B**. Os KPIs variam de acordo com esse filtro.

### KPIS

 ![](/api/attachments.redirect?id=8741e9bf-abe8-4e96-bc74-a1fafd594e1c " =1228x433")

* **MAPE Global:** É o erro percentual absoluto médio de faturamento do imóvel. Ele representa a variação total entre o que foi previsto e o que foi realizado.
* **Dias com conflito:** Mede os dias que o modelo "alucinou", ou seja, modelo prevendo receita onde não há disponibilidade.
* **MAPE Bloqueios:** Mede o erro de previsão de bloqueios.
* **MAPE Ocupação:** Mede o erro de previsão de ocupação.
* **MAPE Preço Médio Ocupado:** Mede o erro do valor da diária ocupada.

  \

## Seção 2: Alertas de Granularidade

Essa seção tem como objetivo mostrar as granularidades que estão mais impactando o MAPE. Por exemplo, quais *estados* e *stratas* estão estourados no dia atual. 

 ![](/api/attachments.redirect?id=fefe5a60-c638-4705-a00a-0aa4f0ed2c9b " =1195x298")

* ==Obs: Os valores mostrados são para o dia ATUAL, ou seja, o que está estourando o MAPE no dia atual.==


## Seção 3: Decomposição do Erro

Essa seção visa responder "De quem é a culpa do erro?". Portanto, é feito um gráfico de rosca que demonstra se o erro subiu por causa de bloqueio, preço ou ocupação. É usado o MAPE de 15 dias.

 ![](/api/attachments.redirect?id=c34fb5d3-b0cf-4c1d-ab88-a0162382efee " =1200x398") 


\
## Seção 4: Gráficos Temporais de Ocupação, Bloqueio e Concordância de Modelos

Essa seção possui três gráficos que mostram os dados **previstos vs real** dos últimos 15 dias sobre ocupação, bloqueio e a concordância entre os modelos usados para bloqueio.

### Ocupação:

* É calculado a taxa de ocupação por dia.

 ![](/api/attachments.redirect?id=3393ca8f-790f-4310-8473-1d77c0e78ccd " =1175x455")

### Bloqueio:

* É calculado a quantidade de bloqueios ocorridos no dia.

 ![](/api/attachments.redirect?id=2408486e-6b3e-4898-a135-b467e95f7b80 " =1166x444")

### Concordância entre fontes de detecção de bloqueios:

* Atualmente existem 3 principais formas de detectar bloqueios: modelo de XGBoost, modelo de NN e diversas heurísticas. Esse gráfico demonstra a quantidade de bloqueios realizadas por cada modelo.

 ![](/api/attachments.redirect?id=ad76fc3e-0a2b-4404-99cd-81ea2d581c4e " =1179x451")

* ==Obs.: O heurístico está muito maior que os outros pois é a soma de 8 modelos heurísticos distintos.==

  \

## Seção 5: Top Imóveis Impactadores

Essa seção possui uma tabela que ordena pelo valor do MAPE (no dia atual) os imóveis que estão mais impactando o MAPE. Além disso, mostra qual o principal fator que está influenciando o erro e o link do imóvel no airbnb. A tabela mostra os 10 principais imóveis.

 ![](/api/attachments.redirect?id=6ca8da4f-900a-4dfa-8a29-31d60c3ea073 " =1206x402")