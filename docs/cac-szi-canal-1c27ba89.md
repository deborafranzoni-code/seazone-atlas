<!-- title: CAC SZI - CANAL | url: https://outline.seazone.com.br/doc/cac-szi-canal-L1urHa5mTf | area: Administrativo Financeiro -->

# CAC SZI - CANAL

\
📌

O cálculo do indicador CAC (Custo de Aquisição de Cliente) é uma maneira de entender quanto a empresa gasta para adquirir cada novo cliente, comprador de uma cota. O CAC é calculado dividindo o total dos gastos com marketing e vendas em um determinado período pelo número de novas cotas vendidas nesse mesmo período. O cálculo do CAC é importante porque ajuda a empresa a entender quanto está investindo para adquirir cada novo cliente e a avaliar a eficácia de suas estratégias de marketing e vendas.


Passo a Passo:


* Validar **[Plano de Contas Consolidado](https://docs.google.com/spreadsheets/d/1G66FNtS61ukYh2vJtTTAxrH7WX25bCLMiXOpCmYOox4/edit#gid=1812094842)** para garantir a inclusão de todas as despesas conforme o Plano de Contas atualizado e categorizações manuais necessários ao cálculo do indicador.
  * Categorizações corretas das despesas do tipo "**CAC SZI";**
  * Categorização corretas dos percentuais de despesas na coluna "**% CAC SZI";**
  * Categorizações corretas dos rateios: "COMERCIAL" e "PV" em "**Rateio CAC SZS & SZI**";
  * Categorizações corretas dos canais: "MARKETING" e "PARCEIROS" em "**Canal Despesa SZS & SZI**";
  * Classificação correta das despesas de RH que possuem "**Bonificação Trimestral**".
* Buscar no **[AdmSys Consolidado](https://docs.google.com/spreadsheets/d/1iglE6IY28DDarrcFJ03QkFuZvvvtwR9Jp_DEPJdkrnw/edit#gid=1247423448&range=1:22092)** as despesas do período em tratativa e colar no **[BD Despesas Realizadas](https://docs.google.com/spreadsheets/d/19tgMUL9El9tO-4D2lrBSzifNXzMrzDiWxErZcDJNHGo/edit#gid=2027505002&range=1:13525).**

  \
* Mediante as categorizações realizadas no **[Plano de Contas Consolidado](https://docs.google.com/spreadsheets/d/19tgMUL9El9tO-4D2lrBSzifNXzMrzDiWxErZcDJNHGo/edit#gid=1408828674&range=1:1500)**, automaticamente as categorizações serão trazidas para o **[BD Despesas Realizadas](https://docs.google.com/spreadsheets/d/19tgMUL9El9tO-4D2lrBSzifNXzMrzDiWxErZcDJNHGo/edit#gid=2027505002&range=1:13525).**
  * Fórmulas de Janeiro/2024 devem ser replicadas para os meses subsequentes, elas estão desde a coluna K até a coluna Z do **[BD Despesas Realizadas](https://docs.google.com/spreadsheets/d/19tgMUL9El9tO-4D2lrBSzifNXzMrzDiWxErZcDJNHGo/edit#gid=2027505002&range=1:13525).**
* Após as categorizações trazidas ao **[BD Despesas Realizadas](https://docs.google.com/spreadsheets/d/19tgMUL9El9tO-4D2lrBSzifNXzMrzDiWxErZcDJNHGo/edit#gid=2027505002&range=1:13525),** deve-se ajustar a aba **[BD Despesas não Relacionadas](https://docs.google.com/spreadsheets/d/19tgMUL9El9tO-4D2lrBSzifNXzMrzDiWxErZcDJNHGo/edit#gid=20112547&range=1:965)**
  * Fórmulas de Janeiro/2024 devem ser replicadas para os períodos subsequentes.



---

Concluída as verificações de demais planilhas, vamos a aba **[CAC SZI - Canal](https://docs.google.com/spreadsheets/d/19tgMUL9El9tO-4D2lrBSzifNXzMrzDiWxErZcDJNHGo/edit#gid=1772686495&range=1:870),** realizar os cálculos deste indicador:


🚨

Fórmulas de Janeiro/2024 devem ser replicadas para os meses subsequentes, menos nas colunas "**MQL**", "**Opps**", "**Investidores Contratos Assinados**", "**Contratos Assinados" e "Valor acc. dos Contratos Pipedrive",** onde o preenchimento é manual.


* **Investidores Contratos Assinados =** Total de Vendas do período
  * O preenchimento desta informação deve ser manual, buscando o dado no **[\[SZI\] Dashboard Unificado](https://app.powerbi.com/groups/68fb09a1-6636-4fa1-bc21-318d3fc300f0/reports/68792503-c0a3-4a95-9a98-b955602b5cde/ReportSection34d2c532abdcbe53d8ab?experience=power-bi),** filtrando pelo período e canal desejado e preenchendo a informação na respectiva coluna. A informação deste B.I. a ser considerada está informada como "**Won**".

  \
* **Contratos Assinados =** Total de Vendas do período

  🚨

  A princípio essa informação é o mesmo número de "**Investidores Contratos Assinados**", mas a ideia é que logo tenhamos informações separadas, para entender a recorrência de compra de cotas por um determinado cliente.
  * O preenchimento desta informação deve ser manual, buscando o dado no **[\[SZI\] Dashboard Unificado](https://app.powerbi.com/groups/68fb09a1-6636-4fa1-bc21-318d3fc300f0/reports/68792503-c0a3-4a95-9a98-b955602b5cde/ReportSection34d2c532abdcbe53d8ab?experience=power-bi),** filtrando pelo período e canal desejado e preenchendo a informação na respectiva coluna. A informação deste B.I. a ser considerada está informada como "**Won**".

  \
* **MQL =** Total de Leads do período analisado aptos para converter em Opps.
  * O preenchimento desta informação deve ser manual, buscando o dado no **[\[SZI\] Dashboard Unificado](https://app.powerbi.com/groups/68fb09a1-6636-4fa1-bc21-318d3fc300f0/reports/68792503-c0a3-4a95-9a98-b955602b5cde/ReportSection34d2c532abdcbe53d8ab?experience=power-bi),** filtrando pelo período e canal desejado e preenchendo a informação na respectiva coluna.
* **Opps =** Total de oportunidades do período analisado.
  * O preenchimento desta informação deve ser manual, buscando o dado no **[\[SZI\] Dashboard Unificado](https://app.powerbi.com/groups/68fb09a1-6636-4fa1-bc21-318d3fc300f0/reports/68792503-c0a3-4a95-9a98-b955602b5cde/ReportSection34d2c532abdcbe53d8ab?experience=power-bi),** filtrando pelo período e canal desejado e preenchendo a informação na respectiva coluna.
* **TOTAL=** Total de despesas CAC do período, (coluna Z).
  * No total soma-se todas as despesas classificadas como "CAC" da Coluna Z em **[BD Despesas Realizadas](https://docs.google.com/spreadsheets/d/19tgMUL9El9tO-4D2lrBSzifNXzMrzDiWxErZcDJNHGo/edit#gid=2027505002&range=1:13525)**, mais as despesas do **[BD Despesas não Relacionadas](https://docs.google.com/spreadsheets/d/19tgMUL9El9tO-4D2lrBSzifNXzMrzDiWxErZcDJNHGo/edit#gid=20112547&range=1:965)** das linhas "15 a 18" para o período.

  ⚠️

  Ao dividi-las em canais, as despesas CAC classificadas como "COMERCIAL" e "PV "devem ser rateadas para cada canal, seguindo a seguinte lógica de rateio:
  * COMERCIAL: Total das despesas comercias daquele período \* percentual de Opps geradas pelo canal em questão.
  * PV: Total das despesas PV daquele período \* percentual de MQL gerados pelo canal em questão.

  Para melhor entendimento do rateio, apresentaremos a seguir um diagrama de como foram rateadas as despesas de cada canal:

  ![](/api/attachments.redirect?id=444810a8-76da-4259-ab49-15dda0f85a80)
* **Pessoas =** Total de despesas CAC do período (coluna Z), com CC RH.
  * No total soma-se todas as despesas classificadas como "CAC" da Coluna Z e CC RH em **[BD Despesas Realizadas](https://docs.google.com/spreadsheets/d/19tgMUL9El9tO-4D2lrBSzifNXzMrzDiWxErZcDJNHGo/edit#gid=2027505002&range=1:13525),** da Seazone Investimentos, mais as despesas do **[BD Despesas não Relacionadas](https://docs.google.com/spreadsheets/d/19tgMUL9El9tO-4D2lrBSzifNXzMrzDiWxErZcDJNHGo/edit#gid=20112547&range=1:965),** para o período. Entram despesas como Salário, Benefícios, Rescisão, Bonificação e Variável.

  ⚠️

  Ao dividir em canais, a despesa "Pessoas" segue a mesma regra de rateio explicada anteriormente em "TOTAL", para as classificações: "COMERCIAL" e "PV".

  \
* **Ads=** Total de despesas CAC do período, (Coluna Z), com CC "Publicidade" e Canal Despesa "MARKETING".
  * No total soma-se todas as despesas classificadas como "CAC" da Coluna Z e CC Publicidade, mas com o canal de despesa Marketing em **[BD Despesas Realizadas](https://docs.google.com/spreadsheets/d/19tgMUL9El9tO-4D2lrBSzifNXzMrzDiWxErZcDJNHGo/edit#gid=2027505002&range=1:13525).**
  * Aqui trata-se de demais despesas de Marketing não relacionadas a pessoas (RH).
* **S.I.G=** Total de despesas CAC do período, (Coluna Z), com CC "S.I.G".
  * No total soma-se todas as despesas classificadas como "CAC" da Coluna Z e CC S.I.G em **[BD Despesas Realizadas](https://docs.google.com/spreadsheets/d/19tgMUL9El9tO-4D2lrBSzifNXzMrzDiWxErZcDJNHGo/edit#gid=2027505002&range=1:13525).**

  ⚠️

  Para distribuí-las nos canais, basta considerar a despesa classificada para aquele canal, mais "COMERCIAL" e "PV", conforme regra de rateio explicada anteriormente em "TOTAL".
* **Outros=** Total de despesas CAC não relacionadas nas despesas anteriores.

  🚨

  **Atenção especial em despesa de Parceiros pois em: SZI → Comercial →Comissão → Corretagem, as comissão pagas a Seazoners que adquirem Spots da SZI precisamos ajustar manualmente para serem enquadradas como canal "Outros".**

  \
* **CAC Investidor =** Total de despesas CAC (Coluna Z) /Investidores Contratos Assinados
  * A fórmula do total deve ser replicada aos canais.
  * Se algum dos valores da divisão for = zero, a fórmula retornará com a palavra "INFINITO".

  📌

  Esse indicador CAC de extrema importância, demonstra o custo total e por canal, que a Sezoane teve para adquirir 1 cliente investidor.

  \
* **CAC Contrato =** Total de despesas CAC (Coluna Z) /Contratos Assinados
  * A fórmula do total deve ser replicada aos canais.
  * Se algum dos valores da divisão for = zero, a fórmula retornará com a palavra "INFINITO".

  📌

  Esse indicador CAC de extrema importância, demonstra o custo total e por canal, que a Sezoane teve para a venda de cada contrato.

  🚨

  A princípio essa informação é o mesmo número de "**CAC Investidor**", mas a ideia é que logo tenhamos informações separadas, para entender o custo de cada cotas vendida e não por clientes, visto que o mesmo cliente pode adquirir mais de uma cota, reduzindo o valor o CAC Contrato.

  \
* **Valor acc. dos Contratos Pipedrive =** Total de contratos acc do período.
  * Valor preenchido manualmente, retirado do .
* **Comissao =** Valor acc. dos Contratos Pipedrive \* Percentual de comissão do canal
  * Valor de comissão total pago ao canal.
  * Para canal Marketing foi considerado valor de 6%, para o canal Parceiros o valor de 2% e Outros 6%.
* **Comissão/ Contrato=** Comissao / Contratos Assinados
  * Indica o valor de comissão pago a cada contrato, de determinado canal.

  \

🚨

A coluna "**Status"** quando preenchida com **"OK"** serve para indicar que os cálculos já foram conferidos e validados.