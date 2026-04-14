<!-- title: Controle CPG | url: https://outline.seazone.com.br/doc/controle-cpg-IqETCsXniK | area: Administrativo Financeiro -->

# Controle CPG

![](https://www.notion.so/images/page-cover/nasa_space_shuttle_challenger.jpg)

💸

# Controle CPG


 ![](Controle%20CPG%20aba7ce3ed317409fabe70ab824414bef/Repasses%20do%20Fechamento%20(proprieta%CC%81rios)%20e0de5b852fb04592b8e45e22da077d52.html)

[📄Notas Fiscais - Colaboradores](/doc/notas-fiscais-colaboradores-WqTJqpwNLN)

[💙Solicitação Pagamento Caju](/doc/solicitacao-pagamento-caju-fsJDcL8sox)

[💸Processos Contas à Pagar - Omie](/doc/processos-contas-a-pagar-omie-IUoYV1miue)


## Descrição das abas da planilha de contas a pagar

* Colunas brancas com escrita em preto são preenchidas automaticamente via fórmulas e scripts.
* Colunas cinzas com escrita em azul são preenchidas manualmente.
* **Abas de dados e históricos**

  
  1. **BASE_CONFERENCIA_ADMSYS**
  2. **DADOS_COLABORADORES**
  3. **DADOS_NF_COLABORADORES**
  4. **DADOS_PROP**
* **Abas de pagamentos e repasses**

  
   1. **PGTO_REQ**
      * Todos os pagamentos feito via formulário de pedido de pagamentos
      * parte da esquerda da planilha tem a BD
      * a direita tem uma Pivot que mostra o que está aprovado e está em aberto
      * e mais a direita tem uma Pivot que aponta possíveis duplicidades
      * neste caso mesmo se o pagamento estiver aprovado, ele não vai aparecer na Pivot de pagamentos até darmos o check de duplicidade
      * após pagamento, sinaliza com OK o pagamento, insere a data de pagamento e comprovante
   2. **PGTO_PARCELAS**
      * quando alguem sinaliza na REQ que é parcelado, entra nesta aba
      * tem o processo de enriquecimento para garantir que temos todas infos
      * a mesma linha vale durante todas parcelas pois o que conta é a data do ultimo pagamento
   3. **PGTO_RECORRENTE**
   4. **PGTO_DEVOLUCOES**
      * checar no slack
      * executar o pagamento
      * data de vencimento é um SLA hipotético
   5. **PGTO_PARCEIROS**
      * cada vez que sobe uma linha na planilha de parceiros, aparece pra gente
      * prazo de pagamento é d+7
      * lander executa pagamento, marca como pago e preenche tambem na planilha deles (coluna Y é o check que ele preencheu a planiha deles)
      * OBS. tentar linkar a planilha deles na nossa pra dar visibilidade automatica
   6. **PGTO_GESTAO_CONTAS**
      * Mayara (gestão de contas) insere contas novas quando adquirimos novos clientes (colunas A até H)
      * Quando chega uma dessas contas pra pagar, Mayara cadastra nas colunas M - P
      * Tabela dinamica a direita pega as contas que tem data de vencimento mas não tem data de pagamento ainda até o Lander pagar
      * Status da coluna W conforme legenda na própria planilha

      💡

      Treinamento para preenchimento da aba pelo time de Gestão de Contas\n\n<https://drive.google.com/file/d/11R3g_4uGdALLGUFXzR2Hb9DST2PfBpS7/view>\n\n

      \
   7. **PGTO_SALARIOS**
      * puxa da base de RH colaboradores ativos e salarios
      * colaboradores enviam NF e a planilha recebe essas NFs e ja coloca na linha com o nome do colaborador
      * lander abre NF linha a linha, confirmando valor e efetuando pagamento
      * CAJU dos sócios deve vir da base do RH
      * nao fica historico
      * Automação pega o último link
   8. **PGTO_PEOPLE**
   9. **PGTO_COMERCIAL**
  10. **PGTO_REP_STO**
  11. **PGTO_DANOS**
  12. PAGAMENTO VARIÁVEL
  * Time do RH preenche manualmente e pagamos
  * Coisas do comercial, eles preenchem em uma planilha template, mandam pra gente e a gente insere na base
  * Esta bem manual, precisa repensar, apesar de estar funcionando

  \