<!-- title: Sytem Price | url: https://outline.seazone.com.br/doc/sytem-price-2RzK2WsZDk | area: Tecnologia -->

# Sytem Price

# 1. Plano de Ação

**PM Responsável:** Lucas Abel 

**Objetivo Principal do Plano de Ação:** Concluir a fase de Product Discovery, gerando os artefatos necessários (conforme definidos no documento de discovery) para permitir que o Time de Dados inicie o desenvolvimento da primeira fase de melhorias no System Price (foco em Regiões Não Sazonais).

 **Prazo Estimado para Conclusão do Discovery (PM):** Finalizar até final do trimestre(31-06-2025)


---

## Fases e Atividades Principais:

### Imersão, Mapeamento e Entendimento Inicial


1. **ATIVIDADE: Mapeamento Detalhado das Regras de Negócio Atuais do System Price**
   * **Descrição:** Revisar a documentação existente (`Sazonalidade.csv`, `Feriados.csv`, `regras_agc.csv`), analisar o código Lambda fornecido para entender o fluxo de dados, a lógica de aplicação das regras e os cálculos efetuados.
   * **Tarefas Específicas:**
     - [x] Consolidar a análise dos arquivos CSV em um resumo de regras de configuração.
     - [x] Documentar o fluxo lógico de como as `regras_agc` são selecionadas (Sazonalidade -> Ocorrência -> Ocupação de Concorrentes -> Antecedência).
     - [x] Clarificar cada tipo de cálculo de percentil (`occ`, `avb`, `min`, `max`, `mix`).
     - [x] Entender como a "Razão do Preço Sugerido" e o "Check da Categoria" são construídos.
     - [x] Agendar sessão com 1-2 membros do Time de Dados para tirar dúvidas sobre o código Lambda e a lógica de processamento, se necessário.
   * **Entregável Parcial:** Versão preliminar do documento "Mapeamento das Regras de Negócio do System Price".
   * **Stakeholders a Envolver:** Time de Dados (para consultas técnicas).
2. **ATIVIDADE: Mapeamento do Comportamento e Dores do Time de RM (Regiões Não Sazonais)**
   * **Descrição:** Conduzir sessões de observação e entrevistas com os precificadores (Nicole, Elisangela) e o gerente (Fábio) para entender como eles precificam manualmente as regiões Não Sazonais, quais seus critérios, dores com o System Price atual e expectativas.
   * **Tarefas Específicas:**
     - [x] Preparar roteiro para as sessões (foco: processo atual, ferramentas usadas, como o System Price é (ou não) usado, pontos de divergência, o que consideram um "bom preço").
     - [x] Agendar e conduzir sessões de acompanhamento/entrevista com Nicole e Elisangela (mínimo 1 sessão cada).
     - [x] Agendar e conduzir entrevista de aprofundamento com Fábio (Gerente RM).
     - [x] Consolidar os achados em um "Relatório de Análise do Comportamento de Precificação do RM e Dores Identificadas (Regiões Não Sazonais)".
   * **Entregável Parcial:** Relatório de entrevistas e observações.
   * **Stakeholders a Envolver:** Fábio, Nicole, Elisangela (Time RM).

### Análise, Síntese e Definição da Estratégia de Melhoria


3. **ATIVIDADE: Análise Cruzada e Identificação de Gaps e Oportunidades**
   * **Descrição:** Comparar o mapeamento das regras atuais do System Price com o comportamento e as dores levantadas junto ao time de RM. Identificar os principais desalinhamentos, pontos de falha das regras atuais e oportunidades de melhoria.
   * **Tarefas Específicas:**
     - [x] Cruzar o "Mapeamento das Regras" com o "Relatório do RM".
     - [x] Listar explicitamente onde as regras atuais divergem da prática do RM ou não atendem às suas necessidades para regiões Não Sazonais.
     - [x] Começar a esboçar quais parâmetros da `regras_agc.csv` poderiam ser ajustados ou que novas lógicas simples poderiam ser testadas.
   * **Entregável Parcial:** Documento interno de "Análise de Gaps e Oportunidades Iniciais".
4. **ATIVIDADE: Definição da Lista Preliminar de Novas Features/Parâmetros**
   * **Descrição:** Com base na análise de gaps, no feedback do RM e em benchmarks (como o PriceLabs, se a análise inicial já estiver disponível), começar a listar potenciais novas features ou parâmetros que poderiam, no futuro, aprimorar o System Price para além dos ajustes simples.
   * **Tarefas Específicas:**
     - [x] Brainstorming (pode ser individual ou com um par do time de Dados/RM) de possíveis novas entradas/lógicas.
     - [x] Documentar cada ideia com uma breve justificativa e o problema que visa resolver.
     - [x] Priorizar inicialmente esta lista (MoSCoW ou similar) para focar no que seria mais impactante ou fácil de testar.
   * **Entregável Parcial:** Rascunho da "Lista Priorizada de Novas Features/Parâmetros".
5. **ATIVIDADE: Desenho do Plano de Teste A/B e Definição de KPIs (Regiões Não Sazonais)**
   * **Descrição:** Em colaboração com o RM (Fábio) e com suporte do Time de Dados (para viabilidade da coleta de dados), definir a estrutura do teste A/B para as regiões Não Sazonais e os KPIs para medir o sucesso.
   * **Tarefas Específicas:**
     - [ ] Workshop/Sessão com Fábio (RM) para:
       - [ ] Definir critérios para seleção de imóveis para Grupo de Teste (System Price Automático) e Grupo de Controle (Manual).
       - [ ] Discutir a estratégia de comparação com o PriceLabs.
       - [ ] Validar os KPIs de negócio e de usuário mais relevantes (ex: Diária Média, Taxa de Ocupação, RevPAR, Tempo de Precificação, Satisfação do RM com as sugestões).
       - [ ] Definir KPIs de *processo* e *confiança* do RM.
       - [ ] Definir metas ou critérios de sucesso para os KPIs.
     - [ ] Validar com o Time de Dados a viabilidade de coletar os dados para os KPIs definidos e de implementar a segmentação para o A/B.
     - [x] Documentar formalmente o "Plano de Teste A/B e KPIs".
   * **Entregável Parcial:** Documento "Plano de Teste A/B e KPIs para Regiões Não Sazonais".
   * **Stakeholders a Envolver:** Fábio (RM), Representante do Time de Dados.

### Consolidação, Documentação Final e Preparação para Handover


6. **ATIVIDADE: Finalização dos Artefatos do Discovery**
   * **Descrição:** Consolidar todos os entregáveis parciais nos documentos finais do discovery, garantindo clareza, completude e alinhamento com os stakeholders.
   * **Tarefas Específicas:**
     - [x] Revisar e finalizar o "Mapeamento das Regras de Negócio do System Price".
     - [x] Revisar e finalizar o "Relatório de Análise do Comportamento de Precificação do RM (Não Sazonais)".
     - [x] Revisar e finalizar a "Lista Priorizada de Novas Features/Parâmetros".
     - [x] Revisar e finalizar o "Plano de Teste A/B e KPIs para Regiões Não Sazonais".
     - [ ] Validar os documentos finais com Fábio (RM) e um representante do Time de Dados.
   * **Entregáveis Finais (Inputs para Time de Dados):** Todos os documentos acima finalizados.
7. **ATIVIDADE: Criação do Epic e User Stories para o Time de Dados (Fase 1 - Não Sazonais)**
   * **Descrição:** Traduzir os achados e definições do discovery em um Epic claro e acionável para o Time de Dados, detalhando o trabalho necessário para a primeira fase de implementação e testes em regiões Não Sazonais.
   * **Tarefas Específicas:**
     - [ ] Escrever a descrição do Epic, objetivos, e escopo da Fase 1.
     - [ ] Quebrar o trabalho em User Stories ou Tasks técnicas (em alto nível, o Time de Dados pode detalhar mais).
     - [ ] Definir os Critérios de Aceite (DoD) para o Epic e para as principais User Stories.
     - [ ] Referenciar os documentos de discovery no Epic para consulta.
   * **Entregável Final:** Epic criado no Jira (ou ferramenta de gestão) com User Stories/Tasks e DoD.
   * **Stakeholders a Envolver:** Revisão com Tech Lead/Representante do Time de Dados.
8. **ATIVIDADE: Preparação e Condução da Reunião de Handover/Kick-off com Time de Dados**
   * **Descrição:** Apresentar os resultados do discovery, o Epic e os próximos passos para o Time de Dados.
   * **Tarefas Específicas:**
     - [ ] Preparar apresentação resumida dos achados e do plano.
     - [ ] Agendar e conduzir a reunião de kick-off com o Time de Dados e, se pertinente, com Fábio (RM).
     - [ ] Garantir o alinhamento e esclarecer dúvidas.
   * **Entregável:** Reunião realizada e alinhamento obtido.


---

## Monitoramento e Comunicação:

- [ ] Atualizar o documento "Product Discovery: Melhoria da Confiança e Precisão do System Price" semanalmente.
- [ ] Manter comunicação regular com Fábio (RM) sobre o progresso.
- [ ] Agendar checkpoints com o Time de Dados conforme necessário.


---

# 2. Mapeamento Detalhado das Regras de Negócio

**Objetivo:** Descrever de forma clara e sequencial como o "System Price" é calculado, focando na lógica de negócio e nas decisões tomadas pelo sistema.

[Diagrama](https://miro.com/app/board/uXjVIu-lLZs=/)

## Parte 1: Configurações Fundamentais – Como o Sistema Entende o Contexto

Antes de sugerir um preço, o sistema precisa entender o contexto de cada data para cada imóvel. Isso é feito através de configurações pré-definidas:

1\.1. Definição de Sazonalidade - Aba: `Sazonalidade`:

* *O que é:* O sistema classifica os períodos do ano em diferentes tipos de "Sazonalidade" (ex: Alta Temporada, Média Temporada, Baixa Temporada).
* *Como é definido:*
  * Primeiro, os imóveis são agrupados por "Clima" (ex: "Região Fria", "Região Quente", "Não Sazonal", "Madego" – um tipo específico).
  * Para cada "Clima", são definidos os períodos de cada "Sazonalidade" com datas de início e fim.

    (Exemplo: Para o Clima "Região Fria", a "Alta Temporada" pode ser de 01/06 a 01/09).
  * Resultado: Para qualquer data, o sistema sabe qual "Sazonalidade" está vigente para um imóvel, baseado no seu "Clima".

    A baixo a figura mostra a aba `Sazonalidade` e como é definida na planilha `[S2.0] [PROD] Planilha de Setup`

 ![](/api/attachments.redirect?id=ae4bdcd1-2b12-4aab-8d74-2715e34fdb06 " =430x429")\n**1.2. Definição de Ocorrências (Feriados e Eventos) - Aba:** `Feriados`**:**

* O que é: O sistema identifica se uma data é um dia comum, um fim de semana, um feriado ou se há algum evento especial ocorrendo.
* Como é definido:
  * Uma lista de "Feriados" (ex: Natal, Carnaval) e/ou "Eventos" (ex: Oktoberfest, Ironman) é configurada.
  * Para cada Feriado/Evento, define-se:
    * A quais imóveis ou grupos de imóveis se aplica (ex: "Todos os imóveis", "Florianópolis, SC").
  * O nome do Feriado/Evento.
  * As datas de início e fim.
* Lógica de Prioridade (Hierarquia):

  
  1. Se uma data possui um Evento configurado para aquele imóvel/região, ela é classificada como "Evento".
  2. Se não há Evento, mas há um Feriado configurado, ela é classificada como "Feriado".
  3. Se não há Evento nem Feriado, a data é classificada como "Fim de Semana" (Sextas e Sábados) ou "Dia de Semana" (Domingo a Quinta).


* Resultado: Para qualquer data, o sistema sabe o tipo de "Ocorrência" (Dia de Semana, Fim de Semana, Feriado ou Evento específico).

  \
  A baixo a figura mostra a aba `Feriados`e como é definida na planilha `[S2.0] [PROD] Planilha de Setup`:

 ![](/api/attachments.redirect?id=1ae0c8f8-c860-409d-a009-0ec270eba19b " =1100x792")

## Parte 2: A Matriz de Decisão – Onde a Estratégia de Preço é Definida 

O coração do sistema é uma grande tabela de regras (Localizada na aba `RegrasAGC` da `[S2.0] [PROD] Planilha de Setup`) que diz ao sistema qual estratégia de preço dos concorrentes seguir. Esta tabela considera quatro dimensões principais:

2\.1. Dimensões da Regra:


1. Sazonalidade da Data - coluna:`Sazonalidade` (Conforme definido na Parte 1.1 – ex: "Baixa Temporada").
2. Ocorrência da Data - coluna: `Ocorrência`: (Conforme definido na Parte 1.2 – ex: "Dia de semana", "Feriado", ou "evento").
3. Nível de Ocupação dos Concorrentes - `Ocupação` : O sistema verifica, para a data em questão, qual a porcentagem de imóveis concorrentes que já estão ocupados. Com base nisso, classifica o cenário em:

   
   1. Baixa Ocupação de Concorrentes - `Low`: Poucos concorrentes ocupados (ex: <= 25%).
   2. Média Ocupação de Concorrentes - `Medium` : Um número moderado de concorrentes ocupados (ex: entre 25% e 75%).
   3. Alta Ocupação de Concorrentes `High`: Muitos concorrentes ocupados (ex: > 75%).


4. Antecedência da Reserva colunas E até T: Quantos dias faltam entre hoje e a data da estadia para a qual o preço está sendo definido (ex: 0-5 dias, 6-15 dias, ..., 91-360 dias).

   \
   A baixo a figura mostra a aba `RegrasAGCe` como é definida na planilha `[S2.0] [PROD] Planilha de Setup`:

 ![](/api/attachments.redirect?id=7c2a0957-7775-47ee-9b8b-835f3b05f048 " =1435x794")


2\.2. O que a Regra Define (A Estratégia):

* Para cada combinação possível dessas quatro dimensões, a tabela especifica duas coisas:
  * Percentil de Preço dos Concorrentes: Um número que indica qual "fatia" do mercado de concorrentes o sistema deve mirar (ex: P25 significa pegar o preço que está abaixo de 25% dos concorrentes e acima de 75%; P50 é a mediana; P75 é um preço mais alto).
  * Tipo de Concorrente para o Percentil: De qual grupo de concorrentes esse percentil de preço será extraído:
    * `occ`: Preços dos concorrentes que já estão Ocupados.
    * `avb`: Preços dos concorrentes que ainda estão Disponíveis (Available).
    * `min`: O menor preço entre o percentil dos Ocupados e o percentil dos Disponíveis.
    * `max`: O maior preço entre o percentil dos Ocupados e o percentil dos Disponíveis.
    * `mix`: Uma mistura dos preços dos concorrentes Ocupados e Disponíveis antes de calcular o percentil.

```none
 (Exemplo de uma linha de regra: Para "Baixa Temporada" (Sazonalidade), em um "Fim de Semana" (Ocorrência),
  quando a "Ocupação dos Concorrentes" está Alta, e a reserva é feita com "16-30 dias" de Antecedência, a regra 
  pode ser: seguir o Percentil 75 (P75) dos preços dos concorrentes Ocupados (`occ`)).
```


## Parte 3: O Cálculo do Preço Sugerido – Como o Sistema Chega a um Número

 Uma vez que o contexto da data (Sazonalidade, Ocorrência) e a situação atual (Ocupação dos Concorrentes, Antecedência) são conhecidos, o sistema executa os seguintes passos: 

3\.1. Coleta de Dados dos Concorrentes:

* Para a data em questão e o grupo de imóveis sendo precificado:
  * O sistema busca os preços atuais de todos os concorrentes relevantes.
  * Separa esses preços em duas listas: preços de concorrentes Ocupados e preços de concorrentes Disponíveis.
  * Calcula a taxa de ocupação geral dos concorrentes para determinar se o cenário é de Baixa, Média ou Alta ocupação (conforme Parte 2.1, item 3).

3\.2. Seleção da Regra Estratégica:

* Com base na Sazonalidade da data, Ocorrência, nível de Ocupação dos Concorrentes (recém calculado) e Antecedência, o sistema encontra a linha correspondente na Matriz de Decisão (Parte 2).
* A partir desta linha, ele obtém o Percentil de Preço a ser usado (ex: P50) e o Tipo de Concorrente (ex: occ).

3\.3. Cálculo dos Preços de Referência dos Concorrentes:

* Usando o Percentil de Preço definido pela regra:
  * Calcula o valor desse percentil na lista de preços dos concorrentes Ocupados.
  * Calcula o valor desse percentil na lista de preços dos concorrentes Disponíveis.
  * Calcula o valor desse percentil na lista combinada de preços de concorrentes Ocupados e Disponíveis (para o tipo mix).

3\.4. Aplicação do "Tipo" da Regra para Obter um Preço Base:

* Agora, usando o Tipo de Concorrente definido pela regra:
  * Se o tipo for occ, o preço base é o percentil dos Ocupados.
  * Se for avb, é o percentil dos Disponíveis.
  * Se for min, é o menor entre o percentil dos Ocupados e dos Disponíveis.
  * Se for max, é o maior entre o percentil dos Ocupados e dos Disponíveis.
  * Se for mix, é o percentil da lista combinada.
* Este é o suggested_price inicial para aquela data.

3\.5. Ajuste Final: O "System Price"

* O sistema verifica se dias consecutivos (ex: uma sexta e um sábado dentro do mesmo feriado) acabaram usando exatamente a mesma lógica de regra para chegar ao suggested_price inicial.
* Se sim, o "System Price" final para esses dias agrupados será a média dos suggested_price individuais calculados. Isso ajuda a suavizar pequenas variações e manter consistência para períodos curtos com a mesma justificativa de preço.
* Se não houver agrupamento (ou seja, cada dia tem uma lógica de regra diferente), o "System Price" é igual ao suggested_price inicial. Coluna: `System_price` na aba `Análise por Categoria` **e** `Análise por Imóvel ` na  `Planilha Análise Geral de Concorrentes`

  ![](/api/attachments.redirect?id=ced73ac5-35ed-44c1-a638-8b918b1033c1 " =638x781")

## Parte 4: Entendendo o Porquê – A Justificativa do Preço

Para cada "System Price" gerado, o sistema também fornece uma "Razão do Preço Sugerido". Esta razão é uma frase que resume os principais fatores que levaram àquela sugestão, incluindo:

* O tipo de Sazonalidade.
* A sigla da regra principal utilizada.
* O nome do Feriado ou Evento (se aplicável).
* A faixa de Antecedência e o número de dias.
* O nível de Ocupação dos Concorrentes (Baixa, Média, Alta).
* O Percentil de Preço e o Tipo de Concorrente que foram aplicados

Casos especiais para a razão:

* Se não houver nenhuma regra na Matriz de Decisão para a combinação de fatores: "Sem Regra".
* Se não foram encontrados concorrentes para aquela data/imóvel: "Sem Competidores".

  Coluna: `Reason` na aba `Análise por Categoria` **e** `Análise por Imóvel ` na  `Planilha Análise Geral de Concorrentes`

 ![](/api/attachments.redirect?id=dbc585a2-25b6-4fe0-a669-77d1ff35a631 " =1245x804")\n


# 3. Mapeamento do Comportamento e Dores do Time de RM (Foco em Regiões Não Sazonais)

**PM Responsável:** Lucas Abel\n**Data da Coleta dos Dados:** 21/05/2025( Responsável RM Elisângela Bento) e 15/05/2025( Responsável RM Nicole Escaler )           \n**Objetivo:** Entender o processo atual de precificação manual do time de Revenue Management (RM) para regiões não sazonais, identificar as ferramentas utilizadas, a percepção sobre o "System Price", as principais dores e as oportunidades de melhoria para a ferramenta.

## Processo Geral de Precificação Manual Observado (Regiões Não Sazonais)

* **Preparação e Contexto Inicial:**
  * As precificadoras geralmente copiam os últimos preços enviados ("last price") como base para os novos preços ("new price") na planilha AGC.
  * Definem uma frequência de revisão para cada grupo de imóveis (geralmente 2 vezes por semana).
* **Análise de Ocupação Interna (Seazone):**
  * Consulta intensiva à ferramenta de **BI (Calendário de Ocupação Seazone)** para:
    * Verificar a ocupação atual dos imóveis da Seazone dentro da mesma categoria/polígono.
    * Identificar gaps de disponibilidade.
    * Analisar os preços de reservas já efetivadas para o período em questão.
* **Análise de Mercado e Concorrentes:**
  * Consulta à **Planilha AGC (Análise Geral de Concorrentes)** para:
    * Avaliar os níveis de ocupação dos concorrentes.
    * Analisar os preços dos concorrentes (disponíveis vs. ocupados).
    * Verificar a sugestão do "System Price".4. Análise Cruzada e Identificação de Gaps e Oportunidades
  * **Consideração de Fatores Adicionais e Limitações:**
    * **Limitação por Preços Mínimos:**
      * As precificadoras estão cientes dos preços mínimos definidos pelos proprietários para cada imóvel/categoria.
      * O sistema Sirius (onde os preços da AGC são enviados) **automaticamente ignora/impede** que preços sejam efetivados abaixo do preço mínimo estabelecido.
      * **Observação/Dor do RM:** Em alguns cenários, especialmente para imóveis com baixo desempenho ou em períodos de baixa demanda, as precificadoras se veem limitadas, pois suas tentativas de reduzir os preços para estimular a ocupação esbarram no preço mínimo. Qualquer preço enviado abaixo do mínimo não surte efeito, tornando o ajuste inócuo. Esta é uma dor enfrentada pelo RM, mas cuja resolução depende da negociação com o proprietário, não de ajustes no sistema de cálculo de preço em si (que já respeitaria essa restrição se o System Price sugerisse algo abaixo, o que não parece ser o caso principal da dor aqui, mas sim a limitação da ação do RM).
    * **Desempenho Histórico (Ano Anterior):** Para imóveis com histórico, comparam:
      * Preços praticados no mesmo período do ano anterior (FDS vs. FDS, Dia de Semana vs. Dia de Semana, mesmo feriado).
      * Nível de ocupação que o imóvel/categoria tinha no mesmo período do ano anterior, considerando a antecedência.
    * **Eventos/Feriados:** Ajuste de preços para cima em datas com eventos ou feriados, verificando os preços dos concorrentes para essas datas.
    * **Características da Região/Demanda:**
      * Regiões Não Sazonais (Centro-Oeste, Porto Alegre) tendem a ter reservas de **última hora**.
      * Estratégia de definir preços **mais altos para datas futuras distantes** para capturar valor e, posteriormente, aplicar descontos agressivos para preencher gaps de última hora.
      * Baixa variação de preço entre dias de semana e fins de semana comuns (sem evento).
    * **Desempenho do Imóvel:**
      * Análise de notas do imóvel e comentários de hóspedes, especialmente para imóveis com baixo desempenho.
      * Abertura de chamados para impulsionamento ou revisão de anúncio/preço mínimo quando necessário.
    * **Definição e Aplicação do Preço:**
      * Ajuste manual dos preços na planilha AGC com base em toda a análise.
      * Para regiões de alta concorrência (ex: Centro-Oeste), pequenas variações de preço 10 a 15 Reais por expemplo, são consideras sifnificativas.
      * Uso de planilhas pessoais (ex: "RM meta" da Elisangela) para tracking e referência de preços definidos.\n

## Principais Dores e Frustrações Identificadas (Relacionadas ao System Price e ao Processo)

* **D1: Desalinhamento com Estratégias Temporais Específicas:** O "System Price" não captura bem a estratégia de "preço alto futuro / desconto última hora" usada em certas regiões.
* **D2: Falta de Visibilidade/Integração de Dados Históricos Relevantes na AGC:**
  * Dificuldade em acessar rapidamente o "preço vendido no ano passado" para comparação direta na AGC.
  * Ausência de uma visão clara da "ocupação no mesmo período do ano passado, na mesma antecedência".
* **D3: Dificuldade em Medir o Impacto Imediato das Ações de Precificação:**
  * Falta de uma forma fácil de ver o "pickup" (ganho/perda de ocupação) desde a última intervenção de preço, para avaliar a eficácia da mudança ou identificar cancelamentos.
* **D4: Percepção de um "System Price" Pouco Dinâmico/Adaptativo:**
  * Não parece se ajustar com base no desempenho recente da própria categoria Seazone.
  * Não considera explicitamente se o mercado de concorrentes como um todo está com faturamento/ocupação acima ou abaixo do ano anterior.
* **D5: Limitação da Ação do RM pelos Preços Mínimos Implacáveis:** A impossibilidade de efetivar preços abaixo do mínimo definido pelo proprietário (devido à regra do sistema Sirius) frustra as precificadoras em situações onde elas acreditam que um preço menor seria necessário para gerar ocupação, tornando seus ajustes ineficazes se já estiverem no limite. (Esta dor é mais sobre a restrição da política de preço mínimo do que sobre o cálculo do System Price em si, que também seria limitado por ele).
* **D6: Complexidade e Falta de Transparência do "System Price":** Dificuldade em entender *como* a sugestão é gerada, o que impacta a confiança.

# 4. Análise de Gaps, Oportunidades e Lista Preliminar de Novas Features/Parâmetros para o System Price

**PM Responsável:** Lucas Abel\n**Data:** 29-05-20255\n**Fontes de Input:**

* Mapeamento do Comportamento e Dores do Time de RM (Regiões Não Sazonais)
* TCC "Otimização de precificação dinâmica para aluguel de temporada" (André Warschauer de Crescenzo)
* Feedbacks do COO (Bruno Benetti)

**Objetivo:** Cruzar os aprendizados das diversas fontes para identificar as principais lacunas (gaps) no "System Price" atual e as oportunidades de melhoria, culminando em uma lista preliminar de novas features e parâmetros a serem considerados para desenvolvimento futuro.

## I. Análise Cruzada: Principais Gaps e Oportunidades Identificados

### **GAP 1: Desalinhamento com Estratégias Temporais Específicas do RM (Especialmente Longo Prazo e Última Hora)**

* **Observado (RM):** RM (especialmente Nicole para Centro-Oeste) define preços mais altos para datas futuras distantes e aplica descontos agressivos na última hora. O System Price atual, mesmo com faixas de antecedência, não parece replicar essa amplitude ou estratégia de forma consistente, tendendo a sugerir preços mais baixos para o futuro distante do que o RM gostaria.
* **Observado (COO):** Reforça a necessidade de tratamento diferenciado para Sazonalidade (Alta demanda = mais agressivo/alto, Baixa demanda = proativo/ajustar antes).
* **Insight (TCC):** Variável advance (antecedência) é a de maior impacto na probabilidade de ocupação; menor antecedência = maior probabilidade. Isso suporta a estratégia do RM de precificar diferente na última hora.
* **Oportunidade:**
  * Revisar profundamente os percentis e tipos de regra nas faixas de antecedência da RegrasAGC, permitindo maior flexibilidade para o RM configurar estratégias de "premium" para longo prazo e "desconto agressivo" para curto prazo, com variações regionais.
  * Considerar uma lógica mais explícita para modular a agressividade com base na demanda percebida (derivada da sazonalidade ou outros indicadores).

    \

### **GAP 2: Falta de Visibilidade e Integração de Dados Históricos Relevantes (Performance Própria e de Concorrentes)**

* **Observado (RM):** Precificadoras consultam ativamente dados de performance do ano anterior (preços vendidos, ocupação na mesma antecedência), mas essa informação não está facilmente integrada ou visível na AGC onde o System Price é apresentado. Querem ver o "preço vendido ano passado".
* **Observado (COO):** Sugere usar o preço histórico como balizador mínimo (vender acima do ano passado + inflação) e considerar a performance atual do mês do imóvel (subir se bem, baixar se mal).
* **Insight (TCC):** Não foca em preço histórico Seazone, mas a dificuldade em modelar preço x ocupação sugere que benchmarks históricos podem ser âncoras importantes.
* **Oportunidade:**
  * **Feature (Dados Históricos Seazone):** Integrar colunas na AGC (ou em um dashboard vinculado) mostrando:
    * Preço médio vendido para o mesmo imóvel/categoria no mesmo período/dia da semana do ano anterior.
    * Ocupação do imóvel/categoria no mesmo período do ano anterior, na mesma antecedência.
  * **Feature (Lógica de Preço Mínimo Dinâmico):** O System Price poderia ter uma regra opcional para não sugerir preços abaixo do \[Preço Ano Anterior + X% (Inflação)\], como um "piso dinâmico" além do preço mínimo do proprietário.
  * **Feature (Feedback de Performance Recente):** Incorporar um indicador da performance de faturamento do imóvel no mês corrente para modular a sugestão do System Price (mais complexo, mas alinhado com feedback do COO).

### **GAP 3: Dificuldade em Medir o Impacto Imediato das Ações de Precificação (Pickup)**

* **Observado (RM):** Elisangela mencionou a falta de uma forma fácil de ver o "pickup" (ganho/perda de ocupação) desde a última intervenção de preço.
* **Oportunidade:**
  * **Feature (Visualização de Pickup):** Embora possa ser mais uma feature da ferramenta de BI ou da própria AGC como um todo, ter um indicador de "Variação de Ocupação desde a Última Precificação" para o período/imóvel em análise seria muito valioso para o RM. Poderia ser um input visual para o RM, mesmo que não usado diretamente no cálculo do System Price.

    \

### **GAP 4: Percepção de um "System Price" Estático e Pouco Adaptativo a Condições Recentes (Além dos Concorrentes)**

* **Observado (RM):** O System Price parece reagir bem aos concorrentes, mas não a outros fatores dinâmicos como o desempenho recente da própria categoria Seazone ou mudanças mais amplas na demanda de mercado não capturadas apenas pela ocupação dos concorrentes.
* **Observado (COO):** Reforça a necessidade de considerar a performance atual do mês do imóvel.
* **Insight (TCC):** O modelo de ML tentou usar pandemic como uma variável. Embora não queiramos reviver dados da pandemia, a ideia de identificar e reagir a "condições de mercado atípicas" é válida.
* **Oportunidade:**
  * **Feature (Modulador por Performance de Categoria):** O System Price poderia ter um ajuste (pequeno multiplicador ou somador) baseado na performance recente (últimos 7/15 dias) da categoria Seazone em termos de ocupação ou RevPAR em comparação com um período anterior ou meta.
  * **Feature (Considerar Tendências de Mercado Mais Amplas):** Como sugerido pelo COO e RM, analisar tendências do Booking.com ou indicadores macro de demanda para uma região poderia, no futuro, informar um "índice de demanda de mercado" que module o System Price. (Mais complexo e para o futuro).

    \

### **GAP 5: Tratamento Diferenciado por Qualidade/Características do Imóvel (Strata, Imóvel Novo)**

* **Observado (COO):**
  * Imóveis TOPs podem ter dinâmica de venda diferente de SUP/JR.
  * Imóveis novos precisam de desconto inicial.
* **Insight (TCC):** O TCC focou em "apartamentos muito similares" para reduzir o impacto da escolha do apartamento. Isso indica que as características do imóvel importam.
* **Oportunidade:**
  * **Feature (Modulador por Strata):** Introduzir um parâmetro na RegrasAGC ou uma lógica no System Price que permita aplicar um multiplicador/ajuste diferente com base na Strata do imóvel (ex: TOPs podem seguir percentis mais altos ou ter menos descontos de última hora).
  * **Feature (Lógica para Imóveis Novos):** Implementar uma regra que aplique um desconto padrão (configurável) para imóveis com menos de X dias de ativação ou Y reservas, para ajudar no ranqueamento inicial.

    \

### **GAP 6: Complexidade da Sazonalidade e Potencial para Sazonalidade Intrasemanal**

* **Observado (RM):** Embora a sazonalidade (Alta, Média, Baixa) seja usada, a percepção é que o System Price poderia ser mais "inteligente" na forma como lida com a demanda (feedback COO).
* **Observado (COO):** Mencionou estudo sobre sazonalidade intrasemanal (ex: terças melhores que outras dias de semana em Goiânia).
* **Insight (TCC):** A variável month foi significativa. A variável weekend também.
* **Oportunidade:**
  * **Melhoria na RegrasAGC:** Permitir regras mais granulares dentro da Ocorrência para capturar dias específicos da semana que se comportam como "mini-picos" em certas regiões/sazonalidades, além do simples "Dia de Semana" vs. "Fim de Semana". Isso exigiria um input de configuração mais detalhado.

**Feature (Índice de Demanda):** No futuro, em vez de apenas "Alta/Média/Baixa" Sazonalidade, o sistema poderia trabalhar com um "índice de demanda" numérico para cada data (derivado de histórico, eventos, buscas, etc.), permitindo uma modulação mais fina do preço. (Complexo, para o futuro).


### **GAP 7: Falta de Transparência e Explicabilidade do System Price (Dor Contínua)**

* **Observado (RM):** Dificuldade em entender *como* a sugestão é gerada.
* **Oportunidade:**

Melhorar continuamente a "Razão do Preço Sugerido", tornando-a o mais clara e detalhada possível, talvez até com links para as regras ou dados específicos que mais influenciaram.\n

### **GAP 8: Complexidade e Falta de Feedback na Reparametrização e Manutenção do System Price pelo RM**

* **Observado (Preocupação do PM):** O atual sistema de parametrização (via RegrasAGC e outras abas) é complexo. Se as futuras reparametrizações ou a inclusão de novas features mantiverem essa complexidade sem ferramentas de apoio para o RM, há um alto risco de:
  * O RM não se sentir confiante para ajustar os parâmetros de forma autônoma.
  * Os parâmetros ficarem desatualizados.
  * O System Price perder relevância e cair em desuso, invalidando o esforço de melhoria.
* **Dor Implícita do RM (Futura):** "Não sei como ajustar esses parâmetros para minha realidade sem quebrar o sistema ou piorar os resultados", "Não entendo o impacto de mudar X para Y".
* **Oportunidade:**
  * Desenvolver mecanismos ou ferramentas que auxiliem o RM a:
    * Entender o impacto de mudanças nos parâmetros.
    * Receber indicações ou simulações de como os parâmetros poderiam ser otimizados.
    * Facilitar o processo de ajuste dos parâmetros de forma mais intuitiva.

## II. Lista Preliminar de Novas Features/Parâmetros para o System Price

Com base nos Gaps e Oportunidades, segue uma lista preliminar de potenciais novas features/parâmetros. A priorização e detalhamento técnico virão depois.


### **Features Relacionadas a Dados Históricos e Performance:**


1. **FH-01: Exibição de Preço Médio Vendido Ano Anterior (Seazone):**
   * *Descrição:* Mostrar na AGC/dashboard o preço médio que o mesmo imóvel (ou categoria similar) foi vendido no mesmo período/dia da semana do ano anterior.
   * *Gap Atendido:* GAP 2.
2. **FH-02: Exibição de Ocupação Ano Anterior (Seazone):**
   * *Descrição:* Mostrar na AGC/dashboard a ocupação que o imóvel/categoria tinha no mesmo período do ano anterior, na mesma antecedência.
   * *Gap Atendido:* GAP 2.
3. **FH-03: Lógica de Piso de Preço Baseado no Histórico (Opcional):**
   * *Descrição:* Permitir configurar o System Price para não sugerir valores abaixo de \[Preço Ano Anterior + X% Inflação\].
   * *Gap Atendido:* GAP 2 (Feedback COO).
4. **FH-04: Modulador por Performance Atual do Mês (Imóvel):**
   * *Descrição:* Ajustar a sugestão do System Price com base no faturamento/ocupação do imóvel no mês corrente em relação a uma meta ou histórico. (Requer definição clara de como medir "bem" vs "mal").
   * *Gap Atendido:* GAP 2, GAP 4 (Feedback COO).
5. **FH-05: Visualização de "Pickup" de Ocupação:**
   * *Descrição:* Mostrar a variação de ocupação desde a última vez que o RM precificou/enviou preços para aquele período/imóvel.
   * *Gap Atendido:* GAP 3.

### **Features Relacionadas à Estratégia e Dinâmica de Mercado:**


1. **FE-01: Parâmetros de Agressividade para Longo Prazo vs. Curto Prazo na RegrasAGC:**
   * *Descrição:* Tornar mais explícito na RegrasAGC como definir percentis/tipos para estratégias de "premium futuro" vs. "desconto última hora", possivelmente com mais faixas de antecedência ou opções de modulação.
   * *Gap Atendido:* GAP 1.
2. **FE-02: Modulador por Strata (Qualidade do Imóvel):**
   * *Descrição:* Permitir que a RegrasAGC ou o System Price aplique ajustes específicos (ex: percentis mais altos/baixos, ou um multiplicador) com base na classificação de qualidade do imóvel (TOP, SUP, JR).
   * *Gap Atendido:* GAP 5 (Feedback COO).
3. **FE-03: Lógica de Desconto para Imóveis Novos:**
   * *Descrição:* Aplicar um desconto padrão configurável (X% por Y dias/reservas) para imóveis recém-ativados.
   * *Gap Atendido:* GAP 5 (Feedback COO).
4. **FE-04: Configuração de Sazonalidade Intrasemanal:**
   * *Descrição:* Permitir na aba "Ocorrência" (ou similar) a definição de dias específicos da semana (ex: Terça-feira em Goiânia) com tratamento diferenciado, além de "Dia de Semana" / "Fim de Semana" genéricos, para certas regiões/climas.
   * *Gap Atendido:* GAP 6 (Feedback COO).

### **Features Relacionadas à Inteligência e Adaptação do Sistema (Mais Complexas/Futuras):**


1. **FI-01: Modulador por Performance Recente da Categoria (Seazone):**
   * *Descrição:* Ajustar a sugestão do System Price com base na performance (ocupação, faturamento) da categoria nos últimos 7/15 dias em relação a um período anterior ou meta.
   * *Gap Atendido:* GAP 4.
2. **FI-02: Integração de um "Índice de Demanda de Mercado Externo":**
   * *Descrição:* (Visão de futuro) Usar dados externos (buscas, tendências Booking.com, etc.) para criar um índice de demanda que module o System Price.
   * *Gap Atendido:* GAP 4.

### Features Relacionadas à **Gerenciabilidade, Simulação e Otimização de Parâmetros (Foco no RM)**


1. **FG-01: Simulador de Impacto de Parâmetros (Visão de Futuro):**
   * *Descrição:* Uma ferramenta (poderia ser uma aba na planilha com lógicas adicionais ou uma interface simples) onde o RM pudesse selecionar uma categoria/região, alterar um ou mais parâmetros da RegrasAGC (ou de novas features) e ver uma *simulação* de como isso impactaria as sugestões de preço do System Price para um conjunto de datas históricas ou futuras.
   * *Exemplo:* "Se eu mudar o percentil da antecedência X de P50 para P60 para a Baixa Temporada em Dias de Semana, como os preços sugeridos para as próximas 4 semanas mudariam?"
   * *Gap Atendido:* GAP 8.
2. **FG-02: Dashboard de Análise de Sensibilidade de Parâmetros (Visão de Futuro):**
   * *Descrição:* Um relatório ou dashboard que mostre, para uma dada região/categoria, quais parâmetros atuais do System Price têm o maior impacto nas sugestões de preço ou no desalinhamento com os preços praticados/objetivos de RM.
   * *Exemplo:* "Para a região Centro-Oeste, o parâmetro de 'Percentil para Alta Antecedência' é o que mais causa divergência entre o System Price e a estratégia do RM".
   * *Gap Atendido:* GAP 8.
3. **FG-03: Sistema de Alerta para Parâmetros Potencialmente Desatualizados/Mal Ajustados (Visão de Futuro):**
   * *Descrição:* O sistema poderia monitorar a performance do System Price (ex: quão próximo ele fica dos preços efetivamente locados ou das metas de RM) e, se detectar um desvio consistente para uma região/categoria, poderia sugerir que certos parâmetros relacionados podem precisar de revisão.
   * *Exemplo:* "O System Price para a categoria X tem consistentemente sugerido preços 15% abaixo do preço médio locado nos últimos 30 dias. Considere revisar os parâmetros de percentil para esta categoria."
   * *Gap Atendido:* GAP 8.
4. **FG-04: Assistente de Otimização de Parâmetros (Visão MUITO de Futuro / P&D):**
   * *Descrição:* Um sistema mais avançado que, com base em dados históricos e metas de RM (ex: maximizar RevPAR, atingir X% de ocupação), pudesse rodar simulações e *sugerir* conjuntos de parâmetros otimizados para uma determinada região/categoria. O RM ainda teria a decisão final de aplicar ou não.
   * *Gap Atendido:* GAP 8.
5. **FG-05: Documentação Interativa e Guias de Parametrização:**
   * *Descrição:* Além do mapeamento inicial, criar e manter uma documentação viva, talvez com exemplos práticos e "receitas" de como ajustar parâmetros para diferentes cenários ou objetivos de negócio. "Se você quer ser mais agressivo na última hora para a região Y, ajuste os parâmetros A e B desta forma...".
   * *Gap Atendido:* GAP 8, GAP 7.

### **Mitigando o Risco Imediatamente (mesmo sem as features FG-XX):**


1. **Documentação e Treinamento:** Na entrega da Fase 1 (System Price reparametrizado para Não Sazonais), a documentação (seu mapeamento + o "como e porquê" dos novos parâmetros) e um treinamento/workshop com o RM são cruciais.
2. **Processo de Revisão Conjunta:** Definir um processo, talvez trimestral, onde PM e RM se sentam para revisar a performance do System Price e os parâmetros das regiões já "ao vivo", mesmo que o ajuste ainda precise de algum apoio de Dados para simulações mais complexas.
3. **Foco em Simplicidade (onde possível):** Ao definir novas features, sempre se perguntar: "Quão fácil será para o RM entender e ajustar os parâmetros desta feature no futuro?".\n

# 5. Definição de KPIs

**PM Responsável:** Lucas Abel\n**Data:** 02-06-2025\n**Objetivo:** Definir os Indicadores Chave de Performance (KPIs) para medir tanto o desempenho técnico das sugestões do "System Price" quanto o impacto do "System Price" como produto para o time de Revenue Management (RM) e para os objetivos de negócio da Seazone.

## Parte 1: KPIs de Desempenho da Ferramenta "System Price"

**Objetivo Destes KPIs:** Avaliar a precisão, aderência e qualidade das sugestões de preço geradas pelo System Price. Ajudar a identificar onde o System Price está bem parametrizado e onde necessita de ajustes.


1. **KPI: Aderência ao Preço do Precificador (RM)**
   * **Métrica Principal:** MAPE (Mean Absolute Percentage Error) entre o System_Price e o Preco_Final_RM (preço efetivamente enviado pelo RM após sua análise).
   * **Granularidade:**
     * Geral (todas as precificações).
     * Por Região/Cluster de Mercado.
     * Por Sazonalidade (Média, Baixa, Alta, Não Sazonais).
     * Por Tipo de Ocorrência (Dia de Semana, FDS, Feriado, Evento específico).
     * Por Faixa de Antecedência.
     * Por Nível de Ocupação dos Concorrentes (Low, Medium, High - usado na RegrasAGC).
     * Por Strata do Imóvel (TOP, SUP, JR).
   * **Meta Exemplo:** Reduzir o MAPE Geral em X% após as melhorias. Para segmentos específicos (ex: Não Sazonais, Curta Antecedência), atingir MAPE < Y%.
   * **Como Ajuda:** Indica o quão próximo o System Price está das decisões do RM. Um MAPE alto em um segmento específico sinaliza um forte desalinhamento e necessidade de revisão dos parâmetros daquele segmento.\n
2. **KPI: Aderência ao Preço Efetivamente Locado (quando há locação)**
   * **Métrica Principal:** MAPE entre o System_Price (da data da reserva) e o Preco_Locado_Efetivo.
   * **Granularidade:** Similar ao KPI 1.
   * **Meta Exemplo:** Manter o MAPE em relação ao preço locado abaixo de Z% para imóveis onde o System Price foi a principal referência.
   * **Como Ajuda:** Mede a "acurácia" do System Price em relação ao que o mercado realmente pagou. Complementa o KPI 1, pois o RM pode errar.\n
3. **KPI: Taxa de "Ignorar" o System Price (Override Rate)**
   * **Métrica Principal:** Percentual de vezes que o Preco_Final_RM é significativamente diferente (ex: > ±10%) do System_Price sugerido.
   * **Granularidade:** Similar ao KPI 1.
   * **Meta Exemplo:** Reduzir a Taxa de Override em X% após as melhorias.
   * **Como Ajuda:** Mede diretamente a confiança e aceitação do RM nas sugestões. Uma alta taxa de override indica baixa confiança.

     \
4. **KPI: Cobertura de Regras do System Price**
   * **Métrica Principal:** Percentual de cenários de precificação (combinação de Sazonalidade, Ocorrência, Ocupação, Antecedência) para os quais existe uma regra definida na RegrasAGC e o System Price consegue gerar uma sugestão (não resulta em "Sem Regra").
   * **Meta Exemplo:** Manter cobertura > 70%.
   * **Como Ajuda:** Garante que o sistema é abrangente e não deixa o RM sem uma sugestão base.

     \
     \
5. **KPI: Performance Relativa ao PriceLabs (Benchmark)**

* **Métrica Principal:**
  * Diferença Percentual Média entre System_Price e sugestão do PriceLabs_Price para o mesmo imóvel/data.
  * Comparativo de performance (RevPAU, Ocupação) em grupos de imóveis onde um segue o System Price e outro (hipoteticamente) seguiria PriceLabs (mais complexo, talvez via simulação ou análise de imóveis que *usam* PriceLabs).
* **Granularidade:** Por Região/Strata.
* **Meta Exemplo:** System Price apresentar resultados de RevPAU X% melhores ou Y% mais próximos das sugestões do PriceLabs para segmentos chave, OU manter uma diferença estratégica justificada.
* **Como Ajuda:** Posiciona o System Price em relação a uma ferramenta de mercado reconhecida.

  \

## Parte 2: KPIs de Impacto do Produto "System Price" (Para o RM e para o Negócio)

**Objetivo Destes KPIs:** Medir como as melhorias no System Price estão contribuindo para os objetivos de negócio (OKRs) e melhorando a experiência/eficiência do time de RM. Requerem, em muitos casos, um baseline pré-melhoria e a capacidade de comparar grupos (ex: Teste A/B com System Price automático vs. Manual).


### **Dimensão: Eficiência Operacional do Time RM**



1. **KPI: Tempo Médio de Precificação por Grupo de Imóveis/Polígono**
   * **Métrica Principal:** Redução do tempo gasto pelo RM para precificar um conjunto de imóveis.
   * **Como Medir:** Cronometragem (antes e depois das melhorias) ou estimativa do RM. Difícil de automatizar.
   * **Meta Exemplo:** Reduzir o tempo de precificação em X% para regiões onde o System Price é mais utilizado.
   * **Como Ajuda:** Mede o ganho de produtividade do RM.

     \
2. **KPI: Nível de Confiança/Satisfação do RM com o System Price**
   * **Métrica Principal:** Pesquisa de satisfação qualitativa/quantitativa com o time de RM (ex: Escala Likert "Quão confiante você está nas sugestões do System Price para a região X?").
   * **Como Medir:** Survey periódico (ex: trimestral).
   * **Meta Exemplo:** Aumentar a nota média de confiança/satisfação em X pontos.
   * **Como Ajuda:** Mede diretamente a percepção do usuário e a adoção.

     \
3. **KPI: Adoção da Precificação Automática (Quando implementado)**
   * **Métrica Principal:** Percentual de imóveis/categorias/regiões elegíveis que estão utilizando o System Price em modo de precificação automática.
   * **Meta Exemplo (Visão de Futuro):** Atingir X% de adoção da precificação automática em regiões Não Sazonais validadas.
   * **Como Ajuda:** Mede o sucesso da transição para um modelo mais automatizado, que é um dos objetivos de longo prazo.


### **Dimensão: Performance de Receita e Ocupação (Impacto no Negócio)**


*Estes KPIs idealmente seriam medidos através de Testes A/B: Grupo com System Price (automático ou como forte guia) vs. Grupo de Controle (precificação manual tradicional).*



1. **RevPAU (Revenue Per Available Unit / Receita por Unidade Disponível)**
   * **Métrica Principal:** Receita Total Gerada no Período / Número Total de Diárias de Imóveis Efetivamente Disponíveis para Locação no Período.
   * **Granularidade:**
     * Geral (para o portfólio do teste).
     * **Por Tipologia/Categoria do Imóvel (Essencial para comparações justas):** Ex: RevPAU para Estúdios, RevPAU para Apartamentos de 2 quartos, etc.
     * Por Região.
     * Por Sazonalidade.
   * **Meta Exemplo:** Grupo de teste com System Price apresentar um RevPAU X% superior ao grupo de controle para as principais tipologias de imóveis.
   * **Como Ajuda:** KPI fundamental de rentabilidade de aluguel de temporada, combinando os efeitos da ocupação e da diária média em uma única métrica por unidade disponível.
2. **KPI: Taxa de Ocupação**
   * **Métrica Principal:** Comparação da Taxa de Ocupação entre o grupo de teste e o grupo de controle.
   * **Granularidade:** Por Região, Strata, Sazonalidade.
   * **Meta Exemplo:** Grupo de teste com System Price apresentar uma Taxa de Ocupação X p.p. (pontos percentuais) superior ou igual (se o objetivo for aumentar diária) ao grupo de controle.
   * **Como Ajuda:** Mede a capacidade de gerar demanda e preencher o inventário.
3. **KPI: Diária Média Efetiva (ADR - Average Daily Rate)**
   * **Métrica Principal:** Comparação da ADR entre o grupo de teste e o grupo de controle.
   * **Granularidade:** Por Região, Strata, Sazonalidade.
   * **Meta Exemplo:** Grupo de teste com System Price apresentar uma ADR X% superior ou igual (se o objetivo for aumentar ocupação) ao grupo de controle.
   * **Como Ajuda:** Mede o valor médio obtido por diária vendida.
4. **KPI: % de Alcance da Meta de Faturamento por Imóvel/Categoria**
   * **Métrica Principal:** Comparar o percentual de imóveis no grupo de teste que atingem/superam suas metas de faturamento vs. o grupo de controle.
   * **Meta Exemplo:** Aumentar em X% o número de imóveis que atingem a meta no grupo de teste.
   * **Como Ajuda:** Conecta diretamente com as metas financeiras da empresa.\n

### **Dimensão: Sustentabilidade e Manutenibilidade do Sistema pelo RM**



1. **KPI: Frequência de Reparametrização pelo RM (Visão de Futuro)**
   * **Métrica Principal:** Número de vezes que o RM proativamente revisa e ajusta os parâmetros do System Price (quando as ferramentas de suporte FG-XX estiverem disponíveis).
   * **Meta Exemplo:** RM realiza revisões/ajustes de parâmetros pelo menos uma vez por trimestre para as principais regiões.
   * **Como Ajuda:** Indica que o RM se sente capaz e engajado em manter o sistema otimizado.

     \
2. **KPI: Tempo para RM Entender e Aplicar um Novo Parâmetro/Feature (Visão de Futuro)**
   * **Métrica Principal:** Tempo médio desde o lançamento de uma nova feature de parametrização até o RM começar a utilizá-la efetivamente.
   * **Meta Exemplo:** Reduzir o tempo de adoção de novas features de parametrização para menos de Y semanas.
   * **Como Ajuda:** Mede a facilidade de uso e a clareza das novas funcionalidades de gestão de parâmetros.\n


# 6. Separação em fases de implementação

### **Fase 1: "Diagnóstico, Ferramentas de Suporte e Validação da Reparametrização" (Até 2025-Q3)**

* **Conteúdo:**

  
  1. **Análise de Erros e Parametrização:** Realizar a análise de dados profunda para entender onde o sistema atual falha e qual seu potencial.
  2. **Desenvolvimento de Ferramentas de Suporte:** Criar as primeiras ferramentas que ajudem a *visualizar* os problemas de parametrização e o impacto das regras (ex: Dashboards de MAPE Granular, talvez um protótipo de "Simulador de Impacto").
  3. **Reparametrização Colaborativa:** Usar as novas ferramentas para, junto com o RM, propor uma nova parametrização para as regiões Não Sazonais.
  4. **Teste A/B para Validação:** Implementar a nova parametrização em um grupo de teste (com automação) e comparar com um grupo de controle para provar o valor.
  5. **Acompanhamento da Evolução:** Monitorar os KPIs definidos.

### **Fase 2: "Expansão da Validação e Introdução de Novas Features Prioritárias" (Até 2025-Q4)**

* **Conteúdo:**

  
  1. **Inclusão de Novas Features:** Com base nos aprendizados da Fase 1, implementar as primeiras features da lista (FH, FES, etc.) que se mostrarem mais necessárias para atacar os problemas que a simples reparametrização não resolveu.
  2. **Aprimoramento das Ferramentas de Suporte:** Evoluir as ferramentas da Fase 1 para acomodar os novos parâmetros/features.
  3. **Expansão da Automação (Não Sazonais):** Se a Fase 1 for um sucesso, expandir a automação para mais imóveis dentro das regiões Não Sazonais.
  4. **Piloto em Regiões Sazonais:** Introduzir um pequeno grupo de teste em regiões Sazonais, já com a nova parametrização e as novas features, para começar a medir o desempenho em cenários mais complexos.

### **Fase 3: "Escalabilidade da Automação e Otimização para Sazonalidade" (Até 2026-Q1)**

* **Conteúdo:**

  
  1. **Validação dos Testes Sazonais:** Analisar os resultados do piloto da Fase 2.
  2. **Expansão da Automação (Sazonais):** Com base nos resultados, validar a possibilidade de expandir a automação para mais categorias/imóveis dentro das regiões Sazonais.
* **Minha Avaliação:** Também muito bom. É um plano de escala que depende da validação da fase anterior. Mostra um pensamento de roadmap de longo prazo, iterativo e baseado em dados.