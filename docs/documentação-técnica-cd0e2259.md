<!-- title: Documentação Técnica | url: https://outline.seazone.com.br/doc/documentacao-tecnica-lYc4gDi4P7 | area: Tecnologia -->

# Documentação Técnica

## Sistema de Cadência Automática – MIA + Pipedrive + Baserow


---

# Visão Geral da Arquitetura

## 🔗 Workflows n8n

### 🔹 Trigger (Scheduler)

`https://n8n.seazone.com.br/workflow/t98qLYc10mdjCEOv `

Workflow responsável por:

* Buscar deals elegíveis
* Calcular idade
* Identificar step atual
* Definir se executa Step 1 ou Step N
* Chamar workflow principal

Base:

\[ TRIGGER \] Fluxo de Cadência


---

### 🔹 Fluxo Principal (Execução do Step)

`https://n8n.seazone.com.br/workflow/hwHHccoSwZQguk8S `

Workflow responsável por:

* Enviar mensagem via MIA
* Registrar step
* Criar atividade no Pipedrive
* Atualizar labels
* Controlar erro
* Registrar logs

Base:

\[MARKETING\] Fluxo de Cadência (…


---

# Bancos e Tabelas (Baserow)

Database: **MIA - Relação**

## 🗂 Tabelas

### tb_parametrizacao_cadencia (tableId 1360)

Define:

* pipeline_id
* tag
* se está ativa
* quantidade máxima de steps
* instance_id
* product_id

### tb_parametrizacao_cadencia (tableId 1361)

Define:

* template da mensagem por step
* tag
* step
* se está ativo

### tb_cadence_steps (tableId 1363)

Registra:

* deal_id
* step
* status (DONE / FAILED)
* erro (se houver)


---

# Fluxo Técnico Detalhado


---

## 🔄 TRIGGER – Execução a cada 30 minutos

Node: `Schedule Trigger`\nConfiguração:

`interval: 30 minutes `

Fluxo:


1. Busca deals via filtro Pipedrive (filter_id 395789)
2. Calcula idade do deal
3. Filtra deals > 1470 minutos (\~24h)
4. Busca parametrização da cadência
5. Busca último step executado
6. Decide:

| Caso | Ação |
|----|----|
| Não possui step | Executa Step 1 |
| Possui step e ainda não atingiu limite | Executa Step N+1 |
| Já atingiu limite | Marca cadência concluída |


---

## 🔁 Execução do Step (Workflow Principal)

Entrada:

`deal_id tag step instance_id product_id stage_id `


---

## 🔹 Validações iniciais

* Deal precisa estar status = open
* Se não estiver → cadência interrompida
* Registra STOP no Baserow
* Atualiza atividade como done


---

## 🔹 Definição do Template

Busca em:

`tb_cadence_steps `

Filtros:

* tag
* step
* active = true


---

## 🔹 Normalização de telefone

Subworkflow:

`[UTIL] Normalize Phone to E.164 `


---

## 🔹 Envio via MIA

Endpoint:

`https://mia-gateway.morada.ai/send-notification `

Body inclui:

* nome
* telefone normalizado
* email
* instanceId
* template
* parâmetros dinâmicos


---

## 🔹 Tratamento de erro

Se erro:

* Atualiza proprietário para Jennifer Correa
* Cria nota no deal
* Notifica Slack:

`#erros-mia `

* Registra FAILED no Baserow


---

## 🔹 Sucesso

Se sucesso:

* Registra conversationId
* Atualiza link da conversa no deal
* Cria nota com link Morada
* Cria próxima atividade
* Marca step como DONE no Baserow


---

# Controle de Estados

## Status possíveis no Baserow

| Status | Significado |
|----|----|
| DONE | Step executado com sucesso |
| FAILED | Erro no envio |
| STOPPED | Deal não elegível |


---

 Regras de Negócio

## Deal elegível se:

* status = open
* idade > 1470 minutos
* não atingiu limite de steps
* não mudou stage
* não foi lost


---

# Controle de Labels

IDs envolvidos:

| ID | Significado |
|----|----|
| 4651 | Em cadência |
| 4659 | Cadência concluída |

Fluxo remove 4651 e adiciona 4659 ao concluir.


---

# Logs e Auditoria

* Execução salva ID do workflow:

`https://workflows.seazone.com.br/workflow/{{workflow_id}}/executions/{{execution_id}} `

* Slack alerta erros
* Baserow registra execução
* Nota no Pipedrive registra conversa