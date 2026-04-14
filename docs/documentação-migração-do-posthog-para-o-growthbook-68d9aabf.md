<!-- title: Documentação: Migração do Posthog para o Growthbook | url: https://outline.seazone.com.br/doc/documentacao-migracao-do-posthog-para-o-growthbook-RbjBu36kvm | area: Tecnologia -->

# Documentação: Migração do Posthog para o Growthbook

# Motivação

Devido à necessidade de migrar do PostHog para o Growthbook (e manter a possibilidade de alternar entre eles sem reescrever o código de negócio), foi criada uma camada de **abstração** de feature flags baseada em contratos, adapters e factory.

# **O que foi feito (e por quê)**

## Interfaces

Definimos um contrato único de uso no sistema, com duas variações: uma interface async (para chamadas em contextos assíncronos, como API) e uma interface sync (para contextos bloqueantes, como Worker/Celery).

Essa divisão async/sync foi necessária porque observamos que ao tentar usar a abordagem async no worker, percebemos que os valores das flags não atualizavam corretamente, ou seja, ao desligar/ligar uma flag, o worker ainda enxergava somente o estado antigo.

Sobre as interfaces, essa foi a abordagem escolhida para evitar que o restante do código precisasse conhecer detalhes do provider, e também possibilitar uma migração gradual.

## Adapters

Implementamos adapters por provider, traduzindo as operações do provider para o contrato comum (ex: is_enabled e get_payload).

Na prática, isso significa ter adapters para o Posthog e para o GrowthBook. A ideia é que eles expõem a mesma "cara" para o domínio, mesmo que a API/Integração de cada provider seja diferente.

## Factories

Criamos duas factories (uma async e uma sync) para escolher o provider, isso é feito lendo `FEATURE_FLAG_PROVIDER` e instanciando o adapter correto. Com isso, a troca de provider se tornou mudança de configuração (deploy/env) em vez de alteração espalhada em várias partes do código.

# **Como o código ficou organizado**

* `reservations_api/feature_flags/feature_flag_port.py`: define as classes abstratas (`FeatureFlagAsyncPort` e `FeatureFlagSyncPort`) e concentra comportamento comum. Acesse [aqui](https://github.com/seazone-tech/reservas-api/blob/develop/reservations_api/feature_flags/feature_flag_port.py).
* `reservations_api/feature_flags/posthog_adapter.py` e `reservations_api/feature_flags/growthbook_adapter.py`: implementa os adapters concretos de cada provider para os dois contextos (async e sync). Acesse [aqui](https://github.com/seazone-tech/reservas-api/blob/develop/reservations_api/feature_flags/posthog_adapter.py) e [aqui](https://github.com/seazone-tech/reservas-api/blob/develop/reservations_api/feature_flags/growthbook_adapter.py).
* `reservations_api/feature_flags/factory.py`: expõe a função `get_feature_flag_port()`, responsável por devolver o provider a partir da variável `FEATURE_FLAG_PROVIDER`. O controle de sync e async é feito através do parâmetro `use_async_client`. Acesse [aqui](https://github.com/seazone-tech/reservas-api/blob/develop/reservations_api/feature_flags/factory.py).

# Uso da abstração "na prática"

Como mencionado anteriormente, a abstração de feature flags foi projetada para que tanto a API quanto os workers tenham as mesmas capacidades (avaliar flags e obter payloads) sem conhecer os detalhes do provider (Posthog ou Growthbook).

O "cliente" do sistema interage apenas com as interfaces (`FeatureFlagAsyncPort` ou `FeatureFlagSyncPort`), enquanto a implementação concreta permanece encapsulada em adapters, selecionados pela factory com base na variável de ambiente `FEATURE_FLAG_PROVIDER`.

## Uso na API

Na API, a "classe de caso de uso" recebe o `FeatureFlagAsyncPort` por injeção de dependência no construtor (por exemplo: `AsyncReservationCreate(..., feature_flag_port: FeatureFlagAsyncPort)`).

Isso garante que o caso de uso dependa apenas do contrato, e não diretamente de Posthog ou Growthbook, tornando a migração transparente para a camada de domínio.

Quando precisa tomar uma decisão, o fluxo fica assim:

* O código chama da seguinte forma:

  ```python
  payload = await self._feature_flag_port.get_payload("ff_use_async_user_creation_auth0", user_identifier="seazone_backend")
  ```

  Nesse caso de flags controladas por payload, é mantida a lógica já existente, na qual o payload é interpretado (por exemplo, `payload.get("production")` e `payload.get("dev_staging")`) para decidir se a criação do usuário deve ocorrer via task assíncrona (`create_auth0_user.apply_async(...)`) ou por meio de uma chamada síncrona ao Auth0. Explore [aqui](https://github.com/seazone-tech/reservas-api/blob/develop/reservations_api/reservations/create.py#L75).

## **Uso no Worker/Celery (contexto síncrono)**

Nos workers, as tasks e utilitários são síncronos, portanto, o uso correto é por meio do `FeatureFlagSyncPort`, obtido via factory (por exemplo: `feature_flag_port = get_feature_flag_port(use_async_client=True)`).

O exemplo `_is_whatsapp_disabled_in_dev()` ilustra bem a intenção da abstração.

A regra de negócio, "em DEV não enviar WhatsApp, a menos que a flag force o envio", permanece local, explícita e fácil de entender. Já a consulta ao provider fica totalmente encapsulada na chamada:

```python
force_send = feature_flag_port.is_enabled_sync("ff_dev_force_send_whatsapp_message", "seazone_backend")
```

Caso o provider mude de Posthog para Growthbook no futuro, esse código permanece inalterado. Para mais detalhes desse código, comece explorando por [aqui](https://github.com/seazone-tech/reservas-api/blob/develop/reservations_api/worker/messaging/tasks.py#L145).

Ainda no worker, temos a obtenção síncrona do payload na task `check_reservation_expiration`. A task obtém a abstração síncrona via factory `feature_flag_port = get_feature_flag_port(use_async_client=False)` e, a partir daí, a task não precisa saber se o provider real é Posthog ou Growthbook, porque o adapter traduz para a mesma interface.

Então, o payload é buscado de forma síncrona:

```python
notify_abandoned_cart = feature_flag_port.get_payload_sync("ff_abandoned_cart_notification", "seazone_backend")
```

E a partir dai o payload é interpretado conforme mencionado antes, porque é uma regra padrão do website. Acesse o código [aqui](https://github.com/seazone-tech/reservas-api/blob/develop/reservations_api/worker/reservations/tasks.py#L200).

# Sobre o Growthbook

Estamos usando a versão selfhosted do Growthbook. Ele pode ser acessado através desse [link](https://ff.seazone.com.br/features).

## Instalação

O Growthbook disponibiliza um SDK que pode ser instalado no projeto. Além disso, na documentação há exemplos de como usar em [FastAPI](https://docs.growthbook.io/lib/python#async-web-framework-integration-fastapi) e [Django](https://docs.growthbook.io/lib/python#traditional-web-frameworks-django-flask-etc).

## Async Client e Legacy Client

O SDK Python do Growthbook disponibiliza duas formas principais de uso: o Legacy Client (síncrono) e o Async Client (assíncrono). No caso do website, utilizamos as duas formas em contextos diferentes, acesse o código da integração [aqui](https://github.com/seazone-tech/reservas-api/blob/develop/reservations_api/integration/growthbook/client.py).

### Legacy Client (síncrono)

O Legacy Client segue o modelo tradicional síncrono. As chamadas para carregar ou atualizar as features são bloqueantes, o que significa que, ao buscar as definições de flags no servidor do Growthbook, a thread atual fica aguardando a resposta.

Esse modelo é adequado para fluxos síncronos, como workers ou aplicações baseadas em frameworks tradicionais (ex: Django). No caso do website de reservas, ele é o mais apropriado para o contexto do Celery/Worker, onde o fluxo já é síncrono por natureza.

Para possibilitar o uso no worker, foi necessário inicializar [dessa forma](https://github.com/seazone-tech/reservas-api/blob/develop/reservations_api/worker/__init__.py#L344).

### Async Client (assíncrono)

O Async Client foi projetado para integração com aplicações baseadas em ASGI, como FastAPI. Ele permite utilizar `async/await` e evita bloqueios na event loop durante operações de rede.

No nosso caso, o Async Client é utilizado na API, onde os casos de uso já são assíncronos e dependem de `await`. Isso garante que a avaliação de feature flags não bloqueie o processamento de requisições.

Para possibilitar o uso na api, foi necessário inicializar no [main.py](https://github.com/seazone-tech/reservas-api/blob/develop/reservations_api/main.py#L128).

## Detalhe importante

Como a API do PostHog é síncrona, no adapter assíncrono foi utilizado o `anyio.to_thread.run_sync` para executar a chamada bloqueante em uma thread separada e retornar o resultado via `await`.

Inicialmente, a ideia era adotar apenas a abordagem assíncrona, mas posteriormente foi identificado que, no contexto do worker, isso não seria possível. Nesse momento, o uso do `anyio.to_thread.run_sync` já havia sido validado com sucesso no cenário em que as feature flags eram chamadas a partir da API (endpoints).

Além disso, essa implementação facilita a separação de responsabilidades entre a API (assíncrona) e o worker (síncrono). Caso essa abordagem não fosse utilizada, seria necessário introduzir uma lógica adicional para decidir dinamicamente quando usar chamadas síncronas ou assíncronas na API, aumentando a complexidade da solução.

## Funcionamento do Cache

O Growthbook implementa dois caches: (1) um cache em memória do nosso lado (no código do SDK), que a gente consegue ajustar o TTL; e (2) um cache de requisição. Quando o cache em memória expira, o SDK do GB faz uma requisição para o servidor solicitando as FFs. O servidor do GB retorna as FFs e a requisição retorna 200. Em seguida, ele pega o valor do header ETag e faz um cache dele (tag xxx -> response.body). Depois disso, ele salva o valor da FF no cache em memória. Nas próximas requisições, enquanto o cache não expirar, ele vai retornar a FF do cache. Porém, quando o cache expirar, na próxima requisição ele passa o ETag. Se o servidor do GrowthBook estiver com o ETag igual, significa que nenhuma mudança ocorreu nas FFs, e ele retorna um status 304. Ao receber esse status, o SDK pega do cache  de requisição o retorno relacionado com esse ETag. Creio que ele faz isso para evitar ficar enviando todos os dados do servidor para os clientes. Ele só reenvia todas as FFs quando ocorrer alguma mudança. Portanto, a bronca está do lado do servidor do GrowthBook, que por algum motivo, ele está demorando para atualizar a ETag quando a gente muda algo na página. Pelo que eu vi, não tem como a gente dizer para o GB para não usar o ETag.

## Links

:link: PR que implementa essas mudanças: <https://github.com/seazone-tech/reservas-api/pull/1201>