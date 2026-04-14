<!-- title: Principais DAGs | url: https://outline.seazone.com.br/doc/principais-dags-pRcvXR4cxy | area: Tecnologia -->

# Principais DAGs

Link da documentação com as DAGs no Miro: **<https://miro.com/app/board/uXjVLUoS9nE=/>**


* **DAG - SETUP**

  A planilha de SETUP possui uma aba muito importante que é a aba "Grupos".


 ![](https://outline.seazone.com.br/api/attachments.redirect?id=95fb5a4e-4bc5-4dc5-b0c6-3785a82605b4 " =406x")


Nessa aba tem 4 botões. O primeiro deles é responsável por dar início a execução de um fluxo que tem como objetivo o armazenamento de dados presentes em diversas abas da planilha de SETUP em buckets no S3.

A imagem abaixo, com um recorte da DAG SETUP, ilustra esse fluxo, onde após o botão ser clicado, ele vai executar o appscript da planilha, que por sua vez terá códigos contendo um request para o endpoint, ativando ele. Cada endpoint irá ativar uma função lambda, e esse lambda irá fazer uma cópia do conteúdo da aba e salvar o conteúdo no bucket s3.


 ![](https://outline.seazone.com.br/api/attachments.redirect?id=67772503-1935-4524-9c04-527aaed5c29f)


Dentre as funções lambdas, a função "SetupGroupsMakeDiff" é a única que além de fazer uma cópia do conteúdo e salvar ele no bucket S3, ela também retorna dados para a aba "Warning Groups" da planilha. Nessa aba constará quais imóveis estão faltando na aba grupos e quais imóveis que estão na aba grupos mas estão sobrando (que podem ser imóveis inativados, por exemplo). A imagem abaixo ilustra isso.

Uma observação importante é que os endpoints não são ativados de forma paralela. Esse processo acontece de forma sequencial. Na DAG completa, que está no Miro, é mostrada toda essa sequência que começa a partir da ativação do endpoint setup-groups/make-diff, que é mostrado na imagem abaixo.

Outro ponto é que a maioria das funções lambdas irão ler o bucket da "SetupGroupsMakeDiff", e isso está ilustrado pela seta laranja. Nas DAGs, sempre que há uma seta laranja, significa que se trata de obtenção de dados.\n


 ![](https://outline.seazone.com.br/api/attachments.redirect?id=e64f48ee-c3cf-4c06-bac1-794285759cb8 " =513x")

Aqui está um recorte um pouco maior de como está a estrutura da DAG em relação ao primeiro botão da aba de "Grupos".


\
 ![](https://outline.seazone.com.br/api/attachments.redirect?id=5836c711-6558-4da8-a63f-de0bde4eda4c " =760x")

O segundo e terceiro botão estão relacionados com a seleção de concorrentes, onde o segundo botão tem o objetivo de atualizar os polígonos e o terceiro botão tem o objetivo de enviar os concorrentes já selecionados e presentes na aba "Concorrentes por ID", da planilha de SETUP, para a tabela "competitors_plus". Como temos uma DAG específica para concorrentes, na DAG de SETUP, esses dois botões aparecem, mas neles tem um link que redirecionará para a DAG Concorrentes, como mostrado na imagem abaixo.


\
 ![](https://outline.seazone.com.br/api/attachments.redirect?id=39ce26d3-8ade-4127-bbf9-6d283de25adc " =262x")

E por último, temos o quarto botão dessa aba "Grupos", o qual está relacionado com a parte de sazonalidade, regrasAGC, AGC - categoria e AGC - imóvel. Quanto às duas primeiras partes, o fluxo é acontecer o salvamento de dados em buckets S3.


\
 ![](https://outline.seazone.com.br/api/attachments.redirect?id=03d01574-735b-4c8d-bfea-b34ca3244203)


Já na parte de AGC - categoria e AGC - imóvel, há uma stepfunction que realiza a leitura de buckets, realiza o salvamento de dados em buckets e envia uma mensagem para a fila de mensagens SQS. Há também uma função lambda que consulta esta fila e reage a mensagem contida nela.


 ![](https://outline.seazone.com.br/api/attachments.redirect?id=cb40f881-0690-47af-a25d-52d37df01d1e)


* **DAG - CONCORRENTES**

Nos botões relacionados aos concorrentes, os quais se encontram na aba de grupos da planilha de SETUP, o primeiro deles está relacionado a atualização de polígonos. Há uma stepfunction na qual é feito o salvamento de dados em buckets e que também está relacionada a dados dos polígonos, os quais podem ser visualizados no Google Maps.

Exemplo de polígonos:


 ![](https://outline.seazone.com.br/api/attachments.redirect?id=7674ca06-4f62-4b95-9090-187bd4feea16)


No fluxo gerado por esse botão também há um lambda que verifica uma mensagem na fila SQS e atualiza os dados na aba "**Conc﻿orrentes Sirius"** e "**Conc﻿orrentes Sem Strata"** da planilha de Rm_concorrentes, e a aba "**Conc﻿orrentes por ID"** da planilha de SETUP.


 ![](https://outline.seazone.com.br/api/attachments.redirect?id=b05b44b0-a6de-4e80-87bd-1c37def68b98)

Já o segundo botão se trata de atualizar concorrentes. Nessa etapa também há uma stepfunction a qual faz o salvamento de dados em buckets, também é gerada uma mensagem para fila SQS, e há um lambda que lê dados do bucket "Competitors_Plus" e atualizada a aba "Warnings_concorrentes" na planilha de SETUP.


\
 ![](https://outline.seazone.com.br/api/attachments.redirect?id=ac57e91f-bc8a-4dc7-a270-861c3c12bb24)


* **DAG - AGC**

No botão **Análi﻿se por Imóvel,** há uma stepfunction que lê dados de buckets, envia uma mensagem SQS, e há um lambda que pega os resultados e passa os dados para formato JSON e CSV e fornece um link para download desses arquivos. O mesmo sistema acontece para o botão de **Análi﻿se por categoria.**

Exemplo do fluxo para o botão **Análi﻿se por Imóvel:**


 ![leitura aos buckets](https://outline.seazone.com.br/api/attachments.redirect?id=017eb16e-bafb-40e6-b967-14b4af43bea3)

*leitura aos buckets*

 ![lambda e formatação dos dados para json e csv](https://outline.seazone.com.br/api/attachments.redirect?id=1baf01e9-198a-414a-b868-d915ce734fbf)

*lambda e formatação dos dados para json e csv*

Nessa planilha também há um menu que oferece as opções de enviar preços por categoria e enviar preços por imóvel.


\
 ![menu de opções](https://outline.seazone.com.br/api/attachments.redirect?id=8bf9301f-6475-4402-a03e-c1a0d5c98db8)


O fluxo do botão de enviar preços por categoria envolve um lambda que realiza leitura de buckets, atualização da aba desconto na planilha de SETUP e o envio de preços para a Stays. Já o botão de enviar preços por imóvel está relacionado com o envio dos preços para a Stays.

* \
  ![](https://outline.seazone.com.br/api/attachments.redirect?id=2cd0cc47-d735-4150-ab56-c4c5af126f2a)**DAG - Precificação de concorrentes**

  \
  Na aba Preços há o botão Trazer Grupo/Imóvel que possui um lambda relacionado que lê dados de buckets e gera um json e um link para baixar os arquivos na SETUP groups.

  \
  ![](https://outline.seazone.com.br/api/attachments.redirect?id=a9fa92d6-e585-4a0f-873b-f0d99f1703c6)

  \

Também há o botão Enviar Preços, que possui um lambda relacionado que salva dados no bucket, um lambda que envia uma mensagem SNS e outro lambda que consulta essa mensagem.


 ![](https://outline.seazone.com.br/api/attachments.redirect?id=f63b8447-94fd-4a06-ab65-03ba7bc5b63d)

Há também a aba Preços Categoria, que possui o botão Trazer Grupo, o qual gera novas datas para serem preenchidas de acordo com o intervalo da coluna "Janela de dias".


\
 ![](https://outline.seazone.com.br/api/attachments.redirect?id=64e0a50d-f00b-4c12-a1df-b0bae369ef0e)

O botão de Enviar Preços da aba Preços Categoria segue a mesma estrutura de fluxos que o botão Enviar Preços da aba Preços.


\n