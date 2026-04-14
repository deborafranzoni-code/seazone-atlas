<!-- title: Sorveteria de Dados | url: https://outline.seazone.com.br/doc/sorveteria-de-dados-c3X10te1OM | area: Tecnologia -->

# Sorveteria de Dados

<aside> 💡 **[Formulário para solicitação de Dados](https://forms.gle/A2zm2382r4Vy79vE7)**

</aside>

# Documentação Usuário

* Com a ideia de tornar mais fácil e prático o acesso aos dados que a Seazone possui, foi aberta a **sorveteria de dados!**

  Nesta sorveteria não servimos sorvete, mas sim dados. Cada sabor representa uma consulta que comumente é realizada, e é entregue normalmente como um arquivo .csv via slack ou planilha do google. Estes sabores estão sempre "frescos" e esperando para serem pedidos, sendo entregues rapidamente.

  No nosso menu, serão apresentados os sabores tradicionais, e o método que o mesmo é entregue. Alguns são enviados pelo Slack toda semana ou mês, em outros sabores basta entrar em uma planilha do google, colocar os seus filtros e você já recebe os dados na hora. Mas, para os mais exigentes, e que preferem um sabor exclusivo, ainda é possível solicitar! Nesse caso, pedimos que utilizem os sabores como base, facilitando para a compreensão e construção do sabor novo.

  Vale ressaltar que qualquer sabor novo é mais demorado, pois precisa passar por processos de construção e validação.

# Menu de Sorvetes

 ![sorvete.gif](../../Dados(%20Desatualizada,%20sera%CC%81%20descontinuada%20)%20d711b57f0c9b4a2b80282f6633895f91/Pipe%2024cc54f61f5f460c9515bbdd7b7fd43d/Sorveteria%20de%20Dados%206e46e3df5d694904bb2d94464e9b5bbf/sorvete.gif)

### Acessos:

* **SLACK: Para solicitar acesso nos canais do slack dos sabores de sorvetes falar com @Lucas Abel da Silveira**
* **Planilha Google: Contas da Seazone no google possuem acesso as planilhas, somente entrar no link e aproveitar(lembre de verificar se não existe alguém usando no mesmo momento).**
* **"*Sou bom com SQL e quero queriar os dados diretamente do Lake*" → então basta acessar o [Athena na AWS](/doc/como-acessar-e-usar-o-athena-na-aws-KjAYcvMETi)**

## Dados Airbnb

### Diagnóstico de Faturamento

[Treinamento do uso da tabela( Atualizar )](https://www.loom.com/share/e180e9e51460440ebf305e2bc034aa8e)

[Drive Template](https://drive.google.com/drive/folders/1mGX9SBubT20HnwwYTPwAawaqv4qfjvJn)

<https://drive.google.com/drive/u/0/folders/1FWCTSswYTbOAEpyP5Okepxz3vgLEurio>

## Faturamento por cidade/bairro strata histórico (Slack)

Este sabor é enviado mensalmente no canal do slack ***faturamento-cidade-strata***, nele é possível encontrar dados históricos agrupados por cidade e bairro, sobre o valor de faturamento pelo Airbnb. Dentro da mesma cidade/bairro, ainda temos o faturamento diferenciado por casas, apartamentos e os números de quartos. Conseguindo visualizar a diferença de faturamento em uma determinada cidade para diferentes tipos de imóveis.

Para um mesmo tipo de imóvel e cidade/bairro é possível visualizar que temos a coluna percentil, que classifica em 5 valores de faturamento sendo o mais baixo em 25% e o mais alto em 90%, para assim entender melhor a distribuição dos valores de faturamento em cada categoria.

| state | city | suburb | type | bedrooms | year | month | percentil | faturamento | n_listings |    |
|----|----|----|----|----|----|----|----|----|----|----|
| Ceará | Juazeiro do Norte | Cidade Universitária | casa | 1 | 2020 | 2 | 25% | 606.6112094827586 | 10 |    |
| Ceará | Juazeiro do Norte | Cidade Universitária | casa | 1 | 2020 | 2 | 50% | 736.2224189655171 | 10 |    |
| Ceará | Juazeiro do Norte | Cidade Universitária | casa | 1 | 2020 | 2 | 60% | 788.0669027586207 | 10 |    |
| Ceará | Juazeiro do Norte | Cidade Universitária | casa | 1 | 2020 | 2 | 75% | 865.8336284482758 | 10 |    |
| Ceará | Juazeiro do Norte | Cidade Universitária | casa | 1 | 2020 | 2 | 90% | 943.6003541379309 | 10 |    |
| Ceará | Juazeiro do Norte | Cidade Universitária | casa | 1 | 2020 | 3 | 25% | 403.0147096774194 | 11 |    |

* **Dicionário de Dados**
  * **State**

    Coluna que representa o estado que está localizado a cidade, bairro… Esta coluna é do tipo String.
  * **City**

    Coluna que representa a cidade que está localizado o bairro, casa ou aparatamento… Esta coluna é do tipo String.
  * **Suburb**

    Coluna que representa o Bairro dos dados. Esta coluna é do tipo String.
  * **Type**

    Coluna que representa o tipo de imóvel, podendo ser até 4 opções: apartamento, casa, hotel e outros. Esta coluna é do tipo String.
  * **Bedrooms**

    Bedrooms, que significa quartos em inglês, é o número de quartos que o imóvel possui. Esta coluna é do tipo Int, isto é um número inteiro.
  * **Year**

    Coluna que representa o ano dos dados. É do tipo Int, isto é um número inteiro.
  * **Month**

    Coluna que representa o mês. É do tipo Int, isto é um número inteiro.
  * **Percentil**

    Representa o valor do percentil do faturamento em %, possuindo 5 valores: 25%, 50%, 60%, 75% e 90%. O valor de 50% representa a mediana do faturamento. Esta coluna é String.
  * **Faturamento**

    Coluna que representa o valor do faturamento, em reais, que um imóvel com as dadas características possui no percentil informado pela coluna "percentil". Esta coluna é do tipo float, isto é um número com virgula.
  * **N_listings**

    Representa o número de imóveis utilizados para o cálculo do faturamento, quanto maior esse número, melhor ficará os valores do faturamento por percentil. Isto é, quanto maior o valor desta coluna, melhor a qualidade do dado. Coluna do tipo Int.
* **Lista de possíveis filtros**
  * Número de quartos.
  * Nota.
  * Número de meses com faturamento maior que zero.
  * Região, Estado, Cidade, Bairro.
  * Número de anfitriões mínimos ou máximo.
  * Número de reviews.
  * Superhost.
  * Além de casa e apartamentos, também pode ser adicionado hotéis e outros.

**Casos de uso:** Identificar cidades com maiores faturamento para possíveis expansão.

**Nome query Athena:** Faturamento por cidade/bairro com strata.

**Link Athena(Saved queries):**


## Listings info (Slack)

Este sabor é enviado toda primeira segunda-feira do mês, no canal do slack ***monthly-listings-info***, nele é possível encontrar o faturamento mensal de um determinado listing do Airbnb, o historico de faturamento, sua nota e número de reviews. Vale ressaltar que só mandamos listings nesse sabor que ainda estão vivos.

Temos também o strata que classificamos por tipo de imóvel, podendo ter bastante utilidade para classicar concorrentes e fazer analises por cidade por tipo de imóvel com maior precisão do que por exemplo o sabor de sorvete "faturamento por cidade/bairro strata histórico".

| airbnb_listing_id | year | month | state | city | suburb | type | bedrooms | strata | revenue | number_of_reviews | star_rating | is_superhost | can_instant_book |
|----|----|----|----|----|----|----|----|----|----|----|----|----|----|
| 10002896 | 2016 | 11 | Santa Catarina | Florianópolis | Santinho | apartamento | 1 | MASTER | 866.723780456543 | 2 | 0.0 | false | false |
| 10002896 | 2017 | 1 | Santa Catarina | Florianópolis | Santinho | apartamento | 1 | MASTER | 4856.3018 | 2 | 0.0 | false | false |
| 10002896 | 2017 | 2 | Santa Catarina | Florianópolis | Santinho | apartamento | 1 | MASTER | 3840.7853744890476 | 2 | 0.0 | false | false |
| 10002896 | 2017 | 3 | Santa Catarina | Florianópolis | Santinho | apartamento | 1 | MASTER | 3498.3880610579963 | 2 | 0.0 | false | false |
| 10002896 | 2017 | 4 | Santa Catarina | Florianópolis | Santinho | apartamento | 1 | MASTER | 184.71804160325365 | 2 | 0.0 | false | false |
| 10002896 | 2017 | 5 | Santa Catarina | Florianópolis | Santinho | apartamento | 1 | MASTER | 1224.9880262214908 | 2 | 0.0 | false | false |
| 10002896 | 2017 | 6 | Santa Catarina | Florianópolis | Santinho | apartamento | 1 | MASTER | 6287.50149 | 2 | 0.0 | false | false |
| 10002896 | 2017 | 7 | Santa Catarina | Florianópolis | Santinho | apartamento | 1 | MASTER | 735.0439793208953 | 2 | 0.0 | false | false |

* **Dicionário de Dados**
  * **Airbnb_listing_id**

    Id que representa cada imóvel no Airbnb. Tipo string.
  * **Year**

    Coluna que representa o ano dos dados. É do tipo Int, isto é um número inteiro.
  * **Month**

    Coluna que representa o mês. É do tipo Int, isto é um número inteiro.
  * **State**

    Coluna que representa o estado que está localizado a cidade, bairro… Esta coluna é do tipo String.
  * **City**

    Coluna que representa a cidade que está localizado o bairro, casa ou aparatamento… Esta coluna é do tipo String.
  * **Suburb**

    Coluna que representa o Bairro dos dados. Esta coluna é do tipo String.
  * **Type**

    Coluna que representa o tipo de imóvel, podendo ser até 4 opções: apartamento, casa, hotel e outros. Esta coluna é do tipo String.
  * **Bedrooms**

    Bedrooms, que significa quartos em inglês, é o número de quartos que o imóvel possui. Esta coluna é do tipo Int, isto é um número inteiro.
  * **Strata**

    Parecido com o percentil da ultima coluna, o Strada classifica os imóveis por faturamento, as 5 categorias existentes são: SUP, JR, SIM, MASTER, TOP. Tipo String.
  * **Revenue**

    Coluna que representa o valor do faturamento em reais. Ela varia baseada no percentil. Esta coluna é do tipo float, isto é um número com virgula.
  * **Number_of_reviews**

    Número de reviews que aquele imóvel já recebeu no Airbnb. Coluna do tipo Int.
  * **Star_rating**

    Nota que o imóvel possui no Airbnb. Tipo float.
  * **Is_superhost**

    Coluna que representa se o dono do imóvel no Airbnb é Superhost, pode ter dois valores, True representado que é superhost e False que não é superhost. Tipo boolean.
  * **Can_instant_book**

    Da mesma foram da coluna anterior, é do tipo booleano. Representando se o imóvel pode ser reservado diretamente, sem aprovação do dono.
* **Lista de possíveis filtros**
  * Strada(SUP, JR,…).
  * Tipe(Casa, apartamento…).
  * Número de meses com faturamento maior que zero.
  * Número de reviews.
  * Estado/Cidade/Bairro.
  * Número de quartos.
  * Nota.
  * Visualizar somente para um anunciante, exemplo Seazone.
  * Visualizar somente para um listings.

**Casos de uso:** Verificar variação de faturamento ao longo dos meses e comparações entre alguns listings.

**Nome query Athena:** listings_info.

**Link Athena(Saved queries):**


## Faturamento por listing (Planilha do Google)

Diferente do sabor anterior este sabor não e enviado pelo slack, mas sim possui uma planilha no google para ser utilizado. O usuário fornece o id do listing do Airbnb que deseja consultar, e é retornado o histórico de faturamento do mesmo, dias ocupados, dias bloqueados e dias disponíveis.

O exemplo abaixo é retornado na primeira página, temos os dados do pipeline da Seazone e os dados do Airdna(dados comprados) para uma maior comparação. Existem ainda duas outras abas, podendo assim só utilizar os dados do pipeline da Seazone ou somente o do Airdna.

| airbnb listing_id | month | year | month fat pipe | month fat airdna | avg price pipe | avg price airdna | days in month pipe | days in month airdna | occupied dates pipe | occupied dates airdna | available dates airdna | available dates pipe | blocked dates pipe | blocked dates airdna |
|----|----|----|----|----|----|----|----|----|----|----|----|----|----|----|
| 16857745 | 7 | 2017 |    | 3.471 |    | 496 | 0 | 31 |    | 7 | 24 |    |    | 0 |
| 16857745 | 8 | 2017 |    | 0 |    |    | 0 | 31 |    | 0 | 31 |    |    | 0 |
| 16857745 | 9 | 2017 |    | 0 |    |    | 0 | 30 |    | 0 | 30 |    |    | 0 |
| 16857745 | 10 | 2017 |    | 0 |    |    | 0 | 31 |    | 0 | 31 |    |    | 0 |
| 16857745 | 11 | 2017 |    | 0 |    |    | 0 | 30 |    | 0 | 30 |    |    | 0 |
| 16857745 | 12 | 2017 |    | 6.725 |    | 1.345 | 0 | 31 |    | 5 | 26 |    |    | 0 |
| 16857745 | 1 | 2018 |    | 9.171 |    | 1.310 | 0 | 31 |    | 7 | 24 |    |    | 0 |
| 16857745 | 2 | 2018 |    | 0 |    |    | 0 | 28 |    | 0 | 28 |    |    | 0 |
| 16857745 | 3 | 2018 |    | 2.279 |    | 760 | 0 | 31 |    | 3 | 28 |    |    | 0 |

**Casos de uso:** Identificar faturamento histórico do listing.

**Link da planilha:**


**Dicas de uso:** Para utilizar basta acessar o link inserir um id de imóvel do airbnb e clickar no menu Rodar_Query e clickar em rodar.

## Listing Details Seazone (Slack)

Este sabor é enviado toda terça-feira no slack no canal ***listing_details***, nele temos as informações de todos os listings que estão ativos no Airbnb da Seazone. Possibilitando verificar se as informações estão corretas.

| airbnb_listing_id | url | ad_name | ad_description | space | house_rules | amenities | safety_features | number_of_bathrooms | number_of_bedrooms | number_of_beds | latitude | longitude | star_rating | additional_house_rules | owner | check_in | check_out | number_of_guests | is_superhost | number_of_reviews | cohosts | cleaning_fee | can_instant_book | owner_id | aquisition_date | is_dead | listing_type | picture_count | min_nights | response_rate_shown | response_time_shown | guest_satisfaction_overall | ano | mes | dia | airbnb_listing_id.1 | id_seazone |    |
|----|----|----|----|----|----|----|----|----|----|----|----|----|----|----|----|----|----|----|----|----|----|----|----|----|----|----|----|----|----|----|----|----|----|----|----|----|----|----|
| 41784758 | <https://www.airbnb.com.br/rooms/41784758> | Apto centralizado c/ mobília nova em Jurerê CPS107 | Apartamento espaçoso e aconchegante e com ótima localização na avenida principal de Jurerê. Sua mobilia é planejada e é ideal para casais, famílias ou amigos, tanto para passar as férias, final de semana, ou até mesmo trabalhar.Possui cozinha completa, camas confortáveis e ar condicionado em um dos quartos, além de possuir sacada com churrasqueira.IMPORTANTE: Para check-in após as 20h há cobrança adicional de conveniência! | Para o conforto de nossos hóspedes, o apartamento possui:- Suíte com cama de casal;- Quarto com cama de casal;- Banheiro social;- Ar-condicionado na suite e na sala;- Tv a cabo na sala de estar;- Wifi disponível;- Cozinha completa com microondas, geladeira, fogão, panelas e chaleira elétrica;- Produtos de higiene e cuidado pessoal (sabonete, shampoo e papel higiênico);- Roupas de cama e banho de qualidade hoteleira (roupas de cama extra são cobrados pela Seazone);- Sacada com Churrasqueira;- Garagem Coberta.Venha, relaxe, divirta-se e não se preocupe com mais nada :) | \["Proibido fumar", "Não permite animais de estimação", "Não são permitidas festas ou eventos"\] | \["Xampu", "Estacionamento incluído", "Wi-Fi", "Cozinha", "Ar-condicionado", "TV", "Básico", "Água quente", "Roupa de cama", "Alarme de monóxido de carbono", "Detector de fumaça", "Louças e talheres", "Microondas", "Refrigerador", "Fogão"\] | \["Alarme de monóxido de carbono", "Detector de fumaça"\] | 2.0 | 2 | 2 | -2.744.099.998.474.120 | -484.900.016.784.668 | 4.43 | NÃO É PERMITIDO (Sujeito a multa): -> Festas -> Volume alto -> Visitas fora da capacidade de hóspedes da acomodação. | Seazone | 15:00 - 20:00 | 11:00 | 4 | FALSO | 42 | Seazone,Gustavo | 285.0 | VERDADEIRO | 227777128 | 2023-03-20 15:06:17.128 | FALSO | apartamento | 0 | 0 | <NA> | <NA> | 0 | 2023 | 3 | 20 | 41784758 | CPS107 |    |

* **Dicionário de Dados**

  Colunas com **pipe** no nome representam dados da Seazone, colunas com **Airdna** no nome representam dados provenientes do Airdna(site de dados sobre Airbnb).
  * **Airbnb_listing_id**

    Id que representa cada imóvel no Airbnb. Tipo string.
  * **URL**

    Link para acessar o anúncio no Airbnb. Tipo string.
  * **Ad_name**

    Nome que aparece no anúncio no site do Airbnb. Tipo String.
  * **Ad_description**

    Descrição do anúncio no site do Airbnb. Tipo string.
  * **Space**

    Descrição do espaço que o imóvel possui. Tipo string.
  * **House_rules**

    Regras para utilização do imóvel, exemplo: proibido fumar ou proibido festas. Tipo String.
  * **Amenities**

    O que o imóvel possui, exemplo: TV ou ar-condicionado. Tipo String.
  * **Safety_features**

    Parecido com amenities, mas para critérios de segurança. Exemplos: Alarme de incêndio. Tipo String.
  * **Number_of_bathrooms**

    Número de banheiros que o imóvel possui. Tipo double.
  * **Number_of_bedrooms**

    Número de quartos que o imóvel possui. Tipo int.
  * **Number_of_beds**

    Número de camas que o imóvel possui. Tipo int.
  * **Latitude**

    Representa a latitude que o imóvel se encontra. Tipo double.
  * **Longitude**

    Representa a longitude que o imóvel se encontra. Tipo double.
  * **Star_rating**

    Nota que o imóvel recebe pelo os inquilinos. Tipo Double.
  * **Additional_house_rules**

    Mais algumas regras e explicações sobre o que pode e não pode no imóvel. Tipo string.
  * **Owner**

    Nome do dono do imóvel no site do Aribnb. Tipo String.
  * **Check_in**

    Horários que o inquilino pode entrar no imóvel para aproveitar sua estadia. Tipo String.
  * **Check_out**

    Horários limites para o inquilino sair no imóvel. Tipo String.
  * **Number_of_guests**

    Número máximo de pessoas por imóvel. Tipo int.
  * **Is_superhost**

    Coluna que representa se o dono do imóvel no Airbnb é Superhost, pode ter dois valores, True representado que é superhost e False que não é superhost. Tipo boolean.
  * **Number_of_reviews**

    Número de reviews que aquele imóvel já recebeu no Airbnb. Coluna do tipo Int.
  * **Cohosts**

    Além da conta principal do imóvel, outras contas responsáveis pelo mesmo. Tipo String.
  * **Cleaning_fee**

    Taxa de limpeza. Tipo Double.
  * **Can_instant_book**

    Da mesma foram da coluna Is_superhost, é do tipo booleano. Representando se o imóvel pode ser reservado diretamente, sem aprovação do dono.
  * **Owner_id**

    Como o imóvel tem um id para representar ele no site do Airbnb, o dono também possui um id de sua conta. Tipo String.
  * **Aquisition_date**

    Data de aquisição do dado, isto qual dia o código rodou para obter está informação. Tipo Data.
  * **Is_dead**

    Coluna para dizer se o imóvel está ativo ou desativado. Quando verdadeiro está morto, falso vivo. Tipo Booleano.
  * **Listing_type**

    Coluna que representa o tipo de imóvel, podendo ser até 4 opções: apartamento, casa, hotel e outros. Esta coluna é do tipo String.
  * **Picture_count**

    Número de fotos no anúncio. Esse dado não é muito confiável e nem sempre retorna o valor correto. Tipo int.
  * **Min_nights**

    Número de noites mínimas que o inquilino precisa alugar o imóvel. Tipo int.
  * **Response_rate_shown**

    Tempo de resposta do dono da conta. Tipo String.
  * **Response_time_shown**

    Tempo de resposta do dono da conta para aceitar inquilino. Tipo String.
  * **Guest_satisfaction_overall**

    Satisfação do inquilo com a estadia e contato com o dono. Tipo int.
  * **Ano**

    Coluna que representa o ano dos dados. É do tipo string.
  * **Mes**

    Coluna que representa o mês.  É do tipo string.
  * **Dia**

    Coluna que representa o dia numeral do mês.  É do tipo string.
  * **Id_seazone**

    Id interno do imóvel da seazone. Tipo String.
* **Lista de possíveis filtros**
  * Número de quartos.
  * Tipo casa ou apartamento.
  * Nota no Airbnb.
  * Número de reviews.
* **Informações importantes**

  O scraper que alimente essa tabela funciona toda segunda-feira nas primeiras horas do dia, assim se algum imóvel for registrado entre segunda-feira e terça-feira, ele não aparecerá no .csv no slack na terça-feira.

**Casos de uso:** Verificar se as informações estão corretas dos anúncios.

**Nome query Athena:** Seazone details.

**Link Athena(Saved queries):**


## Comentários Seazone (Planilha do Google)

Este sabor é fornecido em um planilha do google. Você pode consultar por um intervalo de data, um id especifico da Seazone ou deixar em branco e irá retornar todos os comentários que a Seazone já recebeu no Airbnb.

| comment_id | id_airbnb | id_seazone | comment | rating | language | date | reviewer_id | reviewer_name |
|----|----|----|----|----|----|----|----|----|
| 861635891438820481 | 37054433 | ILC1206 | Tivemos uma excelente estadia. o único ponto a melhorar é que o quarto foi somente limpo no final do dia. | 5 | pt | 2023-04-03T19:56:42.000 | 12323444 | Bill |
| 861625226054756893 | 791271236223458391 | VEC209 | Ótimo | 5 | en | 2023-04-03T19:35:31.000 | 12323444 | Bill |
| 861611104384687497 | 783331361381409232 | RMV002 | Casa muito boa, exatamente como nas fotos. Porém tivemos alguns divergências no anúncio. Lá dizia que a casa é térrea e não possui escadas, porém somente um quarto fica no térreo, os outros três no piso superior. Dizia também que três suítes possuíam ar condicionado, porém somente duas estão com aparelho. E por fim tivemos problemas para entrar no condomínio no período da noite, pois nos foi entregue apenas um controle e atendentes da noite nunca encontravam nosso cadastro, demorou uns três dias para que isso fosse normalizado. | 4 | pt | 2023-04-03T19:07:27.000 | 12323444 | Bill |
| 861609588021901336 | 624408395159293356 | EIA205 | Alguns itens estavam faltando,  como uma segunda toalha de rosto, pano de prato tb estavam muito velhos. O apto é  maravilhoso, acho que a pessoa que faz a faxina que deve ser revista. | 5 | pt | 2023-04-03T19:04:26.000 | 12323444 | Bill |

* **Dicionário de Dados**
  * **Comment_id**

    Coluna que representa o id do comentário no site do Airbnb. Esta coluna é do tipo String.
  * **Id_airbnb**

    Coluna que representa o id do imóvel no site do Airbnb. Esta coluna é do tipo String.
  * **Id_seazone**

    Coluna que representa o id do imóvel no sistema da Seazone. Esta coluna é do tipo String.
  * **Comment**

    Comentário realizado no site do Airbnb para o imóvel. Tipo String.
  * **Rating**

    Nota dada pelo usuário ao imóvel. Tipo Int.
  * **Language**

    Idioma utilizado pelo usuário ao escrever o comentário. Tipo String.
  * **Date**

    Data e hora que o comentário foi realizado. Coluna do tipo timestamp.
  * **Reviewer_id**

    Id de quem fez o comentário.
  * **Reviewer_name**

    Nome de quem fez o comentário.

**Casos de Usos:**  Atualização da planilha e avaliação dos franqueados..

**Link da planilha:**


**Nome query Athena:** Comentários Seazone.

**Link Athena(Saved queries):**


## Último preço e disponibilidade imóveis Airbnb (Planilha do Google)

Este sabor é fornecido em uma planilha do google. Você pode consultar por um intervalo de data e deve fornecer uma lista separada por vírgulas de IDs Airbnb. Ela retorna a última aquisição de preços e disponibilidade dos imóveis requeridos.

**Obs.: um imóvel não disponível não implica que foi realmente alugado!!! Pode ser que o proprietário do listing resolveu bloquear em um certo período para uso próprio (recração, reforma, fotos etc).**

**Link da planilha para a requisição dos dados:** <https://docs.google.com/spreadsheets/d/1aprDFbnwJ0I86TOyZ3zLQsrJotI88hS8mksqP4BfEYE/edit#gid=0>

* **Exemplo de retorno para uma requisição (apenas parte do retorno):**

| **airbnb_listing_id** | **id_seazone** | **date** | **available** | **price** | **min_stay** |
|----|----|----|----|----|----|
| 734952595951319778 |    | 30/06/2023 | VERDADEIRO | 235 | 2 |
| 734952595951319778 |    | 01/07/2023 | VERDADEIRO | 222 | 2 |
| 734952595951319778 |    | 02/07/2023 | VERDADEIRO | 211 | 2 |
| 734952595951319778 |    | 03/07/2023 | VERDADEIRO | 210 | 2 |
| 734952595951319778 |    | 04/07/2023 | VERDADEIRO | 210 | 2 |
| 734952595951319778 |    | 05/07/2023 | VERDADEIRO | 210 | 2 |
| 734952595951319778 |    | 06/07/2023 | VERDADEIRO | 210 | 2 |
| 734952595951319778 |    | 07/07/2023 | VERDADEIRO | 220 | 2 |
| 734952595951319778 |    | 08/07/2023 | VERDADEIRO | 222 | 2 |
| 734952595951319778 |    | 09/07/2023 | VERDADEIRO | 211 | 2 |
| 734952595951319778 |    | 10/07/2023 | VERDADEIRO | 210 | 2 |
| 734952595951319778 |    | 11/07/2023 | VERDADEIRO | 210 | 2 |
* **Dicionário de dados:**

  **airbnb_listing_id:** id do listing no Airbnb. Tipo: string

  **id_seazone:** id do listing na Seazone (retorna em branco caso não seja um listing da Seazone). Tipo: string.

  **date:** data a que se refere o preço e a disponibilidade. Tipo: data.

  **available:** indica se o imóvel estava ou não disponível no dia. Tipo: booleano (verdadeiro ou falso)

  **price:** preço do imóvel no dia. Tipo: inteiro.

  **min_stay:** mínimo número de noites para fazer uma reserva do imóvel começando naquele dia. Tipo: inteiro.

## Anfitriões Airbnb - Concorrentes Seazone (Slack)

O sabor deste sorvete é 'Flocos'. São três tabelas: nossa tabela de 'Baunilha', contendo informações sobre os anfitriões do Airbnb com uma classificação superior a 4 de nota. Ela apresenta o nome e o link do anfitrião, o número total de propriedades, número de reviews, nota que possuem e em quais estados eles operam.

Temos a versão da 'Baunilha sem flocos', isto é, não temos os dados sobre os estados. Somente temos os dados principais dos hosts, facilitando visualizar os principais hosts do Brasil.

Já os nossos 'Flocos de Dados'. Temos o estado, o número de listagens e o número de anfitriões. A divisão é feita em intervalos de dez, ou seja, por exemplo o intervalo de 1 a 10 no estado 'X', mostramos o número de anfitriões.

Os dados são enviados mensalmente na primeira quarta-feira do mês no começo da tarde. O canal no slack é **concorrentes-seazone**.

Você pode visualizar as tabelas abaixo, sendo a primeira nosso 'floquinhos', a segunda nossa 'baunilha' e a terceira 'baunilha sem flocos.

| Estado | Número de Listings | Número de Hosts |    |
|----|----|----|----|
| Acre | 1 - 10 | 96 |    |
| Alagoas | 1 - 10 | 4715 |    |
| Alagoas | 11 - 20 | 16 |    |
| Alagoas | 21-30 | 3 |    |

* **Dicionário de Dados:**
  * **Estado**

    Coluna que representa o estado do dado. Tipo String.
  * **Número de Listings**

    Possui o intervalo de listings, isto é, número de imóveis que um host possui no Aribnb.
  * **Número de Hosts**

    Número de Hosts que possuem aquela quantidade de imóveis naquele estado.
* **Informações importantes:**

  Na coluna número listings, o intervalo é sempre de 10 listings. Caso não existe nenhum host ele não mostra, sendo assim pode pular de um intervalo para outro. Por exemplo mostrar de 1 - 10 e depois de 81 -90.

| Host | Link | Número de Listings Total | Número de Reviews | Nota do Host | Número de Listings no Estado | Estado | Estado Principal |
|----|----|----|----|----|----|----|----|
| Francisca | https://www.airbnb.com.br/users/show/105336211 | 6 | 10 | 4.5 | 6 | Acre | Acre |
| Maria Do Carmo | https://www.airbnb.com.br/users/show/241708680 | 6 | 11 | 4 | 1 | Acre | Bahia |
| Luan | https://www.airbnb.com.br/users/show/132219071 | 4 | 12 | 5 | 4 | Acre | Acre |
| Simone De Oliveira Silva | https://www.airbnb.com.br/users/show/190176475 | 4 | 13 | 5 | 4 | Acre | Acre |
| Fábio | https://www.airbnb.com.br/users/show/190891282 | 4 | 15 | 4.76 | 4 | Acre | Acre |
| Valéria Aquino | https://www.airbnb.com.br/users/show/348195160 | 4 | 16 | 3.66 | 3 | Acre | Acre |
| Samuel | https://www.airbnb.com.br/users/show/76670899 | 4 | 111 | 3.5 | 4 | Acre | Acre |
| Anfitrião Prime | https://www.airbnb.com.br/users/show/319227148 | 552 | 222 | 4 | 16 | Alagoas | São Paulo |

* **Dicionário de Dados:**
  * **Host**

    Nome do Host na conta do Airbnb. Tipo String.
  * **Link**

    Link para acessar a conta do host no Airbnb.
  * **Número de Listings Total**

    Número total de listings que host possui.
  * **Número de Reviews**

    Número total de reviews que host possui.
  * **Nota do Host**

    Nota que o host possui.
  * **Número de Listings no Estado**

    Número total de listings que host possui no estado da coluna estado.
  * **Estado**

    Coluna que representa o estado do dado. Tipo String.
  * **Estado Principal**

    Estado principal de atuação do host. Ou seja, é o estado que ele possui mais imóveis no Airbnb.

| Host | Link | Número de Listings Total | Número de Reviews | Nota do Host |
|----|----|----|----|----|
| Francisca | https://www.airbnb.com.br/users/show/105336211 | 6 | 10 | 4.5 |
| Maria Do Carmo | https://www.airbnb.com.br/users/show/241708680 | 6 | 11 | 4 |
| Luan | https://www.airbnb.com.br/users/show/132219071 | 4 | 12 | 5 |
| Simone De Oliveira Silva | https://www.airbnb.com.br/users/show/190176475 | 4 | 13 | 5 |
| Fábio | https://www.airbnb.com.br/users/show/190891282 | 4 | 15 | 4.76 |
| Valéria Aquino | https://www.airbnb.com.br/users/show/348195160 | 4 | 16 | 3.66 |
| Samuel | https://www.airbnb.com.br/users/show/76670899 | 4 | 111 | 3.5 |
| Anfitrião Prime | https://www.airbnb.com.br/users/show/319227148 | 552 | 222 | 4 |

* **Dicionário de Dados:**
  * **Host**

    Nome do Host na conta do Airbnb. Tipo String.
  * **Link**

    Link para acessar a conta do host no Airbnb.
  * **Número de Listings Total**

    Número total de listings que host possui.
  * **Número de Reviews**

    Número total de reviews que host possui.
  * **Nota do Host**

    Nota que o host possui.

## Predição de faturamento por cidade (Planilha do Google)

Este sabor foi criado para auxiliar nas predições dos faturamentos dos imóveis. Separada por estado, cidade, tipo  e número de quartos. Possibilita o usuário ter uma primeira noção. São apresentados dois faturamentos, um considerado alto e outro considerado baixo.

| Estado | Cidade | Tipo | N° Quartos | Limite Baixo - Faturamento | Limite Alto - Faturamento |
|----|----|----|----|----|----|
| Acre | Feijó | casa | 3 | R$ 27.656,96 | R$ 27.678,48 |
| Acre | Rio Branco | apartamento | 1 | R$ 8.970,41 | R$ 18.474,50 |
| Acre | Rio Branco | apartamento | 2 | R$ 16.589,17 | R$ 28.216,87 |
| Acre | Rio Branco | casa | 1 | R$ 9.500,40 | R$ 18.627,50 |
| Acre | Rio Branco | casa | 2 | R$ 17.627,85 | R$ 28.663,64 |
| Acre | Rio Branco | casa | 3 | R$ 19.455,15 | R$ 28.874,26 |
| Alagoas | Anadia | casa | 3 | R$ 4.791,59 | R$ 5.667,38 |
| Alagoas | Arapiraca | apartamento | 1 | R$ 9.357,48 | R$ 11.847,56 |
| Alagoas | Arapiraca | apartamento | 2 | R$ 14.886,79 | R$ 22.634,22 |
| Alagoas | Arapiraca | casa | 2 | R$ 11.989,03 | R$ 16.585,79 |
| Alagoas | Arapiraca | casa | 3 | R$ 11.935,18 | R$ 21.257,23 |

* **Dicionário de Dados:**
  * **Estado**

    Coluna que representa o estado do dado. Tipo String.
  * **Cidade**

    Coluna que representa a cidade do dado. Tipo String.
  * **Tipo**

    Tipo do imóvel. Podendo ser casa ou apartamento. Tipo String
  * **N° Quartos**

    Número de quartos para imóveis. Podendo ser de 1 até 3. Tipo Int.
  * **Limite Baixo - Faturamento**

    Valor do faturamento considera baixo. Tipo Int.
  * **Limite Alto - Faturamento**

    Valor do faturamento considera alto. Tipo Int..

**Link da planilha para a requisição dos dados:**


**Obs.: A planilha é atualizada automaticamente uma vez por mês, no dia 15. Sempre entre 6h e 7h da manhã.**

## Dados Airbnb E Vivareal

## Cities-info (Slack)

Este sabor é enviado pelo slack toda primeira segunda-feira do mês no canal ***cities-info***, para praticamente todas cidades do Brasil.

Aqui conseguimos unir dados do Airbnb com dados do VivaReal, e ver ao longo do tempo a evolução de faturamento, número de imóveis do Airbnb, tipo dos imóveis do Airbnb. Como também saber o número de terrenos disponíveis pelo VivaReal e evolução do preço do metro quadrado, o mesmo para casa e apartamentos.

Além da tabela apresentada abaixo, é enviado uma tabela contendo somente estado e cidade e as colunas de contagem de imóveis. Sendo enviado as 100 cidades com mais imóveis no Airbnb atualmente. O objetivo desta tabela é facilitar a seleção de cidades para iniciar uma análise de possibilidade de expansão.

| state | city | suburb | month_year | count_listings_airbnb | average_revenue_airbnb | count_apartament_airbnb | count_houses_airbnb | count_super_hosts_airbnb | count_owners_airbnb | count_qualified_listings_airbnb | price_m2_land_vivareal | lands_vivareal | price_m2_house_vivareal | houses_vivareal | price_m2_apartament_vivareal | apartaments_vivareal | price_m2_release_vivareal | realeases_vivareal |
|----|----|----|----|----|----|----|----|----|----|----|----|----|----|----|----|----|----|----|
| Santa Catarina | Florianópolis | Jardim Atlântico | 2023-02-01 | 39 | 745.8918918918919 | 21 | 12 | 10 | 27 | 0 | 1621.2704 | 306 | 4469.599 | 1091 | 8762.082 | 2879 | 24044.732 | 20 |
| Santa Catarina | Florianópolis | Jurerê Internacional | 2023-03-01 | 867 | 3278.753792298716 | 510 | 274 | 199 | 492 | 81 | 7258.6387 | 628 | 14364.424 | 3656 | 16107.978 | 3102 | 19864.184 | 12 |
| Santa Catarina | Florianópolis | Cacupé | 2022-02-01 | 59 | 4105.883660178937 | 5 | 51 | 13 | 31 | 0 | 1280.689 | 396 | 9226.877 | 1875 | 11777.649 | 1427 | 15755.567 | 18 |
| Santa Catarina | Florianópolis | Jurerê | 2022-11-01 | 1313 | 2435.52436436643 | 1029 | 179 | 296 | 684 | 66 | -2922.7183 | 675 | 10981.866 | 2373 | 13778.496 | 9648 | 15327.983 | 15 |

* **Lista de possíveis filtros**
  * Bairro
  * Faturamento
* **Informações importantes**

  Os dados referentes a preço por metro quadrado e casas, terrenos… são provenientes do site do vivareal, durante o mês de Julho de 2022, tivemos problemas, assim está linha estará com valores nulos para essas colunas. Sendo assim, quando tiver valores nulos que dizer que houve algum problema com a aquisição ou que ainda não fazíamos a aquisição do mesmos.

**Casos de uso:** Verificar evolução do Airbnb e do setor imobiliário em um determinada cidade.

**Nome query Athena:** cities_info.

**Link Athena(Saved queries):**


## Dados Vivareal

## Contato corretores por cidade/bairro, número de anúncios e valor (R$) total anunciado (Planilha do Google)

Este sabor é fornecido em um planilha do google. Agrupamos por Cidade/Bairro os corretores da seus contatos. Fazendo a contagem e ordenando pelo número de anúncios. No exemplo podemos ver que foi filtrado para mostrar somente corretores que possuem terrenos, isto pode ser mudado, para anúncios totais, apenas apartamentos residenciais, terrenos e lançamentos.

Na planilha o usuário escolhe o tipo do anúncio, o estado, cidade, caso queria pode adicionar o bairro também, mas vale lembrar que bairro é opcional. Entra no menu Rodar_Query e e click em rodar, os resultados aparecem na página Resultado.

| Estado | Cidade | Bairro | Corretor | Telefone | Whatsapp | Anuncios | anuncios_venda | anuncios_aluguel | valor_imoveis_venda | valor_imoveis_aluguel | aquisiton_date |
|----|----|----|----|----|----|----|----|----|----|----|----|
| Santa Catarina | Florianópolis | Canasvieiras | Andre Fernandes | \["48991944204"\] | 48991944204 | 16 | 0 | 16 | 1707427968 |    | 2023-03-07T00:00:00.000 |
| Santa Catarina | Florianópolis | Canasvieiras | Imobiliaria JJ Imóveis | \["4833640079", "48998420500"\] | 48998420500 | 15 | 0 | 15 | 1707427968 | 129640 | 2023-03-07T00:00:00.000 |
| Santa Catarina | Florianópolis | Canasvieiras | João Luz Corretor de Imóveis | \["48998091117", "48991650410"\] | 48991650410 | 15 | 12 | 8 | 1707427968 | 668440 | 2023-03-07T00:00:00.000 |
|    |    |    |    |    |    |    |    |    |    |    |    |

* **Dicionário de Dados**
  * **Estado**

    Coluna que representa o estado que está localizado a cidade, bairro… Esta coluna é do tipo String.
  * **Cidade**

    Coluna que representa a cidade que está localizado o bairro, casa ou aparatamento… Esta coluna é do tipo String.
  * **Bairro**

    Coluna que representa o Bairro dos dados. Esta coluna é do tipo String.
  * **Corretor**

    Nome da conta do corretor no site do Vivareal. Tipo String.
  * **Telefone**

    Número de telefones do corretor. Tipo String.
  * **Whatsapp**

    Número de telefone para contato pelo whatsapp do corretor. Tipo String.
  * **Anuncios**

    Número de anúncios que o corretor possui naquela cidade/bairro. Importante ressaltar que anuncios_venda + anuncios_aluguel pode não resultar em anúncios, pois alguns imóveis estão tanto para venda como aluguel. Coluna do tipo Int.
  * **Anuncios_venda**

    Número de anúncios para venda que o corretor possui naquela cidade/bairro. Coluna do tipo Int.
  * **Anuncios_aluguel**

    Número de anúncios para aluguel que o corretor possui naquela cidade/bairro. Coluna do tipo Int.
  * **Valor_imoveis_venda**

    Valore total dos anúncios para venda que o corretor possui naquela cidade/bairro. Coluna do tipo Int.
  * **Valor_imoveis_aluguel**

    Valore total dos anúncios para aluguel que o corretor possui naquela cidade/bairro. Coluna do tipo Int.

**Casos de Usos:** Necessidade do contato de corretores/imobiliárias em um determinado local. Podendo ser focado para encontrar algum determinado tipo de imóvel para comprar ou para simplesmente achar novas parcerias para Seazone.

**Link da planilha:**


**Nome query Athena:** Lista de Prospecção do Comercial - Cidade/Bairro, Lista de Prospecção do Comercial - Cidade, Corretores_Por_Cidade_Bairro_Somente_Terrenos.

**Link Athena(Saved queries):**

## Diagnóstico de Faturamento

# Documentação Técnica

<https://drive.google.com/file/d/1PogyGjf4C0Z0xTbX3eEib4XtN5Jvywsp/view>