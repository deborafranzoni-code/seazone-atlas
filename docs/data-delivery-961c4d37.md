<!-- title: Data Delivery | url: https://outline.seazone.com.br/doc/data-delivery-gLlUJ0ihhq | area: Tecnologia -->

# Data Delivery

O Data Delivery é a venda de dados para empresas externas. Os dados vendidos são salvos em parquets no S3 e é gerado um link para essas empresas baixarem os arquivos.

Todos os dados vendidos também pode ser consultados no Athena no database "default".

# Dados

Atualmente, é vendido dados do vivareal, olx e airbnb. Algumas informações, como número de telefone, são intencionalmente desconsideradas, visto que podem infligir na LGPD.

Todos os scripts estão no git do [pipe-lake/sorveteria](https://github.com/seazone-tech/pipe-lake/tree/dev/sorveteria). Eles são jobs no Glue que uma vez por mês vão fazer consultas nas tabelas do clean ou raw e salvar no s3.

## viva_real

| **listing_id** | **link_name** | **link_url** | **listing_type** | **listing_title** | **business_types** | **unit_type** | **unit_subtype** | **property_type** | **usage_type** | **sale_price** | **rental_price** | **rental_period** | **yearly_iptu** | **monthly_condo_fee** | **amenities** | **usable_area** | **total_area** | **bathrooms** | **bedrooms** | **suites** | **parking_spaces** | **address_state** | **address_city** | **address_neighborhood** | **address_street** | **address_street_number** | **address_zipcode** | **advertiser_id** | **advertiser_url** | **aquisition_date** | **ano** | **mes** |
|----|----|----|----|----|----|----|----|----|----|----|----|----|----|----|----|----|----|----|----|----|----|----|----|----|----|----|----|----|----|----|----|----|
| 2634693482 | Apartamento com 2 Quartos à venda, 41m² | __<https://www.vivareal.com.br/imovel/apartamento-2-quartos-santa-etelvina-bairros-manaus-com-garagem-41m2-venda-RS185000-id-2634693482/>__ | USED | Imagine acordar todos os dias em um lugar que é seu - Me chame no https://wa.me/c/ | \["SALE"\] | APARTMENT |    | UNIT | RESIDENTIAL | 185000 |    |    | 500 | 250 | \["POOL", "BARBECUE_GRILL", "GATED_COMMUNITY", "GYM", "PETS_ALLOWED", "PLAYGROUND", "SPORTS_COURT", "BICYCLES_PLACE", "CONCIERGE_24H", "AMERICAN_KITCHEN", "DISABLED_ACCESS", "COWORKING", "ELECTRONIC_GATE"\] | 41 | 41 | 1 | 2 |    | 1 | AM | Manaus | Santa Etelvina | Rua Vicente Martins | 932 | 69059830 | b55309db-7d6d-cdf8-b3a6-13a2fa5dfe17 | __<https://www.vivareal.com.br/666427/maria-freitas/>__ | 2023-08-01 | 2023 | 8 |
| 2634800059 | Apartamento com 3 Quartos à venda, 134m² | __<https://www.vivareal.com.br/imovel/apartamento-3-quartos-lapa-zona-oeste-sao-paulo-com-garagem-134m2-venda-RS1999000-id-2634800059/>__ | USED | Apartamento com 3 dormitórios à venda, 134 m² por R$ 1.999.000 - Lapa - São Paulo/SP | \["SALE"\] | APARTMENT |    | UNIT | RESIDENTIAL | 1999000 |    |    | 1000 | 1900 | \["POOL", "BARBECUE_GRILL", "ELEVATOR", "GOURMET_BALCONY", "SPORTS_COURT", "SAUNA"\] | 134 | 134 | 4 | 3 | 3 | 3 | SP | São Paulo | Vila Romana |    |    | 5047001 | 5911e983-5848-c968-855f-b4ff6c1db187 | __<https://www.vivareal.com.br/609272/union-sp/>__ | 2023-08-29 | 2023 | 8 |
| 2634825158 | Apartamento com 2 Quartos à venda, 62m² | __<https://www.vivareal.com.br/imovel/apartamento-2-quartos-bom-fim-bairros-porto-alegre-62m2-venda-RS340000-id-2634825158/>__ | USED |    | \["SALE"\] | APARTMENT |    | UNIT | RESIDENTIAL | 340000 |    |    | 55 | 300 | \[\] | 62 | 78 | 2 | 2 | 0 |    | RS | Porto Alegre | Bom Fim | Rua Fernandes Vieira | 175 | 90035091 | 28afc059-1006-ced4-e687-6958126a302a | __<https://www.vivareal.com.br/50622/berte-imoveis/>__ | 2023-08-29 | 2023 | 8 |
| 2634826688 | Apartamento com 3 Quartos à venda, 105m² | __<https://www.vivareal.com.br/imovel/apartamento-3-quartos-bom-fim-bairros-porto-alegre-105m2-venda-RS595000-id-2634826688/>__ | USED |    | \["SALE"\] | APARTMENT |    | UNIT | RESIDENTIAL | 595000 |    |    | 127 | 483 | \["ELEVATOR"\] | 105 | 117 | 2 | 3 | 0 |    | RS | Porto Alegre | Floresta | Rua Santo Antônio | 938 | 90220010 | 28afc059-1006-ced4-e687-6958126a302a | __<https://www.vivareal.com.br/50622/berte-imoveis/>__ | 2023-08-29 | 2023 | 8 |
| 2634916761 | Apartamento com 2 Quartos à venda, 73m² | __<https://www.vivareal.com.br/imovel/apartamento-2-quartos-vila-joaquim-inacio-bairros-campinas-com-garagem-73m2-venda-RS209000-id-2634916761/>__ | USED | apartamento - Vila Joaquim Inácio - Campinas | \["SALE"\] | APARTMENT |    | UNIT | RESIDENTIAL | 209000 |    |    | 400 | 350 | \["INTERCOM"\] | 73 | 73 | 2 | 2 |    | 1 | SP | Campinas | Vila Joaquim Inácio | Rua Frederico Ozanam | 177 | 13045640 | 198e5397-2388-7e6e-97be-aedd328a6aeb | __<https://www.vivareal.com.br/136365/claudia-miranda-alcantara-ribeiro/>__ | 2023-08-29 | 2023 | 8 |

## olx

| **listing_id** | **title** | **category** | **business_types** | **created** | **link_url** | **price** | **iptu** | **condominium** | **usable_area** | **bathrooms** | **rooms** | **garage** | **beds** | **state** | **region** | **features** | **complex_features** | **zone** | **municipality** | **neighbourhood** | **zipcode** | **raw_location** | **aquisition_date** | **user_id** | **ano** | **mes** |
|----|----|----|----|----|----|----|----|----|----|----|----|----|----|----|----|----|----|----|----|----|----|----|----|----|----|----|
| 1225122897 | Apartamento Locação Higienópolis 230 m² 3 Dormitórios | apartamento | Aluguel | 2023-08-22 15:11:59 | __<https://sp.olx.com.br/sao-paulo-e-regiao/imoveis/apartamento-locacao-higienopolis-230-m-3-dormitorios-1225122897>__ | 16999 | 820 | 4500 | 230 | 3 | 3 | 2 |    | SP | São Paulo e região, SP | Área de serviço | null | zona-oeste | São Paulo | Higienópolis | 1240020 |    | 2023-08-29 | 119920569 | 2023 | 8 |
| 1225124116 | Apartamento com elevador e vista para o mar em Rio das Ostras, RJ. | apartamento | Venda | 2023-08-22 15:15:51 | __<https://rj.olx.com.br/norte-do-estado-do-rio/imoveis/apartamento-com-elevador-e-vista-para-o-mar-em-rio-das-ostras-rj-1225124116>__ | 220000 | 0 | 370 | 50 | 1 | 2 | 1 |    | RJ | Norte do Estado e Região dos Lagos, RJ | Armários na cozinha | Salão de festas | regiao-dos-lagos | Rio das Ostras | Jardim Campomar | 28890395 | {"suburb": "Jardim Campomar", "city": "Rio das Ostras", "municipality": "Regi\\u00e3o Geogr\\u00e1fica Imediata de Maca\\u00e9-Rio das Ostras", "state_district": "Regi\\u00e3o Geogr\\u00e1fica Intermedi\\u00e1ria de Maca\\u00e9-Rio das Ostras-Cabo Frio", "state": "Rio de Janeiro", "ISO3166-2-lvl4": "BR-RJ", "region": "Regi\\u00e3o Sudeste", "postcode": "28890-281", "country": "Brasil", "country_code": "br"} | 2023-08-29 | 124052769 | 2023 | 8 |
| 1225124281 | APARTAMENTO VL ANTONIETA CONDOMÍNIO CLUBE-45MTS- 2 DORMS, SALA C/ SACADA, COZINHA, 1 VAGA | apartamento | Venda | 2023-08-22 15:16:28 | __<https://sp.olx.com.br/sao-paulo-e-regiao/imoveis/apartamento-vl-antonieta-condominio-clube-45mts-2-dorms-sala-c-sacada-cozinha-1-vaga-1225124281>__ | 370000 | 0 | 300 | 45 | 1 | 2 | 1 |    | SP | São Paulo e região, SP | Academia, Churrasqueira, Mobiliado, Piscina | Academia, Condomínio fechado, Elevador, Permitido animais, Piscina, Portaria, Salão de festas | zona-leste | São Paulo | Vila Antonieta | 3474017 | {"suburb": "Vila Santa Antonieta", "city_district": "Mar\\u00edlia", "city": "Mar\\u00edlia", "municipality": "Regi\\u00e3o Imediata de Mar\\u00edlia", "state_district": "Regi\\u00e3o Geogr\\u00e1fica Intermedi\\u00e1ria de Mar\\u00edlia", "state": "S\\u00e3o Paulo", "ISO3166-2-lvl4": "BR-SP", "region": "Regi\\u00e3o Sudeste", "country": "Brasil", "country_code": "br"} | 2023-08-29 | 123624649 | 2023 | 8 |
| 1225123975 | CASA 3 DORMITÓRIOS EM NOVA TRAMANDAÍ | casa | Venda | 2023-08-22 15:15:27 | __<https://rs.olx.com.br/regioes-de-porto-alegre-torres-e-santa-cruz-do-sul/imoveis/casa-3-dormitorios-em-nova-tramandai-1225123975>__ | 279000 | 0 | 0 | 127 | 3 | 3 | 1 |    | RS | Porto Alegre e região, RS | Área de serviço, Churrasqueira | null | outras-cidades | Tramandaí |    | 95590000 | {"amenity": "Prefeitura Municipal de Tramanda\\u00ed", "road": "Avenida da Igreja", "hamlet": "Beira-Mar", "suburb": "Centro", "city_district": "Tramanda\\u00ed", "town": "Tramanda\\u00ed", "municipality": "Regi\\u00e3o Geogr\\u00e1fica Imediata de Tramanda\\u00ed - Os\\u00f3rio", "county": "Aglomera\\u00e7\\u00e3o Urbana do Litoral Norte", "state_district": "Regi\\u00e3o Geogr\\u00e1fica Intermedi\\u00e1ria de Porto Alegre", "state": "Rio Grande do Sul", "ISO3166-2-lvl4": "BR-RS", "region": "Regi\\u00e3o Sul", "postcode": "95625-000", "country": "Brasil", "country_code": "br"} | 2023-08-29 | 119421767 | 2023 | 8 |
| 1225123997 | Vende-se terreno murado. | casa | Venda | 2023-08-22 15:15:30 | __<https://ap.olx.com.br/amapa/imoveis/vende-se-terreno-murado-1225123997>__ | 50000 | 0 | 0 | 0 | 0 | 0 |    |    | AP | Amapá, AP | null | Área murada, Permitido animais | macapa | Macapá | Brasil Novo | 68909308 |    | 2023-08-29 | 18744740 | 2023 | 8 |

## airbnb

| **aquisition_date** | **url** | **ad_name** | **listing_id** | **amenities****\["Wi-Fi", "TV a Cabo", "Cozinha", "Ferro de passar", "Espaço de trabalho exclusivo", "Cabides", "TV", "Máquina de Lavar", "Básico", "Estacionamento pago fora da propriedade", "Estacionamento gratuito na rua", "Rede/grade de proteção nas janelas", "Blackout nas cortinas", "Água quente", "Roupa de cama", "Cobertores e travesseiros extras", "Microondas", "Cafeteira", "Refrigerador", "Louças e talheres", "Itens básicos de cozinha", "Forno", "Fogão", "É permitido deixar as malas", "Estadias de longa duração são permitidas", "O anfitrião recebe você", "Mesa de jantar", "Torradeira", "Ventiladores portáteis", "Produtos de limpeza", "Varal para secar roupas", "Local para guardar as roupas", "Taças de vinho"\]****\["Estacionamento incluído", "Cozinha", "Piscina", "Ar-condicionado", "TV", "Básico", "Entrada privada", "Água quente", "Roupa de cama", "Microondas", "Refrigerador", "Louças e talheres", "Itens básicos de cozinha", "Forno", "Fogão", "Casa térrea", "Churrasqueira", "Pátio ou varanda", "Quintal", "Acesso ao lago", "Chaleira de água quente", "Ventilador de teto", "Área de jantar externa", "Chuveiro externo", "Mesa de jantar", "Freezer", "Assadeira", "Utensílios para churrasco", "Local para guardar as roupas"\]****\["TV", "TV a Cabo", "Wi-Fi", "Ar-condicionado", "Cozinha", "Máquina de Lavar", "Básico", "Ferro de passar"\]****\["TV", "TV a Cabo", "Wi-Fi", "Ar-condicionado", "Cozinha", "Estacionamento incluído", "Café da Manhã", "Elevador", "Aquecimento Central", "Máquina de Lavar", "Kit de primeiros socorros", "Extintor de incêndio", "Básico", "Xampu", "Cabides", "Secador de cabelo", "Ferro de passar"\]****\["Estacionamento incluído", "Lareira interna", "Café da Manhã", "Wi-Fi", "Cozinha", "Academia", "TV", "Máquina de Lavar"\]** | **number_of_bathrooms** | **number_of_bedrooms** | **latitude** | **longitude** | **star_rating** | **check_in** | **check_out** | **number_of_guests** | **number_of_reviews** | **owner_id** | **listing_type** | **ano** | **mes** |
|----|----|----|----|----|----|----|----|----|----|----|----|----|----|----|----|----|----|
| 2023-06-26 15:00:12 | __<https://www.airbnb.com.br/rooms/1138171>__ | Apto super espaçoso e bem localizado na Bela Vista | 1138171 | 1 | 2 | -23.55699921 | -46.64099884 | 5 | 14:00 - 00:00 | 11:00 | 5 | 248 | 6243451 | Espaço inteiro: apartamento | 2023 | 6 |
| 2023-06-26 15:38:57 | __<https://www.airbnb.com.br/rooms/11528893>__ | Lindo Sítio de Lazer em Meaípe | 11528893 | 3 | 3 | -20.68565941 | -40.56647873 | 4.5 | 15:00 - 18:00 | 12:00 | 12 | 50 | 10415876 | Espaço inteiro: casa | 2023 | 6 |
| 2023-06-26 16:03:19 | __<https://www.airbnb.com.br/rooms/11892542>__ | Ver fotos. Natureza, vista, calmo | 11892542 | 2 | 3 | -22.92295074 | -43.36326981 |    |    |    | 6 | 0 | 63422338 | Espaço inteiro: casa | 2023 | 6 |
| 2023-06-26 15:30:04 | __<https://www.airbnb.com.br/rooms/12038128>__ | Apartamento Jd. Botânico Olimpíadas | 12038128 | 2 | 4 | -22.9611702 | -43.21723175 |    |    |    | 8 | 0 | 64439025 | Espaço inteiro: apartamento | 2023 | 6 |
| 2023-06-26 14:53:10 | __<https://www.airbnb.com.br/rooms/13098651>__ | Suíte Granja Viana, Cotia - SP | 13098651 | 1 | 1 | -23.59038925 | -46.86798096 |    | 11:00 - 20:00 | 11:00 | 2 | 0 | 72755404 | Quarto privativo em condomínio | 2023 | 6 |

# Planilha

Toda a configuração para a venda externa é realizada na Planilha [dados-seazone-setup](https://docs.google.com/spreadsheets/d/1_elPld91D80u-qKNdpv4TM41RxQAwFmU1FTxv2uIxo4/edit?gid=1846300571#gid=1846300571). Até hoje, foram vendido dados para três empresas, oases, locates e brognoli.

Os respectivos links das planilhas de venda se encontram no próprio appscript.

 ![](/api/attachments.redirect?id=59efc459-c139-4cbc-ad7f-44ce7557e6eb " =381x37")

## Automação

A lógica é:

* Uma vez por semana, o appscript roda para a empresa X
* Ele vê quais dados de quais OTAs essa empresa comprou pro mês de agora
* Ele dispara o endpoint do lambda data_delivery_url que gera um link de download de até 7 dias de expiração (7 dias é o máximo) para esses arquivos do mês de agora.
* O appscript adiciona o link na planilha da empresa X junto com a data de expiração.

Nas abas com os respectivos nomes das empresas é feita a configuração de quais dados serão permitidos a venda.

 ![](/api/attachments.redirect?id=2cb3a7fa-3997-434f-9892-2b65c7974940 "left-50 =257x353")


\
Nesse exemplo da Locates, de 2023-12 até 2024-12 eles estavam comprando dados de viva-real e olx.

Entretanto, depois, passaram a comprar dados apenas da olx, então REMOVEMOS as linhas de olx de 2025 e MANTEMOS apenas as de viva-real.


\

\
 ![](/api/attachments.redirect?id=4666ea3e-a215-45a4-b386-180f639d4084 "left-50 =300x348")


\
Hoje é dia 2026-03-09, Locates renovaram o contrato até uma data indefinida, então, manualmente foi colocado na planilha para permitir a venda até 2027-12 de viva-real.

Se, por exemplo, eles cancelarem o contrato em 2027-01, então temos que manualmente apagar as linhas após 2027-01.


\

\
## Manual

Caso aconteça algum problema e seja necessário manualmente atualizar os links, é possível utilizar a aba "especificar_urls". Basta selecionar quais meses de quais OTAs precisam ser atualizados e qual a Planilha. Depois, só rodar a função "specifyUrls" do appscript.

 ![](/api/attachments.redirect?id=ec17928b-ad1b-473a-b04a-f7b48d4be421 " =455.5x187")


\

\