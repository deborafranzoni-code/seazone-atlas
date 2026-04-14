<!-- title: Processo de clusterização para análise de anomalias | url: https://outline.seazone.com.br/doc/processo-de-clusterizacao-para-analise-de-anomalias-g25tsAAqlY | area: Tecnologia -->

# Processo de clusterização para análise de anomalias

O intuito desta documentação é de entender o processo de clusterização e os grupos de dados criados pelo algoritmo. A maneira mais intuitiva de tentar analisar esse grupos de dados é olhar para as features utilizadas para realização do algoritmo, por isso essa documentação seguirá a estrutura:

* Distribuição das features numéricas do agrupamento;
* Distribuição das features geográficas do agrupamento;
* Considerações sobre os grupos gerados;


# Distribuição das features numéricas de agrupamento

Referente às características do agrupamento, tem-se que do dataset de análise de faturamento as features selecionadas como descritivas para o algoritmo de agrupamento são: 


* **occupied_dates**: numero de dias no mes que o imovel foi ocupado; 
* **blocked_dates**: numero de dias no mes que o imovel foi bloqueado;
* **available_dates**: numero de dias no mes que o imovel esteve disponivel;
* **faturamento**: faturamento mensal do imovel;


Ao analisar a distribuição de faturamento dos imóveis, podemos observar que o cluster (grupo) com os faturamentos mais baixos é o cluster 1, enquanto o cluster 2 apresenta os maiores faturamentos. Essa distribuição é consistente com a ocupação das datas: os imóveis com menor número de datas ocupadas e menor faturamento pertencem à mesma classe. Esses fatores estão diretamente proporcionais ao número de datas disponíveis e ao preço médio.

 ![](/api/attachments.redirect?id=8647c7b6-4f63-409f-8e08-0de7acbbbc06 "left-50 =379x271") ![](/api/attachments.redirect?id=ac01a2bc-ec3e-477c-8bce-7413e98623cc "right-50 =379x271")


\

\

\

\
fig 1 e 2 -  Respectivamente a distribuição do preço médio por cluster e datas disponíveis por cluster


\
 ![](/api/attachments.redirect?id=7bd55fe9-ae47-4b77-92af-36d7d3f82674 "left-50 =379x271")

 ![](/api/attachments.redirect?id=df2546b1-a9b1-4354-b669-dcda305e6fbc "right-50 =379x271")


\

\

\

\
fig 3 e 4 - Respectivamente distribuição de datas ocupadas por cluster e distribuição de faturamento por cluster


\
# Distribuição das features categóricas do agrupamento

Das características escolhidas para o agrupamento, as cateegóricas são: estado, cidade, suburb, strata e tipo.

Ao analisar a distribuição do número de ocorrências de imóveis por grupo em cada uma dessas categorias, é possível observar a porcentagem de imóveis distribuída por grupo. Por exemplo, na distribuição de imóveis por cluster em relação ao estado, nota-se que a porcentagem de imóveis do cluster 1 é a mesma para todos os estados, sendo 47%. Para o cluster 0, a porcentagem é de 31%, enquanto para o cluster 2, é de 21%. ![](/api/attachments.redirect?id=c7c2057e-d691-4210-aa1f-6f41696980c7)


O mesmo pode ser observado em relação ao tipo de imóvel. Os imóveis do grupo 1 ainda apresentam a maior amostragem em comparação aos demais, especialmente nos imóveis do tipo casa. Com isso, é possível que imóveis de áreas amplas, com atrativos relacionados a espaços maiores (características comuns de casas), estejam mais associados ao grupo 1. Contudo, para regiões com alta frequência de apartamentos, ou seja, menos residenciais, a associação predominante tende a ser com os grupos 0 ou 2.


 ![](/api/attachments.redirect?id=ecc30025-7850-4350-a504-26d3253e9e32)


Em relação à strata, podemos observar que, na base de dados, a strata com maior amostragem é a SUP, independentemente do grupo. Contudo, o grupo 1 apresenta a maior proporção para essa categoria. Além disso, diferentemente das demais features categóricas, a strata possui uma relação distinta na distribuição de imóveis por grupo para as diferentes categorias. Para os imóveis do tipo SUP, o grupo com maior proporção é o 1; já para os imóveis do tipo MASTER, o grupo 1 é o menos representativo.


\
 ![](/api/attachments.redirect?id=10dd3d8f-69b7-4453-97dd-a3964163af9d)


\

\
Com isso, podemos concluir algumas observações sobre o agrupamento realizado. O cluster 2 representa imóveis mais "premium", pois apresenta alta representatividade nos imóveis das categorias strata TOP e MASTER, além de ter o maior faturamento, a maior taxa de ocupação e a menor taxa de disponibilidade. Por outro lado, os imóveis do cluster 1 são mais econômicos, com características mais residenciais e predominância nas categorias strata JR ou SUP. Isso pode justificar o baixo desempenho em faturamento, mesmo com alta representatividade nos estados em relação aos demais clusters.

Já o cluster 0 pode ser classificado como intermediário: apresenta faturamento abaixo do cluster 2, mas acima do cluster 1. Além disso, possui alta representatividade em imóveis das categorias TOP e MASTER, mas também contém um grande número de imóveis classificados como SUP.