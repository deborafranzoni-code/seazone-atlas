<!-- title: AdmSys | url: https://outline.seazone.com.br/doc/admsys-kpVUHW87iB | area: Administrativo Financeiro -->

# AdmSys

![](/api/attachments.redirect?id=6d671f03-4119-4a65-b235-1173c741fd0e)

📊

# AdmSys


\
Cada uma das empresas da Seazone possui uma planilha que registra suas transações financeiras, denominadas AdmSys. Temos, portanto, o AdmSys Seazone Serviços, AdmSys Seazone Investimentos, AdmSys Khanto Reservas e AdmSys Seazone Holding.

Cada AdmSys contém abas dedicadas aos bancos com os quais as empresas mantêm contas. Embora haja várias abas em cada AdmSys, para fins de categorização, as abas relevantes são as de Entradas e Saídas.

As abas de entrada e saída nas planilhas são uma cópia fiel do extrato bancário, porém organizadas para distinguir as entradas e saídas de recursos. Portanto, é recomendado evitar fazer alterações significativas nelas, como adicionar, excluir ou modificar linhas inteiras. As colunas que podem ser editadas manualmente serão explicadas detalhadamente.

A atualização do conteúdo de cada aba de saída e entrada é feita diariamente por meio de um script. Normalmente, esse processo captura as transações que ocorreram do dia útil anterior para trás, embora, em algumas situações, possa também incluir atualizações do dia atual. Os AdmSys também contam com as informações de saídas de cartão de crédito. Neste caso, a atualização é feita mensalmente.

Resumidamente, nossas abas de interesse para categorização são:

* [AdmSys Seazone Serviços](https://docs.google.com/spreadsheets/d/1YHvus3u692wr75lO_SDJgYuCo6kPqcLh9VxJ5WQ7GhQ/edit#gid=374184868)
  * Entradas e Saídas do Sicoob,
  * Entradas e Saídas do BTG,
  * Entradas e Saídas do Inter,
  * Entradas e Saídas do Sicredi.
* [AdmSys Seazone Investimentos](https://docs.google.com/spreadsheets/d/1czZEE6ajQDyaPgXQra9zBgaFvXXkhgUbLqGI7YQZcSM/edit#gid=952664530)
  * Entradas e Saídas do Inter,
  * Entradas e Saídas do Sicredi.
* [Saída Khanto Reservas](https://docs.google.com/spreadsheets/d/1L6vm5RINTTpXV-80Hih0-W2GIFoCX8jlYhflEtACguc/edit#gid=952664530)
  * Entradas e Saídas do Sicredi.
* [Saída Seazone Holding](https://docs.google.com/spreadsheets/d/1MhdH237LfRloOmq2_za-UdOkaR-l-m7vKSSiZnJAhMU/edit#gid=0)
  * Entradas e Saídas do Sicoob.


Após a atualização, novas linhas são adicionadas com as datas, valores e descrições do extrato. As colunas de [Atividade, Empresa, Setor, CC (Centro de Custo), Categoria e Subcategoria](/doc/elementos-da-categorizacao-N75ectuyOq) inicialmente estão vazias, mas serão preenchidas durante o processo de categorização. A coluna "Nome da Conta" é preenchida somente quando a saída corresponde a uma transferência ou transação PIX. Essa informação é obtida diretamente da descrição do extrato, onde é retido apenas o nome da conta que recebeu o pagamento.

Após a atualização, a o AdmSys será similar ao seguinte formato:


 ![](/api/attachments.redirect?id=81b44f33-3f3b-47fa-ba71-4ce7fb1a8f58)


É comum criar colunas nas planilhas, porém, não devemos fazer isso sem considerar cuidadosamente o impacto. Qualquer alteração significativa nas planilhas, seja por exclusão ou adição de colunas, deve ser discutida e acordada com toda a equipe, já que pode impactar scripts e outras planilhas derivadas dos AdmSys.


\