<!-- title: KPIs BU Comercial Automação | url: https://outline.seazone.com.br/doc/kpis-bu-comercial-automacao-eKXL35gXif | area: Tecnologia -->

# KPIs BU Comercial Automação

## Visão Geral

Esta automação coleta diariamente os KPIs do painel **KPIs - BU Comercial** do Pipefy e registra os valores em uma planilha do Google Sheets. A execução ocorre todos os dias às **06:00 da manhã** (horário de Brasília).


---

## Componentes

### Workflow n8n

* **Nome:** \[KPI\] Pipefy BU Comercial - Daily 6AM
* **Servidor:** [automation.seazone.com.br](https://automation.seazone.com.br/workflow/ZjqgrakA5xrej4ZS)
* **Status:** Published (ativo)
* **Trigger:** Schedule Trigger - diário às 6h

### Planilha Google Sheets

* **Nome:** KPIs - BU Comercial - Pipefy
* **URL:** [Abrir planilha](https://docs.google.com/spreadsheets/d/1witVFGwfiIGPN_Oo4llM_0nCgShEmS10Qp8NYALn66g/edit)

### Painel Pipefy

* **Pipe:** \[Tech\] Suporte BU Comercial (ID: 304437472)
* **Dashboard:** [KPIs - BU Comercial](https://app.pipefy.com/pipes/304437472/dashboards/164083)


---

## Arquitetura do Workflow

O workflow é composto por 4 nós executados em sequência:

### 1. Schedule Trigger

Dispara a execução diariamente às 06:00.

### 2. HTTP Request

Faz uma chamada POST à API GraphQL do Pipefy com queries que buscam:

* Todas as **fases do pipe** com contagem de cards
* Cards por **prioridade** (P0 a P4) via findCards
* Cards de **bugs** via findCards com filtro no campo categoria

**Autenticação:** Bearer Token (Personal Access Token do Pipefy).

### 3. Code (JavaScript)

Processa os dados e calcula os 15 KPIs. Faz chamadas HTTP adicionais para:

* Buscar **cards recentes** (allCards com filtro updated_at >= 30 dias)
* Buscar os **últimos 100 cards da fase Concluídas** (paginação 2x50)

### 4. Append or Update Row in Sheet

Escreve os valores na planilha Google Sheets, uma linha por KPI, com coluna nomeada pela data (ex: 21.mar.).


---

## Lista de KPIs Monitorados

| ID | KPI | Fonte de Dados |
|----|----|----|
| KPI001 | Solicitados Hoje | allCards filtro created_at = hoje |
| KPI002 | Em Atendimento | Fase Em atendimento (cards_count) |
| KPI003 | Abertos Agora P0 | findCards prioridade=P0-Highest |
| KPI004 | Abertos Agora P1 | findCards prioridade=P1-High |
| KPI005 | P0 últimos 30 dias | findCards P0 created_at <= 30d |
| KPI006 | P0 últimos 7 dias | findCards P0 created_at <= 7d |
| KPI007 | Concluídos 7 dias | Fase Concluídas finished_at <= 7d |
| KPI008 | Concluídos 30 dias | Fase Concluídas finished_at <= 30d |
| KPI009 | Abertos P2, P3 e P4 | findCards P2/P3/P4 fases abertas |
| KPI010 | Concluídos Hoje | Fase Concluídas finished_at = hoje |
| KPI011 | Tempo médio Atendimento | Não implementado |
| KPI012 | Tempo médio Jira P0/P1 | Não implementado |
| KPI013 | Tempo médio Jira P2 | Não implementado |
| KPI014 | Bugs em Produção | findCards categoria=Bug fases abertas |
| KPI015 | Escalados Automação | Fase Escalar Jira AUTOMAÇÃO |


---

## Fases Consideradas Abertas

* Caixa de entrada
* Triagem
* Priorização
* Em atendimento
* Escalar Jira SAPRON
* Escalar Time
* Necessário Investigação


---

## Credenciais

| Recurso | Credencial | Tipo |
|----|----|----|
| Pipefy API | Token n8n-kpi-bu-comercial | Bearer Token |
| Google Sheets | Sheets - Gerador de Códigos | OAuth2 |

> O token do Pipefy pode expirar. Gere um novo em app.pipefy.com/tokens e atualize no nó HTTP Request.


---

## Limitações Conhecidas


1. **Concluídos 7d/30d:** Pequena divergência possível pois a API retorna os últimos 100 cards da fase (2 páginas de 50).
2. **Tempo médio (KPI011-013):** Não implementado - requer cardPhaseHistory individual.
3. **Solicitados Hoje:** Limitado a 200 cards recentes via allCards.


---

## Manutenção

### Renovar Token Pipefy


1. Acesse app.pipefy.com/tokens
2. Gere novo token
3. No n8n: HTTP Request > Header Parameters > Value
4. Substitua por Bearer NOVO_TOKEN
5. Publique o workflow

### Adicionar novo KPI


1. Identifique fonte de dados
2. Adicione query findCards no HTTP Request (se necessário)
3. Adicione cálculo no Code node
4. Adicione ID no array ids e valor no array v
5. Adicione header na planilha


---

## Histórico

| Data | Alteração |
|----|----|
| 19/03/2026 | Criação inicial do workflow e planilha |
| 21/03/2026 | Migração para automation.seazone.com.br |
| 21/03/2026 | Fix: Acento em Concluídas (Concluídos 7d = 0) |
| 21/03/2026 | Fix: Paginação fase Concluídas (2x50 cards) |
| 21/03/2026 | Fix: Bugs em Produção usando campo categoria |