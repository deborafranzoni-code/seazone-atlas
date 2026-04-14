<!-- title: Controle CRC | url: https://outline.seazone.com.br/doc/controle-crc-MGwJ7PzMzh | area: Administrativo Financeiro -->

# Controle CRC

![](../Fluxo%20de%20Caixa%20a4063094702e4c66a4627bfa67bc7035/FUNDOS_TRELLO_5.png)

📈

# Controle CRC


Planilha CRC: **[Link](https://docs.google.com/spreadsheets/d/1Q1dV4hkJqfKABiPMsYXY5sLYVVq8l1NyBBediuWqApE/edit#gid=1223932848)**

Dono: Gabriel Kennedy

## Descrição das abas da planilha de contas a receber

* Colunas brancas com escrita em preto são preenchidas automaticamente via fórmulas e scripts.
* Colunas cinzas com escrita em azul são preenchidas manualmente.
* **Abas de dados e históricos**

  
  1. **Dados_NFs** - dados e definições contábeis para a emissão de todas as notas da empresa.
  2. **Dados_Proprietários** - dados de todos os proprietários de imóveis da carteira da Seazone. Os nomes e imóveis são importados via importrange da planilha de logins e via script com o restante das informações do metabase de base de dados do Sapron.
  3. **BD NF Emitidas** - log de todas as notas emitidas de todas as empresas do grupo Seazone.(incluindo as canceladas)
  4. **REC_DECOR** e **REC_COWORKING** são **históricos** dessas duas linhas de **receitas** que foram **descontinuadas**.
* **Receitas Seazone Serviços**

  
  1. **REC_GESTAO_CONTAS**
     * Receita referente a mensalidade cobrada pelo serviço de gestão de contas (por imóvel).
     * Da coluna B a coluna N, temos o controle dos imóveis que contrataram o serviço de gestão de contas. Esses dados são inseridos manualmente pelo time de gestão de contas.
       * O valor já pago YTD pode ser conferido na coluna H.
       * O valor pago mensalmente por imóvel (valor da NF) pode ser conferido na coluna J.
     * Da coluna P a coluna AA, temos o controle de emissão de NFs e lançamento de despesa no Sapron. Para cada imóvel é cobrada uma mensalidade e emitida uma NF. Os dados para emissão de cada uma das notas são inseridos manualmente.
       * Pela coluna AA é possível acompanhar o status do lançamento da despesa referente a mensalidade do serviço no Sapron.
     * Para a emissão das notas, temos uma basket para lançamento das NFs de forma automática pela ferramenta [NFE.io](http://NFE.io) (da coluna AH a coluna AW).
       * Os dados da basket são inseridos automaticamente. É necessário apenas copiar e colar os dados na planilha modelo do NFE e fazer a importação dessa planilha na ferramenta.
  2. **REC_OTA**
     * Receita referente ao valor da taxa de OTA Seazone nas reservas via website.
  3. **REC_IMPLANTAÇÃO**
     * Receita referente a taxa de implantação dos novos imóveis. Essa taxa é cobrada para deixar os imóveis nos padrões da Seazone.
     * Da coluna B a coluna E, temos os valores de taxa de implantação de cada imóvel e a forma de pagamento. Esses dados são importados automaticamente da planilha "Handover Comercial > Onboarding".
     * Da coluna F até a coluna T temos o controle de pagamento das taxas e o controle da emissão das NFs.
       * Os dados referentes a taxas e formas de pagamento são inseridos automaticamente.
     * O controle do valor recebido é feito via fórmula a partir do extrato de recebimentos (colunas V até AB). Esse extrato é atualizado manualmente pelo time financeiro (recebimentos em conta, cartão ou boleto) e pelo time de fechamento quando a forma de pagamento escolhida for abatimento.
     * A partir da coluna AH, temos a basket para lançamento das NFs automaticamente através da ferramenta NFE.io. **VERIFICAR SE OS DADOS TEM QUE SER PREENCHIDOS MANUALMENTE.**
  4. **REC_FRANQUIA**
     * Receita referente a venda de novas franquias Seazone.
     * Da coluna B a coluna G, temos os dados referentes a cada franquia vendida pela Seazone importados via script.
     * O controle dos recebimentos é feito nas colunas H-K através dos extratos de recebimentos pela conta da SZN e de abatimentos no fechamento.
       * Os dados de recebimentos são importados automaticamente via script das entradas do admsys da serviços (coluna S a coluna W). O anfitrião a qual o pagamento da taxa de franquia se refere deve ser inserido manualmente na coluna X.
       * Os dados de recebimentos via abatimento são inseridos pelo time de fechamento (coluna Z até coluna AC).
     * Nas colunas AF-AK temos o controle de churn de franqueados (cancelamento de franquias).
       * Os dados são inseridos automaticamente através de um f**luxo de trabalho do slack??**
     * Os dados para a emissão das NFs são inseridos automaticamente nas linhas AM-W sempre que novas franquias são inseridas na planilha.
     * O controle das NFs emitidas é feito de forma manual nas colunas M-P.
       * As NFs são emitidas com o valor total a ser pago pela venda da franquia.
       * Caso o anfitrião cancele o contrato com a SZN sem finalizar o pagamento da taxa, o valor restante é dado como perdido.
  5. **REC_ROYALTY_FRANQ**
     * Receita referente a comissão da Seazone pela gestão digital dos imóveis.
     * Colunas B-E são os valores de comissão do fechamento atual. Os dados são importados automaticamente via script da planilha de fechamento mensal.
     * Colunas G-O apresentam o histórico de comissões dos fechamentos anteriores. Os dados são importados automaticamente da planilha de compilado do fechamento via script.
     * Para a emissão em massa das notas referentes a comissão, temos a basket com os dados da NF nas colunas R-AF
       * Os dados são preenchidos automaticamente.
  6. **REPASSE_STO**
     * Valor a ser repassado ao proprietário dos imóveis no Costão do Santinho referente ao consumo dos hóspedes durante a reserva.
     * **Verificar qual das duas abas é a funcional**
  7. **REC_NO_SHOW**
     * Receita referente aos valores das reservas canceladas que ficam com a Seazone.
     * **Ainda sendo finalizada pelo Bizops**
  8. **REPASSE_DANOS**
     * Repasse a ser feito semanalmente aos proprietários.
     * São inicialmente inseridos via formulário para validação do time de operação e posterior cobrança dos hóspedes pelo time de atendimento.
       * Após a validação do recebimento pela equipe de contas a receber, os danos entram linha a linha na planilha para então serem reembolsados aos proprietários.
* **Receitas Seazone Investimentos**

  
  1. **REEMBOLSO_SPE**
     * Valor referente aos custos arcados pela SZN inicialmente (arras de terreno, viabilidades)
     * Da coluna B a coluna N, temos o controle de recebimento dos reembolsos de cada empreendimento (incluindo os empreendimentos cancelados).
       * Os valores e datas previstas para o reembolso são inseridos manualmente seguindo o trello e a documentação financeira da SPE.
       * Para os empreendimentos que ainda não foram finalizados, temos o valor estimado do reembolso a ser feito e a data prevista para tal.
     * Da coluna P a coluna S, temos o extrato dos reembolsos já realizados que são importados manualmente das abas de entrada do admsys da investimentos.
     * O status do recebimento pode ser acompanhado na coluna N.
  2. **REC_ESTRUTURAÇÃO**
     * Receita referente à prestação de serviços por parte da SZN a SPE de um empreendimento pela concepção, viabilização, acompanhamento e fiscalização do que foi estruturado e será implantado.
     * Da coluna B a coluna O, temos o controle de recebimento da taxas de estruturação de cada empreendimento da Seazone.
       * Os valores e datas previstas para o recebimento são inseridos manualmente seguindo o trello gerencial (controle feito pelos times financeiro e compliance) e a documentação financeira da SPE.
       * Para os empreendimentos que ainda não foram finalizados, temos o valor estimado da taxa (J) e a data prevista para recebimento (K).
       * Nas colunas N e O temos o controle da emissão das NF's referentes as taxas recebidas, sendo a data da emissão da nota em N e o status da emissão em O.
     * Da coluna Q a coluna X, temos o extrato dos pagamentos já realizados pelos empreendimentos e os links e datas das NFs associadas a cada recebimento. Os dados são importados manualmente das entradas do admsys da investimentos.
     * Mais a direita (da coluna Z a AD) temos uma tabela dinâmica que mostra as NFs que ainda precisam ser emitidas. —> DELETAR DA PLANILHA
  3. **REC_COMISSAO_SZI**
     * Receita referente a comissão pela venda de unidades Spots.
     * Da coluna B a coluna R, temos o controle de recebimento das comissões de vendas das unidades dos empreendimentos da Seazone.
       * As informações referentes a cada empreendimento são importadas manualmente do trello gerencial. O restante dos dados tem preenchimento automático de acordo com o extrato.
     * Da coluna V a coluna AE, temos os valores a serem recebidos por unidade de cada empreendimento, sendo que são comparados os valores no contrato e os inseridos no pipedrive pela equipe do comercial.
       * Os dados dos contratos são importados manualmente do canal #szni-comercial-financeiro do slack. A cada contrato assinado, um aviso é gerado automaticamente com os dados do contrato no canal.
       * Os dados do pipe são importados automaticamente.
       * Pagamentos já realizados pelos empreendimentos são inseridos manualmente de acordo com as entradas do admsys da investimentos.
       * A coluna AA é utilizada para controle de valores divergentes entre pipedrive e valor de contrato.
       * É possível ter a emissão de duas notas para uma mesma cota vendida. Esses casos acontecem quando são vendas divididas entre corretor e imobiliária, por exemplo.
         * São feitos dois pagamentos para CNPJs diferentes e a emissão de duas notas diferentes.
     * Da coluna AF a coluna AK, temos as notas emitidas pelo recebimento das comissões.
       * O link da da pasta com as NFs associadas a cada empreendimento é inserido na coluna AI.
     * Por fim, temos os dados vindos do pipedrive da SZNI (coluna AM a coluna AZ) referentes as vendas e os parceiros que efetuaram cada uma delas (podendo ser um parceiro terceiro ou a própria SZNI). Esses dados são importados de forma automática.
     * **VERIFICAR A SITUAÇÃO DO MARKETPLACE —> SE AINDA É CONSIDERADO UM PARCEIRO OU SE VOLTA A SER VENDA SZNI**
  4. **REC_MKT**
     * Vai ser descontinuada
     * Volta a ser considerada uma venda interna
     * Repasse de cota: cotas revendidas pelo comercial da SZNI
       * Recebemos a comissão duas vezes (uma da SPE da venda primária, e a segunda do novo comprador)
     * Venda de terceiros

  \


[💵Recebimento Taxa Estruturação SZI](/doc/recebimento-taxa-estruturacao-szi-bqeDMgrda9)

[💵Recebimento Comissão SZI](/doc/recebimento-comissao-szi-DsHKlB1Kre)

[💵Dash Invoice](/doc/dash-invoice-gokWTTVDeS)

[💵REC_Dados](/doc/rec_dados-rlEs4deKCZ)

[💵REC_TAXAADM_POOL](/doc/rec_taxaadm_pool-3oh8vO6mdY)

[💵Recebimento Comissão REC_VISTORIA](/doc/recebimento-comissao-rec_vistoria-seOh9H0Jkz)

[💵Recebimento Comissão REC_PROJETO](/doc/recebimento-comissao-rec_projeto-p3wi7ukC5U)

[💵Recebimento Comissão SZI MKTPLACE](/doc/recebimento-comissao-szi-mktplace-4iV64CtwaW)

[💵Recebimento Reembolso Empreendimentos](/doc/recebimento-reembolso-empreendimentos-eslhQXoRnN)

[📝Recibos Hóspede](/doc/recibos-hospede-gopwvfqFHL)

[📝Danos](/doc/danos-goXG3vxDAg)

[🏦 Saque plataformas](/doc/saque-plataformas-jEKJaZx5Fo)

[🤑Repasse Comissão do Spot SZI para Seazoner](/doc/repasse-comissao-do-spot-szi-para-seazoner-KKPXztopV0)

[📄Gestão de Contas - Controle_CRC, NFs e Sapron.](/doc/gestao-de-contas-controle_crc-nfs-e-sapron-eIpqg8EFki)

[📄Taxa de Implantação - Controle_CRC e NFs.](/doc/taxa-de-implantacao-controle_crc-e-nfs-Wz938JR9HE)

[📄Taxa de Franquia e Royalties - Controle_CRC e NFs.](/doc/taxa-de-franquia-e-royalties-controle_crc-e-nfs-apzBSB373Z)