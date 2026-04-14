<!-- title: State | url: https://outline.seazone.com.br/doc/state-cdsGEtI2pd | area: Tecnologia -->

# State

## O que é state

O parâmetro **state** em protocolos de autorização serve para restaurar o estado anterior de uma aplicação. Ele armazena informações definidas pelo usuário durante uma solicitação de autorização e as retorna na resposta.

Essa medida é fundamental para proteger contra ataques CSRF, nos quais um usuário é enganado para executar ações não desejadas em uma aplicação web em que está autenticado.

Para implementar essa segurança, ao iniciar uma solicitação de autenticação, envia-se um valor aleatório como estado e valida-se o valor recebido ao processar a resposta. Esses valores são armazenados no lado do cliente (em cookies, sessão ou localstorage) para permitir a validação. Se a resposta retornar com um estado diferente, é possível inferir que pode estar ocorrendo um ataque, pois seria uma resposta não solicitada ou uma tentativa de falsificação.


---

## Problema que enfrentamos

No dia 26/04/2024 foi feita uma investigação para entender o motivo pelo qual alguns usários recebiam um internal server: [CSRF Warning! State not equal in request and response](https://us-west-2.console.aws.amazon.com/cloudwatch/home?region=us-west-2#logsV2:log-groups/log-group/$252Fecs$252Fseazone-reservas-api-staging/log-events/ecs$252Fseazone-reservas-api$252F3de28346b6a44ed69710e9262479e885$3Fstart$3D1710787507764$26refEventId$3D38151836301704268681063073201747836567227085735834878128) na tentativa de se logar ao sistema do website reservas.

Ao realizar uma análise de como estava estruturado o código que envolve a **lógica do fluxo de login/autenticação**, identificamos um problema de incompatibilidade de estados devido à ausência do argumento `state` no método `oauth.auth0.authorize_redirect()`.

Isso resultou em uma exceção chamada `MismatchingStateError()` ao tentar validar o login no **callback** através do método `oauth.auth0.authorize_access_token()`, causando um erro interno no servidor e fazendo com que a experiência do usuário fosse prejudicada já que esse erro era exibido na tela.

Exemplo: Se o valor de state em `/login` for foo_123 e no `/callback` for bar_456 ocorrerá uma exceção `MismatchingStateError()` por conta da incompatibilidade de estado citada acima.


---

## Solução encontrada

Como sugerido na documentação do [FastAPI OAuth Client](https://docs.authlib.org/en/latest/client/fastapi.html#fastapi-oauth-client) devemos adicionar ao app um middleware chamado `SessionMiddleware` para que seja possível gerenciar sessões de usuário já que ele permite o armazenamento dados específicos como informaçãoes relacionadas ao login entre consecutivas solicitações HTTP.

```python
app = FastAPI()
# Devemos adicionar o SessionMiddleware para salvar temporariamente
# o state na sessão em uso
app.add_middleware(SessionMiddleware, secret_key="some-random-string-token")
```

Após adicionarmos `SessionMiddleware` ao nosso app precisamos realizar a verificação do `state` em duas rotas:

* `/login`
  * Criamos uma variável `state` que receberá um token gerado utilizando a biblioteca *built-in*  `secrets`;
  * Adicionamos esse mesmo `state` à sessão da requisição;
  * Adicionamos esse mesmo `state` ao método `authorize_redirect()` para informar ao **Auth0** qual usuário está interagindo com o aplicativo. Isso ajuda a garantir a segurança da sessão e permite que o Auth0 identifique corretamente o usuário durante o processo de autorização.

  ```python
  # Geração do state através da lib secrets
  state = secrets.token_urlsafe(32)
  # Associação do state à sessão da requisição
  request.session['oauth_state'] = state
  
  # Informando ao auth0 o state daquela sessão
  oauth.auth0.authorize_redirect(
          request=request,
          redirect_url="https://exemplo.com.br",
          audience="autho_audience_api_example",
          state=state
      )
  ```
* `/callback`
  * Recuperamos o `state` da sessão informado na rota `/login`;
  * Recuperamos o `state` do parâmetro de consulta localizado em `https://api.com.br?state='estado_gerado_no_login'` (informado pelo auth0 após `authorize_redirect()`);
  * Verificamos se o `state` da sessão é diferente do `state` informado no parâmetro de consulta.
  * Caso os `states` sejam **diferentes** tratamos a exceção para que usuário não receba mais internal server error.

  ```python
  # Recupera estado da sessão 
  session_state = request.session.get('oauth_state')
  # Recupera estado do parâmetro de consulta informado pelo auth0
  request_state = request.query_params.get('state')
  
  try:
  	# Verifica se estados são diferentes
  	if session_state != request_state:
  		logger.info("State mismatch in request: %s", request.__dict__)
  		# Caso estados sejam diferentes subimos a exceção StateMismatch 
  		raise StateMismatch()
  
  except StateMismatch:
      # Caso exceção seja lançada, retornamos usuário para url de redirecionamento
      return RedirectResponse("url_de_redirecionamento")
  ```


---

## Links extras

Evitar ataques e redirecionar usuários com parâmetros de estado com OAuth 2.0 → **<https://auth0.com/docs/secure/attack-protection/state-parameters>**