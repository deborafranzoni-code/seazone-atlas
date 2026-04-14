<!-- title: [Parceiros] Atualização de SPOTs disponíveis para reserva | url: https://outline.seazone.com.br/doc/parceiros-atualizacao-de-spots-disponiveis-para-reserva-X3gd0CxVZC | area: Tecnologia -->

# [Parceiros] Atualização de SPOTs disponíveis para reserva

**Como** parceiro,\n**Quero** acessar o SAPRON, visualizar apenas as unidades de Spot disponíveis para reserva,\n**Para** indicar um cliente e acompanhar o status de cada indicação até a conclusão do negócio.\n

### **Descrição**


1. **Visualização de unidades disponíveis**
   * Ao acessar o formulário "Vender Spot", devem ser listadas apenas as unidades com `status = 'disponível'`.
   * Cada item exibido deve conter:
     * Nome do Spot (Empreendimento ID)
     * Código da unidade
2. Inserir dois inputs no formulário\nLogo após o campo "E-mail do investidor", deve ser adicionado uma sessão intitulada "Documentos".\nEsta sessão deve conter dois inputs:\nCNH: input string\nComprovante de residência: input string\n\nAmbos com validação de input url\n 
3. **Reserva automática ao indicar**
   * Ao enviar o formulário de indicação:
     * A indicação deve ser criada no Pipedrive na coluna "Reservado".
     * O `status` da unidade indicada na base de dados deve ser alterado de `disponível` para `reservada`.
     * A unidade não deve mais aparecer para outros parceiros no formulário de "Vender Spot".
     * A indicação deve ser incluída na **Partners Indications Investment, com os ids atualizados de acordo com a tabela de referência.**
     * No momento do encio do formulário devemos checar se a unidade ainda possui o status de disponível na tavela, caso não, retornar mensagem de erro

   \n**Como analista** SZI\n**quero** visualizar as cotas com status atualizado de acordo com as indicações feitas no sapron e de acordo com as colunas do pipedrive\n

   **Movimentação de cards no funil de Vendas Spot**
   * Quando a indicação no Pipedrive for movida para a coluna "Contrato" && ,

     O `status` da unidade na base de dados deve ser alterado para `contrato`. Inserir este status na bd\n
   * Quando a indicação no Pipedrive for marcado como PERDA

     Alterar status da unidade na base de dados para `disponível` novamente (liberando-a para novas indicações).

     Alterar status da indicação na tabela indications para `lost`\n
   * Quando a indicação no Pipedrive for marcado como Ganho

     O `status` da unidade na base de dados deve ser alterado para `vendida`(necessário alterar negociada → vendida) .

     Alterar status da indicação na tabela indications para `won`
   * Visualizar o link dos documentos CNH && comprovante de residência\n\n**Essas alterações serão aplicadas apenas se status comercial do empreendimento ao qual a unidade do card está associada não esteja com o valor** `**marketplace.**`\n\n**Como** parceiro,\n**Quero** acessar o SAPRON, quero visualizar as minhas indicações de reserva de spot\n**Para** acompanhar as indicações realizadas\n\n**Visão para o parceiro (Minhas Indicações)**\n\n**1.** Garantir que os dados das unidades indicadas pelo parceiro, estejam sendo recuperadas a partir da tabela `Unidades` bd szi\n**2.** Os demais dados de indicação devem ser recuperados a partir da tabela indications investiment\n3. Alterar o status de "Em andamento" para "Reservada" (front)\n4.  In progress - status reservada ou contrato, tornar visualização dinâmica

   \

**Tabela de Status da Tabela de Referência** 

| Status na Base de Dados (status) | Origem / Ação | Observação para parceiro |
|----|----|----|
| **disponível** | Estado inicial / unidade ainda não reservada | Unidade aparece como disponível no SAPRON |
| **reservada** | Indicação criada → unidade bloqueada para outros parceiros | Parceiro vê como "Em andamento" |
| **negociada** | Indicação movida para a coluna Contrato no Pipedrive | Parceiro vê como "Em andamento" (até ter TAG de ganho) |
| **disponível** (retorno) | Indicação na coluna Contrato ou diferente de contrato && com TAG Perda | Unidade volta a aparecer como disponível |
| **bloqueada** | Não contemplado neste fluxo, mas reservado para outros casos | Unidade não aparece para parceiros |
| **marketplace** | Fora de escopo desta entrega | Não utilizado neste fluxo |

\n**Cenários Possíveis**

| Cenário | Resultado esperado |
|----|----|
| Parceiro acessa "Vender Spot" | Apenas unidades com status = disponível são listadas. |
| Parceiro indica cliente | Unidade é movida para status = reservada, aparece no Pipedrive em "Reservado". |
| Indicação movida para "Contrato" no Pipedrive | Status da unidade muda para negociada. |
| Indicação em "Contrato" recebe TAG Ganho | Parceiro vê status = Ganho,  |
| Indicação em "Contrato" ou diferente de contrato e com a TAG Perda | Parceiro vê status = Perda, status da unidade volta para disponível (aparece novamente no SAPRON). |
| Unidade com status = bloqueada ou marketplace | **Não aparece no SAPRON para parceiros (fora do escopo).** |

\n\n