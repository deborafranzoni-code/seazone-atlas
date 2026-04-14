<!-- title: Preço e Disponibilidade do Imóvel | url: https://outline.seazone.com.br/doc/preco-e-disponibilidade-do-imovel-s58JsqQo35 | area: Tecnologia -->

# Preço e Disponibilidade do Imóvel

### APIs

* `/properties/{property_id}/booking-price` - Retorna o preco mais atualizado passando checkin e checkout.
* `/properties/{property_id}/booking-price` - Retorna a disponibilidade mais atualizada por dia (para habilitar / desabilitar no calendario)

**OBS:** Essas apis estao indo direto na Stays. Há um pequeno cache nas chamadas pra Stays, para não ficar indo toda hora lá, visto que ir na Stays deixa mais lento.