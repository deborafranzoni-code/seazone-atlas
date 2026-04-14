<!-- title: 9.0 Sanity Check: AWS<>Fechamento | url: https://outline.seazone.com.br/doc/90-sanity-check-awsfechamento-SmXLNRjcfE | area: Administrativo Financeiro -->

# 9.0 Sanity Check: AWS<>Fechamento

# **==__________________Sobre_______________________==**

## *==———Descrição———————————-==*

* Objetivo dessa planilha é fazer uma comparação com os valores gerados pelo Fechamento Sheets (Planilha de conciliação e Fechamento) e as tabelas do Sapron


## *==———Modificação——————————-==*

* Troca dos códigos de requisição do metabase


## *==———Histórico da Planilha———————==*

* **[9.0 Sanity Check: AWS<>Fechamento](https://docs.google.com/spreadsheets/d/1aCE_6g1dWrvJZKEmH7Q_G9XLQiVMjoxjv70vdPvpD_Y/edit?gid=814545073#gid=814545073)**
* Possui outras versões dessa planilha, porém não estão abordadas nesse outline



---

# **==__________________Scripts______________________==**

## *==———Passo 1 - Puxar os Dados para Match==*

### `closingSeazoneResume`

* **Objetivo**: puxar todos os dados do imóvel e anfitrião, tanto do Sapron, quando do Sheets, para comparação do fechamento Seazone
* **Base de dados:**
  * **Metabase (v3)**
    * Closing Seazone Resume
    * Property Property
    * Reservation Reservation
    * Financial Host Manual Fit
    * Account Host
    * Account User

      \
  * **Folder**
    * Nome do folder, com link

      \
  * **Input Manual**
    * breve descrição do input manual

      \
  * **Sheets**
    * [04 - Conciliação futura e verificações](https://docs.google.com/spreadsheets/d/1k3fqGBd5bgsGYaRUywe69aa7qWPD22IzV_1XMwuIODA/edit?gid=128461091#gid=128461091)
      * Saldos em conta props

      \
      \
    * [Fechamento Mensal Template - BizOps](https://docs.google.com/spreadsheets/d/1KGzbDR73lPKpi2g7an21kvU9Xp6ud1wtdOIjJxdBF_Y/edit?gid=2081357185#gid=2081357185)
      * Ajustes
      * Despesas Mes
      * Anfitrião
      * Imovel

        \
    * [Conciliação Reservas Sapron](https://docs.google.com/spreadsheets/d/1lP2f1RLk3aV0bhwHFbHG92_ORe36NNlCmUnRg-_tIQs/edit?gid=2097081422#gid=2097081422)
      * Conciliação Fechamento
      * Limpezas Mes


### `closingHostResume`

* **Objetivo**: puxar todos os dados do anfitrião, tanto do Sapron, quando do Sheets, para comparação do fechamento anfitrião
* **Base de dados:**
  * **Metabase (v3)**
    * Account Host
    * Account User
    * Closing Host Resume
    * Reservation Reservation
    * Closing Seazone Resume
    * Property Property
    * Financial Host Manual Fit
    * Financial_Host_Franchise_Fee_Payment
    * Financial_Host_Franchise_Fee

      \
  * **Sheets**
    * [Conciliação Reservas Sapron](https://docs.google.com/spreadsheets/d/1lP2f1RLk3aV0bhwHFbHG92_ORe36NNlCmUnRg-_tIQs/edit?gid=2097081422#gid=2097081422)
      * Conciliação Fechamento
      * Limpezas Mes

        \
    * [Fechamento Mensal Template - BizOps](https://docs.google.com/spreadsheets/d/1KGzbDR73lPKpi2g7an21kvU9Xp6ud1wtdOIjJxdBF_Y/edit?gid=2081357185#gid=2081357185)
      * Ajustes
      * Despesas Mes
      * Resumo Anfitrião

        \
    * [Controle CRC_2023.06.21 GKMA](https://docs.google.com/spreadsheets/d/1Q1dV4hkJqfKABiPMsYXY5sLYVVq8l1NyBBediuWqApE/edit?gid=350306181#gid=350306181)
      * REC_FRANQUIA


### `closingPropertyResume`

* **Objetivo**: puxar todos os dados do imóvel, tanto do Sapron, quando do Sheets, para comparação do fechamento Imóvel
* **Base de dados:**
  * **Metabase (v3)**
    * Closing Property Resume
    * Reservation Reservation
    * Property Property
    * Closing Property Balance

      \
  * **Sheets**
    * [Conciliação Reservas Sapron](https://docs.google.com/spreadsheets/d/1lP2f1RLk3aV0bhwHFbHG92_ORe36NNlCmUnRg-_tIQs/edit?gid=2097081422#gid=2097081422)
      * Conciliação Fechamento

        \
    * [Fechamento Mensal Template - BizOps](https://docs.google.com/spreadsheets/d/1KGzbDR73lPKpi2g7an21kvU9Xp6ud1wtdOIjJxdBF_Y/edit?gid=2081357185#gid=2081357185)
      * Despesas Mes
      * Imovel

        \
    * [04 - Conciliação futura e verificações](https://docs.google.com/spreadsheets/d/1k3fqGBd5bgsGYaRUywe69aa7qWPD22IzV_1XMwuIODA/edit?gid=128461091#gid=128461091)
      * Saldos em conta props


### `tedImovelCSVSapron`

* **Objetivo**: 
* **Base de dados:** puxar os dados de Notas Fiscais do Sapron
  * **Sapron**
    * financial_closing/property/generate_nfs_csv/?actual_route=/listadenfs
    * API Route: actual_route=/listadenfs

  \


## *==———Passo 2 - Envio de Dados==*

### `enviaCheckNF`

* **Objetivo**: enviar os dados de NF para a planilha de [Check NFs](https://docs.google.com/spreadsheets/d/11sJnY4PMhThoukbR_WH2Nt4ig3gck0So7TraEAiBBMU/edit?gid=1525660162#gid=1525660162), para as abas de Gestão de Contas (caso o imóvel tenha contratado gestão de contas) ou Remessa 0
* **Base de dados:**
  * **Sheets**
    * **Própria Planilha**
      * SPN_TED_Imovel

        \
    * [04 - Conciliação futura e verificações](https://docs.google.com/spreadsheets/d/1k3fqGBd5bgsGYaRUywe69aa7qWPD22IzV_1XMwuIODA/edit?gid=128461091#gid=128461091)
      * Histórico Plano