<!-- title: Stays | url: https://outline.seazone.com.br/doc/stays-Y5MqiO7ayE | area: Administrativo Financeiro -->

# Stays

# **==__________________Sobre_______________________==**

## *==———Descrição———————————-==*

* Esta planilha tem uma API da Stays que puxa os dados das reservas


## *==———Modificação——————————-==*

* Esta é a primeira versão da planilha


## *==———Histórico da Planilha———————==*

* [Stays](https://docs.google.com/spreadsheets/d/1drVxVgHdmt6vClkJ0H7iLRTn9dshAPhc4xoIti5FYfg/edit?gid=0#gid=0)



---

# **==__________________Scripts______________________==**

## *==———Nome do Agrupamento==*

### `GET_ReservasExpress`

* **Objetivo**: puxar os dados de reserva da Stays, baseado em um range de data
* **Base de dados:**
  * **API: Stays**
    * `external/v1/booking/reservations-export`