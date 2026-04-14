<!-- title: Mapa de calor  polígonos RM | url: https://outline.seazone.com.br/doc/mapa-de-calor-poligonos-rm-eS45DH8pob | area: Tecnologia -->

# Mapa de calor  polígonos RM

**Autor:** Lucas Abel PM Dados (Unificada) 

**Versão:** 1.0

**Data:** 22/01/2026

Sugestão de Titulo do Produto: 

**Objetivo:** Permitir que o RM identifique visualmente, em um mapa interativo, quais polígonos atuais contêm micro-regiões com preços/valores distoantes (outliers), facilitando a redefinição estratégica dos limites de concorrência.

### **1. Interface do Usuário (UI) e Filtros Globais**

O objetivo é permitir que o RM navegue rapidamente até a área de interesse.

* **Filtro 1: Macrorregião (Estado/Cidade):**
  * *Descrição:* Dropdown ou Input de busca para selecionar a cidade de análise.
  * *Comportamento:* Ao selecionar a cidade, o mapa deve dar zoom automático para a região e carregar apenas os polígonos daquela localidade.
* **Filtro 2: Parâmetros de Sensibilidade (Configuração):**
  * *Descrição:* Sliders ou Inputs numéricos para calibrar a análise.
  * *Campos:*
    * **Amostra Mínima (N):** Mínimo de imóveis concorrentes por agrupamento (Strata + Quartos) para ser considerado válido (ex: "Ignorar grupos com menos de 5 imóveis").
    * **Limite de Discrepância (%):** Qual é a tolerância? (ex: "Se a média do grupo for 20% maior/menor que a média do polígono, considere distoante").

### **2. Lógica de Processamento de Dados (O "Cérebro" do App)**

Aqui definimos como o sistema deve calcular o "Calor" do mapa. O sistema **não** deve exigir que o RM selecione a categoria manualmente; ele deve escanear todas.

**Regra de Cálculo - "Score de Discrepância":**


1. **Agrupamento:** Para cada Polígono ativo, o sistema deve agrupar os concorrentes por: `**Strata (JR/SUP/TOP/Master)**` + `**Número de Quartos**`.
2. **Filtro de Amostragem:** Descartar grupos que não atendam ao parâmetro de "Amostra Mínima" (definido no Filtro 2). *Rationale: Garantir significância estatística.*
3. **Cálculo de Média Local:** Calcular a métrica alvo (Preço Médio, ADR ou Faturamento) para cada agrupamento dentro do polígono.
4. **Cálculo de Média Global do Polígono:** Calcular a média ponderada de toda a região do polígono (considerando todos os agrupamentos válidos).
5. **Comparação e Detecção de Anomalia:**
   * Verificar se a média de algum agrupamento específico (ex: JR1Q) está fora do limite de tolerância (%) em relação à Média Global do Polígono.
   * *Exemplo:* Se a média geral do polígono é R$ 500 e o grupo TOP2Q cobra R$ 800 (+60%), isso gera um alerta.
6. **Geração do Score (Heat):** Atribuir um "Score de Discrepância" ao polígono baseado na intensidade dos desvios encontrados.

### **3. Visualização do Mapa (UX)**

O mapa deve ser estilo "Google Maps" (estilo visual familiar), sobreposto com os polígonos.

**Estado Inicial:**

* Mapa exibe os polígonos preenchidos com cores baseadas no **Score de Discrepância**.
  * **Verde/Azul:** Polígono homogêneo (os preços dos diferentes Stratas/Quartos andam juntos ou não há discrepância relevante).
  * **Amarelo/Verde Água:** Discrepância moderada.
  * **Laranja/Vermelho (Cores Quentes):** Alta discrepância detectada (existe um grupo de imóveis pagando muito mais ou muito menos que a média da região, sugerindo que aquele pedaço do polígono é diferente).

**Interatividade (Drill-down):**

* **Ao passar o mouse (Hover) sobre um polígono "Quente":**
  * Exibir um Tooltip rápido: *"Discrepância Detectada: Grupo TOP2Q está 40% acima da média."*
* **Ao clicar no Polígono:**
  * O mapa deve dar zoom focado naquele polígono.
  * **Modo de Análise Micro (O "Raio-X"):**
    * O sistema exibe os pontos (imóveis) dentro do polígono coloridos pelo valor real (Preço/Renda).
    * *Visualização:* Isso permitirá ver a "mancha" de calor. Se o sistema alertou que o grupo TOP2Q está caro, o RM verá visualmente que todos os pontos TOP2Q estão concentrados na "parte de cima" do polígono, confirmando a micro-região nobre.

### **4. Dados Necessários (Inputs)**

Definição clara do que a área de dados precisa preparar (Data Core/BigQuery):

* **Polígonos:** Definições Geográficas (Lat/Long bounds ou GeoJSONs).
* **Concorrentes:**
  * Identificador único.
  * Strata (JR, SUP, TOP, Master).
  * Quantidade de Quartos.
  * Localização (Lat/Long).
  * Métricas de Negócio (Preço Diário Médio, ADR ou Faturamento - configurável pelo usuário).


---

### **5. Resultado Esperado (Success Criteria)**

Para validar se a ferramenta está resolvendo o problema:


1. O RM não precisa filtrar manualmente "Category -> TOP -> 2 Quarters". Ele olha para o mapa da cidade inteira.
2. Ele identifica rapidamente quais polígonos estão "Vermelhos".
3. Ao clicar no polígono vermelho, ele visualiza onde estão os imóveis caros/baratos e pode desenhar um novo polígono para separar aquela micro-região.
4. O processo de revisão de polígonos que demorava horas (analisando tabelas Excel) passa a ser feito em minutos via interface visual.