<!-- title: BraimStorming | url: https://outline.seazone.com.br/doc/braimstorming-EVPnR4r9sj | area: Tecnologia -->

# BraimStorming

### Documentação do Brainstorming sobre Detecção de Anomalias


---

#### **1. Contexto:**

No setor de aluguel por temporada, identificar anomalias no faturamento, preços e ocupação dos imóveis é crucial para otimizar as estratégias de precificação e garantir a maximização da receita. Anomalias podem indicar situações atípicas que requerem análise e intervenção, como preços excessivamente baixos ou altos, ou ocupações fora do comum. Para isso, é necessário o uso de técnicas avançadas de análise de dados, incluindo métodos de inteligência artificial, para monitoramento e detecção precisa.


---

#### **2. Objetivo:**

O objetivo deste brainstorming é detalhar as diferentes formas de identificar e tratar anomalias nos dados relacionados ao aluguel por temporada, como faturamento, ocupação e comportamento de preços. O plano inclui técnicas específicas de detecção, métodos de análise e ações corretivas que podem ser tomadas automaticamente ou de forma assistida.


---

#### **3. Pontos debatidos:**

##### **3.1 Definição de Anomalias:**

* **Imóvel com faturamento acima de seus similares:**
  * Comparar o faturamento de um imóvel com outros similares para detectar excessos.
* **Mudança de comportamento do preço - mesmo host:**
  * Detectar grandes variações de preços em comparação com o mesmo período de anos anteriores.
  * Analisar alterações de preços de maneira anormal.
* **Diferenças do padrão de faturamento do imóvel:**
  * Identificar imóveis com faturamento desproporcional ao número de reviews recebidos.
* **Diferenças grandes de preços de Grupo similar:**
  * Comparar preços de grupos similares ao longo do tempo para encontrar desvios significativos.
  * Analisar alterações de preços em grupos.
* **Anomalias gritantes de ocupação:**
  * Exemplo: ocupação consistentemente próxima de 100%, o que pode indicar preços inadequados.

    ![](/api/attachments.redirect?id=bbc4ffed-ac37-4456-8623-3267fe7b5e31 " =1340x547")

##### **3.2 Como Identificar Anomalias:**

* **Comparar dados atuais com o histórico:**
  * Comparar padrões atuais com dados históricos para detectar variações.
* **Comparar dados de imóveis similares:**
  * Utilizar benchmarks de imóveis semelhantes para análises comparativas.

    ![](/api/attachments.redirect?id=711f5e63-dac4-48b2-a2ec-579df683d7f4 " =624x262")

##### **3.3 Tipos de Técnicas:**

* **Técnicas de autoencoders:**
  * Uso de redes neurais (ML) para identificar padrões não lineares.
* **Lógicas de Heurística:**
  * Aplicação de regras específicas para detecção rápida.
* **IA Generativa:**
  * Analisar dados complexos com modelos de inteligência artificial.
* **Técnicas Time Series:**
  * Aplicar métodos como ARIMA, SARIMA, e Forecast para prever anomalias.
* **Definição de filtros:**
  * Utilização de limites mínimos e máximos para detectar desvios.
* **Técnicas de clusterização:**
  * Uso de algoritmos como K-means para segmentar e identificar outliers.

    ![](/api/attachments.redirect?id=742cf3b0-3715-44be-992f-3d52cd88391b " =847x498")

##### **3.4 Ações a serem Tomadas:**

* **Canal de Alertas:**
  * Notificar automaticamente os stakeholders sobre as anomalias detectadas.
* **Limpeza:**
  * Corrigir ou excluir dados incorretos para manter a integridade do banco de dados.
* **Correção Automática:**
  * Implementar sistemas que ajustam os preços automaticamente.
* **Visualização em Planilhas:**
  * Representar as anomalias detectadas de forma clara e intuitiva.
* **Dashboard:**
  * Criar painéis para o monitoramento contínuo das anomalias.
* **Integração de avisos:**
  * Incorporar alertas nas entregas de dados regulares.
* **Tag de Anomalia:**
  * Marcar automaticamente tabelas com dados anômalos para facilitar o acompanhamento.

    ![](/api/attachments.redirect?id=b0e965aa-5756-4d6a-a6bc-9dad97389942 " =845x369")