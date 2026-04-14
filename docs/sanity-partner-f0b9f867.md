<!-- title: Sanity Partner | url: https://outline.seazone.com.br/doc/sanity-partner-RbyDQzhjkt | area: Administrativo Financeiro -->

# Sanity Partner

# **==__________________Sobre_______________________==**

## *==———Descrição———————————-==*

* Planilha de comparação dos dados de parceiro do Metabase e sheets Fechamento Parceiro


## *==———Modificação——————————-==*

* Esta é a primeira versão da planilha


## *==———Histórico da Planilha———————==*

* [Sanity Partner](https://docs.google.com/spreadsheets/d/1VzdzDbRQcPXpVD2u9L7Ok11HBEiBVxVKA4zXY1bDpK0/edit?gid=0#gid=0)



---

# **==__________________Scripts______________________==**

## *==———Parceiro==*

### `partnerComissionProperty`

* **Objetivo**: puxar os dados do Sheets e Metabase consolidar os dados de parceiro
* **Base de dados:**
  * **Metabase (V3)**
    * partners_indications_property
    * property_property
    * account_partner
    * account_user

      \
  * **Sheets**
    * **[Fechamento Parceiros SZS 2.0](https://docs.google.com/spreadsheets/d/1O0qo1xyZnNyy1dLg8S5WCk-1XMH51GbC5T5bw3LrZAQ/edit?gid=1428695488#gid=1428695488)**
      * BD_ImovelParceiro
    * [\[Comercial\] Base de Dados Nekt](https://docs.google.com/spreadsheets/d/1bhUk24Xu7QRhPACSaFPaZjTk0nQlAxT5QS9t9nQPZxY/edit?gid=153032220#gid=153032220)
      * \[Pipedrive\] Ganhos SZS

        \


### `consolidado`

* **Objetivo**: puxar os dados do Sheets e Metabase e consolidar por parceiro
* **Base de dados:**
  * **Metabase (V3)**
    * financial_partner_commission_property
    * financial_partner_withdraw
    * account_partner
    * account_user

      \
  * **Sheets**
    * **[Fechamento Parceiros SZS 2.0](https://docs.google.com/spreadsheets/d/1O0qo1xyZnNyy1dLg8S5WCk-1XMH51GbC5T5bw3LrZAQ/edit?gid=1428695488#gid=1428695488)**
      * BD_Acumulo
      * BD_SolicitacaoResgate
    * [Compilado Fechamentos](https://docs.google.com/spreadsheets/d/1HDgd7eOk1P23zwJyzAGqR5k5cWDN4jd2kJZ87RXFi0c/edit?gid=0#gid=0)
      * Imóveis


### `quebrado`

* **Objetivo**: puxar os dados do Sheets e Metabase e consolidar por imóvel
* **Base de dados:**
  * **Metabase (V3)**
    * financial_partner_commission_property
    * closing_property_resume
    * property_property
    * account_partner
    * account_user

      \
  * **Sheets**
    * **[Fechamento Parceiros SZS 2.0](https://docs.google.com/spreadsheets/d/1O0qo1xyZnNyy1dLg8S5WCk-1XMH51GbC5T5bw3LrZAQ/edit?gid=1428695488#gid=1428695488)**
      * BD_Acumulo
    * [Compilado Fechamentos](https://docs.google.com/spreadsheets/d/1HDgd7eOk1P23zwJyzAGqR5k5cWDN4jd2kJZ87RXFi0c/edit?gid=0#gid=0)
      * Imóveis