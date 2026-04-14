<!-- title: Controle CRC_2023.06.21 GKMA | url: https://outline.seazone.com.br/doc/controle-crc_20230621-gkma-m8hWJ7ci9Q | area: Administrativo Financeiro -->

# Controle CRC_2023.06.21 GKMA

# **==__________________Sobre_______________________==**

## *==———Descrição———————————-==*

* Consolidar os dados de receita


## *==———Modificação——————————-==*

* Existe uma versão [2.0 CRC](https://docs.google.com/spreadsheets/d/1_b6YL8q6T-wbtrGRcneqH3rVCMk_-ZoHp-GXJytxG_4/edit?gid=2114030530#gid=2114030530), que foi criada, mas não está em uso


## *==———Histórico da Planilha———————==*

* [Controle CRC_2023.06.21 GKMA](https://docs.google.com/spreadsheets/d/1Q1dV4hkJqfKABiPMsYXY5sLYVVq8l1NyBBediuWqApE/edit?gid=822640047#gid=822640047)
* [2.0 CRC](https://docs.google.com/spreadsheets/d/1_b6YL8q6T-wbtrGRcneqH3rVCMk_-ZoHp-GXJytxG_4/edit?gid=2114030530#gid=2114030530)



---

# **==__________________Scripts______________________==**

## *==———Suporte==*

### `bringRoyalt`

* **Objetivo**: trazer os dados de comissão da Seazone para emissão de NF
* **Base de dados:**
  * **Sheets**
    * **Própria Planilha**
      * REC_ROYALTY_FRANQ

        \
    * **[Compilado Fechamentos](https://docs.google.com/spreadsheets/d/1HDgd7eOk1P23zwJyzAGqR5k5cWDN4jd2kJZ87RXFi0c/edit?gid=0#gid=0)**
      * NF Anfitriões


### `pipedriveRecFranquia`

* **Objetivo**: puxar os ganhos de imóveis
* **Base de dados:**
  * **Sheets**
    * **Própria Planilha**
      * REC_FRANQUIA

        \
    * **[00 - BD Pipedrive](https://docs.google.com/spreadsheets/d/1D48hhoKz7sRUNrMdcOnWvg6okQxzu-aex4-QDZeWKBM/edit?gid=0#gid=0)**
      * Expansao

        \
    * [00 - Banco de dados PMS](https://docs.google.com/spreadsheets/d/1u6C2KtkJqDvR6-ZKDRLsLKZ5leaAnYPp78tTG3v6NXo/edit?gid=169327024#gid=169327024)
      * User


### `REC_IMPLANTAÇÃO_Churn`

* **Objetivo**: puxar os dados de churn
* **Base de dados:**
  * **API: nome_da_empresa_api**
    * Endpoint

      \
  * **Slack**
    * Nome do Fluxo e Link

    \
  * **Sapron**
    * nome da pergunta com o link

      \
  * **Metabase**
    * nome das tabelas

      \
  * **Folder**
    * Nome do folder, com link

      \
  * **Input Manual**
    * breve descrição do input manual

      \
  * **Sheets**
    * **Própria Planilha**
      * REC_IMPLANTAÇÃO

        \
    * **[Controle BOs e alterações de taxa de limpeza](https://docs.google.com/spreadsheets/d/1D44LvEO6MTzueJ65591es4CnmfvZXxR1pdP5B8v4Jcc/edit?gid=855501021#gid=855501021)**
      * Controle Ajustes Diretos e Imóvel


### `mainMetaImplantacao`

* **Objetivo**: puxar as novas taxas de implantação
* **Base de dados:**
  * **Metabase**
    * Property Handover Details
    * Property Property
    * Account Host
    * Account User

      \
  * **Sheets**
    * **Própria Planilha**
      * REC_IMPLANTAÇÃO

### `puxarIDApto`

* **Objetivo**: puxar os ids dos imóveis
* **Base de dados:**
  * **Metabase**
    * Property Property
    * Account Owner
    * Account User
    * Account Host
    * Account User

      \
  * **Sheets**
    * **Própria Planilha**
      * REC_IMPLANTAÇÃO

  \