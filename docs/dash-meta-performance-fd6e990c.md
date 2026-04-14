<!-- title: Dash Meta Performance | url: https://outline.seazone.com.br/doc/dash-meta-performance-2EjslskDxb | area: Tecnologia -->

# Dash Meta Performance

Atualizado em: 02-12-2025

## **1. Visão Geral**

O **Dash Meta Performance** é uma ferramenta de Business Intelligence (BI) desenvolvida para monitorar, analisar e otimizar o desempenho de faturamento de um portfólio de imóveis. Seu objetivo é permitir que gestores e equipes operacionais tomem decisões rápidas e baseadas em dados, identificando pontos de atenção, oportunidades de melhoria e o impacto de ações ao longo do tempo.

## **2. Estrutura e Pipeline de Dados**

O dashboard é alimentado por um pipeline de dados rodado de forma manual e local, dividido em três etapas principais:


1. **Extração de Dados (**`**1_import_data.py**`**):**
   * **Fontes:** Coleta dados brutos de múltiplas fontes:
     * **Google BigQuery:** Dados de performance (faturamento, metas, concorrência) e de preços/disponibilidade.
     * **AWS Athena:** Dados de Preço Mínimo (`**dias_pmin**`) e status de precificação (`**has_system_price**`).
   * **Processo:** Executa queries SQL para extrair os dados do dia ou de um período específico.
   * **Saída:** Gera arquivos CSV com timestamp no nome (ex: `**meta_analysis_price_2025-10-17.csv**`) e os salva na pasta `**data/raw**`. Isso cria um **histórico de snapshots**.
2. **Preparação e Enriquecimento (**`**2_data_prepar.py**`**):**
   * **Processo:** Lê os arquivos brutos, consolida as fontes, limpa os dados e calcula métricas derivadas complexas.
   * **Saída:** Cria dois arquivos enriquecidos na pasta `**data/processed**`:
     * `**meta_analysis_final_enriched_YYYY-MM-DD.csv**`: Contém a visão geral de todos os imóveis com suas métricas.
     * `**berlinda_prepared_YYYY-MM-DD.csv**`: Contém uma análise focada e tática apenas para os imóveis no grupo "berlinda".
3. **Visualização e Interatividade (**`**streamlit_app.py**`**):**
   * **Processo:** É a aplicação web (desenvolvida em Streamlit) que serve os dados preparados.
   * **Funcionalidades:** Permite ao usuário selecionar snapshots históricos, aplicar filtros dinâmicos e explorar os dados através de gráficos e tabelas interativos.

## **3. Regras de Negócio e Métricas-Chave**

O dashboard se baseia em um conjunto de regras de negócio para classificar e medir o desempenho.

* **Atingimento de Meta:** Métrica fundamental que compara o faturamento atual com a meta do mês.
  * **Fórmula:** `**faturamento_mes / meta**`
* **Grupo de Criticidade:** Classificação dos imóveis com base no seu atingimento de meta.
  * `**crítico**`: `**atingimento <= 50%**`
  * `**atenção**`: `**50% < atingimento <= 80%**`
  * `**berlinda**`: `**80% < atingimento <= 110%**` (Grupo principal de foco para ação).
  * `**ok**`: `**110% < atingimento <= 200%**`
  * `**meta_subestimada**`: `**atingimento > 200%**`
* **Métricas de Impacto Financeiro:**
  * **Faturamento Perdido por Bloqueio:** Estimativa do que deixou de ser faturado devido a dias bloqueados.
  * **Falta para a Meta:** Valor restante para atingir a meta do mês.
* **Análise da Berlinda (Foco Tático):**
  * **Status Operacional:** Classifica os imóveis da "berlinda" com base na viabilidade de atingir a meta.
  * **Score de Prioridade:** Algoritmo que calcula a urgência de ação para cada imóvel. A lógica é separada para:
    * **Abaixo da Meta:** Prioriza quem precisa de menos esforço para bater a meta.
    * **Acima da Meta:** Prioriza quem tem maior risco de cair da meta.
* **Identificação de Preços Mínimos (Pmin):**
  * **Dias em Pmin (**`**dias_pmin**`**):** Número de dias no mês em que o imóvel foi vendido pelo preço mínimo.
  * **Status de System Price (**`**has_system_price**`**):** Flag booleano que indica se o imóvel possui um preço gerado pelo sistema de precificação.
  * **Filtro de Carteira:** Imóveis com `**has_system_price = True**` têm sua coluna `**carteira**` sufixada com `**_sys-price**` para permitir filtragem.

## **4. Funcionalidades Chave do Dashboard**

* **Seleção de Dados Históricos:** Permite comparar snapshots de diferentes dias e analisar a evolução das métricas.
* **Filtros Dinâmicos:** Filtros interativos por Estado, Carteira, Categoria, Cidade, etc., que se aplicam a todas as visualizações.
* **Aba "Visão Geral":**
  * KPIs de performance geral.
  * Gráfico de barras da distribuição dos grupos de criticidade.
  * **Heatmap de performance por estado/cidade.**
  * **Gráfico de impacto de bloqueio e falta de meta por cidade** (exibido ao filtrar um estado).
  * **Scatter plot** para análise multidimensional com múltiplas opções de eixo e cor.
  * **Gráfico de evolução temporal** para mostrar a tendência dos grupos de criticidade.
* **Aba "Berlinda Detalhada":**
  * Tabela operacional com colunas de status, prioridade, score e métricas de viabilidade.
  * Gráficos e filtros específicos para a análise tática deste grupo.

## **5. Stack de Tecnologias**

* **Linguagem Principal:** Python
* **Manipulação de Dados:** Pandas, NumPy
* **Aplicação Web:** Streamlit
* **Visualização de Dados:** Plotly Express
* **Bancos de Dados:** Google BigQuery, AWS Athena
* **Controle de Versão:** Git