<!-- title: System Price Sazonal - Lab Floripa (Fase Centro) | url: https://outline.seazone.com.br/doc/system-price-sazonal-lab-floripa-fase-centro-ukBZtKz5Jv | area: Tecnologia -->

# System Price Sazonal - Lab Floripa (Fase Centro)

**Autor:** PM Dados (Unificada) 

**Versão:** 1.0

**Data:** 14/01/2026


## **1. Visão Geral e Objetivos**

O objetivo desta iniciativa é expandir o motor de precificação dinâmica (System Price) para mercados de **Alta Sazonalidade**, iniciando com um laboratório controlado em Florianópolis. O foco é validar se o algoritmo consegue manter os imóveis dentro ou acima da Meta de Faturamento, reduzindo o trabalho manual do time de Revenue Management (RM).

## **2. Escopo de Dados (Cluster Piloto)**

O algoritmo deve ser aplicado exclusivamente a um recorte específico de imóveis (Cluster) definido como:

* **Localização:** Cidade de Florianópolis (Foco: Região Centrão + Região da UFSC).
* **Estratos (Strata):** Apenas **JR** (Junior) e **SUP** (Superior).
  * *Exclusão:* Estratos TOP e MASTER.
* **Característica:** Imóveis com **<= 3 quartos**.
* *Nota:* O sistema deve permitir fácil configuração para inclusão/remoção de imóveis deste cluster via tabela de configuração ou flag de categoria.

## **3. Estratégia de Entrega e Fases de Desenvolvimento**

Para garantir o sucesso da implementação e validação, o projeto foi dividido em duas fases sequenciais.

### **Fase 1: Implementação Base e Simulação (Shadow)**

Esta fase tem como objetivo calibrar o motor na nova região sem impacto no faturamento real, validando a base e a segurança.

* **Matriz de Parâmetros:**
  * Utilizar a **estrutura de matriz existente** (Sazonalidade x Ocorrência x Antecedência).
  * Realizar a **reparametrização** dos valores (percentis) para adequar ao comportamento de Florianópolis Centrão/UFSC.
  * *Nota:* Manter a lógica atual de Final de Semana (FDS) dentro da matriz, apenas ajustando os números para a realidade local.
* **Clusterização:**
  * Criar o cluster **"Sazonais-centro-SC-imóveis-JRSUP-3Q"**.
  * Adicionar todos os imóveis elegíveis a este cluster.
* **Limites de Segurança (Floor/Ceiling):**
  * Implementar a lógica de limites baseada em **Match Sazonal** (histórico do mesmo período do ano anterior).
  * Aplicar estes limites já na Fase 1 para garantir segurança da simulação.
* **Execução (Modo Shadow):**
  * Adicionar as categorias apenas no **Cluster**.
  * **NÃO** adicionar as categorias na aba de Setup (AGC).
  * O sistema calculará os preços, mas eles não serão enviados para as OTAs.
  * Dados ficarão disponíveis para validação via BI.
* **Validação:** O RM analisará se os preços sugeridos fazem sentido.

### **Fase 2: Granularidade de Eventos e Refinamento**

Após validação e aprovação da Fase 1 pelo RM, procede-se para adicionar complexidade para eventos críticos.

* **Matriz de Parâmetros:**
  * Adicionar **Granularidade de Eventos**: Diferenciação de Feriados e Eventos por níveis de importância (1, 2, 3).
  * Ajustar a infraestrutura/Setup para receber essa nova classificação.
  * Parametrizar os percentis específicos para cada nível (ex: Carnaval/ Réveillon com percentis mais agressivos que um feriado comum).
* **Teste e Validação:** Nova rodada de simulação para validar se os níveis de impacto dos eventos estão corretos.

## **4. Requisitos Funcionais e Lógica de Negócio**

### **4.1. Lógica de Limites de Segurança** 

O motor deve aplicar limites inferiores e superiores antes de gerar o preço final, tanto na Fase 1 quanto na 2.

* **Regra de Match Sazonal:** O preço mínimo  e máximo  deve ser baseado no **histórico de precificação manual** de **mesmo período sazonal** (ano anterior ou equivalente).
* **Inflação:** Nesta fase, **NÃO** aplicar índices de correção inflacionária sobre o histórico. Usar o valor nominal histórico.

### **4.2. Lógica de Feriados Históricos**

Ao calcular preços ou simular backtesting, o sistema deve considerar a data de referência (data de precificação) para saber quais feriados estavam vigentes naquele momento.

* *Requisito:* Se calcular um preço para uma data futura "hoje", considerar o calendário de feriados atual. Se simular um preço no passado (backtesting), considerar o calendário de feriados daquela data passada.

### **4.3. Fluxo de Execução (Shadow vs Go-Live)**

O desenvolvimento deve aproveitar a mecânica natural do Sirius:


1. **Simulação (Shadow):** Ocorre ao adicionar os imóveis apenas no **Cluster**. O preço é calculado, mas o Setup não o envia para o canal.
2. **Produção (Go-Live):** Ocorre ao adicionar as categorias na **Setup**. A partir deste momento, o preço gerado pelo Cluster é enviado para as OTAs.
   * *Instrução:* Para o MVP, iniciaremos apenas na etapa 1 (Simulação/Shadow).

## **5. Requisitos de Dados e Entradas**

O desenvolvedor deve garantir que o pipeline de dados alimente o motor com:


1. **Matriz de Parâmetros (CSV/DB):** Fase 1 (Estrutura Atual + Reparametrização) -> Fase 2 (Estrutura com Níveis de Evento).
2. **Configuração de Cluster:** Lista de imóveis/IDs pertencentes ao "Sazonais-centro-SC-imóveis-JRSUP-3Q".
3. **Preços Manuais Históricos:** Para cálculo do Floor/Ceiling sazonal (necessário desde a Fase 1).
4. **Classificação de Eventos (Fase 2):** Tabela ou dicionário que informe, para cada data/evento, qual é o seu Nível (1, 2 ou 3). *Alimentado pelo RM.*

## **6. Saídas Esperadas**


1. **Fase 1:**
   * Cluster criado e populado.
   * Matriz reparametrizada carregada.
   * Backtest/Simulação rodando com sucesso para validação do RM.
2. **Fase 2:**
   * Atualização da estrutura de dados para suportar Níveis de Evento.
   * Atualização do Dashboard (Looker) para visualizar o impacto de eventos N1, N2, N3.

## **7. Critérios de Aceite (Success Criteria)**

*  O motor roda a simulação (Fase 1) para o cluster Centrão/UFSC sem erros.
*  Os Limites de Segurança baseados em histórico sazonal são aplicados corretamente na Fase 1.
*  O sistema permite a transição de Simulação (Cluster only) para Produção (Setup) sem mudança de código, apenas configuração.
*  (Fase 2) O sistema distingue e aplica percentis diferentes para Eventos de nível 1 vs 3.

\n