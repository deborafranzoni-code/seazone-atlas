<!-- title: Controle BOs e alterações de taxa de limpeza | url: https://outline.seazone.com.br/doc/controle-bos-e-alteracoes-de-taxa-de-limpeza-G9CjxAqdim | area: Administrativo Financeiro -->

# Controle BOs e alterações de taxa de limpeza

# **==__________________Sobre_______________________==**

## *==———Descrição———————————-==*

* Breve planilha que consolida os dados de BOs de reservas


## *==———Modificação——————————-==*

* Esta é a primeira versão da planilha


## *==———Histórico da Planilha———————==*

* **[Controle BOs e alterações de taxa de limpeza](https://docs.google.com/spreadsheets/d/1D44LvEO6MTzueJ65591es4CnmfvZXxR1pdP5B8v4Jcc/edit?gid=1633374478#gid=1633374478)**



---

# **==__________________Scripts______________________==**

## *==———Suporte==*

### `metabaseAllBringIDReserva`

* **Objetivo**: puxar o código da reserva
* **Base de dados:**
  * **Metabase**
    * reservation_reservation
    * reservation_ota
    * property_property
    * account_guest
    * account_user

      \
  * **Sheets**
    * [Stays](https://docs.google.com/spreadsheets/d/1drVxVgHdmt6vClkJ0H7iLRTn9dshAPhc4xoIti5FYfg/edit?gid=0#gid=0)
      * Stays Reservas
    * **Própria Planilha**
      * Controle BOs

        \

  \

### `onEdit2`

* **Objetivo**: criar lista suspensa dos nomes dos proprietários e anfitriões
* **Base de dados:**
  * **Sheets**
    * **Própria Planilha**
      * Controle BOs
      * Base culpados x motivos BOs

        \
    * **Nome da planilha, com link**
      * nome da aba


### `pmsAnfPropDataControle`

* **Objetivo**: puxar dados do imóvel, proprietário e anfitrião
* **Base de dados:**
  * **Metabase**
    * account_owner
    * account_user
    * property_property
    * account_host

      \
  * **Sheets**
    * **Própria Planilha**
      * Controle BOs

### `pmsAnfPropDataDireto`

* **Objetivo**: puxar dados do imóvel, proprietário e anfitrião
* **Base de dados:**
  * **Metabase**
    * account_owner
    * account_user
    * property_property
    * account_host

      \
  * **Sheets**
    * **Própria Planilha**
      * Controle Ajustes Diretos e Imóvel

### `calcularColT`

* **Objetivo**: código para calcular o valor da crise Seazone
* **Base de dados:**
  * **Sheets**
    * **Própria Planilha**
      * Controle BOs


### `ajustarData`

* **Objetivo**: ajustar a data
* **Base de dados:**
  * **Sheets**
    * **Própria Planilha**
      * Controle BOs

### `bringChargeBack`

* **Objetivo**: trazer as reservas com chargeback
* **Base de dados:**
  * **Sheets**
    * **Própria Planilha**
      * Chargeback

        \
    * **[Chargebacks](https://docs.google.com/spreadsheets/d/1ODzkUSnMe3GxcXMzrd8DuIvcaXnB1bS9D_9zTr8IFpw/edit?gid=1745741308#gid=1745741308)**
      * **Chargebacks**