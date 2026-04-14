<!-- title: Projetos Internos | url: https://outline.seazone.com.br/doc/projetos-internos-TZ0yz8C3Bh | area: Tecnologia -->

# Projetos Internos

## Clusterização Geoespacial

### Motivação  

O principal objetivo é aprimorar a qualidade dos dados de bairros na aplicação "Análise de Faturamento 2.0".

Na planilha dessa aplicação, determinadas consultas por imóveis com critérios específicos como estado, cidade, bairro, strata e número de quartos, retornavam poucos registros, dificultando análises relacionadas ao faturamento para esses determinados casos. Visando solucionar essa limitação, foi aplicada uma técnica de **clusterização geoespacial**, permitindo expandir a busca para imóveis em regiões próximas.

### Definição

O processo de clusterização geoespacial consiste em agrupar imóveis próximos geograficamente com base em suas coordenadas de latitude e longitude. Essa abordagem foi adotada para aumentar o número de imóveis retornados nas buscas, garantindo que, caso não existam registros suficientes no bairro pesquisado, imóveis vizinhos possam ser considerados.

### Etapas do processo

#### Estudo de Viabilidade e Testes


1. *Coleta de dados:* 

   Foi escolhido o estado de Minas Gerais para os testes iniciais. A consulta foi feita na base de dados para obter registros de imóveis, incluindo latitude e longitude. Abaixo é mostrada a consulta realizada:

```javascript
def get_dados_regiao():
    df = wr.athena.read_sql_query(
        sql=f"""
            WITH ids_loc_af AS (
                SELECT 
                airbnb_listing_id, state, city, suburb 
                FROM 
                analise_faturamento 
                WHERE 
                state = 'Minas Gerais'
                GROUP BY 
                airbnb_listing_id, state, city, suburb
            )
            SELECT 
                ila.airbnb_listing_id, ila.state, ila.city, ila.suburb, lla.latitude, lla.longitude
            FROM 
                ids_loc_af ila
            LEFT JOIN 
                location_last_aquisition lla
            ON 
                ila.airbnb_listing_id = lla.airbnb_listing_id

            """,
            database="brlink_seazone_enriched_data",
            workgroup='SorveteriaDados'
    )
    return df 
  
```

Dados retornados após consulta:

 ![](/api/attachments.redirect?id=e82117ce-705e-4f56-a50a-1e6ceacc9a95 " =418.5x152.5")


2.  *Análise dos dados:* 

   
   1. Foram identificados dados faltantes na coluna 'suburb' (9,45% dos registros).
   2. Os casos de ausência encontrados foram de dados com valor = 'none'; não houve registros NULL ou NaN.

   \

 ![](/api/attachments.redirect?id=a7ca4836-084e-431d-accb-42d5508b5d0b " =137.5x101.5")


3. *Escolha de cidade para teste:* 

   A cidade escolhida para os testes foi Nova Lima - MG, pois apresenta bairros com diferentes densidades de listings, variando entre bairros com poucos imóveis (exemplo: 7 listings) e bairros mais densos (exemplo: 52 listings). Essa diversidade permite avaliar o impacto da clusterização na expansão das buscas.

   \
   Essa configuração é relevante porque, em bairros com poucos listings, a busca tradicional pode ser limitada. No entanto, se houver bairros próximos geograficamente, a clusterização geoespacial pode expandir a pesquisa, permitindo considerar imóveis adicionais nas proximidades.

   ![](/api/attachments.redirect?id=42f2f8d3-40d8-4396-8eeb-311578e48252 " =371x283.5")
4. *Aplicação da Clusterização Geoespacial na cidade de teste:* 

   O algoritmo de clusterização utilizado para realização desse processo foi o HDBSCAN (Hierarchical Density-Based Spatial Clustering of Applications with Noise). Esse é um algoritmo baseado em densidade que permite detectar agrupamentos de diferentes tamanhos e identificar pontos que não pertencem a nenhum cluster.

   Os parâmetros testados foram o *min_cluster_size*, que é usado para determinar o número mínimo de pontos que um cluster deve ter para ser formado, e o segundo parâmetro foi o *min_samples*, que determina uma quantidade mínima de vizinhos que um ponto deve ter para ser considerado parte de um cluster. 

   Em relação aos parâmetros *min_cluster_size e* *min_samples*, foram feitos testes com diferentes combinações de valores nestes parâmetros e foi visto que a combinação que gerou o melhor resultado foi com o min_samples = 5 e o min_cluster_size = 5. 

   \
5. *Métricas de avaliação:*

   Foram utilizadas métricas de avaliação para avaliar os resultados gerados na clusterização, e as métricas são:
   * **Davies-Bouldin Index (DBI):** Esta métrica avalia a qualidade do agrupamento comparando a dispersão interna dos clusters (quão espalhados os pontos estão dentro de um cluster) com a separação entre clusters (quão distantes eles estão uns dos outros). Quanto mais compactos e bem separados os clusters, melhor o agrupamento. Se os clusters estiverem muito espalhados ou próximos uns dos outros, a qualidade do agrupamento é considerada pior. **A pontuação mínima é zero, com valores mais baixos indicando melhor separação e coesão dos clusters.**
   * **Calinski-Harabasz Index:** Esta métrica irá avaliar o quão separados os clusters estão uns dos outros (dispersão entre clusters) e o quão compactos os pontos estão dentro do mesmo cluster (dispersão intra clsuter). Ela tem a sua pontuação definida como a razão entre a soma da dispersão entre clusters e da dispersão dentro do cluster. **Um valor mais alto do índice CH significa que os clusters são densos e bem separados, embora não haja um valor de corte "aceitável".**
   * **Silhouette Score:** Esta métrica compara a proximidade dos pontos dentro do mesmo cluster e a distância para outros clusters. É calculada a distância média de um imóvel para os outros imóveis dentro do mesmo cluster e também é calculada a menor distância média do imóvel para qualquer outro cluster vizinho. De acordo com o Silhouette Score, quando os imóveis dentro do mesmo cluster forem parecidos e diferentes dos de outros clusters, isso aponta que a clusterização está bem feita. **A pontuação para denotar isso varia de -1 a 1, sendo 1 o melhor cenário e -1 o pior.**
   * **Taxa de Outliers:** A Taxa de Outliers é uma métrica que aponta a proporção de pontos de dados considerados como outliers (ruído) em relação ao total de pontos no conjunto de dados. Quanto mais baixa esta taxa, melhor.

     \
6. *Avaliação dos resultados na cidade de teste:*

    Com a aplicação dessa técnica foram obtidos os seguintes resultados nas métricas: 

   
   1. Silhouette Score: 0.707
   2. Davies-Bouldin Index: 0.304
   3. Calinski-Harabasz Index: 648.87
   4. Taxa de outliers: 8.76%

      \
7. *Avaliação dos resultados no estado de Minas Gerais:*

   Após a aplicação da clusterização geoespacial na cidade de Nova Lima, essa aplicação foi expandida para Minas Gerais. Foram realizados testes de diferentes combinações de valores nos parâmetros da técnica HDBSCAN e foi feito o uso das métricas de avaliação para ajustes e otimização dos resultados de clusterização generalizando para o estado de Minas Gerais. Os valores nas métricas permaneceram estáveis mesmo após essa expansão, indicando algo positivo, porém foi necessário fazer um ajuste nos parâmetros para min_cluster_size = 20 e  min_samples = 15. Nesse caso o melhor resultado encontrado foi:
   * Silhouette Score: 0.722
   * Davies-Bouldin Index: 0.356
   * Calinski-Harabasz Index: 195308.91
   * Taxa de Outliers: 30.23%

     \
8. *Definição do cálculo dos clusters vizinhos:* 

   Para identificar clusters vizinhos e expandir a busca para regiões próximas, foi utilizada a estrutura de árvore cKDTree, que permite a busca eficiente dos vizinhos mais próximos em um espaço multidimensional.

   Primeiramente, foram calculados os centróides dos clusters, obtidos pela média das coordenadas de latitude e longitude dos imóveis pertencentes a cada cluster.

   Em seguida, a estrutura cKDTree foi empregada para armazenar esses centróides e facilitar a busca dos vizinhos mais próximos. Em vez de comparar cada ponto individualmente, a árvore descarta regiões inteiras irrelevantes, tornando a busca mais eficiente.

   Por fim, para cada cluster, foram identificados os três clusters mais próximos geograficamente.

#### Expansão para englobar região de praia

Foi feita uma expansão primeiramente considerando a cidade de Florianópolis - Santa Catarina, por ter regiões de praia, e esse ponto ser alvo de observação na clusterização gerada.

Nessa expansão foram consideradas as cidades de Florianópolis - Santa Catarina e Nova Lima - Minas Gerais. Foram feitos novamente testes de diferentes combinações de valores de parâmetros da técnica HDBSCAN e foi feito também o uso das métricas de avaliação. 

Foi feito o ajuste de parâmetros para a expansão da região de praia e avaliado o resultado das diferentes métricas, e o melhor ponto de equilíbrio no momento resultou em:

* min_cluster_size: 50
* min_samples: 20
* Silhouette Score: 0.480 (sendo 1 o melhor cenário).
* Davies-Bouldin Index: 0.516 (sendo zero o melhor cenário).
* Calinski-Harabasz Index: 1.885718e+06 (sendo quanto mais alto melhor).	
* Taxa de Outliers: 15.74% (sendo quanto mais baixo melhor). 

  \
  Ou seja, a partir dos resultados das métricas, foi possível identificar que houve um decaimento na performance da clusterização. Também foi identificado que para lugares com densidades diferentes os melhores parâmetros podem mudar. Logo, foi adotada a abordagem de calcular a densidade de imóveis por cidade e posteriormente definir classes de densidade, sendo elas muito baixa, baixa, média, alta e muito alta, e aplicar o HDBSCAN para cada classe de densidade, encontrando o melhor conjunto de parâmetros para cada classe.

  É possível visualizar a diferença de densidades nas cidades que foram consideradas:

  ![](/api/attachments.redirect?id=502b70fa-53a4-4f1d-a612-7f3cdb6bad60 " =365x283")

 ![](/api/attachments.redirect?id=95763ade-ab88-42c1-a819-d693a33206db " =368x281")

#### Expansão para englobar todo o território nacional


1. *Análise dos dados:* 

   
   1. Foram identificados dados faltantes com valor = 'none' na coluna 'suburb' e na coluna 'city'.

      \
      ![](/api/attachments.redirect?id=6eae32d8-9f1f-4b73-b167-1d88309ac70e " =145x103")b. Também foram encontrados dados faltantes com valor = 'NaN'![](/api/attachments.redirect?id=dfe900af-8bed-4a89-a188-eed7099a244d " =142.5x103.5")

   \
2. *Segmentação por classes de densidade:*

   Ao tentar fazer a generalização do modelo ao expandir, foi notado que o maior problema era a diversidade de densidades de quantidade de ids nas regiões analisadas. Afim de melhorar a parametrização do modelo tornando ele generalista, identificamos a necessidade de segmentar o treinamento do modelo para diferentes classes de densidade, e encontrar a partir dos testes e resultados das métricas de avaliação, a melhor combinação de valores para os parâmetros do modelo a serem usados para a clusterização em cada classe. 

   \
   Foram feitos testes com diferentes métodos para o cálculo da classificação de densidade por cidade e definição de classes para a densidade como (muito baixa, baixa, média, alta e muito alta). O melhor resultado foi com o uso do log em conjunto com o min-max para normalização. 

   Aqui está a comparação dos histogramas para cada abordagem testada:

 ![](/api/attachments.redirect?id=7259565f-bf8b-42cc-8761-4f50631fb0b5)

Os intervalos para cada classe de densidade utilizando o Min-Max + Log resultou em:

| Classe de densidade | Quantidade mínima de imóveis | Quantidade máxima de imóveis |
|----|----|----|
| Muito Alta | 11284 | 26297 |
| Alta | 2468  | 8077 |
| Média | 231 | 2416 |
| Baixa  | 21 | 228 |
| Muito Baixa  | 1 | 20 |



3. *Testes para definir a melhor parametrização para cada classe de densidade:*

   Após a estruturação da classificação de densidades nas classes: muito baixa, baixa, média, alta e muito alta, foram feitos testes para encontrar os melhores parâmetros para cada subgrupo de densidade, e foram utilizadas métricas de avaliação como *Silhouette Score*, *Davies-Bouldin Index, Calinski-Harabasz Index* e *Taxa de Outlier*s. Os resultados para cada classe foram:

   \
   **Densidade muito baixa:**

   *min_cluster_size:* 10

   *min_samples:* 10

   *Silhouette Score:* 0.6878 (sendo 1 o melhor cenário).

   *Davies-Bouldin Index:* 0.3648 (sendo zero o melhor cenário).

   *Calinski-Harabasz Index:* 39816.1513 (sendo quanto mais alto melhor).

   *Taxa de Outliers:* 26.97% (sendo quanto mais baixo melhor).

   \
   **Densidade baixa:**

   *min_cluster_size:* 15

   *min_samples:* 15

   *Silhouette Score:* 0.7840 (sendo 1 o melhor cenário).

   *Davies-Bouldin Index:* 0.2817 (sendo zero o melhor cenário).

   *Calinski-Harabasz Index:* 2.410892e+06 (sendo quanto mais alto melhor).

   *Taxa de Outliers:* 16.18% (sendo quanto mais baixo melhor).

   \
   **Densidade média:**

   *min_cluster_size:* 20

   *min_samples:* 20

   *Silhouette Score:* 0.8224 (sendo 1 o melhor cenário).

   *Davies-Bouldin Index:* 0.2182 (sendo zero o melhor cenário).

   *Calinski-Harabasz Index:* 1.794899e+06 (sendo quanto mais alto melhor).

   *Taxa de Outliers:* 8.82% (sendo quanto mais baixo melhor).

   \
   **Densidade alta:**

   *min_cluster_size:* 50

   *min_samples:* 20

   *Silhouette Score:* 0.8040 (sendo 1 o melhor cenário).

   *Davies-Bouldin Index:* 0.2676 (sendo zero o melhor cenário).

   *Calinski-Harabasz Index:* 1.081758e+07 (sendo quanto mais alto melhor).

   *Taxa de Outliers:* 5.22% (sendo quanto mais baixo melhor).

   \
   **Densidade muito alta:**

   *min_cluster_size:* 50

   *min_samples:* 15

   *Silhouette Score:* 0.7711 (sendo 1 o melhor cenário).

   *Davies-Bouldin Index:* 0.4122 (sendo zero o melhor cenário).

   *Calinski-Harabasz Index:* 2.634984e+06 (sendo quanto mais alto melhor).

   *Taxa de Outliers:* 11.94% (sendo quanto mais baixo melhor).

   \
4. *Refinamento de Clusters Geoespaciais com Heurísticas Contextuais:*

Nessa etapa o foco foi no refinamento do modelo de clusterização geoespacial para o Brasil, incorporando heurísticas geográficas e contextuais para aprimorar a qualidade e relevância dos clusters para a análise de faturamento. A aplicação das heurísticas objetivaram evitar clusters entre cidades distintas e limitar a distância entre clusters vizinhos.

* Heurística de Limite de Cidades: 
  * Para a aplicação da heurística, primeiramente foram identificados os clusters que possuíam mais de uma cidade, isso para os clusters em cada classe de densidade. Após a identificação desses casos problemáticos, foi aplicada a correção em cada um deles, a partir de um loop que itera por cada cluster com múltiplas cidades e para cada cidade\ndentro dele atribui um novo ID, onde para evitar conflitos ou repetições os novos ids começam uma numeração após a última numeração de ID já existente nos clusters. (novo_cluster_id = max(clusters_existentes) + 1). 

Foi realizado, para cada classe de densidade, o mapeamento de casos que são alvos de melhoria a partir da aplicação da regra heurística de um cluster não se expandir para mais de uma cidade, para que após o desenvolvimento da regra isso fosse validado. Segue um exemplo:

Classe de densidade baixa:

Antes da heurística:

 ![Cluster contendo imóvel da cidade de Carlos Barbosa](/api/attachments.redirect?id=a59b3da8-5c3e-49cb-8d44-473fc168043d " =547.5x148")

 ![Cluster contendo imóvel da cidade de Farroupilha](/api/attachments.redirect?id=8a178354-835d-4e00-a514-f839e546dc0d " =462x175.5")

 ![Cluster contendo imóvel da cidade de Garibaldi](/api/attachments.redirect?id=5059b785-71fd-4f35-922f-f54763e426c7 " =482.5x169")

Depois da heurística:

 ![Cluster separado contendo apenas imóveis da cidade de Garibaldi](/api/attachments.redirect?id=1e077986-b196-44bc-bdc8-c8d24ea45813 " =495x173.5")

 ![Cluster separado contendo apenas imóveis da cidade de Carlos Barbosa](/api/attachments.redirect?id=47a68443-31b8-4964-b58a-13061d13dc7c " =562.5x149")

 ![Cluster separado contendo apenas imóveis da cidade de Farroupilha](/api/attachments.redirect?id=56dba397-0605-4a46-9a4c-6659833104a2 " =449x171")

* Heurística de Distância Máxima entre Clusters Vizinhos
  * O objetivo da aplicação desta heurística é garantir que exista uma distância máxima para considerar clusters vizinhos. Isso é importante pois clusters considerados vizinhos podem, na prática, estar a uma distância geográfica significativa, o que prejudica análises de proximidade. Para evitar isso, foi feita a definição de um limite máximo de distância para considerar a vizinhança relevante.
  * Para a aplicação da heurística, foram testados diferentes valores para o parâmetro de "max_dist_km", mais especificamente sendo eles: None, 1, 2, 3, 5, 7, 10, 12, 15, 20, 25. E os testes com esses valores foram feitos para cada classe de densidade considerando também métricas de distância.
  * Foram aplicados diferentes valores de distância máxima e foi calculada a média da distância entre os clusters vizinhos (quanto menor, melhor, pois indica que os clusters estão mais compactos.) e a distribuição de clusters vizinhos em cada classe de densidade, para encontrar um equilíbrio entre a distância menor possível, para que se tenham os vizinhos próximos e uma distribuição que tenha a maior quantidade possível de casos com 3 vizinhos.


1. Classe de densidade muito baixa: max_dist_km = 15. 

* Mantém a média das distâncias entre clusters vizinhos mais baixa possível (**21.06** km). Anteriormente, **sem a aplicação da heurística** a média estava em (**34.93**).


* Distribuição do número de vizinhos: 1 vizinho - 4144 casos; 2 vizinhos - 2440 casos; 3 vizinhos - 1912 casos


2. Classe de densidade baixa: max_dist_km = 10.

* Minimiza a média das distâncias entre clusters vizinhos (**15.81**). Anteriormente, **sem a aplicação da heurística** a média estava em (**30.91).**
* Distribuição do número de vizinhos: 1 vizinho - 20246 casos; 2 vizinhos - 7450 casos; 3 vizinhos - 3077 casos


3. Classe de densidade média: max_dist_km = 7.

* A partir de max_dist_km = 7, o número de mudanças começa a diminuir gradativamente. Neste ponto, a média das distâncias entre clusters vizinhos é  (**8.14**) ,  e apesar de a menor média ocorre em max_dist_km = 5 (7.97), sugerindo um ponto ótimo, é visto que as médias são próximas. Anteriormente, **sem a aplicação da heurística** a média estava em (**18.68)**.
* Além disso,  a distribuição do número de clusters vizinhos é melhor para max_dist_km = 7, apontando um maior potencial de abrangência da vizinhança quando necessário.
* Distribuição do número de vizinhos: 1 vizinho - 49204 casos ; 2 vizinhos - 19729 casos; 3 vizinhos - 64862 casos


4. Classe de densidade alta: max_dist_km = 5.

* max_dist_km = 3 apresenta a menor média de distâncias entre clusters vizinhos (3.83), o que indica uma maior proximidade entre os clusters vizinhos. Já max_dist_km = 5 possui uma média um pouco maior (**4.13**), mas ainda assim mantém uma média de distâncias baixa. Anteriormente, **sem a aplicação da heurística** a média estava em (**6.50)**.
* Outro fator que contribui para max_dist_km = 5 ser preferível é que, com esse valor, a maioria dos clusters já passa a ter 3 vizinhos, indicando uma melhor distribuição.
* Distribuição do número de vizinhos: 1 vizinho - 22794 casos; 2 vizinhos - 11104 casos; 3 vizinhos - 93384 casos.


5. Classe de densidade muito alta: max_dist_km = 3.

* max_dist_km = 3 possui uma das menores médias, ficando com a média de distâncias entre clusters vizinhos em (**1.82**). Anteriormente, **sem a aplicação da heurística** a média estava em (**2.32).**
* Além disso, a distribuição de vizinhos está equilibrada, com boa proporção entre 1, 2 e 3 vizinhos, priorizando o maior número possível de ocorrências com 3 vizinhos. Distribuição do número de vizinhos: 1 vizinho - 11491 casos; 2 vizinhos - 5796 casos; 3 vizinhos - 64147 casos.


#### Implementação dos resultados na planilha de teste 


1. Foi colocado o novo parquet ("dados_brasil.parquet") com os dados expandidos a nível brasil no bucket s3;


2. ![](/api/attachments.redirect?id=f18e7fcc-50b5-4f99-b064-c6396f366621 " =823.5x202.5")Foi executado o crawler "location_mg" manualmente;

   \
   ![](/api/attachments.redirect?id=7f2abbed-3456-453b-80bf-84d3cf20ccb8 " =959x359")
3. Foi feita a atualização manual da tabela no athena e foi feita uma consulta com os novos dados no athena;

 ![](/api/attachments.redirect?id=68ced863-d8c2-4480-b430-a326fe88c658 " =599x275.5")


#### Testes e validação dos resultados na planilha de teste 

Foram feitos testes na planilha anterior a inclusão da clusterização geoespacial e foram feitos testes na planilha mais atualizada que já conta com a inclusão desse projeto. Segue um exemplo:

Resultados de um exemplo de busca na planilha anterior:

 ![](/api/attachments.redirect?id=42dfd8f5-5d8b-4c0c-a9b9-c0e36bd8d3c2 " =646x386")

 ![](/api/attachments.redirect?id=8ac949b7-b55d-4c59-9cd5-361f62f2f3df " =956.5x161")

Resultados do mesmo exemplo de busca na planilha que conta com a parte de clusterização geoespacial:

 ![](/api/attachments.redirect?id=9b2a81d2-6330-4bc9-b957-69b93feaad3a " =446x371")

 ![](/api/attachments.redirect?id=04eae2f7-4860-435c-9c23-845c06bf5035 " =958.5x286")

 ![](/api/attachments.redirect?id=4cddc8d1-7d86-4ffe-9498-b707616b009a " =583x406")


Outro exemplo:

Resultados de um exemplo de busca na planilha anterior:


 ![](/api/attachments.redirect?id=6f0dc916-c5e7-49dc-a73d-84cedbeadeb7 " =358.5x376")

 ![](/api/attachments.redirect?id=b9da249f-96cb-40d7-82d8-2df011af10ed " =956.5x253.5")

Resultados do mesmo exemplo de busca na planilha que conta com a parte de clusterização geoespacial:

 ![](/api/attachments.redirect?id=fd638edc-e136-4491-9432-d147c455d72d " =418x363")

 ![](/api/attachments.redirect?id=59ef3fe6-080a-4d0f-875c-55c80c71ae97 " =951.5x410.5")

 ![](/api/attachments.redirect?id=53f761ac-b26e-4d3e-9b60-44799dffa559 " =590.5x393")

 ![](/api/attachments.redirect?id=0b2a05f2-ae0c-40b8-b216-9ab660de9050 " =596x405")

 ![](/api/attachments.redirect?id=6147c3b1-34ad-4096-b8b1-6c4de7d9724c " =775x421")


\