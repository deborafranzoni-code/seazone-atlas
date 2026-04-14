<!-- title: Supervisório | url: https://outline.seazone.com.br/doc/supervisorio-g8UuuAzvTg | area: Tecnologia -->

# Supervisório

O módulo Supervisório se encontra no repositório <https://github.com/Khanto-Tecnologia/sirius-supervisorio> e sua planilha correspondente de input e output em produção é <https://docs.google.com/spreadsheets/d/1suOzWghNtpIodt19mv5xBTSz1aDJbMvr5pj80Tz-B_s/edit#gid=0>.

Este módulo consiste em mostrar para o operador de RM quais datas de quais imóveis seazone estão com preços muito acima ou muito abaixo com relação a seus concorrentes. Esta comparação é feita usando threshold dos percentis de cada listing-data dos concorrentes: usuário entra como input os percentis de threshold e um range de datas e na planilha de output são retornados os listings-data seazone que estão acima ou abaixo dos percentis de threshold e dentro do range de datas selecionado.

# Superviory

O processo supervisório é feito em duas etapas: primeiro faz-se o processamento dos dados necessários e salva-se o arquivo no S3. Enquanto isso, existe um lambda que fica verificando quando o processamento dos dados terminou, ou seja, quando o arquivo foi escrito no S3. Definimos isso como o método "post" e "get" do supervisório, respectivamente. Abaixo ilustra-se o StepFunction que implementa o método "post":

 ![Untitled](Superviso%CC%81rio%208bf83396631947bab542e5ba0c3d8be4/Untitled.png)

**Trigger:** O Trigger do StepFunction é feito de forma manual (botão) através do endpoint [post → /supervisory](/doc/comunicacao-e-dados-aWFByTFvPo) que é ativado dentro da própria planilha. O endpoint recebe o Arn do StepFunction a ser triggado e também os parametros que serão utilizados.

Os parâmetros são os percentis inferior e superior, o range de datas e os percentis das colunas de output:

 ![Untitled](Superviso%CC%81rio%208bf83396631947bab542e5ba0c3d8be4/Untitled%201.png)

As colunas de percentil de output estão hardcodadas no AppScript e os percentis e range de datas são input do usuário.

## LambdaSupervisory

Este lambda é o que de fato faz o processamento dos dados. Ele recebe cada um dos parâmetros passados de percentis e datas e faz uma sequência de subqueries para pegar as informações de todos os listings seazone e seus concorrentes e calcular os percentis de preço para cada data-listing seazone. Os preços são pegos da tabela block_and_occupancy do pipe e os listing ids das tabelas competitors_general e brlink_seazone_clean_data.seazone_listings.

**Output**

O resultado é escrito de forma append no S3 no formato parquet no bucket supervisorio-bucketsupervisory/price_supervisory e no formato json no bucket supervisorio-bucketsupervisory/output/price_supervisory. O PATH do S3 do resultado escrito no formato json é retornado pelo lambda.

## SQSQueueSupervisory

Esta queue recebe como mensagem o PATH retornado pelo [LambdaSupervisory](/doc/supervisorio-KtPSAV5Or1). A utilidade dela é simplesmente receber esta mensagem para que a método "get" do supervisório possa consumir e baixar para a planilha o json correspondente ao PATH.

## **LambdaSupervisoryGet**

Este lambda serve como consumidor das mensagens da [SQSQueueSupervisory](/doc/supervisorio-KtPSAV5Or1). No AppScript, o método post e get são feitos assincronamente. Enquanto o post trigga o StepFunction [Superviory](/doc/supervisorio-KtPSAV5Or1), o método get trigga este lambda para consumir a mensagem da fila.

Se não houver mensagem, o trigger é refeito a cada 20 segundos, até no máximo 160 segundos. Quando houver mensagem na fila, o lambda consome e envia para o AppScript uma url assinada do arquivo json cujo path do S3 veio da mensagem. No AppScript será feito o download do arquivo json para a planilha.