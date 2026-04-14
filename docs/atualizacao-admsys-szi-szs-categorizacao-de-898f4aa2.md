<!-- title: Atualização AdmSys - SZI SZS (categorização de | url: https://outline.seazone.com.br/doc/atualizacao-admsys-szi-szs-categorizacao-de-1TgEAGlC10 | area: Administrativo Financeiro -->

# Atualização AdmSys - SZI SZS (categorização de

!\[\](Atualizac%CC%A7a%CC%83o%20AdmSys%20-%20SZI%20SZS%20(categorizac%CC%A7a%CC%83o%20de%20782f8ab3cce14b16a9c667ac046574f4/Atualizao_AdmSys_-*SZI_SZS*(categorizao_de_sadas_e_cartes).png)

Este processo de atualização é cabível para as seguintes tarefas:\n-\n**Importação dos extratos bancários para o AdmSys\n- Extrato conta corrente - Holding / Khanto Reservas\n- Categorização saídas - SZS / SZI / Marketplace\n- Categorização saídas - Holding / Khanto Reservas\n- Categorização cartão - SZS / SZI\n**

O AdmSys atualmente é onde centralizamos todas as movimentações financeiras das empresas Seazone. Abaixo estão as pastas do AdmSys que utilizamos. Dentro de cada pasta está a planilha que utilizaremos para atualização e a pasta para salvar o extrato:

[Seazone Serviços\n\n](https://drive.google.com/drive/folders/1hVyd_sWrW9XV1UKdR6EbKSS6O-hu--xb)[Seazone Investimentos](https://drive.google.com/drive/folders/1UlRfeRAtfj5czdhlRqBUh5RZirDvrYB3)\n\n[Khanto Reservas](https://drive.google.com/drive/folders/1rwcqdPdTem93EjvHHgEhe1o69MbJj7E1)\n\n[Holding](https://drive.google.com/drive/folders/19-2AR_SbC94VbLZg6YsnfC5psC4nc5IN)\n\n[Marketplace](https://drive.google.com/drive/folders/1aTSoNQP4kp7Thd_Wti9RazyISnV4QSgh)

**Link do vídeo as-is:**

<https://www.loom.com/share/248fb3ab4f744718a536d088bc28560d>

# POP:

Para atualização do AdmSys das Empresas, iremos seguir os passos abaixo:

1 - Acessar todos os bancos onde temos movimentações financeiras. Atualmente são: Banco Inter, Banco Sicredi, Banco Sicoob, Banco BTG e suas respectivas faturas de cartão. Os bancos Inter e Sicredi, conseguimos fazer a atualização automática através de script nas planilhas, porém o lançamento do Sicoob e BTG são feitos de forma manual.

1\.1 - Consultar o extrato referente a data de atualização. A data de atualização tem de contemplar a última data registrada na aba de "Saídas" do relatório;

1\.2 - Salvar os extratos em ".csv" referente a data de atualização na pasta "Extratos Bancários" da respectiva empresa;

1\.3 - Após salvar o extrato na pasta, copiar o nome do extrato existente ("Extrato SI.csv" para o exemplo que estamos utilizando);

1\.4 - Mover o extrato anterior para a pasta "00-Archive";

1\.5 - Renomear o extrato salvo para atualização com o nome que foi copiado ("Extrato SI.csv"). Esse é um passo crucial, pois o script de cada planilha consulta esse extrato para atualizar os registros;


2 - Após renomear o novo arquivo, retorne para a raiz da pasta da empresa que estamos atualizando e abra a planilha "AdmSys - \*Nome da Empresa\*";

2\.1 - Na planilha referente a Seazone Investimentos, na aba "Dashboard" temos os botões para atualizar o Extrato, Saída e Entrada. Executaremos apenas os botões referente ao banco Inter. Clique no botão e aguarde a mensagem de "Cmplete!" e siga para o próximo botão;

2\.1.1 - Para a planilha da [Seazone Serviços](https://drive.google.com/drive/folders/1hVyd_sWrW9XV1UKdR6EbKSS6O-hu--xb), na aba "Dashboard", iremos executar os botões "Categoriza Saída" e "Categoriza Entrada", nesta ordem. Clique no botão e aguarde a mensagem de "Complete" e siga para o próximo botão;

2\.2 - Caso o relatório apresente algum erro após o clique no botão, se atente a data de atualização, em alguns casos o extrato que foi salvo, não contém a última data registrada no AdmSys. Atualize o extrato e execute novamente clicando no botão, caso o erro persista, atualmente o Fabiano Carniel nos auxilia com a planilha do AdmSys;


3 - Tudo certo com a atualização do extrato, vamos para as categorizações das saídas;

3\.1 - Acesse a aba "Saídas" e verifique os lançamentos que não tem preenchimento da coluna "Desc Extrato" para frente, pois as colunas anteriores foram atualizadas quando executamos os botões anteriormente com base nas informações dos extratos;

3\.2 - Para consultar as informações das colunas Atividade, Empresa, Setor, CC e Categoria, podemos:

3\.2.1 - Consultar o canal **#pedidos-de-pagamento** no Slack, buscando pelo nome na descrição do extrato, valor, data ou outro dado que nos retorne as informação correta sobre sobre o pagamento;

3\.2.2 - Outra possibilidade é a consulta da despesa dentro do e-mail do "Administrativo";

3\.3 - Atualize as informações sobre:

3\.3.1 - Atividade: Motivo do pagamento);

3\.3.2 - Empresa: Para qual empresa da Holding foi solicitado o pagamento;

3\.3.3 - Setor: É o setor dentro da respectiva empresa para qual o gasto será direcionado;

3\.3.4 - Centro de Custo e Categoria: Essa informação será preenchida com base no motivo da utilização, temos a aba "Manual", dentro da planilha de "[Orçamento](https://docs.google.com/spreadsheets/d/1e0tu1IdTqbqvHR89D0494VSPgde8W-bhQEnrTPiQX3k/edit#gid=81932380)", que contem algumas explicações de gastos, mas caso ainda fique em dúvida, consulte o responsável pela solicitação para categoriza-la da forma correta;

3\.3.5 - Para inserir as informações de Empresa, Setor, CC e Categorias consulte a aba "BD CC e categorias" dentro da mesma planilha de "Orçamento" seguindo a ordem de seleção;

3\.3.6 - Consulte também lançamentos anteriores sobre a mesma utilização do valor para se basear na categoria utilizada historicamente;

3\.3.7 - Caso a categoria prevista do gasto já exista, copie e cole os nomes (colar como valor) em seus respectivos campos. Caso não tenha a categoria correspondente ao gasto, a informação será apresentada na aba "Divergências \*Nome da Empresa\*" para que seja cadastrada essa categoria futuramente;

3\.4 - Execute o mesmo processo de atualização, porém de forma manual para os bancos Sicoob e BTG, caso tenham lançamentos;

3\.4.1 - Para esses bancos é necessário também atualizar a aba de extrato, seguindo as informações já existentes;

3\.5 - Siga os mesmos conceitos para atualização do cartão de crédito de cada banco após o fechamento da fatura.

# Melhorias

Atualmente o processo de atualização e categorização é, em sua grande maioria, manual. A forma que vem sendo feita acarreta grande gasto de tempo e por consequência o aumento dos possíveis erros em cada etapa.

Para que possamos agilizar e mitigar os erros, podemos criar script que atualize tanto entradas como saídas de cada banco e que acusam o motivo de um possível erro de importação. Também podemos criar o fluxo de atualização automática do banco de dados com base em categorização anteriores (válidas previamente), para economizarmos tempo de atualização.


[Categorização 2024](/doc/categorizacao-2024-tlLZr1ZDD9)