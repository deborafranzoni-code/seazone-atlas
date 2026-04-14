<!-- title: Call dia 18-11-25 | url: https://outline.seazone.com.br/doc/call-dia-18-11-25-R43uA5WVwb | area: Tecnologia -->

# Call dia 18-11-25

## **Resumo da Reunião Quinzenal BU Dados Geográficos**

## **1. Abertura e Contexto da BU**

* **Objetivo da BU:** Tatiana iniciou a reunião reafirmando o propósito da BU de Dados Geográficos: centralizar todas as iniciativas de dados espaciais (mapas, faturamento, dados do Viva Real, etc.) para criar uma fonte única e coerente de inteligência.
* **Stakeholders Principais e suas Necessidades:**
  * **Análise de Terrenos (Tatiana/Becca):** Uso diário para análise e compra de terrenos.
  * **Expansão (Caio):** Dados para identificar regiões e incorporadoras para novas atuações.
  * **Comercial (JP):** Dados para gestão e para criar apresentações de venda dos spots.
  * **Marketing (Priscila):** Dados para construir a autoridade da marca Seazone, criando "cases Jurerê" para qualquer região.

### **2. Projeto: Panorama do Marketing (Top 20)**

* **Validação com a Stakeholder (Priscila):** Priscila validou que o objetivo do projeto é exatamente o que ela precisa: a capacidade de criar apresentações tipo "case Jurerê" para qualquer cidade (ex: Natal, Goiânia) com dados de faturamento, ritmo, sazonalidade, etc.
* **Formato e Frequência:** A necessidade é que os dados sejam atualizados mensalmente para que o Marketing sempre possa usar o mês anterior como base, garantindo relevância para demandas internas (ex: Summit) e externas.
* **Autonomia:** Priscila confirmou que prefere extrair os dados do BI e montar as apresentações com seu time, sem necessidade de trabalho manual do time de Dados, a menos que um dado novo seja solicitado.
* **Status:** O desenvolvimento está em andamento, com a primeira entrega de validação prevista para a semana seguinte (24/11).

### **3. Projeto: BI dos Spots (Apresentação Spot)**

* **Objetivo e Uso Comercial (JP):** JP explicou que a necessidade surgiu após o sucesso da apresentação do spot Jurerê. O objetivo é replicar essa capacidade de análise para outras regiões (ex: Goiânia, Caraguatatuba, Bonito), destacando as particularidades e os diferenciais de cada uma.
  * **Exemplo de Uso:** Mostrar que Goiânia é uma região "flat" (sem sazonalidade), o que gera previsibilidade. Ou que em Caraguá, studios e quartos de 2 dormitórios faturam quase o mesmo, uma informação valiosa para a venda.
* **Demonstração ao Vivo e Feedbacks:** O grupo testou o BI ao vivo, e vários pontos de melhoria e dúvidas surgiram:
  * **Dado de Vaga na Garagem:** Mateus (Comercial) destacou que este dado é crucial para Caraguatatuba e teria um impacto enorme na venda. Foi verificado que o filtro já existe no BI.
  * **Diária Média vs. Máxima:** Caio (Expansão) questionou o uso da "diária máxima". A justificativa é para mostrar o potencial de pico (ex: Carnaval), mas foi levantada a sugestão de incluir também a diária média para um contexto mais completo.
  * **Filtros e Consistência:** Foi identificado um bug no filtro de período (ano a ano) que não retornava dados. JP também sugeriu a evolução de mostrar o crescimento ano a ano.
  * **Qualidade dos Dados:** Lucas (PM) usou o exemplo de Cacoapé, onde um único imóvel com faturamento altíssimo distorceu a média, levando a uma limpeza nos dados para exigir um número mínimo de listings para um bairro entrar no ranking.
* **Processo de Uso e Validação:**
  * **Quem Opera?** Tatiana e JP alinharam que, idealmente, o time de Análise de Terrenos (Becca) deve extrair e tratar os dados para o Comercial, evitando que diferentes pessoas cheguem a conclusões erradas a partir da mesma ferramenta.
  * **Validador do Dia a Dia:** Foi reconfirmado que **Becca Sassaki** é a responsável pela validação durante o desenvolvimento, e JP participa do treinamento e validação final.
  * **Acesso Imediato:** Tatiana liberou o time de Comercial a usar o BI imediatamente, mesmo em fase de validação, para já começarem a extrair valor.

### **4. Dor Central: Falta de uma Fonte Única de Dados**

* **O Problema:** Tatiana levantou um ponto crítico: hoje, diferentes áreas (Comercial, CS, Precificação) usam bases e definições diferentes para analisar os mesmos dados (ex: faturamento bruto vs. líquido, se o custo do condomínio está incluso ou não).
* **Consequência:** Isso gera incoerência e impede que a empresa tenha um "case de sucesso" unificado e confiável (ex: os dados do spot Jurerê).
* **Solução Esperada:** A expectativa é que os BIs desenvolvidos pela BU se tornem essa fonte única, padronizando as métricas e as análises em toda a empresa.

### **5. Próximos Passos e Processo de Feedback**

* **Coleta de Feedback:** Todos os stakeholders (Caio, JP, Becca, Priscila) foram incentivados a testar as ferramentas (principalmente o BI dos Spots) e enviar suas sugestões de melhorias e bugs para o Lucas.
* **Centralização:** Lucas sugestou que os feedbacks sejam enviados no canal da BU para dar visibilidade a todos.
* **Priorização:** Lucas irá compilar todos os feedbacks. Tatiana, como Head da BU, será a responsável final por negociar e definir as prioridades com cada área, para que o time de Dados não fique perdido e o trabalho seja focado.
* **Foco:** O foco imediato é continuar evoluindo os dois projetos ativos (Panorama e BI dos Spots) com base no feedback, em vez de iniciar novas demandas.

### **6. Outras Iniciativas e Backlog**

* Lucas mencionou brevemente outras iniciativas que estão no radar para o Q4 e no backlog, como:
  * Análise de valorização no BI Viva Real.
  * Expansão da categorização automática de listings.
  * Melhorias no Mapa de Terrenos (performance, link por terreno).
  * Uma "Calculadora de Faturamento" preditiva.

### **7. Encerramento**

* A reunião foi encerrada com o alinhamento de que as quinzenais serão a cadência para acompanhamento.
* Tatiana cobrou engajamento de todos para que os feedbacks sejam enviados, permitindo que a BU continue evoluindo.