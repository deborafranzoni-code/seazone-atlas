<!-- title: Auth0 | url: https://outline.seazone.com.br/doc/auth0-xc7TRzWcvr | area: Tecnologia -->

# Auth0

## Para que usamos o Auth0?

O [Auth0](https://auth0.com/) é a plataforma que utilizamos para realizar a autentição (login) do usuário no site de reservas.

Para acessar a conta do Auth0 é preciso solicitar que você seja adicionado à ela. Você poderá solicitar ao: @[Bernardo Ribeiro](mention://e14183b4-61c2-4968-b64b-a746e4a5a0f3/user/d68e5193-1b5c-492d-bca8-56f01bad14a7) ou @[Maria Fernanda Vaz Romero](mention://26d1337b-4b58-4b42-9c06-8c86d5584d83/user/20053ef3-06e9-418b-900f-9eee99d3badb) , que são admins da conta do auth0.

[Auth0: Secure access for everyone. But not just anyone.](https://auth0.com/)



---

## Roles (papéis)

### **Como crio uma nova Role?**


1. Abrir auth0
2. No **Menu lateral**, acessar a opção: **User management > Roles**
3. Clique em **"Create Role"**
4. Preencha os dados no modal e clique em **"Create"**
5. Fim. Para adicionar usuário à essa Role, siga [esses passos](/doc/auth0-PsX5OvzmUU).

### Settings

Nessa aba você pode alterar o nome e descrição da role ou deletá-la.

### Permissions

Nessa aba é possível gerenciar as permissões que os usuários com essa role terão.

### Users

### Como atribuir uma **Role** a um usuário?


1. Abrir [auth0](auth0.com) e fazer login na sua conta. (Caso não tenha acesso solicite ao Bernardo Ribeiro)
2. No **Menu lateral**, acessar a opção: **User management > Roles**
3. Clique na **nome** da role que deseja adicionar o usuário.
4. Vá na terceira aba: **"Users"**. Ao clicar, verá uma lista com todos os usuários que possuem essa role.
5. Clique em **"Add Users"** > Pesquise pelo **Email ou Nome** do usuário
6. Selecione o usuário que deseja vincular à role (pode adicionar mais de um ao mesmo tempo)
7. Clique em **"Assign"** para vincular a role ao usuário
8. **FIM**

### Como adicionar a role "Admin" a um usuário?

Esse caso, é um onde normalmente você vai se encontrar na necessidade de fazer um request em  uma "API gerencial" como Admin.

Porém, para que seu barear token tenham esse nível de permissão, você precisa adicionar essa role ao seu login pelo Auth0 seguindo [essas instruções](/doc/auth0-PsX5OvzmUU), porém no **PASSO 3,** selecione a role **"Admin"**

Ao atribuir "Admin" à algum usuário, ele terá as seguintes permissões em seu escopo:

 ![Untitled](/api/attachments.redirect?id=ff56cad0-1b2f-4b1c-b60e-34a635f7bff7)


---

## Páginas extras

[State](/doc/state-5HWWFaQpyb)

[Auth0](/doc/auth0-7AKhn26FC9)


---