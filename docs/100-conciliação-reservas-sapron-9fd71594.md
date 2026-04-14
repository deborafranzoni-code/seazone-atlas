<!-- title: 10.0 - Conciliação Reservas Sapron | url: https://outline.seazone.com.br/doc/100-conciliacao-reservas-sapron-ozs22TPYKi | area: Administrativo Financeiro -->

# 10.0 - Conciliação Reservas Sapron

# **==__________________Sobre_______________________==**

## *==———Descrição———————————-==*

* Esta planilha tem como objetivo conciliar os dados do Sapron, com os CSVs das OTA


## *==———Modificação——————————-==*

* Otimização dos códigos de requisição de dados do Metabase


## *==———Histórico da Planilha———————==*

* **[10.0 - Conciliação Reservas Sapron](https://docs.google.com/spreadsheets/d/1fbeqpusr2c2_wROOmLrDVAGxKMpo15MOrG1dPflrTFU/edit?gid=1748321476#gid=1748321476)**
* [8.0 - Conciliação Reservas Sapron](https://www.notion.so/8-0-Concilia-o-Reservas-Sapron-2009460c6f9580f0aedcd0a4de761065?pvs=21)
* [8.1 - Conciliação Reservas Sapron](https://www.notion.so/8-1-Concilia-o-Reservas-Sapron-2009460c6f95801ebbd1ffee4ff0caf9?pvs=21)
* [9.0 - Conciliação Reservas Sapron](https://www.notion.so/9-0-Concilia-o-Reservas-Sapron-2009460c6f958070bd8cf597acd67c7c?pvs=21)

  \



---

# **==__________________Scripts______________________==**

## *==———Etapa 1: importação de todos os dados utilizados na conciliação==*

### `importReservaMes`

* **Objetivo**: puxar os dados das reservas do Sapron, para o sheets
* **Base de dados:**
  * **Metabase (v3)**
    * Closing Seazone Resume
    * Reservation Reservation
    * Reservation Ota
    * Property Property
    * Account Guest
    * Account User
    * Property Property Owners
    * Financial Reservation Manual Fit
    * Financial Cleaning Fee Manual Fit


\
### `importDevolucao`

* **Objetivo**: puxar os dados referente aos ajustes de reserva
* **Base de dados:**
  * **Input Manual**
    * Algumas informações são imputadas manualmente pelo time de fechamento

      \
  * **Sheets**
    * [00 - AdmSys Seazone Serviços](https://docs.google.com/spreadsheets/d/1YHvus3u692wr75lO_SDJgYuCo6kPqcLh9VxJ5WQ7GhQ/edit?gid=362456799#gid=362456799)
      * Devolucao

        \
    * [Controle BOs e alterações de taxa de limpeza](https://docs.google.com/spreadsheets/d/1D44LvEO6MTzueJ65591es4CnmfvZXxR1pdP5B8v4Jcc/edit?gid=855501021#gid=855501021)
      * Controle BOs


### `importAirbnbMes`

* **Objetivo**: puxar os dados referente as reservas do Airtbnb, de acordo com o fechamento
* **Base de dados:**
  * **Sheets**
    * [00 - AdmSys Seazone Serviços](https://docs.google.com/spreadsheets/d/1YHvus3u692wr75lO_SDJgYuCo6kPqcLh9VxJ5WQ7GhQ/edit?gid=362456799#gid=362456799)
      * Entrada Airbnb

        \

### `importBookingMes`

* **Objetivo**: puxar os dados referente as reservas do Booking, de acordo com o fechamento
* **Base de dados:**
  * **Sheets**
    * [00 - AdmSys Seazone Serviços](https://docs.google.com/spreadsheets/d/1YHvus3u692wr75lO_SDJgYuCo6kPqcLh9VxJ5WQ7GhQ/edit?gid=362456799#gid=362456799)
      * Entrada Booking

        \

### `importDecolarMes`

* **Objetivo**: puxar os dados referente as reservas do Decolar, de acordo com o fechamento
* **Base de dados:**
  * **Sheets**
    * [00 - AdmSys Seazone Serviços](https://docs.google.com/spreadsheets/d/1YHvus3u692wr75lO_SDJgYuCo6kPqcLh9VxJ5WQ7GhQ/edit?gid=362456799#gid=362456799)
      * Entrada Decolar

        \

### `importExpediaMes`

* **Objetivo**: puxar os dados referente as reservas do Expedia, de acordo com o fechamento
* **Base de dados:**
  * **Sheets**
    * [00 - AdmSys Seazone Serviços](https://docs.google.com/spreadsheets/d/1YHvus3u692wr75lO_SDJgYuCo6kPqcLh9VxJ5WQ7GhQ/edit?gid=362456799#gid=362456799)
      * Entrada Expedia

        \

### `importStaysMes`

* **Objetivo**: puxar os dados referente as reservas da Stays, de acordo com o fechamento
* **Base de dados:**
  * **Sheets**
    * [00 - AdmSys Seazone Serviços](https://docs.google.com/spreadsheets/d/1YHvus3u692wr75lO_SDJgYuCo6kPqcLh9VxJ5WQ7GhQ/edit?gid=362456799#gid=362456799)
      * Entrada PayPal\n
    * [00 - AdmSys Seazone Serviços](https://docs.google.com/spreadsheets/d/1YHvus3u692wr75lO_SDJgYuCo6kPqcLh9VxJ5WQ7GhQ/edit?gid=362456799#gid=362456799)
      * Entrada PayPal
      * Entrada Tuna
      * Entrada Pagar.me
      * Entrada ASAAS
      * Entrada Khanto Reservas
      * Entrada BTG
      * Entrada Itaú


### `importLimpezaMes`

* **Objetivo**: puxar os dados de limpeza do metabase
* **Base de dados:**
  * **Metabase (v3)**
    * closing_seazone_resume csr 
    * property_property
    * reservation_reservation
    * reservation_ota
    * account_guest
    * account_user
    * property_property_owners


### `importAPIStaysMes`

* **Objetivo**: puxar os dados de API
* **Base de dados:**
  * **API: Stays**
    * `external/v1/booking/reservations-export`

## *==———Etapa 2: conciliar valor das reservas entre Sapron x Sheets==*

### `conciliacaoOTA`

* **Objetivo**: código base para match entre a base de dados do Sapron e Sheets, levando em consideração o valor proporcional da reserva, no mês com reservas a cima de 30 dias ou a partir da data de check-out
* **Base de dados:**
  * **Sheets**
    * **Própria Planilha**
      * Aba da OTA conciliada, com o nome "Nome_OTA Mes"
      * Reservas Mes
      * Devolucao & BOs

        \

### `conciliacaoAPIStays`

* **Objetivo**: código base para match entre a base de dados do Sapron e Sheets-API-Stays
* **Base de dados:**
  * **Sheets**
    * **Própria Planilha**
      * API-Stays Mes
      * Reservas Mes

## *==———Etapa 3: Consolidação dos dados==*

### `conciliacaoFechamento`

* **Objetivo**: consolidar todas as bases de reserva, com o valor proporcional
* **Base de dados:**
  * **Sheets**
    * **Própria Planilha**
      * Todas as abas de Conciliação Mes Nome_OTA

        \
    * [Compilado Fechamento - Modelo de Exportação](https://docs.google.com/spreadsheets/d/1r8tQ6i_g5HQSxRkOJRODRjZ8YdCWS_NKLqIvYcVsVlk/edit?gid=401327479#gid=401327479)
      * Modelo de exportação - props


### `metabaseRevenueAccrualDate`

* **Objetivo**: puxar os valores de faturamento do Metabase
* **Base de dados:**
  * **Metabase (v3)**
    * closing_seazone_resume
    * property_property
    * reservation_reservation
    * reservation_ota
    * account_guest
    * account_user
    * property_property_owners


## *==———Etapa 4: Suporte==*

### `removerFormulas`

* **Objetivo**: remover todas as fórmulas da planilha
* **Base de dados:**
  * **Sheets**
    * **Própria Planilha**
      * todas as abas da planilha


### `mainNoShow`

* **Objetivo**: enviar os dados de No-Show de cada OTA, para sua respectiva aba
* **Base de dados:**
  * **Sheets**
    * **Própria Planilha**
      * abas com "OTA Mes"

        \

  \

### `overbooking`

* **Objetivo**: identificar se houve overbooking
* **Base de dados:**
  * **Sheets**
    * **Própria Planilha**
      * Conciliação Fechamento