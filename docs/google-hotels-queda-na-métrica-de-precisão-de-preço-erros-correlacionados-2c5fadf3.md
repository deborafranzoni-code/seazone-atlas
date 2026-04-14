<!-- title: Google Hotels: Queda na métrica de precisão de preço + Erros correlacionados | url: https://outline.seazone.com.br/doc/google-hotels-queda-na-metrica-de-precisao-de-preco-erros-correlacionados-NOmCGCF0tX | area: Tecnologia -->

# Google Hotels: Queda na métrica de precisão de preço + Erros correlacionados

## Erros Infra

### \[INF1\] Identificado erros relacionados à conexão de rede do worker

* Falhas de conexão ao enviar requests ao Google Hotels: 

  ```python
  {"timestamp": "2025-07-24 13:05:44,046", "level": "INFO", "message": "Task google_hotels.push_rate_amount[3043c8fd-e17d-4551-bdab-42957801768e] retry: Retry in 0s: 
  PushRequestError(ConnectionError(MaxRetryError(\"HTTPSConnectionPool(host='www.google.com', port=443): Max retries exceeded with url: /travel/hotels/uploads/ota/hotel_rate_amount_notif 
  (Caused by NewConnectionError('<urllib3.connection.HTTPSConnection object at 0x7f1a05f4abc0>: 
  Failed to establish a new connection: [Errno 101] ENETUNREACH'))\")))", "service": null, "extra_info": {"data": {"id": "3043c8fd-e17d-4551-bdab-42957801768e", "name": "google_hotels.push_rate_amount", "exc": "Retry in 0s:
  ```

  ```python
  PushRequestError(ConnectionError(MaxRetryError(\"HTTPSConnectionPool(host='www.google.com', port=443): Max retries exceeded with url: /travel/hotels/uploads/ota/hotel_rate_amount_notif (Caused by NewConnectionError('<urllib3.connection.HTTPSConnection object at 0x7f1a05f4abc0>: Failed to establish a new connection: [Errno 101] ENETUNREACH'))\")))"}}, "method_name": "info", "file_name": "trace.py", "logger_name": "celery.app.trace", "span_id": 14027172881267721474, "trace_id": 71174927083014517074844354137859127181, "celery_task_id": "3043c8fd-e17d-4551-bdab-42957801768e"}
  ```

  \
* Falhas de conexão do worker com serviços internos: OpenSearch e Elasticache
  * Erro de conexão com OpenSearch:

    ```python
    raise LifetimeTimeout(timeout=duration, errors=errors)\ndns.resolver.LifetimeTimeout: The resolution lifetime expired after 5.468 seconds: Server Do53:10.0.0.10@53 answered The DNS operation timed out.
    ```

    ```python
    raise EAI_EAGAIN_ERROR
    ```

    ```python
    raise NewConnectionError(\nurllib3.exceptions.NewConnectionError: <urllib3.connection.HTTPSConnection object at 0x7fdc5c029c30>: Failed to establish a new connection: [Errno -3] Lookup timed out
    ```

    ```python
    "span_id": 9708081235699352817, "trace_id": 158286871217977693410812968403593092720, "celery_task_id": "7c82b52e-5fef-4f50-b403-3b35e76cbf09"
    ```

    \
  * Erro de conexão com Elasticache:

    ```python
    raise LifetimeTimeout(timeout=duration, errors=errors)\ndns.resolver.LifetimeTimeout: The resolution lifetime expired after 5.103 seconds: Server Do53:10.0.0.10@53 answered The DNS operation timed out.
    ```

    ```python
    raise EAI_EAGAIN_ERROR\n  File \"/usr/local/lib/python3.10/site-packages/eventlet/support/greendns.py
    ```

    ```python
    ConnectionError(self._error_message(e))\nredis.exceptions.ConnectionError: Error -3 connecting to master.service-reservas-cache.bbuttp.usw2.cache.amazonaws.com:6379. Lookup timed out. "celery_task_id": "aafacf36-c368-4736-ad33-0c0fc2d10ea3"
    ```

    Olhando o uso de recursos da AWS, parece que o Elasticache está com certa frequencia atingindo 100% de uso de memória do BD![](/api/attachments.redirect?id=28516d9d-75a4-4446-a8ee-457f5d1e5999)


### **\[INF2\] Identificado queda do worker por falta de memória (erro 137)**

```python
2025-07-24 09:09:15.878 ERROR: Command failed with exit code 137
```

Isso ocorreu na mesma hora em que a geração do XML de Propriedades do Google ia ser executado. Isso fez com que o XML não fosse gerado no dia de hoje (24/07)

*==TODO: Verificar uso de recursos, e verificar se estamos chegando próximo ao limits. Caso sim, devemos aumentar ou pensar separar o worker em mais workers.==*


### \[INF3\] Erro ao carregar credenciais

```python
2025-07-24 15:50:58.256	time="2025-07-24T18:50:58Z" level=error msg="Error Getting Parameters from SSM: operation error SSM: GetParametersByPath, failed to sign request: failed to retrieve credentials: failed to refresh cached credentials, failed to retrieve credentials, operation error STS: AssumeRoleWithWebIdentity, https response error StatusCode: 400, RequestID: b668e52a-7e9d-41a8-b139-260395f485a7, ExpiredTokenException: Token expired: current date/time 1753382758 must be before the expiration date/time 1753089571"
2025-07-24 15:50:58.256	ERROR: operation error SSM: GetParametersByPath, failed to sign request: failed to retrieve credentials: failed to refresh cached credentials, failed to retrieve credentials, operation error STS: AssumeRoleWithWebIdentity, https response error StatusCode: 400, RequestID: b668e52a-7e9d-41a8-b139-260395f485a7, ExpiredTokenException: Token expired: current date/time 1753382758 must be before the expiration date/time 1753089571
2025-07-24 15:50:45.950	ERROR: Command failed with exit code 137
```


## Erros Aplicação

### \[WOK1\] Identificado falhas de validação de XML do Google

* Erro de validação do XML (XML Inválido)

  *Há outros erros de validação ocorrendo além deste abaixo, em outras mensagens ARI.*

  ```python
  {"timestamp": "2025-07-24 13:05:49,717", "level": "ERROR", 
  "message": "ARI Availability Message: Error validating XML against XSD: unknown type '{http://www.opentravel.org/OTA/2003/05}AdvancedBookingWindowValue':\n\nSchema component:\n\n  <xs:union xmlns:xs=\"http://www.w3.org/2001/XMLSchema\" memberTypes=\"AdvancedBookingWindowValue Duration\" />\n\nPath: /xs:schema/xs:simpleType[5]/xs:union\n\nSchema URL: https://www.gstatic.com/ads-travel/hotels/api/ota_hotel_avail_notif_rq.xsd\n", "file_name": "availability.py", "logger_name": "worker", "span_id": 7604991386193624638, "trace_id": 71174927083014517074844354137859127181, "celery_task_id": "e01d146a-39ba-402b-b571-d262cde4068b"}
  ```

  \
* Erro ao incluir schema ao validar XML

  ```python
  {"timestamp": "2025-07-24 12:03:04,057", "level": "WARNING", "message": "/code/reservations_api/util.py:109: XMLSchemaIncludeWarning: Include schema failed: <urlopen error [Errno 101] ENETUNREACH>.\n  xsd_doc = xmlschema.XMLSchema(xsd)\n", "service": null, "extra_info": {}, "method_name": "_showwarnmsg", "file_name": "warnings.py", "logger_name": "py.warnings", "span_id": 12651922122718261582, "trace_id": 158286871217977693410812968403593092720, "celery_task_id": "c133470b-1fc1-402e-b9c7-8f03840418e5"}
  ```

   


### \[WOK2\] Divergência de preço da Busca e Imóvel

Imóvel provavelmente não havia sido sincronizado corretamente, talvez, pelas instabilidades vistas anteriormente no worker *(é uma hipótese, não encontrei provas ainda)*.

**Solução:** Ao executar um sync para esse imóvel, foi resolvido o problema.


### \[GOH1\] Identificado divergência de preços Busca/Stays X Google Hotels

Imóvel EDN1001 período 29/09 a 08/10. Divergência de preço de R$64 ![](/api/attachments.redirect?id=df7b08a8-8051-4850-9c4b-530dcc4fc2ba)


Ao conferir os preços no **OpenSearch/Stay**s, foi visto que as tarefas **a partir do dia 03/10 estão com valores diferentes**. 

Pelo cálculo realizado, a diferença de valores se dá justamente por causa dessa diferença no valor das tarifas/diárias. Onde no Google Hotels, a implementação que fizemos não está preparada para o modelo LOS (Length of Stay), que calcula um preço baseada no tempo de estadia.\n ![https://ssl.stays.com.br/i/apartment/VO17I/sellprice/timeline?from=2025-09-22&to=2025-10-08&type\[\]=reserved&type\[\]=booked&type\[\]=contract&type\[\]=blocked&type\[\]=maintenance](/api/attachments.redirect?id=8daf48fc-2e63-4d82-8ced-e4d4f7c95fd8)


Como vemos abaixo, No Hotel Center cada dia tem apenas **um preço por data**, e esse está sendo o preço considerado no Google (que é referente a tarifa mínima da stays/opensearch). \nO preço vai ser diferente apenas se o imóvel tiver taxa de hóspede extra (diária variável com base na qtd de hóspede).

A **implementação atual** **utiliza o preço baseado em data**. \nPara conseguirmos fornecer um preço baseado na estadia, vamos precisar mudar a forma como geramos o XML e implementar os [Preços com base no LOS](https://developers.google.com/hotels/hotel-prices/xml-reference/ari-rate?hl=pt-br#los-based_pricing). ![https://hotelcenter.google.com/prices/availability?hotelId=4678&a=134972474&startDate=2025-09-29&endDate=2025-10-08](/api/attachments.redirect?id=cc4dfa5d-6519-448d-a7d5-7c4b2fb1c573)


*Aqui vemos que o preço é UM só, só se diferencia com base no número de hóspedes. Essa é uma implementação que utilizada o Preço por Data, diferente do Preço com base na LOS*

 ![XML Rate Amount: Trecho do XML enviado ao Google para informar o preço de cada dia para um determinado imóvel](/api/attachments.redirect?id=a510364a-fc28-4262-a3e5-7f992c6932be)


#### Ação a ser tomada:

Após consultar o time de RM, nos foi informado que há uma desconto para todos os imóveis, para reservas com periodo de >=7 noites e para reservas com período >=28 noites conforme é exibido na imagem anterior da Stays.

Portanto, tendo em vista que o time de RM está usando essa estratégia de precificação baseada em LOS, precisaremos também migrar nossa implementação do Google Hotéis para ser baseado em LOS.


\
### \[GOH2\] Experimento do PIX afetando precisão

O Google está entendendo que o desconto por pagar via PIX é o valor total final, e está acusando isso como divergência de preço.

Para evitar isso, precisamos mover a exibição do desconto PIX apenas na segunda tela, onde mostra os métodos de pagamento.

**Exemplo do erro:** <https://hotelcenter.google.com/prices/accuracy?hotelId=239&flo=MTM0OTcyNDc0OjE3NTM3MDI5OTQzMjMwMDI6MTUzMDQ0MTE0NTQxNzkwNTQxMzE>

 ![](/api/attachments.redirect?id=179c7fe6-73c7-4bf2-83ab-47e41f70b637 "left-50 =380x200") ![](/api/attachments.redirect?id=5e9648e0-9be3-41d8-8200-bdfab5c3d693 "left-50 =380x202")


\

\

\
### \[GOH3\] Exibição de preço zerado no checkout 

O Google Hotéis encontrou um problema onde na página do checkout foi exibido o preço zerado para o imóvel que estava disponível.

Pelo fato do preço estar zerado, o Google acusou como erro do Tipo "Quarto indisponível".

Precisamos entender o que causou esse preço zerado e evitar que isso aconteça. Ao testar no dia de hoje, não consegui resolver o problema, mas precisamos levantar hipóteses do que pode ter sido e implementar medidas para evitar esse problema.

**Exemplo do erro**:\n[https://hotelcenter.google.com/prices/accuracy?hotelId=3583&flo=MTM0OTcyNDc0OjE3NTM2MjQ3MzEyNjYwMDI6NTUxNzYzNzYwMjEyMDQ4OTY1Mg](https://hotelcenter.google.com/prices/accuracy?hotelId=3583&flo=MTM0OTcyNDc0OjE3NTM2MjQ3MzEyNjYwMDI6NTUxNzYzNzYwMjEyMDQ4OTY1Mg "https://hotelcenter.google.com/prices/accuracy?hotelId=3583&flo=MTM0OTcyNDc0OjE3NTM2MjQ3MzEyNjYwMDI6NTUxNzYzNzYwMjEyMDQ4OTY1Mg")

 ![](/api/attachments.redirect?id=ba419c86-b66c-486c-9b9a-312fc589dbe0)


## Sugestões Melhoria/Correção

### \[INF1\] e \[INF2\]: Reduzir frequência de execução da Task do Google:

Executar somente quando recebermos webhook da Stays indicando atualização de preço/disponibilidade/reserva.\n**Objetivo:** Reduzir a carga do worker já que a cada 30min estamos sincronizando todos os imóveis da base.


### \[INF1\] Melhoria no DNS

Precisamos garantir um **DNS mais estável** para que não haja falha de comunicação entre os serviços internos e externos.


### \[WOK1\] Salvar XML para Debug

* Sugestão de Começar salvar no S3 os XMLs que falham para facilitar o Debug.
* Sugestão de remover a validação de XML. A lib utilizada não é tão estável, mesmo durante a época da implementação houve dificuldade em fazê-la funcionar quando haavia um schema que importava outro. E isso tem causado alguns erros na validação.\nPodemos delegar a responsabilidade de validar o XML para o Google, e remover essa etapa do nosso lado. Eles também validam o Schema e retornam erro caso esteja no formato errado.


### \[GOH1\] Sugestão de correção

Dado o problema encontrado, podemos optar por:


1. Solicitar ao time de RM que volte a utilizar uma só tarifa, ou, mesmo preço para todas tarifas; 

   OU
2. Implementar a integração com o Google utilizando os Preços com base na LOS (preço baseado no tempo da estadia) \n**📄** [Doc: Configurar taxas com base na LOS](https://developers.google.com/hotels/hotel-prices/xml-reference/ari-rate?hl=pt-br#los-based_pricing)


###