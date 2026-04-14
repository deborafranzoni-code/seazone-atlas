<!-- title: 00 - AdmSys Seazone Serviços | url: https://outline.seazone.com.br/doc/00-admsys-seazone-servicos-qmin6N8rGf | area: Administrativo Financeiro -->

# 00 - AdmSys Seazone Serviços

# **==__________________Sobre_______________________==**

## *==———Descrição———————————-==*

* Consolidação dos dados referente à Seazone Serviços

## *==———Modificação——————————-==*

* Esta é a primeira versão da planilha

## *==———Histórico da Planilha———————==*

* [00 - AdmSys Seazone Serviços](https://docs.google.com/spreadsheets/d/1YHvus3u692wr75lO_SDJgYuCo6kPqcLh9VxJ5WQ7GhQ/edit?gid=1682638089#gid=1682638089)

# **==__________________Scripts______________________==**

## ==———Importar Dados das OTA==

### `extrairDadosPlanilhasDecolarWebScript`

* **Objetivo**: importar os dados das pastas de cada conta do Decolar, geradas pelo [Colab Decolar](https://www.notion.so/Decolar-1-1ff9460c6f95807ab047e2ef5ef33644?pvs=21)
* **Observação**: para que o código funcione, estes devem ser rodados pela conta [administrativo@seazone.com.br](mailto:administrativo@seazone.com.br)
* **Base de Dados**
  * **Folder**
    * [Decolar - admseazone](https://drive.google.com/drive/folders/1RkzQkG-HVe90LvTkniLDvpFMZ33B-hSr)
    * [Decolar - admseazone2](https://drive.google.com/drive/folders/1bed3lynZI26vBoog_oTgD7ooILcPiASE)
    * [Decolar - atendseazon](https://drive.google.com/drive/folders/1zuo4TaYHystiPR1g6IpaFI7wzq96zSLJ)
    * [Decolar - atendseazon2](https://drive.google.com/drive/folders/1mPGAX9swWpir-E-gfC4HgZLG6uiHOIWI)
    * [Decolar - seazone](https://drive.google.com/drive/folders/1sNc9MWaPCUspoljHLKG2bTP5CHOzLyfQ)

### `importDataAirbnbV2`

* **Objetivo**: importar os dados de CSV do Airbnb
* **Base de Dados**
  * **Folder**
    * [02 - Airbnb](https://drive.google.com/drive/folders/1YaPmYrLy6pUeDg44fAabyc5Jey862qj_)

### `importDataBooking`

* **Objetivo**: importar os dados de CSV do Booking, justar o Payout e puxar os dados de reserva da Stays
* **Base de Dados**
  * **Folder**
    * [04 - Booking](https://drive.google.com/drive/folders/1Zad0u0A-9up9VPqePCrn91A-G9rFXQmE)
    * [06 - Stays](https://drive.google.com/drive/folders/10RDLg_zs9Eq3EMmND_k0o4qV5tEvh6y5)

### `importDataBooking2`

* **Objetivo**: importar os dados de CSV do Booking, justar o Payout e puxar os dados de reserva da Stays
* **Base de Dados**
  * **Folder**
    * [04 - Booking](https://drive.google.com/drive/folders/1Zad0u0A-9up9VPqePCrn91A-G9rFXQmE)
    * [06 - Stays](https://drive.google.com/drive/folders/10RDLg_zs9Eq3EMmND_k0o4qV5tEvh6y5)

### `faturaDecolar`

* **Objetivo**: puxar as faturas da Decolar
* **Base de Dados**
  * **Folder**
    * [Faturas](https://drive.google.com/drive/folders/1jRwnXhtauCLT3QYzopTWG5QdYKNl8MD-)
  * **Sheets**
    * **Própria Planilha**
      * Entrada Decolar

### `extrairDadosExpediaChatBox`

* **Objetivo**: extrair os dados das reservas do Expedia
* **Observação**: é necessário extrair o EPCSID do site do Expedia, manualmente. E esse código é uma API-gambiarra
* **Base de Dados**
  * **Expedia**
    * supply/experience/gateway/graphql
    * lodging/multiproperty/api/v1/user-properties?sortBy=propertyName
  * **Sheets**
    * **Própria Planilha**
      * Entrada Expedia

## ==———Invoice==

### `decolarIvoicePaymentID`

* **Objetivo**: buscar a fatura e data de pagamento
* **Observação**: é necessário extrair o **atp3** do site do Expedia, manualmente. E esse código é uma API-gambiarra
* **Base de Dados**
  * **Decolar**
    * pmp/get-liquidations-history?page=0&size=15&bookingId=
  * **Sheets**
    * **Própria Planilha**
      * Entrada Decolar

### `decolarIvoicePaymentValue`

* **Objetivo**: puxar o payout e ID de pagamento
* **Observação**: é necessário extrair o **atp3** do site do Expedia, manualmente. E esse código é uma API-gambiarra
* **Base de Dados**
  * **Decolar**
    * pmp/get-liquidations-history?page=0&size=15&bookingId=
    * pmp/payment-order-by-id?originalLiquidationId=
  * **Sheets**
    * **Própria Planilha**
      * Entrada Decolar

### `invoiceOMIE`

* **Objetivo**: fazer o match entre o Invoice imputado no OMIE e nas abas das OTAs para verificar se todos os invoices foram pagos pelas OTAs
* **Base de Dados**
  * **Sheets**
    * **Própria Planilha**
      * Entrada "Nome_OTA"

## ==———Payout==

### `apiPaypalTransaction`

* **Objetivo**: importar os dados do Paypal via API e puxar os dados de reserva via Metabase
* **Base de Dados**
  * **Paypal**
    * v1/reporting/transactions
  * **Metabase (v3)**
    * Reservation Reservation
    * Reservation OTA
    * Property Property
    * Account Guest
    * Account User
  * **Sheets**
    * **Própria Planilha**
      * Entrada Paypal

### `capturarPgtoExpediaChatBox`

* **Objetivo**: puxar os pagamentos realizados pelo Expedia
* **Observação**: é necessário extrair o **EPCSID** do site do Expedia, manualmente. E esse código é uma API-gambiarra
* **Base de Dados**
  * **Expedia**
    * lodging/accounting/getAdvancedPaymentSearchResults.json?htid=
  * **Sheets**
    * **Própria Planilha**
      * Entrada Expedia

### `expediaPgtoChatBox`

* **Objetivo**: fazer uma requisição de pagamento do Expedia
* **Observação**: é necessário extrair o EPCSID do site do Expedia, manualmente. E esse código é uma API-gambiarra
* **Base de Dados**
  * **Expedia**
    * lodging/finance/getReservationDetailsByIds.json?htid=${idImovelExpedia}&reservationIds=
  * **Sheets**
    * **Própria Planilha**
      * Entrada Expedia

### `bookingPayoutID`

* **Objetivo**: puxar o payout do booking
* **Base de Dados**
  * **Folder**
    * [Payout](https://drive.google.com/drive/folders/1mM4vIhOB_6FdMrUpzUPd3Ev4wr7IseAV)
  * **Sheets**
    * **Própria Planilha**
      * Entrada Booking

### `payOutDecolar`

* **Objetivo**: imputar os payout do Decolar
* **Base de Dados**
  * **Sheets**
    * **Própria Planilha**
      * Entrada Decolar

### `payoutExpedia`

* **Objetivo**: imputar os dados de payout
* **Base de Dados**
  * **Sheets**
    * **Própria Planilha**
      * Entrada Expedia

## ==———Suporte==

### `apiPaypalToken`

* **Objetivo**: gerar o token de acesso ao Paypal
* **Base de Dados**
  * **Paypal**
    * v1/oauth2/token

### `metabaseAllBringIDReservaCompletoStaysMetabase`

* **Objetivo**: puxar os dados de reserva de acordo com cada OTA
* **Base de Dados**
  * **Sheets**
    * **Própria Planilha**
      * Entrada "Nome_OTA"
    * **[Stays](https://docs.google.com/spreadsheets/d/1drVxVgHdmt6vClkJ0H7iLRTn9dshAPhc4xoIti5FYfg/edit?gid=0#gid=0)**
      * Stays Reservas

### `metabaseAllBringIDReserva`

* **Objetivo**: puxar os dados de reserva de acordo com cada OTA
* **Base de Dados**
  * **Metabase (v3)**
    * Reservation Reservation
    * Reservation OTA
    * Property Property
    * Account Guest
    * Account User
  * **Sheets**
    * **Própria Planilha**
      * Entrada "Nome_OTA"

### `stayAllBringProprerty`

* **Objetivo**: puxar os dados do imóvel por reserva
* **Base de Dados**
  * **Folder**
    * [06 - Stays](https://drive.google.com/drive/folders/10RDLg_zs9Eq3EMmND_k0o4qV5tEvh6y5)
  * **Sheets**
    * **Própria Planilha**
      * Entrada "Nome_OTA"

### `ajusteDecolar`

* **Objetivo**: quebrar uma entrada quando tiver mais de uma reserva paga em uma mesma linha de entrada
* **Base de Dados**
  * **Sheets**
    * **Própria Planilha**
      * Entrada Decolar
    * [Stays](https://docs.google.com/spreadsheets/d/1drVxVgHdmt6vClkJ0H7iLRTn9dshAPhc4xoIti5FYfg/edit?gid=0#gid=0)
      * **Stays Reservas**

### `ajusteBooking`

* **Objetivo**: quebrar uma entrada quando tiver mais de uma reserva paga em uma mesma linha de entrada
* **Base de Dados**
  * **Sheets**
    * **Própria Planilha**
      * Entrada Booking
    * [Stays](https://docs.google.com/spreadsheets/d/1drVxVgHdmt6vClkJ0H7iLRTn9dshAPhc4xoIti5FYfg/edit?gid=0#gid=0)
      * **Stays Reservas**

### `puxarDataPgtoBooking`

* **Objetivo**: puxar a data de pagamento do booking, nas contas bancárias
* **Base de Dados**
  * **Sheets**
    * **Própria Planilha**
      * Entrada BTG
      * Entrada Float
      * Entrada Sicred
      * Entrada Inter

### `statusPgto`

* **Objetivo**: verificar a situação dos pagamentos das OTAs
* **Base de Dados**
  * **Sheets**
    * **Própria Planilha**
      * Entrada "Nome_OTA"

### `criacaoProtestoID`

* **Objetivo**: criar o ID de protesto para reservas não recebidas
* **Base de Dados**
  * **Sheets**
    * **Própria Planilha**
      * Entrada "Nome_OTA"

### `listarContReceber`

* **Objetivo**: puxar os dados imputados no OMIE, sobre contas a receber
* **Base de Dados**
  * **OMIE**
    * ListarContasReceber

### `OmieAPI`

* **Objetivo**: gerar o token de acesso ao OMIE
* **Base de Dados**
  * **OMIE**
    * api/v1