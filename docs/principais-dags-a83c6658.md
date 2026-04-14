<!-- title: Principais DAGs | url: https://outline.seazone.com.br/doc/principais-dags-GMEEbU4AWo | area: Tecnologia -->

# Principais DAGs

Link da documentação com as DAGs no Miro: <https://miro.com/app/board/uXjVLUoS9nE=/>


* **DAG - SETUP**

  A planilha de SETUP possui uma aba muito importante que é a aba "Grupos".

 ![](/api/attachments.redirect?id=2fde9f6d-b20f-40d0-a865-eb31b23ec6bf " =406.5x253.5")

Nessa aba tem 4 botões. O primeiro deles é responsável por dar início a execução de um fluxo que tem como objetivo o armazenamento de dados presentes em diversas abas da planilha de SETUP em buckets no S3.  

A imagem abaixo, com um recorte da DAG SETUP, ilustra esse fluxo, onde após o botão ser clicado, ele vai executar o appscript da planilha, que por sua vez terá códigos contendo um request para o endpoint, ativando ele. Cada endpoint irá ativar uma função lambda, e esse lambda irá fazer uma cópia do conteúdo da aba e salvar o conteúdo no bucket s3. 

 ![](/api/attachments.redirect?id=d74a5e3b-aae6-4f73-b7f1-f53dca59b7f4 " =1488x71")

Dentre as funções lambdas, a função "SetupGroupsMakeDiff" é a única que além de fazer uma cópia do conteúdo e salvar ele no bucket S3, ela também retorna dados para a aba "Warning Groups" da planilha. Nessa aba constará quais imóveis estão faltando na aba grupos e quais imóveis que estão na aba grupos mas estão sobrando (que podem ser imóveis inativados, por exemplo). A imagem abaixo ilustra isso.

Uma observação importante é que os endpoints não são ativados de forma paralela. Esse processo acontece de forma sequencial. Na DAG completa, que está no Miro, é mostrada toda essa sequência que começa a partir da ativação do endpoint setup-groups/make-diff, que é mostrado na imagem abaixo.

Outro ponto é que a maioria das funções lambdas irão ler o bucket da "SetupGroupsMakeDiff", e isso está ilustrado pela seta laranja. Nas DAGs, sempre que há uma seta laranja, significa que se trata de obtenção de dados.\n

 ![](/api/attachments.redirect?id=04419372-99ba-4fda-a3b5-bdd272395b6a " =513x245")Aqui está um recorte um pouco maior de como está a estrutura da DAG em relação ao primeiro botão da aba de "Grupos".

 ![](/api/attachments.redirect?id=fa9502f2-f139-4f9f-aa48-3a1666e92814 " =760.5x331.5")O segundo e terceiro botão estão relacionados com a seleção de concorrentes, onde o segundo botão tem o objetivo de atualizar os polígonos e o terceiro botão tem o objetivo de enviar os concorrentes já selecionados e presentes na aba "Concorrentes por ID", da planilha de SETUP, para a tabela "competitors_plus". Como temos uma DAG específica para concorrentes, na DAG de SETUP, esses dois botões aparecem, mas neles tem um link que redirecionará para a DAG Concorrentes, como mostrado na imagem abaixo.

 ![](/api/attachments.redirect?id=1d3da712-d9db-487f-9512-4d817aa7e3de " =262x222")E por último, temos o quarto botão dessa aba "Grupos", o qual está relacionado com a parte de sazonalidade, regrasAGC, AGC - categoria e AGC - imóvel. Quanto às duas primeiras partes, o fluxo é acontecer o salvamento de dados em buckets S3.

 ![](/api/attachments.redirect?id=b1347fe8-7d64-4182-b41f-2110072bd7f7 " =398.5x148.5")

Já na parte de AGC - categoria e AGC - imóvel, há uma stepfunction que realiza a leitura de buckets, realiza o salvamento de dados em buckets e envia uma mensagem para a fila de mensagens SQS. Há também uma função lambda que consulta esta fila e reage a mensagem contida nela.

 ![](/api/attachments.redirect?id=e71af97a-982a-4e76-84f7-3760a6a75851 " =460x347")

* **DAG - CONCORRENTES**

Nos botões relacionados aos concorrentes, os quais se encontram na aba de grupos da planilha de SETUP, o primeiro deles está relacionado a atualização de polígonos. Há uma stepfunction na qual é feito o salvamento de dados em buckets e que também está relacionada a dados dos polígonos, os quais podem ser visualizados no Google Maps.

Exemplo de polígonos:

 ![](/api/attachments.redirect?id=97f059dd-ac56-43ed-ad1b-b8c555a463d9 " =920.5x432.5")

No fluxo gerado por esse botão também há um lambda que verifica uma mensagem na fila SQS e atualiza os dados na aba "**Conc﻿orrentes Sirius"** e "**Conc﻿orrentes Sem Strata"** da planilha de Rm_concorrentes, e a aba "**Conc﻿orrentes por ID"** da planilha de SETUP.

 ![](/api/attachments.redirect?id=f4ef4d2e-adba-4881-a52c-a1f038ce5ece " =568x308")Já o segundo botão se trata de atualizar concorrentes. Nessa etapa também há uma stepfunction a qual faz o salvamento de dados em buckets, também é gerada uma mensagem para fila SQS, e há um lambda que lê dados do bucket "Competitors_Plus" e atualizada a aba "Warnings_concorrentes" na planilha de SETUP.

 ![](/api/attachments.redirect?id=15b855fd-d31f-446c-8776-1f4e7a8f094d " =615.5x234")

* **DAG - AGC**

No botão **Análi﻿se por Imóvel,** há uma stepfunction que lê dados de buckets, envia uma mensagem SQS, e há um lambda que pega os resultados e passa os dados para formato JSON e CSV e fornece um link para download desses arquivos. O mesmo sistema acontece para o botão de **Análi﻿se por categoria.**

Exemplo do fluxo para o botão **Análi﻿se por Imóvel:**

 ![leitura aos buckets](/api/attachments.redirect?id=c0352bee-4e58-49f5-93fe-bbd04f40bafd " =263x293.5") ![lambda e formatação dos dados para json e csv](/api/attachments.redirect?id=830cc70c-14b2-4ca6-ac31-1ec581db8110 " =519x291")Nessa planilha também há um menu que oferece as opções de enviar preços por categoria e enviar preços por imóvel.

 ![menu de opções](/api/attachments.redirect?id=45274ed2-77ff-4bae-9521-fe2c044d54ff " =181.5x108.5")

O fluxo do botão de enviar preços por categoria envolve um lambda que realiza leitura de buckets, atualização da aba desconto na planilha de SETUP e o envio de preços para a Stays. Já o botão de enviar preços por imóvel está relacionado com o envio dos preços para a Stays.

* ![](/api/attachments.redirect?id=691258b0-a756-4905-b298-66503fb6883c " =568x300.5")**DAG - Precificação de concorrentes**

  Na aba Preços há o botão Trazer Grupo/Imóvel que possui um lambda relacionado que lê dados de buckets e gera um json e um link para baixar os arquivos na SETUP groups.

  ![](/api/attachments.redirect?id=98191c73-dd0b-483d-8d76-a0a64cd78045 " =553.5x288")

Também há o botão Enviar Preços, que possui um lambda relacionado que salva dados no bucket, um lambda que envia uma mensagem SNS e outro lambda que consulta essa mensagem.

 ![](/api/attachments.redirect?id=928720ca-b4e3-440c-9ec2-ed8f909ee6a3 " =686x234")Há também a aba Preços Categoria, que possui o botão Trazer Grupo, o qual gera novas datas para serem preenchidas de acordo com o intervalo da coluna "Janela de dias".

 ![](/api/attachments.redirect?id=b7b2988e-d73e-407c-ad9f-ddaa97ef4aea " =373x98.5")O botão de Enviar Preços da aba Preços Categoria segue a mesma estrutura de fluxos que o botão Enviar Preços da aba Preços.