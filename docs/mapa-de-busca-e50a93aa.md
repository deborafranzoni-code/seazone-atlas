<!-- title: Mapa de Busca | url: https://outline.seazone.com.br/doc/mapa-de-busca-7MzAdXUu1d | area: Tecnologia -->

# Mapa de Busca

> **Documentação API do Google Maps**
>
> [Começar      |  Maps Static API  |  Google for Developers](https://developers.google.com/maps/documentation/maps-static/start?hl=pt-br)

### Documentação de desenvolvimento


---

## **Tela: Resultados da Busca**

## **Feature: Mapa de Busca**

### **Descrição da feature**

Desenvolver o layout e integração para a funcionalidade de localização e visualização dos imóveis:Utilizando um serviço de localização por mapa, permitir que o hóspede visualize a localização dos imóveis retornados na página de resultados de busca e possivelmente altere a localização mediante uma área "selecionada" no mapa.

**Permissões:** Público, Usuário logado

**Rota para a página:**

* Rota padrão da pesquisa(através de um destino), antes da interação com o mapa: `/resultados-da-busca/qualquer-destino?id=&destinationName=&checkin=&checkout=&adults=1&kids=0&babies=0&page=1`
* Rota após alguma interação do usuário no mapa. **O que muda?** passa a existir a query string "location", através dessa query a função de busca passa a ser realizada por coordenadas + raio. Além de o mapa vir aberto por default: `/resultados-da-busca/qualquer-destino?id=&destinationName=&checkin=&checkout=&adults=1&kids=0&babies=0&page=1&location=-27.529834823083974%2C-48.5076789115135%2C13492.61`

### **Instruções para o usuário**

* **Visualizar MAPA**

  pode ser feito acessando a url com a query "location=lat,lng,raio", ou através do item "MAPA" na tabs da listagem de propriedades;
* **Interações MAPA**

  As interações permitidas são de drag(arrastar para navegar) e zoom desktop/mouse:
  * click+holding+arrastar para navegar
  * cmd/ctrl + scroll do mouse para zoom in/out

  mobile
  * touch+arrastar para navegar
  * touch+2 dedos para zoom in/out (ação padrão de zoom mobile)
* **Visualizar Propriedade**

  Cada propriedade retornada na busca é representada por um "marker" no mapa, com o label representando o valor por noite. Esse marker pode ser clicado, assim o usuário pode obter mais informações sobre a propriedade assim como navegar para a sua página

**Como está codado?**

* **Interações MAPA**

  A cada interação realizada de zoom ou navegação, a função **onMapChange()** (com debounce) é chamada, ela é responsável por pegar as coordenadas do ponto central visível do mapa, criar um raio que representa toda a área visível do mapa e por fim chamar a função **handleSearch()** essa que por sua vez, deve realizar uma nova busca(chamada ao bff), atualizar a query string "location" com as novas coordenadas+raio, após o sucesso dessa requisição a função de **fitbounds** é chamada para que o mapa seja centralizado de acordo com as coordenadas das propriedades retornadas na busca;
* **Busca através do formulário e paginação**

  Para buscas realizadas através do formulário e paginação, um novo parâmetro(boolean) é passado na função \*\*applyFilters() com o valor **true;**

  **Motivo?** Sempre que uma nova busca é realizada a variável "results" retornada do **useSearch()** é atualizada, com isso o mapa sofre uma "interação não humana", que seria a exibição dos markers(pontos da propriedade no mapa) e a navegação para as coordenadas da primeira propriedade retornada da busca. Com essa interação ele chama o **onMapChange()**, nessa função é que é verificado se esse parâmetro esta `true/false` através da variável **searchFromForm**, com ela verdadeira o fluxo completo de uma nova interação é "barrado", evitando assim duplicidade de chamadas e discrepância nos resultados da busca;

  **Obs**: O else seta o valor de **searchFromForm** como falso, para que caso a próxima interação no mapa seja "humana" o fluxo possa seguir corretamente;
* **eventListiner scroll / handleScroll()**

  Esse fluxo tem como objetivo observar o scroll do usuário, para que possa setar os estilos do header, lista, mapa e footer corretamente.

  **Como ele funciona?** O event listener fica ouvindo o "scroll" do usuário, e conferindo a distância do footer para o topo da área visível da página, dessa forma realizamos a seguinte regra. se a distância do footer para o topo visível da página seja maior que a altura da janela(`window.innerHeight`) significa que o footer não está visível na tela, nessa condição os elementos header, buscar, e mapa ficam com o ***position:fixed***, deixando apenas a listagem de propriedades relativa ao scroll, caso a distância do footer para o topo visível seja menor que a altura da janela, entendemos que o footer está visível, então removemos os estilos (position fixed), adicionados anteriormente para que o scroll da página aconteça normalmente, e o footer fique visível;
* **SearchContext**

  Foram adicionados novos estados a esse contexto;
  * **hasResults(boolean)**, sinaliza se o resultado da busca atual possui propriedades/resultados;
  * **openSearchMapComponent/setOpenSearchMapComponent(openMap: boolean, updateSearch: boolean)**: estado que sinaliza e altera o valor que é utilizado na condicional para exibir ou não o componente de mapa; o segundo parâmetro é utilizado para sinalizar se a busca deve ser atualizada(realizar uma nova busca sem as coordenadas) ao fechar o mapa;
  * **searchFromForm**, **setSearchFromForm(boolean)**: sinaliza se a busca foi realizada a partir de algum form de busca, ou paginação;

**APIs utilizadas:**

* /bff/properties/search

### **Como testar esta feature?** *não é necessário descrever*

### **Onde está o código?**<https://github.com/Khanto-Tecnologia/seazone-reservas-frontend/pull/97>

### **Dicas de manutenção/o que está hard coded?**

* **mapOptions:40**

  variável que controla os opcionais que vão fazer parte da instância do Maps, recomendo se basear na documento oficial do google maps api, a documentação da lib não tem nenhum info ou exemplo, sobre todos os valores possíveis de customização;
* **firstInteractions:64**

  esse valor ajuda a controlar a renderização inicial do mapa, por conta das mudanças de estado dos contextos ao chamar a função de abrir o mapa, o componente components/SearchResultComponent/index.tsx é renderizado 2x, essa variável nos ajudar a evitar que as funções que detectam interações no mapa, seja chamada a medida que o mapa é re-renderizado junto com o SearchResultComponent, evitando chamadas em duplicidade a api, e/ou caindo em possível "render hell" ou loop de renderizações;
* **Detalhar um pouco mais o funcionamento do trecho de código a seguir:**

  <https://lh6.googleusercontent.com/9RMF4tRUdOpj_O7dYSY6oNcWXJSHH6GIsvuK_qGtrkkbKR468RIg5hEBod08c2ov31cM_tgpjU9Xuji2eFPHbPVtWry5Qru0zRy2U6YMJHzwCp5-puMLdFXpwsdAvwTuko6W9fUOBA80XDncouvXiLU>

  essa lógica faz com que os estilos de posição fixa sejam adicionadas na versão desktop e mobile;
  * desktop: adiciona styles para posicionamento fixo(position fixed, posicoes(top,left,right,bottom) e z-index) ao header e ao componente de busca, além de setar no estado elementsInfo, a soma da altura do header+busca, para setar como top(margem do topo) ao elemento do mapa;
  * mobile: pega a distância do elemento da lista para o topo da página e salva no elementsInfo, para ser o top(distancia do topo) do elemento do mapa, assim ele sempre vai ficar posicionado no mesmo local da lista, cobrindo dela, por estar com o position fixed; além de remover o scroll do body, para evitar que o usuário possa rolar a tela;
  * o return da linha 250(244 no print), é para remover todos os estilos adicionados ao fechar o componente do mapa, assim evita possíveis bugs na página no formato sem o mapa;

**Obs:** foram adicionados IDs dos elementos do header, busca, footer e lista de propriedades; para que a query de select element seja mais "precisa"(imaginando que a regra de ID único seja mantida);


---

**Origem:**

[Site de Reservas | Resultados da Busca | Mapa de Busca](https://docs.google.com/document/d/1MnJZjKTrCfiXsrI1C0ws9I_u8DkSg5yzUBHFcquvGSI/edit)