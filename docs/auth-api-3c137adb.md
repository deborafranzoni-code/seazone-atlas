<!-- title: Auth API | url: https://outline.seazone.com.br/doc/auth-api-3KkEOBneyC | area: Tecnologia -->

# Auth API

### Serviço utilizado para autenticação

Utilizamos o [Auth0](/doc/auth0-PsX5OvzmUU) para autenticar os usuários.

## Como funciona login?

Exemplo de login em Staging:

* Acessar: [https://api.staging.reservas.sapron.com.br/auth/login?redirect_to=https://seazone-reservas-staging.vercel.app](https://api.staging.reservas.sapron.com.br/auth/login?redirect_to=https://seazone.com.br)
  * Será redirecionado para o fluxo de login gerenciado pelo **[Auth0](https://auth0.com/)**.
  * Após concluir o login a será redirecionado para a URL informada no parâmetro **"redirect_to".** Após o redirect na URL terá um parâmetro `auth_token`. **Exemplo**: `http://localhost:3000/?auth_token=eyJhbGciOiJ...`

    <aside> ℹ️ O token retornado é do tipo **Barear token**

    </aside>
* Nesse momento o Frontend deverá entender que existe um token na URL e guardar ele para usar ao longo da aplicação.
* A primeira coisa que o Frontend pode fazer ao obter o token é chamar o endpoint `/user/me` para pegar os dados do usuário que acabou de logar.

  **Exemplo:**

  ```bash
  curl -X 'GET' \
  'https://api.staging.reservas.sapron.com.br/users/me' \
  -H 'accept: application/json' \
  -H 'Authorization: Bearer eyJhbGciOiJSUz...
  ```


---

### Setup Auth0 <> Google OAuth

> **Obs:** Essa configuração de integração foi realizada apenas no **ambiente de produção** em staging está sendo usado as *developer keys* que o proprio Auth0 disponibiliza, por isso é mostrado aquele warning no canto superior direito ao fazer login em staging.

Para acessar a página onde está configurada a integração do Auth0 com OAuth, no menu lateral vá em: Authentication > Social > **google-oauth2**

As informações das configuração realizadas no Google Cloud e as chaves podem ser encontradas [nesta página](https://console.cloud.google.com/apis/credentials?authuser=1&project=site-de-reservas&supportedpurview=project) (necessário login com a conta do site de reservas).

Toda a configuração das credenciais na integração do OAuth do Google com o Auth0 foi realizada seguindo esta documentação:


**Como testar a conexão/integração**

[Test Connections](https://auth0.com/docs/authenticate/identity-providers/test-connections)