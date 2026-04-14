<!-- title: Autenticação de usuário | url: https://outline.seazone.com.br/doc/autenticacao-de-usuario-ficB9YMykX | area: Tecnologia -->

# Autenticação de usuário

Created by: Bernardo Ribeiro Author: Bernardo Ribeiro Created time: June 19, 2024 10:39 AM Last edited: June 25, 2024 10:54 AM Tags: Auth0, Cadastro, Login

## Como funciona login?

### Exemplo de login em Staging:

* Acessar: `{base_url}/auth/login`
  * Será redirecionado para o fluxo de login gerenciado pelo [Auth0](https://auth0.com/).
  * Após concluir o login a será redirecionado para o frontend e na url terá um parâmetro `auth_token`.
  * Exemplo: <http://localhost:3000/?auth_token=eyJhbGciOiJ>...

    <aside> ℹ️ O token retornado é do tipo **Barear token**

    </aside>
* Nesse momento o frontend deverá entender que existe um token na url e guardar ele para usar ao longo da aplição.
  * A primeira coisa que o frontend pode fazer ao obter o token é chamar o endpoint `{base_url}/user/me` para pegar os dados do usuário que acabou de logar.

### Adicionar redirecionamento customizado no login:

* Quero redirecinar para `https://seazone-reservas-staging.vercel.app/pagina/teste?p=1&p=2` após o login.
* Primeira coisa é usar o encode na url, desse modo a url encodada ficará: `https%3A%2F%2Fseazone-reservas-staging.vercel.app%2Fpagina%2Fteste%3Fp%3D1%26p%3D2`
* Enviar o parâmetro `redirect_to=<URL>`. Exemplo:
  * <https://api.staging.reservas.sapron.com.br/auth/login?redirect_to=https%3A%2F%2Fseazone-reservas-staging.vercel.app%2Fpagina%2Fteste%3Fp%3D1%26p%3D2>


\
## Implementação do Login

### Login

### Callback

O objeto `auth_metadata` possui as seguintes informações:

```json
{
    "access_token": "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ii1xYi1wQXNaSi01dDl3VFh5dE8tUyJ9.eyJp...", // se parece com id_token mas não é igual
    "id_token": "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ii1xYi1wQXNaSi01dDl3VFh5dE8tUyJ9.eyJua...",    // se parece com access_token mas não é igual
    "scope": "openid profile email",
    "expires_in": 86400,
    "token_type": "Bearer",
    "expires_at": 1732662220,
    "userinfo": {
        "nickname": "b.ribeiro",
        "name": "b.ribeiro@seazone.com.br",
        "picture": "https://s.gravatar.com/avatar/a73abcc2b19...",
        "updated_at": "2024-11-25T22:55:15.367Z",
        "email": "b.ribeiro@seazone.com.br",
        "email_verified": True, // pode ser usado futuramente para direcionar o usuário diretamente para a página de confirmar email
        "iss": "https://seazone-dev.us.auth0.com/",
        "aud": "JY7sRG0edOtmDyWt...",
        "iat": 1732575820,
        "exp": 1732611820,
        "sub": "auth0|6656854ba5...", // auth0 user_id (mesmo valor salvo no campo auth0_id na tabela users)
        "sid": "c1RNpsN...",
        "nonce": "moaryNn..."
    }
}
```

### Logout