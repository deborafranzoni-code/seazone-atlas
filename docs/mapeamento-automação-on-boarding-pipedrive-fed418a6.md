<!-- title: Mapeamento automação on-boarding pipedrive | url: https://outline.seazone.com.br/doc/mapeamento-automacao-on-boarding-pipedrive-SA1iN0S2NC | area: Tecnologia -->

# Mapeamento automação on-boarding pipedrive

# Discovery web-hook Pipedrive

## Links

* [Tela de gerenciamento de webhooks](https://seazone-fd92b9.pipedrive.com/settings/webhooks)

### Documentação webhook pipedrive

* [Docs: Exemplos de formatos de retorno de webhook](https://pipedrive.readme.io/docs/webhooks-v2-migration-guide#webhook-v2-examples)
* [Docs: Como criar webhook](https://pipedrive.readme.io/docs/guide-for-webhooks-v2)

### Dicionário de fields pipedrive

`[dealFields](https://seazone-fd92b9.pipedrive.com/api/v1/dealFields?api_token=XXXXXXXXXXXXXXXX)`, `[personFields](https://seazone-fd92b9.pipedrive.com/api/v1/personFields?api_token=XXXXXXXXXXXXXXXX)`, `[organizationFields](https://seazone-fd92b9.pipedrive.com/api/v1/organizationFields?api_token=XXXXXXXXXXXXXXXX)`, `[productFields](https://seazone-fd92b9.pipedrive.com/api/v1/productFields?api_token=XXXXXXXXXXXXXXXX)`, `[activityFields](https://seazone-fd92b9.pipedrive.com/api/v1/activityFields?api_token=XXXXXXXXXXXXXXXX)`, `[noteFields](https://seazone-fd92b9.pipedrive.com/api/v1/activityFields?noteFields=XXXXXXXXXXXXXXXX)`

## Setup webhook

### Criando webhook

**URL**: `https://seazone-fd92b9.pipedrive.com/api/v2/webhooks?api_token=XXXXXXXXX`

**Request Body**:

```json
{
    "subscription_url": "https://0d9777a61c6a.ngrok-free.app/webhook",
    "event_action": "change",
    "event_object": "deal",
    "version": "2.0",
    "http_auth_user": "random_uuid_username",
    "http_auth_password": "99amkd2!@!sssss!sad,00",
    "name": "Sapron test webhook"
}
```

**Response Body**:

```json
{
    "status": "ok",
    "success": true,
    "data": {
        "id": 1828448,
        "name": "Sapron test webhook",
        "company_id": 6083095,
        "owner_id": 16219013,
        "user_id": 16219013,
        "event_action": "change",
        "event_object": "deal",
        "subscription_url": "https://8f4a6457b463.ngrok-free.app/webhook",
        "is_active": 1,
        "add_time": "2026-01-14T17:07:27.000Z",
        "remove_time": null,
        "type": "general",
        "http_auth_user": "v1u:AQIBAHhPHyIcJtrGIXgJua6hr42oO98mZE7trrqAzygDEIJEowHDIhbpbFhjXqUi5Vo4qRXBAAAAfjB8BgkqhkiG9w0BBwagbzBtAgEAMGgGCSqGSIb3DQEHATAeBglghkgBZQMEAS4wEQQMs5NwOaSn7FbCWvacAgEQgDspKkcptP4dHlURgfmql_sLn3fx63F-WJz1BE2jixtIa-mxd7t_WK4b_SB41oN09Ki9_40jdzWbVa6DKw:GOPxtO6nihhpMkj7xK7TEelz_wZkAGFUfmo9VeattrMQeR16S9SOyKAK62-3FBJfP6vks1H7FXqN9sjTi6JBKW8w0wwLbKB1tRnpvrQD1lsY5sTd",
        "http_auth_password": "v1u:AQIBAHhPHyIcJtrGIXgJua6hr42oO98mZE7trrqAzygDEIJEowHDIhbpbFhjXqUi5Vo4qRXBAAAAfjB8BgkqhkiG9w0BBwagbzBtAgEAMGgGCSqGSIb3DQEHATAeBglghkgBZQMEAS4wEQQMs5NwOaSn7FbCWvacAgEQgDspKkcptP4dHlURgfmql_sLn3fx63F-WJz1BE2jixtIa-mxd7t_WK4b_SB41oN09Ki9_40jdzWbVa6DKw:hr_jtO6nihhCwsex6xtT3Lf22QSbB9z3RgPmn092R9TDi5D9DnDiRASytOUkaDNNH7jD02WkHMWPQTF9g-ps1KuHqs21KMoRGWJLzBvmHIdEQgkrfAA",
        "remove_reason": null,
        "version": "2.0"
    }
}
```

### Deletando webhook

**URL**: `https://seazone-fd92b9.pipedrive.com/api/v1/webhooks/<ID>?api_token=XXXXXXXXX`

**Response Body**:

```json
{
    "status": "ok",
    "success": true
}
```

### Como funcionaria a Autenticação do webhook?

O webhook permite a inclusão de http user e http password. Pode-se utilizar esses campos de header para incluir alguma autenticação, oferecendo maior segurança ao fluxo.

Outra opção é incluir um token na url, utilizando https:

**Exemplo utilizando http headers**

```json
{
    "subscription_url": "https://url.com",
    "event_action": "change",
    "event_object": "deal",
    "version": "2.0",
    "http_auth_user": "user",
    "http_auth_password": "password",
    "name": "Sapron deals"
}
```

**Exemplo utilizando url param**

```json
{
    "subscription_url": "https://url.com?token=112391290-asdasd92-asdasd3123",
    "event_action": "change",
    "event_object": "deal",
    "version": "2.0",
    "name": "Sapron deals"
}
```

## Mapeamento de campos vindos do payload

### Identificadores de deal e estágio

* `meta.entityId` - Id do deal (DealID)
* `data.stage_id` - Estágio atual do deal (colunas do painel kanban)
* `previous.stage_id` - Estágio anterior do deal (colunas do painel kanban)
* `data.status` - Status atual do Deal: (**Aberto** (`open`), **Ganho**(`won`) ou **Perdido**(`lost`)
* `previous.status` - Status anterior do Deal

### Valores de payload

* `meta` - Apresenta valores que identificam a entidade, a ação aplicada à entidade, e demais "meta" informações
* `data` - Apresenta todas as informações atuais da entidade, não só as alteradas
* `previous` - Apresenta os dados anteriores da entidade (**APENAS OS CAMPOS ALTERADOS**)

### Mudança de status

O status do deal identifica se o mesmo está **Aberto** (`open`), **Ganho**(`won`) ou **Perdido**(`lost`).

No momento de mudança desse valor, os seguintes campos são criados/alterados:

* `data.status` \[String\] - Status atual do Deal
* `previous.status` \[String\] - Status anterior do Deal
* `close_time` \[DateString\] - Data encerramento do Deal
* `won_time` \[DateString\] - Data em que Deal foi "**Ganho**"

### Um exemplo (com `data` recortado) de payload enviado ao web-hook, ao pressionar `Ganho` no deal do pipedrive é:

 ![](/api/attachments.redirect?id=f32fe877-2044-4948-a6db-fd195b93d1bb " =4380x1002")

```json
{
    "meta": {
        "action": "change",
        "entity_id": "213973",
        "entity": "deal"
    },
    "data": {//Recortado para visualização
        "close_time": "2026-01-14T17:18:22Z",
        "status": "won",
        "update_time": "2026-01-14T17:18:22Z",
        "won_time": "2026-01-14T17:18:22Z"
    },
    "previous": {
        "close_time": null, //Não existia antes
        "status": "open",
        "update_time": "2026-01-14T17:18:20Z",
        "won_time": null //Não existia antes
    },
}
```

No payload acima o status anterior do deal era **Aberto**, e o mesmo foi tido como **Ganho**.

### Já ao reabrir o mesmo deal, depois que este está "Ganho":

 ![](/api/attachments.redirect?id=22c3eb24-d8f2-449e-8c24-9de6bb3c4b56 " =4380x1002")

```json
{
    "meta": {
        "action": "change",
        "entity_id": "213973",
        "entity": "deal"
    },
    "data": { //Recortado para visualização
        "close_time": null, //Set to null
        "status": "won",
        "update_time": "2026-01-14T17:18:28Z",
        "won_time": null //Set to null
    },
    "previous": {
        "close_time": "2026-01-14T17:18:22Z",
        "status": "won",
        "update_time": "2026-01-14T17:18:22Z",
        "won_time": "2026-01-14T17:18:22Z"
    },
}
```

### Ao alterar de **Aberto** para **Perdido**:

 ![](/api/attachments.redirect?id=6caf5ba2-f673-4f90-a1d9-a272b4c0bfe8 " =4380x1002")

```json
{
    "meta": {
        "action": "change",
        "entity_id": "213973",
        "entity": "deal"
    },
    "data": { //Recortado para visualização
        "close_time": "2026-01-14T17:18:17Z",
        "update_time": "2026-01-14T17:18:17Z",
        "lost_time": "2026-01-14T17:18:17Z",
        "lost_reason": "Duplicado/Erro",
        "status": "lost"
    },
    "previous": {
        "close_time": null, //Não existia antes
        "lost_reason": null, //Não existia antes
        "lost_time": null, //Não existia antes
        "status": "open",
        "update_time": "2026-01-14T17:18:03Z"
    },
}
```

### Por fim, reabrindo um Deal (de **Perdido** para **Aberto)**:

 ![](/api/attachments.redirect?id=457d4161-b1f1-4986-b007-24623179fd66 " =4380x1002")

```json
{
    "meta": {
        "action": "change",
        "entity_id": "213973",
        "entity": "deal"
    },
    "data": { //Recortado para visualização
        "close_time": null, //Set to null
        "update_time": "2026-01-14T17:18:20Z",
        "lost_time": null, //Set to null
        "lost_reason": null, //Set to null
        "status": "open"
    },
    "previous": {
        "close_time": "2026-01-14T17:18:17Z",
        "lost_reason": "Duplicado/Erro",
        "lost_time": "2026-01-14T17:18:17Z",
        "status": "lost",
        "update_time": "2026-01-14T17:18:17Z"
    },
}
```

### Mudança de estágio (stage_id)

### Movendo card de Deal de estágio `Aguardando Dados` para estágio `Contrato`:

```json
{
    "meta": {
        "action": "change",
        "entity_id": "213973",
        "entity": "deal"
    },
    "data": { //Recortado para visualização
        "stage_id": 428
    },
    "previous": {
        "stage_id": 427
    },
}
```

### Movendo card de Deal de estágio `Contrato` para estágio `Aguardando Dados`:

```json
{
    "meta": {
        "action": "change",
        "entity_id": "213973",
        "entity": "deal"
    },
    "data": { //Recortado para visualização
        "stage_id": 427
    },
    "previous": {
        "stage_id": 428
    },
}
```

### Mudança de valores customizados

Boa partes dos campos de Deals são customizados (não nativos do pipedrive, e criados manualmente por nós para compor os dados de um Deal). 

Esses campos são disponibilizados dentro de `customFields` - tanto em `data` (dados atuais) quanto em `previous` (dados de campos anteriores que foram alterados).

Além disso, esses são identificados por um "hash", e não pelo seu nome - normalmente dificultando o consumo direto dos dados - sendo necessário uma transformação dos mesmos.

### Mudando Taxa de Adesão de `131` para `13`:

```json
{
    "meta": {
        "action": "change",
        "entity_id": "213973",
        "entity": "deal"
    },
    "data": { //Recortado para visualização
      "custom_fields": {
        "ba4ef52ee7f02f22ba933da067b00d9c9ec807ea": {
          "currency": "BRL",
          "type": "monetary",
          "value": 13
        }
      }
    },
    "previous": {
      "custom_fields": {
        "ba4ef52ee7f02f22ba933da067b00d9c9ec807ea": {
          "currency": "BRL",
          "type": "monetary",
          "value": 131
        }
      }
    }
}
```

Como pode-se perceber, os *hashes* dificultam a fácil identificação dos campos; sendo necessário processamento anterior, a depender da situação.

O Sapron já realiza tratamentos semelhantes ao consumir dados do Pipedrive (`src/property/integration/pipedrive/pipedrive_handover.py`). O dicionário de dados já existente (em `src/channel_manager/action/pipedrive/helper_translation.py`)pode ser facilmente reutilizado.

O tratamento para o consumo dos campos customizados é feito com base no [dicionário de fields](https://outline.seazone.com.br/doc/mapeamento-web-hook-pipedrive-SA1iN0S2NC#h-dicionario-de-fields-pipedrive). No caso de fields de deal, deve-se consultar os `dealFields`.

### Mudando Formas de pagamento:

```json
{
    "meta": {
        "action": "change",
        "entity_id": "213973",
        "entity": "deal"
    },
    "data": { //Recortado para visualização
      "custom_fields": {
        "3e9bb7da4983ebebda9e19851cc6828af134e3c8": {
          "id": 4581,
          "type": "enum"
        },
        "7820e36ef78eb6f5ea15064f7da55adab6a0c4a2": {
          "id": 4573,
          "type": "enum"
        }
      }
    },
    "previous": {
      "custom_fields": {
        "3e9bb7da4983ebebda9e19851cc6828af134e3c8": {
          "id": 4581,
          "type": "enum"
        },
        "7820e36ef78eb6f5ea15064f7da55adab6a0c4a2": {
          "id": 4573,
          "type": "enum"
        }
      }
   }
}
```

No payload acima mudou-se os métodos de pagamento (entrada e restos) para "Pix" - anteriormente estava em "Cartão".

### Quais mudanças no deal triggam o webhook?

Qualquer edição em uma entidade de deal trigga o webhook configurado com a action de `change`.

Por exemplo, edição no `status`, `stage_id` (estágio) e valores de detalhe - como valor de implantação e `person_id`.

### Quando o webhook é ativado? (quando termina a edição de um campo? Tem botão pra salvar?)

Cada webhook pode ser configurado para "ouvir" um tipo de ação de uma entidade.

Considerando um webhook que "ouça" edições de Deal, esse só será acionado quando edições forem realizadas no Deal - e um botão de salvar seja pressionado.

No caso de um webhook que ouça a "criação", esse receberá notificações no momento da criação da entidade - e.g., criação do Deal.


### Como se comportaria o webhook com edição multipla de dados? (várias chamadas, sendo um pra cada campo? Apenas uma com todos os campos modificados?)

No payload enviado ao **webhook**, sempre é realizado o envio de todos os dados atuais do Deal.

Depende da maneira que o usuário realizar as alterações na interface.

No pipedrive, ao lado de cada campo, é possível pressionar um ícone de edição. Ao fazer isso, é apresentado um botão de "*Salvar*" ao lado do campo editado. Ao clicar em "*Salvar*", apenas o campo editado é enviado (mesmo que várias caixas de diálogo de edição semelhantes estejam abertas). Portanto, uma request ao webhook é esperada para cada campo alterado.

 ![](/api/attachments.redirect?id=1480af26-a8e6-43c9-9eb7-d00aad724a8c " =428x171")

Outra forma de edição que o pipedrive oferece é a edição em massa dos detalhes dos deals. Isso é feito clicando no lápis ao lado de **Detalhes** na tela do Deal. Dessa forma, apenas um botão de salvar é apresentado no canto inferior da tela (ao invés de um botão de salvar para cada campo editado). Caso esse tipo de edição seja feita, espera-se que todas as alterações sejam enviadas em uma mesma request ao webhook.

 ![](/api/attachments.redirect?id=b3fd6856-4611-4fd0-b540-e72761080e58 " =385x460")

É importante ressaltar que a alteração de `status` do Deal não parece poder ser feita no modo de edição em massa. Portanto, é de se esperar que a requisição que informe a mudança de `status` seja enviada de forma isolada a outras mudanças para o `webhook`. O mesmo se aplica à mudança de `stage_id`

### Quais eventos temos que considerar no fluxo? Só de update, ou criação de deal também?

É possível criar Deals diretamente na coluna de contrato. No entanto, não parece ser um procedimento muito correto.

Caso seja necessário considerar operações desse tipo, será preciso considerar, também, eventos de criação, além de atualização.


## Exemplo payload completo

```javascript
{
  "data": {
    "add_time": "2025-12-23T15:39:38Z",
    "channel": null,
    "channel_id": null,
    "close_time": null,
    "creator_user_id": 12597982,
    "currency": "BRL",
    "custom_fields": {
      "f0e7dc75928ee7be1d26b6ed65df1e26e944468d": null,
      "3e9bb7da4983ebebda9e19851cc6828af134e3c8": {
        "id": 4581,
        "type": "enum"
      },
      "f06f042452d68bd8b3815643382d7ed5ab5039c4": null,
      "0083d30d9321aec4213ffa6302b32fd1dca9ee6a": null,
      "b57803776a6cd6e6b2b0cb8eecaa34b03e3d3eee": {
        "id": 24233717,
        "type": "user"
      },
      "6ca9743c75415fcd288c24a253be60b31b1fa485": null,
      "f3cdd699709458ba3a87920b0056f88475ba4889": null,
      "1bd6ce9f14cff4db8927ad6cae063e0677f22771": null,
      "2d9366d435709f012cb322f6bba8c71ab7bfbbdc": null,
      "9e80a38aa09a0f876ea5f9df97865bdbbdcfa9fa": null,
      "1c3dc0c98ef8eb86957c390f9cc7208dec66a24e": null,
      "d9ff798ceaf7b0e0c4474097e28221ebe13c7c03": null,
      "45a56c6ae1f43dad4992c3c23d4a2a32787d93d6": null,
      "79e7aad4ac885a3bc9035ee600da3c38ee6a7b50": null,
      "fd9c1b3f0ed391a16f6c781eab63cdedf6bf158d": null,
      "e57dccd11f905f7d2a2994ef4c8f2b837c77f8bf": null,
      "d54e07b14f854746b35ba95ba690eae6c95e11ab": null,
      "865ee61b82fd78c0f8db9dcd7ff12b08dff9e85f": null,
      "c470e77592aace667105d682c28007d10bf429b0": null,
      "34a7f4f5f78e8a8d4751ddfb3cfcfb224d8ff908": null,
      "080b69c6b4122f0aa605af474041393da4c7fc3c": null,
      "d569e5a825ffd77438d40d7e80440a71f843c084": null,
      "e864cd09e824b7cfd4fae889cf47b3affd28d108": null,
      "2f69d6d079f566c78a57f9a2ec4a21a0ffd330b0": null,
      "ee5481f2abd44489d23aa80ce973d9a98de03f14": null,
      "f30bcfa05b0e1b84f166fc3e0ef9b7f7d45b2bb7": null,
      "977b711b69cf4efd9f5221bf17600b7e23b94256": null,
      "02a0e6533ac7d71e3ffbb0fe89b635cd47ee32e8": null,
      "7820e36ef78eb6f5ea15064f7da55adab6a0c4a2": {
        "id": 4573,
        "type": "enum"
      },
      "99ac7cd8c5d6af9bd0a1273521a973810ec286c4": {
        "id": 4519,
        "type": "enum"
      },
      "482743d11858b0b2fe9998647f468a3f05a81969": null,
      "450d78a6dd5adcce45644cba36598aca90204016": null,
      "97f55d5e3f0dc4e6d280162a84f6ea761c7d3435": null,
      "a8ec7059c4bf29cbce20e84fabcf429eeb952f5d": null,
      "e446c37fb126d0a122ae3a1d2f6a5b5716038731": null,
      "7ee36ac719ef6db4c41e9f7ecee736e9aa27e14e": null,
      "f9765a66bff46cef68ef99bfd9cc5819f39f91b3": null,
      "584237f6a263f4e8c1392eecbdcbc202909c763c": null,
      "6254ed96b26cbeffbd31dd664ff8bcd23ef848e7": null,
      "b61d7d3382930314f2648b669882e3b9a5dbc7a1": null,
      "f6e772cef68615e66078357f13023d266bfa7ccc": null,
      "0f54127ee7cc50bf9a9c7d1d583a615b0d636396": null,
      "0b8e64b86461600ab9abe5b165774a03d18d036b": null,
      "73b368067f8d69417f89e12a4d0b20319cfb56a0": null,
      "efeaf16b0bc4ca4f43cc2cce7522886cc47995b3": null,
      "201152c12b05b631e8b1774bcc19866c7e0ddb40": null,
      "2c6726e93834466fd2563167499a3dcc8c512ea9": null,
      "3720b8df53254908844a712b9a6b5af8ded03d69": null,
      "5aba2dc71780ec797b4e110e8f8f4238eb14b87e": null,
      "b865dc9db6a6f527cbde2f5ccfcb6748c1af6afd": null,
      "fdb38b0c2ecfc13e5585bcb43380bedf0783820e": null,
      "93b3ada8b94bd1fc4898a25754d6bcac2713f835": null,
      "3572b09c1953442131354333cc4123a321f342f2": null,
      "f26e8840030ddf23ecf1e8183280b113ac5e80ba": null,
      "54f9c76b34465844f7a5058ee730b64988ebd80e": null,
      "837653ab193c6a293b346fb464a8a89c6259bc0b": null,
      "0adfea58c96df1a21eee3b0da8462bbe58a9d029": null,
      "ff3b1accdc5750aa80cb37b25ef9f2a8ad259f50": null,
      "103afd93c07760d5918b9daf1d6e9e1b52bbd7e5": null,
      "d0ac708e265df3324f6c217f2f96526132479e3b": null,
      "5bdb6b55fed977e940d2ce1f8282dd09972feda9": null,
      "bd63d72258777eff54025780ff1f164cd769a1c6": null,
      "098777fe93b8f0fd6211b063d1d0d30975d7d151": null,
      "4050905156f071d7c38fccc673d29dcd630a2ddb": null,
      "00c1c0fad0e97c3d7d9c8d08c7cc9cf1c474a11f": null,
      "a7c77267b3676bc817ce23ce4b0d72c16018540e": null,
      "658f16abb8e4d9ca1c4426664a48e9a82c390bb5": null,
      "bfafc352c5c6f2edbaa41bf6d1c6daa825fc9c16": null,
      "874c52cec53c7eb63f001d790d1448f7eabb7c2c": null,
      "34336364766f24e1b2fdb25beec9c87856f3ade3": null,
      "ef15468498ed62ef0785a2b9b9230832a83b6d73": null,
      "ce82c3dbb939c391578abeeb1737a04090c1fc7f": null,
      "55bb0bbb3ffd7ac235c453d8c237fa2edcf6fb44": null,
      "793bfc5e4f36ca3a6cd01ae0db08ab7da0f5f085": null,
      "0fc5bd6f32888da0c4d5e1dc6333f72ce25c24f8": null,
      "8d0bd03aea93c04be6576cd6704be03bff44953f": null,
      "de96f2242234b7f854c46ab3cd6212ae7f052c61": null,
      "5ae1b70b2c84cb6af6ca817167bed75a47cbeca4": null,
      "d32bbc9e7063e851899a92e7de97a00fcacddba3": null,
      "2007fa80d665391ce13bfebd8cb4f807fbe4a9a4": null,
      "67afb3066b794ed1f9c93147e99dfc3072e9b18f": null,
      "b002278ee324f27470d7baf3d7ca17b81ed91ca3": null,
      "045b835b9180724125743b8f64abfdab73149946": null,
      "5552f14e1c39e12156fd2b769c82ebaa5ea2ecd5": null,
      "59e41246486ea84188afdde60244473fa4a5f20f": null,
      "8b9019e7cba60c34339afac61004c215590eaee9": null,
      "5d5ae6a7427a001f1b22cf2fa4aa0298269c3c28": null,
      "24168b2266d01ba9c14b4d4fddace1b40c139e38": null,
      "7bc0974cf2eec36d00013d3f1d6037af80b09c84": null,
      "c9875de8dc59b6bab8b414fbf1e483b45cde5f3a": null,
      "22232c3b1a667ff1c81b143f7b9e41f6cb1ecc2c": null,
      "1fd07015419c1f23c5b916c23a2378fa98b47f92": null,
      "6d565fd4fce66c16da078f520a685fa2fa038272": null,
      "f9b23753a78ed314d9ad42f51a9dd02da0b8c751": null,
      "ba4ef52ee7f02f22ba933da067b00d9c9ec807ea": {
        "currency": "BRL",
        "type": "monetary",
        "value": 13
      },
      "145c0d27deafcc3bf3298867ee88db1d770050da": null,
      "03fd3594ff0804d2b16d5410c2fc1552c5dd24c9": null,
      "5c2b5585058df45ab36ce6a66eff9dd3dafc63c9": null,
      "a99270a44f7fabae328750f26155fc8b652d6766": null,
      "e218b3efb7a308a77c142e5f3af73994a0c676eb": null,
      "246d5d76742448ec804a227160510af7fd0410da": null,
      "97b8b2636b120e75017192174f2dbd5a0b3f0915": {
        "id": 24914100,
        "type": "user"
      },
      "3dda4dab1781dcfd8839a5fd6c0b7d5e7acfbcfc": null,
      "6c9ac3132a67cd17c2de3e65f2958896eb34daf0": null,
      "b0e0cbf9246fd732d2ba6b3d988d5a8f6b335fb3": null,
      "735817cc8c69cf68d0c4ffd8fd14b4f5df400253": null,
      "ed3cbe736c5865ea340729f173a4c77d41456964": null,
      "f7b4f7509328a05b7d6d3a1b190f4e1bee882b1f": null,
      "a2abd1ecf59e6d6f6f959a2a62ab40e0e4fd0476": null,
      "d83403e00ded540a62123ee397a0a60ea8d380aa": null,
      "9b517f1d69fe9daca3dc9aebdc60bf58e0c823da": null,
      "f35730ade22660355a1203f13e8524515ecee03b": null,
      "29da9f727ff0dcf5b897598f226aa6d4bc4daff9": null,
      "2c16cb2b8800d6f0da8e8153069c7f974b3d2218": null,
      "42dcfbb94323493caab978135b8f8a7d9f461160": null,
      "9f8adce5d4c5bf336f6462039dd44499a395c460": null,
      "92315902a51b252ab697f846e56381bade14d0a0": null,
      "90b3ed79d43aa61d48754fa30ae6ac71f9aa5c40": null,
      "d7dadb61cca3e75c733dacf964c67a34ae2f05a5": null,
      "be1b51ee4b6b8789ace3f5aea8984c132c357ddf": null,
      "ca6179ea1d899f7aa2e606778dceb37575acaa12": null,
      "f0552384ddb5188742c24f92c586ffd08bdec76e": null,
      "0a9ba7bb5afc8d6f4d804409509438751a49467f": null,
      "99ef0c4d2d06adbaf8e15f53307ab3d02e94852e": null,
      "3fb7223893dba3826f30ad1ceb89d87c433cfa5c": null,
      "37d0071f440d9c207562fec40dcbbff138a7527e": null,
      "6ddc4d167e91119b128e409681f09dbaef21a0d1": null,
      "e2fe29bae351f75e38de04c24081a6307742945b": null,
      "c09def1becff392dca370515fb3c3c075e7c6510": null,
      "bf0e5193f43a49b36990c4ea88c91e01d0858592": null,
      "60e7807427e01cbb6136770320d952d2dd496449": null,
      "7c49d85470c1c8a553fa0faee757883157b7830b": null,
      "06b8065d60ead44cf748bc592d75f67e6cdfb0b5": null,
      "9695a54a9d6c7681efd2b637594a3b621afcbe1f": null,
      "652d1f64ee566754bbadd24ffa61fbb10eed71fd": null,
      "9febb1135cb019af2ea4149d12a0f4d97166a397": null,
      "fdadff5edff5129924c72b855537ca1d1cac57f9": null,
      "ff53f6910138fa1d8969b686acb4b1336d50c9bd": null,
      "e39148bd60e894ca6de63447c3223ec2c3f9b06e": null,
      "3b6419d7a9a8aeb60aff65af19850ad3ea50d172": {
        "currency": "BRL",
        "type": "monetary",
        "value": 0.5
      },
      "1849ccc7ebd54cbba6d23ad2fa880b5924583d28": null,
      "0453a336c5b47ac53c6199a9fb2704bcf7656143": null,
      "96b09dbfa04d9e933b3a4c5482fc21b70d72a00a": {
        "id": 4520,
        "type": "enum"
      },
      "b7dc3918429fb7f0f6f2237b482358b23cac290d": null,
      "3b98ee509fb074a7a50d3b5765c0268e9ad1a6c5": {
        "id": 4578,
        "type": "enum"
      },
      "6a67dcd2a5eb768783594f34fe04e3b11eecbcf6": null,
      "2f1355b7d1e415ccc1ec577cba5374edbfa8efdd": null,
      "1d144b4cff4159b9d8ff1b2db0546c4db53d814c": null,
      "8122fd6fc7a9944c2e726a41c5ad7385c0e943e8": null,
      "1f0263a7f2c9e02f721de0d3f614ecae839a3920": null,
      "c08785e1d2a6bd55caeb88b4ab8ebe9975bf9b4d": null,
      "602d767eee5a8dd5777105efc67c440edb078f64": null,
      "42dfa3c3d13841cef91ffd180528fb57da35778e": null,
      "91eb0c4fb082cf1d6ba88f793a6760234d6350bb": null,
      "9de076a8339ef5dbc3a17bc1188d02e27f04d4d5": null,
      "e7c1cc91f88eeb3c1acda37b9f6fd29d85161665": null,
      "0b8546d3ab3156224126675b930d5d5c4061fa04": null,
      "d541515e91453b2afa4798e857718aa84bb646d9": null,
      "e13d4e4a19f96f113cf9df5800c92af76745144a": null,
      "0991df803259514d51f357faf6c34a88dea9408a": null,
      "06761b52efa6330ad0e05ad92179b62ca7973f26": null,
      "1f91c7451cf87c5f7e69b4af88e04ee0b3655358": null,
      "68702a05ba43ad9741e60df20946fc7110e300f4": null,
      "2af66953d9591fe3530dda00c5f42679b9816530": null,
      "41aa2e7401e2c0f7bf7af95b086c75f58af4633c": null,
      "303890fa11d5956c86eff382b2afe99228e707a4": null,
      "b55b9f7bb5ea134aef1f76b81e08337fbc3e52d0": null,
      "38f50c904c135ea1a2d32163913a88344a8c00df": null,
      "b8adb13f342b421a251f1de63c7dd611ba2fae4e": null,
      "0dd2e7cefd18c944b57d37341af44e4f9fb3c25a": null,
      "513842e3c26022708be47ac08075e719fa366dbe": null,
      "25433aba790ae2baf01bf294219a6a3905e46eb8": null,
      "39707010cc80429443d86f044734f0d5a48b70fd": null,
      "b7000259c867ab50c3d1d0d7e136119405dcd384": {
        "id": 25175614,
        "type": "user"
      },
      "d8a8e0ee6135f606fc8028b865b6630a6397d175": null,
      "29e54585b9cb741be0b6057b6525d2d90c0d6b9f": null,
      "5560779bb633df6c9916f48ad4062d76ffcd2d06": null,
      "95d024f3ecb12760726d846dd0c0201eba17dd5d": null,
      "92426bb24e9f37e47d755b202dc8f8dff8836060": null,
      "bc5189ab694b798cd4d006853659449dc6c65404": null,
      "bc74bcc4326527cbeb331d1697d4c8812d68506e": null,
      "baf019ccd4c4c4032c5a821b5a24265f3243c3b5": null,
      "dce77e93bde83f41a8bdda3087e311431e16bd60": null,
      "354081d444f8028911d9a5408df1fd595d5a0c5a": null,
      "4a8613a99f0c93407c71e09de49a587d7d5ea78e": null,
      "2a062c5a71efa915d3d54c92acd9c0e21a1396c3": null,
      "89624decc4638ac48f396b69329835c225e659d7": null,
      "d0170b1c04837b758dedcce7c7bbf3ee9b332240": null,
      "00ede418b181ace17f30918a19a20a0214edc0eb": null,
      "4ac233d6136c7eb0535d0dad3b2c3dac4c03bf38": null,
      "30f1a980807b764e039980eba100130a44f7c002": null,
      "40092ba51dc1f608466216a68da647d456c4b259": null,
      "93d82411830f9274f9cd72a1ec1fd21a55aadc51": null,
      "ee7b1a2521cc3a95eefdaa47611ad18572bd1a2f": {
        "id": 147834,
        "type": "people"
      },
      "fa80cea4e83bc634acc36dd345b4ee4cb461170f": null,
      "92b196fb1b3ea4ec19e682f6fa932db0f2a34e08": null,
      "ba27517f4313b074f3f7400db6813c6b77c0bd3c": null,
      "7a14dd6a8800addb917cef9b5c2f52230a0fe1f0": null,
      "d29284909b76d150b8b2edb62eeca362c7012fa4": null
    },
    "expected_close_date": "2025-12-23",
    "first_won_time": "2026-01-14T17:08:04Z",
    "id": 213973,
    "label_ids": [],
    "lost_reason": null,
    "lost_time": null,
    "org_id": 5063,
    "origin": "ManuallyCreated",
    "origin_id": null,
    "owner_id": 12597982,
    "person_id": 176578,
    "pipeline_id": 50,
    "probability": 1,
    "stage_change_time": "2026-01-14T18:16:56Z",
    "stage_id": 428,
    "status": "open",
    "title": "TESTEMORANGO001",
    "update_time": "2026-01-14T18:16:56Z",
    "value": 112,
    "visible_to": "3",
    "won_time": null,
    "is_archived": false,
    "archive_time": null
  },
  "previous": {
    "stage_id": 427
  },
  "meta": {
    "action": "change",
    "company_id": "6083095",
    "correlation_id": "bc60674a-2e3d-404c-a268-42945daf16fc",
    "entity_id": "213973",
    "entity": "deal",
    "id": "6ba407fc-006d-4556-9804-8298e584a288",
    "is_bulk_edit": false,
    "timestamp": "2026-01-14T18:16:56.057Z",
    "type": "general",
    "user_id": "12941358",
    "version": "2.0",
    "webhook_id": "1828483",
    "webhook_owner_id": "16219013",
    "change_source": "app",
    "permitted_user_ids": [
      "9251590",
      "10540315",
      "11768759",
      "11778201",
      "11800647",
      "11800651",
      "11816549",
      "12315763",
      "12339010",
      "12457249",
      "12457252",
      "12457255",
      "12597982",
      "12681439",
      "12698731",
      "12710325",
      "12928327",
      "12938344",
      "12941358",
      "12952153",
      "12953381",
      "12988079",
      "12992116",
      "12997084",
      "13031569",
      "13104961",
      "13104972",
      "13132263",
      "13184689",
      "13220982",
      "13236851",
      "13255151",
      "13257109",
      "13268315",
      "13291030",
      "13339386",
      "13346598",
      "13433542",
      "13464357",
      "13478730",
      "13494581",
      "13610162",
      "13619878",
      "13647037",
      "13647048",
      "13666489",
      "13689259",
      "13689270",
      "13713690",
      "13822359",
      "13857082",
      "13877788",
      "13877799",
      "13913604",
      "14007221",
      "14015981",
      "14034105",
      "14064674",
      "14105741",
      "14141865",
      "14148190",
      "14150012",
      "14152865",
      "14214212",
      "14214223",
      "14250464",
      "14261545",
      "14274184",
      "14303675",
      "14303851",
      "14316453",
      "14338875",
      "14338886",
      "14339843",
      "14415655",
      "14455310",
      "14499640",
      "14523554",
      "14603590",
      "14619914",
      "14666752",
      "14725173",
      "14725184",
      "14871759",
      "15114558",
      "15114580",
      "15238455",
      "15264756",
      "15296069",
      "15316665",
      "15316676",
      "15333249",
      "15430053",
      "15555343",
      "15555354",
      "15555365",
      "15594140",
      "15833309",
      "15898011",
      "15898022",
      "16130606",
      "16130617",
      "16174617",
      "16196144",
      "16208211",
      "16219013",
      "16219398",
      "16249659",
      "16250638",
      "16254510",
      "16254521",
      "16254532",
      "16477260",
      "16538464",
      "16538475",
      "16565414",
      "16606411",
      "16606422",
      "16663732",
      "16688416",
      "16696578",
      "16747629",
      "16747651",
      "16771972",
      "16809053",
      "16811726",
      "16811737",
      "16811748",
      "16814641",
      "16825740",
      "16860247",
      "17031704",
      "17100300",
      "17177443",
      "17241529",
      "17241540",
      "20668254",
      "20694819",
      "20694830",
      "20705467",
      "20767188",
      "21130595",
      "21175442",
      "21241233",
      "21330113",
      "21454402",
      "21490680",
      "21550201",
      "21581496",
      "21655493",
      "21856969",
      "21923816",
      "21939810",
      "21999573",
      "22038293",
      "22042517",
      "22198035",
      "22226096",
      "22228901",
      "22232773",
      "22304757",
      "22308552",
      "22344434",
      "22418530",
      "22440321",
      "22440431",
      "22454885",
      "22454896",
      "22470395",
      "22470406",
      "22552543",
      "22579295",
      "22579306",
      "22630874",
      "22630885",
      "22633074",
      "22657065",
      "22683619",
      "22695741",
      "22733636",
      "22784907",
      "22784918",
      "22784929",
      "22787415",
      "22795522",
      "22795533",
      "22795544",
      "22796325",
      "22796347",
      "22805334",
      "22834297",
      "22884677",
      "22887471",
      "22978287",
      "22995865",
      "23065759",
      "23069180",
      "23084492",
      "23093963",
      "23098264",
      "23126424",
      "23171788",
      "23207626",
      "23207637",
      "23207648",
      "23347348",
      "23379281",
      "23379897",
      "23426933",
      "23427428",
      "23454829",
      "23541432",
      "23585487",
      "23635350",
      "23728322",
      "23882201",
      "23972302",
      "24014773",
      "24029172",
      "24085316",
      "24112101",
      "24139172",
      "24139634",
      "24233717",
      "24293513",
      "24293524",
      "24360954",
      "24360976",
      "24421080",
      "24480689",
      "24487553",
      "24505263",
      "24536558",
      "24537273",
      "24540111",
      "24564333",
      "24595078",
      "24602767",
      "24602778",
      "24619685",
      "24655501",
      "24655512",
      "24656920",
      "24665841",
      "24690789",
      "24690976",
      "24760430",
      "24775049",
      "24799887",
      "24806839",
      "24806850",
      "24806861",
      "24814088",
      "24825902",
      "24862323",
      "24894311",
      "24897556",
      "24914100",
      "24914177",
      "24918170",
      "24996787",
      "24997667",
      "25007501",
      "25036893",
      "25084699",
      "25095204",
      "25131416",
      "25131427",
      "25131438",
      "25131449",
      "25152558",
      "25175603",
      "25175614",
      "25210330",
      "25232682",
      "25255661",
      "25291664",
      "25369907",
      "25369918"
    ],
    "attempt": 1,
    "host": "seazone-fd92b9.pipedrive.com"
  }
}
```

# Mapeamento fluxo web-hook Sapron

## Fluxograma back

```mermaidjs
flowchart TB
    A["Start"] --> B["Autentica user do Pipedrive"]
    B --> C{"Autenticação bem sucedida?"}
    C -- Não --> D["Retorna erro 401"]
    C -- Sim --> E@{ label: "event_action == 'update' e event_object == 'deal'?" }
    E -- Não --> F["Sem ação"]
    E -- Sim --> G@{ label: "data.stage_id == 428 e status mudou de 'open' para 'won'?" }
    G -- Não --> H["Sem ação"]
    G -- Sim --> I{"Deal já processado na tabela property_handover_details?"}
    I -- Sim --> J["Retorna erro 422 - Unprocessable"]
    J --> SLACK_ALERT["Comunica erro no slack"]
    I -- Não --> K{"Validações de dados de proprietário e propriedade estão OK?"}
    K -- Não --> L["Retorna erro 400 - Bad request"] & M["Cria endereço proprietário"]
    L --> SLACK_ALERT
    N["Cria usuário do prop"] --> O["Cria Role de owner para prop"]
    O --> P["Cria endereço de propriedade"]
    P --> Q["Cria invoice_details"]
    Q --> R["Cria propriedade"]
    R --> T["Envia email de onboarding"]
    T --> _["Comunica sucesso no slack"]
    S["Gera senha temporária pro owner"] --> N
    M --> S

    E@{ shape: diamond}
    G@{ shape: diamond}
```


\
## Implementação

### Fluxo de Dados

```mermaidjs

flowchart TD
    subgraph Pipedrive["Pipedrive"]
        D[Deal marcado como Ganho]
    end

    subgraph Webhook["Webhook Layer"]
        W[PipedriveDealWebhook]
        T[Celery Task]
        H[PipedriveDealOnboardingHandler]
    end

    subgraph Service["Service Layer"]
        S[OnboardingAutomationService]
        PH[PipedriveHandover]
        NORM[onboarding_helpers<br/>Normalização de dados]
        CS[CredentialsService]
    end

    D -->|Webhook POST| W
    W -->|Enfileira| T
    T -->|Roteia| H
    H -->|should_handle?| H
    H -->|Executa| S
    S -->|Busca dados| PH
    PH -->|Dados brutos| NORM
    NORM -->|Dados normalizados| S

    S -->|Verifica owner| CHECK{Owner existe?}
    CHECK -->|Sim| EXIST[Fluxo Existente]
    CHECK -->|Não| NEW[Fluxo Novo Owner]

    NEW --> ADDR1[Endereço Owner]
    ADDR1 --> USER[User]
    USER --> OWN[Owner]
    OWN --> PROP_FLOW

    EXIST --> PROP_FLOW[Fluxo Propriedade]

    PROP_FLOW --> ADDR2[Endereço Imóvel]
    ADDR2 --> FOREIGN{Owner estrangeiro?}
    
    FOREIGN -->|Sim| INV2[2 Invoices<br/>Owner + Propriedade]
    FOREIGN -->|Não| INV1[1 Invoice]
    
    INV1 --> PROP[Property]
    INV2 --> PROP
    
    PROP --> CRED{Novo owner?}
    CRED -->|Sim| CS
    CRED -->|Não| FIM[Fim]
    CS --> FIM
```

### Tratamentos de Dados (onboarding_helpers)

| Função | Tratamento |
|----|----|
| `format_phone_number` | Adiciona `+`, remove caracteres especiais |
| `translate_marital_status_to_english` | PT→EN (Solteiro→Single) |
| `normalize_state` | Sigla→Nome (SC→Santa Catarina) |
| `normalize_commission_to_decimal` | %→decimal (20→0.20) |
| `get_partner_id_by_name` | Nome→ID (busca Partner) |
| `get_host_id_by_name` | Nome→ID (busca Host) |
| `calculate_plan_flags` | Calcula `has_insurance`, `has_bill_management` |

### Componentess criados

| Módulo | Localização | Descrição |
|----|----|----|
| **PropertyOnboardingRecord** | `property/models.py` | Model que registra execuções de onboarding (status, entidades criadas, erros) |
| **OnboardingAutomationService** | `property/services/onboarding_automation.py` | Orquestra criação de Owner e Property, reutilizando serializers existentes |
| **onboarding_helpers** | `property/services/onboarding_helpers.py` | Funções de normalização: telefone, estado civil, comissões, buscas por nome |
| **PipedriveDealOnboardingHandler** | `webhook/pipedrive_deal_onboarding_handler.py` | Handler que detecta trigger (stage + status won) e chama o service |
| **CredentialsService** | `account/services/credentials_service.py` | Gera senha temporária e envia email de credenciais ao owner |
| **Feature Flag (adição ff)** | `feature_flags/feature_flags.py` | `ENABLE_ONBOARDING_AUTOMATION` controla ativação via PostHog |


### Condição de Trigger

O onboarding é disparado quando:


1. **Stage** = "Contrato" (id do stage buscado dinamicamente por nome em `partner_pipedrive_stage`)
2. **Status** muda para `"won"`


---

### Mecanismos de Segurança

* Verifica `PropertyOnboardingRecord` antes de processar
* Rollback automático em caso de erro
* Desativação instantânea via PostHog
* Erros registrados em `HandoverValidationAudit`

## Tratamentos de dados pelo Front

Nessa seção estão detalhamentos sobre pré-tratamentos/processamentos de dados realizados pelo front-end, aos dados do pipedrive, antes de envio ao Back-end.

Para a construção do web-hook, pode ser importante tê-los em mente a fim de aplicá-los, também. Ou realizar validações adicionais sob os dados recebidos - em service layer.

### Cria endereço proprietário

**Rota utilizada em tela:** `/account/address/`

**Payload enviado:**

```json
{
    "street": "string (max 255, opcional)",
    "number": "string (max 255, opcional)",
    "complement": "string (max 255, opcional)",
    "neighborhood": "string (max 255, opcional)",
    "city": "string (max 255, opcional)",
    "state": "string (max 255, opcional)",
    "postal_code": "string (max 10, opcional)",
    "country": "string (max 70, opcional)",
}
```

**Tratamentos front-end:**

* O front-end realiza a normalização do campo `state` - `app/src/services/Address/states.ts`
* O front-end realiza a normalização do campo `country` - `app/src/services/Address/countries.ts`
* O front-end realiza a normalização dos campos `street` e `neighborhood` com `str.replace(/[,*\-().]/g, '')`

### Cria usuário do prop

**Rota utilizada em tela:** `/account/user`

**Payload enviado:**

```json
{
    "first_name": "string (max 255 chars, obrigatório)",
    "last_name": "string (max 255 chars, obrigatório)",
    "email": "email (único, case-insensitive, obrigatório)",
    "phone_number1": "string (max 255 chars, opcional)",
    "main_role": "string (max 50 chars, choices: Admin, Seazone, Attendant, Host, Owner, Partner, Guest, opcional)",
    "gender": "string (max 50 chars, choices: Female, Male, Not_informed, opcional)",
    "birth_date": "date (formato YYYY-MM-DD, opcional, idade entre 12-123 anos)",
    "is_individual": "boolean (opcional)",
    "cpf": "string (11 dígitos numéricos, opcional, validador CPF_validator)",
    "cnpj": "string (14 dígitos numéricos, opcional, validador CNPJ_validator)",
    "corporate_name": "string (max 100 chars, opcional)",
    "trading_name": "string (max 100 chars, opcional)",
    "is_staff": "boolean (opcional, default 'false')",
    "is_active": "boolean (opcional, default 'true')",
    "main_address": "integer (FK para Address, opcional)",
    "pipedrive_person_id": "string (único, opcional, default '')",
    "password": "string (obrigatório, validação Django password)",
    "password_confirmation": "string (obrigatório, deve coincidir com password)"
}
```

**Tratamentos front-end:**

* Front-end retira caracteres não numéricos de `cpf`, `cnpj`, `phone`
* Front-end adiciona `+` no começo de `phone` (caso já não possua)
* `main_role` sempre enviado como `'Owner'`
* `gender` sempre enviado como `'Not informed'`
* `is_staff` sempre enviado como `false`
* `is_active` sempre enviado como `true`
* `birth_date` tratado para sempre estar em formato `YYYY-MM-DD`
* `is_individual` verdadeiro se não houver cnpj (ignora campo homônimo do pipedrive)

### Cria Role de owner para prop

**Rota utilizada em tela:** `/account/owner/`

**Payload enviado:**

```json
{
    "user": "integer (obrigatório, FK para User)",
    "invoice_address": "integer (obrigatório, FK para Address)",
    "profession": "string (max 255 chars, opcional, validação: sem números)",
    "nationality": "string (max 255 chars, opcional)",
    "marital_status": "string (max 50 chars, opcional, choices: 'Single', 'Married', 'Divorced', 'Widowed', 'Civil Union')",
    "is_partner_indication": "boolean (opcional, default false)",
    "referrer_partner": "integer (opcional, nullable, FK para Partner)"
}
```

**Tratamentos front-end:**

* `profession` - aplicada `str.replace(/[,*\-().]/g, '');` - default: `'Não informado'`


* `nationality` - aplicada `str.replace(/[,*\-().]/g, '');` -  default: `'Não informado'`
* `marital_status` - aplicada normalização `translateMaritalStatus` - `/app/src/utils/Translator/index.ts`
* `referer_partner` - Front-end recebe só o nome do parceiro. Portanto faz busca em `/account/partner/` para obter match por nome - e assim conseguir o id informado em `referer_partner` (consultar `handleGetPartnerSelected` - `app/src/components/OnboardingPage/PageForms/Forms/index.tsx`)
* `is_partner_indication` - True se `referer_partner` existe

### Cria endereço propriedade

**Rota utilizada em tela:** `/account/address/`

**Payload:**

```json
{
    "street": "string (max 255, opcional)",
    "number": "string (max 255, opcional)",
    "complement": "string (max 255, opcional)",
    "neighborhood": "string (max 255, opcional)",
    "city": "string (max 255, opcional)",
    "state": "string (max 255, opcional)",
    "postal_code": "string (max 10, opcional)",
    "country": "string (max 70, opcional)",
    "condominium": "string (max 255, opcional)"
}
```

**Tratamentos front-end:**

* O front-end realiza a normalização do campo `state` - `app/src/services/Address/states.ts`
* `country` - Sempre enviado como `Brasil`  (==Talvez não seja o ideal==)


### Cria invoice_details

**Rota utilizada em tela:** `/financial/owner/invoice_details`

**Payload:**

```json
{
    "is_default": "boolean (default=False)",
    "invoice_entity_name": "string (max 255 chars, opcional)", //Nome completo do proprietário
    "cpf": "string (max 11 chars, opcional)", // CPF formatado (sem pontuação)
    "cnpj": "string (max 14 chars, opcional)", // CNPJ formatado (sem pontuação)
    "email": "string (email, max 254, opcional)",// Email do proprietário
    "phone_number": "string (max 32 chars, opcional)",// Telefone formatado com +
    "postal_code": "string (max 32 chars, opcional)",// CEP do endereço
    "address": "string (max 256 chars, opcional)",// Rua/Logradouro
    "address_number": "string (max 32 chars, opcional)",// Número do endereço
    "complement": "string (max 256 chars, opcional)",// Complemento
    "district": "string (max 64 chars, opcional)",// Bairro
    "city": "string (max 64 chars, opcional)",// Cidade
    "state": "string (max 32 chars, opcional)",// Estado (sigla normalizada)
    "user": "integer (FK para User - obrigatório)"// ID do usuário (user_id)
}
```

**Tratamentos front-end:**

* O front-end realiza a normalização do campo `state` - `app/src/services/Address/states.ts`
* O front-end realiza a normalização do campo `country` - `app/src/services/Address/countries.ts`
* Front-end retira caracteres não numéricos de `cpf`, `cnpj`, `phone`
* Front-end adiciona `+` no começo de `phone` (caso já não possua)


* !==IMPORTANTE==!: Caso o país `country` do endereço do proprietário não seja brasil, é realizada a criação de DOIS INVOICES. Um com o endereço do proprietário, outro com endereço da propriedade (mesmo payload mas substituindo `address`, `address_number` e `city` pelas informações da propriedade).

### Cria propriedade

**Rota utilizada em tela:** 

**Payload de campos fixos (sempre enviados assim pelo front-end):**

```json
// Rules - Sempre fixos
{
  allow_pet: false,
  check_in_time: "11:00",
  check_out_time: "15:00",
  events_permitted: false,
  smoking_permitted: false,
  suitable_for_babies: false,
  suitable_for_children: false
}

// Property
{
  status: "Onboarding",
  host_cleaning_comission_fee: 1, // ou 0 se Digital Management
  country: "Brasil" // Para endereço de propriedade
}

// Handover
{
  bed_linen_photo: null
}
```

**Tratamentos front-end:**

* `contract_start_date` - data atual (YYYY-MM-DD)
* `host_cleaning_comission_fee` - se `plan === 'Digital_Management'` = 0; senão 1
* `host_reservation_comission_fee` - se `plan === 'Digital_Management'` = 0; senão assume valor vindo do pipedrive
* `has_insurance` - True se plano (`plan`) for Safe ou Premium
* `has_bill_management` - True  se plano (`plan`) for Premium
* `invoice_details` - No caso de proprietário estrangeiro, lembrar que dois invoice_details devem ser criados (na etapa anterior). Nesse caso, o valor campo aqui é o do `invoice_details` da propriedade (endereço no Brasil).
* `plan` - Utiliza `normalizePlanValue` (`app/src/components/OnboardingPage/PageForms/Forms/utils.ts`) para normalizar string de plano
* `property_type` - Utiliza `translateTypeProperty` (`sapron-frontend/app/src/utils/Translator/index.ts`) para normalizar tipo, vindo do pipe
* `host` - Faz busca por nome; ou busca por Host de nome `A Definir`, passando seu id como payload padrão.

Verificar se `comission_fee`, `balance_discount_rate` e `host_reservation_comission_fee` estão vindo corretamente (são porcentagens - comparar valores do banco com valores vindos do pipedrive para decidir sobre possíveis tratamentos de valor. `balance_discount_rate` é tratado no fluxo de criação de handover_details, na rota atual. Pode-se consultar o serializer para comparar estratégias).