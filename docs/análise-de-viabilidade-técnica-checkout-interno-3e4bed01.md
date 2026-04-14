<!-- title: Análise de Viabilidade Técnica: Checkout Interno | url: https://outline.seazone.com.br/doc/analise-de-viabilidade-tecnica-checkout-interno-2l72BWtsNr | area: Tecnologia -->

# Análise de Viabilidade Técnica: Checkout Interno

# **Introdução**

O objetivo da integração é aprimorar o controle sobre o processo de checkout no site de reservas. Atualmente, geramos apenas um link de pagamento que redireciona para a tela de checkout da Tuna. A proposta é manter a integração com a Tuna, mas implementando nossa própria tela e fluxo de checkout, permitindo um maior controle sobre esse processo.


**Protótipo**

[https://www.figma.com/design/SxkaCB56BXCDHHZq1oaWOG/Seazone-Site?node-id=1887-1354&t=TnSVqBaJujbzad6f-0](https://www.figma.com/design/SxkaCB56BXCDHHZq1oaWOG/Seazone-Site?node-id=1887-1354&t=TnSVqBaJujbzad6f-0)

# **Análise da API**

A API de Pagamentos da Tuna permite que empresas integrem diversos métodos de pagamento em suas plataformas, como cartões de crédito e débito, boleto bancário, PIX, Nupay e Bitcoin. No nosso caso, usaremos somente as opções de cartão de crédito e PIX.

Em resumo, o fluxo de pagamento inicia-se no checkout, onde o cliente fornece os dados do cartão, que são tokenizados pelas bibliotecas da Tuna. Em seguida, a API de Pagamentos processa a autorização junto aos provedores de pagamento, realiza análises antifraude e executa ações personalizadas conforme o contexto do negócio. Dependendo dos resultados, podem ser solicitadas informações adicionais ao cliente, como autenticação 3DS2 ou desafios via SMS. Após a autorização, o pagamento é capturado pelo provedor de serviços de pagamento, e a liquidação ocorre na data acordada.

## Endpoints

Nesta seção, são detalhados os principais endpoints da API da Tuna que serão integrados ao nosso sistema de checkout interno.

### **Iniciar Nova Sessão**

Para implementar um fluxo de checkout personalizado e manter a integração com a Tuna, é necessário iniciar uma nova sessão para cada cliente. Isso é feito através do endpoint `api/Token/NewSession`, que cria uma sessão única para o usuário.


**Rota: POST** `api/Token/NewSession`

**Doc: <https://dev.tuna.uy/api/token/#operation/NewSession>**

| **Header** |
|----|
| x-tuna-account |
| x-tuna-apptoken |

**Body**

```json
{
  "customer": {
    "id": "user_id-123",
    "email": "maria.romero@seazone.com.br"
  }
}
```

| **Nome** | **Tipo** | **Descrição** |
|----|----|----|
| id | string | Identificador do usuário |
| email | string | Endereço de email do usuário |


**Response**

```json
{
    "sessionId": "KQ8g2V7mq4BzSgbJqucQ9Tzval3mSxymEY2vkLJWe8+0FunnrzlIRl5iae1amTyL3hWImeLKbmhEXUTh4Sd0cW+a+sPb2687un78NPFOq1O7nXf4",
    "code": 1,
    "message": null
}
```

### Validar sessão

O endpoint `api/Token/ValidateSession` da Tuna é utilizado para validar a sessão de um cliente,  essa validação assegura que a sessão está ativa e que as operações subsequentes podem ser realizadas com segurança.


**Rota: POST** `/api/Token/ValidateSession`

**Doc: <https://dev.tuna.uy/api/token/#operation/ValidateSession>**

| **Header** |
|----|
| x-tuna-account |
| x-tuna-apptoken |

**Body**

```json
{
    "sessionId": "1e+8R4fxjqMArzL241OKmPb4vhjyB6H2+9pe94S9xt11LJqAWXXG10vg8ZCLkt+5ka4N3WhtzgZQHrQHUciX9/MMN4JtNp6D3jPhwwnLYantQtuw"
}
```

| **Nome** | **Tipo** | **Descrição** |
|----|----|----|
| sessionId | uuid | Identificador da sessão gerado no [endpoint anterior](https://outline.seazone.com.br/doc/analise-de-viabilidade-tecnica-checkout-interno-iyfdO5xRUr#h-iniciar-nova-sessao) |


**Response**

```json
{
  "partnerId": 4554,
  "partnerUniqueId": "",
  "accountIsolation": false,
  "code": 1,
  "message": "Session is valid"
}
```

### Iniciar pagamento

Após a geração e validação da sessão, é necessário utilizar o endpoint `api/Payment/Init` para iniciar uma transação de pagamento. Esse endpoint recebe os detalhes da compra e as informações do pagamento. É importante destacar que a tokenização do cartão deve ser realizada no front-end, [utilizando a biblioteca fornecida pela Tuna](https://dev.tuna.uy/plugins/javascript), antes de enviar os dados para este endpoint.\n

**Rota: POST** `/api/Payment/Init`

**Doc: <https://dev.tuna.uy/api/payment#operation/Init>**

| **Header** |
|----|
| x-tuna-account |
| x-tuna-apptoken |


**Body (Cartão de Crédito)**

```json
{
    "tokenSession": "1e+8R4fxjqMArzL241OKmPb4vhjyB6H2+9pe94S9xt11LJqAWXXG10vg8ZCLkt+5ka4N3WhtzgZQHrQHUciX9/MMN4JtNp6D3jPhwwnLYantQtuw",
    "partnerUniqueId": "RESERVA_TST_10",
    "customer": {
        "id": "7",
        "email": "maria.romero@seazone.com.br",
        "document": "744.479.870-23",
        "documentType": "CPF",
        "name": "Maria Fernanda Vaz Romero"
    },
    "paymentItems": {
        "items": [
            {
                "amount": 1800,
                "detailUniqueId": "STAYSID123",
                "productDescription": "Reserva no Imóvel TST001",
                "itemQuantity": 1
            }
        ]
    },
    "paymentData": {
        "amount": 2000,
        "paymentMethods": [
            {
                "paymentMethodType": "1",
                "amount": 1800,
                "installments": 1,
                "cardInfo": {
                    "token": "ct_YWM3ZDgyMGQtZWMwMS00M2UwLWE2OTctMGVlNmM2YmE2OThm0",
                    "tokenProvider": "Tuna",
                    "cardHolderName": "Captured",
                    "expirationMonth": 12,
                    "expirationYear": 2023,
                    "brandName": "Visa",
                    "tokenSingleUse": 0,
                    "saveCard": false,
                    "billingInfo": {
                        "document": "744.479.870-23",
                        "documentType": "CPF"
                    }
                },
                "authenticationInformation": {
                  "code": "CXsOSV35t+q8KkpVpNijIZKNGfBbEPEuvYWZlqkbSogecwScXG",
                  "referenceId": "a80f428d e8b2 4a06 8b3a ac8ad263918b",
                  "transactionId": "Cd3GiRax5ntizPsg3fx1"
                }
            }
        ],
        "deliveryAddress": {
            "street": "Rua João Longo",
            "number": "1004",
            "neighborhood": "Jandira",
            "city": "São Paulo",
            "state": "SP",
            "postalCode": "06608-420",
            "phone": "(11) 6536-8864",
            "country": "BR"
        },
        "countryCode": "BR"
    }
}
```

**OBS:** o `authenticationInformation` é obrigatório somente quando o pagamento requer autenticação 3DS, mas como não sabemos se isso vai ser requerido ou não, sempre enviaremos.


**Body (Cartão de Crédito com 3DS)**

```json
{
    "tokenSession": "1e+8R4fxjqMArzL241OKmPb4vhjyB6H2+9pe94S9xt11LJqAWXXG10vg8ZCLkt+5ka4N3WhtzgZQHrQHUciX9/MMN4JtNp6D3jPhwwnLYantQtuw",
    "partnerUniqueId": "RESERVA_TST_10",
    "customer": {
        "id": "7",
        "email": "maria.romero@seazone.com.br",
        "document": "744.479.870-23",
        "documentType": "CPF",
        "name": "Maria Fernanda Vaz Romero"
    },
    "paymentItems": {
        "items": [
            {
                "amount": 1800,
                "detailUniqueId": "STAYSID123",
                "productDescription": "Reserva no Imóvel TST001",
                "itemQuantity": 1
            }
        ]
    },
    "paymentData": {
        "amount": 2000,
        "paymentMethods": [
            {
                "paymentMethodType": "1",
                "amount": 1800,
                "installments": 1,
                "cardInfo": {
                    "token": "ct_YWM3ZDgyMGQtZWMwMS00M2UwLWE2OTctMGVlNmM2YmE2OThm0",
                    "tokenProvider": "Tuna",
                    "cardHolderName": "Captured",
                    "expirationMonth": 12,
                    "expirationYear": 2023,
                    "brandName": "Visa",
                    "tokenSingleUse": 0,
                    "saveCard": false,
                    "billingInfo": {
                        "document": "744.479.870-23",
                        "documentType": "CPF"
                    }
                },
                "authenticationInformation": {
                  "code": "CXsOSV35t+q8KkpVpNijIZKNGfBbEPEuvYWZlqkbSogecwScXG",
                  "referenceId": "a80f428d e8b2 4a06 8b3a ac8ad263918b",
                  "transactionId": "Cd3GiRax5ntizPsg3fx1"
                }
            }
        ],
        "deliveryAddress": {
            "street": "Rua João Longo",
            "number": "1004",
            "neighborhood": "Jandira",
            "city": "São Paulo",
            "state": "SP",
            "postalCode": "06608-420",
            "phone": "(11) 6536-8864",
            "country": "BR"
        },
        "countryCode": "BR"
    }
}
```

[OBS:](https://dev.tuna.uy/api/tuna-codes#payment-methods) A única diferença do cartão normal é o paymentMethodType, que no caso do 3DS, deve ser 7. (<https://dev.tuna.uy/api/tuna-codes#payment-methods>)


**Body (PIX)**

```json
{
  "tokenSession": "+IDrFsAkcTwCsTLewqWm4REBSFI0iMq3nOeVaey+Tyyd/HkUQfFfzZs0ivw43nPGOJ2ert9IUdiB2Ld2ctyEoaN+VTz3t/7hDxRsj+5C25A8AQSG",
  "partnerUniqueId": "RESERVA_TST_11",
  "customer": {
    "id": "7",
    "email": "maria.romero@seazone.com.br",
    "document": "744.479.870-23",
    "documentType": "CPF",
    "name": "Maria Fernanda Vaz Romero"
  },
  "paymentItems": {
    "items": [
      {
        "amount": 20,
        "detailUniqueId": "A01",
        "productDescription": "Test product",
        "itemQuantity": 1
      }
    ]
  },
  "paymentData": {
    "paymentMethods": [
      {
        "paymentMethodType": "D",
        "amount": 20,
        "pix": {
          "name": "Maria Fernanda Vaz Romero",
          "document": "744.479.870-23",
          "documentType": "CPF"
        }
      }
    ],
    "deliveryAddress": {
      "street": "Rua João Longo",
      "number": "1004",
      "neighborhood": "Jandira",
      "city": "São Paulo",
      "state": "SP",
      "postalCode": "06608-420",
      "phone": "(11) 6536-8864",
      "country": "BR"
    },
    "countryCode": "BR"
  }
}
```



| Nome | Tipo | Descrição |
|----|----|----|
| **tokenSession** | string Nullable | Obrigatório apenas para pagamento com cartão de crédito. Use o sessionId criado no endpoint da API Token no método "Nova Sessão". |
| **partnerUniqueID** | string | Seu id único para o pedido. É usado para rastrear o pedido. |
| **customer** | object Nullable | Este objeto é usado para passar dados do cliente, principalmente para prevenção de fraudes. Ao usar um cartão salvo, apenas tokens de cartão pertencentes ao usuário deste cliente funcionarão. |
| **vendor** | object Nullable | Este objeto é usado para passar dados do vendedor. É principalmente usado para prevenção de fraudes. |
| **paymentItems** | object Nullable | Este objeto contém a coleção de itens relacionados a este pedido. |
| **paymentData** | object Nullable | Informações sobre os métodos de pagamento usados neste pedido. |
| **frontData** | object Nullable | Este objeto contém dados que devem ser extraídos do frontend da página de checkout. |
| **extraInfo** | string Nullable | Uma string contendo informações extras. É usada apenas para personalizações. |


**Response (Cartão de Crédito)**

```json
{
    "status": "P",
    "methods": [
        {
            "message": {
                "source": 3,
                "code": "GwResultOk",
                "message": "Operation done."
            },
            "cardInfo": {
                "bin": "411111",
                "brandName": "VISA"
            },
            "acquirer": [
                {
                    "name": "Dummy",
                    "status": "2"
                }
            ],
            "methodType": "1",
            "status": "2",
            "methodId": 0,
            "operationId": "O11CA134FEC80000204A00",
            "methodKey": "134FEC800001A9B00"
        }
    ],
    "paymentKey": "134FEC800001A9B",
    "partnerUniqueId": "RESERVA_TST_17",
    "code": 1,
    "operationId": "O11CA134FEC80000204A"
}
```

**Response (Cartão de Crédito com 3DS)**

```json
{
  "status": "P",
  "methods": [
    {
      "message": {
        "source": 3,
        "code": "GwResultOk",
        "message": "Operation done."
      },
      "cardInfo": {
        "bin": "0000",
        "last4": "1111",
        "brandName": "MasterCard"
      },
      "threeDSInfo": { // campo que o frontend irá usar para autenticação
        "url": "https://centinelapi.cardinalcommerce.com/V2/Cruise/StepUp",
        "provider": "CyberSource",
        "token": "eyJhbGciOiJIUasddweeqwadCI6IkpXVCJ9.eyJqdGkiOiI2MmVkM2QyYy0xMzcxLTrwerqasdadwfdfiLCJpYXQiOjE3NDQ5MTkyNDUsImlzcyI6IjVlMjIwMDVmMzU2ZGNlMDNmMGY3ODcyZiIsImV4cCI6MTc0NDkyMjg0NSwiT3JnVW5pdElkIjoiNjI1ZWNmOWRjNzAzY2IyZDk5ZGJjMWIxIiwiUGF5bG9hZCI6eyJBQ1NVcmwiOiJodHRwczovL2VtdjNkc2F1dGguc2VjdXJlYWNzLmNvbS9hY3Myd2ViL2FjczJudWJhbmtici9hdXRoZW50aWNhdGlvbj9odGNzZmlhZm09MTc0NDkxOTI0NSIsIlBheWxvYWQiOiJleUp0WlhOellXZGxWSGx3WlNJNklrTlNaWEVpTENKdFpYTnpZV2RsVm1WeWMybHZiaUk2SWpJdU1pNHdJaXdpZEdoeVpXVkVVMU5sY25abGNsUnlZVzV6U1VRaU9pSmlOR0V6TldRNVppMDFOR1kxTFRRek9EUXRZbU00WWkwNU5tRmpPV1ZoTmpCa016TWlMQ0poWTNOVWNtRnVjMGxFSWpvaU1qaGxNVFppWlRjdE1UYzNZeTAxTUdJd0xUbGtPR0V0Wm1Wa05EaG1ZMk5sTXpoa0lpd2lZMmhoYkd4bGJtZGxWMmx1Wkc5M1UybDZaU0k2SWpBeUluMCIsIlRyYW5zYWN0aW9uSWQiOiJITGNzUnlnMjYyTU5PVmRoSnNhMCJ9LCJPYmplY3RpZnlQYXlsb2FkIjp0cnVlLCJSZXR1cm5VcmwiOiJodHRwczovL3VzLWNlbnRyYWwxLWNyZWRpYmxlLWFydC0yNzc5MjEuY2xvdWRmdW5jdGlvbnMubmV0L3R1bmEzZHM_aWQ9UDExQ0ExMzRGRjMxMDAwMDI2NTMwMzAwMjYwMSJ9.azxioB2qnaC5naFQ-jKiurVV2JgDjAalFB_ydWMqyk0",
        "paRequest": "eyJtZXNzYWdlVHlwZSI6IkNSZXEiLCJtZXNzfasdfweradsuMi4wIiwidGhyZWVEU1NlcnZlclRyYW5zSUQiOiJiNGEzNWQ5Zi01NGY1LTQzODQtYmM4Yi05NmFjOWVhNjBkMzMiLCJhY3NUcmFuc0lEIjoiMjhlMTZiZTctMTc3Yy01MGIwLTlkOGEtZmVkNDhmY2NlMzhkIiwiY2hhbGxlbmdlV2luZG93U2l6ZSI6IjAyIn0"
      },
      "acquirer": [
        {
          "name": "CyberSource3DS",
          "status": "0",
          "message": "Pending Authentication",
          "time": "2025-04-17T16:47:25.318043",
          "order": 1
        }
      ],
      "methodType": "1",
      "status": "0",
      "methodId": 3,
      "operationId": "O11CA134FF3100002E5803",
      "methodKey": "134FF310000265303"
    }
  ],
  "paymentKey": "134FF3100002653",
  "partnerUniqueId": "SDR001369",
  "code": 1,
  "operationId": "O11CA134FF3100002E58"
}
```

**Response (PIX)**

```json
{
    "status": "P",
    "methods": [
        {
            "message": {
                "source": 3,
                "code": "GwResultOk",
                "message": "Operação efetuada."
            },
            "pixInfo": {
                "qrContent": "PIX-COPY-AND-PASTE",
                "qrImage": "data:image/png;base64,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",
                "qrCopyPaste": "PIX-COPY-AND-PASTE",
                "expiration": 30
            },
            "acquirer": [
                {
                    "name": "Dummy",
                    "status": "C"
                }
            ],
            "methodType": "D",
            "status": "C",
            "methodId": 0,
            "operationId": "O11CA134FEC80000205800",
            "methodKey": "134FEC800001AA900"
        }
    ],
    "paymentKey": "134FEC800001AA9",
    "partnerUniqueId": "RESERVA_TST_11",
    "code": 1,
    "operationId": "O11CA134FEC800002058"
}
```

# **Proposta de Solução**

O fluxo proposto, com base na documentação da Tuna, consiste em uma integração onde o backend realiza as chamadas à API de pagamentos da Tuna. Nesse modelo, o processamento dos pagamentos é dividido entre o frontend e o backend. O Tuna.js é utilizado no frontend principalmente para a tokenização dos dados do cartão de crédito no lado do cliente, enquanto as transações de pagamento são processadas no backend.


## **Fluxo de Integração**


1. **Criação da Sessão no Backend:**
   * No servidor, geramos um `sessionId` utilizando a API da Tuna. Este identificador é associado aos dados do cliente e, opcionalmente, aos detalhes do pedido.
2. **Tokenização no Frontend com Tuna.js:**
   * No frontend o Tuna.js coleta os dados sensíveis do cartão de crédito e os envia para o servidor da Tuna, que retorna um token seguro representando essas informações.
3. **Processamento do Pagamento no Backend:**
   * Com o token de cartão de crédito obtido, o servidor realiza a chamada à API de pagamento da Tuna para iniciar a transação.
   * A Tuna processa o pagamento e retorna o status da transação, que é então comunicado ao frontend para informar ao usuário o resultado do pagamento.

**Vantagens deste Método:**

* **Segurança Aprimorada:** Os dados sensíveis do cartão de crédito são tokenizados no frontend, reduzindo o risco de exposição durante a transmissão e o armazenamento.
* **Controle Total no Backend:** Seu servidor gerencia as transações de pagamento, permitindo maior flexibilidade e controle sobre o processamento de pagamentos.
* **Conformidade com PCI DSS:** Ao não enviar dados sensíveis do cartão para o backend, facilitamos a conformidade com os padrões de segurança de dados da indústria de cartões de pagamento.

  \

 ![Ilustração do fluxo de integração proposto](/api/attachments.redirect?id=16b59b47-e19f-463a-aaef-37bc2363b169 " =464x412")


## **Detalhamento do Processo de Checkout Interno**

**Etapas do Fluxo:**


1. **Início: Confirmar e Pagar (Frontend)**
   * O usuário interage com o frontend e clica em "Confirmar e Pagar".
   * O frontend obtém o `sessionId` do Tuna (detalhes no passo 2).
2. **Obter Tuna sessionId (Reservas API)**
   * O frontend envia o `email` do usuário para a rota `/tuna/auth-token` da API de Reservas para obter um `sessionId`.
   * A API do Tuna cria uma nova sessão de usuário e retorna o `sessionId`.
3. **Tokenizar Cartão (Frontend)**
   * O frontend utiliza a biblioteca Tuna.js para gerar um token do cartão de crédito do usuário, usando o `sessionId` obtido no passo anterior.
   * **Importante:** O token gerado deve ser "singleUse" (só pode ser usado uma vez).
4. **Criação da Reserva (Reservas API)**
   * O frontend envia uma requisição POST para a API de Reservas (`/reservations/create`).
   * Essa requisição inclui os dados da reserva (property_id, check_in_date, check_out_date, etc.).
   * A API de Reservas cria a pré-reserva no banco de dados e na Stays.
5. **Pagamento da Reserva (Reservas API)**
   * O frontend envia uma requisição POST para a API de Reservas (`/reservations/payment/pay`) com os dados necessários para o pagamento. Isso inclui:
     * Dados do cliente (nome, documento, endereço de cobrança, etc.).
     * Dados do pagamento (método de pagamento, token do cartão (se for cartão de crédito), número de parcelas, etc.).
     * Metadata da sessão (endereço IP, etc.).
6. **Validação e Inicialização do Pagamento (Tuna)**
   * A API de Reservas interage com a API do Tuna para validar a sessão do usuário e inicializar o pagamento. Existem dois fluxos principais:
     * **Pagamento com cartão de crédito:** Para pagamentos com cartão de crédito.
     * **Pagamento com PIX:** Para pagamentos com Pix.
   * A API do Tuna pode precisar autorizar e capturar o pagamento (InitPayment).
7. **Recebimento do Webhook (Reservas API)**
   * A API do Tuna envia um webhook para uma rota específica (**/tuna/event**) na API de Reservas, informando o status do pagamento. Ao receber essa informação, a API de Reservas processa os dados e os repassa para um worker.
8. **Atualização do Status do Pagamento**
   * O worker é responsável por atualizar o status do pagamento na tabela `payments` do banco de dados. Inicialmente, a verificação do status do pagamento será feita pelo frontend por meio de polling com backoff na rota `/reservations/payment/status`, evitando requisições excessivas. No futuro, essa abordagem poderá evoluir para um Streaming Response ou EventSource, tornando o processo mais eficiente.
9. **Redirect Detalhes da Reserva (Frontend)**
   * O frontend redireciona o usuário para a página de detalhes da reserva.


**Diagrama do Fluxo**

 ![Diragama do fluxo de integração](/api/attachments.redirect?id=ee27283b-05b8-49a2-850d-13533080f382)

*Disnponível em: <https://miro.com/app/board/uXjVN47euTs=/?moveToWidget=3458764620558850474&cot=14>*

## Registro de Tentativas de Pagamento

Para melhorar o suporte ao cliente e detectar possíveis tentativas de compra suspeitas, o sistema passará a armazenar informações não sensíveis de cada tentativa de pagamento. Isso permitirá que a equipe de atendimento identifique rapidamente padrões irregulares.

Dessa forma, serão salvos o **nome do titular** do cartão e os **últimos quatro dígitos do número do cartão** na tabela `payment_transactions`. 

### Modelagem do Banco de Dados

Para armazenar essas informações, adicionaremos a coluna `payment_details` na tabela `payment_transactions`. Essa coluna utilizará o formato JSON para manter flexibilidade e facilitar futuras alterações.

#### Exemplo

A nova coluna `payment_details` terá a seguinte estrutura:

```javascript
{
  "card_holder_name": "João Silva",
  "last_four_digits": "1234",
  "card_brand": "visa"
}
```

# Referências


---

<https://dev.tuna.uy/api/token/>

<https://dev.tuna.uy/api/payment>

<https://dev.tuna.uy/plugins/javascript>

# Próximas leituras úteis


---

[Guia Interno: Funcionamento do Checkout Interno](/doc/guia-interno-funcionamento-do-checkout-interno-Uu3x3Uksbx)