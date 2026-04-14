<!-- title: [Vendas Spot] – Automação de Confirmação de Agendamento (via MIA) | url: https://outline.seazone.com.br/doc/vendas-spot-automacao-de-confirmacao-de-agendamento-via-mia-bTMQZ9CMda | area: Tecnologia -->

# [Vendas Spot] – Automação de Confirmação de Agendamento (via MIA)

**Status:**  Produção\n**Domínio:** Pipedrive → MIA → N8N\n**Timing:** 2 horas antes da reunião


---

## **Objetivo**

Confirmar automaticamente o compromisso/agendamento criado no Pipedrive para funil de **Vendas Spot**, disparando uma mensagem via **MIA (Morada)** no WhatsApp 2h antes da reunião.

Caso o cliente responda, a tratativa segue normalmente na MIA.


---

## **Quando é acionado**

O fluxo é disparado quando o Pipedrive gera uma Activity do tipo:

`Subject: Pré agendamento de compromisso Status: Scheduled (não concluído)`


---

## **Regras de negócio**

| Regra | Descrição |
|----|----|
| Identificação do gatilho | Activity com subject: `Pré agendamento de compromisso` |
| Funil | `Vendas Spot` (`pipeline_id = 28`) |
| Delay | Enviar mensagem `2h antes` da reunião |
| Template | `mia_fluxoconfirmacao_r` |
| Canal | WhatsApp (via MIA) |
| Fallback | Caso falhe → Cria nota no deal + notifica Slack |


---

## **Arquitetura do fluxo**

`Pipedrive Webhook → N8N → MIA Gateway → Pipedrive                         ↘ Slack (falha) `


---

## **Passo a passo do fluxo**

### **1. Trigger – Start (Webhook Pipedrive)**

Recebe o payload:

`{   "subject": "Pré agendamento de compromisso",   "due_date": "2026-01-07",   "due_time": { "value": "20:30:00" },   "deal_id": 217015 } `


---

### **Filter – Valida atividade**

Critérios:

✔ subject = "Pré agendamento de compromisso"\n✔ deal_id not empty\n✔ due_date not empty


---

### **Get Deal**

Busca dados complementares no Pipedrive:

* Título
* pipeline_id
* pessoa de contato
* telefone
* email
* empreendimento


---

**Set Date Time (Luxon)**

Converte horário UTC para Brazil e calcula horário de envio:

`activityDateTime = meeting at BR confirmationDateTime = meetingAtBR - 2h `


---

### **Wait Until Confirmation Reminder**

Suspende a execução até `confirmationDateTime`.

Ex: Reunião 17:30 → envio 15:30


---

### **6. Run Normalize Phone**

Subworkflow:

➡ Formata telefone para **E.164**\nEx: `+55xxxxxxxxxxx`


---

### **7. Select Template por Funil**

Para Vendas Spot → `mia_fluxoconfirmacao_r`

(Mapeado via `pipeline_id = 28`)


---

### **8. Send Notification (MIA)**

Chamada:

`POST /send-notification `

Body inclui:

* Deal Title
* Telephone
* Template
* Horário 17:30
* InstanceId 1292


---

### **9. Tratamento de Sucesso**

Se `response.success = true`:

✔ Cria Activity "Tentativa de confirmação via MIA"\n✔ Fecha activity como done\n✔ Cria **Note** no deal com link:

`Acesse a conversa aqui: https://app.morada.ai/conversations/<id> `


---

### **10. Tratamento de Falha**

Se `response.success = false`:

Cria note no deal:

`MIA ERROR - Falha no envio de confirmação `

Notifica no Slack (`#teste-automacao`)


---

## **Templates usados**

### **Vendas Spot**

`mia_fluxoconfirmacao_r `


---

## **Resultado Final no Deal**

### **Em caso de sucesso**

* Deal recebe nota
* Conversa aberta no WhatsApp (MIA)
* Activity marcada como done

### **Em caso de falha**

* Deal recebe alerta
* Slack recebe notificação


---

## **Debug & Monitoramento**

| Onde | O que verificar |
|----|----|
| N8N Executions | Erros e payload |
| MIA Logs | Response codes |
| Pipedrive Activities | Confirmações |
| Slack | Alertas de falha |


---


---