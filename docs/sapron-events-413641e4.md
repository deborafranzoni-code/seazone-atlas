<!-- title: Sapron Events | url: https://outline.seazone.com.br/doc/sapron-events-DNc3lpbAd7 | area: Tecnologia -->

# 🔊 Sapron Events

# TL;DR

Adicionar um **broker de eventos** na API do Sapron para externalizar **ações** realizadas em **recursos** da aplicação.

# Objetivo

Permitir a construção de componentes de software distribuídos, específicos e desacoplados que reagem aos eventos emitidos.

# Casos de Uso

## Migração de triggers do BD para event listeners

Pode-se criar eventos de atualização/criação/deleção para as tabelas, e rotinas que são iniciadas no disparo do evento.

**Exemplo**: feature de fechamento; cálculo de saldo é disparado após atualização de reserva.

## Migração da persistência das tabelas `*_audit` para event listeners

Pode-se criar eventos de atualização/criação/deleção para as tabelas, e migrar a lógica de inserção nas tabelas `*_audit` para uma rotina que é iniciada após disparo do evento.

**Bônus**: atualmente, isso é feita de forma síncrona pelo Django; com essa migração, será feita de forma assíncrona, diminuindo a latência.

# Arquitetura

## Broker de eventos

* [Amazon EventBridge](https://docs.aws.amazon.com/eventbridge/latest/userguide/eb-what-is.html)

Ao fim de uma requisição, o Sapron API dispara a emissão do evento para o Amazon Event Bridge:

 ![](/api/attachments.redirect?id=d761d642-373f-4f79-8e47-64b053ddc4b2 " =976x353")

### SNS vs EventBridge

* [ChatGPT Chart Comparison](https://chatgpt.com/share/6942f222-356c-8012-bf0a-e1b0849731f6)
* [Pricing](https://aws.amazon.com/eventbridge/pricing/)

| Dimension | Amazon SNS | Amazon EventBridge |
|----|----|----|
| **Primary Purpose** | Pub/Sub messaging & notifications | Event bus for event-driven architectures |
| **Event Model** | Message-based | Event-based (structured events) |
| **Payload Structure** | Free-form message (string or JSON) | Strongly structured JSON (source, detail-type, detail, etc.) |
| **Schema Enforcement** | ❌ None | ✅ Optional (Schema Registry) |
| **Routing Logic** | Topic → all subscribers | Rule-based filtering (content-based) |
| **Filtering** | Limited (message attributes only) | Advanced filtering on event fields |
| **Fan-out** | Native fan-out to multiple subscribers | Native fan-out via multiple rules |
| **Targets** | SQS, Lambda, HTTP/S, Email, SMS, Mobile push | Lambda, SQS, SNS, Step Functions, API Destinations, many AWS services |
| **Cross-Account Support** | Yes | Yes (first-class) |
| **Cross-Region Support** | Limited | Built-in via event buses |
| **Event Replay** | ❌ Not supported | ❌ (but archive + replay supported) |
| **Event Archiving** | ❌ No | ✅ Yes (with replay) |
| **Event Ordering** | Best-effort | Best-effort |
| **Throughput** | Very high | High (slightly lower than SNS) |
| **Latency** | Very low | Low |
| **Retry & DLQ** | Depends on subscriber (e.g., SQS/Lambda) | Built-in retries + DLQ per rule |
| **Integration with AWS Services** | Limited | Native integrations with 100+ AWS services |
| **Typical Payload Size** | Up to 256 KB | Up to 256 KB |
| **Pricing Model** | Per published message + deliveries | Per event ingested + rules |
| **Best Use Cases** | Notifications, fan-out messaging, simple async workflows | Domain events, integration events, decoupled microservices |

## Payload de eventos

Um evento é composto por três componentes: recurso, ação e payload. Portanto, devem se encaixar no seguinte padrão: "*A ação **<nome_da_ação>** aconteceu no recurso **<nome_do_recurso>**. Estas são as informações: **<dados_do_payload>***".

Exemplo: "*A ação **created** aconteceu no recurso **investment-indication**. Estas são as informações: **{ "id": 123, "emitted_by_user_id": 111, "status": "In Progress" }***"

Abaixo, transcrevendo no formato de payload utilizado pelo EventBridge:

```json
{
  "version": "0",
  "source": "seazone.investment-indication",
  "account": "123456789012",
  "id": "12345678-1234-1234-1234-111122223333",
  "region": "sa-east-1",
  "detail-type": "created",
  "time": "2025-12-15T17:00:00Z",
  "resources": [],
  "detail": {
    "id": 123,
    "emitted_by_user_id": 111,
    "status": "In Progress",
  }
}
```

Dessa forma, para cada recurso da aplicação, existe uma lista pré-definida de ações que poderão ser exercidas sobre o recurso. Além disso, para cada ação de um recurso, existe um payload com formato bem definido. Esse payload pode ser modificado conforme necessidade.

## Emissão de eventos

A emissão do evento só pode ser realizada quando a requisição é feita com sucesso, ou seja, a ação sobre o recurso é finalizada sem nenhum tipo de erro.

Dessa forma, é **imprescindível** que exista uma forma de verificar se ocorreu um erro durante a requisição; se ocorreu, nenhum evento deve ser emitido; caso contrário, todos os eventos da requisição devem ser emitidos.

### Handler agendador de eventos

Deve-se criar um método central responsável por "agendar" a emissão do evento. O objetivo é que todo fluxo que emita um evento utilize esse método.

O método deve ser tipado para permitir apenas a chamada de eventos mapeados, ou seja, **event_name** e **event_action** pré definidos. Da mesma forma, o payload informado no método deve ser o correspondente ao event_name e event_action em questão.

### Middleware disparador de eventos

Ao fim da requisição, o middleware deve recuperar todos os eventos agendados na requisição e dispará-los **somente se** nenhum erro ocorreu.

## Auditoria

Adicionalmente, podemos armazenar em nossa base os eventos emitidos para fins de auditoria:

 ![](/api/attachments.redirect?id=63349ac4-47a3-463f-a64e-3e8d619b3b17 " =887x511")

Dessa forma, toda vez que o Sapron API emite um evento para o EventBridge, devemos armazenar os dados do evento (event_name, event_action e payload). De forma arquitetural, o sistema pode ser visualizado da sequinte forma:

 ![](/api/attachments.redirect?id=895883c4-877a-4a3a-8a15-8228e66db625 " =1419x303")

* **event_logger**: função lambda responsável por registrar o evento recebido no BD