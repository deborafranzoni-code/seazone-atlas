<!-- title: Simulação de Webhooks | url: https://outline.seazone.com.br/doc/simulacao-de-webhooks-rJu0rsqiO0 | area: Tecnologia -->

# Simulação de Webhooks

Created by: Bernardo Ribeiro Created time: June 27, 2024 11:20 AM Last edited: October 14, 2024 3:41 PM Tags: Asaas, Pagar.me, Paypal, Stays, Tuna

Atualmente recebemos e lidamos/tratamos os seguintes Webhooks das seguintes plataformas:

| Stays |    |
|----|----|
| Asaas |    |
| Pagar.me |    |
| Tuna | Init,Capture,Cancel,Chargeback |

No código, as integração que possuem webhooks e que estamos tratando-os, estão nos arquivos nomeados como: `webhooks.py`

**Endpoints pelos quais os Webhooks são recebidos**

| Stays | `POST /stays/event` | No Auth |
|----|----|----|
| Asaas | `POST /asaas/event` | No Auth |
| Pagar.me | `POST /pagarme/event` | No Auth |
| Tuna | `POST /tuna/event` | No Auth |

## Stays


---

[API Reference](https://stays.net/external-api/#webhook-notifications)

* **Cancelamento de reserva**

  Simule o recebimento do evento `reservation.canceled` no endpoint: `POST http://localhost:8001/stays/event`

  ```json
  //body
  {
       "action": "reservation.canceled", // nome do evento
       "payload": {
           "id": "JM98I", // Substitua pelo `stays_id` da pre-reserva que você criou
           "_idlisting": "604e42ff500e5de7df1a1e11" //stays_listing_id do imovel
       }
   }
  ```
* **Atualização de listing**

  Eventos: `listing.modified`, `listing.created`

  Payload:

  ```json
  {
      "action": "listing.modified",
      "_dt": "2024-07-03T12:06:57.574Z",
      "payload": {
          "_id": "665f05161d589706c3713a90",
          "id": "IR01I",
          "internalName": "SDS104"
      }
  }
  ```
* **Atualização de disponibilidade e preços**

  **Eventos:** `calendar.rates.modified`, `calendar.restrictions.modified`, `listing-rates-sell.modified`

  **Payload:**

  ```json
  {
      "action": "calendar.rates.modified",
      "_dt": "2024-07-22T17:28:28.059Z",
      "payload": [
          {
              "_idlisting": "60e73500d0b7c57753e07b92"
          }
      ]
  }
  ```
* **Evento de reservas**

  **Eventos**: `reservation.*`: `reservation.created`, `reservation.modified`, `reservation.canceled`, `reservation.reactivated`

  **Payload**:

  ```json
  {
      "action": "reservation.created",
      "_dt": "2024-07-03T15:07:02.577Z",
      "payload": {
          "_id": "668568de150f6a1f452de5b3",
          "id": "KR97I",
          "creationDate": "2024-07-03",
          "checkInDate": "2024-07-26",
          "checkOutDate": "2024-07-30",
          "_idlisting": "604e42ff500e5de7df1a1e11",
          "type": "reserved",
          "price": {
              "currency": "BRL",
              "_f_total": 40100
          }
      }
  }
  
  ```

## Asaas


---

https://docs.asaas.com/docs/webhook-para-cobrancas

* Criação de cobrança

  Esse evento ocorre assim que a cobrança é criada no Asaas. Ocorre na chamada para geração do Checkout.

  ```json
  {
   "id": "evt_15e444ff9b9ab9ec29294aa1abe68025&7266931",
   "event": "PAYMENT_CONFIRMED",
   "dateCreated": "2024-09-09 19:04:36",
   "payment": {
    "object": "payment",
    "id": "pay_1oj676avl6oa6nfi", // Coloque aqui o gateway_ref
    "dateCreated": "2024-09-09",
    "customer": "cus_000006040165",
    "installment": "c161021c-dac8-48bb-bb01-0d10bf3fdbc0",
    "paymentLink": null,
    "value": 14213.62,
    "netValue": 13717.33,
    "grossValue": null,
    "originalValue": null,
    "interestValue": null,
    "description": "Parcela 1 de 2. Reserva no imóvel TST001 | NG91I | 2024-10-01",
    "billingType": "CREDIT_CARD",
    "confirmedDate": "2024-09-09",
    "creditCard": {
     "creditCardNumber": "4444",
     "creditCardBrand": "VISA",
     "creditCardToken": "47f3091a-07ed-4f3b-858e-4afdbac15994"
    },
    "pixTransaction": null,
    "status": "CONFIRMED",
    "dueDate": "2024-09-09",
    "originalDueDate": "2024-09-09",
    "paymentDate": null,
    "clientPaymentDate": "2024-09-09",
    "installmentNumber": 1,
    "invoiceUrl": "https://sandbox.asaas.com/i/1oj676avl6oa6nfi",
    "invoiceNumber": "06448248",
    "externalReference": "79",
    "deleted": false,
    "anticipated": false,
    "anticipable": false,
    "creditDate": "2024-10-11",
    "estimatedCreditDate": "2024-10-11",
    "transactionReceiptUrl": "https://sandbox.asaas.com/comprovantes/4347763943476176",
    "nossoNumero": null,
    "bankSlipUrl": null,
    "lastInvoiceViewedDate": null,
    "lastBankSlipViewedDate": null,
    "discount": {
     "value": 0,
     "limitDate": null,
     "dueDateLimitDays": 0,
     "type": "FIXED"
    },
    "fine": {
     "value": 0,
     "type": "FIXED"
    },
    "interest": {
     "value": 0,
     "type": "PERCENTAGE"
    },
    "postalService": false,
    "custody": null,
    "refunds": null
   }
  }
  ```
* **Aprovação do pagamento**

  ```json
  {
      "id": "evt_15e444ff9b9ab9ec29294aa1abe68025&7266931",
      "event": "PAYMENT_CONFIRMED",
      "dateCreated": "2024-09-09 19:04:36",
      "payment": {
          "object": "payment",
          "id": "pay_1oj676avl6oa6nfi",
          "dateCreated": "2024-09-09",
          "customer": "cus_000006040165",
          "installment": "c161021c-dac8-48bb-bb01-0d10bf3fdbc0",
          "paymentLink": null,
          "value": 14213.62,
          "netValue": 13717.33,
          "grossValue": null,
          "originalValue": null,
          "interestValue": null,
          "description": "Parcela 1 de 2. Reserva no imóvel TST001 | NG91I | 2024-10-01",
          "billingType": "CREDIT_CARD",
          "confirmedDate": "2024-09-09",
          "creditCard": {
              "creditCardNumber": "4444",
              "creditCardBrand": "VISA",
              "creditCardToken": "47f3091a-07ed-4f3b-858e-4afdbac15994"
          },
          "pixTransaction": null,
          "status": "CONFIRMED",
          "dueDate": "2024-09-09",
          "originalDueDate": "2024-09-09",
          "paymentDate": null,
          "clientPaymentDate": "2024-09-09",
          "installmentNumber": 1,
          "invoiceUrl": "https://sandbox.asaas.com/i/1oj676avl6oa6nfi",
          "invoiceNumber": "06448248",
          "externalReference": "79",
          "deleted": false,
          "anticipated": false,
          "anticipable": false,
          "creditDate": "2024-10-11",
          "estimatedCreditDate": "2024-10-11",
          "transactionReceiptUrl": "https://sandbox.asaas.com/comprovantes/4347763943476176",
          "nossoNumero": null,
          "bankSlipUrl": null,
          "lastInvoiceViewedDate": null,
          "lastBankSlipViewedDate": null,
          "discount": {
              "value": 0,
              "limitDate": null,
              "dueDateLimitDays": 0,
              "type": "FIXED"
          },
          "fine": {
              "value": 0,
              "type": "FIXED"
          },
          "interest": {
              "value": 0,
              "type": "PERCENTAGE"
          },
          "postalService": false,
          "custody": null,
          "refunds": null
      }
  }
  ```
* **Recusa do cartão de crédito**
  * Crie uma reserva e gere um checkout com o ASAAS como gateway (porém, não pague por ela)
  * Simule o fluxo de cartão de crédito recusado:
    * Simular o evento: `PAYMENT_CREDIT_CARD_CAPTURE_REFUSED`
    * Você deverá receber um email informando a falha no pagamento.
    * Status do pagamento vai mudar para Failed, porém ainda deve ser possível pagar por ele.
  * Simule o fluxo de análise de risco:
    * Simular o evento: `PAYMENT_AWAITING_RISK_ANALYSIS`: O pagamento deve alterar o status para `Payment_Analysis`
    * Simular o evento: `PAYMENT_REPROVED_BY_RISK_ANALYSIS`
      * O pagamento será Cancelado (status='Canceled') e a reserva Expirada (status='Expired')
      * Além disso, você deverá receber um email informando que o pagamento foi reprovado.

  Simule um webhook do ASAAS da enviando um `POST /asaas/event/` com o seguinte body:

  ```json
  {
   "id": "evt_05b708f961d739ea7eba7e4db318f621&6762800",
   "event": "evento que se deseja simular", // `PAYMENT_CREDIT_CARD_CAPTURE_REFUSED`, `PAYMENT_AWAITING_RISK_ANALYSIS`, `PAYMENT_REPROVED_BY_RISK_ANALYSIS`
   "payment": {
    "object": "payment",
    "id": "aqui é o order_id que tem no payment dessa reserva", // payment.order_id, ex: 'pay_abcd123efg'
    "value": 10289.2,
    "netValue": 9929.95,
    "description": "Parcela 1 de 3. Reserva no imóvel TST001 | JM192I | 2024-06-25",
    "billingType": "meio de pagamento escolhido", // PIX, CREDIT_CARD
    "creditCard": {
     "creditCardNumber": null,
     "creditCardBrand": null
    },
    "status": "PENDING",
    "invoiceUrl": "https://sandbox.asaas.com/i/u9mudhq8r57dolie",
  }
  ```

## Tuna


---

Para webhooks da tuna, atualmente utilizamos o campo **status** que está dentro do primeiro objeto da lista **methods.** Esse é um status mais detalhado do método que nos permite lidar melhor com os eventos, como por exemplo, diferenciar o webhooks de eventos com statusId=4 (Denied), onde para o evento de abandonado era interpretado como Denied, gerando falsos positivos na KPI de recusas de pagamento.

> **[Doc Webhooks Tuna](https://dev.tuna.uy/api/webhooks-notifications/)**


**Todos os Webhooks da Tuna seguem uma estrutura padrão**

Para saber qual código usar no status, verifique a doc: 

> **[Status possíveis para os](https://dev.tuna.uy/api-guide/tuna-codes#payment-method-status)** [methods](https://dev.tuna.uy/api-guide/tuna-codes#payment-method-status) **[de pagamento](https://dev.tuna.uy/api-guide/tuna-codes#payment-method-status)**
>
> [Status possíveis para o statusId](https://dev.tuna.uy/api-guide/tuna-codes#payment-status)

```json
{
    "id": 98,
    "paymentKey": "134DA1E0000001F", // ALTERAR AQUI. Esse é o payment.gateway_ref
    "partnerUniqueId": "81",
    "statusId": "2", // ALTERAR AQUI. Esse indica o status da TRANSAÇÃO
    "amount": 27900.0, // [OPCIONAL] ALTERAR AQUI. Esse é o total_paid da reserva
    "operationId": "O11CA134DA1E00000020",
    "methods": [
        {
            "methodType": "1", // ALTERAR AQUI. 1=CC, D=Pix
            "status": "2", // ALTERAR AQUI. 2 indica que foi Capturado/Pago
            "methodId": 2,
            "operationId": "O11CA134DA1E0000002002",
            "oprarionAmount": 27900,
            "operationAmount": 27900
        }
    ],
    "items": [ // [OPCIONAL] ALTERE SE QUISER. São os itens da cobrança
        {
            "paymentItemId": 0,
            "productID": 85,
            "productUniqueID": "81",
            "productDescription": "Apartamento de Teste Interno Seazone - TST001",
            "amount": 31000.0,
            "quantity": 1,
            "data": {
                "ProductID": 85,
                "DetailUniqueID": "81",
                "ProductUniqueID": "81",
                "ProductDescription": "Apartamento de Teste Interno Seazone - TST001"
            }
        }
    ]
}
```

## Pagar.me


---


---

## **Docs Relacionadas**

[Fluxo de Criação de Reservas](/doc/fluxo-de-criacao-de-reservas-ho9oO3lOo0)

[Gateways de Pagamento](/doc/gateways-de-pagamento-4jbkAXQQUJ)