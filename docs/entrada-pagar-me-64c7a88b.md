<!-- title: “ENTRADA PAGAR ME” | url: https://outline.seazone.com.br/doc/entrada-pagar-me-90IMGLnlZw | area: Administrativo Financeiro -->

# “ENTRADA PAGAR ME”

➤Após baixar os extratos conforme a "**[Atualização dos extratos bancários e OTA's](/doc/atualizacao-dos-extratos-bancarios-e-otas-Ole0hHyEBJ)**" e rodar as macros (passo1, 2 e 3) da aba dashboard da tabela [AdmSys Khanto](https://docs.google.com/spreadsheets/d/1L6vm5RINTTpXV-80Hih0-W2GIFoCX8jlYhflEtACguc/edit#gid=274702885), ir para a aba "[Entrada pagar-me](https://docs.google.com/spreadsheets/d/1L6vm5RINTTpXV-80Hih0-W2GIFoCX8jlYhflEtACguc/edit#gid=819800630)" para preencher a categorização.

\[

https://docs.google.com/spreadsheets/d/1L6vm5RINTTpXV-80Hih0-W2GIFoCX8jlYhflEtACguc/edit#gid=819800630

\](https://docs.google.com/spreadsheets/d/1L6vm5RINTTpXV-80Hih0-W2GIFoCX8jlYhflEtACguc/edit#gid=819800630)


↳Na aba Entrada [Pagar.me](http://pagar.me/) a coluna "E - Reservas" deve ser preenchida com o ID da reserva Sapron

↳Para que isso ocorra, deixar o cursor na primeira linha em branco da coluna "E - Reservas" e rodar a macro "**Import Dados**"

 ![](/api/attachments.redirect?id=e45c7adb-7e77-4a4a-b703-598c259e24dd)


**Caso a macro não busque os dados do imóvel, nome do hóspede e datas de check-in/ check-out precisam ser preenchidos manualmente.**

***⚹Obs:*** *Esse preenchimento deve ser feito antes de executar a macro"Import Dados", se os dados não estiverem devidamente preenchidos vai ocorrer erro.*


↳Copiar o **ID da transação** da coluna "T"

***⚹Obs:*** *Esse é o código de transação do pagar-me, colar na plataforma pagar-me para obter o código Stays e ter acesso aos dados do imóvel, nome do hóspede e datas de check-in/ check-out.*

↳Abra o site do [pagar-me](https://beta.dashboard.pagar.me/#/account/login)

↳Vendas

↳Transações

↳Colar o **ID da transação** na ""lupa"", filtrar

↳Entrar na transação procurada

 ![](/api/attachments.redirect?id=274919e1-f3fb-48a3-be6a-c8c3a289aac0)

↳No final da pagina vai ter a informação do código Stays

 ![](/api/attachments.redirect?id=0ba2cb19-bb01-4809-a970-b1a36d260116)

↳Abrir site da [Stays](https://ssl.stays.com.br/i/home)

↳Com o código copiado do pagar-me colar na lupa

↳Entrar na reserva

↳Nessa pagina vai estar as informações de dados do imóvel, nome do hóspede e datas de check-in/ check-out a serem preenchidas na aba "Entrada pagar-me"

 ![](/api/attachments.redirect?id=97b2d334-0e0d-43aa-a3f7-9ff09ca55aa6)


**Caso a macro** ***"Import Dados"*** **não busque a "Reserva"(coluna E) precisa ser preenchido manualmente**

↳Copiar código do imóvel (coluna B, "Apto")

↳Abrir site do [Sapron](https://sapron.com.br/fechamentoimovel)

\[

Sapron | Seazone

Seazone - Sapron PMS

 ![](/api/attachments.redirect?id=58a95394-e5d7-47de-954b-fd7f80f59bd0)https://sapron.com.br/fechamentoimovel

\](https://sapron.com.br/fechamentoimovel)

 ![](/api/attachments.redirect?id=dff682f7-949c-46b9-a3bb-556ba864a0cd)

↳Colar código do imóvel na lupa

↳Selecionar período da reserva, o mês será de acordo com a reserva

↳Clicar no sinal de "+" para acessar informações do imóvel

↳Conferir na planilha check-in/ check-out e valor total

↳Copiar reserva e colar na [planilha](https://docs.google.com/spreadsheets/d/1L6vm5RINTTpXV-80Hih0-W2GIFoCX8jlYhflEtACguc/edit#gid=819800630)