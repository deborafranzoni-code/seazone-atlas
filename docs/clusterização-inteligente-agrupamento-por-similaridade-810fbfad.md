<!-- title: Clusterização Inteligente: Agrupamento por Similaridade | url: https://outline.seazone.com.br/doc/clusterizacao-inteligente-agrupamento-por-similaridade-9BCe7F41nJ | area: Tecnologia -->

# Clusterização Inteligente: Agrupamento por Similaridade

### **1. Contexto de Negócio**

**Problema Atual:**\nO System Price tem eficácia comprovada , mas sua parametrização manual é inviável para quantidade excessiva de categorias e 2 mil imóveis. Cada categoria exige configuração de 96 parâmetros em uma matriz complexa, gerando sobrecarga operacional e impedindo a escalabilidade.

**Oportunidade:**\nAo agrupar categorias com comportamentos de precificação semelhantes, podemos reduzir drasticamente a complexidade operacional. Em vez de parametrizar 600 categorias individualmente, o time de RM gerenciaria \~10-15 clusters, com matrizes compartilhadas.

### **2. Objetivos do Projeto**

**Objetivo Principal:**\nCriar grupos de categorias não sazonais com padrões históricos de precificação similares para viabilizar a parametrização em escala do System Price.

**Objetivos Secundários:**

* Reduzir o esforço de parametrização de 96 para 1 decisão por cluster (escolha de agressividade).
* Identificar categorias "exceção" que requerem atenção manual do time de RM.
* Fornecer uma base objetiva (dados) para discussões de estratégia de precificação.


### **3. Requisitos Funcionais**

| **Requisito** | **Prioridade** |
|----|----|
| Agrupar categorias por similaridade de padrões de percentis vs. concorrentes (EX:. últimos 12 meses) | Alta |
| Identificar e rotular categorias atípicas como "exceções" para análise manual | Média |
| Gerar uma matriz de parâmetros representativa para cada cluster | Alta |
| Suportar re-clustering periódico (semestral) para capturar mudanças de mercado | Baixa |


---

### **4. Requisitos Não-Funcionais**

| **Requisito** | **Justificativa** |
|----|----|
| Tempo de processamento < 30 minutos para todas categorias não sazonais | Garantir viabilidade operacional |
| Estabilidade: mesmos dados → mesmos clusters | Essencial para confiança do time de RM |
| Interpretabilidade: capacidade de explicar por que categorias foram agrupadas | Crítico para adoção pelo negócio |
| Robustez a outliers (categorias atípicas não devem distorcer clusters) | Garantir qualidade dos grupos |

### **5. Recomendações Técnicas (Baseadas em Pesquisa)**

*A seguir, recomendações fundamentadas para orientar a arquitetura, sem caráter impositivo.*

**5.1. Abordagem de Clusterização** **Recomendação Principal:**

\n**Clusterização Hierárquica Aglomerativa** com métrica DTW (Dynamic Time Warping).

[Relatório de Pesquisa_ Modelagem de Agrupamento para Precificação de Imóveis.pdf 415537](/api/attachments.redirect?id=972cbbc3-67da-483f-9020-9a4d566663dd)

**Por que esta abordagem?**

* Pesquisa indica que é o método que melhor equilibra interpretabilidade (essencial para validação com RM) e capacidade de lidar com padrões temporais.
* O dendrograma gerado permite ao time de RM visualizar e discutir diferentes cortes de clusters.
* Não exige número pré-definido de clusters, permitindo descoberta baseada em dados.

**Alternativa Complementar:**\n**DBSCAN** para identificação de outliers (categorias exceção).


**5.2. Pré-processamento de Dados** **Passos Essenciais:**


1. **Padronização (Z-Score):**
   * Variáveis como percentis (0-100) e preços (R$) têm escalas diferentes.
   * Pesquisa mostra que sem padronização, variáveis de maior magnitude dominam a distância.
2. **Redução de Dimensionalidade (PCA):**
   * 12 meses × 5 variáveis = 60 dimensões → risco de "maldição da dimensionalidade".
   * Recomendação: Reduzir para componentes que capturem >85% da variância.
3. **Filtragem Inicial:**
   * Excluir categorias com <9 meses de histórico (evitar distorções).
   * Categorias novas ficam em cluster "Default" até acumularem dados.

**5.3. Validação de Qualidade** 

**Métricas Quantitativas (para triagem):**

* Silhouette Score (>0.5 indica boa separação)
* Davies-Bouldin Index (<1 ideal)
* Método do Cotovelo (para definir número de clusters)

**Validação Qualitativa (decisiva):**

* Sessão com time de RM para validar:
  * Coerência dos clusters do ponto de vista de mercado
  * Exemplos de categorias em cada cluster
  * Matrizes representativas geradas

### **6. Entregáveis Esperados**

| **Entregável** | **Formato** |
|----|----|
| Dataset de clusters | Tabela AWS (Athena/Glue) |
| Matrizes por cluster | JSON no S3 (estrutura padronizada) |
| Dendrograma para validação | Visualização interativa (Plotly/D3.js) |
| Documentação de clusters | Com exemplos de categorias |


* #### **Exemplo de Tabela de Saída (Clusters)**

| **categoria_id** | **cluster_id** | **percentil_medio_DS** | **percentil_medio_FS** | **outlier_flag** |
|----|----|----|----|----|
| Saz-Goiania-Leste-apartamento-SUP-1Q | CLUSTER_01 | 42 | 45 | FALSE |
| Saz-Goiania-Oeste-apartamento-SUP-1Q | CLUSTER_01 | 41 | 44 | FALSE |
| Saz-Brasilia-Asa-Norte-apartamento-SUP-1Q | CLUSTER_02 | 38 | 40 | FALSE |
| Saz-PortoAlegre-Centro-apartamento-MASTER-1Q | OUTLIER | 65 | 70 | TRUE |

\n

### **7. Integração com Outros Sistemas**

**7.1. System Price (Motor de Precificação)**

* **Entrada:** ID da categoria → ID do cluster
* **Saída:** Matriz de parâmetros correspondente ao cluster
* **Integração:** Consulta ao DynamoDB para obter matriz do cluster

**7.2. Visualização de Validação ( Relatório )**

* **Dados:** Cluster de cada categoria + métricas de validação
* **Visualização:** Mapa de clusters com exemplos de categorias\n

#### **8. Riscos e Mitigações**

| **Risco** | **Probabilidade** | **Impacto** | **Mitigação** |
|----|----|----|----|
| Clusters não fazem sentido para o negócio | Média | Alto | Validação com RM antes de produção |
| Alto número de clusters (>20) | Baixa | Médio | Definir faixa alvo (10-15) no início |
| Categorias novas sem histórico | Alta | Baixo | Cluster "Default" com matriz genérica |
| Instabilidade entre execuções | Baixa | Alto | Fixar random seed e versão de bibliotecas |

### \n9. **Etapas Propostas (Passo a Passo Sugerido)**

**Etapa 1: Preparação dos Dados** 

*  Extrair dados históricos dos últimos 12 meses (percentis, ocupação, faturamento).( Validar quant. meses )
*  Filtrar categorias com <9 meses de histórico. Validar quant. meses )
*  Aplicar padronização (Z-Score) e redução de dimensionalidade (PCA).

**Etapa 2: Clusterização Inicial** 

*  Executar clusterização hierárquica com DTW.
*  Identificar outliers com DBSCAN.
*  Gerar dendrograma para análise.

**Etapa 3: Validação com Negócio** 

*  Apresentar dendrograma e clusters propostos ao time de RM.
*  Ajustar parâmetros (ex: número de clusters) com base no feedback.
*  Documentar regras de cada cluster (ex: "Cluster 1: Apartamentos 1Q com P40-P45").

**Etapa 4: Geração de Matrizes** 

*  Calcular matriz média para cada cluster.
*  Exportar matrizes para S3 em formato JSON.
*  Criar tabela de mapeamento (categoria → cluster).

**Etapa 5: Integração e Teste** 

*  Atualizar System Price para consultar matrizes por cluster.
*  Testar precificação com 4 categorias piloto.
*  Validar com time de RM se preços gerados fazem sentido.

**Etapa 6: Monitoramento (Contínuo)**

*  Agendar re-clustering trimestral.
*  Criar alerta para clusters com muitas mudanças (ex: >30% das categorias migraram).
*  Revisar documentação a cada atualização.