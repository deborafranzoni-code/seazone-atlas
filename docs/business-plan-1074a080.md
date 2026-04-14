<!-- title: Business Plan | url: https://outline.seazone.com.br/doc/business-plan-RUYq3kuoBx | area: Administrativo Financeiro -->

# Business Plan

![](/api/attachments.redirect?id=1c010a85-731d-4334-9219-e35af2ceddf6)

🗓️

# Business Plan


# Etapas


1. Definir a estrutura da projeção
2. Projeção de gastos e receita

   
   1. Listar todas as receitas e despesas de cada parte do modelo de negócio
   2. Pesquisar as premissas para cada conta da projeção
   3. Calcular como cada receita/despesa se comporta no prazo da projeção

   Na projeção das saídas é necessário identificar todos os gastos, setor por setor, incluindo desde as despesas recorrentes (folha de pagamento, custos operacionais, materiais e contas gerais) até as despesas planejadas no período (como novas contratações e novos investimentos em ferramentas).\n\nNa projeção da receita é necessário incluir todas as linhas de receita da empresa para determinar a base da previsão financeira o que possibilita a tomada de decisões em diferentes frentes, como precificação, estoque de materiais e produção.\n
3. Unir as contas em uma visão integrada
4. Verificar o alinhamento do time com o volume de investimento
5. Validar os números (sense-check)


---

# Estrutura

## Sumário Financeiro Anual e Mensal

* Sumário Financeiro Mensal

|    |    | Mês 1 … Mês Final | Total |
|:---|:---|:---|:---|
| Total de Imóveis |    | Importar da Projeção de Receita Residencial + Resorts | Valor do último mês |
| Unidades Spot estruturadas |    | Importar da Projeção de Receita SZI | Valor do último mês |
|    |    |    |    |
| Receita Bruta | Receita Total | SOMA("Receita Seazone Serviços";"Receita Seazone Investimentos") | Soma de todos os meses |
| Receita Seazone Serviços | Receita Seazone Serviços | SOMA("Implantação Novos Imóveis";"Venda de Franquia";"Comissão venda de reservas diretas";"Royalt das franquias";"Comissão de imóveis em resorts") | Soma de todos os meses |
| Seazone Serviços | Implantação de novos imóveis | Importar da Projeção de Receita Residencial + Resorts | Soma de todos os meses |
| Seazone Serviços | Venda de franquia | Importar da Projeção de Receita Residencial | Soma de todos os meses |
| Seazone Serviços | Comissão venda de reservas diretas | Importar da Projeção de Receita Residencial + Resorts | Soma de todos os meses |
| Seazone Serviços | Royalty das Franquias | Importar da Projeção de Receita Residencial | Soma de todos os meses |
| Seazone Serviços | comissão de imoveis em resorts | Importar da Projeção de Receita Resorts | Soma de todos os meses |
| Receita Seazone Investimentos | Receita Seazone Investimentos | SOMA("Taxa de Estruturação";"Comissão de venda") | Soma de todos os meses |
| Seazone Investimentos | Taxa de Estruturação | Importar da Projeção de Receita SI | Soma de todos os meses |
| Seazone Investimentos | Comissão de venda | Importar da Projeção de Receita SI | Soma de todos os meses |
| Reembolsos | Reembolso total |    |    |
| Seazone Investimentos | Reembolsos | Importar da Projeção de Receita SI | Soma de todos os meses |
| Impostos | Total | Soma Impostos SZS e SZI | Soma de todos os meses |
|    | Seazone Serviços | Importar linha "Valor Imposto Mensal" das abas Cálculo Impostos SZS e Cálculo Impostos Khanto Reservas | Soma de todos os meses |
|    | Seazone Investimentos | Importar linha "Valor Imposto Mensal" das abas Cálculo Impostos SZI e Cálculo Impostos Marketplace | Soma de todos os meses |
| Custo pessoal |    | SOMA("Custo pessoal SS";"Custo Pessoal SI") | Soma de todos os meses |
| Seazone Serviços | Custo pessoal | Importar da aba Despesas RH quando a Empresa for Seazone Serviços | Soma de todos os meses |
| Seazone Investimentos | Custo pessoal | Importar da aba Despesas RH quando a Empresa for Seazone Investimentos | Soma de todos os meses |
| Custos Operacionais |    | SOMA("Custos abaixo") | Soma de todos os meses |
| Seazone Serviços | Custos escaláveis | Importar da aba Despesas Mensais quando a empresa for Seazone Serviços e o custo for Escalável | Soma de todos os meses, exceto Impostos |
| Seazone Serviços | Despesas | Importar da aba Despesas Mensais quando a empresa for Seazone Serviços e o custo for não Escalável | Soma de todos os meses |
| Seazone Investimentos | Custos escaláveis | Importar da aba Despesas Mensais quando a empresa for Seazone Investimentos e o custo for Escalável | Soma de todos os meses |
| Seazone Investimentos | Despesas | Importar da aba Despesas Mensais quando a empresa for Seazone Investimentos e o custo for não Escalável | Soma de todos os meses |
| Khanto Reservas | Custos escaláveis | Importar da aba Despesas Mensais quando a empresa for Khanto Reservas e o custo for Escalável | Soma de todos os meses |
| Khanto Reservas | Despesas | Importar da aba Despesas Mensais quando a empresa for Khanto Reservas e o custo for não Escalável | Soma de todos os meses |
| Seazone Marketplace | Custos escaláveis | Importar da aba Despesas Mensais quando a empresa for Seazone Marketplace e o custo for Escalável | Soma de todos os meses |
| Seazone Marketplace | Despesas | Importar da aba Despesas Mensais quando a empresa for Seazone Marketplace e o custo for não Escalável | Soma de todos os meses |
| Seazone Holding | Custos escaláveis | Importar da aba Despesas Mensais quando a empresa for Seazone Holding e o custo for Escalável | Soma de todos os meses |
| Seazone Holding | Despesas | Importar da aba Despesas Mensais quando a empresa for Seazone Holding e o custo for não Escalável | Soma de todos os meses |
| Lucro/Prejuízo |    | =Receita Bruta - Custo pessoal - Custos Operacionais | Soma de todos os meses |
| Fluxo de Caixa acc | Inserir valor em caixa hoje | Mês 1: Valor em caixa + lucro/prejuízo<br>Meses subsequentes: Fluxo de caixa mês anterior + Lucro/Prejuízo<br> | MÍNIMO no período |
| Aporte | Inserir valor de aporte buscado |    |    |
| Valuation | Multiplicador do valuation | "Faturamento dos últimos 12 meses"\*"Multiplicador do valuation" | MÁXIMO no período |
* Sumário Financeiro Anual

  Igual ao Sumário Anual, porém condensado para mostrar os valores ano a ano. Deve ser feito copiando as colunas A e B do mensal e utilizando uma fórmula de SOMA(FILTER para os valores daquela linha em que o mês esteja dentro do ano.

  Exceções:

  
  1. O "fluxo de caixa acc", que será o valor mínimo do ano
  2. # Imóveis, Unidades Spot estruturadas e Valuation, que será o valor em dezembro
* DRE Projetada

  Construir a aba para a projeção das DRE para todos os anos inclusos no BP:

|    |    |    |
|:---|:---|:---|
|    |    | Cálculo |
| Receita Bruta | Receita Total | Soma de todas as fontes de receita abaixo |
|    | Implantação de novos imóveis | Importar do sumário anual |
|    | Venda de franquia | Importar do sumário anual |
|    | Comissão venda de reservas diretas | Importar do sumário anual |
|    | Royalty das Franquias | Importar do sumário anual |
|    | comissão de imoveis em resorts | Importar do sumário anual |
|    | Taxa de Estruturação | Importar do sumário anual |
|    | Comissão de venda | Importar do sumário anual |
| Reembolso | Total | Importar do sumário anual |
| Impostos |    |    |
|    | ISS,PIS,COFINS | Importar das abas de Cálculo do Imposto |
| Receita Líquida |    | Receita Total - (ISS, PIS, COFINS) |
| Custos Operacionais |    | Soma dos Custos Operacionais Fixos e Variáveis |
| Fixo | Colaboradores, OTAs | Custo anual das posições da aba "Despesas RH" e "Despesas Mensais" marcadas como Despesa Operacional e Fixo |
| Variável | Seazone Serviços | Custo anual das posições da aba "Despesas RH" e "Despesas Mensais" marcadas como Despesa Operacional, Variável e da empresa Seazone Serviços |
| Variável | Seazone Investimentos | Custo anual das posições da aba "Despesas RH" e "Despesas Mensais" marcadas como Despesa Operacional, Variável e da empresa Seazone Investimentos |
| Lucro Bruto |    | Receita Total - Custos Operacionais |
|    | Margem (lucro bruto / receita total) | "Lucro Bruto"/"Receita Total" |
| Despesas Reembolsáveis |    |    |
| Variável | Mídia Off, Terrenos, Projetos e Viabilidade | Custo anual das posições da aba "Despesas RH" e "Despesas Mensais" marcadas como Despesa Reembolsável e Variável |
| Despesas Comerciais |    | Soma despesas comerciais fixas e variáveis |
| Fixo | Times de Venda e Pre-venda | Custo anual das posições da aba "Despesas RH" e "Despesas Mensais" marcadas como Despesa Comercial e Fixo |
| Variável | CRM | Custo anual das posições da aba "Despesas RH" e "Despesas Mensais" marcadas como Despesa Comercial e Variável |
| Despesas de Marketing |    | Soma despesas marketing fixas e variáveis |
| Fixo | Colaboradores, Agência, Gestão de Leads | Custo anual das posições da aba "Despesas RH" e "Despesas Mensais" marcadas como Despesa Marketing e Fixo |
| Variável | Ads, Branding e mídia offline | Custo anual das posições da aba "Despesas RH" e "Despesas Mensais" marcadas como Despesa Comercial e Variável, exceto "Comissão Parceiro Corretor" |
| Variável | Corretagem | Custo anual da "Comissão Parceiro Corretor" |
| Despesas Administrativas |    | Soma despesas administrativas fixas e variáveis |
| Fixo | Colaboradores, S.I.G., Materiais | Custo anual das posições da aba "Despesas RH" e "Despesas Mensais" marcadas como Despesa Administrativa e Fixo |
| Variável | Viagens | Custo anual das posições da aba "Despesas RH" e "Despesas Mensais" marcadas como Despesa Administrativa e Variável |
| Margem Operacional (EBIT) |    | Somar todas as despesas, exceto financeiras e impostos sobre lucro e subtrair da Receita Bruta |
|    | Margem (EBIT / receita total) | "Margem Operacional"/"Receita Bruta" |
| Despesas Financeiras |    | Somas das despesas financeiras |
| Fixo | Despesas Financeiras | Custo anual das posições da aba "Despesas RH" e "Despesas Mensais" marcadas como Despesa Financeira e Fixo |
| Fixo | IRPJ, CSLL | Impostos IRPJ e CSLL das abas de Cálculo Imposto de todas as empresas |
| Lucro Líquido |    | Receita Bruta - Despesas |
| Investimento |    |    |
| Capex Tecnologia |    |    |
| Fixo | Equipamentos e Desenvolvimento | Custo anual das posições da aba "Despesas RH" e "Despesas Mensais" marcadas como Despesa Tecnologia e Fixo |
| Empréstimo | Amortização | Custo anual de gastos com Empréstimos |
| Fluxo de Caixa |    |    |
|    | Fluxo de caixa acc | Valor Mínimo no ano |
| Valuation |    | Valor em dezembro de cada ano |

## Projeção de Receita SNZS


1. Premissas
   * Premissas que podem ser editadas:
     * Taxa de limpeza média: valor médio pago por limpeza a cada reserva em um imóvel. Influência somente a projeção de receitas de imóveis residenciais. Imóveis localizados em resorts não possuem taxa de limpeza.
     * Taxa de implantação média: valor médio cobrado do proprietário para a execução da implantação do imóvel, sendo todos os atos para a disponibilização do imóvel administrado para a locação dentro dos padrão Seazone (adequação, fotos profissionais, vistoria, criação de anúncios, etc…). A taxa pode ser cobrada tanto de imóveis do tipo residencial, quanto para imóveis em resorts/hotéis.
     * % OTA Seazone: taxa cobrada sobre o valor da reserva feita no website da Seazone. Esse valor inclui a taxa cobrada pelo meio de pagamento utilizado pelo hóspede (pagar.me, paypal).
     * % locações pelo website da Seazone: porcentagem das reservas vindas diretamente do website da Seazone.
     * Comissão Seazone: porcentagem média cobrada do proprietário do imóvel pela prestação do serviço de gestão completa. Depende do tipo do imóvel (Residencial ou Resort)
     * Imóveis via parceiro: porcentagem de imóveis que chegam a Seazone via indicação de parceiros.
     * Taxa de franquia: valor médio cobrado pela venda de uma nova franquia a um novo anfitrião.
     * Comissão do franqueado: porcentagem da receita que o anfitrião recebe por imóvel.
     * Trigger para novo franqueado: gatilho para uma nova franquia em uma determinada região.
     * Taxa de churn de imóveis: porcentagem de imóveis que cancelam o contrato com a Seazone.
     * Data inicial e data final: período inicial e final da projeção respectivamente.
     * Comissão por indicação do imóvel: comissão paga ao parceiro por imóvel indicado.
   * Premissas iniciais fixas

     Essas premissas precisam ter seus valores iniciais levantados e inseridos na planilha antes da projeção. São separadas por regiões de atuação.
     * Regiões de atuação
     * Tipo dos imóveis na região: se os imóveis são do tipo residencial (2) ou resort/hotel (1).
     * Data de início da operação na região
     * Número de imóveis iniciais na região
     * Faturamento anual total
     * Reajuste anual
     * Taxa comercial: número de novos imóveis na região mensalmente
     * Distribuição do faturamento ao longo do ano
     * Número de reservas no mês
     * Número inicial de franqueados na região
     * Ponto de saturação: número máximo de imóveis em operação em cada região
2. Projeção de Receitas Residenciais
   * Para a projeção das receitas residenciais é necessário rodar a função "mainProjecaoFase2" através de uma macro. Essa pode ser encontrada no menu de Macros Planejamento → Projeção de Receitas → Residenciais.

     ![](/api/attachments.redirect?id=f477cd51-9e36-4727-88e6-cb22ac08e470)

     Essa função chama 2 outras funções, uma função que estrutura o template da aba definindo suas linhas, colunas e o período da projeção (de acordo com as premissas de data inicial e final) e a função "projecaoFase2" que realiza os cálculos da projeção.\n\nPega todas as regiões com imóveis especificados como sendo residenciais da aba de premissas (Coluna B = 2). Faz inicialmente o calculo da projeção para cada uma das regiões de acordo com o mês da projeção (Linha 23 em diante da aba de projeção). Em seguida, com os a projeção da região feita, são calculados os dados dos imóveis (Linhas 3 a 12) e os dados de comissões e faturamento.\n
     * Para o primeiro mês da projeção:
       * Número de reservas: premissa de quantidade de reservas no mês \* premissa de número de apartamentos iniciais;
       * Número de novos imóveis: são considerados somente os imóveis iniciais e portanto o número de novos imóveis é 0;
       * Número de imóveis: premissa de número de imóveis iniciais;
       * Número de novos franqueados:
         * Se o número de imóveis é > 0:
           * Se a premissa de número de franqueados iniciais for > 0, é = premissa de número de franqueados iniciais.
           * Se a premissa de número de franqueados iniciais for = 0, o número de novos franqueados é projetado como 1.
           * Se a divisão dos imóveis entre os franqueados for maior que o número máximo de imóveis que o franqueado pode operar (imoˊveismfranqi>novoFranqtrigger{imóveis_m \\over franq_i} > novoFranq_{trigger}franqi​imoˊveism​​>novoFranqtrigger​﻿ ), o número de novos franqueados será:

           imoˊveism−(franqi ∗ novoFranqtrigger)novoFranqtrigger{imóveis_m - (franq_i \\space \* \\space novoFranq_{trigger}) \\over novoFranq_{trigger}}novoFranqtrigger​imoˊveism​−(franqi​ ∗ novoFranqtrigger​)​
         * Se o número de imóveis é 0, o número de novos franqueados também será 0.
       * Número de franqueados: premissa de número de franqueados iniciais somada ao número de novos franqueados.
     * Para os meses seguintes da projeção:
       * Número de reservas: premissa de quantidade de reservas no mês \* número de imóveis no mês de projeção.
       * Número de novos imóveis:
         * Se o número total de imóveis é menor que a premissa de saturação da região, o número de novos imóveis é a premissa de taxa comercial da região (Coluna G).
         * Se o número total de imóveis é maior ou igual a premissa de saturação, o número de novos imóveis é 0.
       * Número de imóveis: número de imóveis do mês anterior somado ao número de novos imóveis.
       * Número de novos franqueados:
         * Se o número de imóveis é > 0:
           * Se o número de franqueados no mês anterior for zero, o número de novos franqueados é 1.
           * Caso contrário, o número de novos franqueados é:

           imoˊveism−(franqm−1 ∗ novoFranqtrigger)novoFranqtrigger{imóveis_m - (franq_{m-1} \\space \* \\space novoFranq_{trigger}) \\over novoFranq_{trigger}}novoFranqtrigger​imoˊveism​−(franqm−1​ ∗ novoFranqtrigger​)​
         * Se o número de imóveis é 0, o número de novos franqueados também será 0.
       * Número de franqueados: número de franqueados do mês anterior somado ao número de novos franqueados.

     Com a projeção concluída, são compilados os dados dos imóveis em todas as regiões de atuação por mês:
     * Total de imóveis
     * Total de reservas
     * Total de novos imóveis
     * Total de franqueados
     * Total de novos franqueados
     * Total de regiões
     * Total de novas regiões
     * Total de churns
     * Faturamento total dos imóveis
     * Faturamento total com limpezas

     Com os dados compilados, são calculadas as comissões e faturamentos totais:
     * Comissão do parceiro
       * Comissão paga aos parceiros que indicaram imóveis para a SZN. É o faturamento total multiplicado pela premissa de comissão por indicação de imóveis multiplicado pela premissa de imóveis via parceiro.

     Comp=Fatt ∗ Comind ∗ IndImoveispCom_p = Fat_t \\space \* \\space Com_{ind}\\space \* \\space IndImoveis_{p}Comp​=Fatt​ ∗ Comind​ ∗ IndImoveisp​
     * Faturamento dos franqueados com diárias
       * Faturamento do franqueado com as diárias (receita) dos imóveis. É o faturamento total dos imóveis multiplicado pela premissa de comissão do franqueado.

     Fatd=Fatt ∗ ComfFat_d = Fat_t \\space \* \\space Com_fFatd​=Fatt​ ∗ Comf​
     * Faturamento dos franqueados com limpezas
       * Faturamento do franqueado com as limpezas nos imóveis residenciais. É o número de reservas total multiplicado pela premissa de valor médio de limpeza.

       Fatl=Resn ∗ LimpmFat_l = Res_n \\space \* \\space Limp_mFatl​=Resn​ ∗ Limpm​
     * Faturamento total dos franqueados
       * Soma do faturamento das diárias e limpezas dos franqueados.
     * Faturamento com a implantação de novos imóveis
       * É o número de novos imóveis no mês multiplicado pela premissa de taxa de implantação média de imóveis residenciais.

         Fatimp=Imoveisnovos ∗ Implm2Fat_{imp} = Imoveis_{novos} \\space \* \\space Impl_{m2}Fatimp​=Imoveisnovos​ ∗ Implm2​
       * No BP foi considerado que parte dos imóveis efetuaria o pagamento da taxa de implantação em 6 parcelas.
     * Faturamento com a venda de franquias
       * É o número de novos franqueados multiplicado pela premissa de taxa de franquia média.

       Fatfranq=Franqnovos∗TaxaFranqmFat_{franq} = Franq_{novos} \* TaxaFranq_mFatfranq​=Franqnovos​∗TaxaFranqm​
       * No BP foi considerado que parte dos franqueados efetuaria o pagamento da taxa de franquia em 10 parcelas.
     * Comissão com a venda de reservas diretas (website)
       * Faturamento das reservas vindas do website (Khanto).

       Comota=Fatd+Fatl1−OTAszn∗Taxaloc∗OTAsznCom_{ota} ={{{Fat_d + Fat_l} \\over 1 - OTA_{szn}}\*Taxa_{loc}\*OTA_{szn}}Comota​=1−OTAszn​Fatd​+Fatl​​∗Taxaloc​∗OTAszn​
     * Royalty de franquias
       * Faturamento da Seazone com as diárias (receita) dos imóveis. É o faturamento total dos imóveis multiplicado pela premissa de comissão do imóvel menos a premissa de comissão do franqueado.

       Royaltyf=Fatd ∗ (Comi−Comf)Royalty_f = Fat_d \\space \* \\space (Com_i - Com_f)Royaltyf​=Fatd​ ∗ (Comi​−Comf​)
     * Faturamento total da SZN
       * É a soma do faturamento com a implantação dos imóveis, a venda de franquias, a comissão das reservas do website e do royalty das franquias.

     Fatszn=Fatimp+Fatfranq+FatOTA+RoyaltyfFat_{szn} = Fat_{imp} + Fat_{franq} + Fat_{OTA} + Royalty_fFatszn​=Fatimp​+Fatfranq​+FatOTA​+Royaltyf​
3. Projeção de Receitas Resorts
   * Para a projeção das receitas de imóveis do tipo resort/hotel é necessário rodar a função "mainProjecaoFase1" através de uma macro. Essa pode ser encontrada no menu de Macros Planejamento → Projeção de Receitas → Resorts.

     ![](/api/attachments.redirect?id=160551fc-72f8-44f8-a615-7fc06a006dc8)

     Assim como para a projeção residencial, essa função vai chamar 2 outras funções, uma que estrutura o template da aba definindo suas linhas, colunas e o período da projeção (de acordo com as premissas de data inicial e final) e a função "projecaoFase2" que realiza os cálculos da projeção.\n\nPega todas as regiões com imóveis especificados como sendo resorts na aba de premissas (Coluna B = 1). Faz inicialmente o calculo da projeção para cada uma das regiões de acordo com o mês da projeção (Linha 17 em diante da aba de projeção). Em seguida, com os a projeção da região feita, são calculados os dados dos imóveis (Linhas 3 a 9) e os dados de comissões e faturamento.\n
     * Para o primeiro mês da projeção:
       * Número de reservas: premissa de quantidade de reservas no mês \* premissa de número de apartamentos iniciais;
       * Número de novos imóveis: são considerados somente os imóveis iniciais e portanto o número de novos imóveis é 0;
       * Número de imóveis: premissa de número de imóveis iniciais;
     * Para os meses seguintes
       * Número de reservas: premissa de quantidade de reservas no mês \* número de imóveis no mês de projeção.
       * Número de novos imóveis:
         * Se o número total de imóveis é menor que a premissa de saturação da região, o número de novos imóveis é a premissa de taxa comercial da região (Coluna G).
         * Se o número total de imóveis é maior ou igual a premissa de saturação, o número de novos imóveis é 0.
       * Número de imóveis: número de imóveis do mês anterior somado ao número de novos imóveis.

     Com a projeção concluída, são compilados os dados dos imóveis em todas as regiões de atuação por mês:
     * Total de imóveis
     * Total de reservas
     * Total de novos imóveis
     * Total de regiões
     * Total de novas regiões
     * Total de churns
     * Faturamento total dos imóveis

     Com os dados compilados, são calculadas as comissões e faturamentos totais:
     * Comissão do parceiro
       * Comissão paga aos parceiros que indicaram imóveis para a SZN. É o faturamento total multiplicado pela premissa de comissão por indicação de imóveis multiplicado pela premissa de imóveis via parceiro.

     Comp=Fatt ∗ Comind ∗ IndImoveispCom_p = Fat_t \\space \* \\space Com_{ind}\\space \* \\space IndImoveis_{p}Comp​=Fatt​ ∗ Comind​ ∗ IndImoveisp​
     * Comissão com a venda de reservas diretas (website)
       * Faturamento das reservas vindas do website (Khanto).

       Fatota=Fatt1−OTAszn∗Taxaloc∗OTAsznFat_{ota} ={{{Fat_t} \\over 1 - OTA_{szn}}\*Taxa_{loc}\*OTA_{szn}}Fatota​=1−OTAszn​Fatt​​∗Taxaloc​∗OTAszn​
     * Faturamento com a implantação de novos imóveis
       * É o número de novos imóveis no mês multiplicado pela premissa de taxa de implantação média de imóveis em resorts.

         Fatimp=Imoveisnovos ∗ Implm1Fat_{imp} = Imoveis_{novos} \\space \* \\space Impl_{m1}Fatimp​=Imoveisnovos​ ∗ Implm1​
       * No BP foi considerado que parte dos imóveis efetuaria o pagamento da taxa de implantação em 6 parcelas.
     * Faturamento com a gestão das diárias
       * É o faturamento total dos imóveis multiplicado pela premissa de comissão do imóvel.

       Comszn=Fatt ∗ ComiCom_{szn} = Fat_t \\space \* \\space Com_iComszn​=Fatt​ ∗ Comi​
     * Faturamento total da SZN
       * É a soma do faturamento com a implantação dos imóveis, a comissão das reservas do website e da gestão das diárias.

       Fatszn=Fatimp+Fatota+ComsznFat_{szn} = Fat_{imp} + Fat_{ota} + Com_{szn}Fatszn​=Fatimp​+Fatota​+Comszn​

## Projeção de Receita SZNI


1. Premissas
   * Premissas que podem ser editadas
     * % comissão dos parceiros
     * % permutas
     * % comissão de vendas pelo Marketplace
     * % de repasse de cotas mensal
     * % de vendas via repasse do Marketplace
     * Ticket médio Marketplace
   * Premissas iniciais fixas

     Essas premissas precisam ter seus valores iniciais levantados e inseridos na planilha antes da projeção. A previsão é de um empreendimento estruturado por mês. Para os empreendimentos já estruturados, os dados podem ser obtidos através dos relatórios financeiros do setor de compliance.
     * Região
     * Data de início da estruturação
     * Data de início das vendas
     * Data de fechamento de grupo
     * Data do recebimento do reembolso
     * Data do recebimento das comissões
     * Valor do reembolso
     * Valor da estruturação
     * Valor da prospecção (comissão): Valor total da comissão por prospecção de venda de todas as unidades do
     * Comissão Seazone
     * Número de unidades
     * Unidades vendidas por mês
     * Data de início das obras
     * Data do fim das obras
     * Data para mobília
     * Data para início da operação
     * Modelo light do BP
     * Modelo full do BP

     \
2. Projeção de Receita

* Para a projeção das receitas de imóveis do tipo resort/hotel é necessário rodar a função "mainProjecaoFase1" através de uma macro. Essa pode ser encontrada no menu de Macros Planejamento → Projeção de Receitas → Seazone Investimentos.

  ![](/api/attachments.redirect?id=e700276a-015e-4eb2-aff8-4a3bbef4c13c)

  Essa função vai chamar 2 outras funções, uma que estrutura o template da aba definindo suas linhas, colunas e o período da projeção (de acordo com as premissas de data inicial e final) e a função "projecaoSZNI" que realiza os cálculos da projeção.
  * Dados dos Spots

| **Dado** | Cálculo BP | Fórmula |
|:---|:---|:---|
| Terrenos fechados | Empreendimentos com data de início de estruturação **≤** a data da projeção. | =CONT.NÚM(filter('Premissas Projecao de Receita - SI'!$B:$B;'Premissas Projecao de Receita - SI'!$B:$B <= B$1)) |
| Empreendimentos ativos | Empreendimentos entre fechamento de grupo e a finalização das obras. | =CONT.NÚM(filter('Premissas Projecao de Receita - SI'!$B:$B;B$1 >= 'Premissas Projecao de Receita - SI'!$D:$D; B$1 <= 'Premissas Projecao de Receita - SI'!$N:$N)) |
| Empreendimentos lançados | Empreendimentos com data de início das vendas ≤ a data da projeção. | =CONT.NÚM(filter('Premissas Projecao de Receita - SI'!$C:$C;((MÊS('Premissas Projecao de Receita - SI'!$C:$C)<=MÊS(B$1))\*(ANO('Premissas Projecao de Receita - SI'!$C:$C)=ANO(B$1)))+(ANO('Premissas Projecao de Receita - SI'!$C:$C)<ANO(B$1)))) |
| Novos lançamentos | Empreendimentos com data de início das vendas = a data da projeção. | =CONT.NÚM(FILTER('Premissas Projecao de Receita - SI'!$C:$C;(MÊS('Premissas Projecao de Receita - SI'!$C:$C)=MÊS(B$1))\*(ANO('Premissas Projecao de Receita - SI'!$C:$C)=ANO(B$1)))) |
| Spots entre início de estruturação e início de vendas |    | =CONT.VALORES(filter('Premissas Projecao de Receita - SI'!$A$3:$A;(B$1+1 >= 'Premissas Projecao de Receita - SI'!$B$3:$B) \* (B$1 + 1 < 'Premissas Projecao de Receita - SI'!$C$3:$C))) |
| Grupos abertos | Empreendimentos entre o início da estruturação e o fechamento de grupo. | =CONT.VALORES(filter('Premissas Projecao de Receita - SI'!$A$3:$A;(B$1+1 >= 'Premissas Projecao de Receita - SI'!$B$3:$B)\*(B$1 + 1 < 'Premissas Projecao de Receita - SI'!$D$3:$D))) |
| Total de unidades estruturadas | Unidades dos empreendimentos com data de início de estruturação ≤ ao mês da projeção. | =SOMA(filter('Premissas Projecao de Receita - SI'!$K:$K;'Premissas Projecao de Receita - SI'!$B:$B <= B$1)) |
| Unidades entre início de venda e fim de obra | Unidades dos empreendimentos em que o mês de projeção é > que a data de início das vendas e ≤ a data de fim da obra. | =SOMA(filter('Premissas Projecao de Receita - SI'!$K:$K;B$1 > 'Premissas Projecao de Receita - SI'!$C:$C; B$1 <= 'Premissas Projecao de Receita - SI'!$N:$N)) |
| Unidades estruturadas entre fechamento de grupo e finalização de obra | Unidades dos empreendimentos em que o mês de projeção é > que a data de fechamento do grupo e ≤ a data de fim da obra. | =SOMA(filter('Premissas Projecao de Receita - SI'!$K:$K;B$1 > 'Premissas Projecao de Receita - SI'!$D:$D; B$1 <= 'Premissas Projecao de Receita - SI'!$N:$N)) |
| Unidades vendidas |    | =SOMA(filter('Premissas Projecao de Receita - SI'!$L:$L;('Premissas Projecao de Receita - SI'!$C:$C <= B$1 + 1)\*('Premissas Projecao de Receita - SI'!$D:$D > B$1 + 1))) |
| Unidades a serem mobiliadas |    | =ifna(SOMA(filter('Premissas Projecao de Receita - SI'!$K:$K;'Premissas Projecao de Receita - SI'!$O:$O = B$1));0) |
| Unidades em operação |    | =ifna(SOMA(filter('Premissas Projecao de Receita - SI'!$K:$K;'Premissas Projecao de Receita - SI'!$P:$P < B$1));0) |
  * Faturamento Spots
    * Estruturação: é a soma do valor da estruturação (Coluna H) de todos os empreendimentos em que a data de fechamento do grupo (Coluna D) está prevista para o mês da projeção. O cálculo pode ser feito da seguinte forma:
      * ifna(SOMA(filter('Premissas Projecao de Receita - SI'!$H:$H;(MÊS('Premissas Projecao de Receita - SI'!$D:$D)=MÊS(B$1))\*(ANO('Premissas Projecao de Receita - SI'!$D:$D)=ANO(B$1)));0))
    * Comissão dos parceiros: é a soma do valor da prospecção (Coluna I) de todos os empreendimento em que a data de fechamento do grupo (Coluna D) está prevista para o mês da projeção \* a premissa de % da comissão dos parceiros \* o funil de % de vendas pelos parceiros da SZNI. O cálculo pode ser feito da seguinte forma:
      * ifna(((SOMA(filter('Premissas Projecao de Receita - SI'!$I:$I;(MÊS('Premissas Projecao de Receita - SI'!$D:$D)=MÊS(B$1))*(ANO('Premissas Projecao de Receita - SI'!$D:$D)=ANO(B$1))))*('Premissas Projecao de Receita - SI'!$B$1)\*Funil!B$45));0)
    * Comissão de vendas do Marketplace: é a soma do valor da comissão SZN (Coluna J) de todos os empreendimentos em que a data de fechamento do grupo (Coluna D) está prevista para o mês da projeção multiplicado pelo funil de % de vendas pelo Marketplace. O cálculo pode ser feito da seguinte forma:
      * ifna(((SOMA(FILTER('Premissas Projecao de Receita - SI'!$J:$J;(MÊS('Premissas Projecao de Receita - SI'!$D:$D)=MÊS(B$1))\*(ANO('Premissas Projecao de Receita - SI'!$D:$D)=ANO(B$1))))\*Funil!B$46));0)

## Receitas Realizadas

* Informações são retiradas da aba planilha de Orçado x Realizado x Projeção.
  * **Seazone Serviços**

| **Tipo da Receita** | **Descrição** | **Dono da informação** | Fonte da informação |
|:---|:---|:---|:---|
| Taxa de implantação | Negociada pelo comercial, é a taxa cobrada em contrato e cobre os serviços e produtos para a padronização do imóvel. | Setor Financeiro → Analista Financeiro (Gabriel) | Relação de NF's emitidas no mês pelo setor financeiro ou através da planilha de **[Controle CRC](https://docs.google.com/spreadsheets/d/1Q1dV4hkJqfKABiPMsYXY5sLYVVq8l1NyBBediuWqApE/edit#gid=822640047)** na aba "REC_IMPLANTAÇÃO". |
| Venda de franquia | Negociada pelo comercial de franquias, é a taxa cobrada para criação de novas franquias nas regiões de atuação. | Setor Comercial → Coordenador de Vendas Franquias | Relação de NF's emitidas no mês pelo setor financeiro ou através da planilha de **[Controle CRC](https://docs.google.com/spreadsheets/d/1Q1dV4hkJqfKABiPMsYXY5sLYVVq8l1NyBBediuWqApE/edit#gid=1628900131)** na aba "REC_FRANQUIA". |
| Comissão de venda de reservas diretas | Comissão cobrada sobre o valor da reserva feita no website da SZN. | Setor Financeiro → Analista Financeiro (Gabriel) | NF emitida pela Khanto no mês pelo setor financeiro ou através da planilha de **[Controle CRC](https://docs.google.com/spreadsheets/d/1Q1dV4hkJqfKABiPMsYXY5sLYVVq8l1NyBBediuWqApE/edit#gid=569290165)** na aba "REC_OTA". |
| Gestão de contas | Mensalidade cobrada pelo serviço de gestão de contas (IPTU, condomínio, energia, internet, água, etc.) de um imóvel. | Setor Financeiro → Analista Financeiro (Gabriel) | Relação de NF's emitidas no mês pelo setor financeiro ou através da planilha de **[Controle CRC](https://docs.google.com/spreadsheets/d/1Q1dV4hkJqfKABiPMsYXY5sLYVVq8l1NyBBediuWqApE/edit#gid=505531135)** na aba "REC_GESTAO_CONTAS". |
| Taxa de cancelamento de reservas | Valor referente as reservas canceladas que ficam com a SZN. | Setor Fechamento → Analista de Fechamento (Débora) | Através da planilha de **[No-shows e Cancelamentos](https://docs.google.com/spreadsheets/d/1mcXhCIeYReeYTVStWKxTUQE6gqG9WTjYvhy3Td6Y688/edit#gid=1541319368)** aba "DASH" |
| Comissão de vendas do MKTP | Comissão pela venda de imóveis de terceiros ou de SPOTs através do Martketplace da SZN. | Setor Financeiro → Analista Financeiro (Gabriel) | Relação de NF's emitidas no mês pelo setor financeiro ou através da planilha de **[Controle CRC](https://docs.google.com/spreadsheets/d/1Q1dV4hkJqfKABiPMsYXY5sLYVVq8l1NyBBediuWqApE/edit#gid=1074849367)** na aba "REC_MKT". |
| Royalty de Franquias | Comissão pelo serviço de gestão digital prestado pela SZN para os imóveis do tipo residencial (operados por franqueados). | Setor Financeiro → Analista Financeiro (Gabriel) | Relação de NF's emitidas no mês pelo setor financeiro ou através da planilha de **[Controle CRC](https://docs.google.com/spreadsheets/d/1Q1dV4hkJqfKABiPMsYXY5sLYVVq8l1NyBBediuWqApE/edit#gid=1746361261)** na aba "REC_ROYALTY_FRANQ.". |
| Comissão de Imóveis em Resorts | Comissão pelo serviço de gestão digital prestado pela SZN para os imóveis do tipo residencial (sem operação de franqueados). | Setor Financeiro → Analista Financeiro (Gabriel) | Relação de NF's emitidas no mês pelo setor financeiro ou através da planilha de **[Controle CRC](https://docs.google.com/spreadsheets/d/1Q1dV4hkJqfKABiPMsYXY5sLYVVq8l1NyBBediuWqApE/edit#gid=1074849367)** na aba "REC_MKT". |
  * **Seazone Investimentos**

| **Tipo da Receita** | **Descrição** | **Dono da informação** | Fonte da informação |
|:---|:---|:---|:---|
| Taxa de estruturação | Taxa referente à prestação de serviços por parte da SZN a SPE de um empreendimento pela concepção, viabilização, acompanhamento e fiscalização do que foi estruturado e será implantado. | Setor Compliance → Coordenador de Compliance (Guilherme) | Relação de NF's emitidas no mês pelo setor financeiro ou através da planilha de **[Controle CRC](https://docs.google.com/spreadsheets/d/1Q1dV4hkJqfKABiPMsYXY5sLYVVq8l1NyBBediuWqApE/edit#gid=1323858629)** na aba "REC_ESTRUTURAÇÃO". |
| Comissão de venda Spots | Comissão pela venda de unidades Spots pela SZN. | Setor Comercial → Coordenador de Vendas SZI (Cínthia) | Relação de NF's emitidas no mês pelo setor financeiro ou através da planilha de **[Controle CRC](https://docs.google.com/spreadsheets/d/1Q1dV4hkJqfKABiPMsYXY5sLYVVq8l1NyBBediuWqApE/edit#gid=1302153909)** na aba "REC_COMISSAO_SZI". |
| Taxa de consultoria Decor | Receita **DESCONTINUADA.** Valores de histórico ainda podem ser consultados. | Setor Financeiro → Analista Financeiro (Gabriel) | Relação de NF's emitidas no mês pelo setor financeiro ou através da planilha de **[Controle CRC](https://docs.google.com/spreadsheets/d/1Q1dV4hkJqfKABiPMsYXY5sLYVVq8l1NyBBediuWqApE/edit#gid=1608397687)** na aba "REC_DECOR. |
| Reembolsos | Valor referente aos custos arcados pela SZN inicialmente (arras de terreno, viabilidades) | Setor Compliance → Coordenador de Compliance (Guilherme) | Através da planilha de **[Controle CRC](https://docs.google.com/spreadsheets/d/1Q1dV4hkJqfKABiPMsYXY5sLYVVq8l1NyBBediuWqApE/edit#gid=1909934104)** na aba "REEMBOLSO_SPE". |

## Despesas Mensais

* Despesas
  * 1) Criar aba "Cálculo Despesas" com a lista das despesas de todos os setores através das bases de contas a pagar e do admsys. Incluir as informações de:
    * Nas colunas A:D, criar as colunas **Empresa, Setor, Centro de Custo e Categoria** em que se encaixa a despesa.
    * Na coluna E, adicionar a **escalabilidade** da despesa. Despesas que dependem do número de colaboradores, imóveis e empreendimentos são escaláveis.
    * Na coluna F, adicionar o tipo da linha de despesa. Utilizado para diferenciar as linhas de premissas da linha de cálculo de custo final de cada uma das despesas.
    * Na coluna G, adicionar o nome do **responsável** (diretor/gestor) da despesa.
    * Na coluna H, adicionar a coluna **descrição** para cada linha de premissas.
    * Na coluna I, adicionar a coluna de **constante**, que é utilizada para o cálculo de cada premissa.
    * Na coluna J, adicionar a coluna de **total.**
    * Nas colunas K em diante, adicionar **uma coluna para cada mês** do BP.
    * Na coluna **Total**, colocar a soma do custo da despesa de todos os meses à direita.
    * A fórmula para o cálculo do custo, vai depender das premissas associadas a cada uma das despesas.
    * Durante a revisão, indicar nas linhas de Custo as seguintes informações:
      * Coluna H: Se a despesa é Administrativa, Comercial, Financeira, Imposto, Investimento, Marketing, Operacional ou Reembolsável.
      * Coluna I: Se a despesa é Fixa ou Variável
  * 2) Criar aba de "Despesas Mensais"
    * A aba "Despesas Mensais" funciona como um resumo dos cálculos, mostrando apenas os custos.
      * A aba pode ser calculada usando a função QUERY, selecionando apenas as linhas em que a Col6 (F) é 'Custo'.
      * Para classificar os dados, basta abraçar a função QUERY por uma função SORT.
* People
  * 1) Criar aba "Colaboradores atuais" com a lista atualizada de colaboradores, incluindo as informações:
    * **Dono da informação:** Diretor de People ou Coordenador de Departamento pessoal
    * **Empresa, Setor, Área, Subárea, Sub-subárea, cargo e nível** em que o colaborador está atualmente, bem como as **promoções/desligamentos e mudanças de área já definidas** para os próximos meses.
    * Adicionar também as colunas de **valor do step salarial** para os aumentos semestrais\*\*, piso salarial e teto salarial\*\* para cada entrada.
    * Adicionar a coluna de base cálculo para a bonificação trimestral para preenchimento pelos donos da informação (Diretoria, Departamento pessoal)
    * Adicionar uma coluna indicando se o colaborador recebe VR.
    * Adicionar uma coluna de "Fator CLT", com a informação da data em que o colaborador/posição passará a ser CLT (se já é, colocar a data inicial do BP), se a posição for CLT, adotamos o cálculo simplificado de que o custo daquela posição para a empresa será o dobro quando comparado à modalidade PJ.
    * Adicionar o nome dos colaboradores e a remuneração atual/futura remuneração em caso de uma promoção já definida.
    * Adicionar uma coluna de Total e uma coluna para cada mês do BP.
    * Na coluna Total, colocar a soma da remuneração de todos os meses à direita.
    * A fórmula para o cálculo do custo do colaborador em cada mês deve realizar os seguintes checks para definir o valor:
      * Meses em que os aumentos semestrais acontecem;
      * Meses em que ocorre pagamento de bônus;
      * Mês em que a posição passará a ser CLT;
      * Se a pessoa recebe ou não VR;
      * Se a remuneração da pessoa com os aumentos não excede o teto para aquela posição - o "Teto Salarial" para cada posição é inserido na aba "Premissas Despesas RH".
      * Assim, a fórmula levará as seguintes informações:
        * SE((Remuneração atual + nº de steps de aumento recebidos até o mês\*valor do step)≥"Teto Salarial";"Teto Salarial";(Remuneração atual + nº de steps de aumento recebidos até o mês\*valor do step))\*(fator CLT)
        * Ex: Estamos em jan. 2024 e Murilo recebe R$3.000,00 atualmente de remuneração base e VR no valor de R$500,00. Nos meses de janeiro e julho ele recebe um aumento de R$500,00 e nos meses de janeiro, abril, julho e outubro, um bônus de 30% da remuneração atual. O modelo de contratação é PJ. A remuneração dele em fevereiro/2024 será 3000\*1 + 500 = 3.500, porém em outubro de 2025, já passou por 3 aumentos (jul. 24, jan.25 e jul. 25), assim sua remuneração será (3000 + 3\*500)\*(1) = 4.500. Por fim, supondo que a posição tenha sido convertida em CLT em out. 25, o cálculo se torna: (3000 + 3\*500)\*(2) = 9.000
        * **OBS:** Despesas adicionais como o VR e o bônus são calculadas diretamente na aba "Cálculo Despesas RH"
        * **OBS:** Nos desligamentos programados, duplicar o valor da remuneração base no último mês da pessoa e APAGAR as células seguintes, deixar 0 irá interferir nas fórmulas de filtro usadas na aba "Cálculo Despesas RH".
  * 2) Criar aba com as vagas abertas, incluindo \*\*Empresa, Setor, Área, Subárea, Sub-subárea, cargo, a remuneração e o mês em que a posição irá iniciar (\*\*lembrando que, se a pessoa entra em agosto, seu custo deve ser considerado à partir de setembro). Podem ser adicionadas informações como a modalidade de contratação (CLT ou PJ) e se o cargo terá VR.
    * Dono da informação: Diretor de People ou Coordenador de Recrutamento e Seleção.
  * 3) Adicionar na aba de "Premissas Despesas" - algumas premissas para simplificar a aba de Cálculo
    * Teto salarial para cada cargo (Plano de cargos e salários)
    * Constantes para cálculo das comissões
    * Constante para cargos escaláveis
    * Multiplicador bônus (# de 0 a 1)
    * Data de conversão para CLT
    * Valor do VR
    * Data de implementação do VR para todos
    * Meses de bônus - (1,4,7,10)
    * Meses de aumento salarial (1,7)
    * Trigger para coordenador
    * Trigger para gerente
  * 4) Criar aba de "Cálculo Despesas RH"
    * Essa aba deve conter as colunas de **Empresa, Setor, Área, Subárea, Sub-subárea, cargo** para todas as posições da empresa, independentemente de alguém ocupar a função hoje ou não.
    * Na coluna G, indicar se o cargo é escalável ou não.
    * Na coluna H:J, criar as coluna "Tipo" (Custo, Premissa 1, Premissa 2…), "Descrição" (abaixo) e "Constante" (abaixo)
    * Na coluna K, criar a coluna "Total"
    * Nas colunas L em diante, uma coluna para cada mês do BP.
    * São criadas 9 linhas para cada cargo (1 Custo + 9 premissas):
      * Custo - onde será calculado o custo total da posição
      * Salário Base para novas contratações - a constante será o valor base inicial
      * Step de aumento salarial
      * Bônus trimestral por metas/comissão - aqui será indicado qual o % de bônus que aquela posição recebe ou, caso seja um valor fixo/comissão com base nas vendas, indicado o valor/método de cálculo. Caso não seja um cargo comissionado, esse campo será uma fórmula, pois o valor cheio será multiplicado por um valor entre 0 e 1, definido na aba de Premissas, que é a estimativa de qual % das metas será atingido para pagamento dos bônus.
      * Fator CLT - data em que a posição será convertida para CLT
        * No BP 30 meses de julho-2023, a data era definida separadamente para cada posição, mas uma sugestão para os próximos é colocar a data na aba de Premissas ou, pode ser pensada em uma transição gradual em fases, em que na aba de Cálculo cada posição teria indicado a fase da transição a qual ela pertence, e na aba de Premissas, estaria indicada a data estimada para a transição de cada fase.
      * Colaboradores na função - Linha em que será calculado o # de pessoas em cada posição, somando os colaboradores atuais com os colaboradores futuros que serão necessários devido ao escalonamento das áreas.
      * VR - A constante fica em branco, pois já está na aba "Premissas Despesas RH".
      * Colaboradores atuais - A coluna "Constante" fica em branco. Fórmula que irá contabilizar, via "Colaboradores atuais", a quantidade de colaboradores atuais naquele mês, levando em consideração promoções/demissões já programadas.
      * Despesa colaboradores atuais - A coluna "Constante" fica em branco. Fórmula que irá somar o custo total dos colaboradores atuais naquela posição, mês a mês, via "Colaboradores Atuais".
      * On/Off - Linha de suporte para revisão/análise, na coluna "Constante" fica o espaço para o input (1 ou 0)

    ![](/api/attachments.redirect?id=88f8b49b-89d2-4e64-ab0f-f107e3b25ad8)
    * Após montar todas as linhas com todas as posições, é recomendado criar algumas visualizações de filtro:
      * Cargos que recebem comissão/bônus fixo
      * Cargos escaláveis
      * Coordenadores/Gerentes/Diretores
      * C-level
    * Para as colunas dos meses, as fórmulas são como segue:
      * Custo:
        * O cálculo do custo integra as linhas calculadas abaixo, da seguinte forma:
          * ((("# Colaboradores na função"-"Colaboradores ativos")\*"Salário base"+"Despesa colaboradores atuais")\*Fator CLT+Bônus+VR)\*"On/Off"
      * Salário base:
        * O "Teto Salarial" para cada posição é inserido na aba "Premissas Despesas RH".
        * SE("Constante Salário Base" + "nº de steps"\*"Step de aumento salarial">"Teto Salarial";"Teto Salarial";Constante Salário Base" + "nº de steps"\*"Step de aumento salarial")
      * Step: A linha do step é utilizada para calcular o "nº de steps" no cálculo do salário base acima e a fórmula é:
        * SE("Mês atual"="Mês de aumento";Valor anterior + 1;Valor anterior)
      * Bônus: Aqui é calculado o valor do bônus em cada caso:
        * Caso 1: Bônus proporcional ao salário base:
          * SE("Mês atual"="Mês de pagamento de bônus";"Constante % de bônus"\*"Salário base";0)\*"# Colaboradores na função"
        * Caso 2: Bônus fixo:
          * SE("Mês atual"="Mês de pagamento de bônus";"Valor do Bônus";0)\*"# Colaboradores na função"
        * Caso 3: Comissão:
          * Os valores e a forma de cálculo das comissões devem ser obtidos com as lideranças dos times que possuem comissão: Marketplace - Vendas e Pré-Vendas, Comercial - Vendas e Pré-Vendas (SZS, SZI, Franquias), Parceiros.
          * Os valores e as formas de cálculo das comissões serão configurados na aba "Premissas Despesas RH" e o valor na célula será apenas o valor total, sem multiplicar pelo # de colaboradores na função.
      * Fator CLT: Check verificando se a data é igual ou superior à data estipulada para a transição para regime CLT, se a data tiver chegado, o salário base é multiplicado por 2, assim:
        * SE("Mês atual"≥"Mês de transição";2;1)
      * Colaboradores na função:
        * Caso 1 (Cargos não escaláveis): esse valor será igual ao nº de colaboradores atuais + as vagas novas abertas (incluídas manualmente a partir do mês de entrada delas) + possíveis vagas planejadas e validadas pela Diretoria.
        * Caso 2 (Cargos escaláveis): Cargos escaláveis tem o número de colaboradores definidos através da razão entre a Demanda e a Capacidade por colaborador, por exemplo:
          * São necessários mais analistas de auditoria na Área de Compliance conforme o # de Empreendimentos com status entre Grupo Fechado e Entrega aumenta e cada colaborador consegue atender 7 empreendimentos, assim o # de colaboradores é igual ao (# de empreendimentos com status entre Grupo Fechado e Entrega)/7
          * **OBS:** O # de colaboradores na função não pode diminuir e também não pode ser maior do que o # de colaboradores atuais.
        * Caso 3 (Coordenadores/Gerentes): Os cargos de liderança em que não há nenhum colaborador atualmente, especialmente em áreas escaláveis da empresa, devem conter um trigger para quando essa posição será necessária:
          * Coordenadores: Quando houverem 5 analistas na subsubárea/subárea, deve passar a ter um coordenador.
          * Gerente: Quando alguma sub-área abaixo da área em que a liderança hoje é feita por um coordenador passar a ter um coordenador, o coordenador da área é promovido à gerente da área (assim o # de colaboradores na função "Colaborador da área" passa a ser 0)
      * VR: nessa linha será calculado o gasto com VR para aquela posição, para isso é necessário obter o # de colaboradores da área que recebem VR:
        * Passo 1: Check o VR já foi estendido para toda empresa:
          * SE("Mês atual"≥"Data de Implementação do VR para todos";…)
        * Passo 2: Caso tenha sido, o valor será "Colaboradores na função"\*"Valor VR"
        * Passo 3: Caso não tenha, será necessária:
          * 1) A quantidade de colaboradores atuais que recebem VR naquela posição:
            * CONT.VALORES(IFNA(FILTER('Colaboradores ativos'!"Coluna do mês";'Colaboradores ativos'!"VR"="Sim";(…));0)
            * (…) → as condições do filtro são o match de **Empresa, Setor, Área, Subárea, Sub-subárea, cargo** da aba "Colaboradores Ativos" com as colunas A:F da linha em que a fórmula está sendo inserida.
          * 2) Definir se as novas contratações terão VR (Dono da informação: Diretoria, Diretor de People)
            * Se sim, definir o # de colaboradores novos → # colaboradores novos → "Colaboradores na função" - "Colaboradores atuais"
            * Se não, manter apenas os atuais.
        * Para os colaboradores novos:
          * Passo 1: # colaboradores novos → "Colaboradores na função" - "Colaboradores atuais"
          * Passo 2: check se o VR já foi estendido a toda a empresa (data na aba "Premissas Despesas RH" → SE("Mês atual"≥"Mês VR";1;0)
        * Então, a fórmula total da célula é:
          * (CONT.VALORES(IFNA(FILTER('Colaboradores ativos'!"Coluna do mês";'Colaboradores ativos'!"VR"="Sim");0) + ("Colaboradores na função" - "Colaboradores atuais")\*SE("Mês atual"≥"Mês VR";1;0))\*"Valor do VR"
      * Colaboradores atuais:
        * Aqui é feita uma busca na aba "Colaboradores Ativos" para contar quantos colaboradores estão em cada posição:
          * CONT.VALORES(IFNA(FILTER('Colaboradores ativos'!"Coluna do mês";(…));0))
          * (…) → as condições do filtro são o match de **Empresa, Setor, Área, Subárea, Sub-subárea, cargo** da aba "Colaboradores Ativos" com as colunas A:F da linha em que a fórmula está sendo inserida.
      * Despesa Colaboradores atuais:
        * Fórmula muito similar à fórmula do # colaboradores atuais, porém usando SOMA ao invés de CONT.VALORES.
      * On/Off - O valor da célula no mês é sempre o valor da constante, mas é necessário caso seja desejado desligar uma função só por um período.
    * **Exceção: C-level**
      * Os cargos C-level (CEO Holding, CEO Investimentos, CEO Serviços, CTO e CFO) não precisam de todas as premissas mencionadas, basta apenas:
        * Custo
        * Despesa colaboradores atuais
        * Bônus
        * VR
        * Colaboradores na função
  * 5) Criar a aba "Despesas RH"
    * A aba "Despesas RH" funciona como um resumo dos cálculos, mostrando apenas os custos
      * A aba pode ser calculada usando a função QUERY, selecionando apenas as linhas em que a Col8 (H) é 'Custo'.
      * Para classificar os dados, basta abraçar a função QUERY por uma função SORT.
      * Pode ser usada a formatação condicional para destacar valores acima da média, para facilitar a análise dos dados.

  Durante a revisão, indicar nas linhas de Custo as seguintes informações:
  * Coluna I: Se a despesa é Operacional, Administrativa, Tecnologia, Comercial ou Marketing
  * Coluna J: Se a despesa é Fixa ou Variável

  \

## Log de Alterações


## Funis

* A aba "Funil" é utilizada para calcular as entradas de leads em cada canal de venda necessário para atingir as metas estipuladas pela projeção de receitas.
* Para construir a projeção do funil, deve-se calcular os % de conversão mais recentes utilizando os dados dos times Comercial, Marketplace, Parceiros e Terrenos. Os dados são calculados na aba "Cálculo Conversões Funil":
* Cálculo Conversões Funil

  Aqui na aba são calculadas as conversões com base no histórico recente dos times.
  * Novos imóveis (Seazone Serviços)

|    |    |    |    |
|:---|:---|:---|:---|
| **Informação** | **Fonte** | **Modo de cálculo** | **Dono** |
| # Total de Contratos Assinados | [BI Comercial - Aba Canais](https://app.powerbi.com/reportEmbed?reportId=36b440ba-0af0-406a-a2ec-3a9e441dfd0c&autoAuth=true&ctid=1bc6b8f1-1aa6-4836-90ac-40f3fc44fd46) - Selecionar os últimos 6-12 meses - Tabela Consolidada | - Selecionar os últimos 6-12 meses.<br>- No filtro de canal, selecionar tudo.<br>- Na tabela consolidada, copiar o # de assinados total.<br> | Vendas SZS |
| # Total Oportunidades | [BI Comercial - Aba Canais](https://app.powerbi.com/reportEmbed?reportId=36b440ba-0af0-406a-a2ec-3a9e441dfd0c&autoAuth=true&ctid=1bc6b8f1-1aa6-4836-90ac-40f3fc44fd46) - Selecionar os últimos 6-12 meses - Tabela Consolidada | - Selecionar os últimos 6-12 meses.<br>- No filtro de canal, selecionar tudo.<br>- Na tabela consolidada, copiar o # Ops total<br> | Vendas SZS |
| # Total SQL | [BI Comercial - Aba Canais](https://app.powerbi.com/reportEmbed?reportId=36b440ba-0af0-406a-a2ec-3a9e441dfd0c&autoAuth=true&ctid=1bc6b8f1-1aa6-4836-90ac-40f3fc44fd46) - Selecionar os últimos 6-12 meses - Tabela Consolidada | - Selecionar os últimos 6-12 meses.<br>- No filtro de canal, selecionar tudo.<br>- Na tabela consolidada, copiar o # SQL Total<br> | Pré-Vendas SZS |
| # Total Deals | [BI Comercial - Aba Canais](https://app.powerbi.com/reportEmbed?reportId=36b440ba-0af0-406a-a2ec-3a9e441dfd0c&autoAuth=true&ctid=1bc6b8f1-1aa6-4836-90ac-40f3fc44fd46) - Selecionar os últimos 6-12 meses - Tabela Consolidada | - Selecionar os últimos 6-12 meses.<br>- No filtro de canal, selecionar tudo.<br>- Na tabela consolidada, copiar o # Deals Total<br> | Pré-Vendas SZS |
| # Vendas via Marketing | [BI Comercial - Aba Canais](https://app.powerbi.com/reportEmbed?reportId=36b440ba-0af0-406a-a2ec-3a9e441dfd0c&autoAuth=true&ctid=1bc6b8f1-1aa6-4836-90ac-40f3fc44fd46) - Selecionar os últimos 6-12 meses - Tabela Consolidada | - Filtrar canais para exibir dados apenas dos canais de Marketing (Marketing, Marketing - busca paga e Marketing - mail marketing)<br>- Na tabela consolidada, copiar o # Assinados Total<br> | Vendas SZS |
| # Oportunidades Marketing | [BI Comercial - Aba Canais](https://app.powerbi.com/reportEmbed?reportId=36b440ba-0af0-406a-a2ec-3a9e441dfd0c&autoAuth=true&ctid=1bc6b8f1-1aa6-4836-90ac-40f3fc44fd46) - Selecionar os últimos 6-12 meses - Tabela Consolidada | - Filtrar canais para exibir dados apenas dos canais de Marketing (Marketing, Marketing - busca paga e Marketing - mail marketing)<br>- Na tabela consolidada, copiar o # Ops Total<br> | Vendas SZS |
| # SQL Marketing | [BI Comercial - Aba Canais](https://app.powerbi.com/reportEmbed?reportId=36b440ba-0af0-406a-a2ec-3a9e441dfd0c&autoAuth=true&ctid=1bc6b8f1-1aa6-4836-90ac-40f3fc44fd46) - Selecionar os últimos 6-12 meses - Tabela Consolidada | - Filtrar canais para exibir dados apenas dos canais de Marketing (Marketing, Marketing - busca paga e Marketing - mail marketing)<br>- Na tabela consolidada, copiar o # SQL Total<br> | Pré-Vendas SZS |
| # MQL Marketing | [BI Comercial - Aba Canais](https://app.powerbi.com/reportEmbed?reportId=36b440ba-0af0-406a-a2ec-3a9e441dfd0c&autoAuth=true&ctid=1bc6b8f1-1aa6-4836-90ac-40f3fc44fd46) - Selecionar os últimos 6-12 meses - Tabela Consolidada | - Filtrar canais para exibir dados apenas dos canais de Marketing (Marketing, Marketing - busca paga e Marketing - mail marketing)<br>- Na tabela consolidada, copiar o # Deals Total<br> | Pré-Vendas SZS |
| # Vendas via Parceiros | [BI Comercial - Aba Canais](https://app.powerbi.com/reportEmbed?reportId=36b440ba-0af0-406a-a2ec-3a9e441dfd0c&autoAuth=true&ctid=1bc6b8f1-1aa6-4836-90ac-40f3fc44fd46) - Selecionar os últimos 6-12 meses - Tabela Consolidada | - Filtrar canal para Indicação Parceiro<br>- Na tabela consolidada, copiar o # Assinados Total<br> | Vendas SZS |
| # Oportunidades Parceiros | [BI Comercial - Aba Canais](https://app.powerbi.com/reportEmbed?reportId=36b440ba-0af0-406a-a2ec-3a9e441dfd0c&autoAuth=true&ctid=1bc6b8f1-1aa6-4836-90ac-40f3fc44fd46) - Selecionar os últimos 6-12 meses - Tabela Consolidada | - Filtrar canal para Indicação Parceiro<br>- Na tabela consolidada, copiar o # Ops Total<br> | Vendas SZS |
| # SQL Parceiros | [BI Comercial - Aba Canais](https://app.powerbi.com/reportEmbed?reportId=36b440ba-0af0-406a-a2ec-3a9e441dfd0c&autoAuth=true&ctid=1bc6b8f1-1aa6-4836-90ac-40f3fc44fd46) - Selecionar os últimos 6-12 meses - Tabela Consolidada | - Filtrar canal para Indicação Parceiro<br>- Na tabela consolidada, copiar o # SQL Total<br> | Pré-Vendas SZS |
| # Indicações Parceiros | [BI Comercial - Aba Canais](https://app.powerbi.com/reportEmbed?reportId=36b440ba-0af0-406a-a2ec-3a9e441dfd0c&autoAuth=true&ctid=1bc6b8f1-1aa6-4836-90ac-40f3fc44fd46) - Selecionar os últimos 6-12 meses - Tabela Consolidada | - Filtrar canal para Indicação Parceiro<br>- Na tabela consolidada, copiar o # Deals Total<br> | Pré-Vendas SZS |
| # Vendas via Outros | Calculado no BP | (# Total Assinado sem filtro - SOMA("# Vendas via marketing";"#Vendas via Parceiros") | Vendas SZS |
| # Oportunidades via Outros | Calculado no BP | (# Total Ops sem filtro - SOMA("# Ops via marketing";"#Ops via Parceiros") | Vendas SZS |
| # SQL via Outros | Calculado no BP | (# Total SQL sem filtro - SOMA("# SQL via marketing";"#SQL via Parceiros") | Pré-Vendas SZS |
| # Indicações via Outros | Calculado no BP | (# Total Deals sem filtro - SOMA("# Deals via marketing";"#Deals via Parceiros") | Pré-Vendas SZS |
  * Novos Franqueados (Seazone Serviços)

|    |    |    |    |
|:---|:---|:---|:---|
| **Informação** | **Fonte** | **Modo de cálculo** | **Dono** |
| # Novas Franquias Marketing | [BI Comercial Franquias](https://app.powerbi.com/reportEmbed?reportId=cfd97c01-6dd7-43ea-b9ff-72b56941f4a7&autoAuth=true&ctid=1bc6b8f1-1aa6-4836-90ac-40f3fc44fd46) - Aba TT Selecionar último 6-12 meses - Leads por etapa | Etapa Assinatura: (#Deal ID - # Abertos) | Comercial Franquias |
| # Negociação Marketing | [BI Comercial Franquias](https://app.powerbi.com/reportEmbed?reportId=cfd97c01-6dd7-43ea-b9ff-72b56941f4a7&autoAuth=true&ctid=1bc6b8f1-1aa6-4836-90ac-40f3fc44fd46) - Aba TT Selecionar último 6-12 meses - Selecionar "marketing - busca paga" e "marketing" na tabela Deals por canal - Leads por etapa | # Novas Franquias + Etapa Negociação: (# Deal ID - # Abertos) | Comercial Franquias |
| # Análise COF Marketing | [BI Comercial Franquias](https://app.powerbi.com/reportEmbed?reportId=cfd97c01-6dd7-43ea-b9ff-72b56941f4a7&autoAuth=true&ctid=1bc6b8f1-1aa6-4836-90ac-40f3fc44fd46) - Aba TT Selecionar último 6-12 meses - Selecionar "marketing - busca paga" e "marketing" na tabela Deals por canal - Leads por etapa | # Negociação + Etapa Análise COF: (#Deal ID - # Abertos) | Comercial Franquias |
| # Entrevistas Marketing | [BI Comercial Franquias](https://app.powerbi.com/reportEmbed?reportId=cfd97c01-6dd7-43ea-b9ff-72b56941f4a7&autoAuth=true&ctid=1bc6b8f1-1aa6-4836-90ac-40f3fc44fd46) - Aba TT Selecionar último 6-12 meses - Selecionar "marketing - busca paga" e "marketing" na tabela Deals por canal - Leads por etapa | # Análise COF + Etapa Entrevista: (#Deal ID - # Abertos) | Comercial Franquias |
| # Qualificações Marketing | [BI Comercial Franquias](https://app.powerbi.com/reportEmbed?reportId=cfd97c01-6dd7-43ea-b9ff-72b56941f4a7&autoAuth=true&ctid=1bc6b8f1-1aa6-4836-90ac-40f3fc44fd46) - Aba TT Selecionar último 6-12 meses - Selecionar "marketing - busca paga" e "marketing" na tabela Deals por canal - Leads por etapa | # Entrevista + Etapa Qualificação: (#Deal ID - # Abertos) | Comercial Franquias |
| # Backlog Marketing | [BI Comercial Franquias](https://app.powerbi.com/reportEmbed?reportId=cfd97c01-6dd7-43ea-b9ff-72b56941f4a7&autoAuth=true&ctid=1bc6b8f1-1aa6-4836-90ac-40f3fc44fd46) - Aba TT Selecionar último 6-12 meses - Selecionar "marketing - busca paga" e "marketing" na tabela Deals por canal - Leads por etapa | # Deal ID Total - # Abertos total | Comercial Franquias |
| # Novas Franquias Embaixador | [BI Comercial Franquias](https://app.powerbi.com/reportEmbed?reportId=cfd97c01-6dd7-43ea-b9ff-72b56941f4a7&autoAuth=true&ctid=1bc6b8f1-1aa6-4836-90ac-40f3fc44fd46) - Aba TT Selecionar último 6-12 meses - Selecionar "Indicação Embaixador" na tabela Deals por canal - Leads por etapa | Etapa Assinatura: (#Deal ID - # Abertos) | Comercial Franquias |
| # Negociação Embaixador | [BI Comercial Franquias](https://app.powerbi.com/reportEmbed?reportId=cfd97c01-6dd7-43ea-b9ff-72b56941f4a7&autoAuth=true&ctid=1bc6b8f1-1aa6-4836-90ac-40f3fc44fd46) - Aba TT Selecionar último 6-12 meses - Leads por etapa | # Novas Franquias + Etapa Negociação: (# Deal ID - # Abertos) | Comercial Franquias |
| # Análise COF Embaixador | [BI Comercial Franquias](https://app.powerbi.com/reportEmbed?reportId=cfd97c01-6dd7-43ea-b9ff-72b56941f4a7&autoAuth=true&ctid=1bc6b8f1-1aa6-4836-90ac-40f3fc44fd46) - Aba TT Selecionar último 6-12 meses - Leads por etapa | # Negociação + Etapa Análise COF: (#Deal ID - # Abertos) | Comercial Franquias |
| # Entrevistas Embaixador | [BI Comercial Franquias](https://app.powerbi.com/reportEmbed?reportId=cfd97c01-6dd7-43ea-b9ff-72b56941f4a7&autoAuth=true&ctid=1bc6b8f1-1aa6-4836-90ac-40f3fc44fd46) - Aba TT Selecionar último 6-12 meses - Leads por etapa | # Análise COF + Etapa Entrevista: (#Deal ID - # Abertos) | Comercial Franquias |
| # Qualificações Embaixador | [BI Comercial Franquias](https://app.powerbi.com/reportEmbed?reportId=cfd97c01-6dd7-43ea-b9ff-72b56941f4a7&autoAuth=true&ctid=1bc6b8f1-1aa6-4836-90ac-40f3fc44fd46) - Aba TT Selecionar último 6-12 meses - Leads por etapa | # Entrevista + Etapa Qualificação: (#Deal ID - # Abertos) | Comercial Franquias |
| # Backlog Embaixador | [BI Comercial Franquias](https://app.powerbi.com/reportEmbed?reportId=cfd97c01-6dd7-43ea-b9ff-72b56941f4a7&autoAuth=true&ctid=1bc6b8f1-1aa6-4836-90ac-40f3fc44fd46) - Aba TT Selecionar último 6-12 meses - Leads por etapa | # Deal ID Total - # Abertos total | Comercial Franquias |
  * Hóspedes (Seazone Serviços) → Estruturar nos próximos BPs
  * Venda de Spots (Seazone Investimentos)

|    |    |    |
|:---|:---|:---|
| **Informação** | **Fonte** | **Dono** |
| # Vendas Spot Total | Para o BD 30 meses foi solicitado um levantamento para o time Comercial SZI | Comercial SZI, Marketplace, CEO Investimentos |
| # Vendas Spot via Parceiros | Para o BD 30 meses foi solicitado um levantamento para o time Comercial SZI | Comercial SZI, Marketplace, CEO Investimentos |
| # Indicações via Parceiros | Para o BD 30 meses foi solicitado um levantamento para o time Comercial SZI | Comercial SZI, Marketplace, CEO Investimentos |
| # Vendas Spot via Marketplace | Para o BD 30 meses foi solicitado um levantamento para o time Comercial SZI | Comercial SZI, Marketplace, CEO Investimentos |

    \
  * Compra de terrenos (Seazone Investimentos)

|    |    |    |
|:---|:---|:---|
| **Informação** | **Fonte** | **Dono** |
| # Terrenos Indicados | No BP 30 meses foi solicitado direto para a equipe responsável | Novos Projetos/CEO Investimentos |
| # Terrenos analisados | No BP 30 meses foi solicitado direto para a equipe responsável | Novos Projetos/CEO Investimentos |
| # Terrenos negociados | No BP 30 meses foi solicitado direto para a equipe responsável | Novos Projetos/CEO Investimentos |
| # Terrenos comprados | No BP 30 meses foi solicitado direto para a equipe responsável | Novos Projetos/CEO Investimentos |
* Funil

  O funil segue a seguinte estrutura:
  * Funil Novos Imóveis

|    |    |    |    |
|:---|:---|:---|:---|
| **Informação** | **Forma de cálculo** | **Origem** | **Comportamento mês a mês** |
| **Seazone Serviços - Novos Imóveis** | —-//—— | —-//—— | —-//—— |
| Meta Vendas | (# Novos Imóveis Residenciais) + (# Novos imóveis Resorts) | BP (Projeção de Receitas Residenciais + Projeção de Receitas Resorts) | Variável conforme projeção |
| **Marketing** | —-//—— | —-//—— | —-//—— |
| % Vendas Mkt | (# Vendas via Marketing)/(# Total de Contratos Assinados) | BP (Cálculo de Conversões Funil) | Constante |
| # Vendas Mkt | (Meta Vendas)\*(%Vendas Mkt) | — | Variável conforme projeção |
| % Opp - Venda | (# Vendas via Marketing)/(# Oportunidades Marketing) | BP (Cálculo de Conversões Funil) | Constante |
| # Oportunidades Marketing | (# Vendas Mkt)/(% Opp - Venda) | — | Variável conforme projeção |
| % SQL - Opp | (# Oportunidades via Marketing)/(# SQL Marketing) | BP (Cálculo de Conversões Funil) | Constante |
| # SQL Marketing | (# Oportunidades Marketing)/(% SQL - Opp) | — | Variável conforme projeção |
| % MQL - SQL | (# SQL Marketing)/(# MQL Marketing) | BP (Cálculo de Conversões Funil) | Constante |
| # MQL Marketing | (# SQL Marketing)/(% MQL - SQL) | — | Variável conforme projeção |
| % Lead - MQL | — | Time de Marketing | Constante |
| # Leads Imóveis Marketing | (# MQL Marketing)/(% Lead - MQL) | — | Variável conforme projeção |
| **Parceiros** | —-//—— | —-//—— | —-//—— |
| % Vendas Parceiros | (# Vendas via Parceiros)/(# Total de Contratos Assinados) | BP (Cálculo de Conversões Funil) | Constante |
| # Vendas Parceiros | (Meta Vendas)\*(%Vendas Parceiros) | — | Variável conforme projeção |
| % Opp - Venda | (# Vendas via Parceiros)/(# Oportunidades Parceiros) | BP (Cálculo de Conversões Funil) | Constante |
| # Oportunidades Parceiros | (# Vendas Parceiros)/(% Opp - Venda) | — | Variável conforme projeção |
| % SQL - Opp | (# Oportunidades Parceiros)/(# SQL Parceiros) | BP (Cálculo de Conversões Funil) | Constante |
| # SQL Parceiros | (# Oportunidades Parceiros)/(% SQL - Opp) | — | Variável conforme projeção |
| % Indicação - SQL | (# SQL Parceiros)/(# Indicações Parceiros) | BP (Cálculo de Conversões Funil) | Constante |
| # Indicações Parceiros | (# SQL Parceiros)/(% Indicação - SQL) | — | Variável conforme projeção |
| **Outros** | **—-//——** | **—-//——** | —-//—— |
| % Vendas Outros | (# Vendas via Outros)/(# Total de Contratos Assinados) | BP (Cálculo de Conversões Funil) | Constante |
| # Vendas Outros | (Meta Vendas)\*(%Vendas Outros) | — | Variável conforme projeção |
| % Opp - Venda | (# Vendas via Outros)/(# Oportunidades via Outros) | BP (Cálculo de Conversões Funil) | Constante |
| # Oportunidades Outros | (# Vendas Outros)/(% Opp - Venda) | — | Variável conforme projeção |
| % SQL - Opp | (# Oportunidades via Outros)/(# SQL via Outros) | BP (Cálculo de Conversões Funil) | Constante |
| # SQL Outros | (# Oportunidades Outros)/(% SQL - Opp) | — | Variável conforme projeção |
| % Indicação - SQL | (# SQL via Outros)/(# Indicações via Outros) | BP (Cálculo de Conversões Funil) | Constante |
| # Indicações Outros | (# SQL Outros)/(% Indicação - SQL) | — | Variável conforme projeção |
  * Funil Franqueados

|    |    |    |    |
|:---|:---|:---|:---|
| **Informação** | **Forma de cálculo** | **Origem** | **Comportamento mês a mês** |
| **Seazone Serviços - Novos Franqueados** | —-//—— | —-//—— | —-//—— |
| Meta Novos Franqueados | # Novas Franquias | BP (Projeção Receita Residencial) | Variável conforme projeção |
| **Marketing** | —-//—— | —-//—— | —-//—— |
| % Novas Franquias Mkt | (# Novas Franquias Marketing)/(# Novas Franquias Marketing + # Novas Franquias Embaixador) | BP (Cálculo de Conversões Funil) | Constante |
| # Novas Franquias Mkt | (Meta Novos Franqueados)\*(% Novas Franquias Mkt) | — | Variável conforme projeção |
| % Negociação - Nova Franquia | (# Novas Franquias Marketing)/(# Negociação Marketing) | BP (Cálculo de Conversões Funil) | Constante |
| # Negociação Marketing | (# Novas Franquias Mkt)/(% Negociação - Nova Franquia) | — | Variável conforme projeção |
| % COF - Negociação | (# Negociação Marketing)/(# Análise COF Marketing) | BP (Cálculo de Conversões Funil) | Constante |
| # Análise COF Marketing | (# Negociação Marketing)/(% COF - Negociação) | — | Variável conforme projeção |
| % Entrevista - COF | (# Análise COF Marketing)/(# Entrevistas Marketing) | BP (Cálculo de Conversões Funil) | Constante |
| # Entrevistas Marketing | (# Análise COF Marketing)/(% Entrevista - COF) | — | Variável conforme projeção |
| % Qualificação - Entrevista | (# Entrevistas Marketing)/(# Qualificações Marketing) | BP (Cálculo de Conversões Funil) | Constante |
| # Qualificações Marketing | (# Entrevistas Marketing)/(% Qualificação - Entrevista) | — | Variável conforme projeção |
| % Backlog - Qualificação | (# Qualificações Marketing)/(# Backlog Marketing) | BP (Cálculo de Conversões Funil) | Constante |
| # Backlog Marketing | (# Qualificações Marketing)/(% Backlog - Qualificação) | — | Variável conforme projeção |
| **Embaixadores** | **—-//——** | **—-//——** | **—-//——** |
| % Novas Franquias Embaixadores | (# Novas Franquias Embaixador)/(# Novas Franquias Marketing + # Novas Franquias Embaixador) | BP (Cálculo de Conversões Funil) | Constante |
| # Novas Franquias Embaixadores | (Meta Novos Franqueados)\*(% Novas Franquias Embaixadores) | — | Variável conforme projeção |
| % Negociação - Nova Franquia | (# Novas Franquias Embaixador)/(# Negociação Embaixador) | BP (Cálculo de Conversões Funil) | Constante |
| # Negociação Embaixadores | (# Novas Franquias Embaixadores)/(% Negociação - Nova Franquia) | — | Variável conforme projeção |
| % COF - Negociação | (# Negociação Embaixador)/(# Análise COF Embaixador) | BP (Cálculo de Conversões Funil) | Constante |
| # Análise COF Embaixadores | (# Negociação Embaixadores)/(% COF - Negociação) | — | Variável conforme projeção |
| % Entrevista - COF | (# Análise COF Embaixador)/(# Entrevistas Embaixador) | BP (Cálculo de Conversões Funil) | Constante |
| # Entrevistas Embaixadores | (# Análise COF Embaixadores)/(% Entrevista - COF) | — | Variável conforme projeção |
| % Qualificação - Entrevista | (# Entrevistas Embaixador)/(# Qualificações Embaixador) | BP (Cálculo de Conversões Funil) | Constante |
| # Qualificações Embaixadores | (# Entrevistas Embaixadores)/(% Qualificação - Entrevista) | — | Variável conforme projeção |
| % Backlog - Qualificação | (# Qualificações Embaixador)/(# Backlog Embaixador) | BP (Cálculo de Conversões Funil) | Constante |
| # Backlog Embaixadores | (# Qualificações Embaixadores)/(% Backlog - Qualificação) | — | Variável conforme projeção |
  * Funil Hóspedes → Estruturar nos próximos BPs
  * Funil Venda de Spots

|    |    |    |    |
|:---|:---|:---|:---|
| **Informação** | **Forma de cálculo** | **Origem** | **Comportamento mês a mês** |
| **Seazone Investimentos - Venda de Spots** | **—-//——** | **—-//——** | **—-//——** |
| Meta Venda Spots | (# Spots Vendidos) | BP (Projeção Receita SI) | Variável conforme projeção |
| **Parceiros** | —-//—— | —-//—— | —-//—— |
| % Vendas via Parceiros | (# Vendas Spot via Parceiros)/(# Vendas Spot Total) | BP (Cálculo de Conversões Funil) | Constante |
| # Vendas via Parceiros | (Meta Venda Spots)\*(% Vendas via Parceiros) | — | Variável conforme projeção |
| % Indicação - Venda | (# Vendas Spot via Parceiros)/(# Indicações via Parceiros) | BP (Cálculo de Conversões Funil) | Constante |
| # Indicações via Parceiros | (# Vendas via Parceiros)/(% Indicação - Venda) | — | Variável conforme projeção |
| **Marketplace** | **—-//——** | **—-//——** | **—-//——** |
| % Vendas via Marketplace | (# Vendas Spot via Marketplace)/(# Vendas Spot Total) | BP (Cálculo de Conversões Funil) | Constante |
| # Vendas via Marketplace | (Meta Venda Spots)\*(% Vendas via Marketplace) | — | Variável conforme projeção |
| % Lead - Venda | — | Marketplace | Constante |
| # Leads Marketplace | (# Vendas via Marketplace)/(% Lead - Venda) | — | Variável conforme projeção |
  * Funil Compra de Terrenos

|    |    |    |    |
|:---|:---|:---|:---|
| **Informação** | **Forma de cálculo** | **Origem** | **Comportamento mês a mês** |
| **Seazone Investimentos - Compra de Terrenos** | **—-//——** | **—-//——** | **—-//——** |
| # Terrenos comprados | (# Terrenos comprados) | BP (Projeção Receita SI) | Variável conforme projeção |
| % Negociação - Compra | (# Terrenos comprados)/(# Terrenos negociados) | BP (Cálculo de Conversões Funil) | Constante |
| # Terrenos Negociados | (# Terrenos comprados)/(% Negociação - Compra) | — | Variável conforme projeção |
| % Análise - Negociação | (# Terrenos negociados)/(# Terrenos analisados) | BP (Cálculo de Conversões Funil) | Constante |
| # Terrenos analisados | (# Terrenos negociados)/(% Análise - Negociação) | — | Variável conforme projeção |
| % Indicação - Análise | (# Terrenos Analisados)/(# Terrenos Indicados) | BP (Cálculo de Conversões Funil) | Constante |
| # Terrenos Indicados | (# Terrenos analisados)/(% Indicação - Análise) | — | Variável conforme projeção |

  \

## Cálculo dos Impostos

* Toda a Seazone Holding atua sob o Regime Tributário de Lucro Presumido. Devido à natureza das atividades exercidas, a presunção de lucro é de 32% do faturamento bruto.
* O imposto é pago trimestralmente e uma parte dele é retida na fonte pelo tomador da nota, então o valor do imposto total pago é maior do que está registrado no Admsys.
  * **Trimestre anterior: Não necessariamente quer dizer os 3 meses anteriores, e sim o desempenho entre jan-mar/abr-jun/jul-set/out-dez. Assim, se estamos em agosto, o desempenho do trimestre anterior é o faturamento abr-jun.**
* Um ponto de atenção no cálculo do IRPJ é que a segunda parte do cálculo (10% do lucro mensal que exceder R$60.000,00) irá ficar negativo caso o lucro mensal projetado seja abaixo desse valor, nesse caso, o valor do adicional deve ser 0.
* Cálculo Imposto SZS

|    |    |    |    |    |
|:---|:---|:---|:---|:---|
|    | **Mês 1** | **Mês 2** | … | **Mês Final** |
| **Receita Bruta** | Somar células abaixo |    |    |    |
| Receita Venda Franquias | Importar da projeção de receita SZS Residencial |    |    |    |
| Receita Royalty Franquias | Importar da projeção de receita SZS Residencial |    |    |    |
| Receita Taxa de Implantação | Importar da projeção de receita SZS Residencial |    |    |    |
| Receita Comissão gestão das diárias | Importar da projeção de receita SZS Resorts |    |    |    |
| Faturamento trimestre anterior | 3 primeiros meses: Importar do OrcadoxRealizadoxProjetado<br>Meses 4 - Final: Utilizar a soma das colunas anteriores referentes ao último trimestre completo<br> |    |    |    |
| — // — | — // — | — | — | — |
| Valor Imposto Mensal | Soma dos valores abaixo |    |    |    |
| IRPJ | =("Presunção de Lucro"\*"Alíquota IRPJ\*"Faturamento no período trimestral anterior"+"%Sob faturamento adicional"\*SE("Presunção de Lucro"\*"Faturamento no período trimestral anterior"<"Desconto sobre faturamento adicional";0;("Presunção de Lucro"\*"Faturamento no período trimestral anterior"-"Desconto sobre faturamento adicional")))/3 |    |    |    |
| CSLL | ="Presunção de Lucro"\*"Alíquota CSLL"\*"Faturamento no período trimestral anterior"/3 |    |    |    |
| COFINS | "Alíquota COFINS"\*"Receita Bruta mensal" |    |    |    |
| PIS/PASEP | "Alíquota PIS/PASEP"\*"Receita Bruta mensal" |    |    |    |
| ISS Venda Franquias | "Alíquota ISS 2"\*"Receita bruta com Venda de Franquias no mês" |    |    |    |
| ISS Royalty Franquias | "Alíquota ISS 1"\*"Receita bruta com Royalty de Franquias no mês" |    |    |    |
| ISS Taxa de Implantação | "Alíquota ISS 1"\*"Receita bruta com Taxa de Implantação no mês" |    |    |    |
| — // — | — // — | — | — | — |
| Constantes | — // — | — | — | — |
| Presunção de Lucro | 32% |    |    |    |
| Alíquota IRPJ | 15% |    |    |    |
| % Sob faturamento adicional | 10% |    |    |    |
| Desconto sob faturamento adicional | 60000 |    |    |    |
| Alíquota CSLL | 9% |    |    |    |
| Alíquota COFINS | 3% |    |    |    |
| Alíquota PIS/PASEP | 0,65% |    |    |    |
| Alíquota ISS 1 | 3% |    |    |    |
| Alíquota ISS 2 | 5% |    |    |    |
* Cálculo Imposto SZI

|    |    |    |    |    |
|:---|:---|:---|:---|:---|
|    | **Mês 1** | **Mês 2** | … | **Mês Final** |
| **Receita Taxa de Estruturação + Comissão de Parceiros** | Somar linhas abaixo |    |    |    |
| Receita Taxa de Estruturação | Importar da projeção de receita SZI |    |    |    |
| Receita Comissão dos Parceiros | Importar da projeção de receita SZI |    |    |    |
| **Faturamento trimestre anterior** | 3 primeiros meses: Importar do OrcadoxRealizadoxProjetado<br>Meses 4 - Final: Utilizar a soma das colunas anteriores referentes ao último trimestre completo<br> |    |    |    |
| — // — | — // — | — | — | — |
| **Valor Imposto Mensal** | Soma dos valores abaixo |    |    |    |
| IRPJ | =("Presunção de Lucro"\*"Alíquota IRPJ\*"Faturamento no período trimestral anterior"+"%Sob faturamento adicional"\*SE("Presunção de Lucro"\*"Faturamento no período trimestral anterior"<"Desconto sobre faturamento adicional";0;("Presunção de Lucro"\*"Faturamento no período trimestral anterior"-"Desconto sobre faturamento adicional")))/3 |    |    |    |
| CSLL | ="Presunção de Lucro"\*"Alíquota CSLL"\*"Faturamento no período trimestral anterior"/3 |    |    |    |
| COFINS | "Alíquota COFINS"\*"Receita Bruta mensal" |    |    |    |
| PIS/PASEP | "Alíquota PIS/PASEP"\*"Receita Bruta mensal" |    |    |    |
| ISS Taxa Estruturação | "Alíquota ISS 1"\*"Receita Taxa de Estruturação" |    |    |    |
| ISS Comissão de Parceiros | "Alíquota ISS 2"\*"Receita Comissão de Parceiros" |    |    |    |
| ISS Comissão venda Marketplace | "Alíquota ISS 3"\*"Receita Comissão venda Marketplace" |    |    |    |
| — // — | — // — | — | — | — |
| **Constantes** | — // — | — | — | — |
| Presunção de Lucro | 32% |    |    |    |
| Alíquota IRPJ | 15% |    |    |    |
| % Sob faturamento adicional | 10% |    |    |    |
| Desconto sob faturamento adicional | 60000 |    |    |    |
| Alíquota CSLL | 9% |    |    |    |
| Alíquota COFINS | 3% |    |    |    |
| Alíquota PIS/PASEP | 0,65% |    |    |    |
| Alíquota ISS 1 | 5% |    |    |    |
| Alíquota ISS 2 | 3% |    |    |    |
* Cálculo Imposto Khanto Reservas

|    |    |    |    |    |
|:---|:---|:---|:---|:---|
|    | **Mês 1** | **Mês 2** | … | **Mês Final** |
| **Receita Bruta** | Importar "**Comissão venda de reservas diretas"** da projeção de receitas Residenciais + Resorts |    |    |    |
| **Faturamento trimestre anterior** | 3 primeiros meses: Importar do OrcadoxRealizadoxProjetado<br>Meses 4 - Final: Utilizar a soma das colunas anteriores referentes ao último trimestre completo<br> |    |    |    |
| — // — | — // — | — | — | — |
| **Valor Imposto Mensal** | Soma dos valores abaixo |    |    |    |
| IRPJ | =("Presunção de Lucro"\*"Alíquota IRPJ\*"Faturamento no período trimestral anterior"+"%Sob faturamento adicional"\*SE("Presunção de Lucro"\*"Faturamento no período trimestral anterior"<"Desconto sobre faturamento adicional";0;("Presunção de Lucro"\*"Faturamento no período trimestral anterior"-"Desconto sobre faturamento adicional")))/3 |    |    |    |
| CSLL | ="Presunção de Lucro"\*"Alíquota CSLL"\*"Faturamento no período trimestral anterior"/3 |    |    |    |
| COFINS | "Alíquota COFINS"\*"Receita Bruta mensal" |    |    |    |
| PIS/PASEP | "Alíquota PIS/PASEP"\*"Receita Bruta mensal" |    |    |    |
| ISS | "Alíquota ISS 1"\*"Receita bruta mensal" |    |    |    |
| — // — | — // — | — | — | — |
| **Constantes** | — // — | — | — | — |
| Presunção de Lucro | 32% |    |    |    |
| Alíquota IRPJ | 15% |    |    |    |
| % Sob faturamento adicional | 10% |    |    |    |
| Desconto sob faturamento adicional | 60000 |    |    |    |
| Alíquota CSLL | 9% |    |    |    |
| Alíquota COFINS | 3% |    |    |    |
| Alíquota PIS/PASEP | 0,65% |    |    |    |
| Alíquota ISS 1 | 2,5% |    |    |    |
* Cálculo Imposto Marketplace

|    |    |    |    |    |
|:---|:---|:---|:---|:---|
|    | **Mês 1** | **Mês 2** | … | **Mês Final** |
| **Receita Bruta Marketplace** | Importar "Comissão Vendas Marketplace" da projeção de receita SZI |    |    |    |
| **Faturamento trimestre anterior** | 3 primeiros meses: Importar do OrcadoxRealizadoxProjetado<br>Meses 4 - Final: Utilizar a soma das colunas anteriores referentes ao último trimestre completo<br> |    |    |    |
| — // — | — // — | — | — | — |
| **Valor Imposto Mensal** | Soma dos valores abaixo |    |    |    |
| IRPJ | =("Presunção de Lucro"\*"Alíquota IRPJ\*"Faturamento no período trimestral anterior"+"%Sob faturamento adicional"\*SE("Presunção de Lucro"\*"Faturamento no período trimestral anterior"<"Desconto sobre faturamento adicional";0;("Presunção de Lucro"\*"Faturamento no período trimestral anterior"-"Desconto sobre faturamento adicional")))/3 |    |    |    |
| CSLL | ="Presunção de Lucro"\*"Alíquota CSLL"\*"Faturamento no período trimestral anterior"/3 |    |    |    |
| COFINS | "Alíquota COFINS"\*"Receita Bruta mensal" |    |    |    |
| PIS/PASEP | "Alíquota PIS/PASEP"\*"Receita Bruta mensal" |    |    |    |
| ISS | "Alíquota ISS 1"\*"Receita bruta mensal" |    |    |    |
| — // — | — // — | — | — | — |
| **Constantes** | — // — | — | — | — |
| Presunção de Lucro | 32% |    |    |    |
| Alíquota IRPJ | 15% |    |    |    |
| % Sob faturamento adicional | 10% |    |    |    |
| Desconto sob faturamento adicional | 60000 |    |    |    |
| Alíquota CSLL | 9% |    |    |    |
| Alíquota COFINS | 3% |    |    |    |
| Alíquota PIS/PASEP | 0,65% |    |    |    |
| Alíquota ISS 1 | 3%/2% |    |    |    |


---


* Pontos de melhoria

  Mostrar o quanto os investidores teriam de ganho de valuation nos diferentes planos levantados

  Focar no crescimento sem os imóveis iniciais

  Para todas as despesas colocar o on/off (Despesas e RH)

  Diferenciar as franquias diretas da SZN e as via embaixadores

  Cortar Julho

  Separar as linhas de bônus e salários

  Reembolsos tem que dar match na saída (terrenos)

  É necessário descontar as unidades por permutas dos cálculos de receitas da Investimentos?