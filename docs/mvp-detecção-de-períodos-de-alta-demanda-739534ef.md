<!-- title: MVP - Detecção de Períodos de Alta demanda | url: https://outline.seazone.com.br/doc/mvp-deteccao-de-periodos-de-alta-demanda-hWfgkZCs0s | area: Tecnologia -->

# MVP - Detecção de Períodos de Alta demanda

**Relatório do estudo e análise da aplicação anterior para detecção de alta demanda com base na ocupação dos concorrentes.** 



1. **Compreender o objetivo do MVP de detecção de períodos de alta demanda:**

O projeto é relacionado a seleção de períodos de alta demanda (períodos quentes). Esse projeto já foi feito anteriormente, onde na tabela de Padrão de Precificação por Concorrentes era possível selecionar um imóvel e um período, e os períodos seguintes ao período selecionado eram mostrados num gráfico com um percentual de ocupação dos concorrentes deste imóvel. Mas, isso precisa ser adaptado para que ao invés de retornar os concorrentes a nível imóvel, seja retornado a nível grupo (polígono, strata, número de quartos). 


Quando identificada uma ocupação que chamasse a atenção, a representação visual no gráfico ficava com uma área vermelha. E isso era fruto de uma mudança rápida, por algum dado motivo, na taxa de ocupação dos imóveis dos concorrentes. Então, pode acontecer um cenário em que de um dia para o outro ocorra uma alta demanda de ocupação (por exemplo, estava com uma ocupação de 20% e foi para uma ocupação de 30%), com reservas para daqui a uns dois meses nos imóveis dos concorrentes. Diante de um cenário como esse, é preciso identificar essa mudança considerável de ocupação assim que ela acontecer, pois o RM deseja saber. \n

Uma hipótese é de que pode ter algum evento envolvido nesse período em que está apontando uma alta demanda / alta quantidade de reservas, e isso seja a causa raiz dessa mudança. Então uma ação imediata importante é aumentar um pouco o preço dos nossos imóveis e logo após isso também buscar identificar se a causa raiz é de fato um evento. Mas, seguindo o contexto de exemplo, como as reservas estão sendo feitas agora, dois meses antes de um evento, o interessante é alugar próximo ao evento, pois a demanda estará alta e será possível colocar um preço para reserva ainda maior, gerando mais lucro a partir desses imóveis. Então, é importante fazer a detecção de períodos quentes nas regiões dos concorrentes e gerar esse alerta imediato.


Como dito anteriormente, na planilha de Padrão de Precificação por Concorrentes era possível visualizar um percentual de ocupação dos concorrentes de um imóvel escolhido, e que agora o contexto é para visualização de grupos, como polígono (agrupamento por região). Caso essa estrutura da planilha continuasse sendo utilizada, seria necessário um trabalho frequente de ir manualmente grupo a grupo e verificar se há a detecção de um período quente no gráfico. Então, uma forma de auxílio pode ser, a partir de um alerta para região através do Slack, estruturando num CSV, que sinalize as ocorrências de um período quente nela, onde essas ocorrências podem ser investigadas no gráfico da planilha, retirando a necessidade de investigação de todos os grupos, tornando assim o processo de identificação dessas ocorrências menos manual. \n

Uma observação é que, em períodos próximos é normal estarem mais ocupados. \n


2. **Analisar detalhadamente o código do projeto anterior, entendendo as dificuldades encontradas e as nuances das técnicas utilizadas:**

O código atual se encontra nesse link: __<https://github.com/seazone-tech/sirius-precificacao/tree/dev/pricing/fetch_price_and_occupancy>__


Nele há dois arquivos: "lambda_function.py" e "periods_functions.py" 


No arquivo "periods_functions.py" são utilizadas as bibliotecas pandas e numpy, e nele há 8 funções:

| **Nome da função** | **O que a função realiza** |
|----|----|
| ## `get_periods(df):` | Recebe um DataFrame(df) e retorna um novo df com duas colunas do df original: a coluna 'date' e a coluna 'period' modificada. Essa coluna contém agora números inteiros que representam uma contabilização de períodos consecutivos com estados de 'True' ou 'False' baseados na coluna booleana 'hot_zone'. |
| ## `convert_false_sequence(df):` | Percorre a coluna booleana 'hot_zone' do df recebido, e transforma sequências de "false" com menos de 7 elementos em "true". |
| ## `def expand_zones(hot_zones, expand_loop):` | Realiza o aumento do número de 'hot_zones' iguais a 'true', a depender a condição de "%occupation" ser maior que o "expand_factor", o qual depende da ocupação média e do desvio padrão das zonas quentes atuais. |
| ## `def number_zone(df, zone_type):` | Adiciona uma coluna numérica no DataFrame, com valores para sequências consecutivas de dias em que a zona quente ou zona morna é verdadeira. Essa coluna adicionada indica em qual zona cada linha se encontra, com base em 'zone_type' (pode ser 'hot_zone' ou 'warm_zone'). |
| ## `def calculate_wam_zone_2(warm_zones):` | Realiza uma análise mais refinada para a identificação de 'warm_zones'. A função olha para zonas "warm" e zonas "cold", e com base em informações de ocupação e estatísticas como média e desvio padrão, estabelece condições para considerar como true realmente apenas 'warm_zones' com uma ocupação elevada. A função também renumera o DataFrame no caso de inclusão de novas warm_zones. |
| ## `def calculate_warm_zone(df, z_score_column, warm_zone_column):` | Possui o objetivo de identificar e marcar  zona quentes em um DataFrame "df", com base nos valores de uma coluna de Z-score. É marcado como "zona quente" os intervalos consecutivos (com um tamanho mínimo de 2) de valores positivos da coluna 'z_score_column'. O "df" é atualizado para refletir essas zonas quentes identificadas. |
| ## `def occup_graph_warm_periods(df_warm_periods):` | Realiza a identificação de zonas quentes com base na ocupação dos imóveis ao longo do tempo, usando diferentes janelas de média e desvio padrão para filtrar e identificar padrões de ocupação. A função segue um processo que envolve cálculos de ocupação e estatísticas (média, desvio padrão, z-score); Identificação inicial das zonas mornas; Filtragem e definição de zonas quentes com base nas estatísticas de ocupação; Expansão das zonas quentes para incluir mais dias ao redor e agrupamento de zonas quentes contínuas. |
| ## `def get_date_hot_zones(df: pd.DataFrame):` | Realiza a identificação e retorno dos períodos (intervalos de datas) de zona quente (períodos de alta ocupação) para todos os imóveis do DataFrame original, com colunas para date, hot_zone, e listing. |


No arquivo "lambda_function.py" há 3 funções:

| **Nome da função** | **O que a função realiza** |
|----|----|
| ## `def get_prices_percentil():` | Extrai percentis de preços de imóveis para cada data do período de análise, filtrando por condições específicas. Os percentis ajudam a entender a distribuição de preços. |
| ## `def get_occupancy():` | Extrai dados de ocupação para cada listagem e calcula a porcentagem de ocupação em relação ao número de competidores ativos. A função cria uma versão do mesmo período do ano anterior para comparação. |
| ## `def lambda_handler(event, context):` | Extrai dados de occupancy e prices_percentilusando as funções anteriores, cria intervalos de datas para cada listing e une esses dados com as tabelas de ocupação e preços. Também chama a função "get_date_hot_zones" para calcular períodos de alta ocupação e adiciona esses períodos ao DataFrame. Salva o DataFrame final em um arquivo Parquet no S3 para armazenar os dados processados. |
| ## `def respond(code, body):` | Fornece uma resposta para a função Lambda, que retorna um código de status e uma mensagem. |


3. **Preparar o ambiente de desenvolvimento e obter dados:**

O código do repositório em questão foi adicionado ao Vscode. Lá foram criados dois Jupyter Notebooks para realização da etapa de obtenção de dados. Um deles foi para obtenção dos dados na granularidade anterior (por listing) e o outro deles foi para a obtenção dos dados na granularidade atual que o RM usa (por região/por polígono), logo, por grupo de imóveis.


Foi verificado na planilha de SETUP, na aba "Feriados", na qual consta tanto feriados quanto eventos. Um dos eventos mapeados foi o LOLLAPALOOZA, um festival de música que aconteceu em São Paulo em março de 2024. 

 ![](/api/attachments.redirect?id=07cf0a8e-684b-47fa-8f29-7f0e32400144 " =524x23")

 ![](/api/attachments.redirect?id=a773bba5-dbbd-47a1-b13f-a676c0aa4898 " =524x20")

Pesquisei quando esse evento acontecerá em 2025, e ele acontecerá nos dias 28, 29 e 30 de Março - ***2025***. Autódromo de Interlagos, São Paulo. 


Diante disso, fui no athena AWS, na tabela 'competitors_polygons' para saber como era a estrutura das feições para o campo 'polygon':

 ![](/api/attachments.redirect?id=ad077cc1-d21d-46ce-b76d-5a0b1c42e93e " =262x100")

Resultado da consulta:

 ![](/api/attachments.redirect?id=e59f3382-b83e-4c4a-aadc-353957c1934a " =187x335")

Após isso, pesquisei quais bairros de São Paulo são mais próximos do local onde o evento acontecerá e um deles foi Moema. Logo, consultei por um imóvel que fosse da região São Paulo - Moema e que tivesse um 'listing' existente na tabela 'competitors_plus': 

 ![](/api/attachments.redirect?id=93e61c51-759e-43d2-9fe6-4be0f5d1ea36 " =748x139")

Resultado:

 ![](/api/attachments.redirect?id=db072201-5a87-4217-9fc6-4d50eb32813f " =1381x114")


Com o listing 'AMM0903', executei os códigos no Jupyter Notebook em que a análise é feita por Listing e analisei o resultado da detecção de período de alta demanda para esse listing. Após o codigo selecionar os períodos de hot_zones, temos um DataFrame "periods'", em que eu filtrei para olhar apenas para os dados do listing em questão, e ele vem nessa estrutura da imagem abaixo. 


 ![](/api/attachments.redirect?id=44a9e972-65b9-491e-b7dc-05ba44da7533 " =333.5x159")

De acordo com a função "get_periods(df)", que preenche a coluna de 'period' com números inteiros que representam uma contabilização de períodos consecutivos com estados de 'True' ou 'False' baseados na coluna booleana 'hot_zone', para esse imóvel, os períodos que são hot_zones são os que estão com o número 11 (22-11-2024 até 28-01-2025) e 12 (20-03-2025 até 06-04-2025), e os períodos que não são hot_zones estão com o número 1 (29-01-2025 até 19-03-2025) e 2 (07-04-2025 até 20-05-2025). 


Logo, concluímos que foi detectado como período de alta demanda o **12 (20-03-2025 até 06-04-2025)**, que é um período que engloba o período de acontecimento do evento LOLLAPALOOZA, que acontecerá nos dias 28, 29 e 30 de Março. 


Ao adaptar o código para a granularidade de região, foi mapeado o mesmo evento, sendo ele o LOLLAPALOOZA. Foram selecionados os dados da região São Paulo - Moema e foi verificada que essa identificação do período de alta demanda ocorreu 4 meses antes do evento acontecer, visto que agora estamos no mês 11/2024, e através do código ele detectou o período quente em 03/2024, que é o mês que acontece o evento, e o intervalo de dias também engloba os dias em que o evento acontece. \n

Após o codigo selecionar os períodos de hot_zones, temos um DataFrame "periods_polygons'", em que eu filtrei para olhar apenas para os dados do polygon em questão, e ele vem nessa estrutura da imagem abaixo. \n ![](/api/attachments.redirect?id=27739234-23e9-4136-997e-ffb3c5ab29ab " =441x138.5")\n\nDe acordo com a função "get_periods(df)", que preenche a coluna de 'period' com números que representam uma contabilização de períodos consecutivos com estados de 'True' ou 'False' baseados na coluna booleana 'hot_zone', para esse polígono, os períodos que são hot_zones são os que estão com o número 11 (22/11/2024 até 26/01/2025), 12 (12/02/2025 até 08/03/2025) e **13 (27/03/2025 até 30/03/2025).** Já os períodos que não são hot_zones estão com os números 1 (27/01/2025 até 11/02/2025), 2 (09/03/2025 até 26-03-2025) e 3 (31/-3/2025 até 20/05/2025).

 ![](/api/attachments.redirect?id=6104584b-eaaa-443c-bb46-312b65e7aaaa " =216x193.5")

Logo, concluímos que foi detectado como período de alta demanda o **13 (27/03/2025 até 30/03/2025)**, que é um período em que ocorrerá o evento LOLLAPALOOZA, que acontecerá nos dias 28, 29 e 30 de Março. 


OBS 1: Executei o script para essa mesma região após um dia e o resultado mudou para detectar como período de alta demanda o período **12 (20/03/25 até 06/04/25).** Esse período detectado continua englobando o período em que o evento acontecerá, e que por sua vez foi o mesmo período identificado na granularidade de listing.


 ![](/api/attachments.redirect?id=54675846-8fe1-4dc3-94c1-f6bae8c674e7 " =209x333.5")

OBS 2: Após essas etapas consultei também as colunas '%occupation', 'occupied' e 'num_active_competitors' para saber a porcentagem de ocupação em períodos considerados de alta demanda. Os valores armazenados na coluna de %occupation são coerentes com o cálculo de %occupation sendo ele (occupied / num_active_competitors), mas a porcentagem de ocupação do dia inicial de um período detectado como de alta demanda (período 12) está recebendo um valor de 0% de ocupação, o que não fica coerente com o contexto de alta demanda. Os outros dias desse período 12 também possuem a porcentagem de ocupação próxima de 0. Isso aconteceu tanto para a granularidade de listing quanto para a granularidade de região.

 ![análise por região](/api/attachments.redirect?id=189dec2f-d251-4acb-a71d-0485ee6c9ee0 " =456.5x339") ![análise por listing](/api/attachments.redirect?id=b3922a23-7e4d-4cd1-98d0-a722e1649cec " =449x363")


\
Notebooks estruturados para essa etapa:

[Analise_Regioes.ipynb 1322257](/api/attachments.redirect?id=bafc76c4-06b1-488d-9303-1881c2ab2c6e)

[Analise_Listings.ipynb 10510648](/api/attachments.redirect?id=b4c131bb-da9c-477b-8f32-39c8468826f2)


* **Revisão dos Resultados do Estudo Anterior**:
  * *==Resumo dos pontos fortes e fracos identificados no projeto anterior==:*

    Com base na etapa de estudo e análise da aplicação anterior, os pontos fortes encontrados foram as classificações de hot_zone (representadas pela numeração da coluna 'period' retornada no DataFrame) tanto na granularidade de listing quanto na granularidade de grupos/polígonos, em períodos que foram mapeados como períodos de evento. Citando o exemplo da etapa anterior, o evento Lollapalooza foi mapeado e no período que o evento acontecerá (28, 29 e 30 de Março - ***2025****),* tanto o imóvel analisado, o qual fica na região de  São Paulo - Moema, quanto a própria região São Paulo - Moema, nesse período do evento, receberam uma detecção de período de alta demanda. Logo, em resumo, houve uma correspondência entre detecção de "hot_zone" (período de alta demanda) com um período que de fato será de alta demanda, principalmente na região São Paulo - Moema que é uma região próxima de onde acontecerá o evento. Outro ponto forte é a antecedência em que essa identificação ocorre, visto que o  evento e período de alta demanda mapeado só acontecerá daqui a 4 meses.

    \
    Já o ponto que não é considerado forte para o objetivo atual da detecção de períodos de alta demanda foi voltado para a função "expand_zones", a qual busca identificar, a partir de métricas, períodos que não estão classificados como "hot_zone" mas que poderiam vir a ser. Ela provoca uma expansão desses períodos. Na etapa anterior, por exemplo, o resultado da detecção de período quente para a região São Paulo - Moema alinhada ao período do evento mapeado foi de 4 dias quando executou-se o script. No dia seguinte, ao executar novamente o script, esse intervalo aumentou para 17 dias, englobando o período anteriormente identificado e adicionando dias antes e depois a ele. O que é um comportamento que corresponde ao que a função "expand_zones" realiza. Mas, agora o objetivo é voltar essa identificação de períodos quentes para intervalos menores, como 3 a 4 dias. 

    \
  * *==Destaque para componentes e funções do código que podem ser reaproveitados:==*

    Em relação as funções que podem ser reaproveitadas temos as funções que fazem a aquisição dos dados que serão utilizados como a `def get_occupancy():` e a `def get_prices_percentil(): `. Já a função "expand_zones", diante do objetivo atual de identificação de intervalos menores de 3 a 4dias, foi identificada como uma problemática. Foi feita a execução do script para verificar o comportamento do código antes e depois da exclusão dessa função "expand_zones".

    Com a função "expand_zones" presente o intervalo de hot_zone englobando o período mapeado foi de 16 dias:

    ![](/api/attachments.redirect?id=45c35586-c03c-4aa2-b998-b971d21a9e4d " =206x316.5")

    Foi plotado o gráfico para visualização dessa questão de identificação como hot_zone versus percentual de ocupação antes da desconsideração da função "expand_zones".
* ![](/api/attachments.redirect?id=3259d08d-6b2f-49d5-9c11-c52732e11f28)

  Após a desconsideração da função "expand_zones":

  Com a modificação do código para o descarte da função "expand_zones" o resultado foi um intervalo identificado "hot_zone" menor, próximo ao objetivo atual que é a identificação de um intervalo de 3 a 4 dias.

  ![](/api/attachments.redirect?id=a1be6a68-c541-4e42-8895-a9a353cfd7f9 " =208x106")

  O que foi identificado é que por mais que agora a porcentagem de ocupação em si esteja baixa, mesmo nesse período considerado de alta demanda, há um discrepância nos números da coluna occupied. Nesse caso para entrar no período considerado de alta demanda o número na coluna occupied sobe de 1072 para 3680. Já para sair desse período considerado de alta demanda o número na coluna occupied decai de 2655 para 242. Então, na realidade o foco não está totalmente na coluna %occupation, mas sim na coluna occupied também.\n![](/api/attachments.redirect?id=22ae9340-4721-474f-886e-19e827c67cf1 " =428x247.5")

  Foi plotado o gráfico para visualização dessa questão de identificação como hot_zone versus percentual de ocupação após a desconsideração da função "expand_zones".

  ![](/api/attachments.redirect?id=aca1c1c7-81ec-42e3-894e-6433dfd42614)

  De modo geral, a lógica das outras funções presentes no código também podem ser reaproveitadas, porém será necessário o ajuste de parâmetros para a segmentação dessas hot_zones, focando na identificação de intervalos mais curtos.

  \
  Também foi feita uma consulta no Athena, utilizando a função `def get_occupancy():`para comparar os dados no athena com os dados finais que o código estava mostrando na coluna  "%occupation". E foi visto que os dados dessa coluna mostrados no dataframe no notebook estão correspondentes para os dias presentes em ambos.

  Dados no DataFrame:

  \
  ![](/api/attachments.redirect?id=621fbfdc-f0f8-46b3-a122-808bc3b4bfff " =423x313")

  \
  Dados no Athena:

  \
  ![](/api/attachments.redirect?id=d62fee01-2dfc-486b-8da9-3cec1e88a113 " =655x324")

  \
  Consulta realizada:

  `with fetch_occupied_competitors_per_polygon as (`

  `    select polygon, `

  `           cast(date as date) as date,`

  `           sum(case when occupied = 'true' then 1 else 0 end) as occupied,`

  `           count(*) as num_active_competitors`

  `    from daily_revenue_competitors`

  `    join competitors_plus`

  `    using (airbnb_listing_id)`

  `    join competitors_polygons`

  `    using (airbnb_listing_id)`

  `    where competitors_plus.state = 'current'`

  `      and (date between date '2024-11-27' and date '2025-05-25')`

  `      and (blocked = false or available = 'true') `

  `      and not contains(block_reason, 'dead')`

  `    group by polygon, date`

  `)`

  `select polygon, `

  `       date,`

  `       cast(round(cast(occupied as double) / num_active_competitors, 2) * 100 as integer) as "%occupation",`

  `       num_active_competitors, `

  `       occupied`

  `from fetch_occupied_competitors_per_polygon`

  `where polygon = 'Sao_Paulo-Moema';`

     

 Um ponto observado também é que não há dados dos imóveis necessariamente diariamente, há períodos em que os dados aparecem de 2 em 2 dias e há períodos que os dados aparecem diariamente.

Foi plotado o gráfico para visualização dessa questão de identificação como hot_zone versus percentual de ocupação.

 ![](/api/attachments.redirect?id=7f5726af-2338-4f97-ad2d-aaa189fd047a)

* \
  * ==Identificação de limitações e desafios que precisam ser endereçados na nova implementação:==

    Como apontado anteriormente, os desafios e limitações atuais estão ligados ao intervalo de de duração dessas hot_zones identificadas e definição desse pico de demanda (que pode ser explorada a ideia de detecção de anomalia). Outro ponto que deve ser visto é a análise para a taxa de crescimento da hot_zone.
* **Definição dos Requisitos do MVP**:
  * ==Listagem dos requisitos funcionais (o que o sistema deve fazer) e não funcionais (desempenho, usabilidade, etc.).==

    ==Requisitos funcionais:==
    * O sistema deve identificar períodos que possuam um número de reservas elevado numa região.
    * O sistema deve classificar uma região como estando num período de "hot_zone" apenas se esse período possuir um número elevado de demandas.
    * O sistema deve gerar um alerta na medida em que identificar o período de alta demanda para uma região.
    * O sistema deve realizar o envio desse alerta via ferramenta Slack assim que um novo pico for identificado.
    * O sistema deve enviar no alerta a região identificada com pico de demanda e o período associado a essa região.
    * O sistema deve fornecer uma interface que possibilite a pesquisa de regiões.
    * O sistema deve fornecer uma interface que com base na região pesquisada aponte graficamente se foram identificados períodos de alta demanda e caso sim, quais períodos foram esses. 
    * O sistema deve detectar uma taxa de crescimento da hot_zone / crescimento do pico para realizar a geração de um alerta.

    ==Requisitos não funcionais:==
    * O sistema deve detectar esses períodos de alta demanda ocasionados por eventos e /ou feriados com o maior tempo de antecedência possível.
    * O sistema deve ser intuitivo, com uma interface simples para visualização e análise. Deve ser fácil para os usuários pesquisarem regiões específicas e visualizar os dados de forma clara.
    * Os alertas devem ser concisos e claros, com um resumo das regiões afetadas e dos períodos de alta demanda.
    * O sistema deve ser capaz de processar dados de grandes volumes de reservas sem falhas. As respostas das consultas e os alertas devem ser gerados em tempo real ou com atraso mínimo.
    * As consultas e análises devem ser eficientes, garantindo que o sistema possa escalar com o aumento de dados e número de regiões analisadas.
    * Possível ponto de melhoria futuramente: O sistema deve identificar caso o aumento da demanda seja causado por eventos específicos (como festivais, feriados), o sistema deve ser capaz de correlacionar esses eventos com a demanda, baseando-se em dados históricos e eventos conhecidos.

    \
  * ==Especificação da granularidade da análise (por polígono, categoria, etc.).==

    A granularidade da análise migrou de listing (anteriormente na planilha de Padrão de Precificação por Concorrentes a consulta e análise era feita por imóvel) para região (atualmente a necessidade é que sejam detectados períodos de alta demanda nas regiões e não diretamente imóvel por imóvel).
  * ==Definição dos critérios para identificação de picos de demanda e geração de alertas.==

    Um critério inicial para a identificação dos picos de demanda é seguir a condição de aumento de 10% em relação a média dos dados em questão num período de 7 dias. Manter esse período de antecedência na identificação (o evento mapeado na etapa anterior acontecerá daqui a 4 meses e já foi identificado). 

Notebook estruturado nessa etapa após as modificações realizadas no código:

[Analise_Regioes.ipynb 294353](/api/attachments.redirect?id=e51e4cf1-c66c-45bc-b124-62046585f05c)


### Planejamento da Arquitetura e Detalhamento dos Componentes do MVP

#### **Adaptação para a Detecção de Alta Demanda em Regiões**

O novo sistema precisa identificar a alta demanda não apenas para imóveis individuais, mas para grupos de imóveis (por região/polígono). A ideia é automatizar a detecção desses períodos quentes para evitar a necessidade de uma análise manual de cada grupo de imóveis.

* **Função Lambda**: Assim como era usado anteriormente, será utilizada uma função lambda, contendo funções para consulta de dados, mas agora para uma granularidade de regiões.
* **API Gateway:** Será necessário o uso de uma API para direcionar os dados para o CSV de acompanhamento.


* **Alerta via Slack**: Para tornar o processo mais eficiente, a detecção será acompanhada por alertas enviados via Slack para as regiões que apresentarem alta demanda.
* **CSV para acompanhamento**: A geração de relatórios em formato CSV ajudará os analistas a visualizar as ocorrências, sem a necessidade de verificar manualmente cada região ou imóvel.


\