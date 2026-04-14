<!-- title: Convenia | url: https://outline.seazone.com.br/doc/convenia-ueBE9ezVJG | area: Administrativo Financeiro -->

# Convenia

# **==__________________Sobre_______________________==**

## *==———Descrição———————————-==*

* API de requisição de dados
* Puxar os dados dos colaboradores

## *==———Planilha Base———————————-==*

* [Fechamento RH Original](https://docs.google.com/spreadsheets/d/1FQTvAXAnbNCDeU1dTgOKa9U53S_QRrXrvs9FvlI8e7k/edit?gid=1567888739#gid=1567888739)

## *==———Documentação———————————-==*

* [Link da documentação](https://docs-api.convenia.com.br/#introducao)
* Não há observação

## *==———Sugestão———————————-==*

* Não há sugestões

# **==__________________Scripts______________________==**

## ==———Dados Iniciais==

### `Main`

* **Objetivo**: dados iniciais para a requisição

```jsx
/*--------------------Convenia------------------------*/
var tokens = ["6e869686-199e-469e-947f-6d3a13540a0a", "c3f88344-49d8-49d5-958b-198d45138a03"] //Seazone Serviços e Seazone Investimentos
```

## ==———Puxar Todos os Colaboradores Ativos==

### `requisicaoAllColaborador`

* **Objetivo**: Puxar os colaboradores ativos

```jsx
function requisicaoAllColaborador(){
  var arrayCatch = [] //usando para puxar mais dados do colaborador, através do código puxarDadosColaborador()

  var optionsConvenia = {
    "method": "get",
    "headers": {
      "token": tokens[1],
      "Content-Type": "application/json"
    },
    "muteHttpExceptions": true
  }

  var pageA = 1
  var lastPageA = 1

  while (pageA <= lastPageA){
    try {
      var responseAtivo = UrlFetchApp.fetch(`https://public-api.convenia.com.br/api/v3/employees/?page=${pageA}`, optionsConvenia);
      var csvResponseAtivo = JSON.parse(responseAtivo.getContentText());
      var fullDataAtivo = csvResponseAtivo.data

      lastPageA = responseAtivo.totalPages;

      fullDataAtivo.forEach(row=> {
        arrayCatch.push([ //usado para puxar mais dados sobre o colaborador
          row.id,
        ])

      })

    } catch (error) { }

    pageA++
  }

  return arrayCatch
}
```

### `puxarDadosColaborador`

* **Objetivo**: puxar mais dados do colaborador

```jsx
function puxarDadosColaborador(){
  const batchSize = 45
  var arrayCatch = requisicaoAllColaborador()

  for (var i = 0; i < arrayCatch.length; i += batchSize) {
    var batch = arrayCatch.slice(i, i + batchSize);

    var optionsConvenia = {
      "method": "get",
      "headers": {
        "token": tokens[1],//i < totalSeaPeaple+1 ? tokens[0] : tokens[1],
        "Content-Type": "application/json"
      },
      "muteHttpExceptions": true
    };

    console.log(`Processando lote ${Math.floor(i / batchSize) + 1} com ${batch.length} registros.`);

    batch.forEach(employee => {
      var attempt = 0;
      var success = false;
      var response;

      while (!success && attempt < 5) {
        Utilities.sleep(500)

        response = UrlFetchApp.fetch(`https://public-api.convenia.com.br/api/v3/employees/${employee[0]}`, optionsConvenia);

        if (response.getResponseCode() === 200) {
          success = true;
          break;

        } else {
          Utilities.sleep(40000); // Delay para problemas de rate limit
          console.log("Erro na requisição: " + response.getContentText());
          attempt++;
        }
      }

      var employeeDetail = JSON.parse(response.getContentText());
      var fullColabData = employeeDetail.data

      if (fullColabData) {
        fullColabData.forEach(row=> {

        })
      }
    })
  }
}
```