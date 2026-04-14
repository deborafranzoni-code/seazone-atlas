<!-- title: CAC SZS - CANAL | url: https://outline.seazone.com.br/doc/cac-szs-canal-K7UfPwJySI | area: Administrativo Financeiro -->

# CAC SZS - CANAL

\
📌

O cálculo do indicador CAC (Custo de Aquisição de Cliente) é uma maneira de entender quanto a empresa gasta para adquirir cada novo proprietário como cliente. O CAC é calculado dividindo o total dos gastos com marketing e vendas em um determinado período pelo número de novos proprietários que foram conquistados nesse mesmo período. O cálculo do CAC é importante porque ajuda a empresa a entender quanto está investindo para adquirir cada novo cliente e a avaliar a eficácia de suas estratégias de marketing e vendas.


Passo a Passo:

* Validar **[Plano de Contas Consolidado](https://docs.google.com/spreadsheets/d/1G66FNtS61ukYh2vJtTTAxrH7WX25bCLMiXOpCmYOox4/edit#gid=1812094842)** para garantir a inclusão de todas as despesas conforme o Plano de Contas atualizado e categorizações manuais necessários ao cálculo do indicador.
  * Categorizações corretas das despesas do tipo "**CAC SZS"** e **"CAC NÃO RELACIONAL";**
  * Categorização corretas dos percentuais de despesas na coluna "**% CAC SZS";**
  * Categorizações corretas dos rateios: "COMERCIAL", "PV" e "IMPLANTAÇÃO" em "**Rateio CAC SZS & SZI**";
  * Categorizações corretas dos canais: "B2B", "EMBAIXADOR", "MARKETING" e "PARCEIROS" em "**Canal Despesa SZS & SZI**";
  * Classificação correta das despesas de RH que possuem "**Bonificação Trimestral**".
* Validar a inclusão dos **imóveis ativos** conosco, no período de análise na aba **[BD Propriedades.](https://docs.google.com/spreadsheets/d/19tgMUL9El9tO-4D2lrBSzifNXzMrzDiWxErZcDJNHGo/edit#gid=2047423365&range=1:24819)**

  Cada imóvel é classificado automaticamente, na coluna Q, dentro de um dos 5 canais de análise:
  * Marketing: marketing; marketing - busca paga; Marketing - Mídia Offline.
  * Parceiros: Indicação de Corretor; Indicação Parceiro; Indicação de Parceiro PF; Indicação de Afiliado.
  * B2B: Indicação de Construtora e B2B.
  * Embaixador: Indicação Embaixador.
  * Outros: São todos os demais, como: Indicação de Anfitrião; Indicação de Clientes; *Relacionamento Seazone;* Contato Direto; Cliente SZS, indicação pf; Indicação Colaborador; Prospecção Ativa; crm (contato antigo); Leads Reativados; Indicação Lofteria; Cliente SZI…

  💡

  As informações são um "Importrange" da **[ApartmentSapron](https://docs.google.com/spreadsheets/d/14QwKhwGxMpycXd2dM_osbRCN2Ktn455tbtn5ncw5GTo/edit#gid=428937263&range=1:2982).**
* Buscar no **[AdmSys Consolidado](https://docs.google.com/spreadsheets/d/1iglE6IY28DDarrcFJ03QkFuZvvvtwR9Jp_DEPJdkrnw/edit#gid=1247423448&range=1:22092)** as despesas do período em tratativa e colar no **[BD Despesas Realizadas](https://docs.google.com/spreadsheets/d/19tgMUL9El9tO-4D2lrBSzifNXzMrzDiWxErZcDJNHGo/edit#gid=2027505002&range=1:13525).**

  \
* Mediante as categorizações realizadas no **[Plano de Contas Consolidado](https://docs.google.com/spreadsheets/d/19tgMUL9El9tO-4D2lrBSzifNXzMrzDiWxErZcDJNHGo/edit#gid=1408828674&range=1:1500)**, automaticamente as categorizações serão trazidas para o **[BD Despesas Realizadas](https://docs.google.com/spreadsheets/d/19tgMUL9El9tO-4D2lrBSzifNXzMrzDiWxErZcDJNHGo/edit#gid=2027505002&range=1:13525).**
  * Fórmulas de Janeiro/2024 devem ser replicadas para os meses subsequentes, elas estão desde a coluna K até a coluna Z do **[BD Despesas Realizadas](https://docs.google.com/spreadsheets/d/19tgMUL9El9tO-4D2lrBSzifNXzMrzDiWxErZcDJNHGo/edit#gid=2027505002&range=1:13525).**
* Após as categorizações trazidas ao **[BD Despesas Realizadas](https://docs.google.com/spreadsheets/d/19tgMUL9El9tO-4D2lrBSzifNXzMrzDiWxErZcDJNHGo/edit#gid=2027505002&range=1:13525),** deve-se ajustar a aba **[BD Despesas não Relacionadas](https://docs.google.com/spreadsheets/d/19tgMUL9El9tO-4D2lrBSzifNXzMrzDiWxErZcDJNHGo/edit#gid=20112547&range=1:965)**
  * Fórmulas de Janeiro/2024 devem ser replicadas para os períodos subsequentes.



---


Concluída as verificações de demais planilhas, vamos a aba **[CAC SZS - Canal](https://docs.google.com/spreadsheets/d/19tgMUL9El9tO-4D2lrBSzifNXzMrzDiWxErZcDJNHGo/edit#gid=1944277996&range=1:861),** realizar os cálculos deste indicador:


🚨

Fórmulas de Janeiro/2024 devem ser replicadas para os meses subsequentes, menos nas colunas "MQL" e "Opps" onde o preenchimento é manual.


* **Proprietários Contratos Assinados =** Todos os contratos assinados com proprietários no período analisado.
  * A fórmula busca na aba **[BD Propriedades](https://docs.google.com/spreadsheets/d/19tgMUL9El9tO-4D2lrBSzifNXzMrzDiWxErZcDJNHGo/edit#gid=2047423365&range=1:24819),** todos os contratos assinados *com proprietários* naquele período.

  \
* **Contratos Assinados =** Todos os contratos assinados no período analisado.
  * A fórmula busca na aba **[BD Propriedades](https://docs.google.com/spreadsheets/d/19tgMUL9El9tO-4D2lrBSzifNXzMrzDiWxErZcDJNHGo/edit#gid=2047423365&range=1:24819),** todos os contratos assinados naquele período, aqui consideramos total de imóveis, visto que um mesmo proprietário pode possuir mais de um imóvel sob nossa gestão.

  \
* **Contratos Assinados Sem Taxa de Implantação =** Todos os contratos assinados no período analisado, sem taxa de implantação.
  * A fórmula busca na aba **[BD Propriedades](https://docs.google.com/spreadsheets/d/19tgMUL9El9tO-4D2lrBSzifNXzMrzDiWxErZcDJNHGo/edit#gid=2047423365&range=1:24819),** todos os contratos assinados naquele período, considerando total de imóveis ativados sem cobrança da taxa de implantação, se tornando para a Seazone uma soma no custo de aquisição do cliente.

  \
* **Ativações de Imóveis =** Total de imóveis ativados no período analisado.
  * A fórmula busca na aba **[BD Propriedades](https://docs.google.com/spreadsheets/d/19tgMUL9El9tO-4D2lrBSzifNXzMrzDiWxErZcDJNHGo/edit#gid=2047423365&range=1:24819),** todos os imóveis que foram ativados no período analisado.

  💡

  Entende-se como "Imóveis Ativados" todos os imóveis aptos para geração de receitas.

  \
* **MQL =** Total de Leads do período analisado aptos para converter em Opps.
  * O preenchimento desta informação deve ser manual, buscando o dado no **[B.I. Seazone Serviços](https://app.powerbi.com/reportEmbed?reportId=4a5400bf-0ec7-466d-8151-29bdae9f07ad&autoAuth=true&ctid=1bc6b8f1-1aa6-4836-90ac-40f3fc44fd46),** filtrando pelo período e canal desejado e preenchendo a informação na respectiva coluna.

  \
* **Opps =** Total de oportunidades do período analisado.
  * O preenchimento desta informação deve ser manual, buscando o dado no **[B.I. Seazone Serviços](https://app.powerbi.com/reportEmbed?reportId=4a5400bf-0ec7-466d-8151-29bdae9f07ad&autoAuth=true&ctid=1bc6b8f1-1aa6-4836-90ac-40f3fc44fd46),** filtrando pelo período e canal desejado e preenchendo a informação na respectiva coluna.

  \
* **TOTAL=** Total de despesas CAC do período (Coluna T).
  * No total soma-se todas as despesas classificadas como "CAC" em **[BD Despesas Realizadas](https://docs.google.com/spreadsheets/d/19tgMUL9El9tO-4D2lrBSzifNXzMrzDiWxErZcDJNHGo/edit#gid=2027505002&range=1:13525),** informadas na coluna "T", mais as despesas do **[BD Despesas não Relacionadas](https://docs.google.com/spreadsheets/d/19tgMUL9El9tO-4D2lrBSzifNXzMrzDiWxErZcDJNHGo/edit#gid=20112547&range=1:965),** da linha "2 a 13", para o período.

  ⚠️

  Ao dividi-las em canais, as despesas CAC classificadas como "COMERCIAL", "PV" e "IMPLANTAÇÃO" devem ser rateadas para cada canal, seguindo a seguinte lógica de rateio:
  * COMERCIAL: Total das despesas comercias daquele período \* percentual de Opps geradas pelo canal em questão.
  * PV: Total das despesas PV daquele período \* percentual de MQL gerados pelo canal em questão.
  * IMPLANTAÇÃO: Total das despesas implantação daquele período \* percentual de ativação de imóveis gerados pelo canal em questão.

  \
  \
* **Pessoas =** Total de despesas CAC do período, (Coluna T),com CC RH.
  * No total soma-se todas as despesas classificadas como "CAC" e CC RH em **[BD Despesas Realizadas](https://docs.google.com/spreadsheets/d/19tgMUL9El9tO-4D2lrBSzifNXzMrzDiWxErZcDJNHGo/edit#gid=2027505002&range=1:13525),** mais as despesas do **[BD Despesas não Relacionadas](https://docs.google.com/spreadsheets/d/19tgMUL9El9tO-4D2lrBSzifNXzMrzDiWxErZcDJNHGo/edit#gid=20112547&range=1:965),** para o período. Entram despesas como Salário, Benefícios, Rescisão, Bonificação e Variável.

  ⚠️

  Ao dividir em canais, a despesa "Pessoas" segue a mesma regra de rateio explicada anteriormente em "TOTAL", para as classificações: "COMERCIAL", "PV" e "IMPLANTAÇÃO".
* **Ads=** Total de despesas CAC do período, (Coluna T), com CC "Publicidade" e Canal Despesa "MARKETING".
  * No total soma-se todas as despesas classificadas como "CAC" e CC Publicidade, mas com o canal de despesa Marketing em **[BD Despesas Realizadas](https://docs.google.com/spreadsheets/d/19tgMUL9El9tO-4D2lrBSzifNXzMrzDiWxErZcDJNHGo/edit#gid=2027505002&range=1:13525).**
  * Aqui trata-se de demais despesas de Marketing não relacionadas a pessoas (RH).

  \
  \
* **S.I.G=** Total de despesas CAC do período, (Coluna T), com CC "S.I.G".
  * No total soma-se todas as despesas classificadas como "CAC" e CC S.I.G em **[BD Despesas Realizadas](https://docs.google.com/spreadsheets/d/19tgMUL9El9tO-4D2lrBSzifNXzMrzDiWxErZcDJNHGo/edit#gid=2027505002&range=1:13525).**

  ⚠️

  Para distribuí-las nos canais, basta considerar a despesa classificada para aquele canal, mais "COMERCIAL", "PV" e "IMPLANTAÇÃO", conforme regra de rateio explicada anteriormente em "TOTAL".

  \
  \
* **Taxa de Implantação isenta=** Valor total de contratos do período, assinados sem taxa de implantação.
  * A não cobrança desta taxa gera um aumento de despesas para a Seazone, este indicador informa qual o valor desta despesa. Multiplicando o valor da taxa de implantação \* a quantidade de contratos assinados sem taxa de implantação.

  ⚠️

  Cada novo contrato de imóvel fechado, considera-se cobrar uma taxa de R$ 560,00 para cobrir custos de implantação do imóvel, despesas geradas antes de começar a receber receita por eles.

  \
  \
* **Outros=** Total de despesas CAC não relacionadas nas despesas anteriores.

  \
* **CAC Proprietário =** (Total de despesas CAC - Rateio IMPLANTAÇÃO) / Proprietários Contratos Assinados
  * O cálculo deste indicador por canal, necessita dividir entre eles a despesa Implantação. Para isso o rateio é feito conforme o percentual que o canal correspondente ao total de "Ativações de Imóveis" do período.
  * A despesa IMPLANTAÇÃO aqui é desconsiderada pois não é, necessariamente um custo de aquisição de clientes, mas a "**Taxa de Implantação isenta**" sim, é um custo de aquisição de clientes.

  \
* **CAC Contrato =** (Total de despesas CAC - Rateio IMPLANTAÇÃO) / Contratos Assinados
  * O cálculo deste indicador por canal, necessita dividir entre eles a despesa Implantação. Para isso o rateio é feito conforme o percentual que o canal correspondente ao total de "Ativações de Imóveis" do período.
  * A despesa IMPLANTAÇÃO aqui é desconsiderada pois não é, necessariamente um custo de aquisição de clientes, mas a "**Taxa de Implantação isenta**" sim, é um custo de aquisição de clientes.

  📌

  O número de Contratos Assinados deve ser maior que o Proprietários Contratos Assinados, pois alguns proprietários possuem mais de 1 imóvel sob nossa gestão.

  \
* **CAC Implantação =** TOTAL / Ativações de Imóveis
  * **Esse indicador mostra quanto tivemos de despesas naquele período pra ativação de cada um dos imóveis. A ativação não ocorre necessariamente no período que é ativado, então está correto isso?**

  \