<!-- title: Sprint SAP Automação | url: https://outline.seazone.com.br/doc/sprint-sap-automacao-BPkqTAshW7 | area: Tecnologia -->

# Sprint SAP Automação

## Objetivo

Automatizar o acompanhamento da Saude do Sprint da equipe Sapron Delivery (Wallet de Investidores), registrando semanalmente os dados de progresso de cada sprint em uma planilha Google Sheets, similar ao modelo de KPIs do Pipefy.


---

## Recursos Criados

### 1. Planilha Google Sheets

**Link:** [Saude do Sprint - Sapron Delivery](https://docs.google.com/spreadsheets/d/1E_5CHLDjHM7l6JhxFUtCKbUEOR643HxEpEa_8IIgnsI)

A planilha possui 3 abas:

#### Aba "Dashboard"

Visao geral consolidada de todas as sprints com as seguintes colunas:

* **Sprint** - Identificador (ex: SAP 100)
* **Inicio / Fim** - Datas de inicio e encerramento
* **Status** - FECHADA ou ATIVA
* **SP Comprometidos** - Total de Story Points comprometidos
* **SP Concluidos / Nao Concluidos / Removidos** - Breakdown dos Story Points
* **% Conclusao SP** - Percentual de conclusao
* **Issues Concluidas / Nao Concluidas / Removidas / Adicionadas** - Contagem de issues
* **Velocidade (SP)** - Story Points concluidos
* **Saude** - Indicador visual com cores:
  * SAUDAVEL (verde) - >= 80% de conclusao
  * ATENCAO (amarelo) - entre 50% e 79%
  * CRITICA (vermelho) - abaixo de 50%
  * EM ANDAMENTO (azul) - sprint ativa

#### Aba "Metricas"

Metricas consolidadas:

* Velocidade Media: 7.2 SP/Sprint
* Taxa Media de Conclusao: 45.7%
* Issues Concluidas por Sprint (media): 12.8
* Graficos de velocidade e taxa de conclusao

#### Aba "DadosBrutos"

Dados detalhados para integracao com N8N contendo todas as metricas brutas de cada sprint.


---

### 2. Dados Retroativos

Foram coletados dados das ultimas 20 sprints (SAP 100 a SAP 119) via API REST do Jira.

**APIs Utilizadas:**

* `/rest/agile/1.0/board/3/sprint` - Listar sprints do board Sapron Delivery (Board ID: 3)
* `/rest/greenhopper/1.0/rapid/charts/sprintreport?rapidViewId=3&sprintId={id}` - Relatorio detalhado de cada sprint

| Sprint | ID Jira | Periodo | SP Comprom. | SP Concl. | % Conclusao | Saude |
|----|----|----|----|----|----|----|
| SAP 100 | 2413 | 23/10 - 30/10/25 | 13 | 8 | 62% | ATENCAO |
| SAP 101 | 2446 | 30/10 - 06/11/25 | 23 | 6 | 26% | CRITICA |
| SAP 102 | 2611 | 06/11 - 13/11/25 | 31 | 27 | 87% | SAUDAVEL |
| SAP 103 | 2612 | 13/11 - 19/11/25 | 15 | 7 | 47% | CRITICA |
| SAP 104 | 2710 | 19/11 - 27/11/25 | 14 | 8 | 57% | ATENCAO |
| SAP 105 | 2842 | 27/11 - 04/12/25 | 6 | 1 | 17% | CRITICA |
| SAP 106 | 3009 | 04/12 - 11/12/25 | 11 | 6 | 55% | ATENCAO |
| SAP 107 | 3076 | 11/12 - 18/12/25 | 11 | 2 | 18% | CRITICA |
| SAP 108 | 3143 | 18/12 - 08/01/26 | 19 | 9 | 47% | CRITICA |
| SAP 109 | 3176 | 08/01 - 15/01/26 | 10 | 5 | 50% | ATENCAO |
| SAP 110 | 3375 | 15/01 - 22/01/26 | 5 | 5 | 100% | SAUDAVEL |
| SAP 111 | 3408 | 22/01 - 29/01/26 | 0 | 0 | 0% | CRITICA |
| SAP 112 | 3639 | 29/01 - 05/02/26 | 1 | 1 | 100% | SAUDAVEL |
| SAP 113 | 3672 | 05/02 - 12/02/26 | 2 | 0 | 0% | CRITICA |
| SAP 114 | 3772 | 12/02 - 19/02/26 | 2 | 0 | 0% | CRITICA |
| SAP 115 | 3904 | 19/02 - 26/02/26 | 15 | 7 | 47% | CRITICA |
| SAP 116 | 4003 | 26/02 - 05/03/26 | 13 | 8 | 62% | ATENCAO |
| SAP 117 | 4036 | 05/03 - 12/03/26 | 50 | 18 | 36% | CRITICA |
| SAP 118 | 4342 | 12/03 - 19/03/26 | 33.5 | 19.5 | 58% | ATENCAO |
| SAP 119 | 4375 | 19/03 - 26/03/26 | 26 | 14 | 54% | EM ANDAMENTO |


---

### 3. Apps Script

Script vinculado a planilha (acessar via Extensoes > Apps Script) que:

* Cria as 3 abas (Dashboard, Metricas, DadosBrutos)
* Popula dados retroativos das 20 sprints
* Aplica formatacao condicional (cores na coluna Saude)
* Gera graficos de velocidade e taxa de conclusao


---

### 4. Workflow N8N

**Nome:** \[KPI\] Saude Sprint - Sapron Delivery **Arquivo JSON:** `n8n_workflow_sprint_health.json` (salvo em Documentos/Claude)

#### Fluxo:

```
Toda Sexta 19h > Buscar Sprints Recentes > Extrair Ultima Sprint > Buscar Sprint Report > Processar Dados > Gravar no Google Sheets
```

#### Nodes:


1. **Schedule Trigger** - Toda sexta-feira as 19h
2. **HTTP Request (Buscar Sprints)** - GET `/rest/agile/1.0/board/3/sprint?state=active,closed&maxResults=5` com Basic Auth
3. **Code (Extrair Sprint)** - Filtra a ultima sprint fechada e extrai o sprintId
4. **HTTP Request (Sprint Report)** - GET `/rest/greenhopper/1.0/rapid/charts/sprintreport?rapidViewId=3&sprintId={id}`
5. **Code (Processar)** - Calcula SP, issues, % conclusao e indicador de saude
6. **Google Sheets (Gravar)** - Append na aba DadosBrutos da planilha


---

## Configuracao do N8N (Pendente)

Para ativar o workflow:


1. **Importar** o arquivo JSON no N8N (Menu ... > Import from File)
2. **Criar credencial HTTP Basic Auth** para o Jira:
   * User: email do Jira 
   * Password: API Token (gerar em id.atlassian.com > Security > API Tokens)
3. **Configurar credencial Google Sheets** nos nodes (usar credencial existente "Criacao de Anuncios / Gerador de Codigos")
4. **Publicar** o workflow


---

## Informacoes Tecnicas

| Item | Valor |
|----|----|
| Board Jira | Sapron Delivery Board (ID: 3) |
| Projeto Jira | Sapron Delivery (SAP) |
| Sprint Atual | SAP 119 (ativa em 23/03/2026) |
| Planilha ID | 1E_5CHLDjHM7l6JhxFUtCKbUEOR643HxEpEa_8IIgnsI |
| Aba DadosBrutos GID | 63684000 |
| Dashboard Jira | BU Comercial II (ID: 10291) |
| Frequencia | Semanal (sexta-feira 19h) |
| Periodo Retroativo | SAP 100 a SAP 119 |


---

## Observacoes

* O `startAt` no node de busca pode precisar de ajuste conforme novas sprints forem criadas.
* Algumas sprints possuem 0 SP comprometidos (sem estimativa de Story Points naquela sprint).
* Os dados utilizam as estimativas oficiais do Sprint Report do Jira.
* A sprint SAP 119 estava ativa no momento da coleta (23/03/2026).