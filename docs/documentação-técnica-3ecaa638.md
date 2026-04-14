<!-- title: Documentação Técnica | url: https://outline.seazone.com.br/doc/documentacao-tecnica-P7lTjQK4d8 | area: Tecnologia -->

# 🛠️ Documentação Técnica

Link do Miro: [System Price](https://miro.com/app/board/uXjVJdpcRWU=/)

Link dos Githubs:

* [seazone-tech/api-stays](https://github.com/seazone-tech/api-stays)
* [seazone-tech/sirius-precificacao](https://github.com/seazone-tech/sirius-precificacao)
* [seazone-tech/sirius-supervisorio](https://github.com/seazone-tech/sirius-supervisorio)
* [seazone-tech/gcp-data-resources](https://github.com/seazone-tech/gcp-data-resources)

Os scripts da **GCP não possuem CI/CD,** eles ficam no github apenas para versionamento.

# Infraestrutura do backtesting

Links:

* Video: [Link](https://drive.google.com/file/d/1BLGZkp9chousMQ4LaKyk9M1wYRKR6Luo/view)
* Transcrição: [Link](https://docs.google.com/document/d/1bYUMGeWkbjVRxBP09hMz_QMTOFxlSaYWg5mMZbxdt7Y/edit?tab=t.0#heading=h.dfszkrswy1og)
* Link da Planilha: [System Price - Planilha](https://docs.google.com/spreadsheets/d/1GMQ8MxohgnuyTsXz3eU-Q7QLAWWc_spNi8P61PHRM40/edit?gid=1485299539#gid=1485299539)
* Looker: [System Price - Looker](https://lookerstudio.google.com/u/0/reporting/6918af03-23b8-4f14-af57-ea4c5547b1e0/page/VW0SF)

## Dados Competidores

Uma vez por dia os script são executados e pegamos os concorrentes que temos HJ no Sirius.

Esses concorrentes são adicionados numa tabela histórica para termos dados de TODAS as aquisições e com isso, conseguimos simular o backtesting do system price para todas as aquisições.

**Problema:**

* Como o script começou a rodar recentemente, só temos dados completos a partir de 2025-07-17.
* Para datas dentre 2024-12-05 até 2025-07-16 a tabela foi preenchida com dados que tinhamos da auditória da Meta 1.0, mas esses dados só possuem dentre 50-90 dias da data de aquisição (dependendo de quando a meta rodou).
* Para datas anteriores a 2024-12-05, NÃO TEMOS DADOS.

Depois de adicionar esses dados históricos, é executado uma query que pega eles e os organiza numa tabela por categoria já deixado o dado pré-processado, o que acelera a execução do backtest.

 ![](/api/attachments.redirect?id=818fed91-0fe1-4de2-8a0c-e73d275a1ab1)

## Dados de Preço Seazone

Os dados de preço de imóveis da Seazone são usados como "verdade" na hora de cálcular os erros. Eles são obtidos através da tabela de preços históricos enviados por categoria que temos na AWS.

Foi utilizado um transfer job do BigQuery para gerar essa tabela

 ![](/api/attachments.redirect?id=ef8c62b0-6ecb-4abe-b1b1-9123065f1e08)

## Execução do BackTest

Na planliha o request é iniciado e o script puxa os dados de diversas tabelas que são usados no cálculo do SystemPrice, como tabelas de Sazonalidade, Clima e Feriados.

**Problema dos Feriados:** A útlima versão da tabela que temos dos feriados (que é a usada no cálculo do System Price) possuí apenas a aquisição de hj, então nela não existe feriados criados no ano passado, por exemplo, mas para uma execução correta do SystemPrice a gente precisa dos feriados presentes no MOMENTO da precificação/acquisição.

**Solução:** Criar tabela old_holidays.

* A lógica é pegar a primeira e a décima quinta aquisição de cada mês da tabela de feriados dentre o ano passado e hj e implementar isso na lógica do backtesting.
* O motivo de serem apenas essas 2 aquisições por mês é para não deixar o script lento e para conservar memória do cloud function. No mundo perfeito seriam TODAS as aquisições e, assim, saberiamos com precisão máxima quais datas estavam sendo consideradas como feriados/eventos.

O script em si precisa também precisa fazer todas as consultas e ler de multiplas tabelas em um tempo bom, então o cloud function foi configurado para ter 8 CPUs e ele lê as diversas tabelas em multithread.


 ![](/api/attachments.redirect?id=bf75ed56-6c9f-4cc1-92c1-5d075e2c439a)

# Infraestrutura da Precificação do SystemPrice

Links:

* Vídeo Parte1: [Link](https://drive.google.com/file/d/1y6tiY9iq3xwpO3OGGGfOIPCdNdaCmMAm/view)
* Vídeo Parte2: [Link](https://drive.google.com/file/d/1QwPNNxlgI1ygorB8054nw4WOVYbeG1HO/view)
* Looker: [Dashboard de Acompanhamento - Teste A/B System Price](https://lookerstudio.google.com/u/0/reporting/2106bfe5-6915-459b-b6bb-ff2dd280e856/page/p_fxfkf4agvd/edit)

## Calculo do System Price

O cálculo em si do System Price não foi modificado.

A forma que sempre existiu é que temos um StepFunction ([link github](https://github.com/seazone-tech/sirius-supervisorio/blob/dev/supervisory/statemachine/general_competitors_analysis_category_find_periods.asl.json)) que roda de 3 em 3 horas (trigger na própria planilha) que calcula os dados que vão para a planilha de precificação (AGC), sendo que um desses dados calculados é o SystemPrice.

O StepFunction é responsável por calcular esses dados na granularidade diária, por periodo e por periodo agrupado no mês. Cada um desses tipos são representados pelos lambdas que rodam em paralelo na figura.

A única modificação realizada foi fazer com que, após a execução da AGC por dia, enviar uma mensagem num tópico SNS que starta a precificação do System Price.

**Possível Problema:** Esses dados são calculados para datas dentre hoje e 8 meses no futuro, então se tentarem precifcar com o System Price uma data após esse intervalo, então essas datas não funcionaram e irão pro Warning.

 ![](/api/attachments.redirect?id=01c86e97-6e6b-4f9d-9e24-e42e3e135cf2)

 ![](/api/attachments.redirect?id=e3dc1991-06a5-4901-a9e3-96f5153eedfd)

## Lógica Precificação

Quando o Lambda ([link github](https://github.com/seazone-tech/sirius-precificacao/blob/dev/pricing/system_price/lambda_function.py)) roda, ele faz 5 coisas:


1. Ele pega os períodos que serão permitidos a precificação do System Price (definido na planilha)
2. Ele lê o System Price calculado no lambda da AGC diário e fica com as datas permitidas no período.
3. Ele compara se esses preços já foram enviados HJ, se pelo menos um preço do imóvel ainda não foi enviado HJ, então ele reprecifica todas as diárias desse imóvel. Essa verificação é feita para evitar do script ficar reprecificando datas já precificadas pelo System Price.
4. Ele lê os preços que os analistas estão enviado para imóveis daquela categoria e gera um limite inferior e superior (25% do preço médio da categoria), caso o system price esteja acima ou abaixo desse limite, então ele limita o valor para o próprio limite e envia alertas no Slack.
5. Os dados são salvos na tabela system_price_full e o caminho do arquivo parquet é enviado para o script de precificação com a tag `system_price - v1`

 ![](/api/attachments.redirect?id=0a5ad002-dd3d-43af-bd34-3bae24e7f8bb)

No script de precificação ([link github](https://github.com/seazone-tech/sirius-precificacao/blob/dev/pricing/apply_setup_rules/lambda_function.py)) não foram realizadas muitas mudanças, mas a lógica é:

* Caso o script esteja recebendo um arquivo com tag system_price, então ele não irá preficar datas fora do periodo permitido (isso é uma redundância, em teoria o script anterior já está garantido que apenas datas do periodo estão sendo precificadas)
* Caso o script esteja recebendo uma precificação de algum analista, então será REMOVIDA datas cadastradas na aba de períodos do system price.
* Se for um gapper (de 3 em 3 horas o Sirius reprecifica todas as datas), então nada é feito, o script só pega o último preço enviado para o imóvel e reprecifica essas diárias.

## Tabelas, KPIs e BI

Depois de precificados, os dados ficam salvos nas tabelas da AWS, entretanto, queremos levar isso pro Looker, então a abordagem escolhida foi puxar esses dados de 3 em 3 horas (o processo começa +/- 3h40) e colocar eles no BigQuery.

### **Tabelas**

* last_offered_raw_price_system_price
  * Usada no gráfico de Preços Enviados do Looker Studio.
  * A query dela está basicamente pegando o último preço que enviamod para cada imóvel e adicionando nessa tabela.
  * Imóveis onde o campo 'origin' não tem a tag "system-price" terão o preço NULO. 
  * Teoricamente, daria para gerar essa tabela apenas com a VIEW last_offered_raw_price, mas o bigquery não permite ler views do Athena, então por isso tive que ler de 2 tabelas e juntar o dado.
* last_offered_price_system_price
  * Usado no gráfico de Preços Stays no Looker Studio.
  * Mesma ideia da tabela last_offered_raw_price_system_price.
* daily_revenue_system_price
  * Usada na aba de Desempenho.
  * Ela usa a tabela last_offered_price_system_price para saber se um imóvel foi ou não usado para o system_price. Caso pelo menos 1 data tenha a TAG então a coluna is_system_price será True para todas as linhas desse imóvel.

 ![](/api/attachments.redirect?id=e1eb7398-4794-4fb0-abfd-c361f85125ec)

### BI

Não foi necessário fazer nada fora do comum para a abas preços, mas na aba Desempenho tem um detalhe.

Foi necessário puxar a daily_revenue 2 vezes para o Looker Studio

 ![](/api/attachments.redirect?id=108b74e5-500e-4156-8034-c28f66ee7e21)

O motivo disso foi que, ao filtrar o campo Imóvel, todos os imóveis do gráfico Ranking Detalhado sumiam (menos o imóvel selecionado), então esse gráfico utiliza a segunda daily_revenue_system_price para evitar esse problema.

Fiz com que o campo Imóvel filtrasse um "calculated field", dessa forma ele filtra todos os gráficos, menso o ranking detalhado, visto que a segunda daily_revenue não possuí esse "calculated field"

 ![](/api/attachments.redirect?id=f272770d-4c06-44b0-a667-cb245b980979)

### Como Adicionar o faturamento de datas precificadas com o System Price?

Bem, a tabela daily_revenue_sapron tem o dado de faturamento por imóvel/dia e tem a data de criação da reserva.

A tabela historical_raw_prices vai ter o histórico de TODOS os preços enviados, a partir do campo origin dá pra obter os preços com a tag '"system_price".

O script da daily_revenue_sapron já faz um join com a historical_raw_prices para pegar o dado do preço no MOMENTO de criação da reserva, então daria para puxar e criar uma coluna de tag como "is_reservation_system_price" ou algo assim e puxar isso no BI.