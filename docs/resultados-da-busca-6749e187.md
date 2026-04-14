<!-- title: Resultados da Busca | url: https://outline.seazone.com.br/doc/resultados-da-busca-Nx55Tpr8P6 | area: Tecnologia -->

# Resultados da Busca

**Conteúdos relacionados**

[Preço e Disponibilidade](/doc/preco-e-disponibilidade-mwJfSdgUAQ)


---

# Busca por imóvel

**Endpoints:** `GET /destinations/search` e `GET /properties/search` | [Doc Swagger](http://api.staging.reservas.sapron.com.br/docs)


---

Integrado os componentes de busca por imóveis (home e busca de imóvel) com as APIs de destinos (autocomplete) e busca de imóveis.

* Integrado o campo de **busca de destino** com a API `GET /destinations/search`. Este campo será um autocomplete.
* Integrado a página de **Busca de Imóveis** com API `GET /properties/search` para carregar os imóveis na página de acordo com os **destinos** escolhido pelo usuário.

‌

## **Comportamento:**

Quando o usuário selecionar um destino/localização, deverá ser obtido o ID daquele destino e passado para a API `GET /properties/search` para obter a lista de imóveis relacionadas aquele destino.

* A API vai retornar nada quando não encontrar o destino. Quando isso ocorrer deve ser exibido no seletor que o Destino informado não foi encontrado.
* Limitar visualização do seletor a 18 destinos apenas.
* Carregar na página os imóveis retornados, bem como seus preços. Os imóveis exibidos são aqueles que estão disponíveis no periodo informado. **OBS:** O preço total e de diárias está considerando a taxa de limpeza do imóvel.

### **Busca sem datas informadas**

Atualmente, para buscar, estamos utilizando a seguinte regra para trazer imóveis disponíveis:

Para cada imóvel:

* Trazer seu primeiro periodo de 5 dias disponíveis
  * Caso não possua: traz o primeiro periodo de 4 dias disponíveis
    * Caso não possua: traz o primeiro período de 3 dias disponiveis.

# **Implementação e Integração dos filtros com a API**

**Endpoint:** `GET/properties/search` | **[Doc Swagger](https://api.staging.reservas.sapron.com.br/docs#/properties/search_properties_search_get)**


---

* O próprio botão de **"Filtrar"**, quando clicado, caso não ocorra nenhuma alteração, será utilizada para fechar o modal.
* Se o usuário selecionar um filtro e após clicar em **"Filtrar"** para sair, os filtros não serão salvos.
* Os filtros só serão salvos quando usuário clicar no botão **"Aplicar Filtros"**, que deverá fechar automaticamente o modal e apresentar os resultados de pesquisa retornado pela API correspondentes aos filtros aplicados.

‌

**Filtros:**

* Faixa de preço
* Quartos, camas e banheiros
* Os demais filtros não serão implementados neste momento.

**Ordenação**

* **Recomendados:** retorno padrão, nada de especial implementado
* **Preço:** crescente e decrescente. Está sendo considerado o **preço total** para realizar a ordenação.
* Ao alterar a ordenação, automaticamente o modal que foi aberto deverá ser fechado e a ordenação aplicada aos resultados de busca.
* Ao abrir o modal de ordenação e clicar em "Ordenar" o modal deve ser fechado sem realizar alterações.

# Observações

Na busca geral de imóveis serve pra dar uma ideia muito boa do preço, mas pode não ser preciso (que é o que acontece hoje).

Uma vez que o usuário escolhe o imóvel, as outras APIs estão dizendo exatamente o valor que será cobrado (na página de Detalhes do Imóvel)

### Relacionado

[Detalhes do imóvel](/doc/detalhes-do-imovel-BaMhIIjVEk)

[Preço e Disponibilidade do Imóvel](/doc/preco-e-disponibilidade-do-imovel-gtDs2bC7ZR)