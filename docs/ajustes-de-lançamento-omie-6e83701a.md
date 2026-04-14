<!-- title: Ajustes de Lançamento Omie | url: https://outline.seazone.com.br/doc/ajustes-de-lancamento-omie-9LjiiIQo1O | area: Administrativo Financeiro -->

# Ajustes de Lançamento Omie

# **==__________________Sobre_______________________==**

## *==———Descrição———————————-==*

* Objetivo dessa planilha é ajustar lançamentos de contas a pagar no OMIE

## *==———Modificação——————————-==*

* Esta é a primeira versão da planilha

## *==———Histórico da Planilha———————==*

* [Ajustes de Lançamento Omie](https://docs.google.com/spreadsheets/d/1Yx78lTH3s_ymsuWwe7BDCE2J_3zVjCKpnK8G3vHYDB0/edit?gid=474202860#gid=474202860)

# **==__________________Scripts______________________==**

## ==———Puxar Dados OMIE==

### `OmieAPI`

* **Objetivo**: código mãe para requisição dos dados no OMIE
* **Base de Dados**
  * **API: OMIE**
    * api/v1

### `listarProjeto`

* **Objetivo**: puxar o código e o nome da projeto
* **Base de Dados**
  * **API: OMIE**
    * ListarProjetos

### `listarDepartamento`

* **Objetivo**: puxar o código e o nome da departamento
* **Base de Dados**
  * **API: OMIE**
    * ListarDepartamentos

### `listarCategoria`

* **Objetivo**: puxar o código e o nome da categoria
* **Base de Dados**
  * **API: OMIE**
    * ListarCategorias

## ==———Enviar Dados OMIE==

### `envioOmieCPG`

* **Objetivo**: envio dos dados para o OMIE
* **Base de Dados**
  * **API: OMIE**
    * AlterarContaPagar
  * **Sheets**
    * **Própria Planilha**
      * Ajuste de Lançamento