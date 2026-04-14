<!-- title: Auth0 | url: https://outline.seazone.com.br/doc/auth0-2tcCCeih4C | area: Tecnologia -->

# Auth0

[Auth0 Overview](https://auth0.com/docs/get-started/auth0-overview)

Auth0 é uma solução flexível e fácil de usar para adicionar serviços de autenticação e autorização às suas aplicações. Sua equipe e organização podem evitar o custo, o tempo e o risco associados à criação de sua própria solução para autenticar e autorizar usuários.

## User Account Linking

[User Account Linking](https://auth0.com/docs/manage-users/user-accounts/user-account-linking)

O Auth0 suporta a vinculação de contas de usuários de vários provedores de identidade (serviço que armazena e gerencia identidades digitais).

Por padrão o Auth0 trata todas as identidades separadas, ou seja, se um usuário fizer login primeiro no banco de dados Auth0 e depois via Google ou Facebook, essas duas tentativas irão aparecer para Auth0 como dois usuários separados.

Podemos evitar isto implementando funcionalidades que permitem com que o usuário vincule todas as suas contas.

* **Vantagens**
  * Usuário pode realizar login com qualquer provedor de identidade sem ter que criar perfis separados;
  * Usuários registrados podem usar um novo login social ou sem senha, continuando com o perfil existente;
* **Modos de implementação**

  Existem duas maneiras de implementar a vinculação de contas e nesta documentação iremos abordar sobre a **vinculação de conta sugerida**.

  O que acontece neste cenário é a identificação de contas com o mesmo endereço de e-mail e uma solicitação ao usuário para que ele mesmo vincule as contas caso deseje.
  * ex: Um usuário cria uma conta no Google utilizando usuario@email.com e depois realizar o login no Facebook, com uma conta vinculada ao mesmo e-mail.

## **Account Link Extension**

[Account Link Extension](https://auth0.com/docs/customize/extensions/account-link-extension)

É uma solução mais guiada e fácil de configurar através da Dashboard do Auth0. Essa extensão possibilita a vinculação de contas após a autenticação do usuário. Ela é acionada quando o e-mail utilizado pelo usuário autenticado é igual ao e-mail de uma conta de usuário existente associada a um provedor de identidade.

* **Ex**

  Caso o usuário realize o login utilizando sua conta do Facebook com o e-mail usuario@email.com e em outro momento realiza o login pelo Google também utilizando o e-mail usuario@email.com, a extensão entrará em ação sugerindo que o usuário vincule essas contas.

 ![Untitled](/api/attachments.redirect?id=9f0e9a98-c5c5-416f-a9be-76c59d89a62e)

* **Algumas limitações**
  * Falta de suporte para conexões sem senha;
  * Falta de suporte para fluxos utilizando autorização de dispositivo;
  * A extensão não vincula **automaticamente** usuários com o mesmo e-mail;

## **User Account Linking: Server-Side Implementation**

[User Account Linking: Server-Side Implementation](https://auth0.com/docs/manage-users/user-accounts/user-account-linking/suggested-account-linking-server-side-implementation)

Oferece controle total no servidor, sem depender da interação direta do usuário.

* A implementação do lado do servidor coloca o controle total do processo de vinculação do lado do servidor, sem envolvimento direto do cliente.
* Isso pode ser útil se você quiser gerenciar completamente a lógica de vinculação no backend, sem expor detalhes de implementação ao cliente.
* Pode ser a escolha certa se a lógica de vinculação de contas for complexa e você quiser manter o controle total no servidor.
* **Api para implementação:**

  <https://auth0.com/docs/api/management/v2/users/post-identities>

**User Account Linking: Server-Side Implementation:**

* A implementação do lado do servidor coloca o controle total do processo de vinculação do lado do servidor, sem envolvimento direto do cliente.
* Isso pode ser útil se você quiser gerenciar completamente a lógica de vinculação no backend, sem expor detalhes de implementação ao cliente.
* Pode ser a escolha certa se a lógica de vinculação de contas for complexa e você quiser manter o controle total no servidor.

## Obeservações

* Ao customizar a extensão (html), a interface de login já existente irá ser substituída pela UI antiga (feia) e case seja do nosso interesse teremos que modificá-la para ficar com a aparência que desejamos.
* Caso o usuário só possua como Identity Provider o Google/Gmail, ele não irá conseguir receber um e-mail de recuperação de senha e isso faz sentido já que ele não está sendo autenticado através do Database do Auth0, mas sim pelo Google/Gmail. Devemos lembrar que são Identity Provider distintos. Porém se ele estiver apenas/também cadastrado no Database do Auth0 (Primary Identity Provider ou Account Associated) ele receberá o e-mail como é o esperado. Caso o usuário queira alterar a senha da sua conta Google, precisará fazer isso pelo sua conta do Google/Gmail, o que não está diretamente relacionado ao Auth0. É fundamental o entendimento que essas são plataformas distintas, cada uma com suas próprias configurações e processos de gerenciamento de conta.