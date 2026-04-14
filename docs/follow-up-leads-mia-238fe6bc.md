<!-- title: Follow-up Leads MIA | url: https://outline.seazone.com.br/doc/follow-up-leads-mia-jpdMkRqj7n | area: Tecnologia -->

# Follow-up Leads MIA

# 📌 Cadência de Leads (Pipedrive + n8n + Supabase)

## 1. Visão Geral

Este sistema implementa uma **cadência automatizada de contatos** para negócios do Pipedrive, garantindo:

* Controle de concorrência (um negócio não executa dois passos ao mesmo tempo)
* Persistência de estado (cadência sobrevive a falhas, retries e reprocessamentos)
* Auditoria completa (status de cada step, erros, horários, tentativas)
* Integração clara entre **CRM (Pipedrive)**, **Orquestração (n8n)** e **Estado/Lock (Supabase)**

### 🔑 Ponto-chave

> **Quem dispara o fluxo é o Pipedrive**, não o n8n.

O n8n **não cria a primeira atividade**, ele **recebe o contexto já criado** pelo Pipedrive e passa a **orquestrar os próximos passos da cadência**.


---

## 2. Quem inicia tudo: Automação do Pipedrive

### 📍 Automação no Pipedrive (gatilho real)

No Pipedrive existe uma automação configurada com o seguinte comportamento:


1. **Gatilho**
   * Quando um **negócio é criado** em Vendas Spot e o criador é MIA
2. **Atrasar por 24 horas**
3. **Condições** valida novamente as condições do negócio após as 24 horas:
   * Funil específico (ex: *Vendas Spot*)
   * Criador do negócio **≠ MIA**
   * Negócio em status aberto
   * Etapa específica (ex: *Lead In*)
4. **Ação 1 — Criar atividade**
   * Tipo: WhatsApp chat
   * Assunto: *1ª tentativa de contato pela MIA*
   * Data: no mesmo dia
   * Timezone: America/Sao_Paulo

> 👉 **Essa atividade já nasce no Pipedrive**


4. **Ação 2 — Webhook**
   * Envia para o n8n:

     ```json
     {
       "deal_id": "ID do negócio",
       "activity_id": "ID da atividade criada",
       "vertical": "szi_lancamento"
     }
     ```

📌 **Conclusão**

> O Pipedrive cria o contexto inicial. O n8n apenas continua a cadência com segurança.


---

## 3. Visão Macro do Sistema (Arquitetura)

```mermaidjs

flowchart LR
    Pipedrive -->|Webhook| Orchestrator
    Orchestrator -->|Lock / State| Supabase
    Orchestrator -->|Executa| SubWorkflow
    SubWorkflow -->|Atualiza| Pipedrive
    SubWorkflow -->|Atualiza| Supabase
```


---

## 4. Orchestrator — Visão Geral

O **Orchestrator** é responsável por:

* Validar se o Deal **ainda pode** seguir a cadência
* Garantir **lock exclusivo**
* Executar **um único step por vez**
* Encerrar corretamente quando necessário


---

## 5. Orchestrator

### 🔹 Start

Recebe o webhook do Pipedrive com:

* `deal_id`
* `activity_id`
* `vertical`


---

### 🔹 Get Deal

Busca o negócio atualizado no Pipedrive.

**Por quê?** O negócio pode ter mudado desde a criação da atividade:

* Pode ter sido ganho
* Perdido
* Reatribuído
* Qualificado manualmente


---

### 🔹 Conditions

Normaliza e calcula flags internas:

* `is_open`
* `is_lost`
* `is_qualified`
* `owner_is_mia`


---

### 🔹 Stop conditions?

Decide se a cadência **deve parar antes de começar**.

#### Exemplos:

* Deal já foi qualificado → **STOPPED**
* Deal foi perdido → **STOPPED**
* Owner mudou para humano → **STOPPED**

➡️ Se **não passar**, encerra sem executar step algum.


---

### 🔹 Load Cadence Config

Busca no Supabase a configuração da cadência:

* Steps
* `wait_hours`
* `max_attempts`
* Templates


---

### 🔹 RPC Acquire Cadence Lock

Tenta adquirir um **lock exclusivo** para esse deal.

**Exemplo real:**

> Dois eventos chegam quase juntos (retry, webhook duplicado). Só um pode continuar.


---

### 🔹 Lock acquired?

* ❌ Não → encerra (`End Locked`)
* ✅ Sim → executa o SubWorkflow


---

### 🔹 Execute Step (Subworkflow)

Chama o fluxo responsável por **executar exatamente um step da cadência**.


---

## 6. SubWorkflow — Visão Geral

O SubWorkflow executa **um passo da cadência** com garantia de consistência:

* Envio da MIA
* Atualização do Pipedrive
* Atualização do Supabase
* Decisão: continuar ou encerrar


---

## 7. SubWorkflow — Fluxo Principal (Sucesso)

### 🔹 Load Cadence Config

Carrega novamente a config (imutável, segura).


---

### 🔹 Normalized Phone

Padroniza telefone para envio WhatsApp.


---

### 🔹 MIA Send Notification

Dispara a mensagem via MIA.


---

### 🔹 MIA Success?

* ❌ Falhou → fluxo de erro
* ✅ Sucesso → continua


---

### 🔹 Update Label (Pipedrive)

Atualiza labels/flags visuais do Deal.


---

### 🔹 Add Note in Deal

Registra:

* Step executado
* Template
* Horário
* Message ID


---

### 🔹 Complete last activity

Finaliza a atividade criada pelo Pipedrive (evita pendência).


---

### 🔹 mark_cadence_step (DONE)

Registra no Supabase:

* Step concluído
* Timestamp
* Payload relevante


---

### 🔹 has next step?

* ❌ Não → finaliza cadência
* ✅ Sim → agenda próximo


---

### 🔹 Create Next Activity

Cria a próxima atividade no Pipedrive.


---

### 🔹 Wait until next_run_at

Aguarda o tempo configurado (`wait_hours`).


---

### 🔹 Execute Workflow (loop)

Chama novamente o SubWorkflow para o próximo step.


---

## 8. SubWorkflow — Falha da MIA

### O que acontece quando a MIA falha?

```text

MIA falhou
↓
Step marcado como FAILED
↓
Run marcado como ERROR
↓
Lock liberado
↓
Deal anotado
↓
Alerta enviado
```

### RPCs executadas


1. **mark_cadence_step → FAILED**
2. **update_cadence_run → ERROR**
3. **release_cadence_lock**

📌 Isso **não quebra reprocessamento**.

👉 Um operador pode:

* Corrigir problema
* Reexecutar manualmente o SubWorkflow
* Cadência continua do ponto certo


---

## 9. SubWorkflow — STOPPED (Deal não atende condições)

Quando o Deal:

* Já foi qualificado
* Mudou de dono
* Saiu da etapa

### Ações:


1. `update_cadence_run → STOPPED`
2. `release_cadence_lock`
3. Add Note: *Cadência interrompida*
4. Finaliza atividade atual


---

## 10. Supabase RPCs

### 🔹 acquire_cadence_lock

> "Reserva" o Deal para um único processo.

* Evita execução dupla
* Usa timestamp (`lock_until`)
* Seguro contra concorrência


---

### 🔹 release_cadence_lock

> Libera o Deal para novos processos.

* Chamado em:
  * DONE
  * ERROR
  * STOPPED


---

### 🔹 mark_cadence_step

> Marca o status de **um passo específico**.

Status possíveis:

* `DONE`
* `FAILED`


---

### 🔹 update_cadence_run

> Atualiza o **estado geral da cadência**.

Estados:

* `RUNNING`
* `DONE`
* `STOPPED`
* `ERROR`


---

## 11. Diagramas

### 📌 Orchestrator

```mermaidjs

flowchart TD
    A[Pipedrive Webhook] --> B[Get Deal]
    B --> C[Check Conditions]
    C -->|STOP| Z[End Stopped]
    C -->|OK| D[Acquire Lock]
    D -->|Locked| E[Execute Step]
    D -->|Busy| Y[End Locked]
```


---

### 📌 SubWorkflow

```mermaidjs

flowchart TD
    A[Load Config] --> B[Send MIA]
    B -->|Fail| F[Mark FAILED]
    B -->|Success| C[Update Deal]
    C --> D[Mark Step DONE]
    D --> E{Has Next Step?}
    E -->|No| G[Finish Run]
    E -->|Yes| H[Schedule Next]
```


---

## 12. Conclusão

Esse desenho garante:

* 🔒 Segurança de execução
* 🔁 Reprocessamento manual seguro
* 📊 Auditoria total
* 🧠 Separação clara de responsabilidades
* 🔧 Evolução simples (novos canais, novos steps)