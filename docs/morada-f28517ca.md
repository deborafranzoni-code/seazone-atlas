<!-- title: Morada | url: https://outline.seazone.com.br/doc/morada-g34UBMBcGh | area: Tecnologia -->

# Morada

# Contexto da Investigação

Estávamos investigando um problema onde um deal não estava sendo criado na plataforma. Durante a análise, identificamos que a API da Morada estava retornando status de sucesso ("Deal created successfully"), porém:

* O deal não era criado no Pipedrive
* A MIA não enviava mensagem no WhatsApp
* O deal não aparecia na plataforma da Morada

Após investigação detalhada, descobrimos que o problema estava no messageTemplate incorreto - ele não correspondia ao instanceId/productId configurados. Quando corrigimos o messageTemplate, tudo funcionou perfeitamente.

Diante disso, decidimos testar outros cenários para entender melhor o comportamento da API em situações de erro.

## Testes Realizados

### Teste 1: messageTemplate incorreto

Este foi o caso real que identificamos durante a investigação.

**POST** `https://mia-integration.morada.ai/api/v1/a032acf1-7b79-4670-bcca-04c2479243b6/deal`

**Payload:**

```json
{
  "name": "Teste de Workflow",
  "email": "johnpaulo0602@gmail.com",
  "phoneNumber": "+5561996973287",
  "productId": "344d1d73-cd69-4551-8236-8d5e61b1ed2b",
  "instanceId": "1527",
  "source": "Busca Paga | Facebook Ads",
  "extras": {
    "campaign": "111222333444_[SI]*[LEAD_ADS]*[RS/SC/PR]_[CBO]*Canas_beach_Spot*|_06/10/2025",
    "medium": "SZP_lead_ads_ponta_das_canas_spot_ii"
  },
  "messageTemplate": "szp_canasbeach_1709",
  "specialInstructions": "Perguntas qualificadoras já preenchidas pelo lead: 1- Você procura investimento ou para uso próprio? R: Investimento - renda com aluguel; 2- Qual o valor total que você pretende investir? R$ 300.001 a R$ 400.000 em até 54 meses; 4- Qual a forma de pagamento? R: À vista via PIX ou boleto"
}
```

⚠️ **Campo incorreto:** `"messageTemplate": "szp_canasbeach_1709"` - não corresponde ao instanceId/productId configurados

**Response:**

```json
[
  {
    "dealId": "86132850-0665-48c7-b976-e1dee1fc2340",
    "message": "Deal created successfully"
  }
]
```

**Resultado:**

* ❌ Deal não foi criado no Pipedrive
* ❌ MIA não iniciou contato no WhatsApp
* ❌ Deal não aparece na plataforma Morada
* ✅ API retornou sucesso (200 OK)

**Impacto:** Perdemos tempo significativo tentando identificar o problema, pois a API indicava que tudo havia funcionado corretamente.


---

### Teste 2: messageTemplate correto (controle)

Após identificar o problema, corrigimos o messageTemplate para validar a hipótese.

**Payload:** Mesmo payload do Teste 1, alterando apenas:

```json
{
  ...
  "messageTemplate": "parceiros_campanhaelp_r"
  ...
}
```

✅ **Campo correto:** `"messageTemplate": "parceiros_campanhaelp_r"` - corresponde ao instanceId/productId

**Response:**

```json
[
  {
    "dealId": "86132850-0665-48c7-b976-e1dee1fc2340",
    "message": "Deal created successfully"
  }
]
```

**Resultado:**

* ✅ Deal criado com sucesso no Pipedrive
* ✅ MIA iniciou contato no WhatsApp
* ✅ Deal visível na plataforma Morada
* ✅ API retornou sucesso (200 OK)

Isso confirmou que o problema era realmente o messageTemplate incorreto.


---

### Teste 3: messageTemplate vazio

Para entender melhor o comportamento da API, testamos enviar o messageTemplate vazio.

**Payload:**

```json
{
  "name": "Teste de Workflow",
  "email": "teste@seazone.com.br",
  "phoneNumber": "+5548998411164",
  "productId": "344d1d73-cd69-4551-8236-8d5e61b1ed2b",
  "instanceId": "1527",
  "source": "Busca Paga | Facebook Ads",
  "extras": {
    "campaign": "111222333444_[SI]*[LEAD_ADS]*[RS/SC/PR]_[CBO]*Canas_beach_Spot*|_06/10/2025",
    "medium": "SZP_lead_ads_ponta_das_canas_spot_ii"
  },
  "messageTemplate": "",
  "specialInstructions": "Perguntas qualificadoras já preenchidas pelo lead: 1- Você procura investimento ou para uso próprio? R: Investimento - renda com aluguel; 2- Qual o valor total que você pretende investir? R$ 300.001 a R$ 400.000 em até 54 meses; 4- Qual a forma de pagamento? R: À vista via PIX ou boleto"
}
```

⚠️ **Campo vazio:** `"messageTemplate": ""` - campo obrigatório enviado vazio

**Response:**

```json
[
  {
    "message": "Deal updated successfully. Conversation already open",
    "dealId": "86132850-0665-48c7-b976-e1dee1fc2340",
    "conversationId": "f627ed29-ede2-4084-9916-c3acf98c0e18"
  }
]
```

**Resultado:**

* ❌ API retornou sucesso mesmo com campo obrigatório vazio


---

### Teste 4: messageTemplate e productId vazios

Testamos enviar tanto o messageTemplate quanto o productId vazios.

**Payload:**

```json
{
  "name": "Teste de Workflow",
  "email": "teste@seazone.com.br",
  "phoneNumber": "+5548998411164",
  "productId": "",
  "instanceId": "1527",
  "source": "Busca Paga | Facebook Ads",
  "extras": {
    "campaign": "111222333444_[SI]*[LEAD_ADS]*[RS/SC/PR]_[CBO]*Canas_beach_Spot*|_06/10/2025",
    "medium": "SZP_lead_ads_ponta_das_canas_spot_ii"
  },
  "messageTemplate": "",
  "specialInstructions": "Perguntas qualificadoras já preenchidas pelo lead: 1- Você procura investimento ou para uso próprio? R: Investimento - renda com aluguel; 2- Qual o valor total que você pretende investir? R$ 300.001 a R$ 400.000 em até 54 meses; 4- Qual a forma de pagamento? R: À vista via PIX ou boleto"
}
```

⚠️ **Campos vazios:**

* `"messageTemplate": ""`
* `"productId": ""`

**Response:**

```json
[
  {
    "message": "Deal updated successfully. Conversation already open",
    "dealId": "86132850-0665-48c7-b976-e1dee1fc2340",
    "conversationId": "f627ed29-ede2-4084-9916-c3acf98c0e18"
  }
]
```

**Resultado:**

* ❌ API retornou sucesso mesmo com múltiplos campos obrigatórios vazios


---

## Impacto na Operação

Esta falta de validação e feedback:

* Dificulta o troubleshooting de problemas em produção
* Aumenta o tempo de resolução de incidentes
* Impossibilita tratamento de erros no workflow/automação
* Deixa a equipe "cega" sobre falhas reais na integração

## Solicitação

Solicitamos a implementação de validação adequada e retorno de erros HTTP apropriados (status 4xx) para os casos mencionados acima e outros possíveis.