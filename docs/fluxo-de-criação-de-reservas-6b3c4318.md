<!-- title: Fluxo de Criação de Reservas | url: https://outline.seazone.com.br/doc/fluxo-de-criacao-de-reservas-NPOs8kioAp | area: Tecnologia -->

# Fluxo de Criação de Reservas

Created by: Bernardo Ribeiro Created time: June 19, 2024 10:52 AM Last edited: September 30, 2024 2:48 PM Tags: Asaas, Emails, Pagamento, Pagar.me, Paypal, Reservas

## Criação da reserva


---

Seguir a sequência de requests abaixo para conseguir realizar a criação da reserva.

### Criação da Pré-reserva

\*\*Iniciar processo de reservar `POST** reservations/start`

Ao realizar essa requisição, será criada um registro inicial da reserva no BD com o status ***Pending.***

No retorno, haverá os dados da reserva criada, inclusindo o ID dela que será usado nas próximas requisições.

\*\*Obter informação da reserva `GET** reservations/{reservation_id}`

Aqui, é possível acompanhar como está a reserva atualmente, como por exemplo, o status dela.

\*\*Adição de informações do(s) hóspede(s) da reserva `POST** reservations_guests`

Atualmente, estamos informando apenas os dados do hóspede principal, que é o usuário que está criando a reserva.

\*\*Confirmar criação da reserva `PUT** reservations/{reservation_id}/confirm`

Esse passo é realizado confirmando a reserva. Nesse momento, é criado o que chamamos de "Pré-reserva".

Nesse momento, o backend dispara uma tarefa assíncrona para confirmar a reserva. É possível acompanhar se o processo de confirmação dela foi concluído ou não, enviando requisições à API \*\*`GET** /tasks{task_id}` passando o task_id retornado no response.

Uma vez finalizado a task, deve ser realizado uma requisição pra obter as informações da reserva, pois nesse processo ela pode ser confirmada ou ter havido falha na confirmação.

Então, realize esse passo: [\*\*Obter informação da reserva ](/doc/fluxo-de-criacao-de-reservas-ho9oO3lOo0)`GET** reservations/{reservation_id}`

* Em caso de falha, a reserva ficará com status ***Confirmation_Failed*** deve ser corrigido conforme a causa da falha (retornado pela api de confirmação), e tentar  [\*\*Confirmar criação da reserva ](/doc/fluxo-de-criacao-de-reservas-ho9oO3lOo0)`PUT** reservations/{reservation_id}/confirm`  novamente.
* Caso tenha ocorrido tudo ok, a reserva ficará no status "***Confirmed***", significando que ela foi confirmada e a Pré-reserva foi criada na Stays. Assim, o próximo passado é **Gerar o checkout para reserva**

  <aside> ℹ️ Caso esteja no ambiente de Desenvolvimento ou Staging, as Pré-reservas somente serão criadas na Stays se for no imóvel **TST001**. Caso esteja no ambiente de produção, será possível criar reservas em qualquer imóvel.

  </aside>

### Gerar checkout para reserva

Aqui, após ter criado a reserva e ela estiver no status ***Confirmed****,* seguiremos para geração do checkout para que seja possível pagar pela reserva.

Atualmente, temos **3 opções** de Gateways de pagamento para geração do checkout.

**Opção 1: Pagar.me**

* \*\*`POST** reservations/{reservation_id}/checkout`

  <aside> ℹ️ Aqui, no payload precisa setar a **exp_asaas_variant** como `"control"`. Isso será necessário enquanto o experimento do asaas estiver rodando.

  </aside>
  * Exemplo:

    ```json
    // Body da requisição
    {
        "exp_asaas_variant": "control"
    }
    ```
* Será retornado um link para o checkout do pagarme
* Meios de pagamento:
  * Acesse ele e pague com cartão de crédito, usando um **[cartão de teste](https://docs.pagar.me/docs/simulador-de-cart%C3%A3o-de-cr%C3%A9dito)**
  * Caso escolha PIX, o valor da reservan **não pode ultrapassar** os **500 reais** para que ela seja aprovada pelo Pagarme.
* Quando pagar, vai chegar um webhook. Como estamos rodando localmente ele não vai chegar para nós, então é preciso ir até o pagarme e copiar o conteúdo do Webhook
* Para isso, acesse o **[Dash do Pagarme](https://dash.pagar.me/)** (Confira se está no ambiente de teste)

  <aside> ℹ️ Caso não possua acesso, solicite ao seu Gestor.

  </aside>
* Acesse a aba **"Webhooks"** no menu lateral
* Procure pelo webhook do **evento** **"order.paid"** e copie o request dele
  * Para achar o evento relacionado à sua reserva, pegue o **gateway_ref** que está na tabela **Payments** para sua reserva
  * Cole ele na aba de pesquisa do pagarme
* \*\*`POST** pagarme/event` passando no body o request que copiou do webhook.
* Após o envio do webhook, será disparada a task que vai confirmar o pagamento da sua reserva.
  * Nesse processo, o backend tentará confirmar o pagamento da reserva, podendo ter sucesso ou não
  * Em caso de sucesso, o status da reserva será alterado para **Paid** e um Email de confirmação de pagamento será enviado para o usuário.

**Opção 2: Asaas**

* \*\*`POST** reservations/{reservation_id}/checkout`

  <aside> ℹ️ Aqui, no payload precisa setar a **exp_asaas_variant** como `"test"`. Isso será necessário enquanto o experimento do asaas estiver rodando.

  </aside>

  **Exemplo:**

  ```json
  {
      // "billing_type": "PIX",
      "billing_type": "CREDIT_CARD", // 
      "installment_quantity": 12,
      "payer_full_name": "John Doe",
      "payer_document": "219.114.460-88", // Pode usar um CPF gerado no 4devs.com.br/gerador_de_cpf
      "exp_asaas_variant": "test"
  }
  ```
* Será retornado um link para o checkout
* Acesse ele e pague com cartão de crédito, usando um **[cartão de teste](https://docs.asaas.com/docs/como-testar-funcionalidades)**
* Quando pagar, vai chegar um webhook. Como estamos rodando localmente ele não vai chegar para nós, então é preciso ir até o ASAAS e copiar o conteúdo do Webhook
* Para isso, acesse o **[sandbox do Asaas](https://sandbox.asaas.com/)**
* Acesse a aba **"Webhooks"**
* Para isso, clique no icone de usuario no canto superior direito
* Vá em "Integrações"
* Clique em "Logs de Webhooks"
* Procure pelo webhook do evento "**PAYMENT_RECEIVED**" e copie o conteúdo dele
* Para achar o evento relacionado à sua reserva, pegue o **gateway_ref** que está na tabela **payments** para sua reserva
* Cole ele no filtro "identificador da cobrança"

  <aside> ⚠️ **IMPORTANTE**: Nós salvamos na tabela o ID da cobrança referente a **primeira parcela**. Então, você deve copiar o conteúdo da primeira parcela.

  </aside>

  <aside> ℹ️ O Asaas envia um Webhook para cada parcela.

  </aside>
* Para saber se o conteúdo é realmente o da primeira parcela, veja o campo "description" no payload. Lá vai dizer "`Parcela 1 de X...`"
* \*\*`POST** asaas/event` passando no body o request que copiou do webhook.
* Após o envio do webhook, será disparada a task que vai confirmar o pagamento da sua reserva.
  * Nesse processo, o backend tentará confirmar o pagamento da reserva, podendo ter sucesso ou não
  * Em caso de sucesso, o status da reserva será alterado para **Paid** e um Email de confirmação de pagamento será enviado para o usuário.

**Opção 3: Paypal**

`POST /paypal/create-order`

`POST /paypal/capture-order`

## Webhooks


---

Veja aqui como simular outros Webhooks relacionados à reservas

[Simulação de Webhooks](/doc/simulacao-de-webhooks-Ai1TGhwrJz)

## Emails de Reservas


---

**Confirme sua reserva conosco!**

Email enviado quando a reserva é confirmada e criado a pŕe-reserva.

**Não identificamos o pagamento da Reserva AB123C**

Email enviado quando a reserva não é paga dentro de 30min após sua confirmação (criação da pré-reserva). Assim, ela fica como uma reserva "Expirada".

**Confirmação de Pagamento | Reserva AB123C**

Email enviado quando o pagamento é confirmado pelo gateway e a reserva mudou seu status para "Pago"

**Falha ao confirmar o pagamento da reserva AB123C**

Email enviado quando há uma falha no pagamento da reserva. Geralmente por causa do anti-fraude.

# \[v2\] Criação de reserva

Ao realizar essa requisição, será criada um registro inicial da reserva no BD com o status `waiting_confirmation`***.***

No retorno, haverá os dados da reserva criada, incluindo o pin da reserva e o ID da reserva na stays que será utilizado para visualizar os detalhes da reserva e para efetuar o pagamento. A nova versão de criação de reserva é a união das APIs de [criação da reserva](/doc/fluxo-de-criacao-de-reservas-ho9oO3lOo0) e [confirmação de reserva](/doc/fluxo-de-criacao-de-reservas-ho9oO3lOo0)

`POST /reservations/create`

Exemplo de request:

```json
{
   "property_id":88,
   "user_data":{
      "email":"f.neves@seazone.com.br",
      "first_name":"Fernando",
      "last_name":"Neves",
      "phone_number":"5538998203313",
      "document_type":"CPF",
      "document":"11122299933",
      "birthdate":"2000-01-01",
      "gender":"Male"
   },
   "check_in_date":"2024-09-22",
   "check_out_date":"2024-09-24",
   "adults":1,
   "kids":1,
   "babies":1,
   "promo_code":"destino10",
   "tracking_utm_medium":"localhost",
   "tracking_utm_source":"bernardo.ribeiro",
   "tracking_utm_campaign":"backend_dev_team",
   "tracking_raw_data":{}
}
```

Exemplo de retorno 200 OK:

```json
{
    "id": 45,
    "property_id": 88,
    "status": "Confirmed",
    "check_in_date": "2024-09-22",
    "check_in_time": "15:00:00",
    "check_out_date": "2024-09-24",
    "check_out_time": "11:00:00",
    "guests_quantity": 2,
    "adults": 1,
    "kids": 1,
    "babies": 1,
    "promo_code": "destino10",
    "promo_info": null,
    "total_price": 525.0,
    "effective_price": 472.5,
    "total_paid": null,
    "installments": null,
    "nights_price": 300.0,
    "cleaning_fee": 225.0,
    "confirmation_failure_cause": null,
    "confirmation_failure_details": null,
    "created_at": "2024-07-23T13:36:38.910959",
    "created_by": "Fernando Neves Nogueira",
    "pin": "5382",
    "stays_id": null,
    "reservation_link": null
}
```

## Fluxo backend

Link Projeto: https://drive.google.com/file/d/16cmR4oyKQz5rFCQJOuWmqABQLt3PPthF/view?usp=sharing

 ![Untitled](Fluxo%20de%20Criac%CC%A7a%CC%83o%20de%20Reservas%20fc938c689aa44eefb04e7c596164b3f3/Untitled.png)

 ![Untitled](Fluxo%20de%20Criac%CC%A7a%CC%83o%20de%20Reservas%20fc938c689aa44eefb04e7c596164b3f3/Untitled%201.png)

 ![Untitled](Fluxo%20de%20Criac%CC%A7a%CC%83o%20de%20Reservas%20fc938c689aa44eefb04e7c596164b3f3/Untitled%202.png)