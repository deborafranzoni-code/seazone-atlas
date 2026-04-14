<!-- title: Paypal | url: https://outline.seazone.com.br/doc/paypal-y0WZk4kPRh | area: Administrativo Financeiro -->

# Paypal

# **==__________________Sobre_______________________==**

## *==———Descrição———————————-==*

* API para requisição de dados

## *==———Planilha Base———————————-==*

* [00 - AdmSys Khanto](https://docs.google.com/spreadsheets/d/1L6vm5RINTTpXV-80Hih0-W2GIFoCX8jlYhflEtACguc/edit?gid=274702885#gid=274702885)
* [00 - AdmSys Seazone Serviços](https://docs.google.com/spreadsheets/d/1YHvus3u692wr75lO_SDJgYuCo6kPqcLh9VxJ5WQ7GhQ/edit?gid=274702885#gid=274702885)

## *==———Documentação———————————-==*

* [Link da Documentação](https://developer.paypal.com/api/rest/)
* Não há observação

## *==———Sugestão———————————-==*

* Não há sugestões

# **==__________________Scripts______________________==**

## ==———Requisição do Token de Acesso==

### `apiPaypalToken`

* **Objetivo**: código de requisição de token de acesso

```jsx
function apiPaypalToken() {

  /*------ Requisição do Token Paypal */ 
  var clientId = "AZxC-ksx44WM91APFy5B-lqJmTAgBxNZms18bK-jPcOXHgIhD4p-BjZZQQY4rP2lJa-8s9aqsieRdhwu"
  var clientSecret = "EK6MDgjtgBqW_42V6PXsoqLCnHjo-0njRF1KTXoVenKLCUpGSUNHs2aWQ6qlOKIqKpBUupfssH3Z_w3i"

  var optionsToken= {
    'method': 'post',
    'headers': {
      'Authorization': 'Basic ' + Utilities.base64Encode(clientId + ':' + clientSecret),
      'Content-Type': 'application/x-www-form-urlencoded'
    },
    'payload': 'grant_type=client_credentials'
  }
  
  var responseToken = UrlFetchApp.fetch(`https://api-m.paypal.com/v1/oauth2/token`, optionsToken);
  var paypalToken = JSON.parse(responseToken.getContentText())

  return `${paypalToken.token_type} ${paypalToken.access_token}`
}
```


\
## ==———Requisição de Transação==

### `apiPaypalTransaction`

* **Objetivo**: extração de dados de extrato

```javascript
function apiPaypalTransaction(){
  var today = new Date()
  var month = today.getMonth()
  var year = today.getFullYear()
  var day = today.getDate()

  var lastMonth = new Date(year,month, day-31).toISOString()
  var now = today.toISOString()

  var token = apiPaypalToken()
  
  var options= {
    'method': 'get',
    'headers': {
      'Authorization': token,
      'Content-Type': 'application/json'
    },
    'muteHttpExceptions': true
  }

  var seingPage = 0
  var lastPage = 1

  while(seingPage<=lastPage){
    var response = UrlFetchApp.fetch(`https://api-m.paypal.com/v1/reporting/transactions?start_date=${lastMonth}&end_date=${now}&fields=all&page_size=100&page=1&transaction_status=S`, options);
    var paypal = JSON.parse(response.getContentText())

    var paypalTrans = paypal.transaction_details

    if(paypalTrans){
      paypalTrans.forEach(row=> {

        
      })
    }
    
    lastPage = paypal.total_pages
    seingPage++
  }
}
```