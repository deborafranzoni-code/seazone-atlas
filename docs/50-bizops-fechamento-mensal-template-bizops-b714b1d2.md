<!-- title: 5.0 BizOps - Fechamento Mensal Template - BizOps | url: https://outline.seazone.com.br/doc/50-bizops-fechamento-mensal-template-bizops-HpgpSUdDE9 | area: Administrativo Financeiro -->

# 5.0 BizOps - Fechamento Mensal Template - BizOps

# **==__________________Sobre_______________________==**

## *==———Descrição———————————-==*

* O objetivo dessa planilha é consolidar os valores dos imóveis e dos anfitriões para gerar o valor final a ser repassado aos proprietários e anfitriões, como também calcular os valores da Seazone

## *==———Modificação——————————-==*

* Otimização das funções
* Limpeza da planilha
* Remoção da dependência das planilhas de [00 - Banco de dados PMS](https://docs.google.com/spreadsheets/d/1u6C2KtkJqDvR6-ZKDRLsLKZ5leaAnYPp78tTG3v6NXo/edit?gid=169327024#gid=169327024) e [Plano de Contingência](https://docs.google.com/spreadsheets/d/1daMGyKDwmwK1mQPvVX8E9cknJxKKaidqi7m16TAKgvA/edit?gid=1927281153#gid=1927281153)

## *==———Histórico da Planilha———————==*

* **[5.0 BizOps - Fechamento Mensal Template - BizOps](https://docs.google.com/spreadsheets/d/1KGzbDR73lPKpi2g7an21kvU9Xp6ud1wtdOIjJxdBF_Y/edit?gid=2081357185#gid=2081357185)**


# **==__________________Scripts______________________==**

## ==———Passo 1 - Importação dos dados==

### `insertExpenses`

* **Objetivo**: puxar todas as despesas imputadas no Sapron
* **Base de Dados**
  * **Metabase (v3)**
    * Financial Expenses
    * Account Host
    * Property Property
    * Property Handover Details

### `importFranchise` **(v3)**

* **Objetivo**: puxar todas as taxas de franquia e valores imputadas no Sapron
* **Base de Dados**
  * **Metabase**
    * financial_host_franchise_fee
    * account_host
    * account_user
    * Financial_Host_Franchise_Fee_Payment

### `importAjuste`

* **Objetivo**: puxar todos os ajustes referentes aos anfitriões e imóveis
* **Base de Dados**
  * **Sheets**
    * [Controle BOs e alterações de taxa de limpeza](https://docs.google.com/spreadsheets/d/1D44LvEO6MTzueJ65591es4CnmfvZXxR1pdP5B8v4Jcc/edit?gid=855501021#gid=855501021)
      * Controle BOs
      * Controle Ajustes Diretos e Imóvel

### `importSaldo`

* **Objetivo**: puxar os valores em aberto dos imóveis
* **Base de Dados**
  * **Sheets**
    * [04 - Conciliação futura e verificações](https://docs.google.com/spreadsheets/d/1k3fqGBd5bgsGYaRUywe69aa7qWPD22IzV_1XMwuIODA/edit?gid=1400643550#gid=1400643550)
      * Saldos em conta pro

## ==———Passo 2 - Atualizar abas de consolidação de dados==

### `bringImovel`

* **Objetivo**: puxar os valores referente as imóveis e consolidar tudo em apenas 1 aba
* **Base de Dados**
  * **Metabase (v3)**
    * Property Property
    * Account Owner
    * Account User
    * Account Host
    * Account User
  * **Sheets**
    * **Própria Planilha**
      * Saldos
      * Despesas Mes
      * Ajustes
    * [Conciliação Reservas Sapron](https://docs.google.com/spreadsheets/d/1lP2f1RLk3aV0bhwHFbHG92_ORe36NNlCmUnRg-_tIQs/edit?gid=2097081422#gid=2097081422)
      * Conciliação Fechamento

### `bringAnfitriao`

* **Objetivo**: puxar os valores referente aos anfitriões, que estão atrelados a algum imóvel e consolidar tudo em apenas 1 aba
* **Base de Dados**
  * **Metabase (v3)**
    * Property Host Time In Property
    * Account Owner
    * Account User
    * Property Property
    * Account Host
  * **Sheets**
    * **Própria Planilha**
      * Ajustes
      * Despesas Mes
    * [Conciliação Reservas Sapron](https://docs.google.com/spreadsheets/d/1lP2f1RLk3aV0bhwHFbHG92_ORe36NNlCmUnRg-_tIQs/edit?gid=2097081422#gid=2097081422)
      * Conciliação Fechamento
      * Limpezas Mes

### `bringResumoAnfitriao`

* **Objetivo**: puxar os valores referente aos anfitriões e consolidar tudo em apenas 1 aba
* **Base de Dados**
  * **Metabase (v3)**
    * Account Host
    * Account User
  * **Sheets**
    * **Própria Planilha**
      * Tx Franquia
      * Despesas Mes
      * Ajustes
    * [Conciliação Reservas Sapron](https://docs.google.com/spreadsheets/d/1lP2f1RLk3aV0bhwHFbHG92_ORe36NNlCmUnRg-_tIQs/edit?gid=2097081422#gid=2097081422)
      * Conciliação Fechamento
      * Limpezas Mes
      * nome da aba

### `bringNotasFiscais`

* **Objetivo**: puxar os valores referente as comissões dos hosts e da Seazone, para emissão de notais ficais, quebrados por imóvel
* **Base de Dados**
  * **Metabase (v3)**
    * property_property
    * account_owner
    * financial_invoice_details
  * **Sheets**
    * **Própria Planilha**
      * Anfitrião

### `bringModProp`

* **Objetivo**: puxar todas as reservas da planilha de conciliação
* **Base de Dados**
  * **Sheets**
    * [Conciliação Reservas Sapron](https://docs.google.com/spreadsheets/d/1lP2f1RLk3aV0bhwHFbHG92_ORe36NNlCmUnRg-_tIQs/edit?gid=2097081422#gid=2097081422)
      * Conciliação Fechamento

### `bringModAnf`

* **Objetivo**: puxar todas as reservas da planilha de conciliação
* **Base de Dados**
  * **Sheets**
    * [Conciliação Reservas Sapron](https://docs.google.com/spreadsheets/d/1lP2f1RLk3aV0bhwHFbHG92_ORe36NNlCmUnRg-_tIQs/edit?gid=2097081422#gid=2097081422)
      * Conciliação Fechamento
      * Limpezas Mes

## ==———Passo 3 - Geração de Listas de NF para os Anfitriões==

### `gerarListaNFAnfitriao`

* **Objetivo**: cria novos docs, com os dados consolidados, referentes a cada anfitrião, seguindo este [molde](https://docs.google.com/document/d/15CSm7k7xTYE-TgdBd9cwlSKLSfxM1DeJFflvwqQ7CrA/edit?tab=t.0), e dropando neste [folder](https://drive.google.com/drive/folders/1Pmm2T6sdM8vEngwWWnwtyQdvfC-0IzhJ)
* **Base de Dados**
  * **Sheets**
    * **Própria Planilha**
      * Notas fiscais

### `gerarPdfListaNFAnfitriao`

* **Objetivo**: transformar os novos docs de cada anfitriões em pdf, do código "gerarListaNFAnfitriao"
* **Base de Dados**
  * **Folder**
    * [Prestação de contas](https://drive.google.com/drive/folders/1Pmm2T6sdM8vEngwWWnwtyQdvfC-0IzhJ)

## ==———Passo 4 - Envio das Informações do Fechamento==

### `compiladoFechamentoResumoAnfitriao`

* **Objetivo**: enviar os dados a planilha de fechamento para a planilha de [Compilado Fechamentos](https://docs.google.com/spreadsheets/d/1HDgd7eOk1P23zwJyzAGqR5k5cWDN4jd2kJZ87RXFi0c/edit?gid=1257400142#gid=1257400142), aba Anfitrião
* **Base de Dados**
  * **Sheets**
    * **Própria Planilha**
      * Resumo Anfitrião

### `compiladoFechamentoAnfitriaoImovel`

* **Objetivo**: enviar os dados a planilha de fechamento para a planilha de [Compilado Fechamentos](https://docs.google.com/spreadsheets/d/1HDgd7eOk1P23zwJyzAGqR5k5cWDN4jd2kJZ87RXFi0c/edit?gid=1257400142#gid=1257400142), aba Anfitrião-Imóvel
* **Base de Dados**
  * **Sheets**
    * **Própria Planilha**
      * Anfitrião

### `compiladoFechamentoImovel`

* **Objetivo**: enviar os dados a planilha de fechamento para a planilha de [Compilado Fechamentos](https://docs.google.com/spreadsheets/d/1HDgd7eOk1P23zwJyzAGqR5k5cWDN4jd2kJZ87RXFi0c/edit?gid=1257400142#gid=1257400142), aba Imóveis
* **Base de Dados**
  * **Sheets**
    * **Própria Planilha**
      * Imovel

### `compiladoNFAnfitriao`

* **Objetivo**: enviar os dados a planilha de fechamento para a planilha de [Compilado Fechamentos](https://docs.google.com/spreadsheets/d/1HDgd7eOk1P23zwJyzAGqR5k5cWDN4jd2kJZ87RXFi0c/edit?gid=1257400142#gid=1257400142), aba NF Anfitriões
* **Base de Dados**
  * **Sheets**
    * **Própria Planilha**
      * Notas fiscais

### `compiladoFechamentoModExpAnfitriao`

* **Objetivo**: enviar os dados a planilha de fechamento para a planilha de [Compilado Fechamento - Modelo de Exportação](https://docs.google.com/spreadsheets/d/1r8tQ6i_g5HQSxRkOJRODRjZ8YdCWS_NKLqIvYcVsVlk/edit?gid=401327479#gid=401327479), aba Modelo de exportação - Anfitriões
* **Base de Dados**
  * **Sheets**
    * **Própria Planilha**
      * Mod. Exp. Anfitrião

### `compiladoFechamentoModExpProprietario`

* **Objetivo**: enviar os dados a planilha de fechamento para a planilha de [Compilado Fechamento - Modelo de Exportação](https://docs.google.com/spreadsheets/d/1r8tQ6i_g5HQSxRkOJRODRjZ8YdCWS_NKLqIvYcVsVlk/edit?gid=401327479#gid=401327479), aba Modelo de exportação - props
* **Base de Dados**
  * **Sheets**
    * **Própria Planilha**
      * Mod. Exp. Proprietário

### `pgtoTxImplantacaoCRC`

* **Objetivo**: enviar os abatimentos das taxas de implantação dos imóveis, para a planilha de [Controle CRC_2023.06.21 GKMA](https://docs.google.com/spreadsheets/d/1Q1dV4hkJqfKABiPMsYXY5sLYVVq8l1NyBBediuWqApE/edit?gid=822640047#gid=822640047), aba REC_IMPLANTAÇÃO
* **Base de Dados**
  * **Sheets**
    * **Própria Planilha**
      * Imovel

### `pgtoTxImplantacaoNF`

* **Objetivo**: enviar os dados de taxa de implantação e imóvel, quando houver a finalização dos abatimentos da taxa de implantação do imóvel, para a planilha de [Emissão de NFs de Taxas](https://docs.google.com/spreadsheets/d/1FySZIEhb0XZK1hScT0BJo48-L-QsMxPZZFeS8U7paus/edit?gid=0#gid=0), aba NF Imóvel
* **Base de Dados**
  * **Sheets**
    * **Própria Planilha**
      * Imovel

### `pgtoTxImplantacaoTxFechamento`

* **Objetivo**: enviar os abatimentos das taxas de implantação dos imóveis, para a planilha de [Controle_Taxas_Fechamento](https://docs.google.com/spreadsheets/d/12APg7J31m9QygePPNzfoHymFS4j6MN7_I1_m7TWiC_M/edit?gid=1516985294#gid=1516985294), aba BD_Extrato
* **Base de Dados**
  * **Sheets**
    * **Própria Planilha**
      * Imovel

### `txFranquiaCRC`

* **Objetivo**: enviar os abatimentos das taxas de franquia dos anfitriões, para a planilha de [Controle CRC_2023.06.21 GKMA](https://docs.google.com/spreadsheets/d/1Q1dV4hkJqfKABiPMsYXY5sLYVVq8l1NyBBediuWqApE/edit?gid=822640047#gid=822640047), aba REC_FRANQUIA
* **Base de Dados**
  * **Sheets**
    * **Própria Planilha**
      * Resumo Anfitrião

### `txFranquiaNF`

* **Objetivo**: enviar os dados de taxa de franquia e anfitrião, quando houver a finalização dos abatimentos da taxa de franquia do anfitrião, para a planilha de [Emissão de NFs de Taxas](https://docs.google.com/spreadsheets/d/1FySZIEhb0XZK1hScT0BJo48-L-QsMxPZZFeS8U7paus/edit?gid=0#gid=0), aba NF Anfitrião
* **Base de Dados**
  * **Sheets**
    * **Própria Planilha**
      * Resumo Anfitrião

### `txFranquiaTxFechamento`

* **Objetivo**: enviar os abatimentos das taxas de franquia dos anfitriões, para a planilha de [Controle_Taxas_Fechamento](https://docs.google.com/spreadsheets/d/12APg7J31m9QygePPNzfoHymFS4j6MN7_I1_m7TWiC_M/edit?gid=1516985294#gid=1516985294), aba BD_Extrato
* **Base de Dados**
  * **Sheets**
    * **Própria Planilha**
      * Resumo Anfitrião

### `txFranquiaUploadSapron`

* **Objetivo**: enviar os abatimentos das taxas de franquia dos anfitriões, para a planilha de [Template upload - cobrança de taxa de franquia](https://docs.google.com/spreadsheets/d/1AhZo2AmzXjJLSbRfHDsqv8qT1i99IZXmzaLFYEuE_7U/edit?gid=1805712756#gid=1805712756), aba payments, para upload dos dados no Sapron
* **Base de Dados**
  * **Sheets**
    * **Própria Planilha**
      * Resumo Anfitrião

### `mainConciliacaoFutura`

* **Objetivo**: enviar os valores residuais (Saldo Negativo) ou repasses segurados, dos imóveis para a planilha [04 - Conciliação futura e verificações](https://docs.google.com/spreadsheets/d/1k3fqGBd5bgsGYaRUywe69aa7qWPD22IzV_1XMwuIODA/edit?gid=1400643550#gid=1400643550), aba Saldos em conta props
* **Base de Dados**
  * **Sheets**
    * **Própria Planilha**
      * Imovel

### `cnabCred`

* **Objetivo**: enviar os dados dos imóveis CNA e CNB para a planilha [Acompanhamento saldos CNA - Campos do Jordão](https://docs.google.com/spreadsheets/d/17S9vtalwo8nsZwkh35aOMcSkhRRuwyPubi5ceMtzx5I/edit?gid=0#gid=0), aba Crédito
* **Base de Dados**
  * **Sheets**
    * **Própria Planilha**
      * Imovel

### `cnabAux`

* **Objetivo**: enviar os dados dos imóveis CNA e CNB para a planilha [Acompanhamento saldos CNA - Campos do Jordão](https://docs.google.com/spreadsheets/d/17S9vtalwo8nsZwkh35aOMcSkhRRuwyPubi5ceMtzx5I/edit?gid=0#gid=0), aba Aux
* **Base de Dados**
  * **Sheets**
    * **Própria Planilha**
      * Imovel

### `exportJBV`

* **Objetivo**: enviar os dados dos imóveis JBV para a planilha [Financeiro Pinepin](https://docs.google.com/spreadsheets/d/11PykuPMH9xmYNJc3yDvve1RxU6eVgiDBQP0aaR9nAQU/edit?gid=1990270416#gid=1990270416), aba Pinepin - novo relatório
* **Base de Dados**
  * **Sheets**
    * **Própria Planilha**
      * Imovel

## ==———**Passo 5 - Finalização do Fechamento**==

### `envioDeEmailAnfitriaoNF`

* **Objetivo**: enviar os pdfs gerados pelo código "gerarPdfListaNFAnfitriao", para seu respectivo anfitrião, via email
* **Base de Dados**
  * **Folder**
    * [Prestação de contas](https://drive.google.com/drive/folders/1Pmm2T6sdM8vEngwWWnwtyQdvfC-0IzhJ)
  * **Sheets**
    * **Própria Planilha**
      * Resumo Anfitrião

### `comissaoMadego`

* **Objetivo**: puxar todas as reservas geradas pelos site de reservas da madego
* **Base de Dados**
  * **Sheets**
    * [Conciliação Reservas Sapron](https://docs.google.com/spreadsheets/d/1lP2f1RLk3aV0bhwHFbHG92_ORe36NNlCmUnRg-_tIQs/edit?gid=2097081422#gid=2097081422)
      * API-Stays Mes

### `Fim`

* **Objetivo**: remover todas as fórmulas, deixando apenas os valores estáticos
* **Base de Dados**
  * **Sheets**
    * **Própria Planilha**
      * Todas as abas da planilha

## ==———**Passo 6 - Importar Dados Bancários**==

### `importarDadosImovel`

* **Objetivo**: importar os dados bancários dos imóveis
* **Base de Dados**
  * **Sheets**
    * [3.0 Comparador TEDs](https://docs.google.com/spreadsheets/d/1fPLO33MbJqJ0ROULWDgkevOSlWN63jt9rRdn7nnFt6c/edit?gid=1560402279#gid=1560402279)
      * COPIA_FECH_BANC_PROP

### `importarDadosImovel_anf`

* **Objetivo**: importar os dados bancários dos anfitriões
* **Base de Dados**
  * **Sheets**
    * [3.0 Comparador TEDs](https://docs.google.com/spreadsheets/d/1fPLO33MbJqJ0ROULWDgkevOSlWN63jt9rRdn7nnFt6c/edit?gid=1560402279#gid=1560402279)
      * COPIA_FECH_BANC_ANF