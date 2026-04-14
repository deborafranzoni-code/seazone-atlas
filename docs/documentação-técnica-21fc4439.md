<!-- title: Documentação Técnica | url: https://outline.seazone.com.br/doc/documentacao-tecnica-Q175LdYsU3 | area: Tecnologia -->

# Documentação Técnica

Setor Solicitante: Terrenos                                                                                                                      

Setor Responsável: Dados                                                                                                                     

Versão: 4.0                                                                                                                                              

Data: 30/01/2026

## 1. Visão Geral

O site de terrenos é uma plataforma web para visualização, análise e filtragem de terrenos que estão no BD Terrenos. Utilizando a Google Maps JavaScript API, ele apresenta um mapa interativo que exibe marcadores e polígonos que são atualizados periodicamente. A aplicação não possui um backend tradicional; em vez disso, utiliza Google Cloud Functions para processar arquivos e fornecer dados, estabelecendo a integração direta entre o BigQuery e o frontend em JavaScript. O fluxo de dados é sustentado por ferramentas de automação como N8n e Google Apps Script, que garantem atualização contínua das informações de polígonos.

### 1.1 Acesso ao site

O site de terrenos está hospedado na URL __<https://mapaterrenos.seazone.com.br/>__. Para garantir a segurança e o acesso restrito apenas a usuários que possuem o e-mail da Seazone, a plataforma utiliza o Identity-Aware Proxy (IAP) do Google Cloud, que atua como uma barreira de autenticação para que as funcionalidades da aplicação consigam ser carregadas e fiquem disponíveis para uso. Além da proteção do IAP no acesso à interface, a comunicação entre o frontend e a API do Google Cloud Function também é segura. Cada requisição do site para uma função é acompanhada por um token de autenticação, que é validado pela Cloud Function. 

*==OBS:==* A URL de desenvolvimento é <https://mapaterrenos.seazone.com.br/ambiente-dev/index_dev.html>

### 1.2 Glossário

* **Marcador (Marker):** Ícone no mapa que indica a posição de um terreno 

  \
* **Polígono:** Área colorida desenhada no mapa para representar zoneamentos, microrregiões ou regiões de interesse

  \
* **Infowindow:** Caixa de informação que aparece ao clicar em um marcador ou polígono

  \
* **KML:** Formato de arquivo para dados geoespaciais

  \
* **GeoJSON:** Formato de arquivo baseado em JSON usado para representar dados geográficos

  \

## 2. Tecnologias Utilizadas

Todo o sistema do site combina tecnologias de visualização, processamento de dados e automação para fornecer um mapa sempre atualizado.

* **Frontend:** Desenvolvido com HTML, CSS e JavaScript puro para facilitar integração com a APIs do Google Maps

  \
* **Google Maps JavaScript API:** Utilizada para exibir o mapa interativo, criar marcadores personalizados, adicionar camadas geográficas e manipular eventos de clique. (**[Documentação da API](https://developers.google.com/maps/documentation/javascript?hl=pt_BR)**)

  \
* **Google Places API:** Utilizada para possibilitar a busca de lugares e endereços desejados pelo usuário para aparição no mapa.

  \
* **Google Cloud Functions:**

  \
  **Função converter-kml:** recebe arquivos KML, converte em GeoJSON e disponibiliza para o frontend\n

  **Função bigquery-terrenos:** recebe requisições do frontend, consulta o BigQuery e retorna dados em JSON

  \
* **BigQuery:** Banco de dados responsável por armazenar as informações dos terrenos. As consultas são realizadas em tempo real pelo site por meio da cloud function bigquery-terrenos.

  \
* **Nekt:** Plataforma de inteligência de dados que recebe informações do Pipefy de Terrenos. Na Nekt, é realizada uma consulta que filtra os dados do BD Terrenos e envia para o BigQuery, garantindo sua atualização automática

  \
* **N8n:** Responsável por integrar o Google Drive ao bucket do Google Cloud. Sempre que um arquivo KML é salvo no Drive, ele é automaticamente enviado ao bucket para processamento

  \
* **Google Apps Script:** Executado no Google Drive para identificar novos arquivos KML e acionar o fluxo no N8n, garantindo que sejam enviados e processados de forma automática, sem intervenção manual

## 3. Estrutura e Funcionalidades

### 3.1 **Estrutura do Código do Site**

O site é composto por três arquivos principais que operam em conjunto:

* **index.html:** Arquivo principal que define a estrutura da página. Ele inclui a área do mapa, os campos de filtro e os controles da interface, funcionando como ponto de entrada da aplicação.

  \
* **style.css:** O arquivo responsável pelos estilos visuais, definindo o layout, cores, tipografia.

  \


* **script.js:**  Contém toda a lógica do sistema, incluindo a inicialização do mapa, a busca e manipulação dos dados, o funcionamento dos filtros e a interação dinâmica com os marcadores no mapa.

Esses arquivos estáticos (`index.html`, `style.css` e `script.js`) são hospedados no bucket [mapa-terrenos](https://console.cloud.google.com/storage/browser/mapa-terrenos?pageState=(%22StorageObjectListTable%22:(%22f%22:%22%255B%255D%22))&hl=pt-br&project=data-resources-448418) do Google Cloud Storage. 

Além disso, no bucket, existem duas pastas principais:

* **[kml_uploads](https://console.cloud.google.com/storage/browser/mapa-terrenos/kml_uploads?pageState=(%22StorageObjectListTable%22:(%22f%22:%22%255B%255D%22))&hl=pt-br&project=data-resources-448418):** responsável por receber os arquivos `.kml` enviados para o sistema.\n
* **[data](https://console.cloud.google.com/storage/browser/mapa-terrenos/data?hl=pt-br&project=data-resources-448418&pageState=(%22StorageObjectListTable%22:(%22f%22:%22%255B%255D%22))):** Pasta que armazena os arquivos em formato `GeoJSON,` resultantes da conversão dos arquivos KML, usados para carregar os dados geográficos no site.

### 3.2 Estrutura no Google Cloud Plataform

* **Frontend:** [(item 3.1](https://outline.seazone.com.br/doc/documentacao-tecnica-b0710xJs6h#h-31-estrutura-do-codigo-do-site))

  \
* **Cloud Functions:**\n O site utiliza funções na Google Cloud que operam de formas distintas:
  * **[bigquery-terrenos](https://console.cloud.google.com/run/detail/us-central1/bigquery-terrenos/observability/metrics?hl=pt-br&project=data-resources-448418):** Função que atua como API intermediária, recebendo requisições do frontend, executando consultas SQL no BigQuery e retornando os dados em JSON para o site.

    \
  * [converter-kml-terrenos](https://console.cloud.google.com/run/detail/us-central1/converter-kml-terrenos/source?hl=pt-br&project=data-resources-448418): Função dedicada ao processamento automatizado de arquivos KML, convertendo em GeoJSON para uso no Frontend. Essa função não é chamada diretamente pelo código script.js, pois faz parte do fluxo automatizado de atualização dos dados ([item 4.2](https://outline.seazone.com.br/doc/documentacao-tecnica-b0710xJs6h#h-42-atualizacao-dos-poligonos)).

    \
  * **Banco de Dados (BigQuery):**\nO BigQuery armazena todos os dados estruturados relacionados aos terrenos. A atualização do BigQuery é feita pela Nekt. As consultas são feitas exclusivamente pelas Cloud Functions, evitando acesso direto do frontend ao banco.

    \

### 3.3 Resumo do Script.js


1. **Estrutura e Variáveis Globais** 

   O código utiliza variáveis globais para gerenciar o estado da aplicação: 
   * **map, infoWindow:** Objetos principais da API Google Maps. O map representa a instância do mapa na página, enquanto o infoWindow é a janela de informações que aparece ao interagir com os marcadores.

     \
   * **todosPontos:** Array que armazena os dados de todos os terrenos consultados no BigQuery. 

     \
   * **camadasVisiveis:** Objeto booleano que controla a visibilidade das camadas GeoJSON. 

     \
   * **corPorEstudo:** Objeto para mapear tipos de estudo a cores, utilizado na estilização dos marcadores. Atualmente, segue esse padrão de cores:

     `const corPorEstudo = {
         'triagem': '#0288d1',
         'em': '#81b342',
         'ep': '#097138',
         'ap': '#ffd600',
         'lançamento': '#ff5252'
     };
     const corPadrao = '#757575';`

      \n
2. **Inicialização e Carregamento de Dados**:
   * **window.initMap():** função de inicialização assíncrona que configura a instância do mapa, a InfoWindow e os event listeners para interações globais

     \
   * **getIapToken(clientId):** Função assíncrona que utiliza a biblioteca de autenticação do Google para obter um token JWT (JSON Web Token), essencial para autorizar requisições para Cloud Function bigquery-terrenos.

     \
   * **carregarPinsDaApi():** Faz uma requisição POST para a Cloud Function bigquery-terrenos. O token IAP é enviado no cabeçalho Authorization. A resposta, contendo os dados dos terrenos, é processada para criar o array `todosPontos` e iniciar a renderização dos marcadores.

     \
   * **carregarCamadaGeoJson():** Função assíncrona dedicada a buscar arquivos GeoJSON adicioná-los como camadas de dados ao mapa.

     \
3. **Manipulação de Elementos Visuais** 
   * **criarPinElement(ponto, usarIDComoGlifo):** Função que retorna marcadores com estilização dinâmica. A cor, o ícone (glifo) e a escala são definidos com base nas propriedades do terreno (estudo_tipo). Por exemplo, os marcadores em que o último estudo é "Lançamento", o ícone (glifo) é um estrela.

     \
   * **inicializarTodosMarcadores(pontos):** cria e posiciona um `AdvancedMarkerElement` no mapa para cada terreno. Cada marcador criado recebe um event listener para o evento "click", que quando acionado exibe uma InfoWindow contendo informações detalhadas do terreno selecionado, como área, valor, etc. 

     \
   * **adicionarCamadaAoMapa(layerName)** / **removerCamadaDoMapa(layerName)**: Funções que controlam a visibilidade de camadas GeoJSON no mapa, manipulando o objeto map.data. A estilização é dinâmica e controlada pela função `aplicarFiltroDeCamadas` que define os elementos nos arquivos .geojson que devem ser lidos para colorir corretamente as camadas.

     \
   * **toggleIDs():** Altera a propriedade content de todos os marcadores, alternando entre o ícone padrão e o ID numérico do terreno.

     \

**4. Lógica de Interação e Filtros:**

* **aplicarFiltroCompleto():** A função central de filtragem. Ela coleta valores dos inputs, itera sobre `todosPontos` e ajusta a propriedade map de cada marcador, tornando-o visível ou invisível conforme as regras de filtro. 

  \
* **popularFiltrosBairroCidadeMotivo(pontos):** Popula os dropdowns de filtro com valores únicos extraídos do conjunto de dados dos terrenos, utilizando a biblioteca `Choices.js`. 

  \
* **aplicarBuscaCoordenadas():** Lê coordenadas de um input de texto, cria um marcador temporário e centraliza a visualização do mapa no ponto especificado, melhorando a experiência de navegação. 


**5. URL Dinâmica (Deep Linking):**

* **updateUrlId(id):** Atualiza a URL com o ID do terreno sem atualizar a página.

  \
* **getIdUrl():** Extrai o identificador do terreno a partir dos parâmetros da URL, permitindo o acesso direto a um imóvel específico por meio de link compartilhável.

  \
* **focusTerrenoFromUrl():** Responsável por verificar a existência de um identificador de terreno na URL e, caso presente, centralizar o mapa no imóvel correspondente, ajustando automaticamente a cidade, o zoom e o foco visual do mapa.

## 4. Fluxo e Automação de Dados

### 4.1 Atualização dos dados dos Marcadores

Os Marcadores e as informações que aparecem em seus InfoWindows estão no pipefy e segue o fluxo abaixo até chegar no site:

\n ![](/api/attachments.redirect?id=f5cdb4f6-1447-4ee9-adc1-473ee032a868 " =337x330")


A Nekt atua como uma camada de processamento de dados entre o Pipefy e o BigQuery. O fluxo funciona da seguinte forma:


1. **Entrada de Dados (Pipefy):** A Nekt recebe os dados brutos do [Pipefy de Terrenos](https://app.pipefy.com/pipes/304543320).

   \
2. **Conversão Interna (BD Terrenos):** Dentro da Nekt, esses dados são processados e convertidos em uma estrutura de dados organizada, chamada internamente de "[BD Terrenos](https://docs.google.com/spreadsheets/d/1U7E3wCKaGpMOaMlfKdnR-0L1hyBIjOTlb93f_kg6GIM/edit?gid=220134111#gid=220134111)".

   \
3. **Filtragem e Saída (Query para BigQuery):** Dentro da Nekt foi realizada uma query nesse "BD Terrenos" interno. O resultado dessa [query](https://app.nekt.ai/transformations/transformation-rz0M), que já está filtrado e formatado, é então enviado para o [BigQuery](https://console.cloud.google.com/bigquery?referrer=search&inv=1&invt=Ab5XeA&project=sandbox-439302&ws=!1m5!1m4!4m3!1ssandbox-439302!2sdados_mapa_terrenos1!3spipefy_mapa_terrenos_transformada).


:::info
Os processos 1 e 2 são de responsabilidade do setor de BizOps

:::

Dessa forma, o BigQuery não recebe os dados brutos do Pipefy, mas sim um conjunto de dados já tratados e otimizados pela Nekt, garantindo que a informação no BigQuery esteja sempre limpa e pronta para uso.


### 4.2 Atualização dos dados de Empreendimentos Concorrentes 

A atualização dos desses dados segue esse fluxo:

* A tabela "empreendimentos_concorrentes" (que está alocada dentro da base de dados "dados_mapa_terrenos" no Bigquery da GCP) é composta por dados da aba "BD - Compra e Venda" da planilha [BD Análise de Terrenos](https://docs.google.com/spreadsheets/d/1FoTFMCHLEAG3mD8Lr40qNsXsGXbb6S-pmARC7KsXZb8/edit?gid=1575790608#gid=1575790608).
* Diariamente nos horários 01h, 05h, 06h, 11h e 16h, é executada uma consulta programada que é responsável por atualizar a tabela "clean_empreendimentos_concorrentes", que além de possuir os dados limpos, ficam com os dados atualizados. 

### 4.3 Atualização dos Polígonos


 ![](/api/attachments.redirect?id=22f00504-9984-48f6-b52e-be0ccae57b35 " =688x682")

* **Interface Web:** Foi criada uma **[interface](https://script.google.com/a/macros/seazone.com.br/s/AKfycbxoXw7bt3xJOLztPD98Kvtf23vGBmqXebFBn0b_VFyilzsRAVVqjbm7vNaAcs3LEXdx/exec)** em que o setor de Terrenos consegue enviar os arquivos .kml para o drive. Ao clicar no botão "Enviar e Processar", os arquivos são enviados para o Google Drive e é acionado um script que lê os arquivos recentes e envia para o Make.

  \
* **Google Drive:** os novos arquivos enviados em .kml são armazenados na pasta de Polígonos ([link da pasta](https://drive.google.com/drive/folders/1eu6etmc6I8Nq6uSJNUxe4pPoeG_o3T1Q?hl=pt-br))

  \
* **N8n:** Esta ferramenta de automação que é acionada quando o script identifica um novo arquivo .kml no Google Drive. O N8n recebe esse novo arquivo e faz upload na pasta kml_uploads no bucket Mapa_terrenos.

  \
* **Cloud Storage (Bucket):** O arquivo KML fica armazenado na pasta kml_uploads temporariamente. Salvar o arquivo neste local serve como o gatilho da cloud function converter-kml.

  \
* **converter-kml (Cloud Function):** O salvamento do arquivo .kml no Cloud Storage aciona automaticamente esta Cloud Function. A função processa o arquivo KML, realiza a conversão para o formato GeoJSON. O arquivo GeoJSON resultante é então salvo na pasta data. Além disso, a cloud function também exclui o arquivo .kml que já foi processado.

  \
* **script.js (Frontend):** O script.js busca o arquivo GeoJSON convertido e o adiciona como uma camada de dados no mapa, permitindo que os polígonos sejam estilizados e visualizados pelo usuário.


:::info
Foi definido pelo setor de Terrenos que os arquivos de polígonos em .kml teriam esses nomes por padrão:

* Microrregiões: `Microrregioes.kml`


* Zoneamentos : `Zoneamentos.kml`
* Polígonos de Interesse: `Poligonos de Interesse.kml`

:::


\
### 4.4 Google Apps Script

[Link do Projeto no Google Apps Script](https://script.google.com/home/projects/1TekUf48ebmXFl3_lXlFttYBu1FMFGFe-WkQzHsk8pR2QHYOMIjxNtM9K/edit)

O projeto de arquivos de código pode ser encontrado dentro da pasta de [\[SZI\] Mapa Terrenos](https://drive.google.com/drive/folders/1sLY8YYNJGvu7LJKu1MZTGtffW3jvZr9w?hl=pt-br) no Google Drive, nomeado como `Mapa Terrenos (Drive <> Bucket)`. 

Dentro do projeto existem três arquivos de código com os seguintes nomes e funções:

**==Make_drive_bucket (==[==link==](https://script.google.com/u/1/home/projects/1TekUf48ebmXFl3_lXlFttYBu1FMFGFe-WkQzHsk8pR2QHYOMIjxNtM9K/edit)==): ==**

Esse é o script principal do projeto, ele monitora a pasta de Polígonos e notifica o N8n quando um novo arquivo é adicionado ou um arquivo existente é atualizado. A lógica principal está na função `processarNovosArquivos()`, que segue este fluxo:

* Define qual pasta será monitorada pelo ID da pasta e também o endereço do webhook do N8n para onde os novos arquivos serão enviados

  \
* Consulta as propriedades do usuário do script para saber a última vez que a automação rodou e percorre todos os arquivos dentro da pasta, depois ele compara a última atualização do arquivo com o horário da última execução do script. Se a data de atualização for mais recente, o arquivo é considerado novo ou atualizado.

  \
* Para cada arquivo novo/atualizado, o script envia um POST para o Webhook do N8n, passando o ID e o nome do arquivo. Isso faz com que o fluxo de automação no N8n seja ativado para processar esse arquivo. Após a execução, se algum arquivo tiver sido processado, o script salva o horário atual como o último timestamp processado, garantindo que na próxima vez ele só verifique arquivos a partir desse novo horário.

**==form.html (==[==link==](https://script.google.com/u/1/home/projects/1TekUf48ebmXFl3_lXlFttYBu1FMFGFe-WkQzHsk8pR2QHYOMIjxNtM9K/edit)==): ==**

Estrutura HTML com Javascript que cria a interface para o usuário enviar o arquivo.kml. Consiste em:\n

* **Interface com HTML e CSS:** Criam uma interface bem simples com o título "Envio de arquivo", instruções simples, um botão para selecionar um arquivo.kml e um botão para fazer o upload. 

  \
* **Processo de Upload (JavaScript):** Quando o botão "Enviar e Processar" é clicado, a função script `uploadFile()` dentro desse arquivo verifica se um novo arquivo foi selecionado. Se sim, ela lê o arquivo e converte em uma string em formato Base64.

   
* Após isso, o código usa a API `google.script.run` para chamar a função `uploadAndProcessFile()` que está em outro arquivo. Ele passa o nome do arquivo e os dados em Base64.

**==code-form:==**

Dentro desse arquivo a função `uploadAndProcessFile()` é configurada para:

* Receber o arquivo em formato Base64 que foram enviados do form.html. 


* Procurar os arquivos com o mesmo nome na pasta de destino do Google Drive e os enviar para a lixeira, evitando duplicatas. 
* Converter os dados do arquivo de volta para .kml e após isso, espera 5s com o `Utilities.sleep(5000)` para garantir que o arquivo seja salvo completamente no Google Drive. Em seguida, ela chama a função `processarNovosArquivos()` que está dentro do arquivo Make_drive_bucket. 

### 4.5 Fluxo de automação no n8n

* Responsável por integrar o Google Drive ao bucket do Google Cloud. Sempre que um arquivo KML é salvo no Drive, ele é automaticamente enviado ao bucket para processamento.

 ![fluxo na ferramenta n8n](/api/attachments.redirect?id=1ded25b1-526c-4032-8fa2-81da510841b4 " =828.5x411")

Atualmente o [fluxo no n8n](https://workflows.seazone.com.br/workflow/G9PFh7b9pczQnePw) possui os seguintes componentes:

1 — Webhook: Gatilho HTTP do workflow, permitindo que a interface criada para o usuário colocar o arquivo desejado inicie o fluxo.

2 — Download File: Usa a API do Google Drive para baixar o arquivo original. Possui autenticação via uma conta Google configurada. E mantém controle de permissões via OAuth.

3 — HTTP Request: Executa um POST direto para a API do Google Cloud Storage, usando um endpoint de upload. Também utiliza autenticação OAuth. 

4 — Condição (IF): Existe uma verificação de erro no fuxo e é aplicada uma condição. Caso o fluxo tenha algum erro, significa que é para enviar uma mensagem de erro no slack, caso contrário, o fluxo é finalizado.

5 — Slack: No slack o canal **alert-maps** recebe alertas em caso de erro no fluxo do n8n.

## 5. Links Úteis

[Github](https://github.com/seazone-tech/mapa-terrenos/tree/main)

[BD terrenos](https://docs.google.com/spreadsheets/d/1U7E3wCKaGpMOaMlfKdnR-0L1hyBIjOTlb93f_kg6GIM/edit?gid=220134111#gid=220134111)

[Pipefy de Terrenos](https://app.pipefy.com/pipes/304543320)

[Query do BD Terrenos que vai para o BigQuery](https://app.nekt.ai/transformations/transformation-rz0M)

[Documentação da configuração BigQuery <> Nekt](https://docs.nekt.com/destinations/bigquery) 

[Pasta de arquivos de Polígonos](https://drive.google.com/drive/folders/1eu6etmc6I8Nq6uSJNUxe4pPoeG_o3T1Q?hl=pt-br)

[Documentação da API do Google Maps](https://developers.google.com/maps/documentation/javascript?hl=pt_BR)

[Processo de Automação no N8n](https://outline.seazone.com.br/doc/documentacao-tecnica-Q175LdYsU3#h-42-atualizacao-dos-poligonos)

[Projeto Google Apps Script](https://script.google.com/home/projects/1TekUf48ebmXFl3_lXlFttYBu1FMFGFe-WkQzHsk8pR2QHYOMIjxNtM9K/edit)