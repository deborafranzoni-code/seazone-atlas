<!-- title: CAC SZI - EMPREENDIMENTO | url: https://outline.seazone.com.br/doc/cac-szi-empreendimento-6pBQZpHcxZ | area: Administrativo Financeiro -->

# CAC SZI - EMPREENDIMENTO

\
📌

O cálculo do indicador CAC (Custo de Aquisição de Cliente) é uma maneira de entender quanto a empresa gasta para adquirir cada novo cliente, comprador de uma cota, neste caso. O CAC é calculado dividindo o total dos gastos com marketing e vendas em um determinado período pelo número de novas cotas vendidas nesse mesmo período. O cálculo do CAC é importante porque ajuda a empresa a entender quanto está investindo para adquirir cada novo cliente e a avaliar a eficácia de suas estratégias de marketing e vendas. No CAC SZI - EMPREENDIMENTO, esse custo será apresentado dividido por cada empreendimento, para entender qual pode gerar mais dificuldade de venda de cotas.


Passo a Passo:


* Após todo passo a passo para calcular o **[CAC SZI - Canal](https://docs.google.com/spreadsheets/d/19tgMUL9El9tO-4D2lrBSzifNXzMrzDiWxErZcDJNHGo/edit#gid=1772686495&range=1:870),** considerando a validação das despesas no **[Plano de Contas Consolidado](https://docs.google.com/spreadsheets/d/1G66FNtS61ukYh2vJtTTAxrH7WX25bCLMiXOpCmYOox4/edit#gid=1812094842)** **,** importação e classificação das despesas no **[BD Despesas Realizadas](https://docs.google.com/spreadsheets/d/19tgMUL9El9tO-4D2lrBSzifNXzMrzDiWxErZcDJNHGo/edit#gid=2027505002&range=1:13525)** e **[BD Despesas não Relacionadas](https://docs.google.com/spreadsheets/d/19tgMUL9El9tO-4D2lrBSzifNXzMrzDiWxErZcDJNHGo/edit#gid=20112547&range=1:965)** pode-se iniciar o cálculo do **[CAC SZI - Empreendimento](https://docs.google.com/spreadsheets/d/19tgMUL9El9tO-4D2lrBSzifNXzMrzDiWxErZcDJNHGo/edit#gid=1735807051&range=1:15084).**

  \
* Validar na **[Fonte de Dados Ads - Atualizada](https://docs.google.com/spreadsheets/d/19tgMUL9El9tO-4D2lrBSzifNXzMrzDiWxErZcDJNHGo/edit#gid=40457335&range=1:998),** se as despesas com Ads do período em análise já foram incluídas.

  \
* Consultar os empreendimentos em comercialização para o período analisado e trazer informações:
  * Incluir nova linha de Spot caso tenha ocorrido novo lançamento, com o nome do Spot.
  * Checar **Data de Lançamento** deste novo empreendimento.
  * Verificar se algum dos empreendimentos em aberto teve finalização de vendas e informar no **Status** como "Grupo Fechado".
  * Caso o empreendimento esteja ainda em negociação, informar no **Status** como "Comercialização" e incluir uma nova linha nele, com o período que será calculado (geralmente mês).



---

Concluída as verificações de demais planilhas, vamos a aba **[CAC SZI - Empreendimento](https://docs.google.com/spreadsheets/d/19tgMUL9El9tO-4D2lrBSzifNXzMrzDiWxErZcDJNHGo/edit#gid=1735807051&range=1:15084),** realizar os cálculos do indicador por empreendimento:


📌

Fórmulas de Janeiro/2024 devem ser replicadas para os meses subsequentes em todos os cálculos, menos nas colunas "**MQL**", "**Opps**", "**Contratos Assinados"** e **"Marketing Ads"** onde o preenchimento é manual.


* **Contratos Assinados =** Total de cotas vendidas do empreendimento.
  * O preenchimento desta informação deve ser manual, buscando o dado no **[\[SZI\] Dashboard Unificado](https://app.powerbi.com/groups/68fb09a1-6636-4fa1-bc21-318d3fc300f0/reports/68792503-c0a3-4a95-9a98-b955602b5cde/ReportSection34d2c532abdcbe53d8ab?experience=power-bi),** filtrando pelo período e empreendimento desejado e preenchendo a informação na respectiva coluna. A informação deste B.I. a ser considerada está informada como "**Won**".
* **MQL =** Total de Leads do empreendimento analisado aptos para converter em Opps.
  * O preenchimento desta informação deve ser manual, buscando o dado no **[\[SZI\] Dashboard Unificado](https://app.powerbi.com/groups/68fb09a1-6636-4fa1-bc21-318d3fc300f0/reports/68792503-c0a3-4a95-9a98-b955602b5cde/ReportSection34d2c532abdcbe53d8ab?experience=power-bi),** filtrando pelo período e empreendimento desejado e preenchendo a informação na respectiva coluna.
* **Opps =** Total de oportunidades do empreendimento analisado.
  * O preenchimento desta informação deve ser manual, buscando o dado no **[\[SZI\] Dashboard Unificado](https://app.powerbi.com/groups/68fb09a1-6636-4fa1-bc21-318d3fc300f0/reports/68792503-c0a3-4a95-9a98-b955602b5cde/ReportSection34d2c532abdcbe53d8ab?experience=power-bi),** filtrando pelo período e empreendimento desejado e preenchendo a informação na respectiva coluna.
* **Gasto TOTAL=** Total de despesas CAC do período, (coluna Z) / Spot em "Comercialização"
  * No total soma-se todas as despesas classificadas como "CAC" da Coluna Z em **[BD Despesas Realizadas](https://docs.google.com/spreadsheets/d/19tgMUL9El9tO-4D2lrBSzifNXzMrzDiWxErZcDJNHGo/edit#gid=2027505002&range=1:13525),** mais as despesas do **[BD Despesas não Relacionadas](https://docs.google.com/spreadsheets/d/19tgMUL9El9tO-4D2lrBSzifNXzMrzDiWxErZcDJNHGo/edit#gid=20112547&range=1:965)** das linhas "15 a 18" para o período.

  🚨

  Ao dividi-las em Spots, as despesas CAC classificadas como **"MARKETING", "PARCEIROS",** **"COMERCIAL", "PV "e "OUTRO",** **devem ser rateadas para cada Spot**, seguindo a seguinte lógica de rateio:
  * MARKETING: Total das despesas Marketing Ads daquele período \* percentual de Marketing Ads correspondente ao empreendimento em questão, no período analisado, somando Marketing Ads de todos os empreendimentos daquele período.
  * PARCEIROS: Total das despesas parceiros daquele período / Quantidade de empreendimentos em comercialização no período analisado.
  * COMERCIAL: Total das despesas comercias daquele período \* percentual de Opps correspondente ao empreendimento em questão, no período analisado, somando as Opps de todos os empreendimentos daquele período.
  * PV: Total das despesas PV daquele período \* percentual de MQL correspondente ao empreendimento em questão, no período analisado, somando os MQLs de todos os empreendimentos daquele período.
  * OUTROS: Total de outras despesas não relacionadas anteriormente, daquele período / Quantidade de empreendimentos em comercialização no período analisado.

  Para melhor entendimento dos cálculos de rateio, apresentaremos a seguir um diagrama de como foram rateadas as despesas por empreendimento:

  ![](/api/attachments.redirect?id=e0269f68-c131-4ef7-adb2-b40e4882fda8)
* **Parceiros=** Total de despesas CAC PARCEIROS do período, (coluna Z) / Spot em "Comercialização"
  * Soma-se todas as despesas classificadas como "CAC" da Coluna Z e também como "PARCEIROS" na coluna "X" em **[BD Despesas Realizadas](https://docs.google.com/spreadsheets/d/19tgMUL9El9tO-4D2lrBSzifNXzMrzDiWxErZcDJNHGo/edit#gid=2027505002&range=1:13525)**, mais as despesas do **[BD Despesas não Relacionadas](https://docs.google.com/spreadsheets/d/19tgMUL9El9tO-4D2lrBSzifNXzMrzDiWxErZcDJNHGo/edit#gid=20112547&range=1:965)** linha "16" do período.

  🚨

  Ao dividi-las em Spots, a despesa CAC "**PARCEIROS",** **deve ser rateadas para cada Spot**, seguindo a seguinte lógica de rateio:
  * PARCEIROS: Total das despesas parceiros daquele período / Quantidade de empreendimentos em comercialização no período analisado.
* **Marketing=**( (Total de despesas CAC MARKETING do período - Categoria Ads) \* Percentual de Marketing Ads correspondente ao Spot)+Marketing Ads
  * Soma-se todas as despesas classificadas como "CAC" da Coluna Z e também como "MARKETING" na coluna "X" - Categoria Ads coluna "H" em **[BD Despesas Realizadas](https://docs.google.com/spreadsheets/d/19tgMUL9El9tO-4D2lrBSzifNXzMrzDiWxErZcDJNHGo/edit#gid=2027505002&range=1:13525)**, mais as despesas do **[BD Despesas não Relacionadas](https://docs.google.com/spreadsheets/d/19tgMUL9El9tO-4D2lrBSzifNXzMrzDiWxErZcDJNHGo/edit#gid=20112547&range=1:965)** linha "17" do período.

  ⚠️

  Nesta etapa você precisa retirar do cálculo as despesas classificadas como "Ads" na coluna "H" do **[BD Despesas Realizadas](https://docs.google.com/spreadsheets/d/19tgMUL9El9tO-4D2lrBSzifNXzMrzDiWxErZcDJNHGo/edit#gid=2027505002&range=1:13525)**, pois iremos considerar os ADS da **[Fonte de Dados Ads - Atualizada](https://docs.google.com/spreadsheets/d/19tgMUL9El9tO-4D2lrBSzifNXzMrzDiWxErZcDJNHGo/edit#gid=40457335&range=1:998),** e não do Admsys. Os dados da **[Fonte de Dados Ads - Atualizada](https://docs.google.com/spreadsheets/d/19tgMUL9El9tO-4D2lrBSzifNXzMrzDiWxErZcDJNHGo/edit#gid=40457335&range=1:998)** já está com a informação exata, separada por Spots, por isso será utilizado.

  🚨

  Ao dividi-las em Spots, a despesa CAC "**MARKETING",** **deve ser rateadas para cada Spot**, seguindo a seguinte lógica de rateio:
  * MARKETING: Total das despesas Marketing Ads daquele período \* percentual de Marketing Ads correspondente ao empreendimento em questão, no período analisado, somando Marketing Ads de todos os empreendimentos daquele período.
* **Pré-Vendas=** Total de despesas CAC PV do período, (coluna Z) \* Percentual de MQL relativo ao Spot
  * Soma-se todas as despesas classificadas como "CAC" da Coluna Z e também como "PV" na coluna "W" em **[BD Despesas Realizadas](https://docs.google.com/spreadsheets/d/19tgMUL9El9tO-4D2lrBSzifNXzMrzDiWxErZcDJNHGo/edit#gid=2027505002&range=1:13525)**, mais as despesas do **[BD Despesas não Relacionadas](https://docs.google.com/spreadsheets/d/19tgMUL9El9tO-4D2lrBSzifNXzMrzDiWxErZcDJNHGo/edit#gid=20112547&range=1:965)** linha "18" do período.

  🚨

  Ao dividi-las em Spots, a despesa CAC "**PV",** **deve ser rateadas para cada Spot**, seguindo a seguinte lógica de rateio:
  * PV: Total das despesas PV daquele período \* percentual de MQL correspondente ao empreendimento em questão, no período analisado, somando os MQLs de todos os empreendimentos daquele período.
* **Comercial=** Total de despesas CAC COMERCIAL do período, (coluna Z) \* Percentual de Opps relativo ao Spot
  * Soma-se todas as despesas classificadas como "CAC" da Coluna Z e também como "COMERCIAL" na coluna "W" em **[BD Despesas Realizadas](https://docs.google.com/spreadsheets/d/19tgMUL9El9tO-4D2lrBSzifNXzMrzDiWxErZcDJNHGo/edit#gid=2027505002&range=1:13525)**, mais as despesas do **[BD Despesas não Relacionadas](https://docs.google.com/spreadsheets/d/19tgMUL9El9tO-4D2lrBSzifNXzMrzDiWxErZcDJNHGo/edit#gid=20112547&range=1:965)** linha "15" do período.

  🚨

  Ao dividi-las em Spots, a despesa CAC "**COMERCIAL",** **deve ser rateadas para cada Spot**, seguindo a seguinte lógica de rateio:
  * COMERCIAL: Total das despesas comerciais daquele período \* percentual de Opps correspondente ao empreendimento em questão, no período analisado, somando os Opps de todos os empreendimentos daquele período.
* **Outros=** Total de despesas CAC OUTROS do período, (coluna Z) / Spot em "Comercialização"
  * Soma-se todas as despesas classificadas como "CAC" da Coluna Z e também como "OUTROS" na coluna "X" em **[BD Despesas Realizadas](https://docs.google.com/spreadsheets/d/19tgMUL9El9tO-4D2lrBSzifNXzMrzDiWxErZcDJNHGo/edit#gid=2027505002&range=1:13525).**

  🚨

  **Atenção especial em despesa de Parceiros pois em: SZI → Comercial →Comissão → Corretagem, as comissão pagas a Seazoners que adquirem Spots da SZI precisamos ajustar manualmente para serem enquadradas como canal "Outros".**
* **Pessoas=** Total de despesas CAC do período consideradas "RH" / Spot em "Comercialização"
  * Na despesa de "Pessoas" soma-se todas as despesas classificadas como "CAC" da Coluna Z, mas que também correspondam ao CC "RH" na coluna G, do **[BD Despesas Realizadas](https://docs.google.com/spreadsheets/d/19tgMUL9El9tO-4D2lrBSzifNXzMrzDiWxErZcDJNHGo/edit#gid=2027505002&range=1:13525),** mais as despesas do **[BD Despesas não Relacionadas](https://docs.google.com/spreadsheets/d/19tgMUL9El9tO-4D2lrBSzifNXzMrzDiWxErZcDJNHGo/edit#gid=20112547&range=1:965)** das linhas "15 a 18" para o período. Após essa soma precisa-se dividir a despesa entre os Spots, seguindo as premissas de rateio a seguir:

  🚨

  As despesas CAC coluna Z + RH coluna G, classificadas como **"MARKETING", "PARCEIROS",** **"COMERCIAL" e "PV",** **devem ser rateadas para cada Spot**, seguindo a seguinte lógica de rateio:
  * MARKETING: Total das despesas de RH Marketing daquele período \* percentual de Marketing Ads correspondente ao empreendimento em questão, no período analisado, somando Marketing Ads de todos os empreendimentos daquele período.
  * PARCEIROS: Total das despesas parceiros RH daquele período / Quantidade de empreendimentos em comercialização no período analisado.
  * COMERCIAL: Total das despesas comercias RH daquele período \* percentual de Opps correspondente ao empreendimento em questão, no período analisado, somando as Opps de todos os empreendimentos daquele período.
  * PV: Total das despesas PV RH daquele período \* percentual de MQL correspondente ao empreendimento em questão, no período analisado, somando os MQLs de todos os empreendimentos daquele período.

  \
* **Marketing Ads=** Total de Ads gerados pelo empreendimento analisado
  * O preenchimento desta informação deve ser manual, buscando o dado na **[Fonte de Dados Ads - Atualizada](https://docs.google.com/spreadsheets/d/19tgMUL9El9tO-4D2lrBSzifNXzMrzDiWxErZcDJNHGo/edit#gid=40457335&range=1:998),** nela constará o valor de Ads de cada empreendimento, separado no período meses. Não há fórmulas aplicadas nesta célula.
* **S.I.G=** Total de despesas CAC do período consideradas "S.I.G" / Spot em "Comercialização"
  * Na despesa de "S.I.G" soma-se todas as despesas classificadas como "CAC" da Coluna Z, mas que também correspondam ao CC "S.I.G" na coluna G, do **[BD Despesas Realizadas](https://docs.google.com/spreadsheets/d/19tgMUL9El9tO-4D2lrBSzifNXzMrzDiWxErZcDJNHGo/edit#gid=2027505002&range=1:13525).** Após essa soma precisa-se dividir a despesa entre os Spots, seguindo as premissas de rateio a seguir:

  🚨

  As despesas CAC coluna Z + S.I.G coluna G, classificadas como **"MARKETING", "PARCEIROS",** **"COMERCIAL" e "PV",** **devem ser rateadas para cada Spot**, seguindo a seguinte lógica de rateio:
  * MARKETING: Total das despesas de S.I.G Marketing daquele período \* percentual de Marketing Ads correspondente ao empreendimento em questão, no período analisado, somando Marketing Ads de todos os empreendimentos daquele período.
  * PARCEIROS: Total das despesas parceiros S.I.G daquele período / Quantidade de empreendimentos em comercialização no período analisado.
  * COMERCIAL: Total das despesas comercias S.I.G daquele período \* percentual de Opps correspondente ao empreendimento em questão, no período analisado, somando as Opps de todos os empreendimentos daquele período.
  * PV: Total das despesas PV S.I.G daquele período \* percentual de MQL correspondente ao empreendimento em questão, no período analisado, somando os MQLs de todos os empreendimentos daquele período.

  \
* **Outros=** Total de despesas CAC OUTROS do período, (coluna Z) / Spot em "Comercialização"
  * Soma-se todas as despesas classificadas como "CAC" da Coluna Z mas que correspondem "OUTROS" na coluna "X" no **[BD Despesas Realizadas](https://docs.google.com/spreadsheets/d/19tgMUL9El9tO-4D2lrBSzifNXzMrzDiWxErZcDJNHGo/edit#gid=2027505002&range=1:13525).**
  * Nesta opção deve entrar também todas as demais despesas que não possuem CC = RH ou CC = S.I.G (coluna G) e que não sejam Ads (coluna H) do **[BD Despesas Realizadas](https://docs.google.com/spreadsheets/d/19tgMUL9El9tO-4D2lrBSzifNXzMrzDiWxErZcDJNHGo/edit#gid=2027505002&range=1:13525).**

  🚨

  **Atenção especial em despesa de Parceiros pois em: SZI → Comercial →Comissão → Corretagem, as comissão pagas a Seazoners que adquirem Spots da SZI precisamos ajustar manualmente para serem enquadradas como canal "Outros".**
* **CAC Contrato =** Gasto TOTAL/Contratos Assinados
  * Essa fórmula considera o valor total de despesas daquele empreendimento, dividindo pelos contratos assinados do mesmo, resultando quanto "custou" a venda de cada um dos contratos daquele Spot.
  * A fórmula do total deve ser replicada aos canais.
  * Se algum dos valores da divisão for = zero, a fórmula retornará com a palavra "INFINITO".

  📌

  Esse indicador CAC de extrema importância, demonstra o custo que a Sezoane teve para a venda de cada contrato de determinado empreendimento.
* **Valor acc. dos Contratos Pipedrive =** Total de contratos acc do período.
  * Valor preenchido manualmente, retirado do .
* **Comissao =** Valor acc. dos Contratos Pipedrive \* Percentual de comissão do canal
  * Valor de comissão total pago a determinado empreendimento.
* **Comissão/ Contrato=** Comissao / Contratos Assinados
  * Indica o valor de comissão pago a cada contrato, de determinado empreendimento.

  \


🚨

A coluna "**Check"** quando preenchida com **"OK"** serve para indicar que os cálculos já foram conferidos e validados.


\