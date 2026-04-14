<!-- title: Automatizar Abordagem de Cancelamentos de Reservas | url: https://outline.seazone.com.br/doc/automatizar-abordagem-de-cancelamentos-de-reservas-56COb294GK | area: Tecnologia -->

# 🚫 Automatizar Abordagem de Cancelamentos de Reservas

## **Objetivo**

Automatizar abordagem de clientes que cancelaram suas reservas em outras OTAs na tentativa de reverter o cancelamento oferecendo-os para reservar em nosso site de reservas próprio por um valor menor.

Isso é uma tentativa de reverter o cancelamento e trazer mais pessoas para comprar diretamente pelo nosso site ao invés de comprar pela OTA.


## **Regras**


1. **Não enviar** notificação para hóspede em que **houve cancelamento manual**.\n*Para esta regra, vamos consultar o [pipefy](https://app.pipefy.com/pipes/303828070) via API. Se a reserva cancelada estiver na coluna **"Finalizado"**, não devemos notificar pois significa que foi cancelamento manual (pelo time de atendimento).*
2. **Não enviar** notificação para **cancelamento de pré-reserva** (regra específica do website)

   *Pré-reservas do Website que são canceladas vem com o* `*cancelMessage*`*: "reservation expired" ou "reservation expired (canceled to recreate)".*
3. ==Para usuários que não tem número de telefone cadastrado: ***<descrever aqui como lidar>***==
4. Não é necessário ser em *tempo real.*


:::info
*Prioridade é funcionar para o Booking*

Tentar melhorar alerta de cancelamento de reservas atual: Não precisamos notificar se foi um cancelamento manual. A verificação no Pipefy resolve esse caso.

:::


## Proposta de Solução

Ao receber o webhook da Stays notificando um cancelamento, vamos disparar uma **task do Celery** (a ser criada) que fará algumas validações iniciais (com base nas regras mencionada) e também verificar se a reserva foi cancelada manualmente pelo atendimento, e caso seja uma reserva válida dispara uma outra task do Celery (a ser criada) para notificar.

### Verificando se devemos acionar o fluxo para uma determinada reserva

#### Validações básicas

* Verificar se hóspede possui número de telefone cadastrado: Caso não possua, abortar fluxo e printar nos logs.
* Verificar se a reserva é uma pre-reserva cancelada: Caso seja, abortar o fluxo.
* \

#### Validar se reserva foi cancelada manualmente pelo atendimento 

Para realizar essa validação, vamos precisar verificar no Pipefy se há registro dessa reserva e que tenha a tag/label "Cancelamento de Reserva". No pipefy os cards de cancelamento carrega o ~~ID externo da reserva como atributo, portanto, é por meio desse campo que vamos fazer o match com a reserva do nosso lado.~~ Foi criado um campo novo **<nome_aqui>** que contem o stays_reservation_code para que possamos usá-lo para encontrar o card da reserva.


Para isso vamos precisar:


1. Enviar requisição para API do Pipefy\n*No código já está configurado uma factory para a API do Pipefy, basta reutilizar. No código já há uma classe que implementa uma integração com o Pipefy. O Pipefy utiliza **Graphql** para obter as informações. O retorno é no formato de JSON, trazendo os dados requisitados no payload.*

   
:::warning
   Esta atividade depende que o time de atendimento crie o campo personalizado com ID Stays da Reserva para que possamos obter o card da reserva corretamente. O campo `c_digo_da_reserva_stays` abaixo ainda não é o oficial.

   :::

   ```graphql
   # POST https://app.pipefy.com/graphql
   query searchReservationCanceledCardsByField {
     findCards(
       pipeId: 303828070 # [ATE] PIPE 1 - Solicitação ao Atendimento
       search: {fieldId: "c_digo_da_reserva_stays", fieldValue: "<stays_reservation_code>"}
     ) {
       pageInfo {
         endCursor
         startCursor
         hasNextPage
       }
       nodes {
         id
         title
         done
         updated_at
         current_phase {
           id
           name
         }
         pipe {
           id
           name
         }
         labels {
           id
           name
         }
         fields {
           name
           value
           phase_field {
             id
           }
         }     
       }
     }
   }
   
   ```

   Essa requisição irá trazer uma lista de cards (chave "nodes") que contém os cards com o código informado.

   ```json
   // Exemplo de Response
   {
     "data": {
       "findCards": {
         "pageInfo": {
           "endCursor": "WyIzMTQyLjAiLDEyOTQ3NTIzOTdd",
           "startCursor": "WyIzMTQyLjAiLDEyOTQ3NTIzOTdd",
           "hasNextPage": false
         },
         "nodes": [ // lista de cards; cada dicionário da lista é um card
           {
             "id": "1294752397",
             "title": "SAA0907 ",
             "done": true,
             "updated_at": "2026-02-07T20:15:00Z",
             "current_phase": {
               "id": "323314380",
               "name": "Finalizado" // Card precisa estar nesta Fase
             },
             "pipe": {
               "id": "303828070",
               "name": "[ATE] PIPE 1 - Solicitação ao Atendimento" // Pipe do card precisa ser este
             },
             "labels": [
               {
                 "id": "310239937",
                 "name": "Cancelamento de Reserva" // essa é a label que precisamos verificar a existência
               },
               // outras labels...
             ],
             "fields": [
               // outros campos ...
               {
                 "name": "Código da reserva",
                 "value": "HMWHPCFJHY"
                 "phase_field": {
                   "id": "c_digo_da_reserva" // mesmo ID usado no filtro
                 }
               },
               // outros campos...
             ]
           }
         ]
       }
     }
   }
   ```
2. Verificar se para os nodes retornados (usar um *for-loop* por precaução), há algum que possui a `label.name` "Cancelamento de Reserva" e a `current_phase.name` é **"Finalizado"**.\n*Talvez olhar pelo ID seja o mais ideal pelo fato de o ID ser único, já o nome pode ser editado.*

   
   1. **Pipe desejado**:   `name: "[ATE] PIPE 1 - Solicitação ao Atendimento"` `id: "303828070"`
   2. **Fase desejada**:   `name: "Finalizado"` `id: "323314380"`
   3. **Label NÃO desejada**:  `name: "Cancelamento de Reservas"` `id: "310239937"`

      
      1. **Caso possua essa label**: não aciona o fluxo desejado. (não envia a mensagem)

   ```python
   def is_valid_to_send_message(response: dict):
       for card in response["data"]["nodes"]:
           is_desired_pipe = card["pipe"]["id"] == "303828070"
           is_desired_current_phase = card["current_phase"]["id"] == "323314380"
           has_reservation_cancelled_label = label for label in card["labels"] if label["id"] == "310239937" else None # Cancelamento de Reservas
           # True means we can proceed with next steps
           # False means it's manually canceled or is not in a valid pipe/phase, so we don't proceed to next steps by aborting.
           return is_desired_pipe and is_desired_current_phase and not has_reservation_cancelled_label
   ```


\
### Envio da Mensagem

Usar ["](https://docs.google.com/document/d/1PZfJEmHT0R-fZFXKdVTubzMVmshOoK_qq5gGkVBlE0M/edit?tab=t.0)**[Rota de mensagem de tech cancelamento reserva" da NewByte ](https://docs.google.com/document/d/1PZfJEmHT0R-fZFXKdVTubzMVmshOoK_qq5gGkVBlE0M/edit?tab=t.0)**para envio de mensagem via WhatsApp.

O hóspede receberá a seguinte mensagem:

> Oi, `Bernardo Ribeiro` :wave:\nAqui é a Seazone, administradora do imóvel `TST001` que você estava reservando pela `Airbnb`.\nPercebemos que sua reserva não foi finalizada :cry:\nPodemos te ajudar com algo? Quem sabe um descontinho especial pra dar aquele empurrãozinho? :heart_eyes:\nÉ só mandar uma mensagem aqui que a gente te ajuda rapidinho 

**Endpoint:** 

```json
POST https://autowebhook.newbyte.net.br/webhook/techCancelamentoReserva/seazone
```

**Headers**:

```json
Authorization: K6GBHvbd!mYx&^&Xq4Etm5r8g9iFefmR
```

**Body**:

```json
⁠{
	⁠"phone": "+55389XXXXXXXX",
	⁠"name": "Bernardo Ribeiro",
	⁠"ota_name": "Airbnb", // Airbnb, Booking, Decolar, Expedia, Website Seazone, B2B.Reservas, ...
	⁠"property_code": "TST001"
⁠}
```


:::info
*Verificar que o número de telefone tem o "**+**" no começo, caso não possua, devemos adicionar.*

:::



:::tip
*Toda mensagem enviada via WhatsApp sempre precisa de um template pre-definido. A princípio, não é possível enviar mensagens automáticas em qualquer formato. Os templates são revisados e aprovados pela Meta. Com isso, todo envio de mensagens automáticas via WhatsApp são feitas usando templates.*

:::


## Tarefas


1. **\[Back\] Implementar task async para enviar notificação via WhatsApp usando a NewByte**\nSerá criada o módulo `whatsapp.py` no módulo de `messaging`, e adicionar a task async no celery `send_whatsapp_message()` para envio de mensagens via WhatsApp. Nele deve ser possível especificar o provider (apenas newbyte inicialmente) template e os argumentos usados no template.\n**Celery** **Task:** `**send_whatsapp_message(**``provider_name, provider_params, template, template_params``**)**`

   
   1. Implementar abstração da integração p/ envio de templates de mensagens via WhatsApp.
   2. Implementar envio de mensagem com a NewByte
   3. Implementar a Task em si para envio de mensagens usando o template

   \
2. **\[Back\] Implementar action que dispara task async para lidar com a abordagem de cancelamento**\n**Action:** `handle_reservation_cancelled_by_guest.py` que ficará em `webhook > action` e será chamada no `**finally**` da task `stays_dispatch_delete_reserv_event_task`. Essa action irá: 

   
   1. Realizar validações básicas com base nas regras
   2. Realizar validação no Pipefy para garantir que não é um cancelamento manual.
   3. Realizar envio da mensagem ao hóspede

 ![Diagrama Alto Nível da implementação](/api/attachments.redirect?id=d50372f2-0580-41c7-ad2d-6799958aabab " =1912x295")