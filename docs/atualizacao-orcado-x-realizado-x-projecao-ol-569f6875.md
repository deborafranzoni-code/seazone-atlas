<!-- title: Atualização Orçado x Realizado x Projeção [OL | url: https://outline.seazone.com.br/doc/atualizacao-orcado-x-realizado-x-projecao-ol-dKMJpzeUkC | area: Administrativo Financeiro -->

# Atualização Orçado x Realizado x Projeção [OL

![](https://www.notion.so/images/page-cover/solid_beige.png)

📊

# Atualização Orçado x Realizado x Projeção \[OLD\]


Link da planilha: **[Planilha OrçadoxRealizadoxProjeção](https://docs.google.com/spreadsheets/d/1lMoivuBTy7TGGi-Bsq_wmy7yat0KD_8o5UtQM5p5F_g/edit#gid=1457615361)**\n\n


1. Verificar se existe alguma categorização em aberto no mês a ser atualizado em cada um dos Admsys:
   * **[Admsys Seazone Serviços](https://docs.google.com/spreadsheets/d/1YHvus3u692wr75lO_SDJgYuCo6kPqcLh9VxJ5WQ7GhQ/edit):** abas de entrada, saída, CNAB e cartão de crédito.
     * **Banco Inter:** Entrada, saída e cartão de crédito;
     * **Banco Sicoob:** Entrada, saída e cartão de crédito;
     * **Banco Sicredi:** Entrada, saída, cartão de crédito e CNAB;
     * **Banco BTG:** Entrada, saída.
   * **[Admsys Seazone Investimentos](https://docs.google.com/spreadsheets/d/1czZEE6ajQDyaPgXQra9zBgaFvXXkhgUbLqGI7YQZcSM/edit#gid=274702885):** abas de entrada, saída e cartão de crédito.
     * **Banco Inter:** Entrada, saída e cartão de crédito;
     * **Banco Sicoob:** Entrada, saída e cartão de crédito.
   * **[Admsys Khanto:](https://docs.google.com/spreadsheets/d/1L6vm5RINTTpXV-80Hih0-W2GIFoCX8jlYhflEtACguc/edit#gid=274702885)** abas de entrada e saída.
     * **Banco Sicredi:** Entrada e saída.
   * **[Admsys Marketplace:](https://docs.google.com/spreadsheets/d/1hiRRB-eqXVe8GgOFLa-B8lIGacX8yc9PChlTzeFBNTY/edit#gid=1797358744)** abas de entrada e saída.
     * **Banco BTG:** Entrada e saída.
   * **[Admsys Holding:](https://docs.google.com/spreadsheets/d/1MhdH237LfRloOmq2_za-UdOkaR-l-m7vKSSiZnJAhMU/edit#gid=773447403)** abas de entrada e saída.
     * **Banco Sicoob:** Entrada e saída.

   Caso alguma categorização esteja faltando, comunicar o setor financeiro através do canal categorizações-admsys no slack.
2. Despesas Mensais
   * As alterações devem ser feitas na aba "Despesas Mensais".
   * Alterar o cabeçalho do mês de projetado para realizado na linha 5.
   * Alterar a fórmula nas células da coluna do projetado do mês para que as despesas sejam puxadas da aba "Admsys Consolidado Saídas" e não mais da aba "Despesas Mensais Estática. A alteração pode ser feita copiando a fórmula do realizado do mês anterior na do mês que está sendo atualizado. Exemplo para o mês de junho
     * Fórmula projeção: =SOMA(SEERRO(filter('Despesas Mensais Estática'!V$6:V;'Despesas Mensais Estática'!$D$6:$D=$D73;'Despesas Mensais Estática'!$C$6:$C=$C73;'Despesas Mensais Estática'!$B$6:$B=$B73;'Despesas Mensais Estática'!$A$6:$A=$A73);0))
     * Fórmula do realizado: =SOMA(SEERRO(filter('Admsys Consolidado Saidas'!$C:$C;'Admsys Consolidado Saidas'!$E:$E=$A6;'Admsys Consolidado Saidas'!$F:$F=$B6;'Admsys Consolidado Saidas'!$G:$G=$C6;'Admsys Consolidado Saidas'!$H:$H=$D6;'Admsys Consolidado Saidas'!$K:$K=T$2;'Admsys Consolidado Saidas'!$L:$L=T$3);0))
3. Receitas Mensais
   * Os valores das receitas devem ser inicialmente colocados na **[00 - Base de dados central Seazone Serviços.](https://docs.google.com/spreadsheets/d/1Gy_TiV9Dq9nAvNyHSVCSZ9323JhoKQQfpMlAPfvKqD4/edit#gid=1959584655)**
     * Na aba "Faturamento" incluir as receitas da Seazone de acordo com o regime.

| Categoria | Empresa | Regime | Origem dos dados | OBS |
|:---|:---|:---|:---|:---|
| Comissão venda de reservas diretas | SZNS | Caixa | Valor da taxa de OTA Seazone nas reservas via website. Comissão = 1/9 Receita Stays do fechamento | Não é a receita stays do fechamento (Esse valor já é o líquido descontando essa taxa da SZN. |
| Implantação de novos Imóveis | SZNS | Competência | Soma da taxa de implantação do handover do PMS do mês indicado. | Coluna K da aba Handover Comercial > Onboarding da **[00 - Banco de dados PMS](https://docs.google.com/spreadsheets/d/1u6C2KtkJqDvR6-ZKDRLsLKZ5leaAnYPp78tTG3v6NXo/edit#gid=228443289&fvid=1830693420)** |
| Comissão de Imóveis em Resorts | SZNS | Caixa | Comissão total dos imóveis em Resort | Filtrar a aba de anfitriões do fechamento pelo anfitrião Seazone (Coluna H) |
| Royalty das Franquias | SZNS | Caixa | Comissão da Seazone nos imóveis residenciais | Filtrar a aba de anfitriões do fechamento tirando o anfitrião Seazone e vendo o valor total da NF emitida pela empresa (Coluna Y) |
| Venda de Franquia | SZNS | Competência | Valor total de venda de franquias no mês | Verificar se continua sendo na Controle Anfitriões<br>O valor pode ser obtido na aba TxFranquia da planilha<br>**[00 - Controle Anfitriões](https://docs.google.com/spreadsheets/d/1ikd5XQrf4kiv5v4l1LZLzMaWRKzE6D8pOuPcqiB5AqI/edit#gid=1025811388).** |
| Taxa de cancelamento de reservas | SZNS | Caixa |    |    |
| Gestão de contas | SZNS | Caixa | Mensalidade cobrada por imóvel pelo serviço de gestão de contas | O valor pode ser obtido através da relação de NFs emitidas no mês |
| Venda de Franquia | SZNS | Caixa | Valor pago/abatido do valor total da taxa de franquia no mês | O valor pode ser obtido através da relação de NFs emitidas no mês |
| Implantação de novos Imóveis | SZNS | Caixa | Valor pago/abatido do valor total da taxa de implantação no mês | O valor pode ser obtido através da relação de NFs emitidas no mês |
| Venda marketplace | SZNS | Caixa | Valor recebido de comissões de venda | O valor pode ser obtido através da relação de NFs emitidas no mês |
| Receita Decor | SZNI | Caixa | Taxa de consultoria | O valor pode ser obtido através da relação de NFs emitidas no mês |
| Receita Investimentos | SZNI | Caixa | Taxa de estruturação, comissão de vendas e Reembolso | O valor pode ser obtido através da relação de NFs emitidas no mês |
   * Após a atualização da base de dados, é necessário fazer as seguintes alterações na aba ["Receitas Mensais Caixa"](https://docs.google.com/spreadsheets/d/1lMoivuBTy7TGGi-Bsq_wmy7yat0KD_8o5UtQM5p5F_g/edit#gid=1474342056) e na aba ["Sumário"](https://docs.google.com/spreadsheets/d/1lMoivuBTy7TGGi-Bsq_wmy7yat0KD_8o5UtQM5p5F_g/edit#gid=624345387) da planilha.

   
   1. **Receitas Mensais Caixa**

      
      1. Alterar o cabeçalho do mês de projetado para realizado na linha 7.
      2. Alterar as fórmulas das colunas C e D da aba Receitas Mensais Caixa somando a célula da coluna orçado do mês atualizado na coluna C e a célula da coluna realizado do mês atualizado na coluna D. Exemplo:

         ![](/api/attachments.redirect?id=9d4ddfcb-5ad8-42c5-af6b-60e2ee70d66c)
   2. **Sumário**

      
      1. Alterar o cabeçalho do mês de projetado para realizado na linha 7.
      2. Alterar as fórmulas das colunas C e D da aba Sumário somando a célula da coluna orçado do mês atualizado na coluna C e a célula da coluna realizado do mês atualizado na coluna D. Exemplo:

         ![](/api/attachments.redirect?id=cd099338-9caf-4dbc-b581-42887e0081ce)

   \