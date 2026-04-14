<!-- title: Cálculos Importação de Reserva STAYS | url: https://outline.seazone.com.br/doc/calculos-importacao-de-reserva-stays-98YofOv0eh | area: Tecnologia -->

# Cálculos Importação de Reserva STAYS

## Chamads para Stays APIS

* **Busca informações de Reserva (reservation)**

  **Method POST**

  https://ssl.stays.com.br/external/v1/booking/reservations-export
  * Body

    ```json
    {    
    	"from": "string", // stays creation date    
    	"to": "string", // stays creation date    
    	"dateType": "string",    
    	"type": [
    		"blocked",
    		"contract",
    		"booked",
    		"maintenance",
    		"canceled"
    	]
    }
    ```
  * Response

    ```json
    [
        // ...
        {
            "_id": "string",
            "id": "string",
            "type": "string",
            "currency": "string",
            "checkInDate": "string",
            "checkOutDate": "string",
            "guestTotalCount": "float",
            "nightCount": "float",
            "creationDate": "string",
            "forwardingDate": "string",
            "pricePerNight": "float",
            "reserveTotal": "float",
            "listingInvoiceTotal": "float",
            "extraServicesTotal": "float",
            "listing": {
                "id": "string",
                "internalName": "string"
            },
            "baseAmountForwarding": "float",
            "sellPriceCorrected": "float",
            "companyCommision": "float",
            "buyPrice": "float",
            "totalForwardFee": "float",
            "client": {
                "name": "string",
                "firstName": "string",
                "lastName": "string",
                "phoneNumber": "string",
                "email": "string"
            },
            "hasReview": "bool",
            "partnerName": "string",
            "agentName": "string",
            "fee": [],
            "ownerFee": [
                {
                    "val": "float",
                    "desc": "string"
                }
            ],
            "documents": [],
            "partnerCode": "string"
        }
        // ...
    ]
    ```
* **Busca detalhes da Reserva (reservation_details)**

  **Method GET**

  https://ssl.stays.com.br/external/v1/booking/reservations/:STAYS_ID_RESERVATION
  * Response

    ```json
    {
        "_id": "string",
        "id": "string",
        "creationDate": "string",
        "checkInDate": "string",
        "checkInTime": "string",
        "checkOutDate": "string",
        "checkOutTime": "string",
        "_idlisting": "string",
        "_idclient": "string",
        "type": "string",
        "operator": {
            "_id": "string",
            "name": "string"
        },
        "price": {
            "currency": "string",
            "_f_expected": "float",
            "_f_total": "float",
            "hostingDetails": {
                "fees": [
                    {
                        "name": "string",
                        "_f_val": "float"
                    }
                ],
                "discounts": [
                    {
                        "name": "string",
                        "_f_val": "float"
                    }
                ],
                "_f_nightPrice": "float",
                "_f_total": "float"
            },
            "extrasDetails": {
                "fees": [],
                "extraServices": [],
                "discounts": [],
                "_f_total": "float"
            }
        },
        "stats": {
            "_f_totalPaid": "float"
        },
        "guests": "float",
        "guestsDetails": {},
        "partner": {},
        "internalNote": "string",
        "_idpromoCode": "string",
        "reservationUrl": "string"
    }
    ```
* **Buscar Cupom de descontos (cupom_details)**

  **Method GET**
  * Response

    ```json
    {
        "_id": "string",
        "name": "string",
        "status": "string",
        "type": "string", // percent | fixed
        "_f_discount": 10, // quando definido percent
        "_mcdiscount": { // quando definido fixed
            "BRL": "float",
            "USD": "float"
        },
        "maxUsesCount": "int",
        "maxUsesCountPerGuest": "int",
        "usedCount": "int",
        "useWithOtherPromotions": "bool",
        "periodRestrictions": {
            "enable": "bool",
            "from": "string",
            "to": "string"
        },
        "calendarRestrictions": {
            "enable": "bool",
            "validArrivalDates": {
                "from": "string",
                "to": "string"
            }
        },
        "productRestrictions": {
            "enable": "bool",
            "listingsLimit": {
                "type": "string",
                "apartments": [],
                "buildings": []
            }
        },
        "userRestrictions": {
            "enable": "bool"
        },
        "target": "string"
    }
    ```

## Variaves Sapron

* Lista de variaveis
  * `total_price`
  * `ota_fee`
  * `paid_amount`
  * `cleaning_fee_value`
  * `net_cleaning_fee`
  * `ota_comission`
  * `gross_daily_value`
  * `daily_net_value`
  * `extra_fee`
  * `manual_discount`
  * `cupom_discount`

### Metodologia para calcular cada variavel

* `total_price`

  ```python
  # Se presente no response do reservation details, puxa do _f_total
  total_price = reservation_details['price']['_f_total']
  # Se nao, usa o response de reservation
  total_price = reservation['reserveTotal']
  ```
* `night_price`

  ```python
  price_per_night = reservation["pricePerNight"]
  night_count = reservation["nightCount"]
  stays_night_price = reservation["baseAmountForwarding"]
  stays_expected_price = stays_prices["_f_expected"]
  
  calc_night_price = price_per_night * night_count
  
  # Verifica se a diference do valor calculado e o valor da stays 
  # é menor do que 1 se sim retorna o valor da stays 
  # (3 noites X 101.33 = 303.99 ao inves de 304)
  night_price_difference = abs(calc_night_price - stays_night_price)
  if calc_night_price != stays_night_price and night_price_difference < 1:
      total_night_price = stays_night_price
  
  # Verifica se a diference do valor calculado e o valor total da stays 
  # é menor do que 1, se sim retorna o valor da stays 
  # (3 noites X 101.33 = 303.99 ao inves de 304)
  # adicionado essa condição para quando o valor das 
  # diarias da stays não bate com os valores reais
  total_price_difference = abs(total_price - calc_night_price)
  if total_price != calc_night_price and total_price_difference < 1:
      total_night_price = total_price
  
  # caso nenhuma condição anterior seja verdade, 
  # verifica o valor do _f_expected
  expected_difference = abs(stays_expected_price - calc_night_price)
  if stays_expected_price != calc_night_price and expected_difference < 1:
      total_night_price = stays_expected_price
  ```
* `extra_fee`

  ```python
  total_fees = 0
  # Soma todos os valores do array `hostingDetails`
  hosting_fee = sum(
      item['_f_val'] for item in
      reservation_details['price']['hostingDetails']['fees']
  )
  # Soma todos os valores do array `extrasDetails`
  extras_fee =sum(
      item['_f_val'] for item in
      reservation_details['price']['extrasDetails']['fees']
  )
  # resultado da soma de todas as taxas
  extra_fee = hosting_fee + extras_fee
  ```
* `manual_discount`

  ```python
  # Soma todos os valores do array `discounts`
  manual_discount = sum(
      item['_f_val'] for item in
      reservation_details['price']['hostingDetails']['discounts']
  )
  ```
* `cupom_discount`

  ```python
  # Se o campo `_idpromoCode` existe no response do reservation_details
  if reservation_details["_idpromoCode"]
      # Busca detalhes do cupom
      cupom_details = stays_api.get_cupom(reservation_details["_idpromoCode"])
      # se cupom é do tipo percent
      cupom_discount = total_night_price * (cupom_details['_f_discount'] / 100)
      # se cupom é do tipo fixed
      cupom_discount = total_night_price - cupom_details['_mcdiscount']['BRL']
  ```
* `gross_daily_value`

  ```python
  # Se possui desconto manual, considera apenas ele
  if manual_discount:
      discount = manual_discount
  # se não, considera-se apenas o cupom de desconto
  # isso porque a stays tambem retorna o valor do desconto
  # de cupom no campo onde buscamos o valor de desconto manual
  else:
      discount = cupom_discount
  # A soma do valor total das diatias + taxa exta - desconto = valor bruto das diarias
  gross_daily_value = total_night_price + (extra_fee - discount)
  ```
* `cleaning_fee_value`

  ```python
  # Valor da limpeza é a diferenca entre o valor total e 
  # valor bruto das diarias
  cleaning_fee_value = total_price - gross_daily_value
  ```
* `total_paid`

  ```python
  # Se valor presente no response
  total_paid = reservation_details["stats"]["_f_totalPaid"]
  # Se não valor igual ao total da reserva
  total_paid = total_price
  ```
* `ota_comission` #1

  ```python
  # Se comissão presente no response de reservation_details
  ota_comission = reservation_details["partner"]["commission"]["_mcval"]["BRL"]
  # Se não busca informação do response de reservation
  ota_comission = sum(
      item["val"] for item in
      reservation["ownerFee"]
  )
  ```
* `ota_fee`

  ```python
  ota_name = stays_reservation.get("partnerName")
  # Se a data de criação da reserva for menor que 01/08/2023
  # aplica a taxa antiga de 10 % para a stays
  # caso contrario, aplica taxa de 15 %
  stays_creation_date = datetime.strptime(reservation["creationDate"]
  if ota_name == "Stays":
      ota_fee = 0.1
      if stays_creation_date >= datetime(2023, 8, 1, 0, 0, 0):
          ota_fee = 0.15
  # Para as outras OTAs, a `ota_fee` é o resultado da divisião entre
  # comissão e total da reserva
  else:
      ota_fee = 0.
      if ota_comission and total_price and total_price != 0:
          ota_fee = ota_comission / total_price
  ```
* `ota_comission` #2

  ```python
  # Se a comissão é igual a 0, e se `total_price` e `ota_fee`
  # possui valor, calcula-se a comissão atraves da multiplicação
  ota_comission = total_price * ota_fee
  ```
* `net_cleaning_fee`

  ```python
  # Taxa de limpeza liquida é resultado do valor bruto da limpeza
  # menos taxa da ota
  net_cleaning_fee = cleaning_fee_value * (1 - ota_fee)
  ```
* `daily_net_value`

  ```python
  daily_net_value = gross_daily_value * (1 - ota_fee)
  # Valor das diarias liquida é resultado do valor bruto da diaria
  # menos taxa da ota
  
  # Se o valor da diaria liquida for igual a 0
  # calula-se através do valor total da reserva
  if not daily_net_value:
      gross_daily_value = total_price
      daily_net_value = total_price * (1 - ota_fee)
  ```


\