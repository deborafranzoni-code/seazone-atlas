<!-- title: Comparador de Ted’s | url: https://outline.seazone.com.br/doc/comparador-de-teds-co7uyeDVRU | area: Administrativo Financeiro -->

# Comparador de Ted’s

![](https://www.notion.so/images/page-cover/solid_blue.png)

🗒️

# Comparador de Ted's


\
**Objetivo**

Serve para verificar se os dados utilizados no repasse dos proprietários e anfitriões estão de acordo com os dados do Sapron.


Utiliza a planilha [Dados Fechamento](https://docs.google.com/spreadsheets/d/1oZXuwQAP0CNxWaqScJRd8_yx0T2xhwvfhf8JLDzLPzs/edit?gid=638000386#gid=638000386) e a planilha [2.0 Comparador de teds Sapron](https://docs.google.com/spreadsheets/d/1DpLOTPHoTeslq4Gj2VjSY8FfuIGrD_nQMIXpCDHLahw/edit#gid=209742709) para o cruzamento dos dados


**Abas da Dados Fechamento**

* Contas Proprietários
  * Dados bancários dos proprietários utilizados no fechamento.
  * Deve ser sempre atualizada a cada fechamento.
* Contas Anfitriões
  * Dados bancários dos anfitriões utilizados no fechamento.
  * Deve ser sempre atualizada a cada fechamento.
* Exceções Repasses
  * Exceções que devem ser consideradas na hora do repasse.
    * VLE - Repasse é divido proporcionalmente entre os proprietários
    * Pagamentos que devem ser feitos via pix
* Imóvel Propritário
  * Para atualizar a aba é necessário rodar a macro "Import Imóvel/Prop" no Menu_Dados → Import Metabase.
  * Importa do metabase os dados dos imóveis, como id, repasses que devem ser segurados, status e nome dos proprietários
* E-mails Proprietários
  * Para atualizar a aba é necessário rodar a macro "Import Imóvel/Prop" no Menu_Dados → Import Metabase.
  * Importa do metabase a relação de imóveis x proprietários x e-mails
  * Utilizada para montar a relação de e-mails que devem ser utilizados para envio do aviso pelo marketing do teste de R$ 0,01.


**Abas Comparador de teds Sapron**

* Comparador Proprietários

  Aba que vai puxar os dados da aba **PROP_DADOS_BANC_FECH** e comparar com os dados importados do Sapron
* Comparador Anfitriões

  Aba que vai puxar os dados da aba **ANF_DADOS_BANC_FECH** e comparar com os dados importados do Sapron
* Financial Audit

  Importa os dados da tabela Financial Bank Details Audit do metabase.

  Qualquer alteração de conta fica nessa base e serve de referência para verificação de alterações nos dados feitas pelo proprietários.
* Property_Property

  Importa os dados das contas bancárias do metabase

ANF_BASE_TED_ORIGINAL

PROP_BASE_TED_ORIGINAL

* Fechamento Anfitrião

  Importa o fechamento dos anfitriões da planilha de fechamento (aba resumo anfitrião). Informa os anfitriões que precisam ter os dados verificados
* Fechamento Proprietário

  Importa o fechamento dos imóveis da planilha de fechamento (aba imóvel). Informa os imóveis que precisam ter os dados verificados

**Passo a Passo**


1. Atualizar a aba Imóvel Proprietário da planilha Dados Fechamento.
2. Atualizar a aba E-mails proprietários da planilha Dados Fechamento.
3. Revisar as exceções para repasses na aba Exceções Repasse e se certificar que todas estão marcadas como exceção na aba Contas proprietários na coluna M.
4. Atualizar a aba Property_Property da planilha do comparador de teds rodando a macro Dados Props Sapron através do menu Funções.

   
   1. Com isso a aba PROP_BASE_TED_ORIGINAL vai ser atualizada (via query)
5. Atualizar as abas de fechamento de imóveis e anfitriões da planilha do comparador de teds rodando a macro Dados Fechamento através do menu Funções.

   
   1. Com isso a aba ANF_BASE_TED_ORIGINAL vai ser atualizada (via query)
6. **Atualizar a aba Audit → Implementar atualização via macro**
7. Comparador_Proprietários/Franquias

   
   1. **Dados Corretos:**

      
      1. Nos casos em que os dados cadastrados na base de dados do fechamento e no Sapron estiverem iguais, a flag de dados iguais (Coluna AD) estará como TRUE. Nesses casos, o status da Coluna AB podem ser marcados como OK - Dados Corretos.
      2. Importante verificar se existem dados cadastrados no sapron e na dados fechamento. As colunas de E a O não podem estar vazias.
   2. **Exceção:**

      
      1. Casos de exceção estarão com a coluna J marcada como Sim e os repasses seguirão as instruções da aba Exceções da planilha Dados Fechamento.
      2. Nesses casos o Status da coluna AB podem ser marcados como Exceção. Casos em que o repasse deve ser segurado também estarão marcados como exceção
   3. **Sem dados cadastrados**

      
      1. Se as colunas de E a O estiverem vazias, o imóvel não possui dados bancários cadastrados e deve ser aberto um chamado para o CS.
      2. Nesses casos o Status da coluna AB podem ser marcados como Sem dados cadastrados.
      3. Casos em que o repasse deve ser segurado também estarão marcados como exceção
   4. **Teste R$ 0,01**

      
      1. Casos em que as colunas de E a O estão em branco (dados não estão cadastrados na planilha Dados Fechamento)
      2. Casos em que houve alteração da conta bancária no sapron. A Flag Data Audit (coluna AE) possui uma data.
8. Remessa Teste R$ 0,01

   
   1. Enviada para testar as novas contas cadastradas ou alteradas no Sapron.
   2. Lista de imóveis é passada ao financeiro para fazer a remessa e ao comercial para envio dos e-mails avisando os proprietários.
9. Pontos de atenção:

   
   1. FLAG DUP_PROP (coluna Z)

      
      1. Informase uma mesma conta está cadastrada em mais de um imóvel.
      2. Isso serve para verificar quais contas devem realmente entrar na Remessa R$ 0,01.
      3. Imóveis que não possuem uma conta cadastrada na planilha Dados Fechamento mas que possuem uma conta já cadastrada em outro imóvel, não precisam passar pelo teste R$ 0,01.
      4. Nesses casos as contas podem ser inseridas diretamente na planilha Dados Fechamento.
      5. Cuidar para não duplicar as contas bancárias que devem ser testadas na remessa. Uma mesma conta nova pode estar cadastrada em mais de um imóvel

   \
   \