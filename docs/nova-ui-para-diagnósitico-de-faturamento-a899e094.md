<!-- title: Nova UI para Diagnósitico de Faturamento | url: https://outline.seazone.com.br/doc/nova-ui-para-diagnositico-de-faturamento-GqKifj2mn0 | area: Tecnologia -->

# Nova UI para Diagnósitico de Faturamento

**Projeto:** Calculadora de Viabilidade de Faturamento - (Nome provisório)

**Versão:** 1.0 (MVP) 

**Responsável:** Lucas Abel (PM Dados) 

**Data:** 26/01/2026


## **1. Visão Geral**

### **1.1. O Problema**

O time de Expansão e Vendas utiliza atualmente uma planilha complexa para analisar o potencial de faturamento de imóveis. A ferramenta é lenta, pouco intuitiva e não permite criar uma narrativa comercial rápida para fechar negócios com incorporadores e parceiros.

### **1.2. A Solução (MVP)**

Uma aplicação web leve (**Calculadora de Rentabilidade**) que permite ao usuário simular o faturamento de um imóvel em segundos. A interface deve focar em **clareza e visualização de dados**, abandonando a complexidade técnica em favor de uma narrativa comercial persuasiva.


## **2. Arquitetura da Informação & Fluxo**

### **2.1. O Usuário e Seus Objetivos**

* **Perfil 1: Expansão:** Precisa validar um terreno ou prédio novo rapidamente.
  * *Necessidade:* "Esse prédio vale a pena? Qual é o teto de receita possível?"
* **Perfil 2: Parceiro/Corretor:** Precisa convencer um proprietário a entregar o imóvel para a Seazone.
  * *Necessidade:* "Mostre-me números bonitos para eu colocar no meu pitch."

### **2.2. O Fluxo do Usuário** 


1. **Acesso:** O usuário acessa a URL da ferramenta.
2. **Seleção:** Seleciona **Cidade** e **Bairro** (Dropdown).
3. **Tipologia:** Define **Tipo** (Apto/Casa) e **Quartos** (1, 2, 3).
4. **Ação:** Clica em "Simular Rentabilidade".
5. **Resultado:**
   * O sistema calcula e exibe o **Faturamento Líquido Anual (P50)**.
   * Exibe um **Mapa de Calor** (Contexto) mostrando onde estão os imóveis comparáveis.
   * Mostra os **3 Cenários** (P25, P50, P75).


## **3. Regras de Negócio**

### **3.1. Lógica de Cálculo (Percentis)**

Para garantir simplicidade e abrangência, utilizaremos distribuição percentilar baseada nos últimos 12 meses:

* **Cenário Conservador (P25):** O faturamento do quartil inferior (baixa performance). Serve como "piso de segurança".
* **Cenário Base (P50 - Mediana):** O faturamento esperado. **Este será o número principal (Hero).**
* **Cenário Agressivo (P75):** O teto de receita dos imóveis bem gerenciados.

### **3.2. Tratamento de Falta de Dados (Transparência)**

* **Regra:** Se a busca retornar **menos de 10 imóveis**, o sistema **NÃO** deve calcular nem exibir gráficos.
* **Ação:** Exibir uma mensagem de alerta: *"Poucos dados neste bairro para uma análise segura. Tente selecionar a cidade inteira ou bairros vizinhos."*
* **Motivo:** Evitar projeções baseadas em amostra muito pequena que possam ser enganosas.

### **3.3. Variáveis Excluídas (MVP)**

* **Strata (Padrão):** Não será solicitada ao usuário e não será filtro explícito na interface para não complicar o fluxo, sendo usada apenas internamente se necessário para ordenação.


## **4. Funcionalidades da UI (Especificação Visual)**

A interface será dividida em 3 blocos horizontais ou verticais :

### **A. Header & Inputs**

* Inputs limpos: Estado, Cidade, Bairro, Tipo, Quartos.
* Botão CTA: "Calcular".

### **B. Dashboard de Resultados**

* **Hero Card:** Título grande "Faturamento Líquido Anual Estimado". Valor em destaque (Ex: **R$ 84.500**).
* **Sub-texto:** "Baseado na análise de 45 imóveis na região nos últimos 12 meses."
* **KPIs Secundários:** Diária Média (ADR) e Taxa de Ocupação.

### **C. Visualização de Mercado (Mapa & Gráficos)**

* **Gráfico de Barras:** Comparativo dos 3 cenários (P25, P50, P75).
* **Mapa de Contexto (Read-Only):**
  * Mostra a poligonal do bairro selecionado.
  * Plotar "bolinhas" (Heatmap/Pins) dos imóveis usados na média.
  * *Cores:* Bolinhas vermelhas (baixo faturamento) a verdes (alto faturamento) para dar contexto visual de distribuição.
  * *Interatividade:* Ao passar o mouse, mostra o valor do vizinho.
  * *Nota:* O usuário **NÃO** desenhará o polígono nesta fase. É apenas ilustrativo da região selecionada.


## **5. Arquitetura Técnica e Escalabilidade**

Para garantir que esta ferramenta evolua de um MVP para um produto estratégico central para Expansão e Vendas, definimos as seguintes diretrizes técnicas obrigatórias:

### **5.1. Exclusão de Ferramentas de BI (Looker Studio / PowerBI)**

* **Diretriz:** Esta ferramenta **NÃO** deve ser desenvolvida em Looker Studio ou similar.
* **Justificativa:**

  
  1. **Futuro (Mapa Interativo):** As funcionalidades do Roadmap V2.0 (seleção de polígono no mapa, arrastar e soltar para atualizar dados) são inviáveis ou extremamente limitadas em plataformas de BI.

  
  1. **Experiência Externa:** A ferramenta será utilizada por parceiros externos (corretores/incorporadores), exigindo uma interface personalizada (White-label) que transmita profissionalismo, sem a aparência de um relatório interno.
  2. **Manutenibilidade:** Customizar lógicas de negócio complexas (ex: regras de transparência de dados insuficientes) é mais eficiente e escalável em código do que em fórmulas de BI.

### **5.2. Stack Recomendada (Web App)**

* **Frontend:** Uma aplicação Web leve (ex: React ou Next.js) que consuma nossa API atual.
* **Backend:** Reutilizar a estrutura `**analise_faturamento_api**` adicionando o endpoint de agregação.
* **Mapa:** Utilizar uma biblioteca de mapas robusta.
  * *Nota:* No MVP (V1), a biblioteca será usada em modo "Read-Only" (apenas visualização dos pins).

*Evolução:* Na V2, habilitaremos os controles de desenho e interação sem precisar trocar a biblioteca ou arquitetura.


## **6. Roadmap de Evolução (Pós-MVP)**

### **V1.5 (Melhoria de Dados)**

* Implementação de ML para preencher lacunas de dados em regiões carentes (Preditivo).

### **V2.0 (Mapa Interativo)**

* Permitir que o usuário desenhe o polígono (arraste e solte) no mapa para definir a região de análise.
* Atualização em tempo real ao mover o mapa.