<!-- title: Geração de métricas para detecção de anomalias | url: https://outline.seazone.com.br/doc/geracao-de-metricas-para-deteccao-de-anomalias-YEMKYNr0vX | area: Tecnologia -->

# Geração de métricas para detecção de anomalias

Com a implementação do processo de detecção de anomalias, o passo mais fundamental do processo é de avaliação da eficiência da solução proposta para o problema de anomalias de faturamento. O grande impeditivo da implementação dessa etapa, é o fato de não termos o dado anotado acerca se os faturamentos da base dedos são anômalos ou não.


## Detecção de anomalias através da aprendizagem não supervisionada

O fator da escolha da técnica de detecção de anomalias através do agrupamento de dados, aconteceu devido as características dos nossos dados. Por não termos as anomalias de faturamento anotadas, a abordagem de aprendizagem não supervisionada foi adotada com intuito de reconhecer a similaridade entre os dados e a partir disso indicar, os dados com comportamentos que diferem de todos os grupos formados.

Com isso, uma primeira etapa de analise e construção de métricas é observar a eficiência e qualidade desse agrupamento realizado. Então, como aponta a literatura, as métricas a serem feitas sobre os clusters são chamadas, métricas de coesão que avaliam se os clusters formados são compactos internamente (alta coesão) e bem separados entre si (alta separação). \nA base de dados utilizada para clusterização é resultante da consulta da tabela de analise de faturamento:

```sql
select * from analise_faturamento 
where state is not null and
strata is not null and 
city is not null and 
listing_type is not null and 
listing_type != 'hotel' and 
number_of_bedrooms <= 3 and
number_of_reviews > 10  and 
ano in (2024) and 
mes <= 12
```


A clusterização resultante foi de 3 clusters, onde o agrupamento mais detalhado pode ser observado no documento: [Processo de clusterização para análise de anomalias](/doc/processo-de-clusterizacao-para-analise-de-anomalias-WsDSpU0tnn)

 ![](/api/attachments.redirect?id=7d16e6e5-b548-4b0d-a721-fa777ea6e0d2)


Das métricas de agrupamento, foram selecionadas o **[Coeficiente de Silhueta, Índice de Davies-Bouldin e Índice de Calinski-Harabasz](https://medium.com/@kalimarapeleteiro/m%C3%A9tricas-de-agrupamento-coeficiente-de-silhueta-%C3%ADndice-de-davies-bouldin-e-%C3%ADndice-de-9462b87ce676).** que avaliam quão "semelhantes" os dados agrupados são entre si, o quão separados (em um espaço de dimensionalidade) os clusters são um do outro e a relação entre os dois, respectivamente. Os resultados obtidos foram: 

* Coeficiente de Silhueta: 0.4220343985831759;
* Índice de Davies-Bouldin: 0.8028821082610356;
* Índice de Calinski-Harabasz: 249554.3100082317


### **Coeficiente de Silhueta**

O resultado de 0.42 indica um resultado razoável, o que pode indicar dificuldade especialmente no objetivo de detecção de anomalia, visto que as anomalias são classificadas a partir da distancia do centro do cluster, Trabalhar em aumentar essa métrica pode ajudar diretamente a diminuir o número de faturamentos classificados como anomalias, que soam "estranhos".


### Índice de Davies-Bouldin

O valor de "distância" entre os clusters não apresenta um resultado muito bom (interpreta-se que mais baixo, esse valor, mais distante os clusters estão). Contudo, questões importantes podem ser consideradas, por exemplo. O número de dados parecidos, temos dados muito "próximos" independente dos clusters, isso pode ser observado ao analisar a recorrencia dos valores de faturamento do nossa base de dados. Uma solução possível pode ser aumentar o número de clusters. ![](/api/attachments.redirect?id=17d15450-9826-4508-ab21-0f6c0f76f76a)

### Índice de Calinski-Harabasz

Resumidamente, essa métrica indica ["podemos dizer que o índice mede, simultaneamente duas coisas: quão distantes os clusters estão um dos outros (dispersão entre clusters) e quão densos estão os clusters em si (dispersão dentro dos clusters)"](https://medium.com/@kalimarapeleteiro/m%C3%A9tricas-de-agrupamento-coeficiente-de-silhueta-%C3%ADndice-de-davies-bouldin-e-%C3%ADndice-de-9462b87ce676) e ["Seu valor varia de 0 até o infinito positivo, e quanto maior, mais próximo da solução ideal você está."](https://medium.com/@kalimarapeleteiro/m%C3%A9tricas-de-agrupamento-coeficiente-de-silhueta-%C3%ADndice-de-davies-bouldin-e-%C3%ADndice-de-9462b87ce676)

Com isso, podemos dizer que o valor obtido de  249554.31 é bom. Contudo, há espaço para melhorar esse número, aumentando as métricas que citei anteriormente e suas respectivas de melhorias.


\

## Estratégia de melhoria das métricas  

Algumas formas de melhoria das métricas do agrupamento atual, já foram citadas anteriormente. Contudo, pensando na implantação do algoritmo de detecção de anomalias, a estratégia adotada foi de executar a detecção de anomalias de forma incremental, ou seja, o algoritmo de agrupamento aconteceria somente para o mês anterior. 

Essa estratégia de execução do algoritmo, aconteceu para o último mês 12/24. E ao observar as métricas de agrupamento para essas execução (fig 1) os valores se mostram melhores em relação à forma de execução considerando os meses anteriores (fig 2).


 ![fig 1. Métricas de agrupamento considerando o mês isolado](/api/attachments.redirect?id=ab4d7c14-29d3-4590-8182-6b01489a6bd8 " =506x90")


\

\
 ![fig 2. Métricas de agrupamento considerando meses anteriores](/api/attachments.redirect?id=6074e510-8dab-47be-83b6-7b1d6e80474b " =506x90")


\