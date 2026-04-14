<!-- title: Documentação Técnica | url: https://outline.seazone.com.br/doc/documentacao-tecnica-EN9aNh0r0Z | area: Tecnologia -->

# Documentação Técnica

# Documentação Estrutural - Fluxo

 ![](/api/attachments.redirect?id=8af4cf79-3360-43e7-ac8c-4f66bf78589f " =871x338")

O fluxo da planilha está funcionando da seguinte forma, existem três "botões" na parte de funcionalidades:

##  Seleção Automática / Seleção Manual

Caso o usuário selecione uma das duas opções, a planilha acionará a API analise_faturamento_api, hospedada no API Gateway do prd-lake. Em seguida, será invocado o Lambda responsável pelo get_listing_ids. Dentro do Lambda, uma série de manipulações será realizada utilizando as tabelas do banco de dados brlink_seazone_enriched_data. Após a execução dessas manipulações, os dados processados serão retornados à planilha e inseridos nas abas "Selecao Listings" e "Fat Selecionados".

### API

<https://528aaxbla7.execute-api.us-west-2.amazonaws.com/prod/get-listings-id>

### Lambda

<https://us-west-2.console.aws.amazon.com/lambda/home?region=us-west-2#/functions/DataLake-SorveteriaStack--DiagnosticoFaturamentoRe-hZAh2aDMDNSM?tab=code>

## Listings Localização

Caso o usuário selecione a opção, a planilha acionará a API analise_faturamento_api, hospedada no API Gateway do prd-lake. Em seguida, será invocado o Lambda responsável pelo get_listing_details. Dentro do Lambda, uma série de manipulações será realizada utilizando as tabelas do banco de dados brlink_seazone_enriched_data. Após a execução dessas manipulações, os dados processados serão retornados à planilha e inseridos na aba "Lista Localizacao".

### API

<https://528aaxbla7.execute-api.us-west-2.amazonaws.com/prod/get-details-id>

### Lambda

<https://us-west-2.console.aws.amazon.com/lambda/home?region=us-west-2#/functions/DataLake-SorveteriaStack--DiagnosticoFaturamentoDe-RC4WsdGCsrzW?tab=code>

# Documentação Estrutural - Appscript

A planilha conta com duas estruturas dentro do appscript, o código que fica dentro da planilha que defini a api que será usada e as variaveis que serão usadas na fatLib que é uma biblioteca onde está toda a obtenção dos dados e manipulação da planilha.

## FatLib

A biblioteca fatLib gerencia a interação entre o Google Apps Script e serviços Python alocados na AWS, bem como operações de manipulação e processamento de dados em planilhas. Ela encapsula funcionalidades que permitem abstrair a lógica de comunicação, criação de objetos de planilhas e outros métodos auxiliares.

**Local:** <https://script.google.com/u/0/home/projects/1IDRTeNsdksW3CIHXVLkA22g47LlVZWOZhzkebU2UiJV5Ef_y1H8LOPtk>

A biblioteca fatLib conta com 6 estruturas de código e são elas:

### **Utils.gs**

Este módulo da biblioteca fatLib fornece utilitários que auxiliam na comunicação com APIs Python hospedadas na AWS, na manipulação de dados numéricos e estatísticos, e em operações específicas para busca e organização de dados de listagens.



| Função | Descrição |
|----|----|
| **getListingsFromLake** | * **Objetivo**: 
  * Realizar uma chamada GET a uma API para obter listagens de imóveis com base em um payload.
* **Parâmetros**:
  * urlApi (**String**): URL da API.
  * accessToken (**String**): Token de acesso à API.
  * payload (**Object**): Parâmetros de consulta enviados à API.
* **Retorno**:
  * (**Object**) Resposta da API como objeto JSON.
* **Descrição**:
  * Constrói a URL com os parâmetros da payload.
  * Faz a chamada GET à API com o cabeçalho de autenticação.
  * Retorna a resposta JSON ou lança um erro se a API retornar um código diferente de 200. |
| **convertCurrencyToNumber** | * **Objetivo**: 
  * Converter um valor monetário em formato de string para um número.
* **Parâmetros**:
  * value (**String \| Number**): Valor monetário em string ou número.
* **Retorno**:
  * (**Number**) Valor convertido em número.
* **Descrição**:
  * Remove símbolos de moeda e formatações regionais, retornando o valor numérico correspondente. |
| **getPercentile** | * **Objetivo**: 
  * Calcular o percentil de um array de números.
* **Parâmetros**:
  * arr (**Array**): Array de números.
  * p (**Number**): Percentil a ser calculado (0–100).
* **Retorno**:
  * (**Number**) Valor correspondente ao percentil calculado.
* **Descrição**:
  * Ordena o array e calcula o percentil usando interpolação linear. |
| **calculateStatistics** | * **Objetivo**: 
  * Calcular estatísticas (Q1, Q3, IQR, limites inferior e superior) para identificação de outliers.
* **Parâmetros**:
  * arr (**Array**): Array de números.
  * k (**Number**): Fator de multiplicação para o cálculo dos limites.
* **Retorno**:
  * (**Object**) Objeto contendo Q1, Q3, IQR, limites inferior e superior.
* **Descrição**:
  * Calcula o primeiro e terceiro quartis.
  * Determina o intervalo interquartil (IQR) e os limites inferior e superior com base em k. |
| **getDetailsFromLake** | * **Objetivo**: 
  * Realizar uma chamada GET a uma API para obter detalhes de imóveis com base em um payload.
* **Parâmetros**:
  * urlApi (**String**): URL da API.
  * accessToken (**String**): Token de acesso à API.
  * payload (**Object**): Parâmetros de consulta enviados à API.
* **Retorno**:
  * (**Object**) Resposta da API como objeto JSON.
* **Descrição**:
  * Constrói a URL com os parâmetros da payload.
  * Faz a chamada GET à API com o cabeçalho de autenticação.
  * Retorna a resposta JSON ou lança um erro se a API retornar um código diferente de 200. |
| **getListingsIndex** | * **Objetivo**: 
  * Mapear índices de colunas específicas na resposta da API de listagens.
* **Parâmetros**:
  * searchResponse (**Object**): Resposta da API de busca de listagens.
* **Retorno**:
  * (**Object**) Objeto contendo o mapeamento de índices das colunas relevantes.
* **Descrição**:
  * Extrai os índices das colunas, como airbnb_listing_id, state, city, suburb, etc.   |
| **getDetailsIndex** | * **Objetivo**: 
  * Mapear índices de colunas específicas na resposta da API de detalhes.
* **Parâmetros**:
  * searchResponse (**Object**): Resposta da API de busca de detalhes.
* **Retorno**:
  * (**Object**) Objeto contendo o mapeamento de índices das colunas relevantes.
* **Descrição**:
  * Extrai os índices das colunas, como avg_price_year, n_months, last_review_date, etc. |
| **getFieldsWithPrefix** | * **Objetivo**: 
  * Filtrar campos de um array que começam com um prefixo específico.
* **Parâmetros**:
  * fields (**Array**): Lista de campos.
  * prefix (**String**): Prefixo a ser buscado.
* **Retorno**:
  * (**Array**) Campos que começam com o prefixo fornecido.
* **Descrição**:
  * Retorna todos os campos se o prefixo for vazio.
  * Caso contrário, retorna apenas os campos que iniciam com o prefixo. |
| **sortFieldsByYearMonth** | * **Objetivo**: 
  * Ordenar campos por ano e mês no formato ano_mes.
* **Parâmetros**:
  * fields (**Array**): Lista de campos a serem ordenados.
* **Retorno**:
  * (**Array**) Lista de campos ordenados por ano e mês.
* **Descrição**:
  * Extrai os valores ano_mes dos campos e os ordena numericamente. |


\

### **listingSheet.gs**

O módulo **listingSheet.gs** define a classe ListingsSheet, que encapsula a lógica de manipulação de dados em uma aba específica de listagens. Ele gerencia operações como buscar dados de imóveis via API, atualizar dados na planilha e realizar operações auxiliares relacionadas a IDs e receitas.

**Classe ListingsSheet:**

representa uma aba de listagens de imóveis e fornece métodos para buscar dados de APIs, limpar intervalos de dados, atualizar linhas na planilha e manipular IDs de listagens.



| Métodos | Descrição |
|----|----|
| #### **Construtor** | * **Descrição**:
  * Inicializa uma instância da classe ListingsSheet.
  * Valida o formato do intervalo de controle.
* **Parâmetros**:
  * sheetName (**String** \| **Object**): Nome da aba ou objeto da aba.
  * controlRange (**Array**): Intervalo de células no formato \[coluna inicial, linha inicial, coluna final, linha final\].
* **Exceção**:
  * Lança um erro se o intervalo não estiver no formato esperado. |
| **logToConsole** | * **Descrição**:
  * Exibe no console informações da instância atual para depuração.
* **Retorno**: void |
| #### **clear** | * **Descrição**:
  * Limpa o conteúdo e o fundo do intervalo de controle na aba associada.
* **Retorno**: void |
| **searchListings** | * **Descrição**:
  * Faz uma chamada à API para buscar IDs de listagens de imóveis com base em filtros fornecidos.
  * Atualiza os atributos dataList, indexList e revenueResponse com os resultados.
* **Parâmetros**:
  * inputList (**Object**): Dados de entrada, como estado, cidade e tipo de imóvel.
  * parameter (**Object**): Parâmetros adicionais para busca.
  * validador (**Number**): Define o modo de busca (manual ou automático).
  * urlApi (**String**): URL da API.
  * accessToken (**String**): Token de autenticação.* **Retorno**: void |
| **updateSheet** | * **Descrição**:
  * Atualiza a aba com os dados obtidos na busca, linha por linha.
  * Aplica regras de cores para destacar listagens com base em valores específicos.
* **Parâmetros**:
  * validador (**Number**): Define o modo de atualização.
* **Exceções**:
  * Lança um erro e limpa os dados da aba se não houver resultados disponíveis.
* **Retorno**: void |
| **getIdsSeparatedBy** | * **Descrição**:
  * Concatena os IDs das listagens em uma string, separados por um delimitador.
* **Parâmetros**:
  * separator (**String**): Delimitador para separar os IDs.
* **Retorno**:
  * (**String**) String contendo os IDs separados pelo delimitador. |
| **getIds** | * **Descrição**:
  * Retorna uma lista de IDs de listagens.
* **Retorno**:
  * (**Array**) Lista de IDs. |



| **Função Auxiliar** | Descrição |
|----|----|
| **newListingsSheet** | * **Descrição**:
  * Cria uma nova instância da classe ListingsSheet.
* **Parâmetros**:
  * sheetName (**String**): Nome da aba de listagens.
  * controlRange (**Array**): Intervalo de controle para a aba.
* **Retorno**:
  * (**Object**) Objeto ListingsSheet. |


\
### **inputSheet.gs**

O módulo inputSheet.gs define a classe InputSheet, que representa uma aba de entrada de dados. Essa classe gerencia a coleta, validação e preparação de dados para buscas de listagens, além de tratar campos específicos como bairros e tipos de imóveis.

**Classe InputSheet:**

A classe InputSheet encapsula a lógica de manipulação de uma aba que contém dados de entrada. Ela valida os campos fornecidos e os ajusta para serem usados em outras operações, como buscas via APIs.

| Métodos | Descrição |
|----|----|
| **Construtor** | * **Descrição**:
  * Inicializa uma instância da classe InputSheet.
  * Carrega os valores da planilha e realiza validações iniciais nos dados de entrada.
* **Parâmetros**:
  * sheetName (**String**): Nome da aba de entrada.
  * inputList (**Object**): Mapeamento de variáveis de entrada com suas respectivas células (ex.: { estado: "B10", cidade: "B11", ... }).
* **Exceção**:
  * Lança um erro se algum campo obrigatório estiver vazio. |
| **logToConsole** | * **Descrição**:
  * Exibe no console os dados de entrada carregados, útil para depuração.* **Retorno**: void |
| **loadInputVariables** | * **Descrição**:
  * Carrega os valores das células especificadas no inputList e os organiza em um objeto.
* **Parâmetros**:
  * inputList (**Object**): Mapeamento de variáveis de entrada com suas respectivas células.
* **Retorno**:
  * (**Object**) Objeto contendo os valores das variáveis de entrada, organizados por chave. |
| **validateList** | * **Descrição**:
  * Valida os campos obrigatórios e ajusta os valores conforme necessário.
  * Divide o campo de bairros (bairro) em uma lista de bairros separados por vírgula.
* **Parâmetros**:
  * inputList (**Object**): Objeto com os valores das variáveis de entrada.
* **Retorno**:
  * (**Object**) Objeto validado e ajustado.
* **Exceção**:
  * Lança um erro se algum campo obrigatório estiver vazio. |
| **getList** | * **Descrição**:
  * Retorna o objeto contendo os valores das variáveis de entrada, já validados e ajustados.
* **Retorno**:
  * (**Object**) Objeto de entrada. |



| **Função Auxiliar** | Descrição |
|----|----|
| **newInputSheet** | * **Descrição**:
  * Cria uma nova instância da classe InputSheet.
* **Parâmetros**:
  * sheetName (**String**): Nome da aba de entrada.
  * inputList (**Object**): Mapeamento de variáveis de entrada com suas respectivas células.
* **Retorno**:
  * (**Object**) Objeto InputSheet. |


\

### **revenueSheet.gs**

O módulo revenueSheet.gs define a classe RevenueSheet, que representa a aba de receitas em uma planilha. Essa classe é responsável por manipular dados de faturamento, realizar operações de limpeza, atualização e destacar outliers com base em cálculos estatísticos.

**Classe RevenueSheet:**

A classe RevenueSheet encapsula a lógica de manipulação de uma aba de receitas, incluindo a inserção de dados, cálculos, validações e destaques visuais de outliers.



|   Métodos | Descrição |
|----|----|
| **Construtor** | * **Descrição**:
  * Inicializa uma instância da classe RevenueSheet.
  * Valida o formato do intervalo de controle.
* **Parâmetros**:
  * sheetName (**String** \| **Object**): Nome da aba ou objeto da aba.
  * controlRange (**Array**): Intervalo de células no formato \[coluna inicial, linha inicial, coluna final, linha final\].
* **Exceção**:
  * Lança um erro se o intervalo não estiver no formato esperado. |
| **logToConsole** | * **Descrição**:
  * Exibe no console informações da instância atual para depuração.* **Retorno**: void |
| **clear** | * **Descrição**:
  * Limpa o conteúdo do intervalo de controle e uma coluna adicional.* **Retorno**: void |
| **setRevenueData** | * **Descrição**:
  * Define os dados de receita e os campos associados com base na resposta de uma API.
* **Parâmetros**:
  * revenueResponse (**Object**): Objeto contendo os dados e colunas de receita.* **Retorno**: void |
| **setListingsIds** | * **Descrição**:
  * Define os IDs das listagens a serem manipulados.
* **Parâmetros**:
  * ids (**Array**): Lista de IDs.* **Retorno**: void |
| **updateSheet** | * **Descrição**:
  * Atualiza a aba de receitas com os dados fornecidos, incluindo cabeçalhos, linhas de dados e cálculos de soma anual.
* **Parâmetros**:
  * prefix (**String**): Prefixo para os cálculos (não utilizado diretamente no código).* **Retorno**: void |
| **highlightOutliers** | * **Descrição**:
  * Calcula outliers com base em um fator k e destaca visualmente as células que são consideradas outliers.
  * Também permite "remover" dados com base em critérios fornecidos.
* **Parâmetros**:
  * k (**Number \| String**): Fator para cálculo de outliers ou "DESATIVADO".
  * cb (**Callback**): Callback para manipular dados (não utilizado no código).
  * remover (**String**): Indica o tipo de remoção a ser realizado.* **Retorno**: void |



| **Função Auxiliar** | Descrição |
|----|----|
| **newRevenueSheet** | * **Descrição**:
  * Cria uma nova instância da classe RevenueSheet.
* **Parâmetros**:
  * sheetName (**String**): Nome da aba de receitas.
  * controlRange (**Array**): Intervalo de controle para a aba.
* **Retorno**:
  * (**Object**) Objeto RevenueSheet. |

### **detailsSheet.gs**

O módulo detailsSheet.gs define a classe DetailsSheet, que representa a aba de detalhes em uma planilha. Essa classe é responsável por buscar dados detalhados de imóveis, manipular os dados e atualizar as informações na aba correspondente

**Classe DetailsSheet:**

A classe DetailsSheet encapsula a lógica de manipulação de uma aba de detalhes de imóveis, incluindo a busca de dados via API, a atualização da planilha com informações detalhadas e a limpeza de intervalos.



| Métodos | Descrição |
|----|----|
| **Construtor** | * **Descrição**:
  * Inicializa uma instância da classe DetailsSheet.
  * Valida o formato do intervalo de controle.
* **Parâmetros**:
  * sheetName (**String** \| **Object**): Nome da aba ou objeto da aba.
  * controlRange (**Array**): Intervalo de células no formato \[coluna inicial, linha inicial, coluna final, linha final\].
* **Exceção**:
  * Lança um erro se o intervalo não estiver no formato esperado. |
| **logToConsole** | * **Descrição**:
  * Exibe no console informações da instância atual para depuração.* **Retorno**: void |
| **clear** | * **Descrição**:
  * Limpa o conteúdo do intervalo de controle na aba associada.* **Retorno**: void |
| **searchDetails** | * **Descrição**:
  * Faz uma chamada à API para buscar IDs de detalhes de imóveis com base em filtros fornecidos.
  * Atualiza os atributos dataList e indexList com os resultados.
* **Parâmetros**:
  * inputList (**Object**): Dados de entrada, como estado, cidade e lista de bairros.
  * urlApi (**String**): URL da API.
  * accessToken (**String**): Token de autenticação.* **Retorno**: void |
| **updateSheet** | * **Descrição**:
  * Atualiza a aba de detalhes com os dados obtidos, linha por linha.
  * Adiciona links clicáveis para cada listagem do Airbnb.* **Retorno**: void |



| **Função Auxiliar** | Descrição |
|----|----|
| **newDetailsSheet** | * **Descrição**:
  * Cria uma nova instância da classe DetailsSheet.
* **Parâmetros**:
  * sheetName (**String**): Nome da aba de detalhes.
  * controlRange (**Array**): Intervalo de controle para a aba.
* **Retorno**:
  * (**Object**) Objeto DetailsSheet. |

### **parameter.gs**

O módulo parameter.gs define a classe ParameterSheet, que representa a aba de parâmetros em uma planilha. Essa classe é responsável por carregar, validar e disponibilizar os parâmetros que serão utilizados para a busca dos listings.

**Classe ParameterSheet:**

A classe ParameterSheet encapsula a lógica de manipulação de uma aba de parâmetros, incluindo o carregamento de valores definidos pelo usuário, validações de campos obrigatórios e ajuste de valores para uso posterior.



| Métodos | Descrição |
|----|----|
| **Construtor** | * **Descrição**:
  * Inicializa uma instância da classe ParameterSheet.
  * Carrega os valores da aba e realiza validações iniciais nos parâmetros.
* **Parâmetros**:
  * sheetName (**String**): Nome da aba de parâmetros.
  * parameterList (**Object**): Mapeamento de variáveis de parâmetros com suas respectivas células (ex.: { tipo: "B4", quartos: "B5", ... }).
* **Exceção**:
  * Lança um erro se algum campo obrigatório estiver vazio. |
| **logToConsole** | * **Descrição**:
  * Exibe no console os valores dos parâmetros carregados, útil para depuração.* **Retorno**: void |
| **loadInputVariables** | * **Descrição**:
  * Carrega os valores das células especificadas no parameterList e os organiza em um objeto.
* **Parâmetros**:
  * parameterList (**Object**): Mapeamento de variáveis de parâmetros com suas respectivas células.
* **Retorno**:
  * (**Object**) Objeto contendo os valores dos parâmetros. |
| **validateList** | * **Descrição**:
  * Valida os campos obrigatórios e realiza ajustes, se necessário.
* **Parâmetros**:
  * parameterList (**Object**): Objeto com os valores dos parâmetros carregados.
* **Retorno**:
  * (**Object**) Objeto validado e ajustado.
* **Exceção**:
  * Lança um erro se algum campo obrigatório estiver vazio. |
| **getList** | * **Descrição**:
  * Retorna o objeto contendo os valores dos parâmetros carregados e validados.
* **Retorno**:
  * (**Object**) Objeto de parâmetros. |



| **Função Auxiliar** | Descrição |
|----|----|
| **newParameterSheet** | * **Descrição**:
  * Cria uma nova instância da classe ParameterSheet.
* **Parâmetros**:
  * sheetName (**String**): Nome da aba de parâmetros.
    * parameterList (**Object**): Mapeamento de variáveis de parâmetros com suas respectivas células.
* **Retorno**:
  * (**Object**) Objeto ParameterSheet. |


\

## Planilha

Essa parte representa o appscript que está fora da biblioteca FatLib, ou seja, a que está presente diretamente na planilha.

O script está dividido em 6 estruturas de código e são elas

### Code.gs

O script code.gs foi desenvolvido para adicionar funcionalidades customizadas a uma planilha no Google Sheets. Ele implementa um menu personalizado e ativa ações específicas com base nas edições realizadas na planilha.



| Funções | Descrição |
|----|----|
| onOpen | * Objetivo: 
  * Adicionar um menu personalizado chamado Funcionalidades na barra de ferramentas do Google Sheets.
* Descrição:
  * O menu contém três opções:
  * Seleção Automática (aciona activateAutomation)
  * Seleção Manual (aciona activateParameter)
  * Listings Localização (aciona activateDetails)
  * Após adicionar o menu, a função também chama addStatesinDropDown para realizar uma configuração adicional. |
| onEdit | * Parâmetros:
  * e (Event): Objeto de evento que contém informações sobre a edição realizada.
* Objetivo:
  * Executar ações específicas dependendo da aba onde ocorreu a edição.
  * Função gatilho acionada automaticamente a cada edição na planilha.
* Descrição:
  * Se a edição ocorrer na aba Fat Selecionados, a função outliersButton(range) será chamada.
  * Se a edição ocorrer na aba Imoveis, a função imoveisButton(range) será chamada. |


### search_ids.gs

Este script implementa a lógica principal para a busca, filtragem e manipulação de dados de imóveis em uma planilha no Google Sheets. Ele utiliza uma biblioteca externa (fatLib) e realiza integração com APIs para buscar dados e atualizar as planilhas.



| Funções | Descrição |
|----|----|
| activateParameter | * Objetivo: 
  * Aciona a função main com o valor 0, ativando o modo de "Seleção Manual". |
| activateAutomation | * Objetivo: 
  * Aciona a função main com o valor 1, ativando o modo de "Seleção Automática". |
| activateDetails | * Objetivo: 
  * Aciona a função main com o valor 2, ativando o modo de "Listings Localização". |
| main | * Objetivo: 
  * Função principal que gerencia toda a lógica do script com base no valor do parâmetro validador. * Parâmetros: 
  * validador (Number): Define o fluxo de execução. 
    * 0: Modo "Seleção Manual". 
    * 1: Modo "Seleção Automática". 
    * 2: Modo "Listings Localização".
* Descrição:
  * Define variáveis de entrada, incluindo nomes de planilhas, intervalos de dados, e APIs usadas.
  * Cria objetos para as planilhas usando métodos da biblioteca fatLib.
  * Executa diferentes lógicas dependendo do valor de validador:
    * 0 ou 1: Limpa os dados existentes, busca novos dados da API e atualiza a planilha.
    * 2: Busca dados de localização e os atualiza na planilha correspondente.
  * Realiza pós-processamento:
    * Exibe alertas baseados no número de resultados encontrados.
    * Calcula faturamento e identifica outliers com base nos parâmetros definidos. |


\

### oneditfunctions.gs

Este script contém funções que são acionadas durante edições na planilha. As funções principais tratam de realçar outliers em uma planilha de faturamento e de popular listas de localização (estados, cidades e bairros) com base nas entradas do usuário.

| Funções | Descrição |
|----|----|
| outliersButton | * Objetivo: 
  * Realçar outliers na aba "Fat Selecionados" com base nos valores de parâmetros definidos nas células P3 e P4.
* Parâmetros:
  * range (Range): Intervalo que foi editado, usado para determinar a célula editada e o valor inserido.
* Descrição:
  * Se a célula editada for P3, o script obtém o parâmetro de outlier (k) baseado em um dicionário de valores.
  * Se a célula editada for P4, o script obtém o valor de "remover".
  * Utiliza esses parâmetros para instanciar a classe RevenueSheet (via fatLib) e chama o método highlightOutliers para identificar e marcar outliers na aba de faturamento. |
| imoveisButton | * Objetivo: 
  * Atualizar listas suspensas de cidades e bairros na aba "Imoveis" com base nos valores inseridos em B10 (estado) e B11 (cidade).
* Parâmetros:
  * range (Range): Intervalo que foi editado, usado para determinar a célula editada e o valor inserido.
* Descrição:
  * Se a célula editada for B10:
    * Carrega as listas de estados e cidades (loadLocation).
    * Obtém a lista de cidades correspondentes ao estado selecionado.
    * Atualiza o dropdown de cidades na célula B11.
  * Se a célula editada for B11:
    * Carrega as listas de estados e bairros (loadLocation).
    * Obtém a lista de bairros correspondentes à cidade selecionada.
    * Atualiza o dropdown de bairros na célula B12. |


### location.gs

Este script gerencia o carregamento, processamento e cache de dados de localização, como estados, cidades e bairros, a partir de uma planilha no Google Sheets. Ele utiliza cache para otimizar o desempenho e evitar carregamentos desnecessários.



| Funções | Descrição |
|----|----|
| loadLocation | * Objetivo: 
  * Carregar dados de localização da aba Index Imoveis e delegar o processamento ao método getLocation.
* Descrição:
  * Obtém a aba Index Imoveis e o intervalo de controle (A2:C).
  * Retorna os dados processados por getLocation. |
| getLocation | * Objetivo: 
  * Processar e armazenar dados de estados e cidades em cache para melhorar o desempenho.
* Descrição:
  * Verifica se os dados estão armazenados no cache.
  * Caso existam, os retorna sem reprocessamento.
  * Caso contrário:
    * Processa os dados em estados e cidades usando splitInLayer.
    * Divide os dados de cidades em três partes com splitObject devido a restrições de tamanho do cache.
    * Armazena os dados no cache.
  * Retorna os dados de estados e cidades. |
| splitInLayer | * Objetivo: 
  * Organizar os dados de localização em estruturas hierárquicas de estados, cidades e bairros.
* Parâmetros:
  * range (Range): Intervalo contendo os dados brutos de localização.
* Descrição:
  * Cria objetos para armazenar estados, cidades e bairros.
  * Processa cada linha para relacionar estados com cidades e cidades com bairros. |
| splitObject | * Objetivo: 
  * Dividir um objeto em três partes para adequação ao limite de tamanho do cache.
* Parâmetros:
  * obj (Object): Objeto que será dividido.
* Descrição:
  * Divide o objeto em três partes com no máximo 700 entradas cada.
  * Retorna os três objetos. |
| combineCities | * Objetivo: 
  * Combinar três objetos de cidades em um único objeto.
* Parâmetros:
  * cachedCities1, cachedCities2, cachedCities3 (String): Strings JSON representando as partes das cidades.
* Descrição:
  * Converte as strings JSON de volta para objetos.
  * Combina os objetos em um único objeto de cidades. |


### onOpenFunctions.gs

Este script contém funções acionadas na abertura da planilha ou em momentos específicos para configurar funcionalidades iniciais, como a população de listas suspensas com valores de localização.



| Funções | Descrição |
|----|----|
| addStatesinDropDown | * Objetivo: 
  * Popula a lista suspensa de estados na célula B10 da aba Imoveis.
* Descrição:
  * Carrega os dados de localização (estados e cidades) utilizando a função loadLocation.
  * Utiliza a função setStatesToDropdown para configurar a lista suspensa de estados na célula B10 da aba Imoveis. |


### utils.gs

Este script fornece funções utilitárias que auxiliam em operações comuns dentro do projeto, como configurar listas suspensas (dropdowns) em células específicas de uma planilha.



| Funções | Descrição |
|----|----|
| setStatesToDropdown | * Objetivo: 
  * Configurar uma lista suspensa (dropdown) em uma célula específica de uma aba com base em uma lista de valores.
* Parâmetros:
  * sheetName (String): Nome da aba onde a lista suspensa será configurada.
  * cell (String): Referência da célula onde será configurado o dropdown (por exemplo, "B10").
  * states (Object): Objeto contendo os valores a serem usados no dropdown (normalmente as chaves do objeto serão os valores exibidos no dropdown).
* Descrição:
  * Obtém a aba especificada pelo nome (sheetName).
  * Obtém o intervalo da célula especificada (cell).
  * Extrai as chaves do objeto states como uma lista de valores.
  * Cria uma regra de validação de dados para exigir que a célula contenha um valor da lista.
  * Aplica a regra de validação à célula. |

# Documentação Estrutural - Python

Existem duas estruturas de código dentro do lambda, chamadas get_listing_ids e get_details_id:

## get_listings_id

Este script é uma função AWS Lambda que processa requisições HTTP para buscar, filtrar e transformar dados relacionados a listagens de imóveis do Airbnb. Ele utiliza o Amazon Athena para consultar dados, aplica regras de seleção e retorna listagens formatadas e seus dados de faturamento.

### Local Lambda

* PRD-Lake

<https://us-west-2.console.aws.amazon.com/lambda/home?region=us-west-2#/functions/DataLake-SorveteriaStack--DiagnosticoFaturamentoRe-hZAh2aDMDNSM?tab=code>

### **Dependências**

* **Bibliotecas Padrão**:
  * json, os, re, unicodedata, datetime, unquote (para manipulação de strings, JSON e datas).
* **AWS**:
  * boto3: Comunicação com SNS (notificações) e Athena.
* **Pandas e NumPy**:
  * pandas: Manipulação de dados tabulares.
  * numpy: Operações numéricas.
* **AWS Wrangler**:
  * awswrangler: Integração com Athena.


### **Estrutura do CódigoEstrutura do Código**

| Funções | Descrição |
|----|----|
| **respond** | * **Descrição**: 
  * Retorna uma resposta HTTP formatada.
* **Parâmetros**:
  * code (**int**): Código HTTP.
  * body (**dict**): Corpo da resposta.* **Retorno**: 
  * (**dict**) Resposta HTTP formatada. |
| **get_normalized_sql_string** | * **Descrição**: 
  * Constrói um SQL que remove acentos, converte para minúsculo e filtra caracteres alfanuméricos.
* **Parâmetros**:
  * column (**str**): Nome da coluna.* **Retorno**: (**str**) 
  * SQL para normalização. |
| **get_normalized_python_string** | * **Descrição**: 
  * Normaliza strings em Python (remove acentos, converte para minúsculo, mantém alfanuméricos).
* **Parâmetros**:
  * raw_string (**str**): String de entrada.* **Retorno**: 
  * (**str**) String normalizada. |
| **transform_fat_from_df** | * **Descrição**: 
  * Pivoteia dados de faturamento e adiciona coluna de total anual.
* **Parâmetros**:
  * data (**pd.DataFrame**): Dados de entrada.* **Retorno**: 
  * (**pd.DataFrame**) Dados pivoteados. |
| **determine_strata** | * **Descrição**: 
  * Determina strata válidas com base na suavização.
* **Parâmetros**:
  * current (**str**): Strata atual.
  * smooth (**str**): Opção de suavização.* **Retorno**: 
  * (**list**) Lista de strata. |
| **filter_num_months_fat** | * **Descrição**: 
  * Gera filtro SQL para listar imóveis faturando pelo menos X meses.
* **Parâmetros**:
  * num_months (**int**): Número mínimo de meses de faturamento.* **Retorno**: 
  * (**str**) SQL para filtro. |
| **wait_results** | * **Descrição**: 
  * Aguarda os resultados de uma query no Athena.
* **Parâmetros**:
  * query_id (**str**): ID da query no Athena.* **Retorno**: 
  * (**pd.DataFrame**) Resultado da query. |
| **get_competitors_selected** | * **Descrição**: 
  * Monta e executa consulta no Athena com base em filtros.
* **Parâmetros**:
  * Filtros como estado, cidade, bairros, tipo de listagem, etc.* **Retorno**: 
  * (**pd.DataFrame**) Resultado da query filtrada. |
| **apply_rules** | * **Descrição**: 
  * Aplica uma regra a um conjunto de linhas em um DataFrame.
* **Parâmetros**:
  * df (**pd.DataFrame**): Dados de entrada.
  * condition (**pd.Series**): Condição booleana.
  * rule_number (**int**): Número da regra.* **Retorno**: 
  * (**pd.DataFrame**) Linhas modificadas. |
| **get_response** | * **Descrição**: 
  * Monta a resposta final para listagens e faturamento.
* **Parâmetros**:
  * body (**dict**): Parâmetros da requisição.* **Retorno**: 
  * (**dict**) Resposta formatada |
| **lambda_handler** | * **Descrição:**
  * Ponto de entrada da função Lambda.
  * Processa os parâmetros da requisição HTTP.
  * Decide entre execução manual e automática:
  * **Automática**: Busca com filtros predefinidos.
  * **Manual**: Filtros personalizados.
  * Monta a resposta final com dados de listagens e faturamento.* **Parâmetros:**
  * event (**dict**): Evento recebido pela Lambda.
  * context (**dict**): Contexto da execução.* **Retorno:**
  * (**dict**) Resposta HTTP formatada. |


## **get_details_id**

Este script é uma função AWS Lambda que processa requisições HTTP para buscar e processar dados detalhados de listagens de imóveis a partir de uma base no Athena. Ele filtra os dados com base em parâmetros  estado, cidade e bairro e retorna as informações processadas em um formato JSON.

### Local Lambda

* PRD-Lake

<https://us-west-2.console.aws.amazon.com/lambda/home?region=us-west-2#/functions/DataLake-SorveteriaStack--DiagnosticoFaturamentoDe-RC4WsdGCsrzW?tab=code>

### **Dependências**

* **Bibliotecas Padrão**:
  * json, re, unicodedata, unquote: Manipulação de strings, JSON e normalização.
* **Pandas e AWS Wrangler**:
  * pandas: Manipulação de dados tabulares.
  * awswrangler: Integração com o Athena para consultas SQL

### **Estrutura do Código**

| Funções | Descrição |
|----|----|
| **get_normalized_sql_string** | * **Descrição**: 
  * Constrói um SQL que remove acentos, converte para minúsculo e mantém apenas caracteres alfanuméricos.
* **Parâmetros**:
  * column (**str**): Nome da coluna.* **Retorno**: 
  * (**str**) SQL para normalização. |
| **get_normalized_python_string** | * **Descrição**: 
  * Normaliza strings em Python (remove acentos, converte para minúsculo e mantém apenas caracteres alfanuméricos).
* **Parâmetros**:
  * raw_string (**str**): String de entrada.* **Retorno**: 
  * (**str**) String normalizada. |
| **get_competitors_listings** | * **Descrição**: 
  * Consulta listagens no Athena com base em estado, cidade e bairros, retornando um DataFrame.
* **Parâmetros**:
  * name_state (**str**): Nome do estado.
  * name_city (**str**): Nome da cidade.
  * suburb_list (**list**): Lista de bairros.* **Retorno**: 
  * (**pd.DataFrame**) DataFrame com as listagens. |
| **build_response** | * **Descrição**: 
  * Processa os dados consultados e monta a resposta final.
* **Parâmetros**:
  * body (**dict**): Parâmetros da requisição.* **Retorno**: 
  * (**dict**) Resposta HTTP formatada. |
| **respond** | * **Descrição**: 
  * Formata uma resposta HTTP no padrão esperado.
* **Parâmetros**:
  * code (**int**): Código HTTP.
  * message (**str** \| **dict**): Mensagem ou dados do corpo da resposta.* **Retorno**: 
  * (**dict**) Resposta HTTP formatada. |
| **lambda_handler** | * **Descrição**
  * Ponto de entrada da função Lambda.
  * Processa os parâmetros da requisição, verifica sua validade e executa as consultas.
  * Monta e retorna a resposta.* **Parâmetros**
  * event (**dict**): Evento recebido pela Lambda.
  * context (**dict**): Contexto da execução. |


\
# Tutorial Deploy

A seguir será apresentado como dar deploy em uma nova atualização:

## Appscript

Quando algo novo será criado dentro da planilha, por segurança, é recomendado utilizar a planilha destinada para [dev](https://docs.google.com/spreadsheets/d/1dQFZrAknlIhi-bjzTZbxO7meLld8I5Pd0eRtRnic6vo/edit).

Com a planilha em mãos, basta clicar em "Extensões" e depois "Apps Script".

Alterações feitas fora da biblioteca FatLib, ou seja, na planilha em sí não tem a necessidade de mexer com versões, mas a FatLib sim, **mas como saber a versão que está atuando na minha planilha e como criar uma nova versão?**\nClicando na própria fatlib, irá aparecer a versão que está operando na tabela e quando se vai criar novas alterações, o recomendado é deixar no modo de desenvolvimento\n ![](/api/attachments.redirect?id=840f71f5-0c68-4bc7-a265-38d908ce5627 " =299x293")

 ![](/api/attachments.redirect?id=7365f3a0-19d0-4c6b-b77b-7dd5dd6344ce " =299x183")


Para alterar a **FatLib**, basta usar o [link](https://script.google.com/u/0/home/projects/1IDRTeNsdksW3CIHXVLkA22g47LlVZWOZhzkebU2UiJV5Ef_y1H8LOPtk) que está disponível no início do código **search_ids.gs**. Dentro da **FatLib**, você estará automaticamente no modo de desenvolvimento, o que significa que pode fazer suas alterações com tranquilidade, sem afetar a planilha de produção.

Após realizar as modificações, o processo para implementar as mudanças é simples. Siga os passos abaixo:


1. Clique no botão azul **"Implementar"**.
2. Selecione **"Nova implementação"**.
3. Clique na engrenagem ao lado de **"Selecione o tipo"** e escolha **"Biblioteca"**.
4. Descreva brevemente a alteração.
5. Clique em **"Implantar"**.

Pronto! Agora, basta voltar à planilha e seguir o processo que mencionei anteriormente para alterar a versão que estará em funcionamento com as novas alterações.


## Python

Para realizar alterações no código Python, o repositório atual está armazenado no GitHub sob o nome **pipe-lake**. Após clonar o repositório para o seu **VS Code** ou outro editor de sua preferência, siga os seguintes passos:


1. Acesse a pasta **"Sorveteria"**.
2. Lá, você encontrará os dois scripts principais: **"get_listings_id"** e **"get_details_id"**.
3. Se precisar adicionar uma nova variável de ambiente, permissões ou modificar a API criada para os dois códigos, também encontrará o arquivo **"SorveteriaStack"**. A API relevante para esses dois scripts chama-se **"analise_faturamento_api"**.

Após realizar as alterações no código, faça o **push** novamente para o Git. O **Git Actions** cuidará do processo de implantação para a AWS, onde você poderá testar localmente.

### Para testar a API, siga os passos abaixo:


1. Clique na API.
2. Clique em **"Deploy API"**.
3. Selecione um **Stage** e clique em **"Deploy"**.

Com esses passos, as URLs necessárias para extrair dados via **Apps Script** serão geradas. Lembre-se: cada vez que realizar alterações no código, será necessário executar o **Deploy** novamente para atualizar a API com as novas mudanças.

Passo a passo em prdução com imagens:

 ![](/api/attachments.redirect?id=3e5b43e7-bd50-4334-b64a-c211f6f0474e " =636x87")


---

 ![](/api/attachments.redirect?id=2c84e7b0-3f8f-41fa-ad10-0d6af584500f " =636x206")


---

 ![](/api/attachments.redirect?id=235121ab-7695-4e60-8011-b202539610aa " =337x204")


---

 ![](/api/attachments.redirect?id=174e9fcf-ea3c-45cd-8ea8-3e5f9c1166cb " =636x163")