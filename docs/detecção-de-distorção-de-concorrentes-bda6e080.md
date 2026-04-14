<!-- title: Detecção de Distorção de Concorrentes | url: https://outline.seazone.com.br/doc/deteccao-de-distorcao-de-concorrentes-QKIao5TS0D | area: Tecnologia -->

# Detecção de Distorção de Concorrentes

**Projeto:** Evolução do PIC (Plataforma de Inteligência de Concorrentes) 

**Responsável:** PM - Lucas ABel

**Stakeholders:** Time de Revenue Management (Fábio, Belle, Victor) 

## 1. Contexto e Problema

O time de Revenue Management (RM) enfrenta dificuldades em identificar a causa raiz para o baixo atingimento de metas em determinados clusters. Frequentemente, o problema não é o desempenho interno dos imóveis da Seazone, mas sim a presença de **concorrentes com dados distorcidos** na base de cálculo da Meta (P60).

Esses "vilões" inflacionam o percentil 60 da categoria, tornando as metas irreais. As ferramentas atuais (Quarentena e PIC Health) indicam que *algo* está errado (saúde baixa ou regras quebradas), mas não oferecem uma visão granular e visual para que o RM identifique rapidamente *qual* concorrente específico está causando a distorção e por quê (ex: preço em dia bloqueado, erro de inferência, faturamento absurdo).

**Dor Principal:** Falta de visibilidade para auditar a consistência da base de concorrentes de forma ágil, obrigando o RM a investigações manuais e demoradas.

## 2. Visão da Solução

A solução consiste em **enriquecer** o dashboard existente do [PIC](https://lookerstudio.google.com/u/0/reporting/e5b097cd-27e9-4f11-808a-64cbf0cb2f34/page/p_8jxgodj0wd) (Looker), transformando-o em uma ferramenta de diagnóstico completo. Não será criado um novo produto, mas sim uma expansão funcional.

A solução deve entregar:


1. **Alertas de Distorção no Nível Cluster:** Métricas para indicar quando a Meta está estatisticamente inflada.
2. **Transparência da Composição:** Visualizar se o cluster é formado por concorrentes nativos ou se depende fortemente de compensação (outros estratos/tipos).
3. **Aba de Auditoria Forense:** Uma nova área no dashboard para investigação profunda, com visualizações gráficas (Boxplot, Calendário) que permitam cruzar dados de faturamento, ocupação e inferência de disponibilidade.

## 3. Requisitos Funcionais

### 3.1. Nível Cluster: Tabela de Saúde (Aba Principal)

A tabela existente deve ser enriquecida com novas colunas para permitir a triagem rápida de categorias problemáticas.

**Novas Métricas de Distorção (Colunas):**

* `**Gap P60 / Mediana**`**:** Porcentagem de diferença entre a Meta (Percentil 60) e a Mediana do faturamento do cluster. (Valores altos indicam distorção).
* `**Z-Score da Meta**`**:** Distância estatística da Meta em relação ao desvio padrão do cluster.
* `**Distância da Média**`**:** Diferença percentual entre a Meta e a Média aritmética do cluster.

**Composição do Cluster (Novas Colunas):**

* `**% Compensação**`**:** Percentual de listing por compensação. 
* `**Detalhe da Compensação**`**:** Indicação visual ou textual dos tipos de compensação ativos naquele cluster (ex: "Compensado por Nº de Quartos", "Compensado por Strata", "Compensado por Tipo").

### 3.2. Nível Listing: Tabela de Detalhamento (Drill-down)

Ao clicar em um cluster específico, a tabela de imóveis deve expor dados operacionais para identificar os "vilões".

**Novos Campos/Colunas:**

* `**Faturamento Mês Atual**`**:** Valor total faturado pelo concorrente no mês corrente.
* `**Meta Atual**`**:** Valor da Meta (P60) definida para aquele cluster.
* `**Distância da Meta (%)**`**:** O quanto o faturamento do concorrente está acima ou abaixo da Meta.
* `**Ocupação**`**:** Taxa de ocupação no mês.
* `**Preço Médio (Imóvel)**`**:** Diária média praticada pelo concorrente.
* `**Preço Médio (Categoria)**`**:** Diária média da categoria inteira (para comparação rápida).
* `**Status Quarentena**`**:** Indicador se aquele listing está atualmente em algum processo de Quarentena (Ex: "Em Análise", "Liberado", "Inativo"). *Objetivo: Evitar retrabalho analisando um problema já conhecido.*

### 3.3. Nova Aba: "Auditoria de Cluster"

Nova aba dedicada para análise visual profunda de uma categoria selecionada por vez.

**Filtros e Seleção:**

* Filtro obrigatório para seleção de **Categoria**.
* Filtro opcional para listar apenas um subconjunto (ex: Top 20 outliers ou lista customizada).

**Visualização 1: Boxplot Comparativo**

* Gráfico de distribuição de faturamento do cluster selecionado.
* **Diferenciação Visual:** Deve ser possível distinguir visualmente no gráfico:
  * Concorrentes **Nativos** (ex: cor sólida).
  * Concorrentes **Compensados** (ex: cor vazada ou formato diferente).
* **Comparação com Adjacentes:** Capacidade de sobrepor ou adicionar ao gráfico dados de **Categorias Adjacentes** (ex: visualizar categoria "TOP-1Q" junto com "SUP-1Q" para validar se a matriz de preços faz sentido entre estratos vizinhos).

**Visualização 2: Calendário Forense**

* Exibição em formato de tabela/matriz: Linhas = Concorrentes, Colunas = Dias do Mês.
* **Conteúdo da Célula:**
  * Status do dia (Livre, Ocupado, Bloqueado).
  * Valor da Diária (Texto numérico).
* **Tratamento de Quarentena:** O sistema deve destacar (marcar/dimensionar) visualmente as listagens que já estão em Quarentena, para que o RM foque apenas nos novos problemas.
* **Objetivo da Visualização:** Permitir que o RM identifique erros de inferência (ex: dias marcados como ocupados/bloqueados com valores de diária inconsistentemente altos).

**Funcionalidade de Ação:**

* **Exportação de Dados:** Botão para exportar em CSV/Excel a lista de concorrentes exibida na tela (respeitando os filtros aplicados). *Objetivo: Permitir que o RM alimente planilhas externas ou dê input para regras.*

## 4. Requisitos Não-Funcionais

* **Performance:** As novas métricas e visualizações não devem degradar a performance de carregamento do dashboard existente.
* **Usabilidade:** A interface deve seguir os padrões visuais já adotados no PIC para garantir curva de aprendizado zero.
* **Atualização de Dados:** Os dados de faturamento e ocupação devem refletir o mês corrente em tempo quase real (conforme a disponibilidade no BigQuery).

## 5. Critérios de Sucesso

* **Redução de Tempo:** Diminuição significativa no tempo que o RM gasta para encontrar o "vilão" responsável por uma meta inflada.
* **Adoção:** Utilização ativa da aba "Auditoria de Cluster" nas revisões quinzenais de metas.
* **Qualidade da Base:** Aumento na identificação e correção de concorrentes com dados distorcidos, refletindo em metas mais realistas nos meses subsequentes.

## 6. O que está Fora do Escopo (Out of Scope)

* Correção automática de dados (o sistema apenas alerta e exibe dados; a ação de inativar/alterar regras continua sendo manual).
* Análise histórica profunda (foco principal é o diagnóstico do mês atual para correção imediata).
* Alteração drástica no layout ou arquitetura do PIC principal (apenas adição de colunas e uma nova aba).