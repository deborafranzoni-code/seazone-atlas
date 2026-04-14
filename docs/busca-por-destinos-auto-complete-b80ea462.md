<!-- title: Busca por Destinos (auto-complete) | url: https://outline.seazone.com.br/doc/busca-por-destinos-auto-complete-a9dvbwvXFt | area: Tecnologia -->

# Busca por Destinos (auto-complete)

**API de Destinos:**  `GET [/destinations/search](https://api.staging.reservas.sapron.com.br/docs#/destinations/search_destinations_search_get)`

* Destinos tem Tipo (Country, State, City, Neighborhood) e Titulo: Será possível inserir um Destino com titulo e tipo personalizado no futuro. Ex: Top 10 do BR
* Destinos são inseridos automaticamente com base no endereço do imóvel inserido (não existe destino onde não temos imóvel).
* Importamos todos imóveis do Sapron.
* Se um novo imóvel é inserido no Sapron, em até 30min ele vai estar no Site de Reservas.
* Com isso é criado a referencia de destinos daquele imóvel automaticamente.
* As buscas no website só vão considerar imóveis ativos.
* \
  * Estamos usando o Google Maps?

  > > Não
* Podemos buscar pelo que?

  > > País, Estado, Cidade e Bairro dos imóveis.
* Estamos buscando com base nos endereços dos nossos imóveis?

  > > Na API não retorna nada, quando não retornar nada o front exibe "Destino não encontrado"