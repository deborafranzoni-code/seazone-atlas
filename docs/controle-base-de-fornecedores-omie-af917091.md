<!-- title: Controle Base de Fornecedores Omie | url: https://outline.seazone.com.br/doc/controle-base-de-fornecedores-omie-aEP6FMHXQh | area: Administrativo Financeiro -->

# Controle Base de Fornecedores Omie

# **==__________________Sobre_______________________==**

## *==———Descrição———————————-==*

* Esta planilha tem como função controlar e atualizar os dados de fornecedores da Seazone no OMIE


## *==———Modificação——————————-==*

* Esta é a primeira versão da planilha


## *==———Histórico da Planilha———————==*

* [Controle Base de Fornecedores Omie](https://docs.google.com/spreadsheets/d/1mMPK1fZ9zEJta6AEU560Ylbc5-YS2AOdwc3EgFL7jCw/edit?gid=0#gid=0)



***

# **==__________________Scripts______________________==**

## *==———Nome do Agrupamento==*

### `compareAndMarkAlterations`

* **Objetivo**: puxar os dados do OMIE, Convenia e Metabase, para identificar alterações com relaçao aos dados do OMIE
* **Base de dados:**
  * **API: OMIE**
    * ListarClientes

      \
  * **API: Convenia**
    * api/v3/employees

    \
  * **Metabase**
    * account_user
    * financial_bank_details
    * financial_invoice_details
    * financial_bank

  \

### `alterarFC`

* **Objetivo**: lançar ajuste de dados dos fornecedores no OMIE, e dropar "Logs de Alteração Omie" dos dados ajustados
* **Base de dados:**
  * **API: OMIE**
    * AlterarCliente
  * **Sheets**
    * **Própria Planilha**
      * Lançamento de Alteração Fornecedores Omie

        \