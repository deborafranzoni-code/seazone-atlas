<!-- title: BD Comprovantes BTG | url: https://outline.seazone.com.br/doc/bd-comprovantes-btg-R9Ifgiy7lr | area: Administrativo Financeiro -->

# BD Comprovantes BTG

# **==__________________Sobre_______________________==**

## *==———Descrição———————————-==*

* Objetivo dessa planilha é fazer o match entre os dados de pagamento, com o comprovante de pagamento

## *==———Modificação——————————-==*

* Esta é a primeira versão da planilha

## *==———Histórico da Planilha———————==*

* [BD Comprovantes BTG](https://docs.google.com/spreadsheets/d/1caPjkBhi5dIXRPeWyPAQsVnsdVOI2hszZO0gCm3E8GE/edit?gid=0#gid=0)

# **==__________________Scripts______________________==**

## ==———Aba **Comprovante BTG**==

### `dadosComprovanteBTG`

* **Objetivo**: puxar os dados dos comprovantes de pagamento da Seazone Serviços
* **Base de Dados**
  * **Folder**
    * [Comprovantes_BTG_01](https://drive.google.com/drive/folders/1f4fqjBiFNI5G8D6-TUt8FLwmt9TPAByv)

### `dadosComprovanteBTGInvest`

* **Objetivo**: puxar os dados dos comprovantes de pagamento da Seazone Investimentos
* **Base de Dados**
  * **Folder**
    * [Comprovantes_BTG_01_Investimentos](https://drive.google.com/drive/folders/17M04bltd2VK8kdGw2gRurKGZjnlb38TJ)

### `ajustarDatasBTG`

* **Objetivo**: ajustar as datas do comprovante BTG
* **Base de Dados**
  * **Sheets**
    * **Própria Planilha**
      * Comprovantes BTG

## ==———Aba **Imóvel**==

### `getFechImovel`

* **Objetivo**: puxar todos os saldos positivos de repasse por imóvel
* **Base de Dados**
  * **Sheets**
    * [Compilado Fechamentos](https://docs.google.com/spreadsheets/d/1HDgd7eOk1P23zwJyzAGqR5k5cWDN4jd2kJZ87RXFi0c/edit?gid=0#gid=0)
      * Imóveis

### `puxarLinkImovel`

* **Objetivo**: fazer o match entre os dados de repasse e o comprovante de pagamento
* **Base de Dados**
  * **Sheets**
    * **Própria Planilha**
      * Comprovantes BTG
      * Repasse Imóvel

### `metabaseTEDOwner`

* **Objetivo**: fazer o match entre os dados de repasse e os lançamentos realizados no Sapron
* **Base de Dados**
  * **Metabase (v3)**
    * Financial Owner Property Ted
  * **Sheets**
    * **Própria Planilha**
      * Repasse Imóvel

### `repasseSegurado`

* **Objetivo**: fazer o match entre os dados de repasse para identificar os repasses segurados
* **Base de Dados**
  * **Sheets**
    * **Própria Planilha**
      * Repasse Imóvel
    * [04 - Conciliação futura e verificações](https://docs.google.com/spreadsheets/d/1k3fqGBd5bgsGYaRUywe69aa7qWPD22IzV_1XMwuIODA/edit?gid=128461091#gid=128461091)
      * Saldos em conta props

### `csvSapronImovelTED`

* **Objetivo**: gerar um csv com os dados de repasse de imóvel, dos imóveis, que houverepasse, e que não possuem repasse registrado no Sapron
* **Base de Dados**
  * **Sheets**
    * **Própria Planilha**
      * Repasse Imóvel

## ==———Aba **Anfitrião**==

### `getFechAnfitriao`

* **Objetivo**: puxar todos os saldos positivos de repasse do anfitrião
* **Base de Dados**
  * **Sheets**
    * [Compilado Fechamentos](https://docs.google.com/spreadsheets/d/1HDgd7eOk1P23zwJyzAGqR5k5cWDN4jd2kJZ87RXFi0c/edit?gid=0#gid=0)
      * Anfitrião

### `puxarLinkAnfitriao`

* **Objetivo**: fazer o match entre os dados de repasse e o comprovante de pagamento
* **Base de Dados**
  * **Sheets**
    * **Própria Planilha**
      * Comprovantes BTG
      * Repasse Anfitrião

### `metabaseTEDHost`

* **Objetivo**: fazer o match entre os dados de repasse e os lançamentos realizados no Sapron
* **Base de Dados**
  * **Metabase (v3)**
    * Financial Host Property Ted
  * **Sheets**
    * **Própria Planilha**
      * Repasse Anfitrião