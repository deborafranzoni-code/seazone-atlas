<!-- title: Como fazer reenvio de mensagem de extensão para o franqueado | url: https://outline.seazone.com.br/doc/como-fazer-reenvio-de-mensagem-de-extensao-para-o-franqueado-yvvbFBLXce | area: Tecnologia -->

# Como fazer reenvio de mensagem de extensão para o franqueado

# Early Checkin

Endpoint: <https://autowebhook.newbyte.net.br/webhook/techEarlyCheckinExtensionHost/seazone>

Authorization: IKgE8iSkU30A3loT22o6icEvV#0WqyjZ

**Exemplo de Payload:**

```json
{
    "phone": "+5543991633104",
    "original_code": "RSV123",
    "extension_code": "RSV321",
    "property_code": "TST001",
    "checkin": "21/03/2026",
    "checkout": "24/03/2026",
    "checkin_time": "11h",
    "guest_quantity": 2
}
```

OBS: Você encontra o payload verdadeiro pra envio na mensagem de falha que é disparada no canal #alerts-notificacoes-via-whatsapp

# Late Checkout

Endpoint: https://autowebhook.newbyte.net.br/webhook/techEarlyCheckinExtensionHost/seazone

Authorization: xXBRboH1IUSoQUfdpYGNA8cpBIt#qjfv

**Exemplo de Payload:**

```json
{
    "phone": "+5543991633104",
    "original_code": "RSV123",
    "extension_code": "RSV321",
    "property_code": "TST001",
    "checkin": "21/03/2026",
    "checkout": "24/03/2026",
    "checkout_time": "11h",
    "guest_quantity": 2
}
```

OBS: Você encontra o payload verdadeiro pra envio na mensagem de falha que é disparada no canal #alerts-notificacoes-via-whatsapp

# Tutorial

[https://drive.google.com/file/d/1W9NNEuer9fJy6B25mi1e8v23xXUEswvH/view?usp=sharing](https://drive.google.com/file/d/1W9NNEuer9fJy6B25mi1e8v23xXUEswvH/view?usp=sharing)