<!-- title: Algoritmo Escadinha | url: https://outline.seazone.com.br/doc/algoritmo-escadinha-03zR8k2jBN | area: Tecnologia -->

# Algoritmo Escadinha

**Data da Elaboração: 03-06-2025**

**Participantes do Discovery (Stakeholders):**

* Time de RM: Responsável Fabio Garcia
* PM de Dados: Lucas Abel


1. **Introdução e Contexto do Negócio:**\nA Seazone administra um portfólio extenso de quase 2.000 imóveis para aluguel de temporada, utilizando OTAs. A precificação desses imóveis é gerenciada através da plataforma interna Sirius, que possui interfaces front-end como a "Planilha Setup" (para configurações) e a "Planilha AGC" (para precificação). Sirius é integrada a um Data Lake na AWS através de API Gateway e funções Lambda, que executam os processos de precificação.

   Iimóveis com características similares são agrupados em "categorias". Mesmo dentro desses grupos, a performance de faturamento individual varia, gerando a necessidade de equalizar o desempenho para tratar todos os proprietários de forma justa, incluindo um tratamento diferenciado para imóveis com performance excepcional (outliers).



2. **O Problema a Ser Resolvido:**\nO time de RM utiliza um processo manual e subjetivo para tentar equalizar o faturamento. Este processo envolve:

* **Análise Manual:** Utilizar uma planilha para consolidar o faturamento dos imóveis.
* **Clusterização "no Olhômetro":** Classificar imóveis em "Bom", "Médio" ou "Ruim".
* **Ajustes de Preço Manuais:** Aplicar +10% para "Bom" e -10% para "Ruim" via planilha "Setup".

 ![](/api/attachments.redirect?id=11175e7d-6b5c-4fed-a95f-e1d9cc879fc1 " =909x734")


**Limitações do Processo Atual:**

* **Subjetividade:** Classificação não padronizada e sem tratamento específico para outliers.
* **Intensidade de Trabalho Manual:** Demorado e propenso a erros.
* **Escalabilidade Limitada:** Aplicado a poucas categorias.
* **Falta de Padronização e Rastreabilidade:** Dificuldade em manter consistência.
* **Frequência Limitada:** Executado aproximadamente uma vez por mês.
* **Ajustes Fixos:** Os percentuais de ajuste são fixos e não facilmente adaptáveis.



3. **Objetivos do Projeto (O que se espera alcançar?):**\nO objetivo principal é **desenvolver e implementar um algoritmo/funcionalidade automatizada**, apelidado de "Algoritmo Escadinha", que permita:

   
   1. **Padronizar a Clusterização:** Definir critérios claros para classificar imóveis em clusters de performance (ex: Muito Alto, Alto, Médio, Baixo) com base em seu percentual de faturamento (utilizando dados do mês atual e mês+1).
   2. **Automatizar Ajustes de Preço Configuráveis:** Aplicar automaticamente modificadores de preço, com valores padrão (ex: +15% para Muito Alto, +10% para Alto, -10% para Baixo) mas que sejam **configuráveis como parâmetros** para futura adaptação. A automação ocorrerá via infraestrutura AWS.
   3. **Aumentar a Escalabilidade:** Aplicar a estratégia a todas as categorias elegíveis (>= 7 imóveis), identificadas automaticamente via Data Lake.
   4. **Equalizar Performance e Otimizar Receita:** Promover uma rotação na performance, equilibrando o faturamento entre proprietários e aplicando um prêmio maior a outliers.
   5. **Reduzir Esforço Manual:** Liberar o time de RM.
   6. **Aumentar a Frequência e Agilidade:** Permitir ciclos de reavaliação e ajuste mais frequentes (ex: 7, 10, 15 dias).
   7. **Garantir Rastreabilidade:** Gerar histórico detalhado das alterações no Data Lake.

      \
4. **Usuários e Seus Papéis:**

* **Time de RM:** Principais usuários. Monitorarão os resultados, analisarão a eficácia e, futuramente, poderão ajustar os parâmetros de percentual de ajuste dos clusters.
* **Time DataSolutions** Responsáveis pelo desenvolvimento, implementação, manutenção e garantia da configurabilidade dos parâmetros.


5. **Processo Desejado (Fluxo da Solução Automatizada):**

   
   1. **Identificação Automática de Categorias:** O sistema, via queries no Data Lake, identifica categorias elegíveis (>= 7 unidades).
   2. **Coleta de Dados de Performance:** Para cada categoria, coleta faturamento do mês atual (M0) e próximo mês (M+1).
   3. **Cálculo de Performance Individual:** Calcula o percentual de participação no faturamento da categoria (M0 e M+1) para cada imóvel.
   4. **Clusterização Automática:**
      * **Identificação de Outliers (Muito Alto):** O sistema primeiro identifica imóveis com performance excepcionalmente alta (outliers) e os classifica como \[categoria\]_muito_alto (ex: com base em desvios padrão acima da média, ou um percentil superior específico).
      * **Classificação dos Demais:** Os imóveis restantes são classificados em \[categoria\]_alto, \[categoria\]_medio, \[categoria\]_baixo, com base em regras pré-definidas sobre sua performance relativa.
   5. **Criação/Atualização de Grupos de Precificação Lógicos:** O sistema associa internamente os imóveis aos seus respectivos clusters.
   6. **Aplicação dos Modificadores de Preço via AWS:**
      * Para imóveis no cluster \[categoria\]_muito_alto, o sistema aplica um acréscimo (valor padrão: +15%, configurável).
      * Para imóveis no cluster \[categoria\]_alto, o sistema aplica um acréscimo (valor padrão: +10%, configurável).
      * Para imóveis no cluster \[categoria\]_baixo, o sistema aplica um desconto (valor padrão: -10%, configurável).
      * Imóveis no cluster \[categoria\]_medio não sofrem alteração por esta regra.
      * **Nota:** Os percentuais de ajuste devem ser implementados de forma a aceitar parâmetros, utilizando os valores citados como default caso nenhum parâmetro seja fornecido.
   7. **Geração de Log de Precificação:**
      * Para cada execução e imóvel alterado, registra no Data Lake: ID do Imóvel, Categoria, Data/Hora, Cluster do Imóvel, Preço Antes, Percentual de Ajuste Aplicado, Preço Depois.
   8. **Agendamento/Recorrência:** O processo completo é executado automaticamente em frequência configurável (ex: a cada 7, 10, 15 dias).

      \
6. **Critérios de Sucesso:**

* Redução significativa do tempo do time de RM.
* Aplicação da estratégia a todas as categorias elegíveis.
* Manutenção/melhoria da satisfação dos proprietários.
* Maior equalização de faturamento.
* Execução do ciclo em intervalos menores.
* Disponibilidade de histórico completo no Data Lake.
* Flexibilidade para configurar os percentuais de ajuste para cada cluster.



7. **Considerações Adicionais / Perguntas em Aberto:**

* **Qual será a regra algorítmica para definir um imóvel como 'Muito Alto' (outlier)?** (Ex: X desvios padrão acima da média do % de faturamento da categoria, top N% imóveis, etc.)
* Qual será a regra exata para definir os clusters "Alto", "Médio" e "Baixo" após a remoção dos outliers? (Ex: tercis do restante, percentis fixos?)
* Os valores de ajuste de preço (default: -10% Baixo, +10% Alto, +15% Muito Alto) serão configuráveis globalmente ou por categoria? Como essa configuração será gerenciada (ex: arquivo de configuração, variável de ambiente da Lambda)?
* Como serão tratados imóveis "novos"?
* Qual a frequência ideal de execução e este parâmetro será facilmente configurável?
* O histórico no Data Lake precisará ser consumido por alguma ferramenta de BI?
* A integração Sirius <> OTAs já lida com atualizações de preço originadas pelo backend?