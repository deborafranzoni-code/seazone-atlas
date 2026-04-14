<!-- title: Refatoração da Integração com a Stays | url: https://outline.seazone.com.br/doc/refatoracao-da-integracao-com-a-stays-ahQf6BzdC3 | area: Tecnologia -->

# Refatoração da Integração com a Stays

## Rotas Utilizadas no Sapron

### POST /external/v1/booking/reservations-export

Retorna um conjunto de reservas de acordo com alguns filtros, que são enviados no body da requisição.

Essa rota é utilizada pelos workers de criação/atualização de reservas, para obter as reservas recentes que foram inseridas ou atualizadas na Stays.

**Payload:**

* *from*: data inicial da consulta;
* *to*: data final da consulta;
* *dateType*: referente ao tipo de data que deve ser filtrado. Por exemplo, `"departure"` representa que a rota vai buscar por reservas em que a data de check-out esteja entre as datas especificadas nos campos "from" e "to". Já `"creation"` representa que a rota deve retornar reservas cuja data de criação esteja entre o intervalo fornecido. Há outras possibilidades também, como `"arrival"`, `"creationorig"` e `included`, mas no contexto de reservas, apenas `"creation"` e `"departure"` são utilzados.
* *type*: tipo da reserva. Por exemplo, pode ser `"blocked"`, `"contract"`, `"booked"`, `"maintenance"` ou `"canceled"`. Nas rotas de criação/atualização de reserva, nenhum tipo é aplicado, ou seja, buscamos todas as reservas em um dado período.

  \

```javascript
{
  "from": "YYYY-AA-MM",
  "to": "YYYY-AA-MM",
  "dateType": "departure"
  "type": null,
}
```

**Resposta:**

```javascript
[
    {
        "_id": "<Stays Reservation ID>",
        "id": "<Stays Reservation Code>",
        "type": "booked",
        "currency": "BRL",
        "checkInDate": "2025-02-15",
        "checkOutDate": "2025-02-16",
        "guestTotalCount": 4,
        "nightCount": 1,
        "creationDate": "2025-02-15",
        "forwardingDate": "2025-02-16",
        "pricePerNight": 242,
        "reserveTotal": 454,
        "listingInvoiceTotal": 454,
        "extraServicesTotal": 0,
        "listing": {
            "id": "<Listing ID in OTA>",
            "internalName": "<Property Code>"
        },
        "baseAmountForwarding": 454,
        "sellPriceCorrected": 383.87,
        "companyCommision": 76.77,
        "buyPrice": 307.1,
        "totalForwardFee": 70.13,
        "totalForwardFeeAfter": 0,
        "totalForwardFeeAll": 70.13,
        "client": {
            "name": "Fulano Silva",
            "firstName": "Fulano",
            "lastName": "Silva",
            "phoneNumber": "+55 61 99901 0203"
        },
        "hasReview": false,
        "partnerName": "API airbnb",
        "agentName": "Sicrano Santos",
        "ownerFee": [
            {
                "val": 70.13,
                "desc": "API airbnb"
            }
        ],
        "ownerFeeAfter": [],
        "documents": [],
        "fee": [],
        "partnerCode": "<partner code>"
    },
    ...
]
```

### GET /external/v1/booking/reservations/<Stays Reservation Code>

Retorna dados específicos relacionados a uma determinada reserva;

Essa rota é utilizada pelos workers de criação/atualização de reservas, para obter detalhes de uma reserva específica. Esses detalhes não são retornados na rota descrita na seção anterior. Por exemplo, ela roetorna detalhes dos guests, ou informação de preços da reserva, que são usados para calcular as taxas da reserva, etc.

**Resposta:**

```javascript
{
    "_id": "<Stays Reservation ID>",
    "id": "<Stays Reservation Code>",
    "creationDate": "2025-02-15",
    "checkInDate": "2025-02-15",
    "checkInTime": "15:00",
    "checkOutDate": "2025-02-16",
    "checkOutTime": "11:00",
    "_idlisting": "6740e4cae273bdd1294e43e0",
    "_idclient": "67b114d0289081c3a799de91",
    "type": "booked",
    "operator": {
        "_id": "<operator ID>",
        "name": "StaysBot"
    },
    "agent": {
        "_id": "<agent ID>",
        "name": "Sicrano Santos"
    },
    "price": {
        "currency": "BRL",
        "_f_expected": 242,
        "_f_total": 454,
        "hostingDetails": {
            "fees": [],
            "discounts": [],
            "_f_nightPrice": 454,
            "_f_total": 454
        },
        "extrasDetails": {
            "fees": [],
            "extraServices": [],
            "discounts": [],
            "_f_total": 0
        }
    },
    "stats": {
        "_f_totalPaid": 454
    },
    "guests": 4,
    "guestsDetails": {
        "adults": 4,
        "children": 0,
        "infants": 0,
        "list": [
            {
                "type": "adult",
                "name": "Fulana Silva",
                "phones": [
                    {
                        "iso": "+55619991010203",
                        "hint": "AirBnB"
                    }
                ],
                "primary": true
            },
            {
                "type": "adult",
                "name": "adult_1"
            },
            {
                "type": "adult",
                "name": "adult_2"
            },
            {
                "type": "adult",
                "name": "adult_3"
            }
        ]
    },
    "partner": {
        "_id": "<partner id>",
        "name": "API airbnb",
        "commission": {
            "type": "fixed",
            "_mcval": {
                "BRL": 70.13
            }
        }
    },
    "partnerCode": "<partner code>",
    "reservationUrl": "https://ssl.stays.com.br/i/account-overview/67b114d0289081c3a799de91?reserve=SN569I"
}
```

### GET /external/v1/settings/listing/<listing ID>/sellprice

Retorna dados de preço de venda para um determinado listing.

Por meio dessa rota, obtemos a taxa de limpeza de uma propriedade.

**Resposta:**

```javascript
{
    "_idlisting": "<Property Listing ID>",
    "mainCurrency": "BRL",
    "fees": [
        {
            "_id": "<Stays Reservation ID>",
            "_f_val": 212,
            "type": "fixed",
            "chargeType": "perReserve",
            "invoiceVisibility": "hidden",
            "internalName": "Cleaning Fee",
            "_mstitle": {
                "pt_BR": "Taxa de Limpeza",
                "en_US": "Cleaning Fee"
            }
        }
    ],
    "guestsIncluded": 4
}
```

### GET /external/v1/booking/promo-codes/<promo_code_id>

Rota que fornece detalhes sobre um determinado código promocional.

Esse promo-code pode ser obtido através da rota de [detalhes de uma reserva](https://outline.seazone.com.br/doc/refatoracao-da-integracao-com-a-stays-AUEEgUqY9k#h-get-externalv1bookingreservationslessstays-reservation-codegreater), no campo `_idpromoCode`. Nem sempre uma reserva terá essa informação.

O desconto dado pode ser de dois tipos: fixo e percentual. Quando o tipo é percentual, o valor percentual do desconto é retornado no campo `_f_discount`. Quando o tipo é fixo, o valor é retornado no campo `_mcdiscount["BRL"]`.

Para calcular o desconto com valor percentual, utiliza-se a seguinte fórmula:

```javascript
total_night_price * (discount_value / 100)
```

Para calcular o desconto com valor fixo, utiliza-se a fórmula:

```javascript
total_night_price - discount_value
```


\

\
### POST /external/v1/booking/reservations/

Utilizada para criação de bloqueios a partir do Multicalendar (Atendimento/Operação) ou do Calendário da Propriedade (Proprietário).

Payload enviada (como no código):

```python
{
  "type": "blocked",
  "checkInDate": check_in_date,
  "checkInTime": check_in_time,
  "checkOutDate": check_out_date,
  "checkOutTime": check_out_time,
  "listingId": reserv.listing.property.stays_listing_id,
  "internalNote": note
}
```

`note` é um comentário customizado, datas e horários vem do Frontend, `stays_listing_id` vem da `property_property`