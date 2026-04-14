<!-- title: Fechamento RH Original | url: https://outline.seazone.com.br/doc/fechamento-rh-original-pgQKPeVcj4 | area: Administrativo Financeiro -->

# Fechamento RH Original

# **==__________________Sobre_______________________==**

## *==———Descrição———————————-==*

* Objetivo dessa planilha é consolidar os valores dos salários dos colaboradores para ser enviado ao financeiro para pagamento

## *==———Modificação——————————-==*

* Esta é a primeira versão da planilha

## *==———Histórico da Planilha———————==*

* [Fechamento RH Original](https://docs.google.com/spreadsheets/d/1FQTvAXAnbNCDeU1dTgOKa9U53S_QRrXrvs9FvlI8e7k/edit?gid=1567888739#gid=1567888739)

# **==__________________Scripts______________________==**

## *==———==*==Puxar Todos os Dados==

### `conveniaColabInvestimento`

* **Objetivo**: puxar os dados dos colaboradores da Seazone Investimentos, via API da Convenia
* **Base de Dados**
  * **Convenia**
    * employees/?page=
    * employees/
  * **Sheets**
    * **Própria Planilha**
      * Guapeco - Mensalidade
      * Convênio - Coparticipação
      * Convênio - Mensalidade
    * [BASE OFICIAL RH](https://docs.google.com/spreadsheets/d/1WPRfbNC3z55Gp4APKTvzB5h_DeoJWsEjx0rqbz2wWXY/edit?gid=740587445#gid=740587445)
      * BASE OFICIAL RH

### `conveniaColabServicos`

* **Objetivo**: puxar os dados dos colaboradores da Seazone Serviços, via API da Convenia
* **Base de Dados**
  * **Convenia**
    * employees/?page=
    * employees/
  * **Sheets**
    * **Própria Planilha**
      * Guapeco - Mensalidade
      * Convênio - Coparticipação
      * Convênio - Mensalidade
    * [BASE OFICIAL RH](https://docs.google.com/spreadsheets/d/1WPRfbNC3z55Gp4APKTvzB5h_DeoJWsEjx0rqbz2wWXY/edit?gid=740587445#gid=740587445)
      * BASE OFICIAL RH

### `importGuapeco`

* **Objetivo**: puxar os dados de cobrança da Guapeco por colaborador
* **Base de Dados**
  * **Sheets**
    * [Guapeco + Seazone - Relatório mensal de adesões](https://docs.google.com/spreadsheets/d/1UojTJDMFu_sNfFUjW9wFuzO5_yK-metKUTf1pn-Vgso/edit?gid=1705254684#gid=1705254684)
      * Nome da aba é de acordo com o mês de fechamento salarial

## *==———==*==Envio de Dados==

### `enviarMensagem`

* **Objetivo**: envia uma mensagem para os colaboradores, que possuem algum tipo de alteração do valor do salário, como descontos de convênio
* **Base de Dados**
  * **Sheets**
    * **Própria Planilha**
      * Consolidado
  * **Slack**
    * [Informativo Nota Fiscal](https://app.slack.com/workflow-builder/TDLTVAWQ6/workflow/Wf072UA9D3G8?unified_user_workflow_builder=1)

### `SendCPG2`

* **Objetivo**: enviar os dados de pagamento dos colaboradores para o [2.0 CPG](https://docs.google.com/spreadsheets/d/18tMzv-PdEH2-QTt0jvzcOVfcnDREfUg0fasoNKKRot8/edit?gid=1111763258#gid=1111763258) aba PGTO_SALARIOS
* **Base de Dados**
  * **Sheets**
    * **Própria Planilha**
      * Consolidado