<!-- title: Definição do Escopo de Dados e Coleta | url: https://outline.seazone.com.br/doc/definicao-do-escopo-de-dados-e-coleta-EhSebjrnsx | area: Tecnologia -->

# Definição do Escopo de Dados e Coleta

* Contexto
* Dados coletados para análise
* Período delimitado de análise
* Dataset para análise


# [Contexto](/doc/contexto-UynZ5gnhJp)

De acordo com o pipeline atual, o faturamento dos imóveis é dado através da análise dos bloqueios do imóvel.  Atualmente, enfrentamos um problema oriundo dessa análise de bloqueios onde, por inúmeros fatores, o faturamento do imóvel excede os limites de faturamento estabelecidos (foge do esperado). Esses casos são denominados anomalias de faturamento. No surgimento deste problema, faz-se necessário um estudo de proposta de uma solução. Com isso, a primeira etapa para que a proposta seja feita é a realização de um estudo exploratório nos dados que descrevem os faturamentos dos imóveis. E para isso, é preciso delimitar quais informações e escopo de tempo sobre esses dados serão analisados, para caracterizar essas anomalias.


# [Dados coletados para análise](/doc/dados-coletados-para-analise-i3VeCpDsF4)

A priori, foi analisado que entender o faturamento esperado de um imóvel uma informação importante seria visualizar a disponibilidade do imóvel dentre um período de tempo. Por isso, foi escolhida a tabela `booked_on` da camada **enriched**. Visto que, através da tabela em questão é possível observar os aspectos característicos de uma reserva naquele imóvel como, a quantidade mínima de estadia no imóvel, taxas de limpeza e o valor da diária do imóvel. Além disso, a tabela fornece informações sobre o "status" do imóvel e predições do nosso pipeline se aquele imóvel está ocupado ou não. 

Com isso, faz-se necessário relacionar as informações de bloqueio citadas anteriormente com as informações de faturamento. Para isso, esses dados foram relacionados com o faturamento diário dos imóveis, presentes na tabela `daily_fat` da camada **enriched** que armazena os dados de faturamento diário dos imóveis. 

Essa relação foi feita, devido a granularidade diária de ambas as tabelas. Sendo assim, a definição do escopo do tempo seria mais livre já que possuímos um grande volume de dados para janelas de semanas ou meses.

Além disso, foram selecionadas dados importantes dos imóveis retirados da camada **clean**, são eles: owner, número de quartos, amenities, número de banheiros, números de camas, rating, núumero de review e o tipo de listing. Que se tratam de dados importantes ao olhar para os bloqueios e faturamentos e estabelece uma amostragem de comparação dos imóveis por proprietário. Há regras específicas para as quais devemos coletar os dados, das quais são elas:

* Apartamento ou Casa (não devemos analisar imóveis do tipo motel);
* 0 a 3 quartos (Aqui 0 quartos são estúdios, muito importante para a analise);
* Nota do anúncio >= 4,5;
* Número de reviews > 10;


# [Período delimitado de análise](/doc/periodo-delimitado-de-analise-TdZxTnP0Ug)

O escopo de tempo delimitado foi pensado dando uma abertura anual na disponibilidade do imóvel, ou seja, a disponibilidade do imóvel ao longo de meses no período de um ano, porém estabelecendo um limite no volume de dados a serem extraídos. Visto que, o número de imóveis disponíveis fica em torno dos 120mil imóveis. Ao relacionar essa quantidade de imóveis com registro diário de bloqueio, faturamento e etc. ao longo de 365 dias, ou seja, cerca 43 milhões de registros a serem analisados. Por isso, a análise foi restringida a 1% a 5% dos número de imóveis por região, de acordo com a consulta abaixo:

```sql
(SELECT 
          distinct airbnb_listing_id,
          amenities,
          number_of_bathrooms,
          number_of_bedrooms,
          number_of_beds, 
          star_rating,
          number_of_reviews, 
          owner_id,
          listing_type, 
          state, country, 
          city
          FROM details_and_location_last_aquisition  
          WHERE ano='2024'
          and is_dead = false
          and listing_type != 'hotel'
          and number_of_bedrooms <= 3
          and star_rating >= 4.5
          and number_of_reviews >= 10
          and country = 'Brasil' 
          and state = 'Acre'
          LIMIT 70)
     UNION ALL (SELECT 
          distinct airbnb_listing_id,
          amenities,
          number_of_bathrooms,
          number_of_bedrooms,
          number_of_beds, 
          star_rating,
          number_of_reviews, 
          owner_id,
          listing_type, 
          state, country, 
          city
          FROM details_and_location_last_aquisition  
          WHERE ano='2024'
          and is_dead = false
          and listing_type != 'hotel'
          and number_of_bedrooms <= 3
          and star_rating >= 4.5
          and number_of_reviews >= 10
          and country = 'Brasil' 
          and state = 'Alagoas'
          LIMIT 375)
     UNION ALL (SELECT 
          distinct airbnb_listing_id,
          amenities,
          number_of_bathrooms,
          number_of_bedrooms,
          number_of_beds, 
          star_rating,
          number_of_reviews, 
          owner_id,
          listing_type, 
          state, country, 
          city
          FROM details_and_location_last_aquisition  
          WHERE ano='2024'
          and is_dead = false
          and listing_type != 'hotel'
          and number_of_bedrooms <= 3
          and star_rating >= 4.5
          and number_of_reviews >= 10
          and country = 'Brasil' 
          and state = 'Amapá'
          LIMIT 90)
     UNION ALL (SELECT 
          distinct airbnb_listing_id,
          amenities,
          number_of_bathrooms,
          number_of_bedrooms,
          number_of_beds, 
          star_rating,
          number_of_reviews, 
          owner_id,
          listing_type, 
          state, country, 
          city
          FROM details_and_location_last_aquisition  
          WHERE ano='2024'
          and is_dead = false
          and listing_type != 'hotel'
          and number_of_bedrooms <= 3
          and star_rating >= 4.5
          and number_of_reviews >= 10
          and country = 'Brasil' 
          and state = 'Amazonas'
          LIMIT 80)
     UNION ALL (SELECT 
          distinct airbnb_listing_id,
          amenities,
          number_of_bathrooms,
          number_of_bedrooms,
          number_of_beds, 
          star_rating,
          number_of_reviews, 
          owner_id,
          listing_type, 
          state, country, 
          city
          FROM details_and_location_last_aquisition  
          WHERE ano='2024'
          and is_dead = false
          and listing_type != 'hotel'
          and number_of_bedrooms <= 3
          and star_rating >= 4.5
          and number_of_reviews >= 10
          and country = 'Brasil' 
          and state = 'Bahia'
          and city != 'Porto Seguro'
          LIMIT 1544)
     UNION ALL (SELECT 
          distinct airbnb_listing_id,
          amenities,
          number_of_bathrooms,
          number_of_bedrooms,
          number_of_beds, 
          star_rating,
          number_of_reviews, 
          owner_id,
          listing_type, 
          state, country, 
          city
          FROM details_and_location_last_aquisition  
          WHERE ano='2024'
          and is_dead = false
          and listing_type != 'hotel'
          and number_of_bedrooms <= 3
          and star_rating >= 4.5
          and number_of_reviews >= 10
          and country = 'Brasil' 
          and state = 'Ceará'
          LIMIT 558)
     UNION ALL (SELECT 
          distinct airbnb_listing_id,
          amenities,
          number_of_bathrooms,
          number_of_bedrooms,
          number_of_beds, 
          star_rating,
          number_of_reviews, 
          owner_id,
          listing_type, 
          state, country, 
          city
          FROM details_and_location_last_aquisition  
          WHERE ano='2024'
          and is_dead = false
          and listing_type != 'hotel'
          and number_of_bedrooms <= 3
          and star_rating >= 4.5
          and number_of_reviews >= 10
          and country = 'Brasil' 
          and state = 'Distrito Federal'
          LIMIT 262)
     UNION ALL (SELECT 
          distinct airbnb_listing_id,
          amenities,
          number_of_bathrooms,
          number_of_bedrooms,
          number_of_beds, 
          star_rating,
          number_of_reviews, 
          owner_id,
          listing_type, 
          state, country, 
          city
          FROM details_and_location_last_aquisition  
          WHERE ano='2024'
          and is_dead = false
          and listing_type != 'hotel'
          and number_of_bedrooms <= 3
          and star_rating >= 4.5
          and number_of_reviews >= 10
          and country = 'Brasil' 
          and state = 'Espírito Santo'
          LIMIT 541)
     UNION ALL (SELECT 
          distinct airbnb_listing_id,
          amenities,
          number_of_bathrooms,
          number_of_bedrooms,
          number_of_beds, 
          star_rating,
          number_of_reviews, 
          owner_id,
          listing_type, 
          state, country, 
          city
          FROM details_and_location_last_aquisition  
          WHERE ano='2024'
          and is_dead = false
          and listing_type != 'hotel'
          and number_of_bedrooms <= 3
          and star_rating >= 4.5
          and number_of_reviews >= 10
          and country = 'Brasil' 
          and state = 'Goiás'
          LIMIT 638)
     UNION ALL (SELECT 
          distinct airbnb_listing_id,
          amenities,
          number_of_bathrooms,
          number_of_bedrooms,
          number_of_beds, 
          star_rating,
          number_of_reviews, 
          owner_id,
          listing_type, 
          state, country, 
          city
          FROM details_and_location_last_aquisition  
          WHERE ano='2024'
          and is_dead = false
          and listing_type != 'hotel'
          and number_of_bedrooms <= 3
          and star_rating >= 4.5
          and number_of_reviews >= 10
          and country = 'Brasil' 
          and state = 'Maranhão'
          LIMIT 108)
     UNION ALL (SELECT 
          distinct airbnb_listing_id,
          amenities,
          number_of_bathrooms,
          number_of_bedrooms,
          number_of_beds, 
          star_rating,
          number_of_reviews, 
          owner_id,
          listing_type, 
          state, country, 
          city
          FROM details_and_location_last_aquisition  
          WHERE ano='2024'
          and is_dead = false
          and listing_type != 'hotel'
          and number_of_bedrooms <= 3
          and star_rating >= 4.5
          and number_of_reviews >= 10
          and country = 'Brasil' 
          and state = 'Mato Grosso'
          LIMIT 128)
     UNION ALL (SELECT 
          distinct airbnb_listing_id,
          amenities,
          number_of_bathrooms,
          number_of_bedrooms,
          number_of_beds, 
          star_rating,
          number_of_reviews, 
          owner_id,
          listing_type, 
          state, country, 
          city
          FROM details_and_location_last_aquisition  
          WHERE ano='2024'
          and is_dead = false
          and listing_type != 'hotel'
          and number_of_bedrooms <= 3
          and star_rating >= 4.5
          and number_of_reviews >= 10
          and country = 'Brasil' 
          and state = 'Mato Grosso do Sul'
          LIMIT 107)
     UNION ALL (SELECT 
          distinct airbnb_listing_id,
          amenities,
          number_of_bathrooms,
          number_of_bedrooms,
          number_of_beds, 
          star_rating,
          number_of_reviews, 
          owner_id,
          listing_type, 
          state, country, 
          city
          FROM details_and_location_last_aquisition  
          WHERE ano='2024'
          and is_dead = false
          and listing_type != 'hotel'
          and number_of_bedrooms <= 3
          and star_rating >= 4.5
          and number_of_reviews >= 10
          and country = 'Brasil' 
          and state = 'Minas Gerais'
          LIMIT 1412)
     UNION ALL (SELECT 
          distinct airbnb_listing_id,
          amenities,
          number_of_bathrooms,
          number_of_bedrooms,
          number_of_beds, 
          star_rating,
          number_of_reviews, 
          owner_id,
          listing_type, 
          state, country, 
          city
          FROM details_and_location_last_aquisition  
          WHERE ano='2024'
          and is_dead = false
          and listing_type != 'hotel'
          and number_of_bedrooms <= 3
          and star_rating >= 4.5
          and number_of_reviews >= 10
          and country = 'Brasil' 
          and state = 'Pará'
          LIMIT 181)
     UNION ALL (SELECT 
          distinct airbnb_listing_id,
          amenities,
          number_of_bathrooms,
          number_of_bedrooms,
          number_of_beds, 
          star_rating,
          number_of_reviews, 
          owner_id,
          listing_type, 
          state, country, 
          city
          FROM details_and_location_last_aquisition  
          WHERE ano='2024'
          and is_dead = false
          and listing_type != 'hotel'
          and number_of_bedrooms <= 3
          and star_rating >= 4.5
          and number_of_reviews >= 10
          and country = 'Brasil' 
          and state = 'Paraíba'
          LIMIT 387)
     UNION ALL (SELECT 
          distinct airbnb_listing_id,
          amenities,
          number_of_bathrooms,
          number_of_bedrooms,
          number_of_beds, 
          star_rating,
          number_of_reviews, 
          owner_id,
          listing_type, 
          state, country, 
          city
          FROM details_and_location_last_aquisition  
          WHERE ano='2024'
          and is_dead = false
          and listing_type != 'hotel'
          and number_of_bedrooms <= 3
          and star_rating >= 4.5
          and number_of_reviews >= 10
          and country = 'Brasil' 
          and state = 'Paraná'
          LIMIT 809)
     UNION ALL (SELECT 
          distinct airbnb_listing_id,
          amenities,
          number_of_bathrooms,
          number_of_bedrooms,
          number_of_beds, 
          star_rating,
          number_of_reviews, 
          owner_id,
          listing_type, 
          state, country, 
          city
          FROM details_and_location_last_aquisition  
          WHERE ano='2024'
          and is_dead = false
          and listing_type != 'hotel'
          and number_of_bedrooms <= 3
          and star_rating >= 4.5
          and number_of_reviews >= 10
          and country = 'Brasil' 
          and state = 'Pernambuco'
          LIMIT 704)
     UNION ALL (SELECT 
          distinct airbnb_listing_id,
          amenities,
          number_of_bathrooms,
          number_of_bedrooms,
          number_of_beds, 
          star_rating,
          number_of_reviews, 
          owner_id,
          listing_type, 
          state, country, 
          city
          FROM details_and_location_last_aquisition  
          WHERE ano='2024'
          and is_dead = false
          and listing_type != 'hotel'
          and number_of_bedrooms <= 3
          and star_rating >= 4.5
          and number_of_reviews >= 10
          and country = 'Brasil' 
          and state = 'Piauí'
          LIMIT 69)
     UNION ALL (SELECT 
          distinct airbnb_listing_id,
          amenities,
          number_of_bathrooms,
          number_of_bedrooms,
          number_of_beds, 
          star_rating,
          number_of_reviews, 
          owner_id,
          listing_type, 
          state, country, 
          city
          FROM details_and_location_last_aquisition  
          WHERE ano='2024'
          and is_dead = false
          and listing_type != 'hotel'
          and number_of_bedrooms <= 3
          and star_rating >= 4.5
          and number_of_reviews >= 10
          and country = 'Brasil' 
          and state = 'Rio de Janeiro'
          LIMIT 4041)
     UNION ALL (SELECT 
          distinct airbnb_listing_id,
          amenities,
          number_of_bathrooms,
          number_of_bedrooms,
          number_of_beds, 
          star_rating,
          number_of_reviews, 
          owner_id,
          listing_type, 
          state, country, 
          city
          FROM details_and_location_last_aquisition  
          WHERE ano='2024'
          and is_dead = false
          and listing_type != 'hotel'
          and number_of_bedrooms <= 3
          and star_rating >= 4.5
          and number_of_reviews >= 10
          and country = 'Brasil' 
          and state = 'Rio Grande do Norte'
          LIMIT 337)
     UNION ALL (SELECT 
          distinct airbnb_listing_id,
          amenities,
          number_of_bathrooms,
          number_of_bedrooms,
          number_of_beds, 
          star_rating,
          number_of_reviews, 
          owner_id,
          listing_type, 
          state, country, 
          city
          FROM details_and_location_last_aquisition  
          WHERE ano='2024'
          and is_dead = false
          and listing_type != 'hotel'
          and number_of_bedrooms <= 3
          and star_rating >= 4.5
          and number_of_reviews >= 10
          and country = 'Brasil' 
          and state = 'Rio Grande do Sul'
          LIMIT 1265)
     UNION ALL (SELECT 
          distinct airbnb_listing_id,
          amenities,
          number_of_bathrooms,
          number_of_bedrooms,
          number_of_beds, 
          star_rating,
          number_of_reviews, 
          owner_id,
          listing_type, 
          state, country, 
          city
          FROM details_and_location_last_aquisition  
          WHERE ano='2024'
          and is_dead = false
          and listing_type != 'hotel'
          and number_of_bedrooms <= 3
          and star_rating >= 4.5
          and number_of_reviews >= 10
          and country = 'Brasil' 
          and state = 'Rondônia'
          LIMIT 18)
     UNION ALL (SELECT 
          distinct airbnb_listing_id,
          amenities,
          number_of_bathrooms,
          number_of_bedrooms,
          number_of_beds, 
          star_rating,
          number_of_reviews, 
          owner_id,
          listing_type, 
          state, country, 
          city
          FROM details_and_location_last_aquisition  
          WHERE ano='2024'
          and is_dead = false
          and listing_type != 'hotel'
          and number_of_bedrooms <= 3
          and star_rating >= 4.5
          and number_of_reviews >= 10
          and country = 'Brasil' 
          and state = 'Roraima'
          LIMIT 21)
     UNION ALL (SELECT 
          distinct airbnb_listing_id,
          amenities,
          number_of_bathrooms,
          number_of_bedrooms,
          number_of_beds, 
          star_rating,
          number_of_reviews, 
          owner_id,
          listing_type, 
          state, country, 
          city
          FROM details_and_location_last_aquisition  
          WHERE ano='2024'
          and is_dead = false
          and listing_type != 'hotel'
          and number_of_bedrooms <= 3
          and star_rating >= 4.5
          and number_of_reviews >= 10
          and country = 'Brasil' 
          and state = 'Santa Catarina'
          LIMIT 3000)
     UNION ALL (SELECT 
          distinct airbnb_listing_id,
          amenities,
          number_of_bathrooms,
          number_of_bedrooms,
          number_of_beds, 
          star_rating,
          number_of_reviews, 
          owner_id,
          listing_type, 
          state, country, 
          city
          FROM details_and_location_last_aquisition  
          WHERE ano='2024'
          and is_dead = false
          and listing_type != 'hotel'
          and number_of_bedrooms <= 3
          and star_rating >= 4.5
          and number_of_reviews >= 10
          and country = 'Brasil' 
          and state = 'São Paulo'
          LIMIT 5000)
     UNION ALL (SELECT 
          distinct airbnb_listing_id,
          amenities,
          number_of_bathrooms,
          number_of_bedrooms,
          number_of_beds, 
          star_rating,
          number_of_reviews, 
          owner_id,
          listing_type, 
          state, country, 
          city
          FROM details_and_location_last_aquisition  
          WHERE ano='2024'
          and is_dead = false
          and listing_type != 'hotel'
          and number_of_bedrooms <= 3
          and star_rating >= 4.5
          and number_of_reviews >= 10
          and country = 'Brasil' 
          and state = 'Sergipe'
          LIMIT 97)
     UNION ALL (SELECT 
          distinct airbnb_listing_id,
          amenities,
          number_of_bathrooms,
          number_of_bedrooms,
          number_of_beds, 
          star_rating,
          number_of_reviews, 
          owner_id,
          listing_type, 
          state, country, 
          city
          FROM details_and_location_last_aquisition  
          WHERE ano='2024'
          and is_dead = false
          and listing_type != 'hotel'
          and number_of_bedrooms <= 3
          and star_rating >= 4.5
          and number_of_reviews >= 10
          and country = 'Brasil' 
          and state = 'Bahia'
          and city = 'Porto Seguro'
          LIMIT 1105)
     UNION ALL (SELECT 
          distinct airbnb_listing_id,
          amenities,
          number_of_bathrooms,
          number_of_bedrooms,
          number_of_beds, 
          star_rating,
          number_of_reviews, 
          owner_id,
          listing_type, 
          state, country, 
          city
          FROM details_and_location_last_aquisition  
          WHERE ano='2024'
          and is_dead = false
          and listing_type != 'hotel'
          and number_of_bedrooms <= 3
          and star_rating >= 4.5
          and number_of_reviews >= 10
          and country = 'Brasil' 
          and state = 'Tocantins'
          LIMIT 37)
    
```

A consulta foi feita na união de subquerries, visto que restringir os estados à um número exato (ex: 1000 registros) seria uma péssima amostragem a alguns estados como São Paulo, 0,002% do número de imóveis no estado, e uma ótima amostragem para outros como Amazonas, 100% do número de imóveis no estado. 

O dataset final resultante foi de 22mil imóveis.


## Consulta dos dados de bloqueio por região

Com a amostragem de imóveis por estados disposta, o próximo passo é a extração diária dos dados de bloqueio e faturamento. 

A consulta dos dados diários para todos os estados ao mesmo tempo, gera um problema de volume de dados muito parecido com a situação anterior. Com isso, a forma mais lógica de quebrar essas consulta é dividindo os estados pela região do território nacional: norte, sul, nordeste, sudeste, centro-oeste. Com isso, as consultas foram realizadas desta forma:

### Região Norte

```sql
select * from block_and_occupancy bao
join daily_fat df on df.airbnb_listing_id = bao.airbnb_listing_id
where bao.available='false'
and bao.airbnb_listing_id in (SELECT distinct airbnb_listing_id  FROM details_and_location_last_aquisition  
 WHERE ano = '2024'
   AND is_dead = false
   AND listing_type != 'hotel'
   AND number_of_bedrooms <= 3
   AND star_rating >= 4.5
   AND number_of_reviews >= 10
   AND country = 'Brasil' 
   AND city != 'Porto Seguro'
   AND state IN ('Acre', 'Amapá', 'Amazonas', 'Pará', 'Rondônia', 'Roraima', 'Tocantins')
 LIMIT 1000)
and bao.year=2023
and df.year=2023
and bao.month<=12
and df.month<=12
```

### Região Sudeste

```sql
select * from block_and_occupancy bao
join daily_fat df on df.airbnb_listing_id = bao.airbnb_listing_id
where bao.available='false'
and bao.airbnb_listing_id in (SELECT distinct airbnb_listing_id  FROM details_and_location_last_aquisition  
 WHERE ano = '2024'
   AND is_dead = false
   AND listing_type != 'hotel'
   AND number_of_bedrooms <= 3
   AND star_rating >= 4.5
   AND number_of_reviews >= 10
   AND country = 'Brasil' 
   AND city != 'Porto Seguro'
   AND state IN ('Espírito Santo', 'Minas Gerais', 'Rio de Janeiro', 'São Paulo')
 LIMIT 10400)
and bao.year=2023
and df.year=2023
and bao.month<=12
and df.month<=12
```

### Região Nordeste

```sql
select * from block_and_occupancy bao
join daily_fat df on df.airbnb_listing_id = bao.airbnb_listing_id
where bao.available='false'
and bao.airbnb_listing_id in (SELECT distinct airbnb_listing_id  FROM details_and_location_last_aquisition  
 WHERE ano = '2024'
   AND is_dead = false
   AND listing_type != 'hotel'
   AND number_of_bedrooms <= 3
   AND star_rating >= 4.5
   AND number_of_reviews >= 10
   AND country = 'Brasil' 
   AND city != 'Porto Seguro'
   AND state IN ('Alagoas', 'Bahia', 'Ceará', 'Maranhão', 'Paraíba', 'Pernambuco', 'Piauí', 'Rio Grande do Norte', 'Sergipe')
 LIMIT 4000)
and bao.year=2023
and df.year=2023
and bao.month<=12
and df.month<=12
```

### Região Sul

```sql
select * from block_and_occupancy bao
join daily_fat df on df.airbnb_listing_id = bao.airbnb_listing_id
where bao.available='false'
and bao.airbnb_listing_id in (SELECT distinct airbnb_listing_id  FROM details_and_location_last_aquisition  
 WHERE ano = '2024'
   AND is_dead = false
   AND listing_type != 'hotel'
   AND number_of_bedrooms <= 3
   AND star_rating >= 4.5
   AND number_of_reviews >= 10
   AND country = 'Brasil' 
   AND state IN ('Paraná', 'Rio Grande do Sul', 'Santa Catarina')
 LIMIT 5000)
and bao.year=2023
and df.year=2023
and bao.month<=12
and df.month<=12


```


### Região Centro Oeste

```sql
select * from block_and_occupancy bao
join daily_fat df on df.airbnb_listing_id = bao.airbnb_listing_id
where bao.available='false'
and bao.airbnb_listing_id in (SELECT distinct airbnb_listing_id  FROM details_and_location_last_aquisition  
 WHERE ano = '2024'
   AND is_dead = false
   AND listing_type != 'hotel'
   AND number_of_bedrooms <= 3
   AND star_rating >= 4.5
   AND number_of_reviews >= 10
   AND country = 'Brasil' 
   AND state IN ('Distrito Federal', 'Goiás', 'Mato Grosso', 'Mato Grosso do Sul')
 LIMIT 1000)
and bao.year=2023
and df.year=2023
and bao.month<=12
and df.month<=12
```