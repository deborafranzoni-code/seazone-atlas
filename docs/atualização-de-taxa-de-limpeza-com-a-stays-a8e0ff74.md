<!-- title: Atualização de Taxa de Limpeza com a Stays | url: https://outline.seazone.com.br/doc/atualizacao-de-taxa-de-limpeza-com-a-stays-GQxXVnnaaZ | area: Tecnologia -->

# Atualização de Taxa de Limpeza com a Stays

O processo de atualização da taxa de limpeza roda no mesmo fluxo em que atualizamos a reserva.

**API usada:** `/external/v1/settings/listing/{*listing_id*}/sellprice`, dentro do body, pego o campo `fees._f_val`. Como é um array, se tiver mais de um `fees.internalName == Cleaning Fee`  é realizado a soma dos `_f_val`.

**Importante:**

O motivo para ter feito a atualização dela durante o processo que atualiza a reserva é que nesse momento vem o `listingId` que é necessário para obter a Cleaning Fee do imóvel na API da Stays. Não encontrei uma que dê pra pesquisar pelo código do imóvel.

No website, por exemplo, para fazer o sync das informações de imóveis tivemos que salvar o `listingId` de cada imóvel na tabela de properties.

**Obs:** caso a reserva seja uma extensão ou seja uma reserva em Hotel, o item `net_cleaning_fee` não será atualizado.