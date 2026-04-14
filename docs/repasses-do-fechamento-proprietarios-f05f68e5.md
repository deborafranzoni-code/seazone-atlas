<!-- title: Repasses do Fechamento (proprietários) | url: https://outline.seazone.com.br/doc/repasses-do-fechamento-proprietarios-OS7VN7glhd | area: Administrativo Financeiro -->

# Repasses do Fechamento (proprietários)

![](/api/attachments.redirect?id=3e0f0c1d-be7b-4c65-986b-bc56fc247d2a)

# Repasses do Fechamento (proprietários)


\
* **Lista de teds**
  * Validação dos dados bancários:
    * A partir da lista gerada no primeiro dia útil ([LINK](https://docs.google.com/spreadsheets/d/1Tkf29uV4ZFZcbvjofAo_9IHVPri9XY5JlTBE3Pcu-jo/edit#gid=1054570959) - aba "Lista TEDs Malice - @André Warschauer Crescenzo é quem avisa que está pronto para uso), vamos validar as novas contas cadastradas e as contas alteradas com uma transferência de R$ 0,01.
    * Planilha para levantamento de alteração de contas: [Comparador de dados bancários](https://docs.google.com/spreadsheets/d/1S063EijL7MGNc6VxhKDOzW3tzwd8CZOvbwoLsHubA3w/edit#gid=1470444427) (**Roberto está fazendo esse processo**).
    * Antes de efetuar os repasses de R$ 0,01, repassar para o CS a lista de proprietários e imóveis que terão os dados bancários testados.
  * Vamos utilizar a lista gerada pelo André Crescenzo na planilha de [Fechamento mensal do Bizops](https://docs.google.com/spreadsheets/d/1Tkf29uV4ZFZcbvjofAo_9IHVPri9XY5JlTBE3Pcu-jo/edit#gid=1054570959), aba lista de Teds Malice
  * Pontos de atenção (Repassados ao André)
    * Dados bancários Sapron - [Link](https://docs.google.com/spreadsheets/d/1EoeGuHvD3zzLTseKZZbKjODrj9xNMCms82hDo8qbn7A/edit#gid=0)
    * Imóveis com troca de proprietário (evitar o repasse para proprietários novos e antigos)
      * Ver se na lista tem o mesmo imóvel 2x
    * Imóveis com contas de franqueados
    * **Modelo de Remessa BTG**

      As colunas devem conter os dados da seguinte forma:
      * **Conta de Origem:** Sempre será **3822906** - referente a conta da SZN.
      * **Agência de Origem:** Sempre será **0050** - referente a conta da SZN.
      * **Banco do Favorecido:** Referente ao banco do favorecido. Sempre **3 caracteres, formatação de texto e sem caracteres especiais.**
      * **Conta do Favorecido:** Referente a conta do favorecido. **Sem caracteres especiais e com formatação de texto.**
      * **Agência do Favorecido:** Referente a agência do favorecido. Sempre os **primeiros 4 caracteres da agência, formatação de texto e sem caracteres especiais.**
      * **Tipo de Conta do Favorecido:** Referente ao tipo de conta do favorecido. Se o tipo da conta no Sapron for **"Individual_Checking_Account"** ou **"Joint_Checking_Account"**, o tipo na remessa deve ser **"Conta corrente"**. Se o tipo da conta no Sapron for **"Saving_Account"**, o tipo na remessa deve ser **"Conta poupança"**.
      * **Mesma Titularidade:** Sempre **"Não"**. Significa que a conta não é da Seazone.
      * **Nome do Favorecido:** Nome do favorecido exatamente como aparece no banco. **Sem caracteres especiais**.
      * **CPF/CNPJ do Favorecido:** Referente ao CPF/CNPJ do favorecido. Formatação de texto, para **CPF são 11 caracteres e para CNPJ são 14 caracteres**.
      * **Identificação no extrato:** Apenas números e letras, sem caracteres especiais.
      * **Valor:** Valor a ser repassado, retirado da planilha do fechamento. Formatação de número, sem cifrão.
      * **Tipo de transferência:** Pix ou TED (até as 17h).
      * **Data de pagamento:** Data da saída do valor da conta da SZNS. Formatação de data.\n\n

      [BTG_planilha_modelo_pagamento_lote. (3).xlsx](Repasses%20do%20Fechamento%20(proprieta%CC%81rios)%20e0de5b852fb04592b8e45e22da077d52/BTG_planilha_modelo_pagamento_lote._(3).xlsx)
* **Remessas**
  * Vamos criar uma planilha com a remessa completa para acompanhamento e controle das transferências. Essa pode conter campos adicionais como ID do imóvel no Sapron, data de pagamento no contrato (5 ou 10), status e um campo de obs. **(Definindo template com Lander e Roberto)**
  * A planilha deve ser criada na [pasta de baskets](https://drive.google.com/drive/folders/1Zb2-iXvVWqdH9epvT498qr5yWgPgXL1C) enviadas de acordo com o mês de referência.
  * **Exceção de repasses:** Alguns imóveis tem mais de uma conta para repasse ou a divisão do valor. Assim se faz necessário sempre verificar os casos levantados pelo time de fechamento e executar essas transferências uma a uma (poucos casos).
    * Planilha de consulta: [Exceções - Fechamento](https://docs.google.com/spreadsheets/d/1Y5KBDloIEqQ3pEDsC516Aw70SMsMPCCEx8sKd4Iu9WY/edit#gid=438146963)
  * Caso ocorram estornos de transferências via remessa, tentar via pix com os dados bancários antes de pedir a confirmação ao CS.
* Ferramenta de validação de TED's
  * Baseado na remessa de teds completa, vamos fazer o cruzamento dessa lista de pagamentos com o extrato do BTG.
  * Exemplo do que foi feito no último mês: [TED's Bizops](https://docs.google.com/spreadsheets/d/1ADhXThlKqNpkiKcHg9V48vJFUgh65D3eTkfh2anjGHU/edit#gid=0)
    * Importante validar nome do favorecido, valor e possíveis estornos.
    * Essa lista já pode ser utilizada para envio de informações para o Sapron. **(Roberto está verificando com o André os prazos e por onde o André quer receber)**
* Comprovantes de pagamento
  * Continuaram sendo enviados em formato de PDF com todos os comprovantes e uma planilha indicando a página em que o comprovante está
  * Será atualizada diariamente até a finalização dos repasses.
  * Exemplo do último mês: [Relação de página por transferência](https://drive.google.com/drive/folders/1XJu9U_KnZR6hBm8d3yG7RfDGbIChxr0I)
* Fluxo de pedidos de ajuste/alteração nos repasses
  * Vamos criar um novo fluxo no canal de CS para possíveis pedidos de ajustes nos repasses (divergências encontradas no fechamento). Isso facilita a categorização dos repasses e o alinhamento entre as equipes do financeiro, fechamento e CS.
  * Os chamados abertos continuaram a ser encaminhados para a planilha [solicitações](https://docs.google.com/spreadsheets/d/1D44LvEO6MTzueJ65591es4CnmfvZXxR1pdP5B8v4Jcc/edit#gid=860408729) para mantermos um log dos problemas e soluções.
  * Antes os pedidos ficavam perdidos em conversas em diferentes canais o que dificultava a categorização dos valores e futuras auditorias (Exemplo da ZART em bombinhas).


\

\