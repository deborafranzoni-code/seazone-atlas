<!-- title: Busca de imóveis | url: https://outline.seazone.com.br/doc/busca-de-imoveis-CcUAxuwgrH | area: Tecnologia -->

# Busca de imóveis

## Busca por imóvel

**Endpoints:** `GET /destinations/search` e `GET /properties/search` | [Doc Swagger](http://api.staging.reservas.sapron.com.br/docs)


---

Realizar integração dos componentes de busca por imóveis (home e busca de imóvel) com as APIs de destinos (autocomplete) e busca de imóveis.

* Integrado o campo de **busca de destino** com a API `GET /destinations/search`. Este campo será um autocomplete.
* Integrado a página de **Busca de Imóveis** com API `GET /properties/search` para carregar os imóveis na página de acordo com os **destinos** escolhido pelo usuário.

‌

**Comportamento:**

Quando o usuário selecionar um destino/localização, deverá ser obtido o ID daquele destino e passado para a API `GET /properties/search` para obter a lista de imóveis relacionadas aquele destino.

* A API vai retornar nada quando não encontrar o destino. Quando isso ocorrer deve ser exibido no seletor que o Destino informado não foi encontrado.
* Limitado visualização do seletor a 5 destinos apenas.
* Carregar na página os imóveis retornados, bem como seus preços. Os imóveis exibidos são aqueles que estão disponíveis no periodo informado.

**Observações:**

* Imóveis com status oculto (hidden) são retornado **apenas em staging.** Em produção não vai retorná-los. Isso foi feito para que a gente possa testar **imóveis de testes** que são **ocultos**.
* **Filtros:**
  * Apenas imóveis sincronizados com a stays recentemente (**3 dias**). Foi feito isso pois hoje nao estamos sabendo se um imovel foi excluido da stays (a stays parou de enviar no request). Esse filtro foi colocado pra garantir apenas imoveis que estamos pegando da stays recentemente. Logo, se a ultima sincronização dele com a stays foi há **4d**, ele não vai aparecer na busca.
  * Guest capacity no mínimo 1
  * Status = active (prod)
  * E precisa ter disponibilidade pelo menos nos proximos 120 dias

## **Implementação e Integração dos filtros com a API**

**Endpoint:** `GET/properties/search` | **[Doc Swagger](https://api.staging.reservas.sapron.com.br/docs#/properties/search_properties_search_get)**


---

* O próprio botão de **"Filtrar"**, quando clicado, caso não ocorra nenhuma alteração, será utilizada para fechar o modal.
* Se o usuário selecionar um filtro e após clicar em **"Filtrar"** para sair, os filtros não serão salvos.
* Os filtros só serão salvos quando usuário clicar no botão **"Aplicar Filtros"**, que deverá fechar automaticamente o modal e apresentar os resultados de pesquisa retornado pela API correspondentes aos filtros aplicados.

‌

**Filtros:**

Será possibilidade ao hóspede selecionar 5 tipos de segmentos de filtros que serão exibidos na seguinte ordem: 1) Preço(limites entre máximo e mínimo), 2) Comodidades, 3) Quantidade de quartos, camas e banheiros, 4) Tipo de propriedades e 5) Regras do imóvel

**Ordenação**

Possibilidades: Preço (Crescente e Decrescente), Recomendados

* Por "Preço"
  * Ao alterar a ordenação, automaticamente o modal que foi aberto deverá ser fechado e a ordenação aplicada aos resultados de busca.
  * Ao abrir o modal de ordenação e clicar em "Ordenar" o modal deve ser fechado sem realizar alterações.
* Por "Recomendados"

  No momento está retornando os imóveis normalmente, sem nenhuma regra de recomendação.