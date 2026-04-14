<!-- title: Lançamento Invoice | url: https://outline.seazone.com.br/doc/lancamento-invoice-RWYw0Vh8OS | area: Administrativo Financeiro -->

# Lançamento Invoice

# **==__________________Sobre_______________________==**

## *==———Descrição———————————-==*

* Objetivo dessa planilha é puxar os dados do OMIE, referente aos recebimentos das OTAs, classifica-los com o Invoice das OTAs no Admsys Serviços e subir essa informação para o OMIE

## *==———Modificação——————————-==*

* Esta é a primeira versão da planilha

## *==———Histórico da Planilha———————==*

* [Lançamento Invoice](https://docs.google.com/spreadsheets/d/1lHr2ROtOtKaLvu6_-0_VSw6zpXzrF6t764g1X_sEwkY/edit?gid=474202860#gid=474202860)
* Esta é a primeira versão da planilha

# **==__________________Scripts______________________==**

## *==———==***==Passo 1 - Importação dos dados==**

### `listarContaReceber`

* **Objetivo**: puxar todos os recebimentos das OTAs, dos extratos bancários do OMIE
* **Base de Dados**
  * **API: OMIE**
    * ListarContasReceber

## *==———==***==Passo 2 - Puxar as informações de Invoice==**

### `preenchimentoInvoice`

* **Objetivo**: fazer o cruzamentos dos dados entre os valores de Invoice das OTAs, com o valor de entrada do OMIE, para identificação dos códigos de Invoice
* **Base de Dados**
  * **Sheets**
    * **Própria Planilha**
      * Ajuste de Lançamento
    * **[00 - AdmSys Seazone Serviços](https://docs.google.com/spreadsheets/d/1YHvus3u692wr75lO_SDJgYuCo6kPqcLh9VxJ5WQ7GhQ/edit?gid=274702885#gid=274702885)**
      * Entrada Airbnb
      * Entrada Booking
      * Entrada Decolar
      * Entrada Expedia

## *==———==***==Passo 3 - Imputar os dados no OMIE==**

### `envioOmie`

* **Objetivo**: enviar esses dados de invoice para o OMIE, via API, dropando na parte de descrição do OMIE
* **Base de Dados**
  * **API: OMIE**
    * AlterarContaReceber
  * **Sheets**
    * **Própria Planilha**
      * Ajuste de Lançamento