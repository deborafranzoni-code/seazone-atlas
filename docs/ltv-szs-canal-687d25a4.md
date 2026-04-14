<!-- title: LTV SZS - CANAL | url: https://outline.seazone.com.br/doc/ltv-szs-canal-8Z35aHGTJD | area: Administrativo Financeiro -->

# LTV SZS - CANAL

\
📌

O cálculo do indicador LTV (Lifetime Value, ou Valor Vitalício do Cliente, em português) é uma medida importante para entender o valor que um cliente representa para o negócio ao longo do tempo. Em termos simples, o LTV representa a receita líquida que se espera obter de um cliente durante todo o período em que se mantém conosco. Nosso LTV é a média dos últimos doze meses de Serviço de Gestão/Gestão de Contas para o cliente Proprietário.


Passo a Passo:


* Após todo passo a passo para calcular o **[CAC SZS - Canal](https://docs.google.com/spreadsheets/d/19tgMUL9El9tO-4D2lrBSzifNXzMrzDiWxErZcDJNHGo/edit#gid=1944277996&range=1:861),** considerando a validação das despesas no **[Plano de Contas Consolidado](https://docs.google.com/spreadsheets/d/1G66FNtS61ukYh2vJtTTAxrH7WX25bCLMiXOpCmYOox4/edit#gid=1812094842)** **,** validação do imóveis ativos e a importação e classificação das despesas no **[BD Despesas Realizadas](https://docs.google.com/spreadsheets/d/19tgMUL9El9tO-4D2lrBSzifNXzMrzDiWxErZcDJNHGo/edit#gid=2027505002&range=1:13525),** pode-se iniciar o cálculo do LTV da SZS.

  Aqui serão levados em consideração 3 categorizações:
  * Categorização correta das despesas "**Despesa Implantação**" em "**Descrição"**.
  * Categorização correta das despesas "**Despesa COGs**" em "**Descrição".**
  * Categorização corretas das despesas do tipo "**CAC SZS".**
* Validar a inclusão dos **imóveis locados** e seus respectivos **faturamentos**, em seu mês de análise na aba **[Faturamento Imóvel](https://docs.google.com/spreadsheets/d/19tgMUL9El9tO-4D2lrBSzifNXzMrzDiWxErZcDJNHGo/edit#gid=1626201884&range=1:21340).**
  * Os faturamentos estão classificados em seus respectivos canais: Marketing, Parceiros, B2B, Embaixador e Outros.

  💡

  As informações são um "Importrange" do **[Dados SAPRON](https://docs.google.com/spreadsheets/d/1HQlYqvFJ3tt7MMsmtWZIaqwCSRItl4mY1l6x3XM0mhQ/edit#gid=718920194&range=1:20840)**
* Validar a inclusão das **Receitas** do mês de análise no **[BD Receitas Realizadas](https://docs.google.com/spreadsheets/d/19tgMUL9El9tO-4D2lrBSzifNXzMrzDiWxErZcDJNHGo/edit#gid=715370846&range=1:1001)** para as linhas de: Royalty das Franquias, Comissão venda de reservas diretas, Comissão de Imóveis em Resorts, Taxa de cancelamento de reservas, Implantação de novos Imóveis, Gestão de contas.
  * Utilizar Regime de caixa para todas as receitas.



---


Concluída as verificações de demais planilhas, vamos a aba **[LTV SZS - Canal](https://docs.google.com/spreadsheets/d/19tgMUL9El9tO-4D2lrBSzifNXzMrzDiWxErZcDJNHGo/edit#gid=135497792&range=1:2247),** realizar os cálculos deste indicador:

🚨

Fórmulas de Janeiro/2024 devem ser replicadas para os meses subsequentes em todos os cálculos.


* **Faturamento Bruto Seazone Serviços (Gestão)** = Receitas - Despesa de implantação.

  Soma-se todas as receitas provenientes do cliente proprietário, na gestão dos imóveis, diminuindo despesas de implantação não consideradas CAC.
  * **Receitas** do **[BD Receitas Realizadas](https://docs.google.com/spreadsheets/d/19tgMUL9El9tO-4D2lrBSzifNXzMrzDiWxErZcDJNHGo/edit#gid=715370846&range=1:1001)** somadas na fórmula: Royalty das Franquias, Comissão venda de reservas diretas, Comissão de Imóveis em Resorts, Taxa de cancelamento de reservas, Implantação de novos Imóveis, Gestão de contas.
  * **Despesa Implantação** que não são do tipo **CAC SZS** serão utilizadas para subtrair da receita de **Implantação de novos Imóveis** neste cálculo. Considera-se tudo que é gasto "recebível", como por exemplo: Vistoria, Fotógrafo, Roupa de cama…

  📌

  Esse percentual serve como base para cálculo do **Lucro Operacional Bruto Seazone Serviços (Gestão)**

  \
* **CGOS** = Soma da Despesa COGs total do período.

  Soma-se todas as de despesas classificadas como "Despesa COGs" da Seazone Serviços, no **[BD Despesas Realizadas](https://docs.google.com/spreadsheets/d/19tgMUL9El9tO-4D2lrBSzifNXzMrzDiWxErZcDJNHGo/edit#gid=2027505002&range=1:13525).** Para dividi-las pelos 5 canais, multiplica-se o valor total pelo "% de distribuição de Faturamento e COGS entre os canais".

  📌

  Esse percentual serve como base para cálculo do **Lucro Operacional Bruto Seazone Serviços (Gestão)**

  \
* **Lucro Operacional Bruto Seazone Serviços (Gestão)** = Faturamento Bruto Seazone Serviços (Gestão) - COGS

  Nesta etapa temos o faturamento bruto subtraindo as despesas COGS ("Custo dos Bens Vendidos") o resultado é o Lucro Operacional da Seazone Serviços, na gestão de imóveis.
  * E para dividi-lo pelos 5 canais, multiplica-se o valor total pelo "% de distribuição de Faturamento e COGS entre os canais".

  📌

  Esse percentual serve como base para cálculo do **LTV (MMA 12 MESES).**

  \
* **% de distribuição de Faturamento e COGS entre os canais** = Faturamento do Canal / Faturamento Total

  A fórmula busca na aba **[Faturamento Imóvel](https://docs.google.com/spreadsheets/d/19tgMUL9El9tO-4D2lrBSzifNXzMrzDiWxErZcDJNHGo/edit#gid=1626201884&range=1:21340),** o valor total faturado naquele período em determinado canal e divide pela total faturado no período, para descobrir **em percentual**, quanto cada canal contribuiu para o faturamento do período.
  * O total desta coluna precisa sempre fechar em 100%.

  📌

  Esse percentual serve como base para cálculo de **COGS** e **Faturamento Bruto Seazone Serviços (Gestão),** por canal.

  \
* **Total de Imóveis Ativos** = Soma do total de imóveis ativos até o período do cálculo.

  A fórmula contabiliza todos os imóveis considerados "Active" no **[BD Propriedades](https://docs.google.com/spreadsheets/d/19tgMUL9El9tO-4D2lrBSzifNXzMrzDiWxErZcDJNHGo/edit#gid=2047423365&range=1:24819),** ativados até o período analisado e que ainda não possuem data de inativação, mais os imóveis "Inactive" que seriam imóveis inativados no período avaliado.

  📌

  Esse percentual serve como base para cálculo do **LTV (MMA 12 MESES).**

  \
* **Total de Imóveis Ativos acima avg churn** = Soma do total de imóveis ativos acima do período de churn.

  A fórmula contabiliza todos os imóveis considerados "Active" no **[BD Propriedades](https://docs.google.com/spreadsheets/d/19tgMUL9El9tO-4D2lrBSzifNXzMrzDiWxErZcDJNHGo/edit#gid=2047423365&range=1:24819),** ativados até o período analisado e que ainda não possuem data de inativação + os imóveis "Inactive" que seriam imóveis inativados no período avaliado, porém que estejam acima do valor da coluna K: **Tempo médio de Churn (Dias).**

  \
* **Tempo médio de retenção (dias)** = Média de quantos dias os imóveis de determinado período permanecem ativos.

  A fórmula contabiliza todos os imóveis ainda "Active"(ativos) no **[BD Propriedades](https://docs.google.com/spreadsheets/d/19tgMUL9El9tO-4D2lrBSzifNXzMrzDiWxErZcDJNHGo/edit#gid=2047423365&range=1:24819),** em determinado período do cálculo, sem considerar imóveis que deram chrun antes disso.

  📌

  Esse percentual serve como base para cálculo do **LTV (MMA 12 MESES).**

  \
* **Tempo médio de Churn (Dias)** = Média de quantos dias os imóveis do histórico total permanecem ativos na Seazone.

  A fórmula contabiliza todos os imóveis administrados pela gestão da Seazone, no **[BD Propriedades](https://docs.google.com/spreadsheets/d/19tgMUL9El9tO-4D2lrBSzifNXzMrzDiWxErZcDJNHGo/edit#gid=2047423365&range=1:24819)** e analisa, em média, quantos dias eles permaneceram até a data de chrun.

  📌

  Esse percentual serve como base para cálculo do **Tempo médio de retenção (dias)** e **Total de Imóveis Ativos acima avg churn.**

  \
* **LTV (MMA 12 MESES)** = Lucro Operacional Bruto Seazone Serviços (Gestão) dos últimos 12 meses / Total de Imóveis Ativos dos últimos 12 meses) \* Tempo médio de retenção (transformado em meses)

  A fórmula contabiliza quanto de receita obtemos em média, com a gestão de determinado imóvel, considerando que ele fique ativo conosco até o tempo de chrun.

  📌

  Esse percentual serve como base para cálculo do **LTV/CAC Contrato.**

  \
* **LTV/CAC Contrato** = LTV (MMA 12 MESES) / CAC Contrato

  Sendo este um dos principais indicadores desta etapa, assim como o LTV, no **LTV/CAC Contrato** dividimos o retorno financeiro que esperamos obter com determinado contrato, pelos custos de aquisição do mesmo\*\*.\*\* Razão utilizada para medir a "saúde" de um negócio. De acordo com as referências encontradas, tem se como uma boa razão entre LTV e CAC o valor de 3. Valores próximos a 1 indicam que está sendo gasto aproximadamente o mesmo valor que um cliente retorna a empresa. Também são considerados ruins valores acima de 5, pois indicam que a empresa está deixando de investir em ações para captar novos clientes.


🚨

**De modo geral, o objetivo é aumentar o LTV (aumentando ticket médio ou a frequência de compras) e diminuir o CAC.**