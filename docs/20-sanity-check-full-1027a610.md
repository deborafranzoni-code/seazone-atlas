<!-- title: 2.0 - Sanity Check Full | url: https://outline.seazone.com.br/doc/20-sanity-check-full-qAvxw07yKD | area: Administrativo Financeiro -->

# 2.0 - Sanity Check Full

# **==__________________Sobre_______________________==**

## *==———Descrição———————————-==*

* Comparar os dados de conciliação, e demais bases de fechamento imóvel/anfitrião, com os dados do Sapron


## *==———Modificação——————————-==*

* Remoção da planilha de fechamento
* Otimização dos códigos do metabase, para a versão v3


## *==———Histórico da Planilha———————==*

* [2.0 - Sanity Check Full](https://docs.google.com/spreadsheets/d/1DBSvU09gmRyqR7kEb30-J_a7YFV-6bk0LjzpcRYIZy4/edit?gid=2011589236#gid=2011589236)



---

# **==__________________Scripts______________________==**

## *==———Requisição de Dados de Fechamento==*

### `anfitriaoGeral`

* **Objetivo**: puxar os dados de fechamento do anfitrião e comparar com os dados do compilado fechamento, de forma consolidada
* **Base de dados:**
  * **Metabase (v3)**
    * closing_host_resume
    * account_host
    * account_user

      \
  * **Sheets**
    * **[Compilado Fechamentos](https://docs.google.com/spreadsheets/d/1HDgd7eOk1P23zwJyzAGqR5k5cWDN4jd2kJZ87RXFi0c/edit?gid=0#gid=0)**
      * **Anfitrião**


### `imovelGeral`

* **Objetivo**: puxar os dados de fechamento da propriedade e comparar com os dados do compilado fechamento, de forma consolidada
* **Base de dados:**
  * **Metabase (v3)**
    * closing_property_resume
    * property_property
    * closing_property_balance

      \
  * **Sheets**
    * **[Compilado Fechamentos](https://docs.google.com/spreadsheets/d/1HDgd7eOk1P23zwJyzAGqR5k5cWDN4jd2kJZ87RXFi0c/edit?gid=0#gid=0)**
      * **Imóveis**


\
## *==———Suporte==*

### `limpesaAnf`

* **Objetivo**: comparar os dados do Sapron e Sheets de limpeza individualmente
* **Base de dados:**
  * **Metabase (v3)**
    * closing_property_resume
    * property_property

      \
  * **Sheets**
    * **[Compilado Fechamento - Modelo de Exportação](https://docs.google.com/spreadsheets/d/1r8tQ6i_g5HQSxRkOJRODRjZ8YdCWS_NKLqIvYcVsVlk/edit?gid=195336355#gid=195336355)**
      * **Modelo de exportação - Anfitriões**


### `despesa`

* **Objetivo**: comparar os dados do Sapron e Sheets de despesas individualmente
* **Base de dados:**
  * **Metabase (v3)**
    * closing_property_resume
    * property_property

      \
  * **Sheets**
    * **[14 -BD despesas](https://docs.google.com/spreadsheets/d/1wL4SBGofNb04MH3nzWVmgus2evD26zUJaquuaR0wbCk/edit?gid=30783992#gid=30783992)**
      * **Despesas (Legacy)**

### `revenue`

* **Objetivo**: comparar os dados do Sapron e Sheets de receita individualmente
* **Base de dados:**
  * **Metabase (v3)**
    * closing_property_resume
    * property_property

      \
  * **Sheets**
    * **[Compilado Fechamento - Modelo de Exportação](https://docs.google.com/spreadsheets/d/1r8tQ6i_g5HQSxRkOJRODRjZ8YdCWS_NKLqIvYcVsVlk/edit?gid=195336355#gid=195336355)**
      * **Modelo de exportação - props**


### `comissao`

* **Objetivo**: comparar os dados do Sapron e Sheets de comissão individualmente
* **Base de dados:**
  * **Metabase (v3)**
    * closing_property_resume
    * property_property

      \
  * **Sheets**
    * **[Compilado Fechamento - Modelo de Exportação](https://docs.google.com/spreadsheets/d/1r8tQ6i_g5HQSxRkOJRODRjZ8YdCWS_NKLqIvYcVsVlk/edit?gid=195336355#gid=195336355)**
      * **Modelo de exportação - Anfitriões**
      * **Modelo de exportação - props**