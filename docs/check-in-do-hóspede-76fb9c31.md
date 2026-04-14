<!-- title: Check-in do Hóspede | url: https://outline.seazone.com.br/doc/check-in-do-hospede-h8GLAeggXA | area: Tecnologia -->

# Check-in do Hóspede

PRD — Sistema de Check-in Digital\n**Objetivo Estratégico:**\nGarantir um processo de check-in digital padronizado, seguro e automatizado, reduzindo fricção operacional da franquia e aumentando compliance documental e previsibilidade de chegada do hóspede.


---

#  Fluxo 1 — Check-in do Hóspede

## 1. Objetivos do Fluxo do Hóspede

* Coletar dados obrigatórios para compliance legal.
* Antecipar informações logísticas.
* Reduzir contato manual da franquia.
* Garantir validação documental e rastreabilidade.
* Antecipar previsibilidade de horário de chegada.


---

## 1.2 Disparo de Comunicação

### Regra de Envio

* **3 dias antes da data de check-in:** envio automático da mensagem com link do formulário.
* **Se a reserva for criada com menos de 3 dias de antecedência:** envio imediato após confirmação da reserva.

### Canal

* WhatsApp - NewByte


---

## Identificação de Hóspede Recorrente

### Fonte de Dados

A verificação deve ocorrer no momento do disparo da mensagem de pré-check-in, utilizando os dados recebidos via integração com o **Channel Manager**.

Campos recebidos do Channel Manager:

* Documento (quando disponível)
* Telefone
* E-mail
* Nome


---

## Regra de Identificação

No momento da criação da reserva ou no disparo da mensagem (o que ocorrer primeiro), o sistema deve:


1. Consultar a base interna de hóspedes.
2. Realizar matching com base nos seguintes critérios (ordem de prioridade):

### Critério 1 — Documento (match exato)

Se o documento recebido for idêntico a um documento existente → considerar hóspede recorrente.

### Critério 2 — E-mail (match exato)

Caso não haja documento, verificar e-mail.

### Critério 3 — Telefone (match exato com normalização)



---

## Resultado da Verificação

A reserva deve receber um dos seguintes flags internos:

* `guest_status = recorrente`
* `guest_status = novo`

Essa informação deve estar disponível para:

* Interface da franquia
* Logs do sistema
* Analytics


---

## Comportamento ao Acessar o Link

Quando o hóspede clicar no link de check-in:

###  Se for identificado como recorrente:

O sistema deve:


1. Exibir mensagem clara no topo da tela:

> "Identificamos que você já se hospedou conosco anteriormente."


2. Informar que seus dados já estão cadastrados.
3. Exibir os dados previamente salvos para revisão.
4. Permitir:
   * Confirmar e seguir
   * Editar qualquer informação antes de confirmar

Importante:

* Mesmo sendo recorrente, o hóspede deve confirmar explicitamente os dados antes de avançar.
* Caso haja atualização, salvar nova versão com log.


---

### Se NÃO for recorrente:

O fluxo segue normalmente para preenchimento completo do cadastro.


---

## Regras de Segurança

* Nunca exibir documento completo (mostrar parcialmente mascarado, ex: \***.123.456-**).
* Selfie não deve ser exibida automaticamente — apenas indicação de que já foi validada anteriormente.
* Alterações devem gerar histórico versionado.


---

## Etapa 2 — Dados do Hóspede Principal

Campos obrigatórios:

* Nome
* E-mail
* Cidade de origem
* Motivo da viagem
* Documento
* Foto do documento (frente)
* Foto do documento (verso)
* Selfie 

Validações:

* Upload obrigatório


---

## Etapa 3 — Dados dos Demais Hóspedes

Para cada hóspede adicional:

Campos obrigatórios:

* Nome
* Documento
* Foto do documento (frente)
* Foto do documento (verso)

Funcionalidade obrigatória:

* O hóspede principal pode:
  * Preencher manualmente
  * Compartilhar link individual para que cada hóspede preencha seus próprios dados

Regra:

* O check-in só poderá ser considerado completo quando todos os hóspedes estiverem com documentação validada.


---

## Etapa 4 — Informações Logísticas

Campos obrigatórios:

### Veículo

* Vai de carro? (Sim/Não)
* Se Sim:
  * Modelo
  * Placa

### Pet

* Vai levar pet? (Sim/Não)


---

## Etapa 5 — Horário de Chegada

Campo obrigatório:

* Horário desejado de chegada (com precisão até o minuto)

Regras:

* Deve permitir horário após 00h do dia seguinte.
* Pode incluir horários até o último dia da reserva.
* Deve ser possível editar a qualquer momento antes do check-in.
* Registro de log de alterações de horário.

Objetivo:

* Permitir planejamento operacional da franquia.


---

## Finalização do Pré-Check-in

Após completar todas as etapas:

* Status da reserva muda para: **Check-in preenchido**


---

##