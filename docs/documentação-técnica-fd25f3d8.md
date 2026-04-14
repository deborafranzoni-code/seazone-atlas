<!-- title: DOCUMENTAÇÃO TÉCNICA | url: https://outline.seazone.com.br/doc/documentacao-tecnica-C7a2u5hlO8 | area: Tecnologia -->

# DOCUMENTAÇÃO TÉCNICA

### **Nome do Fluxo**

> **\[HYPER\] Recuperação de No-Show**
>
> Link:  <https://workflows.seazone.com.br/workflow/lVdTy69AVwJO7YsO>

### **Objetivo**

Automatizar o processo de recuperação de reuniões não comparecidas ("no-show"), enviando mensagem automática via MIA e registrando o resultado no Pipedrive para continuidade da cadência comercial.

### **Contexto**

O fluxo é acionado automaticamente pelo **webhook do Pipedrive** quando um deal entra no estágio de pré-agendamento e possui indicação de no-show.

### **Eventos de Entrada**

| Origem | Tipo | Descrição |
|----|----|----|
| Pipedrive | Webhook | `pipedrive-no-show` contendo IDs e dados do deal |

Trecho do JSON recebido:\n*(resumido para campos relevantes)*

`{   "data": {     "id": 218829,     "stage_id": 340,     "status": "open"   },   "meta": {     "action": "change",     "type": "general"   } } `

### **Regras de Disparo**

O fluxo só continua quando:

* `next_activity.subject == "Pré agendamento de compromisso"`
* `status == "open"`
* `subject != "Tentativa de recuperação de no-show"`
* `stage_id == 340`

Conforme o nó **Filter pré agendamento**

\[ HYPER \] Recuperação de No Show

### **Processo (Pipeline)**

#### **1. Webhook**

* Node: **Start**
* Método: `POST`
* Endpoint: `/pipedrive-no-show`

#### **2. Enriquecimento do contexto**

* Node: **Get a deal**
* Ação: consulta o deal no Pipedrive via API

#### **3. Cálculo de data da próxima tentativa**

* Node: **Próximo dia útil**
* Lógica:
  * soma 1 dia
  * ajusta sábado → +2 dias
  * ajusta domingo → +1 dia
  * define horário fixo `10:00`

Trecho presente no JSON:

`` item.json.activityDateTime = `${dateStr}T10:00:00`;  ``

#### **4. Espera (Delay Programado)**

* Node: **Wait Until Confirmation Reminder**
* Aguarda até a data calculada

#### **5. Normalização de Telefone**

* Node: **Run Normalize Phone**
* Chama workflow utilitário `[UTIL] Normalize Phone to E.164`

#### **6. Envio da mensagem via MIA**

* Node: **MIA Send Notification**
* Endpoint: `POST https://mia-gateway.morada.ai/send-notification`
* Payload inclui:
  * título da reunião
  * telefone normalizado
  * scheduled time
  * template: `mia_fluxonoshow_r`

Se sucesso → JSON contém `success: true`

#### **7. Registro do Resultado**

| Condição | Ação |
|----|----|
| **success == true** | Cria atividade + adiciona nota no Pipedrive |
| **failure** | Adiciona nota de erro + envia alerta no Slack |

Conforme nodes:

* **Create and Done Activity - Tentativa Confirmação**
* **Add Note - Success**
* **Add Note - Failure MIA**
* **Send Slack Notification**

#### **8. Finalização**

Nenhum output externo. O fluxo encerra.


---

### **Lógica de Rebote (fallback)**

Caso o MIA falhe:

* O deal não avança
* O vendedor é alertado via Slack
* Auditor habilitada via `note` no deal


---

### **Dependências do Sistema**

| Componente | Função |
|----|----|
| Pipedrive | Origem das atividades + CRM |
| n8n | Orquestrador |
| MIA | Motor de mensagens |
| Slack | Notificação |
| Workflow UTIL | Normalização de telefone |


---

### **Erros Possíveis**

| Caso | Detecção | Consequência |
|----|----|----|
| MIA indisponível | status != success | deal fica sem tentativa automatizada |
| Telefone inválido | MIA rejeita | Alerta Slack |
| Falha Pipedrive | API error | Fluxo aborta |
| Data nula | Node retorna `null` | Fluxo não tenta |


---

### **Escalabilidade**

O fluxo é **idempotente** (não duplica ações) e **stateless** (estado no Pipedrive).

Logs ficam em:

> Pipedrive → Atividades + Notas\nSlack → Canal `#teste-automacao`