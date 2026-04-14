<!-- title: Análise de Desempenho | url: https://outline.seazone.com.br/doc/analise-de-desempenho-fG8O5HPECB | area: Tecnologia -->

# Análise de Desempenho

A análise de desempenho se encontra dentro do repositório de precificação. Isso acontece porque por enquanto esse é um modulo pequeno e não compensaria criar um repositório especifico para ele e, visto que a precificação também utiliza a análise de desempenho, faz todo sentido os dois ficarem juntos.

Github: <https://github.com/Khanto-Tecnologia/sirius-precificacao>

A análise de desempenho consiste em, dado um período, avaliar se os nossos imóveis estão com o faturamento dentro do esperado em relação aos seus competitors_all_strata (concorrentes filtrados por cidade, bairro, tipo e quartos). Se o imóvel sendo analisado é um SUP, essa analise mostra se ele está realmente faturamento como um SUP.

# **PerformanceAnalysis**

A análise de desempenho é feita através de um único StepFunction que contem dois lambdas e uma fila.

 ![Untitled](Ana%CC%81lise%20de%20Desempenho%2052c107ca35f74eceae1b8058b155861f/Untitled.png)


\
**Trigger:** O Trigger do StepFunction é feito de forma manual (botão) através do endpoint [post → performance/analysis](/doc/comunicacao-e-dados-aWFByTFvPo) que é ativado dentro da própria planilha. O endpoint recebe o Arn do StepFunction a ser triggado e também os parâmetros que serão utilizados.

Os parâmetros são uma lista de dicionários (JSONs), onde cada dicionário possuí os parametros start_date, end_date, label e percentile_list.

O percentile_list está hardcoded no AppScript, mas os outros dependem do input do usuário nas respectivas células da Planilha.

<aside> 💡 O percentile_list deve conter TODOS os intervalos de mínimo e máximo faturamento contidos na Planilha de Setup, durante a seleção de concorrentes.

</aside>

Isso é necessário porque se não conter o LambdaPerformanceSaveAnalysis não terá como saber quais os limites inferior e superior da Strata sendo analisada.

## LambdaPerformanceGetQuantiles

Esse lambda é utilizado não só dentro da analise de desempenho, mas também na precificação por concorrentes. Esse é o lambda principal que faz as queries na análise de desempenho. Ele recebe de parâmetro uma **start_date** e **end_date** (esse é o período sendo analisado, esses campos são string no formato YYYY-MM-DD), **period_label**  (nome pro período, também string, esse nome é usado depois como identificador na planilha) e **percentile_list** (lista de floats, são os percentis que a analise quer encontrar).

O lambda pega os dados de faturamento dos imóveis da Seazone através da daily_revenue e soma a coluna price_after_discount para o período sendo analisado. Ele também realiza uma query na BAO onde é feito um join com a tabela de competitors_all_strata e é somado a informação de faturamento dos concorrentes pra depois calcular os percentis. Utiliza-se a coluna price_after_discount para comparar com o faturamento do Airbnb pois ao multiplicar pelo aumento de preço no Airbnb, as duas informações ficam equivalentes. Ou seja, o faturamento na analise de desempenho é a soma do preço das diárias caso ocupadas.

**MAP**

Esse lambda foi feito pra ser triggado por um MAP, visto que ele calcula a analise de desempenho para apenas um período por vez, mas a analise normalmente é feita para múltiplos períodos.

**Output**

O output do lambda é, para cada lambda triggado pelo MAP, um append na tabela temporária bucketperformanceanalysis/performance_quantiles_temp/ .

O objetivo é salvar uma tabela com os percentis calculados da analise de desempenho pra depois formatar os resultados num lambda posterior. O caminho onde os dados foram salvos é retornado no lambda.

## LambdaPerformanceSaveAnalysis

Esse lambda irá ler todos os caminhos no S3 retornados pelo Lambda/MAP anterior e irá os formatar para para depois serem inseridos na planilha da analise de desempenho.

Passos:


1. Ler os parquets salvos pelo "LambdaPerformanceGetQuantiles".
2. Ler a aquisição mais recente da tabela "bucketsheetscommunication/inputs/competitors", sendo que é utilizado o parameter store pra saber qual o nome do "bucketsheetscommunication". Essa tabela é necessária pra saber qual coluna de percentil usar para o limite superior e inferior do imóvel sendo analisado, visto que esse limite muda dependendo da strata do imóvel.
3. Analisar se o faturamento do imóvel está acima ou abaixo do esperado.
4. Analisar se o imóvel para aqueles períodos possuí regra de preço mínimo ou fixo e, caso possua, retorna a maior regra.
5. Se tudo der certo o resultado é salvo na tabela "bucketperformanceanalysis/performance_analysis" e o caminho do parquet é enviado para a fila "SQSQueuePerformanceAnalysis".

**Output:**

Append na tabela "bucketperformanceanalysis/performance_analysis/state=historic" e overwrite na tabela "bucketperformanceanalysis/performance_analysis/state=current", além disso o path é enviado para a fila "SQSQueuePerformanceAnalysis".

## **SQSQueuePerformanceAnalysis**

Essa fila é utilizada em conjunto com o Lambda do endpoint [get → performance/analysis](/doc/comunicacao-e-dados-aWFByTFvPo). O lambda lê a fila e retorna o resultado em formato JSON para o AppScript da planilha da analise de desempenho. Ele também deleta a mensagem da fila.

A lógica do AppScript é, depois de clicar no script que começa a análise de desempenho, o script entra num loop onde ele chama o Lambda a cada 30 segundos, se não existir mensagem na fila o lambda retorna 202 e é agurdado mais 30 segundos, caso exista mensagem na fila o Lambda retorna 200 e o loop termina. Caso o loop demore muito tempo pra retornar 200 então é levantado um erro no próprio AppScript.