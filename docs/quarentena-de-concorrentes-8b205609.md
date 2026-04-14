<!-- title: Quarentena de Concorrentes | url: https://outline.seazone.com.br/doc/quarentena-de-concorrentes-USJcD9h6mr | area: Tecnologia -->

# Quarentena de Concorrentes

**Versão:** 1.0

**Data:** 23 de Outubro de 2025

**Autor:** Lucas Abel (PM de Dados) 

**Stakeholders:** Time de RM

### **1. Resumo Executivo**

Este projeto visa resolver a instabilidade crônica da métrica de Meta, causada por ajustes manuais e ad-hoc na lista de concorrentes pelo time de RM. A solução proposta é um sistema automatizado em 3 camadas: **Bloqueio** de erros grosseiros de dados, **Normalização** de desempenhos anômalos e **Quarentena** de casos complexos para análise manual. O objetivo é restaurar a confiança nos dados, reduzir o trabalho operacional e garantir a estabilidade das análises de performance.

### **2. O Problema**

O time de RM, na tentativa de "otimizar" a meta, realiza alterações manuais (ativação/desativação) de concorrentes durante o mês, classificando-os como "outliers". Essa prática é equivalente a "mudar as regras do jogo no meio da partida", resultando em:

* **Instabilidade da Meta:** A meta pode oscilar drasticamente (ex: -3% em um dia) sem que o desempenho real dos imóveis tenha mudado.
* **Perda de Confiança:** A equipe desconfia dos números, gerando investigações desnecessárias e horas de trabalho desperdiçadas pelo time de Dados.
* **Processo Manual e Arbitrário:** A decisão de quem é um "outlier" é subjetiva e não segue um processo padronizado ou auditável.

### **3. Objetivos**

* **Objetivo Principal:** Estabilizar o cálculo da Meta, eliminando as alterações manuais de concorrentes durante o mês.
* **Objetivos Secundários:**
  * Automatizar a identificação e o tratamento de dados de concorrentes anômalos.
  * Melhorar a qualidade geral da base de dados de concorrentes.
  * Reduzir o tempo gasto pelo time de Dados na investigação de "problemas nos dados".
  * Criar um processo transparente e auditável para a gestão de concorrentes.

### **4. Escopo**

**Dentro do Escopo:**

* Implementação de regras automatizadas para identificar e tratar dados anômalos.
* Criação de uma tabela de "Quarentena" para isolar concorrentes com problemas.
* Alteração da tabela `**Daily Revenue Competitors**` para aplicar as regras.
* Remoção do acesso do time de RM para ativar/desativar concorrentes manualmente.
* Impacto nos cálculos de Meta e nos dashboards de performance.

**Fora do Escopo:**

* Alteração na lógica core da ferramenta de precificação (AGC), exceto para bloquear dados ruins.
* Recategorização automática de imóveis.
* Desenvolvimento de modelos complexos de Machine Learning para esta primeira fase.

### **5. Proposta de Solução (Visão Geral)**

A solução será implementada em camadas, tratando os problemas de acordo com sua criticidade e complexidade.

* **Camada 1: Bloqueio Imediato de Erros Grosseiros:** Regras agressivas para identificar e descartar dados que são claramente erros de captura ou manipulação.
* **Camada 2: Normalização de Desempenho:** Regras para corrigir o impacto de concorrentes que distorcem a média, mas sem necessariamente terem dados "errados". *(A ser detalhado na Fase 2)*.
* **Camada 3: Quarentena para Análise Manual:** Isolamento de casos complexos que exigem avaliação humana para decidir se devem ou não participar da meta.


### **6. Fase 1: Detalhamento das Regras Iniciais (Bloqueio e Quarentena)**

Esta fase foca em implementar as regras mais críticas para conter os erros mais grosseiros e isolar os casos mais complexos.

#### **Regra A: Imóveis com Alta Ocupação e Sem Interação**

* **Descrição:** Identifica imóveis com padrão de ocupação suspeito, sem o feedback de hóspedes para validar as estadias.
* **Lógica / Gatilho:**

  
  1. 
     1. Se `**idade_do_imóvel > 6 meses**`:
        * `**ocupação_intrames > 1.3 \* média_ocupação_categoria_intrames**` E `**total_noites_ocupadas_no_mes > 10**` E `**data_último_review > 6 meses atrás**`.
     2. Se `**idade_do_imóvel <= 6 meses**`:
        * `**ocupação_intrames > 1.5 \* média_ocupação_categoria_intrames**` E `**total_noites_ocupadas_no_mes > 10**` E `**total_de_reviews = 0**`.
* **Ação:** Bloquear toda a ocupação do imóvel e movê-lo para a tabela de Quarentena.
* **Tag na Quarentena:** `**'6m-ocup'**`

#### **Regra B: Diárias Ocupadas com Faturamento Muito Acima**

* **Descrição:** Identifica reservas pontuais com preços absurdamente altos, provavelmente erros de dados.
* **Lógica / Gatilho:**
  * Para cada dia ocupado, se `**diária_ocupada > 3 \* mediana_móvel_diária_ofertada_proximos_30d**` E `**diária_ocupada > 1.3 \* média_diária_categoria**`. \nOBS:. desconsiderar datas de eventos. 
* **Ação:**

  
  1. Bloquear apenas a ocupação do dia específico que atende à condição.
  2. Se o imóvel tiver **5 ou mais dias** bloqueados por esta regra no mesmo mês, movê-lo para a Quarentena.
* **Tag no Log de Bloqueio:** `**'day-fat_acima'**`
* **Tag na Quarentena (se aplicável):** `**'multi-day-fat_acima'**`

#### **Regra C: Padrão de Ocupação e Preço Anômalos**

* **Descrição:** Identifica imóveis que, de forma consistente, apresentam um desempenho muito superior à sua categoria, distorcendo a meta. São os casos que o RM chamava de "outliers".
* **Lógica / Gatilho:**
  * Se `**ocupação_imóvel > 1.3 \* média_ocupação_categoria**` E `**quantidade_booked_on_distintos > 2**` E `**preço_medio_ocupado > P60_preço_ocupado_categoria**` E `**total_noites_ocupadas_no_mes > 10**` 
* **Ação:** 
  * **Identificar o Ponto de Virada:** Encontrar a data da reserva mais recente (`**booked_on**`) que contribuiu para o disparo da métrica.
  * **Bloquear Imediatamente:**
    * Bloquear a ocupação a partir da data identificada no passo 1.
    * Bloquear **todos os dias disponíveis** no restante do calendário do mês vigente.
  * **Mover para Quarentena:** Mover o imóvel para a tabela de Quarentena.
* **Tag na Quarentena:** `**'ocup_alta'**`


### **7. Fase 2: Construção e Governança do Sistema de Quarentena**

\n**1. Visão Geral**

A Fase 2 foca na construção do sistema de governança que dará suporte às regras definidas na Fase 1. Este sistema, chamado "Quarentena", é uma tabela central no BigQuery (BQ) que isola concorrentes anômalos, acompanhada por um dashboard no BI para visualização e um processo controlado para tomada de decisões. O objetivo é automatizar a gestão de anomalias, fornecer transparência total e estabelecer um fluxo de trabalho claro e seguro, eliminando a interferência manual na meta. OBS:. Incluir no BI da PIC(<https://lookerstudio.google.com/u/0/reporting/e5b097cd-27e9-4f11-808a-64cbf0cb2f34/page/p_8jxgodj0wd>)


#### **2. Arquitetura e Componentes**


1. **Tabela de Quarentena (BigQuery):**
   * **Nome Sugerido:** `**data_lake.concorrentes_quarentena**`
   * **Função:** Ser a fonte da verdade para todos os imóveis em quarentena, armazenando o histórico completo de movimentações e decisões.
2. **Dashboard de Governança (BI - PIC):**
   * **Função:** Visualizar a lista de imóveis em quarentena, filtrar por motivo, mês de inclusão, status atual, e acompanhar o histórico de cada imóvel.
3. **Planilha de Governança (Google Sheets):**
   * **Função:** Ser a interface de usuário para as decisões manuais. O PM de Dados ou responsável irá atualizar esta planilha com o veredito final sobre cada imóvel.

OBS:. Permissão de edição apenas para time data, RM comentador. 


#### **3. Fluxo Operacional e Cronograma Mensal**

O processo será executado de forma automatizada e padronizada todos os meses:

* **(Contínuo)** As regras da Fase 1 são executadas. Quando um imóvel atende a um critério, ele é inserido automaticamente na tabela de quarentena com o status `**EM_QUARENTENA**`.
* **(Dia 01 do Mês)** Um job automatizado envia uma notificação para um canal do Slack (ex: `**#data-alerts**`) com a lista dos novos imóveis que entraram na quarentena no mês anterior, incluindo um link direto para o dashboard do BI.
* **(Entre Dia 01 e 05)** A equipe de Dados/PM analisa a lista no dashboard e na planilha de governança.
* **(Até as 18h do Dia 05)** O responsável atualiza a planilha de governança com a decisão final para cada imóvel que está em `**EM_QUARENTENA**`.
* **(Dia 06)** Um job automatizado de "processamento de decisões" é executado:

  
  1. Lê a planilha de governança.
  2. Atualiza a tabela de quarentena no BQ com o status final e a data da decisão.
  3. Aplica as decisões de `**INATIVAR**` na tabela principal de concorrentes (`**Daily Revenue Competitors**`), definindo `**participante_meta: NÃO**` para o mês vigente.
* **(Após Dia 06)** A lista de concorrentes para a meta do mês fica "travada" e não sofrerá mais alterações.


#### **4. Estrutura da Tabela de Quarentena (Schema)**

| **Coluna** | **Tipo** | **Descrição** |
|----|----|----|
| `**listing_id**` | STRING | ID único do imóvel. |
| `**data_inclusao_quarentena**` | DATE | Data em que o imóvel entrou na quarentena. |
| `**mes_referencia**` | STRING | Mês de referência que a quarentena impacta (Formato 'YYYY-MM'). |
| `**motivo_quarentena**` | STRING | Regra que moveu o imóvel para quarentena ('6m-ocup', 'ocup_alta', 'IQR', 'MANUAL'). |
| `**status_atual**` | STRING | Status atual do imóvel ('EM_QUARENTENA', 'INATIVADO', 'LIBERADO'). |
| `**status_final**` | STRING | Decisão final do usuário (vindo da planilha). |
| `**data_decisao**` | DATE | Data em que a decisão foi tomada. |
| `**responsavel_decisao**` | STRING | E-mail ou nome do responsável pela decisão. |
| `**historico**` | JSON | Array de objetos para registrar múltiplas entradas/saídas da quarentena, garantindo que o histórico não se perca. |


#### **5. Regras de Movimentação para a Quarentena**

Um imóvel pode ser movido para a quarentena por:


1. **Regras Automáticas (Fase 1):** Ao ser acionado por uma das regras de bloqueio ('6m-ocup', 'ocup_alta').
2. **Regra Estatística de Segurança:** Um job mensal que identifica imóveis com `**faturamento_90d > (Q3 + 1.5 \* IQR)**` de sua categoria e os move para quarentena com o motivo `**'IQR'**`.
3. **Inclusão Manual:** O PM de Dados pode incluir manualmente um imóvel na planilha de governança, que será processada e movida para a tabela com o motivo `**'MANUAL'**`.

#### **6. Ações e Decisões do Usuário (via Planilha)**

O responsável terá três opções para cada imóvel em `**EM_QUARENTENA**`:


1. `**Manter em Quarentena**`**:** O imóvel continua isolado por mais um mês para reavaliação.
2. `**Inativar da Meta**`**:** O imóvel é oficialmente removido do cálculo da meta. **Esta é a ação principal.**
3. `**Liberar da Quarentena**`**:** Foi um falso positivo. O imóvel é liberado e pode voltar a participar da meta no mês seguinte.

### **Pontos de Validação e Riscos (Checklist Final)**

Vamos validar os pontos para garantir que não esquecemos nada:


1. **✅ Fonte da Verdade da Decisão:** A planilha é a interface. O job do dia 06 precisa ter **tratamento de erros robusto**. O que acontece se a planilha estiver mal formatada ou indisponível no dia 06? O job deve falhar de forma segura e notificar o time no Slack.
2. **✅ Histórico Preservado:** A coluna `**historico**` (JSON) é fundamental para não perdermos o rastro. Precisamos garantir que a lógica de inserção sempre adicione um novo objeto ao array, e não sobrescreva o existente.
3. **✅ Reavaliação Futura:** Um imóvel com status `**INATIVADO**` permanece na tabela. No futuro, um PM pode analisar esse histórico e decidir reativá-lo (`**LIBERAR**`), tornando-o elegível para a meta novamente. Isso está coberto.
4. **✅ Automação vs. Controle:** O fluxo está bem definido. A automação cuida da identificação e aplicação, e o humano cuida da decisão estratégica dentro de uma janela de tempo clara.
5. **🔍 Ponto Adicional de Validação - Conflito de Motivos:** E se um imóvel entra na quarentena por `**'ocup_alta'**` no dia 15, e no dia 20 ele também atinge o critério `**'6m-ocup'**`? A lógica deve ser: **não criar uma nova linha**. Apenas atualizar a linha existente, registrando o novo motivo no campo `**historico**`. O `**motivo_quarentena**` principal pode ser o primeiro que o levou para lá.
6. **🔍 Ponto Adicional de Validação - Performance da Tabela:** A tabela de quarentena crescerá indefinidamente. É importante **particioná-la por** `**mes_referencia**` **ou** `**data_inclusao_quarentena**` no BigQuery para garantir que as consultas permaneçam rápidas e os custos controlados.

<https://docs.google.com/spreadsheets/d/1hPqlSLkH_2h3nUrauRPkK3BKDakwR8LnPjISYHU5QNY/edit?gid=1343764927#gid=1343764927>