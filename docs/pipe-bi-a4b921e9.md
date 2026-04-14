<!-- title: Pipe-BI | url: https://outline.seazone.com.br/doc/pipe-bi-O5ZtNhTJP2 | area: Tecnologia -->

# Pipe-BI

## Documentação Usuário

## Documentação Técnica


1. Fonte de dados e conexão com datalake:
2. Fluxo de dados:

Atualmente o dashboard está conectado aos seguintes fluxos de dados:

* **dim_details**:

Define 4 tabelas dimensão que são queries diretas (select \*) das seguintes views no Athena(schema clean):

<https://lh7-us.googleusercontent.com/docsz/AD_4nXcEHIuo-m1AlW7M1kL0dtHnOhaTuCHQRiEtuGUpSNyDvj2NBmP-Fa6f9WM6L_1ErTpgDE9yQhqzKpa40Olse-RhaESB5oRDYWznE-fASHn6tcsrLI21bO-nQbSj7Ozi558DqF7N4mblwvqI6Fg9LizGnFEh?key=SAVWjqB-52GrRRsMepV-aQ>

* **fato_details:**

Define 1 tabela fato que é query direta da view **fato_details** no Athena(schema clean). Esta view é a última aquisição de cada listing da tabela clean_details.

* **fato_modelo:**

Define 2 tabelas fato e 1 "dimensão": as tabelas **fact_models** e           **fact_models_by_year** são queries diretas das views de mesmo nome no Athena(schema models). A tabela "dimensão" **mapped_suburbs** é query direta da tabela **new_suburb** e serve como auxiliar para exibir quais bairros(apenas de floripa) foram agrupados em quais grupos no modelo de predição de faturamento.

* **fato_block_occupancy**:

Define 1 tabela fato que é query direta da view de mesmo nome no Athena(shcema enriched). A view é uma query quase que direta à tabela **monthly_fat**(sim, o nome é ruim).

A conexão dos fluxos de dados ao Athena é feito pelo driver ODBC, configurada no gateway do powerBI com o nome "**datalake-pipe**"(credenciais no Vault).

Como o dashboard está conectado ao fluxo de dados que querya, na maior parte das vezes, uma view, o dev pode escolher alterar os dados: **na view, no fluxo de dados ou no Power Query** do próprio dashboard. É recomendável alterar a view e deixar o fluxo de dados e o Power Query só alterarem no máximo a tipagem das colunas.

A conexão do dashboard com o fluxo de dados se dá com a conexão nativa do Power BI nomeada "**PowerBI-Dataflows**" que exige somente o login do Power BI(credenciais no Vault).


2. Atualização:

Como o principal workflow de jobs no datalake é rodado na segunda, os fluxos de dados estão settados para atualizar assim que suas respectivas tabelas são atualizadas no datalake. Dessa forma o dashboard está settado para atualizar após todos os fluxos de dados atualizarem, às 20h.


3. Estrutura:

Páginas:

* Geral:

Aqui estão as informações agregadas dos listings: distribuição de anúncios por localização e tipo; faturamento, ocupação e diária média.

* Análise Listing:

Esta página contém a predição de faturamento por cenário e o faturamento real dos últimos 12 meses dos listings do cenário. O semáforo serve como indicativo de confiabilidade nos números de faturamento da predição.

* Faturamento Cidade Strata:

Esta página surgiu como uma necessidade de expor as informações do sabor de sorvete de mesmo nome em um BI. Aqui os dados utilizados para fornecer o faturamento são similares aos dados utilizados na página "Análise listing" mas dessa vez agrupados anualmente e com uma legenda diferenciada para os percentis.

Relacionamentos:

As tabelas dimensão se relacionam com a tabela fato_details(1-*) e a fato_details se relaciona com a tabela fato_block_occupancy(1-*). Tomar cuidado que as tabelas de modelo NÃO se relacionam com as demais tabelas, somente com a calendário(dim_dates).

Medidas:

Em geral, as medidas têm nomes bem sugestivos, mas é importante tomar cuidado com dois grupos: as medidas do **modelo de predição** e as medidas do **semáforo**.

* Modelo:

Lembrando que como não há relacionamento das tabelas modelo com a tabela details, as medidas foram feitas para se utilizarem do filtro da details com a função "SELECTEDVALUE()". Além disso, há uma lógica para identificar os bairros que foram agrupados em determinados cenários em Florianópolis e mostrar quais bairros estão no grupo.

* Semáforo:

O semáforo é dependente de uma série de regras relativas à quantidade de dados usados para a predição de faturamento do determinado cenário. A principal medida é a "**Classificacao Semaforo**" que define as regras.