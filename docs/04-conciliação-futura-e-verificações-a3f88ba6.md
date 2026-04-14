<!-- title: 04 - Conciliação futura e verificações | url: https://outline.seazone.com.br/doc/04-conciliacao-futura-e-verificacoes-5mjZXC9GqB | area: Administrativo Financeiro -->

# 04 - Conciliação futura e verificações

## **==__________________Sobre_______________________==**

## *==———Descrição———————————-==*

* Objetivo dessa planilha é consolidar os dados necessários para realização do fechamento

## *==———Modificação——————————-==*

* Esta é a primeira versão da planilha

## *==———Histórico da Planilha———————==*

* [04 - Conciliação futura e verificações](https://docs.google.com/spreadsheets/d/1k3fqGBd5bgsGYaRUywe69aa7qWPD22IzV_1XMwuIODA/edit?gid=128461091#gid=128461091)

# **==__________________Scripts______________________==**

## ==———Trocas==

### `trocaImovel`

* **Objetivo**: puxar todas as trocas de código do imóvel, que estão como finalizadas
* **Base de Dados**
  * **Sheets**
    * [BD - Troca de código](https://docs.google.com/spreadsheets/d/18RA5MumcfycazS7uV9pW6Q8J0fQSriFDs_-X6aZA3Pk/edit?gid=1980896385#gid=1980896385)
      * BD - Respostas do formulário

### `trocaPropForm`

* **Objetivo**: puxar todas as trocas de proprietários
* **Base de Dados**
  * **Sheets**
    * **Planilha Própria**
      * Troca Proprietário
  * **Metabase (v3)**
    * Apartment
    * Account Owner
    * Account User

### `trocaAnfForm`

* **Objetivo**: puxar todas as trocas de anfitriões
* **Base de Dados**
  * **Sheets**
    * **Planilha Própria**
      * Migração Anfitrião
  * **Metabase (v3)**
    * Apartment
    * Account Owner
    * Account User

## ==———Suporte==

### `metabaseChurn_CheckOut` Desligada

* **Objetivo**: trazer a última reserva do imóvel, quando der churn
* **Base de Dados**
  * **Metabase**
    * [Última Reserva dos Imóveis com Churn](https://metabase.seazone.com.br/question/413-ultima-reserva-dos-imoveis-com-churn)
      * reservation_reservation
      * reservation_listing
      * reservation_ota
      * property_propert

### `saldosPropBase`

* **Objetivo**: puxar a taxa de implantação dos novos imóveis
* **Base de Dados**
  * **Metabase (v3)**
    * Property Handover Details
    * Property Property

### `metabasePlanos`

* **Objetivo**: puxar apenas as propriedades ativas que possuem o plano Plus
* **Base de Dados**
  * **Metabase (v3)**
    * Property Handover Details
    * Property Property

### `ajusteData`

* **Objetivo**: ajustar a data, para o formato de data reconhecido pelo sheets
* **Base de Dados**
  * **Sheets**
    * **Própria Planilha**
      * Mudança de código


\

\
### `importFranchise`

* **Objetivo**: puxar os dados de taxa de franquia e valor de comissão dos franquiados
* **Base de Dados**
  * **Metabase (v3)**
    * Property Handover Details
    * Property Property
  * **[Controle CRC_2023.06.21 GKMA](https://docs.google.com/spreadsheets/d/1Q1dV4hkJqfKABiPMsYXY5sLYVVq8l1NyBBediuWqApE/edit?gid=350306181#gid=350306181)**
    * REC_FRANQUIA


### `ajusteSaldoSznRepasseSegurado`

* **Objetivo**: ajustar os dados da coluna "**Saldo Atualizado Seazone (AE)**" da planilha de Compilado Fechamento dos imóveis que tiveram repasse segurado
* **Base de Dados**
  * **Sheets**
    * **Própria Planilha**
      * Repasses Segurados
    * **[Compilado Fechamentos](https://docs.google.com/spreadsheets/d/1HDgd7eOk1P23zwJyzAGqR5k5cWDN4jd2kJZ87RXFi0c/edit?gid=0#gid=0)**
      * Imóveis