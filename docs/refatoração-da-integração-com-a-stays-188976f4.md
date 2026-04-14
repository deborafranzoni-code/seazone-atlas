<!-- title: Refatoração da Integração com a Stays | url: https://outline.seazone.com.br/doc/refatoracao-da-integracao-com-a-stays-FrgdUhM4YT | area: Tecnologia -->

# Refatoração da Integração com a Stays

# **Atualização de Disponibilidade e Preços dos Listings**

## Rotas Utilizadas

### **GET** /external/v1/calendar/listing/{listing_id}?from={date_from}&to={date_to}

Retorna informações sobre disponibilidade, preços, restrições para determinado período.

Utilizada em:

* Worker
  * Task que atualiza a disponibilidade de preços de um listing.
* API:
  * Obtém o preço de uma reserva:
    * Na página de detalhes de um imóvel;
    * Na página de confirmar e pagar.