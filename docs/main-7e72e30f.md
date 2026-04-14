<!-- title: MAIN | url: https://outline.seazone.com.br/doc/main-v7MkPHhNVm | area: Administrativo Financeiro -->

# MAIN

# **==__________________Sobre_______________________==**

## *==———Descrição———————————-==*

* Esta aba não é destinada para nenhum tipo de código, mas apenas para centralizar as variáveis utilizadas pelo código

## *==———Planilha Base———————————-==*

* Não há documentação

## *==———Documentação———————————-==*

* Não tem documentação

## *==———Sugestão———————————-==*

* Não fazer a requisição da planilha ou da aba, pois isso diminui a velocidade de execução das informações `openByID` e `getSheetsByName`

  \

# **==__________________Scripts______________________==**

## *==———Spreadsheets Atual==*

### `Main`

* **Objetivo**: Requisição base para acionamento da planilha utilizada

```jsx
/********************************* Spreadsheet Atual ***********************************/
const ssa = SpreadsheetApp.getActiveSpreadsheet();






/********************************* Variáveis de Suporte ***********************************/
const monthName = ["Janeiro","Fevereiro","Março","Abril","Maio","Junho","Julho","Agosto","Setembro","Outubro","Novembro","Dezembro"];
const monthNameAbbreviated = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];
const monthName2 = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"];
```


\
### [00 - AdmSys Seazone Serviços](https://docs.google.com/spreadsheets/d/1YHvus3u692wr75lO_SDJgYuCo6kPqcLh9VxJ5WQ7GhQ/edit?gid=274702885#gid=274702885)

### `Main`

* **Objetivo**: Requisição base para acionamento da planilha utilizada

```jsx
/********************************* Admsys Serviço ***********************************/
const admsysServicoID= "1YHvus3u692wr75lO_SDJgYuCo6kPqcLh9VxJ5WQ7GhQ";

const ssSheetsAdmsServNameAirbnb = "Entrada Airbnb"
  const entAirbnbID = 1
  const entAirbnbIDReserva = 27
  const entAirbnbReservaCode  = 26
  const entAirbnbAmount = 15;
  const entAirbnbCheckOut = 25;
  const entAirbnbCheckIn = 8
  const entAirbnbGuest = 10;
  const entAirbnbApto = 5
  const entAirbnbIDBnb = 2;
  const entAirbnbPaidOut = 3;
  const entAirbnbDate = 4;
  const entAirbnbType = 6;
  const entAirbnbCode = 7;
  const entAirbnbNights = 9;
  const entAirbnbListing = 11;
  const entAirbnbDetails = 12;
  const entAirbnbReference = 13;
  const entAirbnbCurrency = 14;
  const entAirbnbHostFee = 16;
  const entAirbnbCleaningFee = 17;
  const entAirbnbAux = 18; //Coluna que guarda os valores das datas p/ comparação
  const entAirbnbComent = 19;
  const entAirbnbFlagInter = 22
  const entAirbnbFlagSicred = 23
  const entAirbnbFlagBTG = 24
  const entAirbnbFlagFloat = 27

const ssSheetsAdmsServNameBooking = "Entrada Booking"
  const entBookingID = 1
  const entBookingIDPayout = 7
  const entBookingImovel = 2
  const entBookingHospede = 11
  const entBookingIDReservaBooking = 6
  const entBookingIDReserva = 30
  const entBookingReservaCode = 28
  const entBookingCheckOut = 10;
  const entBookingCheckIn = 9
  const entBookingAmount = 5;
  const entBookingDataPgto = 37;
  const entBookingStatus = 20;
  const entBookingObs = 27;

const ssSheetsAdmsServNameExpedia = "Entrada Expedia"
  const entExpediaID = 1
  const entExpediaIDPgto = 4
  const entExpediaImovel = 2
  const entExpediaHospede = 5
  const entExpediaIDExpedia= 13
  const entExpediaDataPgto= 22
  const entExpediaIDReserva = 26
  const entExpediaReservaCode = 6
  const entExpediaCheckOut = 8;
  const entExpediaCheckIn = 7
  const entExpediaAmount = 11;

const ssSheetsAdmsServNameDecolar = "Entrada Decolar"
  const entDecolarID = 1
  const entDecolarIDFatura = 25
  const entDecolarImovel = 8
  const entDecolarHospede = 13
  const entDecolarIDReservaDecolar = 9
  const entDecolarDataPgto = 26
  const entDecolarIDReserva = 31
  const entDecolarReservaCode = 23
  const entDecolarCheckOut = 11;
  const entDecolarCheckIn = 10
  const entDecolarAmount = 20;

const ssSheetsAdmsServNameDevolucao = "Devolucao"
  const devolHospValor = 3;
  const devolHospAtividade = 5
  const devolHospID = 13
  const devolHospResCode = 10;
  const devolHospResID = 18;
  const devolHospCheckOut = 9;
  const devolHospCheckIn = 8;
  const devolHospMotivo = 12;

const ssSheetsAdmsServNamePayPal = "Entrada PayPal"
  const entPayPalID = 1
  const entPayPalDataPgto = 10
  const entPayPalIDReserva = 24
  const entPayPalReservaCode = 5
  const entPayPalCheckOut = 7
  const entPayPalCheckIn = 6
  const entPayPalAmount = 14
  const entPayPalImovel = 2
  const entPayPalHospede = 4
  const entPayPalObs = 23
```

### [Controle CRC_2023.06.21 GKMA](https://docs.google.com/spreadsheets/d/1Q1dV4hkJqfKABiPMsYXY5sLYVVq8l1NyBBediuWqApE/edit?gid=350306181#gid=350306181)

### `main`

* **Objetivo**: dados básicos para requisição

```jsx
//-------------------------- CRC ------------------------\\
var ssIDCRC = "1Q1dV4hkJqfKABiPMsYXY5sLYVVq8l1NyBBediuWqApE"
var ssCRCNameFranquia = "REC_FRANQUIA"
  var ssCRCFranquiaIDHost = 10
  var ssCRCFranquiaReceb = 12
  var ssCRCFranquiaAbat = 13
  var ssCRCFranquiaDesc = 14
  var ssCRCFranquiaDataAbatimento = 30

var ssCRCNameImplantacao = "REC_IMPLANTAÇÃO"
  var ssCRCImplantacaoIDApto = 12
  var ssCRCImplantacaoReceb = 17
  var ssCRCImplantacaoDesc = 18
  var ssCRCImplantacaoIDAptoAbatimento = 31
```

### [9.0 - Conciliação Reservas Sapron](https://docs.google.com/spreadsheets/d/1lP2f1RLk3aV0bhwHFbHG92_ORe36NNlCmUnRg-_tIQs/edit?gid=2097081422#gid=2097081422)

### `main`

* **Objetivo**: dados básicos para requisição

```jsx
//-------------------------- Conciliação Sapron ------------------------\\
var ssConSapronNameStaysAPIMes = "API-Stays Mes"
  const ssStaysAPICanal = 3
  const ssStaysAPIID = 2

var ssConSapronNameStaysMes = "Stays Mes"
  const ssStaysMesReserva = 5
  const ssStaysMesValor = 6
  const ssStaysMesPlataforma = 2

var ssConSapronNameFech = "Conciliação Fechamento"
  var ssConSapronFechReserva = 2
  var ssConSapronFechHospedes = 3
  var ssConSapronFechCodeApto = 4
  var ssConSapronFechCheckIn = 5
  var ssConSapronFechCheckOut = 6
  var ssConSapronFechValor = 9
  var ssConSapronFechValorDiaria = 12
  var ssConSapronFechPlataforma = 17
  var ssConSapronFechIDApto = 18
  var ssConSapronFechIDHost = 19
  var ssConSapronFechIDOwner = 20
  var ssConSapronFechComisSeazone = 23
  var ssConSapronFechComisHost = 24
  
  var ssConSapronFechLimpeza = 25
  var ssConSapronFechStaysCode= 26
  var ssConSapronFechDiariaBD = 15

var ssConSapronNameFat = "Faturamento Reservas Mes"
  var ssConSapronFatReserva = 2
  var ssConSapronFatPlataforma = 5
  var ssConSapronFatValor = 10
  var ssConSapronFatIDApto = 11
  

var ssConSapronNameLimpeza = "Limpezas Mes"
  var ssConSapronLimpezaReserva = 2
  var ssConSapronLimpezaIDApto = 6
  var ssConSapronLimpezaIDHost = 7
  var ssConSapronLimpezaIDOwner = 8
  var ssConSapronLimpezaValor = 13
  var ssConSapronLimpezaPlataforma = 10
  var ssConSapronLimpezaCheckIn = 3
  var ssConSapronLimpezaCheckOut = 4
```

### [Controle BOs e alterações de taxa de limpeza](https://docs.google.com/spreadsheets/d/1D44LvEO6MTzueJ65591es4CnmfvZXxR1pdP5B8v4Jcc/edit?gid=855501021#gid=855501021)

### `main`

* **Objetivo**: dados básicos para requisição

```jsx
var ssIDControle = "1D44LvEO6MTzueJ65591es4CnmfvZXxR1pdP5B8v4Jcc"
var ssCroBONameControleBo = "Controle BOs"
  var ssCroBOControleBoDataFech = 8
  var ssCroBOControleBoDescricao = 11
  var ssCroBOControleBoAjusteProp = 17
  var ssCroBOControleBoAjusteAnf = 18
  var ssCroBOControleBoStatus = 34
  var ssCroBOControleBoHostID = 40
  var ssCroBOControleBoAptoID = 42
  var ssCroBOControleBoAptoCode = 3

var ssCroBONameAjusDireto = "Controle Ajustes Diretos e Imóvel"
  var ssCroBOAjusDiretoDataFech = 13
  var ssCroBOAjusDiretoAjusVai = 4
  var ssCroBOAjusDiretoVaiFech = 17
  var ssCroBOAjusDiretoValor = 9
  var ssCroBOAjusDescricao = 8
  var ssCroBOAjusDiretoHostID = 22
  var ssCroBOAjusDiretoAptoID = 24
  var ssCroBOAjusDiretoAptoCode = 6
```

### [04 - Conciliação futura e verificações](https://docs.google.com/spreadsheets/d/1k3fqGBd5bgsGYaRUywe69aa7qWPD22IzV_1XMwuIODA/edit?gid=128461091#gid=128461091)

### `main`

* **Objetivo**: dados básicos para requisição

```jsx
//-------------------------- Conciliação Futura ------------------------\\
var ssIDConFutura = "1k3fqGBd5bgsGYaRUywe69aa7qWPD22IzV_1XMwuIODA"
var ssConFuturaNameSaldo = "Saldos em conta props"
  var ssConFuturaSaldoIDApto = 8
  var ssConFuturaSaldoInicial = 4
  var ssConFuturaSaldoTxImplantacao = 5
  var ssConFuturaSaldoDataFech = 1
  var ssConFuturaSaldoComentario = 6
```

### [Controle CRC_2023.06.21 GKMA](https://docs.google.com/spreadsheets/d/1Q1dV4hkJqfKABiPMsYXY5sLYVVq8l1NyBBediuWqApE/edit?gid=350306181#gid=350306181)

### `main`

* **Objetivo**: dados básicos para requisição

```jsx
//-------------------------- CRC ------------------------\\
var ssIDCRC = "1Q1dV4hkJqfKABiPMsYXY5sLYVVq8l1NyBBediuWqApE"
var ssCRCNameFranquia = "REC_FRANQUIA"
  var ssCRCFranquiaIDHost = 10
  var ssCRCFranquiaReceb = 12
  var ssCRCFranquiaAbat = 13
  var ssCRCFranquiaDesc = 14
  var ssCRCFranquiaDataAbatimento = 30

var ssCRCNameImplantacao = "REC_IMPLANTAÇÃO"
  var ssCRCImplantacaoIDApto = 12
  var ssCRCImplantacaoReceb = 17
  var ssCRCImplantacaoDesc = 18
  var ssCRCImplantacaoIDAptoAbatimento = 31
```