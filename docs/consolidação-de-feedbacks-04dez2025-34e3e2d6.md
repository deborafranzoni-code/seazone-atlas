<!-- title: Consolidação de Feedbacks - 04Dez2025 | url: https://outline.seazone.com.br/doc/consolidacao-de-feedbacks-04dez2025-qJVAvLULDi | area: Tecnologia -->

# Consolidação de Feedbacks - 04Dez2025

# **Relatório Oficial: Definições e Próximos Passos – BI Spots Comercial**

**Data:** 04 de Dezembro de 2025\n**Origem:** Consolidação de Feedbacks (Comercial/Clientes) + Validação Técnica (Dev/BI)\n**Status do Projeto:** Reta Final de Implementação (Sprint de Encerramento: Semana que vem)

**Participantes**: Kailany AlvesKailany, Lucas Machado, Márcio Fazolin, Lucas Abel


---

## **1. Resumo Executivo**

A reunião de alinhamento técnico definiu o escopo final para o lançamento da **Versão 1.0**. O objetivo é garantir que o BI seja uma ferramenta de venda completa. Por isso, a entrega do **ROI (Yield)** foi priorizada para esta sprint, utilizando o cruzamento de dados por Bairro. Funcionalidades como Filtros de Percentil e Link para Auditoria de Listings também entram para fechar o gap entre a análise manual e a automática.

A complexidade de **Seleção por Polígonos (Mapa)** fica para uma fase posterior, momento em que a lógica de ROI precisará ser revista.


---

## **2. Prioridade 1: Acionáveis Imediatos (To-Do Now)**

*Estas tarefas compõem o Escopo da Versão 1.0 e devem ser concluídas até o final da próxima semana.*

### **A. \[CRÍTICO\] Implementação de ROI / Yield**

* **Requisito:** O Comercial precisa apresentar o retorno do investimento (Slide 6/13), e não apenas o faturamento bruto.
* **Ação \[Dev/BI\]:** Criar métrica de **ROI Estimado**.
  * **Lógica de Cálculo:**

    
    1. Obter metragem do imóvel (via base Airbnb).
    2. Obter preço médio do m² de venda (via base VivaReal).
    3. **Cruzamento:** Relacionar as bases pela chave **"Bairro"**.
    4. *Fórmula:* `(Faturamento LTM / (Metragem * Preço m² Bairro)) * 100`.

    \

### **B. Refinamento de Dados (Filtros de Percentil)**

* **Problema:** Médias gerais escondem o potencial de imóveis de alta performance (Case Jurerê).
* **Ação \[Dev/BI\]:** Implementar **Seletores de Percentil**.
  * Criar filtro para alternar a visão: "Média Geral", "Top 25%" e "Top 10% (P90)".
  * *Objetivo:* Permitir que o vendedor simule cenários otimistas validados.

### **C. Aba "Dossiê do Spot" (KPIs Financeiros Consolidados)**

* **Ação \[Dev/BI\]:** Novos cartões de métricas anuais.
  * **Faturamento Médio Anual (LTM)** (Bruto e Líquido).
  * **Diária Média Anual**.
  * Manter "Diária Máxima" por enquanto.

### **D. Auditoria e Transparência (Drill-Through)**

* **Problema:** Comercial precisa "provar" os números (ex: comparar Garagem vs. Sem Garagem).
* **Ação \[Dev/BI\]:** Tabela de Listings Detalhada.
  * Exibir lista dos imóveis que compõem a seleção atual.
  * **Mandatório:** Incluir link clicável (URL Airbnb) para auditoria visual.

### **E. UX e Clareza**

* **Problema:** Confusão de termos ("Top 10" x "Top 10%").
* **Ação \[Dev/BI\]:**
  * Renomear visuais para **"Média Top 10% Estúdios"**.
  * Adicionar Tooltips explicando as regras de negócio nos Rankings.

### **F. Ajustes na "Evolução Temporal"**

* **Ação \[Dev/BI\]:**
  * Corrigir agregação da Ocupação (Média Mensal, não soma).
  * Exibir KPI lateral com a Soma Total do Faturamento no período.


---

## **3. Prioridade 2: Backlog & POC Futura (To-Do Later)**

*Itens estruturais para a Fase 2.*

### **A. POC: Seleção por Polígonos (Geo-Spatial)**

* **Contexto:** Resolver imprecisões de fronteiras de bairros (ex: Novo Campeche vs. Rio Tavares).
* **Desafio Futuro:** Ao mudar a seleção de "Bairro (Texto)" para "Polígono (Mapa)", o cruzamento atual do ROI (que usa nome do bairro) quebrará.
* **Ação:** Na Fase 2, precisaremos resolver a falta de Lat/Long na base VivaReal ou criar uma tabela de-para entre Polígonos e Preço m².

### **B. Filtros Avançados (Quadra do Mar)**

* **Status:** Dependente da POC de Polígonos.


---

## **4. Notas Técnicas**

* **Publicação Power BI:** Verificar erro no filtro de "Ano" que ocorre apenas no ambiente web (Service), mas funciona localmente.
* **Limitação de Dados:** Confirmado que a ausência de "Novo Campeche" é um dado da fonte (API). A solução via Polígonos (Fase 2) é a única correção definitiva; não aplicar correções manuais na base agora.


---

## **5. Cronograma da Reta Final**


1. **Imediato:** Kailany inicia cruzamento Airbnb x VivaReal (por Bairro) para gerar o **ROI**.
2. **Meio da Semana:** Implementação dos filtros de Percentil e Tabela de Links.
3. **Sexta-feira:** Validação final dos dados (ROI e Top 10%) contra a apresentação de referência.
4. **Entrega:** Versão 1.0 liberada.