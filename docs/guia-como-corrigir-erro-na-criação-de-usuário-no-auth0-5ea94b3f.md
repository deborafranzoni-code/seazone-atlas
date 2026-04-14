<!-- title: Guia: Como Corrigir Erro na Criação de Usuário no Auth0 | url: https://outline.seazone.com.br/doc/guia-como-corrigir-erro-na-criacao-de-usuario-no-auth0-FWECwStumF | area: Tecnologia -->

# Guia: Como Corrigir Erro na Criação de Usuário no Auth0

# Objetivo

Esse documento tem como objetivo descrever o processo de correção para casos em que a criação de usuários no Auth0 falhar.

# Contexto

No documento [Perfomance | Análise API de Criação de Reserva](/doc/perfomance-analise-api-de-criacao-de-reserva-A0i47iz5Uh), foi identificado que um dos principais gargalos de desempenho da rota de criação de reserva está no processo de criação do usuário no Auth0. Com o objetivo de melhorar a performance, optou-se por separar essa etapa em uma task assíncrona, responsável exclusivamente por criar o usuário no Auth0. Dessa forma, a rota de criação de reserva apenas aciona a task e segue sua execução normalmente, sem aguardar o resultado da criação do usuário.

Essa nova abordagem apresenta um único trade-off: caso a criação do usuário no Auth0 falhe por algum motivo, ele não poderá realizar login no nosso site posteriormente. Porém, o usuário continuará apto a realizar compras normalmente, sendo a restrição válida apenas para o acesso via login.

Visando driblar esse problema, este guia mostrará como corrigir isso e possibilitar que o usuário consiga logar.

# Passo a Passo

Quando a criação de um usuário falhar, um alerta será disparado no canal `#website-alerts` contendo o email do hóspede. Com essa informação em mãos, siga o passo a passo:


1. Acesse o banco de dados e localize o usuário em questão com a query a seguir:

   ```sql
   SELECT * FROM users WHERE email = {email_do_alerta}
   ```

   note que a coluna auth0_id está vázia, isso é parte do problema, precisaremos criar o usuário e preenchê-la.
2. Acesse o [Auth0](https://accounts.auth0.com/teams/team-5o2ndht/tenants) e localize no menu da esquerda **User Management > Users;**
3. Já na seção **Users**, clique no botão do canto superior direito "Create User" e selecione a opção "Create via UI";

   ![](/api/attachments.redirect?id=6a205cb6-620f-424d-8b84-ba34922b3c5d)
4. Preencha o formulário com o email do alerta e uma senha, a senha não importa verdadeiramente, no processo via código é gerada uma senha aletatória, portando você pode usar um [Gerador de Senhas](https://www.4devs.com.br/gerador_de_senha) qualquer.

   ![](/api/attachments.redirect?id=f43087d5-3e1d-4162-a5d1-ea53478e65e8)
5. Após preencher o formulário e clicar em "Create", copie o auth0 id que irá aparecer na tela para qual você será redirecionado.![](/api/attachments.redirect?id=203a7be7-0975-4156-b347-a2fdcf8ff3bb);
6. Com o `auth0_id` em mãos, execute a query a seguir no bando de dados:

   ```sql
   UPDATE users
   SET auth0_id = 'auth0id_retorado'
   WHERE email = 'email_do_alerta'; -- aqui você pode usar o id do usuário se preferir
   ```
7. Pronto! Com esse processo feito o hóspede conseguirá prosseguir da tela de login para a recuperação de senha.