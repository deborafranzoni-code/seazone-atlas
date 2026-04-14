<!-- title: Diário de bordo - Endereço | url: https://outline.seazone.com.br/doc/diario-de-bordo-endereco-5nFgy8Wq69 | area: Tecnologia -->

# Diário de bordo - Endereço

## Edição de endereço (endereço novo)

* Rota: `PATCH https://ssl.stays.com.br/external/v1/content/listings/:listingId`
* Payload

```json
{
  "address": {
      "additional": "integer",
      "city": "string",
      "countryCode": "string",
      "streetNumber": "integer",
      "region": "string",
      "state": "string",
      "stateCode": "string",
      "street": "string",
      "zip": "string"
    }
}  
```


## Vinculação a endereço existente

* Rota: `PATCH https://ssl.stays.com.br/external/v1/content/listings/:listingId`
* Payload

```json
{
  "_idproperty": "string",
  "_idtype": "5ab8f8a2f6b2dc2e97f97050" // apartamento,
  "address": {
      "additional": "string"
    }
}
```


* Busca de propriedades na Stays (para obtenção do _idproperty): `GET https://ssl.stays.com.br/external/v1/content/properties/:propertyId`


## Limitações

* Após vinculação à uma propriedade, não é possível remover a vinculação, apenas trocar por outro