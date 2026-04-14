<!-- title: System Price - Evolução Não Sazonais | url: https://outline.seazone.com.br/doc/system-price-evolucao-nao-sazonais-dssqQ4m72A | area: Tecnologia -->

# System Price - Evolução Não Sazonais

**Data:** 07 de Novembro de 2025 

**Versão:** 1.0 

**Autor:** Lucas Abel da SIlveira PM(Dados)

## **1. Visão Geral e Contexto**

O objetivo deste Discovery é guiar a próxima onda de evolução do System Price. O foco é transformá-lo de uma ferramenta de automação para um motor de precificação **inteligente, proativo e adaptativo**. As iniciativas a seguir priorizam a resolução de dores atuais, a construção de uma base sólida para o futuro e a exploração de estratégias de alto impacto para maximizar a receita do portfólio.

## **2. Iniciativas Priorizadas**

As iniciativas estão organizadas por prioridade de implementação, balanceando o impacto no negócio com o esforço de desenvolvimento.

### **Prioridade 1: Quick Wins (Alto Impacto, Baixo Esforço)**

**1.1. Alerta de Consistência de Matriz/Estrata**

* **Problema:** Atualmente, imóveis de estrata inferior (ex: SUP 2Q) podem ser precificados mais caro que imóveis de estrata superior (ex: TOP 2Q) na mesma categoria. Isso quebra a lógica de negócio e pode indicar erros de classificação ou de dados de concorrência.
* **Solução Proposta:** Criar um alerta automatizado que notifique a equipe quando essa inconsistência for detectada. O alerta deve conter o imóvel, a categoria e os preços comparados.
* **Critérios de Sucesso:** A equipe consegue identificar e corrigir inconsistências rapidamente. A frequência desses erros é reduzida ao longo do tempo.

**1.2. Alerta de Qualidade de Concorrentes**

* **Problema:** A precisão do System Price depende diretamente da qualidade e quantidade dos concorrentes. Uma queda repcente nesses dados pode comprometer a precificação sem que a equipe perceba.
* **Solução Proposta:** Desenvolver um alerta que monitore a saúde dos dados de concorrência por categoria. Notificar quando o número de concorrentes ativos cair abaixo de um limiar crítico.
* **Critérios de Sucesso:** A equipe é proativamente informada sobre problemas de dados, permitindo ações corretivas antes que impactem negativamente a receita.

**1.3. Ação Imediata: Separar Brasília do Cluster Atual( Primeira a ser feita )**

* **Problema:** Brasília possui um comportamento de final de semana distinto de Goiânia, e estar no mesmo cluster impede um ajuste fino necessário.
* **Solução Proposta:** Tratar Brasília como um caso excepcional, criando um cluster ou parâmetros específicos para ela, em vez de construir uma feature genérica de subcluster.
* **Critérios de Sucesso:** A precificação de Brasília para finais de semana se torna mais assertiva, sem impactar outras cidades.

### **Prioridade 2: Projetos Estruturantes (Alto Impacto, Esforço Médio/Alto)**

**2.1. Sistema de Alertas 2.0**

* **Problema:** O sistema atual de alertas é rudimentar, difícil de gerenciar e não possui um fluxo claro de validação, resultando em ineficiência e possíveis falhas.
* **Solução Proposta:** Evoluir para uma **planilha centralizada e interativa** (ex: Google Sheets conectada ao BigQuery). A planilha deve ter abas separadas para **Limites Superiores** e **Limites Inferiores**, com colunas para status (`**Pendente**`, `**Verificado**`, `**Ajustado**`, `**Ignorado**`) e comentários.
* **Critérios de Sucesso:** O tempo gasto pela equipe para gerenciar alertas é reduzido. Existe um histórico claro das ações tomadas para cada alerta.

**2.2. Motor de Precificação Inteligente**

* **Problema:** O motor atual é reativo apenas aos concorrentes e não se adapta com base na performance do próprio portfólio ou em regras de negócio mais dinâmicas.
* **Solução Proposta:** Introduzir uma nova camada de lógica que permita ao sistema se auto-ajustar com base em métricas internas. Esta iniciativa se desdobra em:
  * **Ajuste de Preços Conforme Desempenho:**
    * **Reativo à Meta:** Identificar imóveis em status "Crítico" (muito distante da meta de faturamento) e aplicar automaticamente uma estratégia de redução de preço.
    * **Reativo à Ocupação:** Ajustar preços de imóveis cuja ocupação está significativamente abaixo da média da categoria e dos concorrentes.
    * **Uso de "Escadinha" Dinâmica em Paralelo:** Utilizar uma versão mais rápida e integrada da lógica de "escadinha" como o mecanismo que viabiliza os ajustes reativos acima.
* **Critérios de Sucesso:** Aumento da ocupação e receita de imóveis com baixo desempenho. Redução da necessidade de intervenção manual para correções de preço.

**2.3. Sensibilidade a Estrata (Strata)**

* **Problema:** O sistema aplica a mesma estratégia de agressividade para todas as estratas (Top, SUP, Júnior), ignorando suas diferentes dinâmicas de mercado e valor percebido.
* **Solução Proposta:** Permitir que os parâmetros de precificação (ex: percentil-alvo) sejam ponderados pela estrata do imóvel.
  * ex:. Imóveis "Top" devem ser menos agressivos e mirar em percentis mais altos.
* **Critérios de Sucesso:** Melhora na performance de receita dos imóveis "Top" e na ocupação dos "Júnior", otimizando a receita geral do portfólio.

### **Prioridade 3: Apostas Estratégicas (Alto Impacto, Alta Complexidade)**

**3.1. Uso de Preço Histórico como Referência**

* **Problema:** Para datas muito distantes, a falta de dados de concorrência torna a precificação uma incerteza.
* **Solução Proposta:** Para datas de longo prazo (ex: >90 dias), incorporar o preço histórico do próprio imóvel para o mesmo período em anos anteriores como um parâmetro de peso no algoritmo.
* **Critérios de Sucesso:** A precificação de longo prazo se torna mais estável e fundamentada, reduzindo o risco de grandes erros de precificação para o futuro.
* **Perguntas Abertas:** Como ponderar o dado histórico vs. o dado de concorrente? Como lidar com anos atípicos?