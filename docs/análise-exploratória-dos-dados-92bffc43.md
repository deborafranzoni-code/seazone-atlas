<!-- title: Análise exploratória dos dados | url: https://outline.seazone.com.br/doc/analise-exploratoria-dos-dados-SEy0FiPE7u | area: Tecnologia -->

# Análise exploratória dos dados

De acordo com a documentação disponível no outline sobre a [análise de anomalias](https://www.google.com/url?q=https%3A%2F%2Foutline.seazone.com.br%2Fdoc%2Fdefinicao-do-escopo-de-dados-e-coleta-GRO6Q7HYEj). Foi feita uma analise exploratória dos dados coletados, os dados são extraídos do csv disponível no drive de Data Ops para análise de anomalias, a análise foi organizada dessa forma:

* Introdução
* Objetivo
* Metodologia
* Resultados ou Análises
* Conclusões


\
# Dataset trabalhado


Como pode ser obserado, para os listings que atendem as exigencia mencionada na documentação, temos uma lista de 64951 registros (listings). O dataframe possui dados acerca da propriedade como pode ser observado à seguir


 ![](/api/attachments.redirect?id=86422ef5-b72a-43fa-939b-bde97622c788)


Uma etapa que surgiu durante analise dos dados, foi a etapa de filtragem para analise apenas imóveis que possui classificação. Atualmente, o processo de classificação dos imóveis acontece de forma manual e está disponivel no SIRIUS.

A seguir pode ser observado a lista de imóveis com classificação feita pelo time de RM, observada no campo strata. O número de registros é de 45.990 registros

 ![](/api/attachments.redirect?id=2c1af730-1391-4a93-8363-6127d073b740)


\
# Análise dos status e faturamento diário dos imóveis 


Os dados de faturamento e disponilidade diária dos imóveis para o ano de 2023, são apresentados a seguir. Resumidamente, as informações sobre o status do imóvel, se ele está bloqueado, ocupado/reservado ou disponível, e informação do fatuamento do imóvel estão presentes no dataFrame que possui 6279948 registros (visto que são os número de imóveis x 365 dias)


 ![](/api/attachments.redirect?id=77ad4103-5ce4-467a-89af-c9344ae36501)

Dados de 2023

 ![](/api/attachments.redirect?id=2457b9eb-792e-4ee9-a2b3-98050db8e8f4)Dados de 2024


Para a análise dos dados, facilita juntarmos em um unico dataframe, os dados de categorização (strata) com os dados do imóvel que possui categorias importantes como o estado e cidade do imóvel. A junção das duas tabelas deve ser focado em analisar os imóveis que foram caracterizados, por isso a junção deve ser um left join. É importante lembrar que os imóveis selecionados são imóveis que foram classificados pelo time de RM, ou seja, possuem valor de strata.

\n ![](/api/attachments.redirect?id=009e1e08-fdd0-4b47-8b7e-95cd099b1774)


A partir disso, foram gerados gráficos para verificar a dispersão dos valores de bloqueios e reservas. 

Os bloqueios são os registros diários marcados como bloqueio e as reservas são as diárias marcadas como indisponíveis e ocupadas. Com isso, temos o gráfico a seguir, onde conseguimos que ao observar essa disposição agrupando os bloqueios e reservas geograficamente, nessa distribuição de estados, não temos um dado claro visto que o número de bloqueios e reservas será praticamente o mesmo.

Distribuição de reservas e bloqueios por estados

 ![](/api/attachments.redirect?id=8c73d7dd-ef41-4292-af7f-24556d88e828)


Contudo, ao observar esses dados em uma distribuição temporal, temos uma visualização mais descritiva onde o número de bloqueios oscila em relação ao número de reservas visto que se um imóvel está reservado não pode estar bloqueado e vice e versa

Distribuição de reservas e bloqueios mensalmente

 ![](/api/attachments.redirect?id=d04ee772-bdc7-4f52-8abc-2e2104fdff83)


Distribuição de reservas e bloqueios diariamente

 ![](/api/attachments.redirect?id=8a816e70-b109-4d99-9774-2931eb1f7009)


Uma maneira mais inteligente de observar os dados em relação a uma distribuição geografica é ao observa a distribuição dos valores de faturamento em relação à região. Isso se torna interessante, visto que o intuito futuro da preparação dos dados pra identificação de anomalias é de que seja possível identificar uma anomalia, a partir do faturamento do imóvel em relação à seus similares. Organizando os imóveis geograficamente é possível que tenhamos imóveis mais parecidos em strata e características agrupados juntos


\

\

\
Distribuição do faturamento diário por estados


\
 ![](/api/attachments.redirect?id=68f48cce-8991-435c-80d0-702a3889906c)


\

Distribuição do faturamento diário por strata


\

\
 ![](/api/attachments.redirect?id=4bd647ce-5068-4fbf-ad52-fe5fef1dd7db "left-50")


\
Distribuição do faturamento diário por cidades da Bahia


\

 ![](/api/attachments.redirect?id=e8856ad6-c893-4bdc-abe1-07e61e658ecb)