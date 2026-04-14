<!-- title: Integração Afiliado Booking | url: https://outline.seazone.com.br/doc/integracao-afiliado-booking-meRwEMsEDk | area: Tecnologia -->

# Integração Afiliado Booking

# Estudo inicial

Esta integração visa permitir a criação de links afiliados para o Booking por meio da API do Awin. Assim, quando não houver imóveis disponíveis em nosso site, podemos oferecer ao usuário opções do Booking que correspondam aos filtros aplicados. Dessa forma, caso o usuário conclua a reserva de uma acomodação pelo nosso link, receberemos uma comissão sobre a transação.

## Awin

https://www.awin.com/br

Awin é uma plataforma de marketing de afiliados que conecta empresas a parceiros que promovem seus produtos e serviços online por meio de links personalizados. As empresas pagam comissões aos parceiros por cada venda.

### Geração de link

<https://developer.awin.com/apidocs/generatelink>

Foi verificado que é possível gerar o link de afiliado caso a partir do link de destino da booking que teremos. Abaixo segue um exemplo de como realizá-lo:


**ROTA:** /publishers/{publisherId}/linkbuilder/generate


**Parâmetros da Query**

| **Nome** | **Descrição** | **Valor** |
|----|----|----|
| publisherId | ID do publisher, obrigatório, informado no caminho da URL. | Disponível no [vault](https://vault.sapron.com.br/ui/vault/secrets/secret/show/Website-Reservas/Awin/credenciais_de_conex%C3%A3o) |
| accessToken | Token de acesso. | Disponível no [vault](https://vault.sapron.com.br/ui/vault/secrets/secret/show/Website-Reservas/Awin/credenciais_de_conex%C3%A3o) |

**Parâmetros do Body**

| **Nome** | **Tipo** | **Descrição** |
|----|----|----|
| advertiserId | int | Identificador do anunciante no Awin para o qual o link será gerado (no nosso caso, o Booking). Esse campo é obrigatório. |
| destinationUrl | str | URL de destino onde o usuário será redirecionado, como uma página específica de hotel no Booking. Esse campo é opcional, mas essencial para direcionar o tráfego ao site correto. |
| shorten | bool | Booleano opcional que, se definido como `true`, solicita que a Awin encurte o link gerado. |
| parameters | dict | Um objeto com parâmetros opcionais para rastreamento. Inclui `campaign`, `clickref` até `clickref6`, para capturar informações personalizadas, como identificadores de usuário ou seções específicas do site. |

**Exemplo de código:**

```python

import requests

our_publisher_id = ""

booking_advertiser_id = ""

api_token = ""

prefix = "https://api.awin.com"
endpoint = f"/publishers/{our_publisher_id}/linkbuilder/generate"
url = f"{prefix}{endpoint}"

destination_url_example = "https://www.booking.com/hotel/br/flat-lindo-e-tranquilo.pt-br.html?aid=304142&label=gen173nr-1FCAEoggI46AdIM1gEaCCIAQGYAS24ARnIAQzYAQHoAQH4AQOIAgGoAgO4AtrXs7kGwAIB0gIkZmEwNDE0NGYtNzEyYi00MzYwLWI3NTItYWM1ODFjMDZiZmNj2AIG4AIB&sid=8fb9008d9981abc833ae063f04dd4b84&all_sr_blocks=1150135101_392652749_2_0_0;checkin=2025-02-28;checkout=2025-03-04;dist=0;group_adults=2;group_children=0;hapos=8;highlighted_blocks=1150135101_392652749_2_0_0;hpos=8;matching_block_id=1150135101_392652749_2_0_0;no_rooms=1;req_adults=2;req_children=0;room1=A%2CA;sb_price_type=total;sr_order=popularity;sr_pri_blocks=1150135101_392652749_2_0_0__67576;srepoch=1730997222;srpvid=5cb7746e69d0027b;type=total;ucfs=1&"

payload = {
    "advertiserId": booking_advertiser_id,
    "destinationUrl": destination_url_example,
    "shorten": True,
}

headers = {"accept": "application/json", "content-type": "application/json"}

response = requests.post(
    f"{url}?accessToken={api_token}", json=payload, headers=headers
)

print(response.json()["shortUrl"])
```

**Output exemplo:**

```python
https://tidd.ly/40DMKqW
```

### Geração de links em lote

<https://developer.awin.com/apidocs/generatebatchlinks>

Também é possível gerar links em lote, com um limite de até 100 links por requisição, porém, nesse caso, não é possível gerar o link curto. Abaixo segue um exemplo de como fazer:


**ROTA:** /publishers/{publisherId}/linkbuilder/generate-batch


**Parâmetros da Query**

| **Nome** | **Descrição** | **Valor** |
|----|----|----|
| publisherId | ID do publisher, obrigatório, informado no caminho da URL. | Disponível no [vault](https://vault.sapron.com.br/ui/vault/secrets/secret/show/Website-Reservas/Awin/credenciais_de_conex%C3%A3o) |
| accessToken | Token de acesso. | Disponível no [vault](https://vault.sapron.com.br/ui/vault/secrets/secret/show/Website-Reservas/Awin/credenciais_de_conex%C3%A3o) |

**Parâmetros do Body**

| requests | list | Uma lista de objetos, onde cada objeto define as informações necessárias para criar um link de afiliado. Cada item na lista deve incluir o `advertiserId` (ID do anunciante), `destinationUrl` (URL de destino) e, opcionalmente, parâmetros como clickref para rastreamento  |
|----|----|----|

**Exemplo de código:**

```python
import requests

our_publisher_id = ""
booking_advertiser_id = ""
api_token = ""
prefix = "https://api.awin.com"
endpoint = f"/publishers/{our_publisher_id}/linkbuilder/generate-batch"
url = f"{prefix}{endpoint}"

destination_urls = [
    "https://www.booking.com/hotel/br/flat-lindo-e-tranquilo.pt-br.html?aid=304142&label=gen173nr-1FCAEoggI46AdIM1gEaCCIAQGYAS24ARnIAQzYAQHoAQH4AQOIAgGoAgO4AtrXs7kGwAIB0gIkZmEwNDE0NGYtNzEyYi00MzYwLWI3NTItYWM1ODFjMDZiZmNj2AIG4AIB&sid=8fb9008d9981abc833ae063f04dd4b84&all_sr_blocks=1150135101_392652749_2_0_0;checkin=2025-02-28;checkout=2025-03-04;dist=0;group_adults=2;group_children=0;hapos=8;highlighted_blocks=1150135101_392652749_2_0_0;hpos=8;matching_block_id=1150135101_392652749_2_0_0;no_rooms=1;req_adults=2;req_children=0;room1=A%2CA;sb_price_type=total;sr_order=popularity;sr_pri_blocks=1150135101_392652749_2_0_0__67576;srepoch=1730997222;srpvid=5cb7746e69d0027b;type=total;ucfs=1&",
    "https://www.booking.com/hotel/br/casa-de-vista-para-o-mar.pt-br.html?aid=304142&label=gen173nr-1FCAEoggI46AdIM1gEaCCIAQGYAS24ARnIAQzYAQHoAQH4AQyIAgGoAgO4Arqp07kGwAIB0gIkMWU2ZTc3NTEtMTYzOC00MzJmLWI5YzctYWJkMTRkOGMyMDFh2AIG4AIB&sid=8fb9008d9981abc833ae063f04dd4b84&all_sr_blocks=1160188501_389826455_2_0_0&checkin=2025-02-28&checkout=2025-03-04&dest_id=-643337&dest_type=city&dist=0&group_adults=2&group_children=0&hapos=8&highlighted_blocks=1160188501_389826455_2_0_0&hpos=8&matching_block_id=1160188501_389826455_2_0_0&no_rooms=1&req_adults=2&req_children=0&room1=A%2CA&sb_price_type=total&sr_order=popularity&sr_pri_blocks=1160188501_389826455_2_0_0__69300&srepoch=1731515601&srpvid=577c74643dff0403&type=total&ucfs=1&"
]

requests_payload = [
    {
        "advertiserId": booking_advertiser_id,
        "destinationUrl": url,
    }
    for url in destination_urls
]

payload = {"requests": requests_payload}

headers = {"accept": "application/json", "content-type": "application/json"}

response = requests.post(f"{url}?accessToken={api_token}", json=payload, headers=headers)

for link in response.json()["responses"]:
    print(link["body"]["url"])
```

**Output exemplo:**

```python
https://www.awin1.com/cread.php?awinmid=18120&awinaffid=1661985&ued=https%3A%2F%2Fwww.booking.com%2Fhotel%2Fbr%2Fflat-lindo-e-tranquilo.pt-br.html%3Faid%3D304142%26label%3Dgen173nr-1FCAEoggI46AdIM1gEaCCIAQGYAS24ARnIAQzYAQHoAQH4AQOIAgGoAgO4AtrXs7kGwAIB0gIkZmEwNDE0NGYtNzEyYi00MzYwLWI3NTItYWM1ODFjMDZiZmNj2AIG4AIB%26sid%3D8fb9008d9981abc833ae063f04dd4b84%26all_sr_blocks%3D1150135101_392652749_2_0_0%3Bcheckin%3D2025-02-28%3Bcheckout%3D2025-03-04%3Bdist%3D0%3Bgroup_adults%3D2%3Bgroup_children%3D0%3Bhapos%3D8%3Bhighlighted_blocks%3D1150135101_392652749_2_0_0%3Bhpos%3D8%3Bmatching_block_id%3D1150135101_392652749_2_0_0%3Bno_rooms%3D1%3Breq_adults%3D2%3Breq_children%3D0%3Broom1%3DA%252CA%3Bsb_price_type%3Dtotal%3Bsr_order%3Dpopularity%3Bsr_pri_blocks%3D1150135101_392652749_2_0_0__67576%3Bsrepoch%3D1730997222%3Bsrpvid%3D5cb7746e69d0027b%3Btype%3Dtotal%3Bucfs%3D1%26&platform=pl
https://www.awin1.com/cread.php?awinmid=18120&awinaffid=1661985&ued=https%3A%2F%2Fwww.booking.com%2Fhotel%2Fbr%2Fcasa-de-vista-para-o-mar.pt-br.html%3Faid%3D304142%26label%3Dgen173nr-1FCAEoggI46AdIM1gEaCCIAQGYAS24ARnIAQzYAQHoAQH4AQyIAgGoAgO4Arqp07kGwAIB0gIkMWU2ZTc3NTEtMTYzOC00MzJmLWI5YzctYWJkMTRkOGMyMDFh2AIG4AIB%26sid%3D8fb9008d9981abc833ae063f04dd4b84%26all_sr_blocks%3D1160188501_389826455_2_0_0%26checkin%3D2025-02-28%26checkout%3D2025-03-04%26dest_id%3D-643337%26dest_type%3Dcity%26dist%3D0%26group_adults%3D2%26group_children%3D0%26hapos%3D8%26highlighted_blocks%3D1160188501_389826455_2_0_0%26hpos%3D8%26matching_block_id%3D1160188501_389826455_2_0_0%26no_rooms%3D1%26req_adults%3D2%26req_children%3D0%26room1%3DA%252CA%26sb_price_type%3Dtotal%26sr_order%3Dpopularity%26sr_pri_blocks%3D1160188501_389826455_2_0_0__69300%26srepoch%3D1731515601%26srpvid%3D577c74643dff0403%26type%3Dtotal%26ucfs%3D1%26&platform=pl
```

## JSON de Propriedades

Os dados das propriedades disponíveis no Booking são obtidos e disponibilizados pelo time de dados. A partir dessas informações, os dados serão tratados para gerar um JSON estruturado com as propriedades.


**Formato:**

```json
[
  {
    "platform_id": 4511171,
    "platform_name": "Booking",
    "address_state": "Rio de Janeiro",
    "address_state_code": "RJ",
    "address_city": "Rio de Janeiro",
    "title": "Casa da Coruja",
    "type": "House",
    "room_quantity": 1,
    "guest_capacity": null,
    "min_night_price": 350.0,
    "review_number": 10,
    "review_score": 10,
    "affiliate_link": "https://www.awin1.com/cread.php?awinmid=18120&awinaffid=1661985&ued=https%3A%2F%2Fwww.booking.com%2Fhotel%2Fbr%2Fcasa-da-coruja-rio-de-janeiro.pt-br.html%3Faid%3D304142%26label%3Dgen173nr-1FCAsoIEIdY2FzYS1kYS1jb3J1amEtcmlvLWRlLWphbmVpcm9ILVgEaCCIAQGYAS24ARnIAQzYAQHoAQH4AQqIAgGoAgO4AvyM87kGwAIB0gIkYWJmODQ4Y2QtNjVlYi00NTVjLThhMDgtODI2MDYzY2I2YzY52AIF4AIB%26sid%3D8fb9008d9981abc833ae063f04dd4b84%26age%3D1%26checkin%3D2025-01-06%26checkout%3D2025-01-10%26dest_id%3D-666610%26dest_type%3Dcity%26dist%3D0%26do_availability_check%3D1%26group_adults%3D2%26group_children%3D1%26hp_avform%3D1%26hp_group_set%3D0%26no_rooms%3D1%26origin%3Dhp%26sb_price_type%3Dtotal%26src%3Dhotel%26type%3Dtotal%26%23group_recommendation&platform=pl",
    "main_image": "https://cf.bstatic.com/xdata/images/hotel/max1024x768/336998046.jpg?k=5a238bf5c448ff09009707e75234e5bd58811372b537471baf7beab1a94ac759&o=&hp=1",
    "images": null,
    "platform_url": "https://www.booking.com/hotel/br/casa-da-coruja-rio-de-janeiro.pt-br.html?-1FCAsoIEIdY2FzYS1kYS1jb3J1amEtcmlvLWRlLWphbmVpcm9ILVgEaCCIAQGYAS24ARnIAQzYAQHoAQH4AQqIAgGoAgO4AvyM87kGwAIB0gIkYWJmODQ4Y2QtNjVlYi00NTVjLThhMDgtODI2MDYzY2I2YzY52AIF4AIB&sid=8fb9008d9981abc833ae063f04dd4b84&age=1&checkin=2025-01-06&checkout=2025-01-10&dest_id=-666610&dest_type=city&dist=0&do_availability_check=1&group_adults=2&group_children=1&hp_avform=1&hp_group_set=0&no_rooms=1&origin=hp&sb_price_type=total&src=hotel&type=total&#group_recommendation&aid=1784973&label=affnetawin-index_pub-1661985_site-_pname-KHANTO+RESERVAS+LTDA_plc-_ts-_clkid-18120_1732045560_c7fa1561dc1e5492f574f1b5fee5c0f1&sv1=affiliate&sv_campaign_id=1661985&aid=1784973&label=affnetawin-index_pub-1661985_site-_pname-KHANTO+RESERVAS+LTDA_plc-_ts-_clkid-18120_1732045560_c7fa1561dc1e5492f574f1b5fee5c0f1"
  },
  {
    "platform_id": 11228355,
    "platform_name": "Booking",
    "address_state": "Rio de Janeiro",
    "address_state_code": "RJ",
    "address_city": "Rio de Janeiro",
    "title": "Casa linda em Campo Grande rj",
    "type": "House",
    "room_quantity": 2,
    "guest_capacity": null,
    "min_night_price": 328.0,
    "review_number": 10,
    "review_score": 10,
    "affiliate_link": "https://www.awin1.com/cread.php?awinmid=18120&awinaffid=1661985&ued=https%3A%2F%2Fwww.booking.com%2Fhotel%2Fbr%2Fcasa-linda-em-campo-grande-rj.pt-br.html%3Faid%3D304142%26sid%3Dc59d5aa6d995910ed7c5561b4b36e3dd%26dest_id%3D0%26%3Bno_rooms%3D1%3Bgroup_adults%3D2%3B&platform=pl",
    "main_image": "https://cf.bstatic.com/xdata/images/hotel/max1024x768/513351378.jpg?k=6df958bed4495b4c2fcc32776df31d9a6da5f60372ea250808629080a1e48dd0&o=&hp=1",
    "images": null,
    "platform_url": "https://www.booking.com/hotel/br/casa-linda-em-campo-grande-rj.pt-br.html?sid=c59d5aa6d995910ed7c5561b4b36e3dd&dest_id=0&;no_rooms=1;group_adults=2;&aid=1784973&label=affnetawin-index_pub-1661985_site-_pname-KHANTO+RESERVAS+LTDA_plc-_ts-_clkid-18120_1732045700_7a4792f6cc7617be225057e413ac1970&sv1=affiliate&sv_campaign_id=1661985&aid=1784973&label=affnetawin-index_pub-1661985_site-_pname-KHANTO+RESERVAS+LTDA_plc-_ts-_clkid-18120_1732045700_7a4792f6cc7617be225057e413ac1970"
  }
]
```


Esse JSON está armazenado no bucket `seazone-reservas-referral-acommodations-prod` com o nome `booking_affiliate_properties.json`.

# Rota para obter as propriedades de afiliados

Foi criada uma rota para disponibilizar o arquivo `booking_affiliate_properties.json`.

**Endpoint:**  `GET /affiliates/properties`

Ao enviar a requisição para esse endpoint, será retornado o **JSON** no formato definido na seção de [JSON de Propriedades](/doc/integracao-afiliado-booking-GRJcfceA8L), contendo as informações das propriedades.

O arquivo mencionado é acessado por meio de uma integração com o S3, de onde é obtido através da busca por nome. O retorno do endpoint foi cacheado visando uma melhor performance, fazendo com que o response time da API fique em torno de 55 a 150ms.

# Referências


---

https://developer.awin.com/docs

**Geração de link**

https://developer.awin.com/apidocs/generatelink

**Geração de links em lote**

https://developer.awin.com/apidocs/generatebatchlinks