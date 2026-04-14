<!-- title: 00 - AdmSys Khanto | url: https://outline.seazone.com.br/doc/00-admsys-khanto-xUIewXatQJ | area: Administrativo Financeiro -->

# 00 - AdmSys Khanto

# **==__________________Sobre_______________________==**

## *==———Descrição———————————-==*

* Esta planilha é para consolidar os dados financeiros da Khanto


## *==———Modificação——————————-==*

* Esta é a primeira versão da planilha


## *==———Histórico da Planilha———————==*

* [00 - AdmSys Khanto](https://docs.google.com/spreadsheets/d/1L6vm5RINTTpXV-80Hih0-W2GIFoCX8jlYhflEtACguc/edit?gid=274702885#gid=274702885) (Esta é a primeira versão da planilha)



---

# **==__________________Scripts______________________==**

## *==———Importação de Dados==*

### `importDataPagme`

* **Objetivo**: importar os dados de reserva do pagarme
* **Base de dados:**
  * **Folder**
    * [02 - Pagarme](https://drive.google.com/drive/folders/1tTauFhMYh0aJkbFaWVxuKVDXsI4B-aOc)

      \
  * **Sheets**
    * **Própria Planilha**
      * Entrada Pagar.me

        \
    * **[Stays](https://docs.google.com/spreadsheets/d/1drVxVgHdmt6vClkJ0H7iLRTn9dshAPhc4xoIti5FYfg/edit?gid=0#gid=0)**
      * Stays Reservas

        \


### `importExtratoPagMe`

* **Objetivo**: importar os dados de extrato do pagarme
* **Base de dados:**
  * **Folder**
    * [02 - Pagarme](https://drive.google.com/drive/folders/1tTauFhMYh0aJkbFaWVxuKVDXsI4B-aOc)

      \
  * **Sheets**
    * **Própria Planilha**
      * Extrato Pagar.me


### `importTransacoesPgme`

* **Objetivo**: importar os dados de transação do pagarme
* **Base de dados:**
  * **Folder**
    * [02 - Pagarme](https://drive.google.com/drive/folders/1tTauFhMYh0aJkbFaWVxuKVDXsI4B-aOc)

      \
  * **Sheets**
    * **Própria Planilha**
      * Entrada Pagar.me

        \

### `entradaPagarme`Desativado

* **Objetivo**: importar os dados do pagarme
* **Base de dados:**
  * **Folder**
    * [02 - Pagarme](https://drive.google.com/drive/folders/1tTauFhMYh0aJkbFaWVxuKVDXsI4B-aOc)

      \
  * **Sheets**
    * **Própria Planilha**
      * Entrada Pagar.me

        \
    * **[Stays](https://docs.google.com/spreadsheets/d/1drVxVgHdmt6vClkJ0H7iLRTn9dshAPhc4xoIti5FYfg/edit?gid=0#gid=0)**
      * Stays Reservas

        \

### `importExtratoSicred`

* **Objetivo**: importar os dados de extrato do sicred
* **Base de dados:**
  * **Folder**
    * [01 - Extratos Bancários](https://drive.google.com/drive/folders/1Usu6KJpVSUn6-ieA6cPHyLQGu_K6v5Ib)

      \
  * **Sheets**
    * **Própria Planilha**
      * Extrato Sicred


### `preenchimentoInvoice`

* **Objetivo**: preencher os invoice na Entrada Khanto Reservas
* **Base de dados:**
  * **Sheets**
    * **Própria Planilha**
      * Extrato Pagar.me
      * Entrada Khanto Reservas


### `importExtratoASAAS` Desativado

* **Objetivo**: importar o Extrato do ASAAS
* **Base de dados:**
  * **Folder**
    * [07 - ASAAS](https://drive.google.com/drive/folders/1EeTJLap3Cfq9drxnAW-lBXvsvWsXk_yE)

      \
  * **Sheets**
    * **Própria Planilha**
      * Extrato ASAAS


### `importASAAS` Desativado

* **Objetivo**: importar dados do ASAAS
* **Base de dados:**
  * **Metabase**
    * Reservation Reservation
    * Reservation OTA
    * Property Property
    * Account Guest
    * Account User

      \
  * **Folder**
    * [07 - ASAAS](https://drive.google.com/drive/folders/1EeTJLap3Cfq9drxnAW-lBXvsvWsXk_yE)

      \
  * **Input Manual**
    * breve descrição do input manual

      \
  * **Sheets**
    * **Própria Planilha**
      * Entrada ASAAS

        \
    * **[Stays](https://docs.google.com/spreadsheets/d/1drVxVgHdmt6vClkJ0H7iLRTn9dshAPhc4xoIti5FYfg/edit?gid=0#gid=0)**
      * Stays Reservas

        \
    * **[Taxas Asaas Cartão](https://docs.google.com/spreadsheets/d/1SFDCKB7VAv-8mbBC391GBectB-DKqLivqb2ysIZUp5o/edit?gid=0#gid=0)**
      * **Sheet1**


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


\
### `importBTGExtrato`

* **Objetivo**: importar os dados de extrato, entrada e saída do BTG
* **Base de dados:**
  * **Folder**
    * [10 - BTG](https://drive.google.com/drive/folders/1RWO5oW_jy6q9AmNH3j5b6luS5R8hMgFh)

      \
  * **Sheets**
    * **Própria Planilha**
      * Extrato BTG
      * Entrada BTG
      * Saída BTG

        \

### `importItauExtrato`

* **Objetivo**: importar os dados de extrato, entrada e saída do Itaú
* **Base de dados:**
  * **Folder**
    * [09 - Itaú](https://drive.google.com/drive/folders/1kRWGSJOLUtp8709TBjGnANNzir5zy-uK)

      \
  * **Sheets**
    * **Própria Planilha**
      * Extrato Itaú
      * Entrada Itaú
      * Saída Itaú

### `importExtratoTuna3`

* **Objetivo**: importar os dados de extrato da tuna
* **Base de dados:**
  * **Folder**
    * [Tuna - Atendimento](https://drive.google.com/drive/folders/1GHraql4lB2AqI13ndjHHhPRCNtYXHR7s)

      \
  * **Sheets**
    * **Própria Planilha**
      * Extrato Tuna

        \

### `importTuna2`

* **Objetivo**: importar os dados de extrato da tuna
* **Base de dados:**
  * **Folder**
    * [Tuna - Atendimento](https://drive.google.com/drive/folders/1GHraql4lB2AqI13ndjHHhPRCNtYXHR7s)

      \
  * **Sheets**
    * **Própria Planilha**
      * Extrato Tuna

        \
    * **[Stays](https://docs.google.com/spreadsheets/d/1drVxVgHdmt6vClkJ0H7iLRTn9dshAPhc4xoIti5FYfg/edit?gid=0#gid=0)**
      * Stays Reservas

        \
    * **[Taxas Asaas Cartão](https://docs.google.com/spreadsheets/d/1SFDCKB7VAv-8mbBC391GBectB-DKqLivqb2ysIZUp5o/edit?gid=0#gid=0)**
      * **Sheet1**

## ==———Suporte==

### `apiPaypalToken`

* **Objetivo**: gerar o token de acesso ao Paypal
* **Base de Dados**
  * **Paypal**
    * v1/oauth2/token


### `stayReservationData`

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