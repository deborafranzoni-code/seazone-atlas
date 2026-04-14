<!-- title: Investigação erros #backend-boyz | url: https://outline.seazone.com.br/doc/investigacao-erros-backend-boyz-ODy0bWKGvI | area: Tecnologia -->

# Investigação erros #backend-boyz

**Período investigado**:  01/01/25 - 26/03/25

## Celery

### Tipo: NoOriginalReservationFound

**Mensagem**: 

> extension=TZ190I

**Exemplo**: <https://seazone-fund.slack.com/archives/C029VMKJRT9/p1742976588507109>

**Frequência**: Diário+

**Gravidade**: Nenhuma, todas são importações falhas de reservas canceladas.

**Origem**: <https://github.com/seazone-tech/sapron-backend/blob/f9c99b0b3c413c7a1e550e4c27af11531833644c/src/channel_manager/action/stays/stays_extender.py#L82>

São reservas da Stays que são marcadas como extensões (acredito que indevidamente) e canceladas manualmente. O Log faz sentido por quê atualmente ela está marcada como extensão, mas não há nenhuma ligação com outras reservas (canceladas ou concluídas), então realmente não há reserva original para ser encontrada. Exemplos:

TZ190I - Cancelada e está como extensão na Stays, mas não possui nada que a referencie a outra reserva

TF495I - Idem

TV577I - Idem

**Proposta**: Se a intenção é espelhar o banco de dados da Stays, criar a reserva do mesmo jeito ao invés de retornar a exceção. Porém, acredito que esse erro esteja correto e seja um erro de processo externo ao Sapron.


---

### Tipo: NoOriginalReservationFound

**Mensagem**: 

`Original reservation does not match this extension TE112I`

**Exemplo**: <https://seazone-fund.slack.com/archives/C029VMKJRT9/p1742976588111509>

**Frequẽncia**: Diário+

**Gravidade**: Nenhuma, todas são importações falhas de reservas canceladas.

**Origem**:[https://github.com/seazone-tech/sapron-backend/blob/f9c99b0b3c413c7a1e550e4c27af11531833644c/src/channel_manager/action/stays/stays_extender.py#L](https://github.com/seazone-tech/sapron-backend/blob/f9c99b0b3c413c7a1e550e4c27af11531833644c/src/channel_manager/action/stays/stays_extender.py#L82)91

São reservas da Stays que, apesar de terem um link com uma reserva existente e concluída, tem discrepância nas datas de check-in ou check-out. Nos casos que encontrei, elas também foram todas canceladas (em alguns casos até refeitas), mas tentamos atualizar elas durante 30 dias e durante esses 30 dias se a data não for corrigida, o log vai surgir. Exemplos:

* TZ346I - ID Externo pra reserva errada (e por consequência pras datas erradas, extensão stays)
* TE112I - ID Externo não bate as datas (extensão stays pra reserva airbnb)
* TL237I - ID Externo não bate as datas (idem) 
* TS295I - ID Externo não bate as datas (idem)
* TV577I - sem ID Externo, cancelada
* SR43I - ID Externo não bate as datas (idem)

**Proposta**: Se a intenção é espelhar o banco de dados da Stays, criar a reserva do mesmo jeito e associar a reserva que está marcada como original, independente das datas não baterem. ao invés de retornar a exceção. Porém, acredito que esse erro esteja correto e seja um erro de processo externo ao Sapron.


---

### Tipo: AttributeError

**Mensagem**: 

> 'NoneType' object has no attribute 'listing_created'

**Exemplo**: <https://seazone-fund.slack.com/archives/C029VMKJRT9/p1742918963783379>

**Frequência**: Diário

**Gravidade**: Nenhuma, impede o envio de uma mensagem a um canal que não existe mais

**Origem**: <https://github.com/seazone-tech/sapron-backend/blob/8b3653f372115ccb4a9ce970116d8dff5dece3b1/src/channel_manager/tasks_stays.py#L264>

Ocorre por erro de lógica interna. Acredito que mais investigação sobre seja irrelevante, por quê a verificação tenta enviar mensagem pra um canal inexistente.

**Proposta**: Deletar o trecho de código que tenta enviar a mensagem.


---

### Tipo: ConnectionError

**Mensagem**: 

> ('Connection aborted.', ConnectionResetError(104, 'Connection reset by peer'))

**Exemplo**: <https://seazone-fund.slack.com/archives/C029VMKJRT9/p1742903103814369>

**Frequência**: Esporádico

**Gravidade**:

**Origem**:


---

### Tipo: HTTPError 504

**Mensagem**: 

> 504 Server Error: Gateway Time-out for url:

**Exemplo**: <https://seazone-fund.slack.com/archives/C029VMKJRT9/p1742686589125599>

**Frequência**: Esporádico 

**Gravidade**:

**Origem**:


---

### Tipo: Exception

**Mensagem**: 

> Error posting message: The request to the Slack API failed. (url: <https://slack.com/api/chat.postMessage>)\nThe server responded with: {'ok': False, 'error': 'ratelimited'}

**Exemplo**: <https://seazone-fund.slack.com/archives/C029VMKJRT9/p1741017070558329>

**Frequência**: Esporádico

**Gravidade**: Baixa

**Origem**: Por enviarmos muitas mensagens em horários de atualização de reservas e em algumas ocasiões enviamos mais do que a API do Slack permite. O único risco presente é perdermos alguma mensagem de erro que seja realmente importante e não se repita, mas é comum que erros problemáticos gerem muitos logs.

**Proposta**: Diminuir os outros erros que enviam mensagens demais e continuar monitorando. Se voltar a acontecer, investigar novamente para propôr outras soluções.


---

## Django

### Tipo: MemoryError

**Mensagem**: (vazio)

**Exemplo**: <https://seazone-fund.slack.com/archives/C029VMKJRT9/p1738330517750369>

**Frequência**: Único

**Gravidade**:

**Origem**:


---

### Tipo: HTTPError 404

**Mensagem**: Exception Type: HTTPError

> Exception Message: 404 Client Error: Not Found for url: [WEBHOOK_REDACTED]

**Exemplo**: https://seazone-fund.slack.com/archives/C029VMKJRT9/p1742945794276589

**Frequência**: Quinzenal

**Gravidade**:

**Origem**: