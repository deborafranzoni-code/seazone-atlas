<!-- title: Contas a Receber - OMIE | url: https://outline.seazone.com.br/doc/contas-a-receber-omie-4P9RBqHknv | area: Administrativo Financeiro -->

# Contas a Receber - OMIE

# **==__________________Sobre_______________________==**

## *==———Descrição———————————-==*

* Puxar os dados de taxa de franquia e seus recebimentos
* Lançar dados de taxa e recebimento de taxa de franquia no OMIE


## *==———Modificação——————————-==*

* [Esta é a primeira versão da planilha](https://www.loom.com/share/11579020b6fd4c0bab127d0398b66fe7)


## *==———Histórico da Planilha———————==*

* [Contas a Receber - OMIE](https://docs.google.com/spreadsheets/d/1oyXULmhlqJSsZw-Fnpqc6HS6qWBzcwc0wzYFgbXi-IU/edit?gid=194474170#gid=194474170)



---

# **==__________________Scripts______________________==**

## *==———Suporte==*

### `omieBringData`

* **Objetivo**: puxar os dados do OMIE
* **Base de dados:**
  * **API: OMIE**
    * `api/v1/`
    * `ListarCategorias`
    * `ListarContasCorrentes`
    * `ListarDepartamentos`
    * `ListarProjetos`
    * `extratoFornClient`


## *==———Lançamento no Contas a Receber==*

### `taxaFranquia`

* **Objetivo**: puxar os dados de novas taxas de franquia
* **Base de dados:**
  * **Metabase**
    * financial_host_franchise_fee
    * account_host
    * account_user


* **Própria Planilha**
  * Histórico Contas Receber

    \

### `incluirCRC`

* **Objetivo**: imputar uma nova receita no OMIE
* **Base de dados:**
  * **API: OMIE**
    * IncluirContaReceber

      \
  * **Sheets**
    * **Própria Planilha**
      * Pendência Contas Receber

## *==———Lançamento de Recebimentos==*

### `pendenciaRecebimento`

* **Objetivo**: puxar do metabase, os valores de pagamento da taxa de franquia
* **Base de dados:**
  * **Metabase**
    * financial_host_franchise_fee_payment
    * account_host
    * account_user

      \
  * **Sheets**
    * **Própria Planilha**
      * Histórico Recebimento

        \

### `lancarRec`

* **Objetivo**: lançar os dados de recebimento no OMIE
* **Base de dados:**
  * **API: OMIE**
    * LancarRecebimento

      \
  * **Sheets**
    * **Própria Planilha**
      * Pendência Recebimento
      * Base OMIE

        \
* \