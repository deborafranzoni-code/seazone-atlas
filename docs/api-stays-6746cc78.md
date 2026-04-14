<!-- title: API - Stays | url: https://outline.seazone.com.br/doc/api-stays-TOGNRE71aD | area: Administrativo Financeiro -->

# API - Stays

# **==__________________Sobre_______________________==**

## *==———Descrição———————————-==*

* Código para puxar os dados de reserva da Stays

## *==———Planilha Base———————————-==*

* [Stays](https://docs.google.com/spreadsheets/d/1drVxVgHdmt6vClkJ0H7iLRTn9dshAPhc4xoIti5FYfg/edit?gid=0#gid=0)

## *==———Documentação———————————-==*

* [Link da documentação](https://stays.net/external-api/#reservations-report-xlsx)
* Não tem documentação

## *==———Sugestão———————————-==*

* Não há sugestões

  \

# **==__________________Scripts______________________==**

## *==———Reservas==*

### `Listar Reservas` 

* **Objetivo**: listar todas as reservas de um período

```jsx
function importAPIStaysMes() {
  var row =0
  var numDia = 7

  var dashboard = fechamentoImp.getSheetByName(ssaSheetNameDashboard);
  var dataInicio =  new Date( dashboard.getRange(dashStaysInicio).getValue())
  var dataFim =  new Date(dataInicio.getFullYear(), dataInicio.getMonth(), dataInicio.getDate()+numDia)
  
  var ultimoDiaMes = new Date( dashboard.getRange(dashStaysFim).getValue())

  var numSemanas = Math.ceil((ultimoDiaMes - dataInicio)/ (1000 * 60 * 60 * 24) / numDia)

  var fechamStaysMes = fechamentoImp.getSheetByName(ssaSheetNameAPIStaysMes)
  fechamStaysMes.getRange(2,1,fechamStaysMes.getLastRow(), fechamStaysMes.getLastColumn()).clear();

  console.log(numSemanas)
  var arrayPrint = []

  while(row<numSemanas){
    var inicio = dataInicio.toISOString().split('T')[0]
    var fim = dataFim.toISOString().split('T')[0]

    console.log(row)

    var url = "https://ssl.stays.com.br/external/v1/booking/reservations-export"
    var payload = {
      "from": inicio,
      "to": fim,
      "dateType": "arrival",
      "type": ["reserved", "booked","contract"]
    }
    var options = {
      "method": "POST",
      "payload": JSON.stringify(payload),
      "headers": {
        "Authorization": "Basic MzkyZGQzYWE6NTE0Nzk1NjQ="
      },
      "contentType": "application/json"
    }

    var request = UrlFetchApp.fetch(url, options)
    var requestJSON = JSON.parse(request.getContentText())

    requestJSON.forEach((row, index)=> 
      arrayPrint.push([
        index + 2,
        row.id,
        row.partnerName,
        row.checkInDate,
        row.checkOutDate,
        row.listingInvoiceTotal,
      ])
    )

    row++ 
    dataInicio.setDate(dataInicio.getDate() + numDia+1)
    dataFim.setDate(dataInicio.getDate() + numDia)
  }

  fechamStaysMes.getRange(2,1,arrayPrint.length,arrayPrint[0].length).setValues(arrayPrint)
}
```