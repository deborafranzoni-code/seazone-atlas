<!-- title: Catálogo externo de Dados do Pipe | url: https://outline.seazone.com.br/doc/catalogo-externo-de-dados-do-pipe-Yr8aRMTdfl | area: Tecnologia -->

# Catálogo externo de Dados do Pipe

# Introdução

O Pipe é quem, entre outras coisas, cuida das bases de dados do Airbnb, OLX, Vivareal e Booking (*em construção*) que a Seazone utiliza em inúmeros processos.

Para dar visibilidades às outras equipes quanto aos dados que elas têm acesso por meio do Pipe, está sendo criado este Catálogo de Dados.

## Dados e os seus desafios

No que diz respeito aos dados, temos 3 grandes desafios:

### **Aquisição de dados em escala:**

Todos os dados que fornecemos são publicamente acessíveis e podem ser pegos nas respectivas plataformas, mas obviamente que **fazer isso acontecer para o Brasil inteiro, todos os dias,** não é uma tarefa que pode ser feita manualmente, e é aí que o time do Pipe entra.

Com **scrapers** eficientes e rápidos, processos de Engenharia de Dados e utilizando as vantagens da computação e armazenamento na nuvem (*utilizamos AWS!*) conseguimos fazer isso acontecer. Todos os dias scrapamos dados de mais de 420.000 anúncios no Airbnb, XXXX na OLX e YYYY no Vivareal. Esses dados variam desde preço e disponibilidade de diárias, passando por detalhes do imóvel (número de quartos, mobília, ar condicionado etc) até regras de hospedagem (número máximo de hóspedes, se pode ou não fumar etc).

### **Inteligência:**

Mais do que adquirir adquirir essa infinidade de dados, muitas vezes é preciso utilizar alguns métodos que extraiam informações "escondidas", que não estão disponíveis diretamente: é o caso de saber **se um imóvel qualquer do Airbnb foi alugado ou não**.

Essa é uma informação que **apenas o dono daquele anúncio possui com 100% de certeza**, mas **nós podemos utilizar nossos dados diários para conseguir essa informação com uma precisão bem boa**. Nós basicamente comparamos o calendário de disponibilidade do imóvel hoje com o de ontem e com isso sabemos se o imóvel foi ou não alugado (mas tem 1 fator que complica bastante essa história, mais sobre isso aqui).

### **Compartilhamento dos dados:**

Finalmente, de nada adiantaria pegar dados apenas por pegar (por mais que o desafio de fazer isso seja super legal). Dados não valem nada se não forem utilizados da forma correta, e também é nossa responsabilidade auxiliar os outros times da Seazone no uso deste dados.

Isso passa desde gerar dados agrupados/filtrados de alguma maneira que uma área esteja precisando (nós chamamos esses pedidos de dados de sorvete, e cada tipo diferente de pedido é um [Sabor de Sorvete](/doc/sorveteria-de-dados-n0Gi0dQDpg) diferente), mas também em dar visibilidade para QUAIS dados as outras áreas podem utilizar.

Um Seazoner de qualquer outra área deve saber quais dados a gente consegue fornecer, assim ele pode ter ideias legais para explorar esses dados ou já partir para uma solicitação de sabor de sorvete caso a ideia já esteja formada.

***O objetivo, no fim, é gerar valor para as outras áreas com os nosso dados.***

# Onde os dados vivem

Os dados do Pipe ficam num Data Lake que vive no ambiente cloud da Amazon, a AWS. Dessa maneira os dados ficam seguros e todo mundo tem acesso, já que eles não ficam restritos ao computador de uma pessoa.

O nosso Data Lake é dividido em 5 partes:

* a **camada Raw** (do inglês "cru"): dados sem tratamento algum, do mesmo jeito que eles foram scrapados;
* a **camada Clean** (do inglês "limpo"): dados tratados para remover erros, duplicatas etc;
* a **camada Enriched** (do inglês "enriquecido"): dados que passaram por algum processo de inteligência para extrair informações "escondidas", agregar dados de mais de 1 lugar diferente etc;
* a **camada Models** (do inglês "modelos"): dados que passaram por algum modelo estatístico ou de Machine Learning para gerar informações ainda mais valiosas;
* a **camada Seazone Real Data** (do inglês "dados reais"): são os dados reais dos imóveis da Seazone. Já que nós somos os anunciantes, possuímos a informação verdadeira, e utilizamos ela como "gabarito" para calibrar nossos modelos.

De maneira simplificada (mas não muito longe da realidade) o fluxo é o seguinte:



1. Os dados são scrapados das plataformas de anúncio e são armazenados na camada Raw
2. Os dados da camada Raw são limpos e tratados, e então armazenados na camada Clean
3. Os dados da camada Clean são filtrados, agregados, e passam por scripts que possuem algum tipo de regra heurística para extrair mais informações, e então são armazenados na camada Enriched; ou então eles passam por algum tipo de algoritmo de Machine Learning e são armazenados na camada Models
4. Os dados da camada Enriched passam por outros modelos estatísticos ou de Machine Learning e são armazenados na camada Models

E agora, depois de uma grande introdução (talvez eu mova isso para outra página do Notion), vamos aos dados!!!

# Catálogo

## Camada RAW

### airbnb_internal_conversion_rate

**Descrição:** Tabela contendo as informações de taxa de conversão dos anúncios da Seazone no Airbnb.  A taxa de conversão é taxa de visitantes distintos que visualizaram o anúncio nas buscas e depois o reservaram.

Ela é atualmente alimentada pelo processo de aquisição dos scrapers de desempenho.

 ![Lugares de onde os dados são coletados](Cata%CC%81logo%20Interno%20de%20Dados%20do%20Pipe%20b47c172b039e4f41a58ce2f97d6b80ca/taxa_de_conversao.png)

Lugares de onde os dados são coletados

As informações vindas diretamente do gráfico, são referentes ao anúncio em questão na **data_alvo** escolhida. As informações vindas de cima do gráfico, são referentes ao anúncio em questão durante o período entre a **primeira_data_do_intervalo** e **ultima_data_do_intervalo** data escolhida no calendário de busca.

**Frequência de aquisição:** 1 vez ao dia.

Trigger/Cron/Schedule: 8:45

* **Colunas:**
  * **airbnb_listing_id:** id Airbnb do anúncio
  * **aquisition_date:** data e hora de aquisição do anúncio
  * **data_alvo:** data alvo dos dados adquiridos diretamente do gráfico
  * **taxa_de_conversao_seazone:** taxa de conversão do anúncio
  * **taxa_de_conversao_anuncios_similares:** taxa de conversão de anúncio similares ao anúncio alvo
  * **primeira_data_do_intervalo**: primeira data alvo do intervalo de datas escolhido no calendário de busca
  * **ultima_data_do_intervalo**: última data alvo do intervalo de datas escolhido no calendário de busca
  * **taxa_global_de_conversao**: taxa de conversão média do anúncio durante o período escolhido no calendárido
  * **taxa_de_impressoes_de_busca_na_primeira_pagina:** taxa média de impressões de busca vindas da primeira página de busca durante o período escolhido no calendárido
  * **conversao_de_busca_para_acesso_ao_anuncio**: taxa média de clicks no anúncio após ele aparecer nos resultados de busca durante o período escolhido no calendárido
  * **conversao_de_anuncio_para_reserva**: taxa média de conversão para reserva de visitantes distintos que visualizaram a página do anúncio durante o período escolhido no calendárido

### airbnb_internal_return_guest

**Descrição:** Tabela contendo as informações de taxa de hóspedes regulares dos anúncios da Seazone no Airbnb. Hóspedes regulares que retornam são a taxa de hóspedes que já ficaram hospedados em alguma de suas acomodações anteriormente.

Ela é atualmente alimentada pelo processo de aquisição dos scrapers de desempenho.

 ![Lugares de onde os dados são coletados](Cata%CC%81logo%20Interno%20de%20Dados%20do%20Pipe%20b47c172b039e4f41a58ce2f97d6b80ca/hospedes_regulares.png)

Lugares de onde os dados são coletados

**Frequência de aquisição:** 1 vez ao dia.

* **Colunas:**
  * **airbnb_listing_id:** id Airbnb do anúncio
  * **aquisition_date:** data e hora de aquisição do anúncio
  * **data_alvo:** data alvo dos dados adquiridos diretamente do gráfico
  * **taxa_de_hospedes_regulares_seazone:** taxa de hospedes regulares do anúncio

    **Frequência de aquisição:** 1 vez ao dia.

### airbnb_internal_time_between

**Descrição:** Tabela contendo as informações do período de antecedência entre confirmação da reserva e check-in dos anúncios da Seazone no Airbnb.

O período de antecedência das reservas é o tempo médio entre o momento em que um hóspede reserva e o dia do check-in.

Ela é atualmente alimentada pelo processo de aquisição dos scrapers de desempenho.

 ![Lugares de onde os dados são coletados](Cata%CC%81logo%20Interno%20de%20Dados%20do%20Pipe%20b47c172b039e4f41a58ce2f97d6b80ca/tempo_de_antecedencia.png)

Lugares de onde os dados são coletados

**Frequência de aquisição:** 1 vez ao dia.

* **Colunas:**
  * **airbnb_listing_id:** id Airbnb do anúncio
  * **aquisition_date:** data e hora de aquisição do anúncio
  * **data_alvo:** data alvo dos dados adquiridos diretamente do gráfico
  * **periodo_de_antecedencia_seazone:** período de antecedência de anúncio similares ao anúncio alvo
  * **periodo_de_antecedencia_anuncios_similares:** período de antecedência de anúncio similares ao anúncio alvo

### airbnb_internal_views

**Descrição:** Tabela contendo as informações de visualizações das páginas dos anúncios da Seazone no Airbnb. O número de visualizações é a quantidade de visitantes diferentes que viram à página do anúncio ao buscar datas de viagem em suas datas selecionadas, durante os 90 dias que as antecederam.

Ela é atualmente alimentada pelo processo de aquisição dos scrapers de desempenho.

 ![Lugares de onde os dados são coletados](Cata%CC%81logo%20Interno%20de%20Dados%20do%20Pipe%20b47c172b039e4f41a58ce2f97d6b80ca/visualizacoes.png)

Lugares de onde os dados são coletados

As informações vindas diretamente do gráfico, são referentes ao anúncio em questão na **data_alvo** escolhida. As informações vindas de cima do gráfico, são referentes ao anúncio em questão durante o período entre a **primeira_data_do_intervalo** e **ultima_data_do_intervalo** data escolhida no calendário de busca.

**Frequência de aquisição:** 1 vez ao dia.

O scraper de visualizações pega mais de uma data por aquisição, pois ele pega datas até 90 dias no futuro para a analise temporal dos dados.

* **Colunas:**
  * **airbnb_listing_id:** id Airbnb do anúncio
  * **aquisition_date:** data e hora de aquisição do anúncio
  * **data_alvo:** data alvo dos dados adquiridos diretamente do gráfico
  * **visualizacoes_seazone:** número de visualizações do anúncio
  * **visualizacoes_anuncios_similares:** número de visualizações de anúncio similares ao anúncio alvo
  * **primeira_data_do_intervalo**: primeira data alvo do intervalo de datas escolhido no calendário de busca
  * **ultima_data_do_intervalo**: última data alvo do intervalo de datas escolhido no calendário de busca
  * **total_de_impressoes_de_busca_de_primeira_pagina**: número de visualizações na primeira página dos resultados de busca para o intervalo de datas selecionado durante os 90 dias que antecederam essas datas

### airbnb_internal_wishlist

**Descrição:** Tabela contendo as informações do número de adições à wishlist dos anúncios da Seazone no Airbnb. As adições à wishlist são o número de vezes que os anúncios são adicionados às wishlists dos hóspedes.

Ela é atualmente alimentada pelo processo de aquisição dos scrapers de desempenho.

 ![Lugares de onde os dados são coletados](Cata%CC%81logo%20Interno%20de%20Dados%20do%20Pipe%20b47c172b039e4f41a58ce2f97d6b80ca/wishlist.png)

Lugares de onde os dados são coletados

**Frequência de aquisição:** 1 vez ao dia.

* **Colunas:**
  * **airbnb_listing_id:** id Airbnb do anúncio
  * **aquisition_date:** data e hora de aquisição do anúncio
  * **data_alvo:** data alvo dos dados adquiridos diretamente do gráfico
  * **adicoes_wishlist_seazone:** total de adições à wish list de anúncio similares ao anúncio alvo
  * **adicoes_wishlist_anuncios_similares:** total de adições à wish list de anúncio similares ao anúncio alvo

### discounts

**Descrição:** Possui informação de descontos por duração de estadia nas reservas do Airbnb (valor é nulo caso não tenha tido desconto); o dado de desconto é armazenado em valor absoluto e em porcentagem do valor total da reserva.

* **Colunas:**

| **Nome da coluna** | **descrição** | **tipo de dado** |
|----|----|----|
| id_airbnb | ID do listing no Airbnb | string |
| checkin | data do checkin da reserva | date |
| checkout | data do checkout da reserva | date |
| stay_price | preço total da reserva | double |
| discount | valor absoluto do desconto por duração de estadia | double |
| discount_rate | valor percentual do desconto por duração de estadia | double |
| discount_title | descrição do desconto aplicado | string |
| cleaning_fee | taxa de limpeza da reserva | double |
| guest_fee | taxa de hospedagem da reserva | double |
| aquisition_date | data da aquisição dos dados | timestamp |
| ano | ano em "aquisition_date" | string |
| mes | mês em "aquisition_date" | string |
| dia | dia em "aquisition_date" | string |

**Frequência:** 1x por dia

**Descrição técnica:** Usa uma API do Airbnb para conseguir os descontos. Para não precisar scrapar todas as possíveis reservas que poderiam ter acontecido (o que seria um número infinitamente grande) apenas as reservas que o Pipe identificou como tendo realmente ocorrido são scrapadas; ou seja, esse é um scraper que depende de dados da camada Enriched (o que é exceção nos scrapers), mais especificamente da tabela "reservations".

### hotel_costao_do_santinho

**Descrição:** Possui os dados de preço para diferentes dias das diferentes suítes do hotel Costão do Santinho em Florianópolis/SC. Site do hotel: <https://www.costao.com.br/>

* **Colunas:**

| **Nome da coluna** | **descrição** | **tipo de dado** |
|----|----|----|
| aquisition_date | data da aquisição dos dados | string |
| target_date | diária a qual os preços se referem | string |
| suíte_junior | preço da diária da suíte junior | double |
| suíte_luxo | preço da diária da suíte luxo | double |
| apartamento_superior_1_dormitório | preço da diária do apto superior 1 dormitório | double |
| suíter_master | preço da diária da suíte master | double |
| superior | preço da diária do quarto "superior" | double |
| apartamento_luxo_1_dormitório | preço da diária do apartamento luxo 1 dormitório | double |

**Frequência:** 1x por semana

### hotel_il_campanario

**Descrição:** Possui os dados de preço para diferentes dias das diferentes suítes do hotel il Campanário em Florianópolis/SC. Site do hotel: <https://www.ilcampanario.com.br/>

* **Colunas:**

| **Nome da coluna** | **descrição** | **tipo de dado** |
|----|----|----|
| aquisition_date | data da aquisição dos dados | string |
| target_date | diária a qual os preços se referem | string |
| suite_jr_jurere | preço da diária da suíte JR Jurere | double |
| suite_jr_boulevard | preço da diária da suíte JR Boulevard | double |
| suite_buzios | preço da diária da suite Buzios | double |
| suite_jurere | preço da diária da suíte Jurere | double |
| suite_boulevard | preço da diária do suíte Boulevard | double |

**Frequência:** 1x por semana

### hotel_jurere_beach_village

**Descrição:** Possui os dados de preço para diferentes dias das diferentes suítes do hotel Jurerê Beach Village em Florianópolis/SC. Site do hotel:  <https://www.jurerebeachvillage.com.br/>

* **Colunas:**

| **Nome da coluna** | **descrição** | **tipo de dado** |
|----|----|----|
| aquisition_date | data da aquisição dos dados | string |
| target_date | diária a qual os preços se referem | string |
| studio_lateral | preço da diária do studio lateral | double |
| suite_alameda | preço da diária da suíte alameda | double |
| studio_lateral_luxo | preço da diária do studio lateral luxo | double |
| suite_lateral | preço da diária da suíte lateral | double |
| suite_lateral_luxo | preço da diária do suíte lateral luxo | double |
| suite_frente_mar_luxo | preço da diária da suíte frente mar luxo | double |

**Frequência:** 1x por semana

### hotel_majestic

**Descrição:** Possui os dados de preço para diferentes dias das diferentes suítes do hotel Majestic Palace em Florianópolis/SC. Site do hotel: <https://www.majesticpalace.com.br/>

* **Colunas:**

| **Nome da coluna** | **descrição** | **tipo de dado** |
|----|----|----|
| aquisition_date | data da aquisição dos dados | string |
| target_date | diária a qual os preços se referem | string |
| apartamento_standard_duplo_casal | preço da diária do apartamento standard duplo com cama de casal | double |
| apartamento_standard_duplo_solteiro | preço da diária do apartamento standard duplo com camas de solteiro | double |
| apartamento_luxo_duplo_casal | preço da diária do apatamento luxo duplo com cama de casal | double |
| apartamento_superior_casal_mais_sofa_cama | preço da diária do apartamento superior com cama de casal e sofá cama | double |
| apartamento_luxo_triplo_casal_mais_solteiro | preço da diária do apartamento luxo triplo com cama de casal mais cama de solteiro | double |
| apartamento_luxo_sacada_duplo_casal | preço da diária do apartamento luxo com cama de casal e sacada | double |
| apartamento_executivo_casal_mais_sofa_cama | preço da diária do apartamento executivo com cama de casal e sofá cama | double |
| suite_junior_casal_mais_sofa_cama | preço da diária da suíte junior com cama de casal e sofá cama | double |
| suite_executivo_casal_mais_sofa_cama | preço da diária da suite executiva com cama de casal e sofá cama | double |

**Frequência:** 1x por semana

### hotel_mercure

**Descrição:** Possui os dados de preço para diferentes dias das diferentes suítes do hotel Mercure em Florianópolis/SC. Site do hotel: <https://all.accor.com/hotel/5693/index.pt-br.shtml>

* **Colunas:**

| **Nome da coluna** | **descrição** | **tipo de dado** |
|----|----|----|
| aquisition_date | data da aquisição dos dados | string |
| target_date | diária a qual os preços se referem | string |
| quarto_standard_2_cama_solteiro | preço da diária do quarto standard com 2 camas de solteiro | double |
| apartamento_superior_1_cama_queen | preço da diária do apartamento superior com 1 cama queen | double |
| apartamento_executivo_2_camas_solteiro | preço da diária do apartamento executivo com 2 camas de solteiro | double |
| suite_deluxe_cama_king | preço da diária do suíte deluxe com cama king | double |
| apartamento_executivo_1_cama_queen | preço da diária do apartamento executivo com 1 cama queen | double |
| quarto_standard_1_cama_casal | preço da diária do quarto standard com 1 cama de casal | double |

**Frequência:** 1x por semana

### mesh_ids

**Descrição:** É uma tabela com os IDs dos anúncios do Airbnb no Brasil inteiro, assim como a latitude/longitude do listing e a data de aquisição. A tabela é criada a partir de um algoritmo que percorre o mapa do Airbnb pegando os IDs que vão aparecendo e salvando.

* **Colunas:**

| **Nome da coluna** | **descrição** | **tipo de dado** |
|----|----|----|
| aquisition_date | data da aquisição dos dados | string |
| ano | ano em "aquisition_date" | string |
| mes | mes em "aquisition_date" | string |
| dia | dia em "aquisition_date" | string |
| airbnb_listing_id | id do listing no Airbnb | string |
| latitude | latitude do listing no Airbnb | double |
| longitude | longitude do listing no Airbnb | double |

**Frequência:** 1x a cada 15 dias

**Descrição técnica: [Mesh](/doc/mesh-Gyugvr7JKI)**

### listing_booking_comments

**Descrição:** Tabela de comentários do Booking para os listings da Seazone, com dados adquiridos semanalmente. Contém avaliações e feedbacks dos hóspedes, incluindo aspectos positivos e negativos, além de informações do avaliador. A tabela é particionada pela coluna aquisition_date_partition.

* **Colunas:**

|   **Nome da Coluna** | **Descrição** | **Tipo de Dado** |
|----|----|----|
| ```javascript
hotel_id
``` | ID do hotel no sistema. | string |
| ```javascript
room_id
``` | ID do quarto no sistema. | string |
| ```javascript
comment_id
``` | ID único do comentário. | string |
| ```javascript
commenter_name
``` | Nome do usuário que realizou o comentário. | string |
| ```javascript
rating
``` | Avaliação do hóspede (em nota). | int |
| ```javascript
liked_comment
``` | Aspecto positivo destacado pelo hóspede. | string |
| ```javascript
liked_comment_language
``` | Idioma do comentário positivo. | string |
| ```javascript
disliked_comment
``` | Aspecto negativo destacado pelo hóspede. | string |
| ```javascript
disliked_comment_language
``` | Idioma do comentário negativo. | string |
| ```javascript
commenter_nationality
``` | Nacionalidade do comentarista. | string |
| ```javascript
stay_length
``` | Duração da estadia (em dias). | int |
| ```javascript
stay_type
``` | Tipo de estadia (ex.: lazer, negócios). | string |
| ```javascript
date
``` | Data de publicação do comentário. | string |
| ```javascript
aquisition_date
``` | Data de aquisição do dado. | string |
| ```javascript
aquisition_date_partition
``` | Partição pela data de aquisição do dado. | string (Particionado) |

**Frequência:** 1x por semana

### listing_booking_details

**Descrição:** Tabela com detalhes dos listings do Booking vinculados à Seazone, atualizada semanalmente. Contém informações detalhadas sobre os hotéis e quartos, incluindo nome, cidade, tipo de acomodação, tamanho do quarto e instalações. A tabela é particionada pela coluna aquisition_date_partition.

* **Colunas:**

| **Nome da Coluna** | **Descrição** | **Tipo de Dado** |
|----|----|----|
| ```javascript
hotel_id
``` | ID do hotel no sistema. | string |
| ```javascript
room_id
``` | ID do quarto no sistema. | string |
| ```javascript
hotel_name
``` | Nome do hotel. | string |
| ```javascript
city_name
``` | Nome da cidade onde o hotel está localizado. | string |
| ```javascript
accommodation_type
``` | Tipo de acomodação (ex.: hotel, pousada). | string |
| ```javascript
room_name
``` | Nome ou descrição do quarto. | string |
| ```javascript
room_surface_in_m2
``` | Tamanho do quarto em metros quadrados. | string |
| ```javascript
room_facilities
``` | Lista de facilidades disponíveis no quarto. | array<string> |
| ```javascript
aquisition_date
``` | Data de aquisição do dado. | string |
| ```javascript
aquisition_date_partition
``` | Partição pela data de aquisição do dado. | string (Particionado) |

**Frequência:** 1x por semana

### listing_booking_house_rules

**Descrição:** Tabela com as regras de hospedagem dos listings do Booking vinculados à Seazone, atualizada semanalmente. Inclui informações sobre horários de check-in e check-out, políticas de cancelamento, restrições de idade, regras para pets, entre outros detalhes específicos da hospedagem. A tabela é particionada pela coluna aquisition_date_partition.

* **Colunas:**

| **Nome da Coluna** | **Descrição** | **Tipo de Dado** |
|----|----|----|
| ```javascript
hotel_id
``` | ID do hotel no sistema. | string |
| ```javascript
checkin
``` | Horário de check-in permitido. | string |
| ```javascript
checkout
``` | Horário de check-out permitido. | string |
| ```javascript
cancellation
``` | Políticas de cancelamento da reserva. | string |
| ```javascript
children
``` | Políticas para hospedagem de crianças. | string |
| ```javascript
age_restriction
``` | Restrições de idade para hospedagem. | string |
| ```javascript
payments
``` | Métodos de pagamento aceitos. | string |
| ```javascript
parties
``` | Regras sobre festas e eventos. | string |
| ```javascript
quiet_hours
``` | Horários de silêncio estabelecidos pela acomodação. | string |
| ```javascript
pets
``` | Política para animais de estimação. | string |
| ```javascript
fine_print
``` | Informações adicionais importantes (fine print). | string |
| ```javascript
aquisition_date
``` | Data de aquisição do dado. | string |
| ```javascript
aquisition_date_partition
``` | Partição pela data de aquisição do dado. | string (Particionado) |

**Frequência:** 1x por semana

### listing_booking_mesh

**Descrição:** Tabela com informações detalhadas dos listings do Booking para o Brasil inteiro, incluindo dados coletados via API de mapas do Booking. A tabela contém o título do hotel, tipo de acomodação, localização (latitude e longitude), nota de avaliação e quantidade de avaliações, e é particionada pela coluna aquisition_date_partition.

* **Colunas:**

| **Nome da Coluna** | **Descrição** | **Tipo de Dado** |
|----|----|----|
| ```javascript
booking_id
``` | ID do hotel no Booking. | string |
| ```javascript
hotel_title
``` | Nome do hotel. | string |
| ```javascript
url
``` | URL da página do hotel no Booking. | string |
| ```javascript
lat
``` | Latitude do hotel. | string |
| ```javascript
long
``` | Longitude do hotel. | string |
| ```javascript
is_preferred
``` | Indica se o hotel é preferido no Booking. | string |
| ```javascript
accommodation_type
``` | Tipo de acomodação (ex.: hotel, pousada). | string |
| ```javascript
review_score
``` | Nota de avaliação do hotel. | string |
| ```javascript
review_nr
``` | Número de avaliações do hotel. | string |
| ```javascript
aquisition_date
``` | Data de aquisição do dado. | string |
| ```javascript
aquisition_date_partition
``` | Partição pela data de aquisição do dado. | string (Particionado) |

**Frequência:** A definir

### listing_booking_priceav

**Descrição:** Tabela com informações sobre a disponibilidade e preços dos listings da Seazone, coletada diariamente. A tabela contém dados sobre o ID do hotel, data, preço, disponibilidade e duração mínima da estadia, sendo particionada pela coluna aquisition_date_partition.

* **Colunas:**

| **Nome da Coluna** | **Descrição** | **Tipo de Dado** |
|----|----|----|
| ```javascript
hotel_id
``` | ID do hotel no sistema. | string |
| ```javascript
date
``` | Data referente ao preço e disponibilidade. | string |
| ```javascript
price
``` | Preço do hotel para a data especificada. | string |
| ```javascript
available
``` | Indica se o hotel está disponível para a data especificada. | boolean |
| ```javascript
min_stay
``` | Duração mínima da estadia em noites. | int |
| ```javascript
aquisition_date
``` | Data de aquisição do dado. | string |
| ```javascript
aquisition_date_partition
``` | Partição pela data de aquisição do dado. | string (Particionado) |

**Frequência:** Diária

### listing_booking_ratings

**Descrição:** Tabela contendo as avaliações dos listings da Seazone, com informações sobre a pontuação em diferentes aspectos, como instalações, limpeza, conforto, relação custo-benefício e localização. A tabela é particionada pela coluna aquisition_date_partition e atualizada semanalmente.

* **Colunas:**

| **Nome da Coluna** | **Descrição** | **Tipo de Dado** |
|----|----|----|
| ```javascript
hotel_id
``` | ID do hotel no sistema. | string |
| ```javascript
facilities
``` | Nota atribuída às instalações do hotel. | double |
| ```javascript
cleanliness
``` | Nota atribuída à limpeza do hotel. | double |
| ```javascript
comfort
``` | Nota atribuída ao conforto do hotel. | double |
| ```javascript
value_for_money
``` | Nota atribuída à relação custo-benefício do hotel. | double |
| ```javascript
location
``` | Nota atribuída à localização do hotel. | double |
| ```javascript
total
``` | Nota total do hotel, considerando todos os aspectos. | double |
| ```javascript
free_wifi
``` | Nota referente à disponibilidade de Wi-Fi gratuito. | double |
| ```javascript
number_of_ratings
``` | Número total de avaliações recebidas pelo hotel. | int |
| ```javascript
aquisition_date
``` | Data de aquisição do dado. | string |
| ```javascript
aquisition_date_partition
``` | Partição pela data de aquisição do dado. | string (Particionado) |

**Frequência:** 1x por semana

## Camada CLEAN

### airdna_details

**Descrição:** Tabela com os detalhes dos listings no Airbnb. Tabela idem à nossa "details_last_aquisitiondetails" (da camada Enriched), porém os dados vem do Airdna ao invés de serem os dados que o Pipe adquiriu.

* **Colunas:**

| **Nome da coluna** | **descrição** | **tipo de dado** |
|----|----|----|
| property_id | ID do listing no Airbnb | string |
| listing_title | Título do listing no Airbnb | string |
| property_type | Tipo da propriedade (apto, casa, dormitório etc) | string |
| listing_type | Tipo do listing (apto inteiro, parte de um apto, quarto compartilhado, quarto privativo etc) | string |
| created_date | Data da criação do listing | string |
| last_scraped_date | Data da última scrapagem do listing em questão | string |
| country | País do listing | string |
| state | Estado do listing | string |
| city | Cidade do listing | string |
| zipcode | CEP do listing | string |
| neighborhood | Bairro do listing | string |
| metropolitan_statistical_area | Não possui dados para o Brasil | string |
| currency_native | Código da moeda do país (BRL para Real) | string |
| average_daily_rate_usd | Preço média da diária em dólares | double |
| average_daily_rate_native | Preço média da diária na moeda nativa | double |
| annual_revenue_ltm_usd | Faturamento anual nos últimos 12 meses em dólares | bigint |
| annual_revenue_ltm_native | Faturamento anual ndos últimos 12 meses na moeda nativa | bigint |
| occupancy_rate_ltm | Taxa de ocupação nos últimos 12 meses | double |
| number_of_bookings_ltm | Número de reservas nos últimos 12 meses | bigint |
| number_of_reviews | Número de reviews nos últimos 12 meses | bigint |
| bedrooms | Número de quartos | bigint |
| bathrooms | Número de banheiros | double |
| max_guests | Número máximo de hóspedes permitido | bigint |
| calendar_last_updated | Data da última alteração no calendário do imóvel | string |
| response_rate | Taxa de resposta do host do listing | bigint |
| airbnb_response_time | Tempo que o host costuma levar para responder | string |
| airbnb_superhost | Indica se é ou não superhost | boolean |
| homeaway_premier_partner |    | boolean |
| cancellation_policy | Política de cancelamento do listing | string |
| security_deposit_usd | Taxa de depósito de segurança em dólares | bigint |
| security_deposit_native | Taxa de depósito de segurança na moeda nativa | bigint |
| cleaning_fee_usd | Taxa de limpeza em dólares | bigint |
| cleaning_fee_native | Taxa de limpeza na moeda nativa | bigint |
| extra_people_fee_usd | Taxa para extrapolar o limite máximo de hóspedes, em dólares | bigint |
| extra_people_fee_native | Taxa para extrapolar o limite máximo de hóspedes, na moeda nativa | bigint |
| published_nighlty_rate_usd | Preço de 1 diária em dólares | bigint |
| published_monthly_rate_usd |    | bigint |
| published_weekly_rate_usd |    | bigint |
| checkin_time | Horário de checkin | string |
| checkout_time | Horário de checkout | string |
| minimum_stay | Estadia mínima | bigint |
| count_reservation_days_ltm | Número de dias reservados nos últimos 12 meses | bigint |
| count_available_days_ltm | Número de dias disponíveis nos últimos 12 meses | bigint |
| count_blocked_days_ltm | Número de dias bloqueados nos últimos 12 meses | bigint |
| number_of_photos | Número de fotos | bigint |
| instantbook_enabled | Indica se o instant book está ativado ou não | boolean |
| listing_url | URL do listing | string |
| listing_main_image_url | URL da imagem de capa do listing | string |
| listing_images | Lista com URLs de todas as imagens do listing | string |
| latitude | Latitude do listing | double |
| longitude | Longitude do listing | double |
| exact_location | Indica se é a localização informada é a localização exata ou não | boolean |
| overall_rating | Nota geral do listing | bigint |
| airbnb_communication_rating | Nota de comunicação do listing | bigint |
| airbnb_accuracy_rating | Nota de exatidão do listing | bigint |
| airbnb_cleanliness_rating | Nota de limpeza do listing | bigint |
| airbnb_checkin_rating | Nota de experiência de checkin do listing | bigint |
| airbnb_location_rating | Nota de localização do listing | bigint |
| airbnb_value_rating | Nota de custo-benefício do listing | bigint |
| pets_allowed | Indica se aceita ou não pets | boolean |
| integrated_property_manager |    | boolean |
| amenities | Indica todas as comodidades do listing (cozinha, estacionamento, piscina, wi-fi, fogueira, etc) | string |
| homeway_location_type |    | string |
| airbnb_property_plus |    | boolean |
| airbnb_home_collection |    | string |
| license |    | string |
| airbnb_property_id | ID do anúncio no Airbnb | string |
| airbnb_host_id | ID do host no Airbnb | string |
| homeaway_property_id |    | string |
| homeaway_property_manager_id |    | string |
| ano | ano em "last_scraped_date" | string |
| mes | mes em "last_scraped_date" | string |

**Frequência**: 1x por mês, manualmente

### booking_priceav

**Descrição:** Tabela com informações sobre a disponibilidade e preços dos listings do Booking da Seazone e da cidade do Rio de Janeiro, coletada diariamente. A tabela contém dados sobre o ID do anúncio, data, preço, disponibilidade e duração mínima da estadia. Ela é particionada pela coluna aquisition_date_partition.

* **Colunas:**

| **Nome da Coluna** | **Descrição** | **Tipo de Dado** |
|----|----|----|
| ```none
booking_listing_id
``` | ID do hotel no sistema de reservas. | string |
| ```none
date
``` | Data referente ao preço e disponibilidade. | date |
| ```none
price
``` | Preço do hotel para a data especificada. | Int32 |
| ```none
available
``` | Indica se o hotel está disponível para a data especificada. | boolean |
| ```none
min_stay
``` | Duração mínima da estadia em noites. | Int32 |
| ```none
aquisition_date
``` | Data de aquisição do dado, incluindo data e hora. | timestamp |
| ```none
aquisition_date_partition
``` | Partição pela data de aquisição do dado. | date (Particionado) |

**Frequência:** Diária

### booking_details

**Descrição:** Tabela com informações sobre detalhes dos imóveis do Booking da Seazone e da cidade do Rio de Janeiro, coletada semanalmente. Ela é particionada pela coluna aquisition_date_partition.

* **Colunas:**

| **Nome da Coluna** | **Descrição** | **Tipo de Dado** |
|----|----|----|
| ```none
booking_listing_id
``` | ID do anúncio no sistema de reservas. | string |
| ```none
booking_room_id
``` | ID do imóvel no sistema de reservas. | string |
| ```none
listing_name
``` | Título do anúncio. | string |
| ```none
city_name
``` | Nome da cidade onde se encontra o anúncio. | string |
| ```none
accommodation_type
``` | Tipo do imóvel (ex.: casa, apartamento, etc.). | string |
| ```none
room_name
``` | Título do imóvel. | string |
| ```none
number_of_rooms
``` | Número de quartos no imóvel. | Int32 |
| ```none
number_of_bathrooms
``` | Número de banheiros no imóvel. | Int32 |
| ```none
room_surface_in_m2
``` | Tamanho do imóvel em metros quadrados. | int |
| ```none
room_facilities
``` | Comodidades do imóvel. | array<string> |
| ```none
aquisition_date
``` | Data de aquisição do dado. | string |
| ```none
booking_listing_url
``` | URL da página do anúncio | string |
| ```none
aquisition_date_partition
``` | Partição pela data de aquisição do dado. | string (Particionado) |

**Frequência:** Semanal (segundas às 11:00 UTC)

### dates

**Descrição:** Tabela com datas desde 01/01/2014 até 24/12/2034, indicando se é feriado, final de semana ou fez parte da pandemia.

* **Colunas:**

| **Nome da coluna** | **descrição** | **tipo de dado** |
|----|----|----|
| index | Índice da tabela quando foi gerada manualmente (porém possui valores duplicados, então na verdade não é um índice!) | bigint |
| date | Data em questão | date |
| holiday | Indica qual é o feriado | string |
| month | Mês em "date" | bigint |
| weekend | Indica se a data é parte de um final de semana | string |
| pandemic | Indica se a data fez parte da pandemia | string |

**Frequência:** estática, as datas já foram criadas até 2034

### details

**Descrição:** Tabela com os detalhes dos listings do Airbnb para cada data de aquisição (para conseguir apenas os detalhes **mais recentes** de cada listing, olhe "[details_last_aquisitiondetails](/doc/catalogo-interno-de-dados-do-pipe-Z7Ccq3Ixjv)")

* **Colunas:**

| **Nome da coluna** | **descrição** | **tipo de dado** | **Exemplo** |
|----|----|----|----|
| airbnb_listing_id | ID do listing no Airbnb | string |    |
| url | URL do listing | string |    |
| ad_name | Título do listing | string |    |
| ad_description | Descrição do listing | string |    |
| space | Descrição do espaço do listing (funciona como um complemento de "ad_description") | string |    |
| house_rules | Regras do listing | string |    |
| amenities | Indica todas as comodidades do listing (cozinha, estacionamento, piscina, wi-fi, fogueira, etc) | string |    |
| safety_features | Indica todos os equipamentos de segurança do listing | string |    |
| number_of_bathrooms | Número de banheiros | double |    |
| number_of_bedrooms | Número de quartos | bigint |    |
| number_of_beds | Número de camas | bigint |    |
| latitude | Latitude do listing | double |    |
| longitude | Longitude do listing | double |    |
| star_rating | Nota geral do listing | double |    |
| additional_house_rules | Regras adicionais do listing | string |    |
| owner | Proprietário do listing(é um ID único dentro do Airbnb, o ID do anunciante) | string |    |
| check_in | Horário de checkin | string |    |
| check_out | Horário de checkout | string |    |
| number_of_guests | Número máximo de hóspedes permitido | bigint |    |
| is_superhost | Indica se é superhost ou não | string |    |
| number_of_reviews | Número de reviews que o listing possui | bigint |    |
| cohost | Coproprietários do listing (não é um ID único, é informado apenas o nome do coproprietário) | string |    |
| cleaning_fee | Taxa de limpez | double |    |
| can_instant_book | Indica se o instant book está ativado ou não | string |    |
| owner_id | ID único do proprietário do listing dentro do Airbnb | string |    |
| aquisition_date | Data de aquisição dos dados na camada Raw | timestamp |    |
| listing_type | Tipo do listing (já realizada a [equivalência entre os tipos](/doc/catalogo-interno-de-dados-do-pipe-Z7Ccq3Ixjv) do Airbnb e os tipos que a Seazone considera, ou seja, aqui é o tipo que a Seazone considera) | string |    |
| picture_count | Número de fotos do anúncio | bigint |    |
| min_nights | Estadia mínima | bigint |    |
| response_rate_shown | Taxa de resposta do host do listing | string |    |
| response_time_shown | Tempo que o host costuma levar para responder | string |    |
| guest_satisfaction_overall |    | bigint |    |
| index |    |    |    |
| ano | Ano de "aquisition_date" | string |    |
| mes | Mês de "aquisition_date" | string |    |
| dia | Dia de "aquisition_date" | string |    |

**Frequência:** 1x na semana

### hotels

**Descrição:** Tabela com dados de +38.000 hotéis e pousadas do Brasil, que vão desde CNPJ e nome fantasia até CNAE, capital social e data de início das atividades.

* **Colunas:**

| **Nome da coluna** | **descrição** | **tipo de dado** |
|----|----|----|
| cnpj | CNPJ do hotel/pousada | bigint |
| nome fantasia | Nome fantasia | string |
| razão social | Razão social | string |
| data início atividade | Data de inauguração (jurídica) do hotel/pousada | date |
| capital social | Capital social da empresa | bigint |
| cnae | CNAE primário da empresa | string |
| cnaes secundárias | CNAEs secundárias | string |
| natureza jurídica | Natureza jurídica | string |
| qualificação do responsável | Indica a qualificação do responsável pela empresa | string |
| matriz/filial | Indica se o CNPJ é a matriz ou uma filial | string |
| porte | Porte da empresa | string |
| situação cadastral | Situação cadastral | string |
| data situação cadastral | Data da situação cadastral adquirida | date |
| motivo situação | Motivo da situação cadastral | bigint |
| tipo de logradouro | Tipo do logradouro (Rua, Avenida etc) | string |
| logradouro | Endereço da empresa | string |
| número | Número do endereço | string |
| complemento | Complemento do endereço | string |
| bairro | Bairro da empresa | string |
| município | Município da empresa | string |
| uf | Estado da empresa | string |
| cep | CEP da empresa | bigint |
| e-mail | E-mail | string |
| telefone 1 | Telefone primário | bigint |
| tipo telefone 1 | Indica se celular ou fixo | string |
| telefone 2 | Telefone secundário | bigint |
| ddd fax | DDD do fax | bigint |
| número fax | Número do fax | bigint |
| opção pelo simples | Indica se a empresa é optante pelo regime de arrecadação, cobrança e fiscalização chamado "Simples Nacional" | string |
| data opção simples | Data que a empresa optou pelo regime "Simples Nacional" | date |
| data exclusão simples | Data que a empresa optou em sair do regime "Simples Nacional" | date |
| opção pelo mei | Indica se a empresa é optante pelo regime MEI (Microempreendedor Individual) | string |
| data opção mei | Data que a empresa optou pelo regime MEI | date |
| data exclusão mei | Data que a empresa optou em sair do regime MEI | date |

**Frequência:** estática

### listing_type

**Descrição:** Tabela com a equivalência entre os inúmeros tipos de listing que o Airbnb permite cadastrar e alguns tipos de listing que a Seazone trata (apartamento, casa, hotel ou outros). Há mais de 450 dessas equivalências hoje, exemplo:

| **listing_type** | **new_type** |
|----|----|
| Quarto inteiro em pousada | hotel |
| Espaço inteiro: loft | apartamento |
| Espaço inteiro: apartamento | apartamento |
| Espaço inteiro: casa residencial | apartamento |
| Quarto compartilhado em casa residencial | outros |

* **Colunas:**

| **Nome da coluna** | **descrição** | **tipo de dado** |
|----|----|----|
| listing_type | Tipo do listing originalmente no Airbnb | string |
| new_type | Novo tipo do listing (apartamento, casa, hotel ou outros) | string |

**Frequência:** estática

### location

**Descrição:** Tabela com as localizações dos listings no Airbnb como latitude, longitude, País, Estado, Cidade, Bairro e data de aquisição. É criada a partir dos dados da camada "raw", estruturando-os de maneira adequada e realizando alguns processos de limpeza.

* **Colunas:**

| **Nome da coluna** | **descrição** | **tipo de dado** |
|----|----|----|
| airbnb_listing_id | ID do listing no Airbnb | string |
| latitude | Latitude | double |
| longitude | Longitude | double |
| raw_location | Localização "crua" do listing | string |
| country | País do listing | string |
| state | Estado do listing | string |
| city | Cidade do listing | string |
| suburb | Bairro do listing | string |
| aquisition_date | Data de aquisição dos dados na camada Raw | timestamp |

**Frequência:** 1x por semana

### monthly_reviews

**Descrição:** Notas mensais de review dos listings da Seazone. Cada listing/mês possui as diferentes notas de review do Airbnb (limpeza, custo-benefício, geral etc) até a data atual. Todos os dias os valores vão sendo atualizados com os novos reviews que os hóspedes vão colocando. Quando o mês se encerra o processo é reiniciado para o mês novo.

Exemplo:

| **id_seazone** | **overall** | **clean** | **…** | **month_reviews** | **cleaning_date** |
|----|----|----|----|----|----|
| JBV108 | 4 | 4 | … | 1 | 12/07/2023 |
| … | … | … | … | … | … |
| JBV108 | 4,2 | 5 | … | 3 | 15/07/2023 |
| … | … | … | … | … | … |
| JBV108 |    |    | … | 0 | 02/08/2023 |
| … | … | … | … | … | … |
| JBV108 | 5 | 5 | … | 1 | 03/08/2023 |

O Airbnb não fornece a nota mensal, apenas vai acumulando as notas ao longo do tempo. Essa tabela é gerada por um algoritmo que executa a lógica de:

* comparar:
  * o número de reviews/nota neste mês (até a data atual, já que o algoritmo é executado todos os dias)
  * o número de reviews/nota no mês passado
* fazer uma regra de 3 para conseguir as notas apenas deste mês

**Obs.: o Airbnb fornece as notas de cada tipo de review ARREDONDADAS, o que faz com que ocorram erros de arredondamento no algoritmo.**

* **Colunas:**

| **Nome da coluna** | **descrição** | **tipo de dado** |
|----|----|----|
| id_airbnb | ID do listing no Airbnb | string |
| id_seazone | ID do listing na Seazone | string |
| overall | Nota geral do listing no mês em questão (até a data "cleaning_date") | string |
| clean | Nota de limpeza do listing no mês em questão (até a data "cleaning_date") | string |
| communication | Nota de comunicação do listing no mês em questão (até a data "cleaning_date") | string |
| checkin | Nota de checkin do listing no mês em questão (até a data "cleaning_date") | string |
| accuracy | Nota de exatidão do listing no mês em questão (até a data "cleaning_date") | string |
| value | Nota de custo-benefício do listing no mês em questão (até a data "cleaning_date") | string |
| location | Nota de localização do listing no mês em questão (até a data "cleaning_date") | string |
| month_reviews | Número de reviews do listing no mês em questão (até a data "cleaning_date") | bigint |
| total_reviews | Número total de reviews do listing desde sua criação | bigint |
| month | Mês em questão da realização dos cálculos | bigint |
| year | Ano em questão da realização dos cálculos | bigint |
| cleaning_date | Data exata da realização dos cálculos | string |
| total_overall | Nota geral do listing desde a sua criação | double |

**Frequência:** 1x por dia.

### olx

**Descrição:** Tabela com os listings da OLX. Possui informações do listing (como preço, título, tipo de anúncio, localização), do dono do listing, e dados de contato. Diversos processos de limpeza são aplicados.

* **Colunas:**

| **Nome da coluna** | **descrição** | **tipo de dado** |
|----|----|----|
| listing_id | ID do listing na OLX | string |
| title | Título do listing | string |
| description | Descrição do listing | string |
| business_types | Indica se é um listing do tipo venda ou aluguel (caso seja ambos, terá duas linhas nesta tabela, uma para venda e outra para aluguel) | string |
| category | É o tipo de listing (casa, apartamento, terreno, comercial, lançamentos, materiais de construção e jardim, outros) | string |
| created | Data de criação do listing | timestamp |
| link_url | URL do listing | string |
| owner | Proprietário do listing | string |
| price | Preço do listing (quer seja de venda ou de aluguel) | bigint |
| iptu | Preço do IPTU do listing | int |
| condominium | Preço do condomínio do listing | int |
| usable_area | Área útil | int |
| bathrooms | Número de banheiros | int |
| rooms | Número de quartos | int |
| garage | Número de vagas de garagem | int |
| beds | Número de camas | int |
| state | Estado (UF) do listing | string |
| region | Região geográfica do listing (é um tipo de divisão própria da OLX) | string |
| zone | Zona geográfica do listing (é um tipo de divisão própria da OLX) | string |
| municipality | Município do listing | string |
| neighbourhood | Bairro do listing | string |
| zipcode | CEP do listing | string |
| aquisition_date | Data de aquisição dos dados na camada Raw | timestamp |
| owner_id | ID do proprietário do listing | string |
| owner_phone | Telefone do proprietário do listing | string |
| phone_verified | Indica se o telefone foi verificado ou não | boolean |
| features | Itens/comodidades do listing (ar condicionado, academia, churrasqueira, piscina, varada etc) | string |
| complex_features | Outros itens/comodidas dos listing, mais geralmente do condomínio o qual o listing pertence (elevador, permitido animais, portaria, salão de festas, academia, segurança 24h etc) | string |
| ano | Ano de "aquisition_date" | string |
| mes | Mês de "aquisition_date" | string |
| dia | Dia de "aquisition_date" | string |

**Frequência:** mesma frequência do "olx_listings".

### price_av

**Descrição:** Tabela com os dados limpos de preço e disponibilidade dos listings do Airbnb, para todos os dias de todos os meses que aparecem no calendário do listing.

Aqui há alguns pontos importantes:

* a disponibilidade é literalmente isso: se está disponível ou não. O fato de não estar disponível **NÃO** significa que foi alugado!!! O proprietário do imóvel pode ter pedido para usar, ou estar tendo alguma reforma, estarem ocupando para tirar fotos, limpar etc.
  * Quando a indisponibilidade é uma reserva → chamamos de reserva de fato
  * Quando a indisponibilidade não é uma reserva de fato → chamamos de bloqueio

É uma tabela bem grande já que, para todos os listings do Brasil, todos os dias, todo o calendário do imóvel é scrapado. São aproximadamente 149 Milhões de novas linhas que são inseridas nessa tabela por dia, todos os dias.

Obs.: diárias com preço > R$50.000,00 são filtradas para fora desta tabela, já que são competidores que geralmente escreveram o preço errado ou competidores que estão distantes do perfil de imóvel da Seazone (foi feito um estudo para validar isso, mesmo nos casos de reservas que são normalmente mais caras, como no reveillon).

* **Colunas:**

| **Nome da coluna** | **descrição** | **tipo de dado** |
|----|----|----|
| airbnb_listing_id | ID do listing no Airbnb | string |
| date | Data a qual o preço e a disponibilidade se referem (é a data selecionada no calendário do listing) | date |
| available | Indica se o listing está disponível ou não | string |
| price | Preço da diária | float |
| price_string | Preço da diária no formato texto | string |
| min_stay | Estadia mínima naquela data | smallint |
| av_for_checkin | Disponibilidade de checkin | string |
| av_for_checkout | Disponibilidade de checkout | string |
| aquisition_date | Data da aquisição dos dados na camada Raw | timestamp |
| ano | Ano de "aquisition_date" | string |
| mes | Mês de "aquisition_date" | string |
| dia | Dia de "aquisition_date" | string |

**Frequência:** 1x por dia

### price_av_dropped

**Descrição:** São os dados que iriam para a price_av da camada Clean mas foram filtrados por algum motivo. Essa tabela indica o motivo.

* **Colunas:**

| **Nome da coluna** | **descrição** | **tipo de dado** |
|----|----|----|
| airbnb_listing_id | ID do listing no Airbnb | string |
| date | Data a qual o preço e a disponibilidade se referem (é a data selecionada no calendário do listing) | date |
| available | Indica se o listing está disponível ou não | string |
| price | Preço do listing | float |
| price_string | Preço do listing no formato texto | string |
| min_stay | Estadia mínima naquela data | smallint |
| av_for_checkin | Disponibilidade de checkin | string |
| av_for_checkout | Disponibilidade de checkout | string |
| aquisition_date | Data da aquisição dos dados na camada Raw | timestamp |
| drop_reason | Motivo pelo qual o dado foi filtrado para fora da price_av | string |
| ano | Ano de "aquisition_date" | string |
| mes | Mês de "aquisition_date" | string |
| dia | Dia de "aquisition_date" | string |

**Frequência:** 1x por dia

### seazone_listings_historic

**Descrição:** Tabela com a relação entre o ID de um listing no Airbnb e o ID interno do listing dentro da Seazone. Puxa os dados diretamente da conta do Airbnb da Seazone.

Armazena todo o histórico (já que o ID dentro da Seazone não muda, mas um anúncio pode ser refeito no Airbnb e consequentemente seu ID Airbnb mudar).

Exemplo:

| **airbnb_listing_id** | **id_seazone** | **aquisition_date** |
|----|----|----|
| 48420221 | JBV108 | 12/07/2023 |
| … | … |    |
| 875461348 | JBV108 | 12/12/2023 |

Caso queira ver apenas a última relação (ou seja, a que está atualmente válida), veja "[seazone_listings](/doc/catalogo-interno-de-dados-do-pipe-Z7Ccq3Ixjv)".

* **Colunas:**

| **Nome da coluna** | **descrição** | **tipo de dado** |
|----|----|----|
| airbnb_listing_id | ID do listing no Airbnb | string |
| id_seazone | ID do listing na Seazone | string |
| aquisition_date | Data de aquisição dos dados | timestamp |
| ano | Ano de "aquisition_date" | string |
| mes | Mês de "aquisition_date" | string |
| dia | Dia de "aquisition_date" | string |

*Essa tabela não possui variante na camada Raw, os dados são lançados diretamente na camada Clean.*

**Frequência:** 1x por dia

### seazone_listings

**Descrição:** Tabela com a relação entre o ID de um listing no Airbnb e o ID interno do listing na Seazone.

Possui apenas a última relação adquirida pelo scraper (ou seja, aquela que está atualmente válida).

Caso queira ver todo o histórico de mudança, veja "[seazone_listings_historic](/doc/catalogo-interno-de-dados-do-pipe-Z7Ccq3Ixjv)".

* **Colunas:**

| **Nome da coluna** | **descrição** | **tipo de dado** |
|----|----|----|
| airbnb_listing_id | ID do listing no Airbnb | string |
| id_seazone | ID do listing na Seazone | string |

**Frequência:** 1x por dia

### urbit

**Descrição:** Tabela com dados geográficos, estatísticos e sociais de várias localizações (Estado/Cidade/Bairro).

* **Colunas:**

| **Nome da coluna** | **descrição** | **tipo de dado** |
|----|----|----|
| estado | Estado (UF) | string |
| cidade | Cidade | string |
| bairro | Bairro | string |
| renda média | renda média per capta | double |
| potencial de consumo |    | double |
| domicílios totais | Número de domicílios | double |
| apartamentos | Número de apartamentos | double |
| % domiciios b.r |    | double |
| # domicilios a.r |    | double |
| % esgoto aberto |    | double |
| % dom. c/ trataento sanitário |    | double |
| tem favela em 2km? |    | bigint |
| ivs-média |    | double |
| ivs-mínimo |    | double |
| ivs-máximo |    | double |
| distância aeroporto (km) |    | double |
| nome aeroporto |    | string |
| ticket médio aptos 1q |    | bigint |
| m2 média aptos 1q |    | bigint |
| ticket médio aptos 2q |    | bigint |
| m2 médio aptos 2q |    | bigint |
| empreendimentos em lançamentos na região |    | bigint |

**Frequência:** estática

### vivareal_listing_type

**Descrição:** Tabela com a equivalência entre os inúmeros tipos de listing que o Vivareal permite cadastrar e alguns tipos de listing que a Seazone trata (apartamento, casa, hotel ou outros). Há mais de 40 dessas equivalências hoje, exemplo:

| **listing_type** | **usage_type** | **new_type** |
|----|----|----|
| APARTMENT | RESIDENTIAL | apartamento |
| HOME | RESIDENTIAL | casa |
| CONDOMINIUM | RESIDENTIAL | casa |
| COUNTRY_HOUSE | RESIDENTIAL | outros |
| RESIDENTIAL_ALLOTMENT_LAND | RESIDENTIAL | terreno |
| SHED_DEPOSIT_WAREHOUSE | COMMERCIAL | comercial |

* **Colunas:**

| **Nome da coluna** | **descrição** | **tipo de dado** |
|----|----|----|
| unit_type | Tipo 1 do listing (apartamento, casa, fazenda, galpão etc) | string |
| usage_type | Tipo 2 do listing (residencial, comercial etc) | string |
| new_type | Novo tipo do listing (terreno, comercial, apartamento, casa, outros) | string |

**Frequência:** estática

### vivareal

**Descrição:** Tabela com os listings do Vivareal e Zap. Possui informações do listing (como preço, título, tipo de anúncio, localização), do dono do listing, e dados de contato. Diversos processos de limpeza são aplicados e listing types são mapeados para alguns tipos específicos utilizando a tabela "vivareal_listing_type".

* **Colunas:**

| **Nome da coluna** | **descrição** | **tipo de dado** |
|----|----|----|
| listing_id | ID do listing no Vivareal/Zap | string |
| link_name | Título 1 do listing | string |
| link_url | URL do listing | string |
| listing_newness | Se é imóvel novo ou usado | string |
| listing_title | Título 2 do listing | string |
| listing_desc | Descrição do listing | string |
| business_types | Se é venda/aluguel ou ambos | string |
| listing_type | Tipo do listing (já com o listing_type convertido para o que a Seazone utiliza internamente) | string |
| property_type | Se é um imóvel único ou parte de um condomínio | string |
| sale_price | Preço de venda | string |
| rental_price | Preço de aluguel | string |
| rental_period | Tipo do contrato de aluguel (anual, mensal, semanal), caso aplicável | string |
| yearly_iptu | Valor do aluguel anual | float |
| monthly_condo_fee | Valor do condomínio mensal | float |
| amenities | Itens/comodidades do listing e ou do condomínio que ele faz parte (ar condicionado, academia, churrasqueira, piscina, varada etc) | string |
| usable_rea | Área útil do listing | int |
| bathrooms | Número de banheiros | smallint |
| bedrooms | Número de quartos | smallint |
| parking_spaces | Número de vagas de garagem | smallint |
| country | País do listing | string |
| state | Estado (UF) do listing | string |
| city | Cidade do listing | string |
| suburb | Bairro do listing | string |
| zipcode | CEP do listing | string |
| advertiser_id | ID do proprietário do listing | string |
| advertiser_name | Nome do proprietário do listing | string |
| advertiser_phones | Telefones do proprietário do listing | string |
| advertiser_whatsapp | Whatsapp do proprietário do listing | string |
| advertiser_url | URL do perfil do proprietário do listing | string |
| portal | Se é do Vivareal ou Zap | string |
| aquisition_date | Data de aquisição dos dados na camada Raw | timestamp |
| ano | Ano em "aquisition_date" | string |
| mes | Mês em "aquisition_date" | string |
| dia | Dia em "aquisition_date" | string |

**Frequência:** 1x por semana


## Camada ENRICHED

### block_and_occupancy

**Depende de**:

* clean.price_av
* clean.date
* enriched.booked_on

**Descrição:** É a tabela que é uma "evolução" direta da tabela "booked_on". Enquanto na "booked_on" o objetivo é ver quais datas foram ocupadas, aqui o objetivo é classificar essas datas ocupadas em **bloqueio** ou **reservas de fato**.

Logo, essa tabela tem sempre dados únicos para um par "imóvel/data". Para cada par "imóvel/data" será indicado o preço da diária naquele dia, preço com desconto, se é um bloqueio ou reserva de fato, quando a data se tornou indisponível (que no caso de uma reserva de fato é a data de criação da reserva) etc.

Esta tabela é 100% dependente de processos de inteligência, que no momento são heurísticas definidas após extensa análise dos dados.

* **Colunas:**

| **Nome da coluna** | **descrição** | **tipo de dado** |
|----|----|----|
| airbnb_listing_id | ID do listing no Airbnb | string |
| date | Data a qual os dados se referem | date |
| month | Mês em "date" | int |
| price | Preço da diária | double |
| price_after_discount | Preço da diária após o desconto por duração de estadia | double |
| available | Indica se a data está disponível ou indisponível | string |
| min_stay | Estadia mínima naquela data | int |
| av_for_checkin | Disponibilidade de checkin | string |
| av_for_checkout | Disponibilidade de checkout | string |
| aquisition_date | Data em que os dados foram adquiridos na camada Raw, na tabela "listing_price_av" | timestamp |
| cleaning_fee | Taxa de limpeza | double |
| price_string | Preço da diária no formato de texto | string |
| booked_on | Indica quando a data "date" deixou de estar disponível, logo, caso seja uma reserva de fato, também indica a data de criação da reserva | timestamp |
| blocked | Indica se é um bloqueio ou não | boolean |
| block_reason | Indica a razão de ter sido identificado como bloqueio (caso tenha sido) | string |
| occupied | Indica se é uma reserva de fato ou não | string |
| ano | Ano em "aquisition_date" | string |
| mes | Mês em "aquisition_date" | string |
| dia | Dia em "aquisition_date" | string |

**Frequência:** 1x por semana

### booked_on

**Descrição:** É a tabela que é uma "evolução" da tabela "price_av" da camada CLEAN. Enquanto na "price_av" o foco é olhar para datas do calendário de um imóvel individualmente e verificar o preço/disponibilidade delas, aqui o objetivo é comparar datas do calendário de um imóvel em diferentes dias e marcar os dias em que uma certa data deixou estar disponível.

**Exemplo:** Pela comparação dos calendários abaixo, sabemos que os dias 20/08/23, 21/08/23 e 22/08/23 deixaram de estar disponíveis entre 18/07/23 e 19/07/2023 (assim assumimos que o dia que deixou de estar disponível é **19/07/2023**). O dia 19/07/2023 é o que chamamos de "booked_on" na coluna desta tabela (e também o nome da própria tabela).

*Calendário do imóvel XYZ123 em **18/07/2023***

 ![Untitled](Cata%CC%81logo%20Interno%20de%20Dados%20do%20Pipe%20b47c172b039e4f41a58ce2f97d6b80ca/Untitled.png)

*Calendário do imóvel XYZ123 em **19/07/2023***

 ![Untitled](Cata%CC%81logo%20Interno%20de%20Dados%20do%20Pipe%20b47c172b039e4f41a58ce2f97d6b80ca/Untitled%201.png)

* **Colunas:**

| **Nome da coluna** | **descrição** | **tipo de dado** |
|----|----|----|
| airbnb_listing_id | ID do listing no Airbnb | string |
| date | Data a qual os dados se referem | date |
| price | Preço da diária | double |
| available | Indica se a data está disponível ou indisponível | string |
| min_stay | Estadia mínima naquela data | int |
| av_for_checkin | Disponibilidade de checkin | string |
| av_for_checkout | Disponibilidade de checkout | string |
| aquisition_date | Data em que os dados foram adquiridos na camada Raw, na tabela "listing_price_av" | timestamp |
| price_string | Preço da diária no formato de texto | string |
| booked_on | Indica quando a data "date" deixou de estar disponível | timestamp |
| ano | Ano em "aquisition_date" | string |
| mes | Mês em "aquisition_date" | string |
| dia | Dia em "aquisition_date" | string |

**Frequência:** 1x por dia

**Descrição técnica:**

**[Cálculo de booked_on](/doc/calculo-de-booked_on-P903oulN3W)**


**Descrição:** Lista dos anunciantes (corretores e imobiliárias) que aparecem no Vivareal, com dados como nome, contato (telefone ou whatsapp), número de anúncios, número de terrenos, número de apartamentos/casas, localizações que ele atua (Estado-Cidade-Bairro).

Há um [sabor de sorvete](/doc/sorveteria-de-dados-n0Gi0dQDpg) que já fornece esses dados!!

* **Colunas:**

| **Nome da coluna** | **descrição** | **tipo de dado** |
|----|----|----|
| advertiser_id | ID do anunciante | string |
| advertiser_name | Nome do anunciante | string |
| advertiser_phones | Telefone do anunciante | string |
| advertiser_whatsapp | Whatsapp do anunciante | string |
| advertiser_url | URL do perfil do anunciante | string |
| anuncios | Número de listings que o anunciante possui cadastrado | bigint |
| terrenos | Número de terrenos que o anunciante possui cadastrado | bigint |
| apartamento_ou_casa | Número de apartamentos e casas que o anunciante possui cadastrado | bigint |
| location_array | Array (lista) com todas as localizações que o anunciante possui listings. As localizações estão no formato: Estado-Cidade-Bairro. | string |

**Frequência:** 1x por semana

### daily_fat

**Descrição:** Esta é a tabela que compila o faturamento diário de qualquer imóvel do Airbnb. É uma "evolução" direta da "block_and_occupancy".

A lógica é simples. Para um par "imóvel/data":

* se houve uma reserva de fato, o faturamento daquele dia é o preço da reserva após o desconto;
* se não houve uma reserva de fato (pois foi bloqueado ou porque ficou disponível), o faturamento é R$0,00
* **Colunas:**

| **Nome da coluna** | **descrição** | **tipo de dado** |
|----|----|----|
| airbnb_listing_id | ID do listing no Airbnb | string |
| date | Data a qual os dados se referem | date |
| month | Mês em "date" | int |
| price | Preço da diária | double |
| price_after_discount | Preço da diária após o desconto por duração de estadia | double |
| available | Indica se a data está disponível ou indisponível | string |
| min_stay | Estadia mínima naquela data | int |
| av_for_checkin | Disponibilidade de checkin | string |
| av_for_checkout | Disponibilidade de checkout | string |
| aquisition_date | Data em que os dados foram adquiridos na camada Raw, na tabela "listing_price_av" | timestamp |
| cleaning_fee | Taxa de limpeza | double |
| price_string | Preço da diária no formato de texto | string |
| booked_on | Indica quando a data "date" deixou de estar disponível, logo, caso seja uma reserva de fato, também indica a data de criação da reserva | timestamp |
| blocked | Indica se é um bloqueio ou não | boolean |
| block_reason | Indica a razão de ter sido identificado como bloqueio (caso tenha sido) | string |
| occupied | Indica se é uma reserva de fato ou não | string |
| year | Ano em "date" | int |
| day_fat | Faturamento do listing naquele dia | double |
| day_fat_after_discount | Faturamento do listing, naquele dia, após o desconto por duração de estadia | double |
| ano | Ano em "aquisition_date" | string |
| mes | Mês em "aquisition_date" | string |
| dia | Dia em "aquisition_date" | string |

**Frequência:** 1x por semana

### dead_alive

**Descrição:** Tabela que fornece a informação se o listing está ativo ou inativo no Airbnb, o dia que foi scrapado pela primeira vez, o dia que ele morreu (caso tenha sido inativado) etc.

* **Colunas:**

| **Nome da coluna** | **descrição** | **tipo de dado** |
|----|----|----|
| airbnb_listing_id | ID do listing no Airbnb | string |
| date_of_birth | Data em que o listing foi scrapado pelo Pipe pela primeira vez | date |
| last_aq_date | Última data em que o listing foi scrapado pelo Pipe | date |
| alive | Indica se o listing está ativo ou inativo | boolean |
| date_of_death | Data em que o listing deixou de estar ativo | date |
| ano | Ano em "last_aq_date" | string |
| mes | Mês em "last_aq_date" | string |
| dia | Dia em "last_aq_date" | string |

**Frequência:** 1x por semana

### details (details_last_aquisition)

**Descrição:** Tabela equivalente à 'details' da camada CLEAN, porém possui apenas a última aquisição dos dados (ao invés de guardar o histórico todo), ou seja, os detalhes mais recentes de cada listing.

* **Colunas:**

| **Nome da coluna** | **descrição** | **tipo de dado** |
|----|----|----|
| airbnb_listing_id | ID do listing no Airbnb | string |
| url | URL do listing | string |
| ad_name | Título do listing | string |
| ad_description | Descrição do listing | string |
| space | Descrição do espaço do listing (funciona como um complemento de "ad_description") | string |
| house_rules | Regras do listing | string |
| amenities | Indica todas as comodidades do listing (cozinha, estacionamento, piscina, wi-fi, fogueira, etc) | string |
| safety_features | Indica todos os equipamentos de segurança do listing | string |
| number_of_bathrooms | Número de banheiros | double |
| number_of_bedrooms | Número de quartos | bigint |
| number_of_beds | Número de camas | bigint |
| latitude | Latitude do listing | double |
| longitude | Longitude do listing | double |
| star_rating | Nota geral do listing | double |
| additional_house_rules | Regras adicionais do listing | string |
| owner | Proprietário do listing(é um ID único dentro do Airbnb, o ID do anunciante) | string |
| check_in | Horário de checkin | string |
| check_out | Horário de checkout | string |
| number_of_guests | Número máximo de hóspedes permitido | bigint |
| is_superhost | Indica se é superhost ou não | string |
| number_of_reviews | Número de reviews que o listing possui | bigint |
| cohost | Coproprietários do listing (não é um ID único, é informado apenas o nome do coproprietário) | string |
| cleaning_fee | Taxa de limpez | double |
| can_instant_book | Indica se o instant book está ativado ou não | string |
| owner_id | ID único do proprietário do listing dentro do Airbnb | string |
| aquisition_date | Data de aquisição dos dados na camada Raw | timestamp |
| is_dead | Indica se o listing está ativo ou inativo | boolean |
| listing_type | Tipo do listing (já realizada a [equivalência entre os tipos](/doc/catalogo-interno-de-dados-do-pipe-Z7Ccq3Ixjv) do Airbnb e os tipos que a Seazone considera, ou seja, aqui é o tipo que a Seazone considera) | string |
| picture_count | Número de fotos do anúncio | bigint |
| min_nights | Estadia mínima | bigint |
| response_rate_shown | Taxa de resposta do host do listing | string |
| response_time_shown | Tempo que o host costuma levar para responder | string |
| guest_satisfaction_overall |    | bigint |
| index |    |    |
| ano | Ano de "aquisition_date" | string |
| mes | Mês de "aquisition_date" | string |
| dia | Dia de "aquisition_date" | string |

**Frequência:** 1x por semana

### host_star_rating

**Descrição:** Tabela que mostra a nota dos anunciantes do Airbnb.

* **Colunas:**

| **Nome da coluna** | **descrição** | **tipo de dado** |
|----|----|----|
| owner_id | ID do anunciante no Airbnb | string |
| total_listings | Número total de listings que o anunciante possui | bigint |
| mean_star_rating | Nota média do anunciante | double |
| max_star_rating | Nota máxima do anunciante | double |
| min_star_rating | Nota mínima do anunciante | double |

**Frequência:** 1x por semana


**Descrição:** Possui os imóveis do tipo "casa" ou "apartamento" listados como "aluguel" na OLX e Vivareal. Possui informações da página do anúncio (tamanho, número de quartos, banheiros etc), preço etc.

* **Colunas:**

| **Nome da coluna** | **descrição** | **tipo de dado** |
|----|----|----|
| listing_id | ID do listing no Vivareal ou OLX | string |
| title | Título do listing | string |
| description | Descrição do listing | string |
| link_url | URL (link) do listing | string |
| price | Preço do aluguel | float |
| owner | Nome do proprietário do listing | string |
| bedrooms | Número de quartos | smallint |
| bathrooms | Número de banheiros | smallint |
| garage | Número de vagas de garagem | smallint |
| usable_area | Área útil | int |
| condominium | Preço do condomínio | float |
| iptu | Preço do IPTU | float |
| data_primeira_aquisicao | Data da primeira aquisição do listing pelo Pipe | timestamp |
| data_ultima_aquisicao | Data da última aquisição (a mais recente) do listing pelo Pipe | timestamp |
| type | Tipo do listing (se casa ou apartamento) | string |

**Frequência:** 1x por semana


**Descrição:** Possui os imóveis do tipo "casa" ou "apartamento" listados como "venda" na OLX e Vivareal. Possui informações da página do anúncio (tamanho, número de quartos, banheiros etc), preço etc.

* **Colunas:**

| **Nome da coluna** | **descrição** | **tipo de dado** |
|----|----|----|
| listing_id | ID do listing no Vivareal ou OLX | string |
| title | Título do listing | string |
| description | Descrição do listing | string |
| link_url | URL (link) do listing | string |
| price | Preço de venda | float |
| price_per_meter | Preço de venda do metro quadrado | float |
| owner | Nome do proprietário do listing | string |
| bedrooms | Número de quartos | smallint |
| bathrooms | Número de banheiros | smallint |
| garage | Número de vagas de garagem | smallint |
| usable_area | Área útil | int |
| iptu | Preço do IPTU | float |
| data_primeira_aquisicao | Data da primeira aquisição do listing pelo Pipe | timestamp |
| data_ultima_aquisicao | Data da última aquisição (a mais recente) do listing pelo Pipe | timestamp |
| type | Tipo do listing (se casa ou apartamento) | string |

**Frequência:** 1x por semana

### monthly_fat

**Descrição:** É tabela que compila o faturamento mensal de qualquer imóvel do Airbnb. É uma "evolução" direta da "daily_fat" (os dados são agrupados por mês). Também são inseridos os dados de faturamento mensal levantados pelo Airdna (útil para comparar faturamento informado pelo Pipe vs Airdna).

* **Colunas:**

| **Nome da coluna** | **descrição** | **tipo de dado** |
|----|----|----|
| airbnb_listing_id | ID do listing no Airbnb | string |
| month | Mês a qual os dados se referem | int |
| year | Ano a qual os dados se referem | int |
| month_fat_pipe | Faturamento do listing naquele mês, informado pelo Pipe | double |
| month_fat_pipe_after_discount | Faturamento do listing, naquele mês, após o desconto por duração de estadia, informado pelo Pipe | double |
| month_fat_airdna | Faturamento do listing naquele mês, informado pelo Airdna | double |
| avg_price_pipe | Preço médio da diária das reservas de fato, informado pelo Pipe | double |
| avg_price_pipe_after_discount | Preço médio da diária das reservas de fato, após o desconto por duração de estadia, informado pelo Pipe | double |
| avg_price_airdna | Preço médio da diária das reservas de fato, informado pelo Airdna | double |
| days_in_month_pipe | Número de dias que o imóvel poderia ter faturado naquele mês (se o imóvel entrou no meio do mês ele não poderia ter faturado no mês inteiro), informado pelo Pipe | bigint |
| days_in_month_airdna | Número de dias que o imóvel poderia ter faturado naquele mês, informado pelo Airdna | int |
| occupied_dates_pipe | Número de dias com reservas de fato do listing naquele mês, informado pelo Pipe | bigint |
| occupied_dates_airdna | Número de dias com reservas de fato do listing naquele mês, informado pelo Airdna | smallint |
| available_dates_pipe | Número de dias disponíveis do listing naquele mês, informado pelo Pipe | bigint |
| available_dates_airdna | Número de dias disponíveis do listing naquele mês, informado pelo Airdna | smallint |
| blocked_dates_pipe | Número de dias bloqueados do listing naquele mês, informado pelo Pipe | bigint |
| blocked_dates_airdna | Número de dias bloqueados do listing naquele mês, informado pelo Airdna | smallint |
| ano | Ano a qual os dados se referem | string |
| mes | Mês a qual os dados se referem | string |

**Frequência:** 1x por semana

### monthly_fat_locations

**Descrição:** É a tabela com os faturamentos mensais dos listings do Airbnb, porém agrupada por Estado, Cidade e Bairro. É a "monthly_fat" agrupada por Estado, Cidade, Bairro.

* **Colunas:**

| **Nome da coluna** | **descrição** | **tipo de dado** |
|----|----|----|
| city | Cidade | string |
| suburb | Bairro | string |
| count_listings | Número de listings naquela localização | bigint |
| average_revenue | Faturamento mensal médio dos listings daquela localização | double |
| count_apartament | Número de apartamentos | bigint |
| count_house | Número de casas | bigint |
| count_super_hosts | Número de super hosts naquela localização | bigint |
| count_owners | Número de proprietários (donos dos listings/anúncions) naquela região | bigint |
| count_qualified_listings | Número de listings qualificados, que são aqueles com +10 reviews, instant book e faturamento nos últimos 6 meses maior que zero | bigint |
| month_year | Mês e ano a qual os dados se referem | string |
| state | Estado (UF) | string |

**Frequência:** 1x por mês


**Descrição:** Possui os imóveis do tipo "terreno" listados como "venda" na OLX e Vivareal. Possui informações da página do anúncio (tamanho, número de quartos, banheiros etc), preço etc.

* **Colunas:**

| **Nome da coluna** | **descrição** | **tipo de dado** |
|----|----|----|
| listing_id | ID do listing no Vivareal ou OLX | string |
| title | Título do listing | string |
| description | Descrição do listing | string |
| link_url | URL (link) do listing | string |
| price | Preço de venda | float |
| price_per_meter | Preço de venda do metro quadrado | float |
| owner | Nome do proprietário do listing | string |
| usable_area | Área útil | int |
| iptu | Preço do IPTU | float |
| data_primeira_aquisicao | Data da primeira aquisição do listing pelo Pipe | timestamp |
| data_ultima_aquisicao | Data da última aquisição (a mais recente) do listing pelo Pipe | timestamp |

**Frequência:** 1x por semana

### booking_details_price_av

**Descrição:** Tabela com informações sobre preço, disponibilidade e detalhes dos imóveis do Booking da Seazone e da cidade do Rio de Janeiro, executada semanalmente. Ela é particionada pela coluna aquisition_date_partition.

* **Colunas:**

| **Nome da Coluna** | **Descrição** | **Tipo de Dado** |
|----|----|----|
| ```none
booking_listing_id
``` | ID do hotel no sistema de reservas. | string |
| ```none
date
``` | Data referente ao preço e disponibilidade. | date |
| ```none
price
``` | Preço do hotel para a data especificada. | int |
| ```none
available
``` | Indica se o hotel está disponível para a data especificada. | boolean |
| ```none
min_stay
``` | Duração mínima da estadia em noites. | Int32 |
| ```none
max_rooms
``` | Maior número de quartos entre imóveis no anúncio | Int32 |
| ```none
min_rooms
``` | Menor número de quartos entre imóveis no anúncio | Int32 |
| ```none
booking_listing_url
``` | URL da página do anúncio no Booking | string |
| ```none
aquisition_date
``` | Data de aquisição do dado, incluindo data e hora. | timestamp |
| ```none
aquisition_date_partition
``` | Partição pela data de aquisição do dado. | date (Particionado) |

**Frequência:** Semanal (segundas às 12:30 UTC)

### analise_faturamento


## Camada MODELS

### daily_fat_blockdetected

**Descrição:** Tabela equivalente à 'daily_fat' da camada ENRICHED porém utilizando a "inteligência" de detecção de bloqueios a partir de um algoritmo de Machine Learning chamado XGBoost Classifier.

* **Colunas:**

| **Nome da coluna** | **descrição** | **tipo de dado** |
|----|----|----|
| airbnb_listing_id | ID do listing no Airbnb | string |
| date | Data a qual os dados se referem | date |
| daily_fat | Faturamento do listing naquele dia | double |
| blocked | Indica se o dia era um bloqueio ou não | int |

**Frequência:** 1x por semana

### daily_fat_blocked_detected_nn

**Descrição:** Tabela equivalente à 'daily_fat' da camada ENRICHED porém utilizando a "inteligência" de detecção de bloqueios a partir de um algoritmo de Machine Learning chamado "Redes Neurais" (Neural Networks).

* **Colunas:**

| **Nome da coluna** | **descrição** | **tipo de dado** |
|----|----|----|
| airbnb_listing_id | ID do listing no Airbnb | string |
| date | Data a qual os dados se referem | date |
| price | Preço da diária | double |
| price_after_discount | Preço da diária após o desconto por duração de estadia | double |
| aquisition_date | Data em que os dados foram adquiridos na camada Raw, na tabela "listing_price_av" | timestamp |
| daily_fat_after_discount | Faturamento do listing, naquele dia, após o desconto por duração de estadia | double |
| daily_fat | Faturamento do listing naquele dia | double |

**Frequência:** 1x por semana

### listings_between_percentile

**Descrição:** Tabela com a cntagem de quantos listings estão dentro de um certo intervalo de percentis, para cada cenário (cidade, bairro, listing type, etc).

Por cenário aqui entende-se: Estado, Cidade, Bairro, Listing type (apto, casa, hotel ou outros) e número de quartos.

* **Colunas:**

| **Nome da coluna** | **descrição** | **tipo de dado** |
|----|----|----|
| state | Estado (UF) | string |
| city | Cidade | string |
| suburb | Bairro | string |
| type | Tipo de listings (apto, casa, hotel ou outros) | string |
| bedrooms | Número de quartos | bigint |
| percentile | Intervalo de percentis a qual os dados se referem | string |
| count_listings | Contagem de quantos listings estão dentro do intervalo de percentis | bigint |

**Frequência:** 1x por mês

### listings_percentile

**Descrição:** Tabela que atribui, para cada listing do Airbnb, qual percentil de faturamento ele se encontra dado o seu cenário. É baseada nos resultados da tabela "monthly_revenue_percentile".

Por cenário aqui entende-se: Estado, Cidade, Bairro, Listing type (apto, casa, hotel ou outros) e número de quartos.

* **Colunas:**

| **Nome da coluna** | **descrição** | **tipo de dado** |
|----|----|----|
| airbnb_listing_id | ID do listing no Airbnb | string |
| percentile | Qual percentil ele está dentro do seu cenário | double |
| little_data_av | Indica que tem poucos dados disponíveis para dar um bom resultado | boolean |

**Frequência:** 1x por mês

### monthly_fat_blockdetected

**Descrição:** Tabela equivalente à 'monthly_fat' da camada ENRICHED porém utilizando a "inteligência" de detecção de bloqueios a partir de um modelo de Machine Learning chamado XGBoost Classifier.

* **Colunas:**

| **Nome da coluna** | **descrição** | **tipo de dado** |
|----|----|----|
| airbnb_listing_id | ID do listing no Airbnb | string |
| ano_mes | Ano e mês a qual os dados se referem | string |
| monthly_fat_ml3 | Faturamento do listing naquele mês | double |
| year | Ano a qual os dados se referem | string |
| month | Mês a qual os dados se referem | string |

**Frequência:** 1x por semana

### monthly_fat_blockdetected_nn

**Descrição:** Tabela equivalente à 'monthly_fat' da camada ENRICHED porém utilizando a "inteligência" de detecção de bloqueios a partir de um algoritmo de Machine Learning chamado "Redes Neurais" (Neural Networks).

* **Colunas:**

| **Nome da coluna** | **descrição** | **tipo de dado** |
|----|----|----|
| airbnb_listing_id | ID do listing no Airbnb | string |
| monthly_fat_nn | Faturamento do listing naquele mês | double |
| monthly_fat_nn_after_discount | Faturamento do listing, naquele mês, após o desconto por duração de estadia | double |
| year | Ano a qual os dados se referem | string |
| month | Mês a qual os dados se referem | string |

**Frequência:** 1x por semana

### monthly_occupancy_metrics

**Descrição:** Tabela com o número de meses utilizado para o cálculo dos percentis, para cada mês, no modelo "monthly-occupancy-models".

* **Colunas:**

| **Nome da coluna** | **descrição** | **tipo de dado** |
|----|----|----|
| state | Estado (UF) | string |
| city | Cidade | string |
| suburb | Bairro | string |
| type | Tipo de listings (apto, casa, hotel ou outros) | string |
| bedrooms | Número de quartos | bigint |
| month | Mês a qual os dados se referem | int |
| total_months | Quantidade total de meses, em todos os diferentes anos, em todos os diferentes listings, que foram utilizados para o cálculo dos percentis | bigint |

**Frequência:** 1x por mês

### monthly_occupancy_models

**Descrição:** Tabela com os resultados do modelo "monthly-occupancy-models", que indica, para cada cenário, quais são os percentis de taxa de ocupação dos listings daquele cenário em cada mês do ano (todos os meses dos diferentes anos são agrupados).

Por cenário aqui entende-se: Estado, Cidade, Bairro, Listing type (apto, casa, hotel ou outros) e número de quartos.

* **Colunas:**

| **Nome da coluna** | **descrição** | **tipo de dado** |
|----|----|----|
| state | Estado (UF) | string |
| city | Cidade | string |
| suburb | Bairro | string |
| type | Tipo de listings (apto, casa, hotel ou outros) | string |
| bedrooms | Número de quartos | bigint |
| month | Mês a qual os dados se referem | int |
| percentil | Percentil de faturamento (25%, 50%, 60%, 75% ou 90%) | string |
| occupancy_rate | Valor detaxa de ocupação daquele cenário, naquele percentil, naquele mês | double |

**Frequência:** 1x por mês

### monthly_revenue_metrics

**Descrição:** Tabela com o número de meses utilizado para o cálculo dos percentis, para cada mês, no modelo "monthly-revenue-models".

* **Colunas:**

| **Nome da coluna** | **descrição** | **tipo de dado** |
|----|----|----|
| state | Estado (UF) | string |
| city | Cidade | string |
| suburb | Bairro | string |
| type | Tipo de listings (apto, casa, hotel ou outros) | string |
| bedrooms | Número de quartos | bigint |
| month | Mês a qual os dados se referem | int |
| total_months | Quantidade total de meses, em todos os diferentes anos, em todos os diferentes listings, que foram utilizados para o cálculo dos percentis | bigint |

**Frequência:** 1x por mês

### monthly_revenue_metrics_by_city

**Descrição:** Tabela com o número de meses utilizado para o cálculo dos percentis, para cada mês, no modelo "monthly-revenue-models-by-city".

* **Colunas:**

| **Nome da coluna** | **descrição** | **tipo de dado** |
|----|----|----|
| state | Estado (UF) | string |
| city | Cidade | string |
| type | Tipo de listings (apto, casa, hotel ou outros) | string |
| bedrooms | Número de quartos | bigint |
| month | Mês a qual os dados se referem | int |
| total_months | Quantidade total de meses, em todos os diferentes anos, em todos os diferentes listings, que foram utilizados para o cálculo dos percentis | bigint |

**Frequência:** 1x por mês

### monthly_revenue_metrics_by_year

**Descrição:** Tabela com o número de meses utilizado para o cálculo dos percentis, para cada mês, no modelo "monthly-revenue-models-by-year".

* **Colunas:**

| **Nome da coluna** | **descrição** | **tipo de dado** |
|----|----|----|
| state | Estado (UF) | string |
| city | Cidade | string |
| suburb | Bairro | string |
| type | Tipo de listings (apto, casa, hotel ou outros) | string |
| bedrooms | Número de quartos | bigint |
| year | Mês a qual os dados se referem | int |
| month | Mês a qual os dados se referem | int |
| total_months | Quantidade total de meses, em todos os diferentes anos, em todos os diferentes listings, que foram utilizados para o cálculo dos percentis | bigint |

**Frequência:**

### monthly_revenue_models

**Descrição:** Tabela com os resultados do modelo "monthly-revenue-models", que indica, para cada cenário, quais são os percentis de faturamento dos listings daquele cenário em cada mês do ano (todos os meses dos diferentes anos são agrupados).

Por cenário aqui entende-se: Estado, Cidade, Bairro, Listing type (apto, casa, hotel ou outros) e número de quartos.

* **Colunas:**

| **Nome da coluna** | **descrição** | **tipo de dado** |
|----|----|----|
| state | Estado (UF) | string |
| city | Cidade | string |
| suburb | Bairro | string |
| type | Tipo de listings (apto, casa, hotel ou outros) | string |
| bedrooms | Número de quartos | bigint |
| month | Mês a qual os dados se referem | int |
| percentil | Percentil de faturamento (25%, 50%, 60%, 75% ou 90%) | string |
| faturamento | Valor de faturamento daquele cenário, naquele percentil, naquele mês | double |

**Frequência:** 1x por mês

### monthly_revenue_models_by_city

**Descrição:** Tabela equivalente à "monthly_revenue_models" porém o cenário agora é maior por não incluir a divisão por bairros.

Por cenário aqui entende-se: Estado, Cidade, Listing type (apto, casa, hotel ou outros) e número de quartos.

* **Colunas:**

| **Nome da coluna** | **descrição** | **tipo de dado** |
|----|----|----|
| state | Estado (UF) | string |
| city | Cidade | string |
| type | Tipo de listings (apto, casa, hotel ou outros) | string |
| bedrooms | Número de quartos | bigint |
| month | Mês a qual os dados se referem | int |
| percentil | Percentil de faturamento (25%, 50%, 60%, 75% ou 90%) | string |
| faturamento | Valor de faturamento daquele cenário, naquele percentil, naquele mês | double |

**Frequência:** 1x por mês

### monthly_revenue_models_by_year

**Descrição:** Tabela equivalente à "monthly_revenue_models" porém os valores de faturamento são divididos pelo mês de um ano específico (os meses de anos diferentes **não** são agrupados).

Por cenário aqui entende-se: Estado, Cidade, Bairro, Listing type (apto, casa, hotel ou outros) e número de quartos.

* **Colunas:**

| **Nome da coluna** | **descrição** | **tipo de dado** |
|----|----|----|
| state | Estado (UF) | string |
| city | Cidade | string |
| suburb | Bairro | string |
| type | Tipo de listings (apto, casa, hotel ou outros) | string |
| bedrooms | Número de quartos | bigint |
| year | Ano a qual os dados se referem | int |
| month | Mês a qual os dados se referem | int |
| percentil | Percentil de faturamento (25%, 50%, 60%, 75% ou 90%) | string |
| faturamento | Valor de faturamento daquele cenário, naquele percentil, naquele mês | double |

**Frequência:** 1x por mês

### semaforo_monthly_revenue

**Descrição:** É a tabela que, para cada cenário, possui a informação de quais predições do modelo "monthly_revenue_models" são confiáveis ou não (farol verde, amarelo ou vermelho).

Por cenário aqui entende-se: Estado, Cidade, Bairro, Listing type (apto, casa, hotel ou outros) e número de quartos.

* **Colunas:**

| **Nome da coluna** | **descrição** | **tipo de dado** |
|----|----|----|
| state | Estado (UF) | string |
| city | Cidade | string |
| suburb | Bairro | string |
| listing_type | Tipo de listings (apto, casa, hotel ou outros) | string |
| bedrooms | Número de quartos | bigint |
| max_pipe_annual_gross_revenue | Faturamento máximo que o Pipe identificou que um listing realizou neste cenário | double |
| avg_n_months | Média de quantos meses foram utilizados na hora de calcular os dados do cenário | double |
| annual_revenue_90_percentile | Faturamento no percentil 90% que o Pipe identificou que foi realizado naquele cenário | double |
| semaforo | Resultado do semáforo (verde, amarelo ou vermelho) | string |
| mini_farol_vermelho | Indica se o percentil 90% é confiável ou não | boolean |

**Frequência:** 1x por semana

## Camada SEAZONE REAL DATA

Nós usamos essa camada como a nossa "tabela verdade" para calibrar nossos modelos e verificar o erro deles. Os dados são adquiridos da Stays, ou seja, são os dados das reservas verdadeiras feitas nos imóveis da Seazone!

### cleaning_blocks

**Descrição:** Tabela com a configuração de quantos dias de bloqueios de limpeza cada listing da Seazone possui.

Possibilidades:

* não tem bloqueio de limpeza → 2
* bloqueio de checkin OU checkout → 1
* bloqueio de checkin E checkout → 2
* **Colunas:**

| **Nome da coluna** | **descrição** | **tipo de dado** |
|----|----|----|
| _stays_id | ID 1 que a Stays usa para o listing | string |
| stays_id | ID 2 que a Stays usa para o listing | string |
| listing | ID do listing dentro da Seazone | string |
| airbnb_listing_id | ID do listing no Airbnb na data de aquisição | string |
| block_days | Quantos dias o imóvel fica bloqueado para fazer limpeza (pode ser 0, 1 ou 2) | bigint |

**Frequência:** 1x por dia

### listings_stays_id

**Descrição:** Tabela com a relação entre o ID de um listing na Stays, no Airbnb e o ID interno do listing na Seazone (ao longo do tempo, então os dados vão sendo acumulados e é necessário pegar a última aquisição para pegar os mais recentes).

Obs.: A Stays usa sempre dois IDs para cadastrar um imóvel.

* **Colunas:**

| **Nome da coluna** | **descrição** | **tipo de dado** |
|----|----|----|
| _stays_id | ID 1 que a Stays usa para o listing | string |
| stays_id | ID 2 que a Stays usa para o listing | string |
| listing | ID do listing dentro da Seazone | string |
| aquisition_date | Data da aquisição dos dados | timestamp |
| airbnb_listing_id | ID do listing no Airbnb na data de aquisição | string |

**Frequência:** 1x por dia

### reservations

**Descrição:** Dados limpos com as reservas reais e bloqueios dos listings da Seazone, com dados adquiridos pela Stays.

Caso seja um bloqueio de limpeza, também é informado nesta tabela com a flag "blocked" = true.

* **Colunas:**

| **Nome da coluna** | **descrição** | **tipo de dado** |
|----|----|----|
| listing | ID do listing dentro da Seazone | string |
| airbnb_listind_id | ID do listing no Airbnb | string |
| creation_date | Data de criação da reserva | timestamp |
| checkin_date | Checkin da reserva | timestamp |
| checkout_date | Checkout da reserva | timestamp |
| n_nights | Número de noites da reserva | bigint |
| blocked | Indica se trata-se de um bloqueio ou de uma reserva | boolean |
| price | Valor bruto da reserva | double |
| net_price | Valor líquido da reserva (retirando taxas da OTA, taxa de limpeza e outras taxas mais incomuns como taxa de hóspede, taxa de Pet etc) | double |
| ota | Indica qual a OTA que criou a reserva | string |
| ota_fee | Taxa da OTA em valor absoluto | double |
| ota_percentage | Taxa da OTA em valor percentual relativo ao valor bruto da reserva | double |
| other_fees | Outras taxas que podem ter incidido sobre a reserva | double |
| daily_price | Valor médio das diárias da reserva (é o 'price' menos 'other_fees' dividido pelo 'n_nights') | double |
| is_last_minute | Indica se é uma reserva de last minute ou não | boolean |
| id | ID do listing dentro da Seazone | string |
| is_cleaning_block | Indica se o bloqueio é um bloqueio de limpeza ou não (caso não seja um bloqueio, será Falso) | boolean |

**Frequência:** 1x por dia

### seazone_daily_revenue

**Descrição:** Tabela com os faturamentos reais diários por listing da Seazone. Usa a reservations + sirius_historical_prices + old_stays_price.

* **Colunas:**

| **Nome da coluna** | **descrição** | **tipo de dado** |
|----|----|----|
| listing | ID do listing dentro da Seazone | string |
| airbnb_listind_id | ID do listing no Airbnb | string |
| creation_date | Data de criação da reserva | timestamp |
| checkin_date | Checkin da reserva | timestamp |
| block_days | Quantos dias o imóvel fica bloqueado para fazer limpeza (pode ser 0, 1 ou 2) | bigint |

**Frequência:** 1x por dia