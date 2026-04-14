<!-- title: GUIA DO USUÁRIO | url: https://outline.seazone.com.br/doc/guia-do-usuario-nVT8G28rDi | area: Tecnologia -->

# GUIA DO USUÁRIO

Este fluxo envia automaticamente uma **mensagem de confirmação de reunião** ao cliente via MIA (WhatsApp) pouco antes da reunião acontecer.

O objetivo é:

✔ reduzir não comparecimentos (no-show)\n✔ melhorar conversão\n✔ automatizar comunicação pré-reunião\n✔ manter histórico direto no CRM (Pipedrive)


---

## **Quando acontece**

O envio é feito **2 horas antes** da reunião marcada no Pipedrive.

> Exemplo: reunião às **16:00** → mensagem enviada às **14:00**

Não é necessário nenhuma ação manual do usuário.


---

## **Condições para o envio**

O envio acontece automaticamente apenas quando:

✔ existe um **pré-agendamento** registrado no Pipedrive\n✔ existe **data e horário** da reunião\n✔ existe **pessoa de contato com telefone**\n✔ o evento está **aberto**\n✔ o proprietário do deal é válido\n✔ o deal não está filtrado por exceção


---

##  **O que o vendedor vê no Pipedrive**

Após o envio da mensagem:

### 1) **Uma atividade é criada automaticamente**

Nome:

> **Tentativa de confirmação via MIA**

Status: **Concluída**

Tipo: **WhatsApp Chat**


---

### 2) **Uma nota é adicionada ao deal**

Conteúdo da nota:

> "Confirmação de reunião enviada via Morada - MIA\nAcesse a conversa: https://app.morada.ai/conversations/XXXXX"

Essa nota contém:

✔ link da conversa\n✔ registro de horário\n✔ auditabilidade


---

## **O que o cliente recebe**

O cliente recebe mensagem via WhatsApp com:

✔ nome da reunião / unidade / empreendimento\n✔ horário da reunião\n✔ identificação da empresa\n✔ template adequado à vertical


---

## **Quando o fluxo não envia a mensagem**

O fluxo **não envia** se faltar alguma das informações mínimas:

| Motivo | Consequência |
|----|----|
| sem horário | sem envio |
| sem data | sem envio |
| sem telefone | sem envio |
| não é "pré-agendamento" | ignorado |
| proprietário filtrado | ignorado |
| já executado | não duplica |

O usuário não é notificado nesses casos — pois é comportamento esperado.


---

## **Se ocorrer erro no envio**

Se o MIA retornar erro:


1. uma nota é criada no deal:

> ❌ MIA ERROR\nFalha ao enviar confirmação automática\n(com dados do deal)


2. é enviado um alerta no Slack para o time responsável

Então o vendedor pode:

✔ tentar contatar manualmente\n✔ reagendar se necessário


---

## **Benefícios para o vendedor**

✔ não precisa mais enviar mensagens manuais\n✔ não precisa lembrar do horário\n✔ não precisa criar atividades\n✔ não precisa logar histórico\n✔ reduz no-show\n✔ histórico centralizado no CRM


---

## **Benefícios para gestão**

✔ rastreável\n✔ auditável\n✔ padronizado\n✔ escalável\n✔ replicável\n✔ mede eficiência por vendedor, equipe e funil


---

## **O que o vendedor precisa fazer**

Nada.

O processo é 100% automatizado.


---

## **O que o vendedor pode fazer se quiser**

Opcionalmente o vendedor pode:

* verificar a conversa no MIA
* checar se cliente confirmou
* ajustar a reunião caso necessário


---

# **Resumo rápido**

> **Se existe reunião → 2h antes → cliente recebe mensagem automática → CRM registra → vendedor não precisa lembrar**