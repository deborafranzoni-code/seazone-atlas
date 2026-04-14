<!-- title: Sprint 1 | url: https://outline.seazone.com.br/doc/sprint-1-5okhE22KaF | area: Tecnologia -->

# Sprint 1

## 1. Objetivo da Sprint

Esta sprint teve como objetivo implementar o fluxo inicial de processamento de mensagens da **SIA**, utilizando **n8n** como orquestrador.

O fluxo é responsável por:

* Receber mensagens externas via **Webhook**
* Normalizar e validar os dados recebidos
* Identificar o usuário remetente
* Interpretar o conteúdo da mensagem
* Estruturar o payload interno
* Encaminhar a mensagem para processamento de **IA**
* Retornar uma resposta ao canal de origem

## 2. Arquitetura do Fluxo

O processamento da mensagem segue a seguinte sequência de execução:

Webhook → Treat Incoming → continue? → UserInfo → HiL (desativado) → ParseMessage → mensagem válida? → Payload → MessageQueue → IA → Response

Fluxos alternativos:

continue? → false → Set erro\nmensagem válida? → false → erro_msg_vazia

 ![](/api/attachments.redirect?id=9f2948d5-f7d4-40cc-a982-085900d5aee8 " =1535x298")

## 3. Fluxo Geral de Processamento


 1. Um evento externo envia uma mensagem para o **Webhook**.
 2. O payload recebido é normalizado pelo **Treat Incoming**.
 3. O sistema verifica se a mensagem deve continuar no fluxo.
 4. O usuário remetente é identificado no **UserInfo**.
 5. A mensagem é analisada no **ParseMessage**.
 6. O sistema valida se o conteúdo da mensagem é válido.
 7. Um payload interno padronizado é criado.
 8. A mensagem é enviada para a **fila de processamento**.
 9. A **IA processa o conteúdo** da mensagem.
10. A resposta final é estruturada e enviada de volta ao canal.

## 4. Documentação dos Nodes

### 4.1 Webhook

**Função**

Receber mensagens externas que iniciam o workflow.


---

**Configuração**

* HTTP Method: POST
* Path: sia
* URL de teste: `https://automation.seazone.com.br/webhook-test/sia`
* Autenticação: None
* Modo de resposta: Respond Immediately


---

**Estrutura esperada da mensagem**

Exemplo de payload recebido:

`{`\n`  "type": "text/plain",`\n`  "content": "opa",`\n`  "id": "fe5c4b92-0f9e-411a-bda7-79fdf7499950",`\n`  "metadata": {`\n`    "date_processed": "timestamp"`\n`  }`\n`}`


### 4.2 Treat Incoming

**Função**

Executar um sub-workflow responsável por **normalizar o payload recebido**.


---

**Configuração**

Source\nDatabase

Workflow\n\[SUB\] Treat Incoming

Input enviado para o subworkflow

`payload: {{ $('Webhook').item.json }}`


---

**Modo de execução**

Run once with all items

**Opção habilitada**

Wait for Sub Workflow Completion = true


---

**Resultado esperado**

`{`\n`  payload: {`\n`    from,`\n`    fromMe,`\n`    continue`\n`  }`\n`}`

### 4.3 continue?

**Função**

Determinar se a mensagem deve continuar no fluxo.


---

**Condição**

`{{ $json.continue }} is true`


---

**Caminhos possíveis**

Se **true**

→ fluxo continua normalmente

Se **false**

→ fluxo direcionado para tratamento de erro

`No Operation`\n`↓`\n`Set erro`

### 4.4 Set erro

**Função**

Definir uma resposta padrão para requisições inválidas.


---

**Campo configurado**

responseText


---

**Valor retornado**

`Requisição inválida`

### 4.5 UserInfo

**Função**

Consultar ou construir informações do usuário remetente.


---

**Workflow chamado**

\[Sub\] UserInfo


---

**Input enviado**

`payload: {{ $('Webhook').item.json.body }}`


---

**Dados utilizados**

type\ncontent\nid


---

**Saída**

Objeto contendo informações do usuário.

### 4.6 HiL (Human in the Loop)

**Status**

Node atualmente **desativado**.


---

**Objetivo futuro**

Permitir intervenção humana antes da resposta da IA.

Possíveis aplicações:

* revisão de respostas
* moderação de conteúdo
* fallback manual

### 4.7 ParseMessage

**Função**

Extrair os dados relevantes da mensagem recebida.


---

**Workflow executado**

\[Sub\] ParseMessage


---

**Input enviado**

`{`\n`  messageType: $('Webhook').first().json.body.type,`\n`  content: $('Webhook').first().json.body.content`\n`}`

**Exemplo de saída**

`{`\n`  "messageType": "text/plain",`\n`  "content": "opa"`\n`}`

### 4.8 mensagem válida?

**Função**

Verificar se a mensagem possui conteúdo válido.


---

**Condição aplicada**

`{{ $json.content }} is not empty`


---

**Caminhos possíveis**

Se **true**

→ Payload

Se **false**

→ erro_msg_vazia

### 4.9 erro_msg_vazia

**Função**

Retornar mensagem de erro quando o conteúdo não puder ser identificado.


---

**Campo configurado**

responseText


---

**Mensagem retornada**

`Não consegui identificar sua mensagem. Tente novamente.`


---

### 4.10 Payload

**Função**

Construir o **payload interno padrão da SIA** para processamento da mensagem.


---

**Campos definidos**

payload.fromMe

`{{ $('Treat Incoming').first().json.fromMe }}`

payload.from

`{{ $('Webhook').first().json.body.from }}`

payload.msg.id

`{{ $('Webhook').first().json.body.id }}`

payload.msg.date

Conversão do timestamp recebido:

`DateTime.fromMillis(`\n`parseInt($node["Webhook"].json["body"]["metadata"]["date_processed"])`\n`).toFormat("yyyy-MM-dd HH:mm:ss")`

payload.msg.content

`{{ $json.content }}`

payload.userInfo

`{{ $('UserInfo').first().json }}`

### 4.11 MessageQueue

**Função**

Encaminhar a mensagem para o sistema de **fila de processamento**.


---

**Workflow chamado**

\[Sub\] MessageQueue


---

**Input enviado**

`payload: {{ $json.payload }}`


---

**Objetivo**

* desacoplar processamento
* evitar gargalos
* permitir escalabilidade
* suportar múltiplos workers


### 4.12 IA

**Função**

Processar a mensagem utilizando o módulo de **inteligência artificial**.


---

**Workflow chamado**

\[Sub\] IA


---

**Input enviado**

`{`\n` ...$node['Payload'].json.payload,`\n` msg: {`\n`   ...$node['Payload'].json.payload.msg,`\n`   content: $json.message`\n` }`\n`}`


---

**Resultado esperado**

`{`\n`  output: "resposta gerada pela IA"`\n`}`

### 4.13 Response

**Função**

Construir a resposta final que será enviada ao canal de origem.


---

**Payload enviado**

`{`\n` payload: $node['Payload'].json.payload,`\n` ai: $node['IA'].json.output,`\n` message_id: $('Webhook').first().json.body.id1w wyhugtwr`\n`}`

## 5. Tratamento de Erros

### Requisição inválida

Ocorre quando:

`continue = false`

Resposta retornada

`Requisição inválida`


---

### Mensagem vazia ou inválida

Ocorre quando:

`content = empty`

Resposta retornada

`Não consegui identificar sua mensagem. Tente novamente.`

## 6. Estrutura Final do Payload Interno

Payload utilizado internamente pela SIA:

`{`\n`  payload: {`\n`    fromMe: boolean,`\n`    from: string,`\n`    msg: {`\n`       id: string,`\n`       date: datetime,`\n`       content: string`\n`    },`\n`    userInfo: object`\n`  }`\n`}`