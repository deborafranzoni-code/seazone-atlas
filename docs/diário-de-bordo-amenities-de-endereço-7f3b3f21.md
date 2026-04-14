<!-- title: Diário de bordo - Amenities de endereço | url: https://outline.seazone.com.br/doc/diario-de-bordo-amenities-de-endereco-2WJtO7QxT3 | area: Tecnologia -->

# Diário de bordo - Amenities de endereço

# Identificar um anúncio pertencente à um "endereço"

Importante notar que, no contexto da stays, existem duas entidades:

`***property***` -> Propriedade que possui anúncios agrupados em si (algum tipo de conjunto habitacional - como um condomínio, prédio ou hotel)

`***listing***` -> Um anúncio de aluguel de uma unidade de habitação (uma casa, um apartamento, uma cabana, etc...)


> Uma ***listing*** pode OU NÃO estar ligada a uma ***property***


Quando um ***listing*** está ligado a uma ***property***, na URL [https://ssl.stays.com.br/external/v1/content/listings/{id}](https://ssl.stays.com.br/external/v1/content/listings/%7Bid%7D) (que oferece detalhes de um ***listing***) pode-se notar que:

* O listing possuirá o atributo _idproperty (que identifica a property à qual ele pertence)
* Não possuirá propertyAmenities

Quando uma listing **NÃO** está ligada à uma property, no entanto, notara-se que:

* O listing NÃO possuirá o atributo _idproperty (que identifica a property à qual ele pertence)


------

Para obter dados relacionados à uma property -> [https://ssl.stays.com.br/external/v1/content/properties/{id}](https://ssl.stays.com.br/external/v1/content/properties/%7Bid%7D)

# Busca de amenities de endereço

A fim de buscar amenities de endereço, pode-se utilizar o endpoint: <https://ssl.stays.com.br/external/v1/translation/property-amenities>


# Amenities de endereço com parâmetros adicionais


\