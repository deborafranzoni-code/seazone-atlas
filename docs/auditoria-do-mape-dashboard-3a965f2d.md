<!-- title: Auditoria do MAPE - DashBoard | url: https://outline.seazone.com.br/doc/auditoria-do-mape-dashboard-pdszjzTLjy | area: Tecnologia -->

# Auditoria do MAPE - DashBoard

**Versão:** 1.0\n**Data:** 19/12/2025\n**Origem:** Product / DataOps\n**Destino:** Data Solutions (Construção do Frontend/BI)\n**Objetivo:** Permitir a auditoria ágil das variações do MAPE de faturamento, identificando ofensores por granularidade, decomposição de erro e impacto por imóvel.


## 1. Fonte de Dados e Lógica de Backend

O backend roda uma Cloud Function diária que realiza um **"Upsert"** (atualiza dados existentes e insere novos) no BigQuery.

### ⚠️ Pontos de Atenção Críticos para o BI:


1. **Janela de Tempo:** A tabela mape_history contém dados de previsão até **60 dias no futuro**. Porém, as tabelas agregadas (ranked e granularity) são calculadas com base no **MAPE de 15 dias** (o KPI oficial).
   * *Diretriz:* Ao cruzar dados, filtrar mape_history para considerar apenas os próximos 15 dias se o objetivo for bater com os agregados.
2. **Erro Infinito (is_inf):**
   * Ocorre quando: Actual Revenue = 0 E Estimated Revenue > 0.
   * *Diretriz:* O BI deve calclular estes casos pra controlarmos seu crescimento. 


## 2. Estrutura das Tabelas (Detalhe Técnico)

### 2.1. mape_history (Granularidade Diária)

* **Função:** Base para gráficos de linha do tempo e drill-down.
* **Campo block_reason:** É um **ARRAY/LIST**. O BI precisará "explodir" ou fazer uma busca textual nessa lista para contar quantas vezes aparece "ML3", "NN" ou "Heuristic" para o gráfico de concordância.
* **Partição:** updated_at.

### 2.2. mape_granularity_analysis (Alertas)

* **Função:** Identificar ofensores macro (Estado, Strata, Quartos).
* **Lógica do Campo comparison_to_base_mape:**
  * Este valor é uma **Variação Percentual Relativa**, não absoluta.
  * *Exemplo:* Se o MAPE Global é **30%** e o valor nesta coluna é **0.5**:
    * Significa que o erro desta granularidade é 50% maior que a base.
    * Cálculo: 30% \* (1 + 0.5) = **45%** (e não 30.5%).
  * **Flag Crítica:** is_critical já vem TRUE quando essa variação passa de 0.5 (50%).

### 2.3. mape_ranked_properties (Top Ofensores)

* **Função:** Tabela de detalhe dos imóveis.
* **Lógica:** Já filtra e calcula o MAPE consolidado de **15 dias**.
* **Impact Score:** Ordenação do maior erro para o menor.

## 3. Especificação Visual do Dashboard (Wireframe)

### 3.1. Filtros Globais

* **Período A (Base) vs Período B (Comparação):**
  * O usuário seleciona datas passadas. O BI deve filtrar a mape_history baseada na coluna date.

### 3.2. Seção 1: KPIs Macro (Scorecards)

Comparativo A vs B.

| **KPI Visual** | **Regra de Cálculo** | **Tabela Fonte** | **Observação** |
|----|----|----|----|
| **MAPE Global** | Média do erro absoluto | mape_history | Excluir registros onde is_inf = TRUE da média. |
| **Variação Ocupação** | Real vs Previsto | mape_history | Coluna occupied |
| **Variação Bloqueios** | Real vs Previsto | mape_history | Coluna blocked |
| **Preço Médio** | Real vs Previsto | mape_history | Coluna price vs preço implícito no revenue |
| **Volumetria de Erros Inf (Novo)** | Contagem distinta de ocorrências is_inf = TRUE | mape_history | **Monitorar crescimento**. Mostra quantas vezes o modelo "alucinou" receita em dias zerados. |

### 3.3. Seção 2: Decomposição do Erro (Gráfico de Rosca)

"De quem é a culpa do erro?"

* **Fonte:** mape_ranked_properties
* **Métrica:** Média das colunas de ratio (block_mape_ratio, occupancy_mape_ratio, price_mape_ratio).
* **Insight:** Responder se o erro subiu por causa de bloqueio, preço ou ocupação.

### 3.4. Seção 3: Alertas de Granularidade (Cards)

* **Filtro:** is_critical = TRUE.
* **Visual:** Exibir granularity_type (ex: Estado) e granularity_value (ex: SP) que estão estourando o MAPE.
* **Dica:** Usar a coluna comparison_to_base_mape para mostrar o quão pior que a média esse grupo está (ex: "SP está 50% acima da média global").

### 3.5. Seção 4: Gráficos Temporais (Linhas/Barras)

* **Eixo X:** date.
* **Séries:**

  
  1. **Ocupação:** Barras Real vs Previsto.
  2. **Bloqueios:** Barras Real vs Previsto.
  3. **Concordância de Fontes:** Linhas contando ocorrências no array block_reason.
     * *Check:* Se o BI tool não ler Array nativamente, criar medida calculada: CONTAINS(block_reason, "ml3").

### 3.6. Seção 5: Top Imóveis (Tabela)

* **Fonte:** mape_ranked_properties.
* **Colunas:** ID, MAPE Value, Fator Principal, Variação (comparado a período anterior se possível, ou apenas valor absoluto).
* **Ação:** Botão/Link para o ID do imóvel.
* **Tratamento de Infinitos:**
  * Registros com is_inf = TRUE **DEVEM aparecer na tabela**.
  * Na coluna de valor MAPE, exibir o texto **"INF"** ou um ícone de alerta vermelho.
  * Eles representam os casos extremos onde o denominador foi zero.


\