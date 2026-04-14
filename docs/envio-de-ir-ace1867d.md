<!-- title: Envio de IR | url: https://outline.seazone.com.br/doc/envio-de-ir-v03YZkyLT6 | area: Administrativo Financeiro -->

# Envio de IR

# **==__________________Sobre_______________________==**

## *==———Descrição———————————-==*

* Objetivo dessa planilha é gerar os IRs dos proprietários e dos anfitriões

## *==———Modificação——————————-==*

* Esta é a primeira versão da planilha

## *==———Histórico da Planilha———————==*

* [Envio de IR](https://docs.google.com/spreadsheets/d/1CFQkxYFkIAP-1vEq712Jj55WNbTdIdem3iS1OtF1B6o/edit?gid=0#gid=0)

# **==__________________Scripts______________________==**

## **==———Gerar IR do Proprietário==**

### `geraIROwner`

* **Objetivo**: cria um novo sheets, baseado nessa planilha [Relatório IR 2023 -> Layout](https://docs.google.com/spreadsheets/d/1H0cV3keuW8eeS1A-wiXU3h2ZOKEQvrpu-f7gWKSsZRc/edit?gid=256734427#gid=256734427), com os dados de repasse dos imóveis, por proprietário, e dropado na pasta [Declaração de Rendimentos do Proprietário](https://drive.google.com/drive/folders/1c9NkbgFjRvb1W_-HrFwJEDEXVSzOTY9P)
* **Base de Dados**
  * **Sheets**
    * [Compilado Fechamentos](https://docs.google.com/spreadsheets/d/1HDgd7eOk1P23zwJyzAGqR5k5cWDN4jd2kJZ87RXFi0c/edit?gid=0#gid=0)
      * Imóveis

### `gerarPDF`

* **Objetivo**: transforma o sheets em PDF
* **Base de Dados**
  * **Folder**
    * [Declaração de Rendimentos do Proprietário](https://drive.google.com/drive/folders/1c9NkbgFjRvb1W_-HrFwJEDEXVSzOTY9P)

### `listFilesInFolder`

* **Objetivo**: puxa todos os PDFs gerados, dando um match com o metabase, para puxar os dados do proprietário
* **Base de Dados**
  * **Metabase (v3)**
    * Account Owner
    * Account User
  * **Folder**
    * [Declaração de Rendimentos do Proprietário](https://drive.google.com/drive/folders/1c9NkbgFjRvb1W_-HrFwJEDEXVSzOTY9P)

### `sendEmails`

* **Objetivo**: enviar os emails para os proprietário de seus respectivos IRs
* **Base de Dados**
  * **Sheets**
    * **Própria Planilha**
      * Owner IR

## **==———Gerar IR do Anfitrião==**

### `geraIRHost`

* **Objetivo**: cria um novo sheets, baseado nessa planilha [Relatório IR Host 2023 -> Layout](https://docs.google.com/spreadsheets/d/1_X0KlESosY5y7XE8FiRP0uFFkVRFfVsGtAW4M-SI4fE/edit?gid=256734427#gid=256734427), com os dados de repasse dos Anfitrião, e dropado na pasta [Declaração de Rendimento do Anfitrião](https://drive.google.com/drive/folders/1fObfTymajIFrJq3eqY3YkVSP0L6jBh9T)
* **Base de Dados**
  * **Sheets**
    * [Compilado Fechamentos](https://docs.google.com/spreadsheets/d/1HDgd7eOk1P23zwJyzAGqR5k5cWDN4jd2kJZ87RXFi0c/edit?gid=0#gid=0)
      * Anfitrião

### `gerarPDF`

* **Objetivo**: transforma o sheets em PDF
* **Base de Dados**
  * **Folder**
    * [Declaração de Rendimento do Anfitrião](https://drive.google.com/drive/folders/1fObfTymajIFrJq3eqY3YkVSP0L6jBh9T)

### `listFilesInFolder`

* **Objetivo**: puxa todos os PDFs gerados, dando um match com o metabase, para puxar os dados do anfitrião
* **Base de Dados**
  * **Metabase (v3)**
    * Account Host
    * Account User
  * **Folder**
    * [Declaração de Rendimento do Anfitrião](https://drive.google.com/drive/folders/1fObfTymajIFrJq3eqY3YkVSP0L6jBh9T)

### `sendEmails`

* **Objetivo**: enviar os emails para os anfitriões de seus respectivos IRs
* **Base de Dados**
  * **Sheets**
    * **Própria Planilha**
      * Host IR