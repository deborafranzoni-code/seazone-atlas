<!-- title: Sapron | url: https://outline.seazone.com.br/doc/sapron-j1k3r8Ldz3 | area: Tecnologia -->

# Sapron

O Sapron é o nosso sistema de gerenciamento de propriedades, utilizado para diversas atividades na Seazone. Atualmente, a criação e o gerenciamento dos usuários de backoffice são realizados pelo time de Governança.

### Criar usuários

1️⃣ Acesse o [admin do django](https://api.sapron.com.br/admin/)

2️⃣ Na opção de users clique em add

 ![Captura de tela 2024-09-16 140324.png](/api/attachments.redirect?id=112ffbbc-cb0f-4258-9bf4-067b5c271b3a)

3️⃣ Adicione as informações do usuário e no campo main role selecione a opção que condiz as permissões solicitadas

* A role **seazone** permite que você adicione o usuário com a permissão de **onboarding** ou **administrativo financeiro**
* **Attedant** libera permissões de atendente

 ![Captura de tela 2024-09-16 140511.png](/api/attachments.redirect?id=7b749cdb-4fe9-46a4-a1ff-6db0889a5e2c)

4️⃣ Gere a senha e deixe armanezada em algum local para ser enviada ao usuário, para gerar utilize algum gerador de senhas aleatórias :

https://www.lastpass.com/pt/features/password-generator

https://www.4devs.com.br/gerador_de_senha

https://www.avast.com/pt-br/random-password-generator#pc

5️⃣ Acesse o dbeaver e utilize o email do usuário para pesquisar o perfil dele na tabela **account_users** e colete o **Id:**

 ![Captura de tela 2024-09-16 142821.png](/api/attachments.redirect?id=850bec1a-25f4-4d0c-8c07-8f576aeacb8c)

6️⃣ Adicione ele na tabela correspondente as permissões solicitadas :

* Para permissões de onboarding, administrativo financeiro ou admin a tabela é

 ![Captura de tela 2024-09-16 143416.png](/api/attachments.redirect?id=945cc19a-b215-475d-a12f-6c0834633e38)

* Para atendentes a conta é **account_attedant**

 ![Captura de tela 2024-09-16 143553.png](/api/attachments.redirect?id=267635e5-1b24-4f30-a354-dc0ecf2a5d1d)

### Recuperar usuários

1️⃣ Acesse o [admin do django](https://api.sapron.com.br/admin/)

2️⃣ Pesquise pelo usuário desejado na tabela **account_users**

3️⃣ Abra o perfil do usuário

 ![Captura de tela 2024-09-16 145120.png](/api/attachments.redirect?id=16e7204e-7d99-4b11-b9cf-b51a7f6663a5)

4️⃣ Na seção de password clique em **this form** e adicione a nova senha , para gerar a senha utilize algum gerador de senha automático :

https://www.lastpass.com/pt/features/password-generator

https://www.4devs.com.br/gerador_de_senha

https://www.avast.com/pt-br/random-password-generator#pc

### Desativar usuários

Acesse o [admin do django](https://api.sapron.com.br/admin/)

2️⃣ Pesquise pelo usuário desejado na tabela **account_users**

3️⃣ Abra o perfil do usuário

4️⃣ Desmarque a opção **is active**

 ![Captura de tela 2024-09-16 145503.png](/api/attachments.redirect?id=e1036551-0b49-498d-a082-df8fc0b3610f)

### Mudar permissões

1️⃣ Acesse o [admin do django](https://api.sapron.com.br/admin/)

2️⃣ Pesquise pelo usuário desejado na tabela **account_users**

3️⃣ Abra o perfil do usuário

4️⃣ Se necessário vá até o campo **Main Role** e troque a role do usuário as roles de backoffice são **Attedant** para atendentes , **seazone** pra onboarding e administrativo financeiro e **admin** para admins da aplicação

 ![image.png](/api/attachments.redirect?id=9df137d6-dabf-4b85-9087-1932fa2dc75f)

5️⃣ Entre no Dbeaver pesquise na tabela **account_user** pelo ID do usuário e faça a mudança necessária na tabela

* Para mudar a permissão de onboarding para Administrativo e vice versa basta acessar a **account_seazone** e trocar o campo **department**
* Para mudar a permissão de atendente para onboarding ou administrativo o usuário deve ser inserido na **account_seazone** com o department desejado, também deve ser removido da **account_attedant**
* Para ser admin o usuário tem que estar na **account_seazone** , caso contrário ele faz login mas não aparece nada na tela

### Adicionar IP no security group

1️⃣ [Acesse a AWS](https://d-926761dadf.awsapps.com/start/#/?tab=accounts) na conta Seazone Technology

2️⃣ Abra a EC2

 ![image.png](/api/attachments.redirect?id=25232144-04a9-46e1-acf6-984434f3905d)

3️⃣ Acesse o recurso de **security groups**

 ![image.png](/api/attachments.redirect?id=e02b795d-8b1d-48cc-aed3-5e289d3951b2)

4️⃣ pesquise pelo security group rds-sapron-production-sg

 ![image.png](/api/attachments.redirect?id=898f2b43-1a7a-4b40-bc8a-a2b3f83dee6a)

5️⃣ Clique em **edit inbound rules** e adicione ou atualize seu **IP**

 ![image.png](/api/attachments.redirect?id=c0077251-6c0f-4bda-ae93-48ce821c7f55)

## Tabela de responsabilidades 🫂

| Responsabilidade | Responsável |
|----|----|
| Criar contas backoffice | Governança |
| Remover contas backoffice | Governança |
| Recuperar contas backoffice | Governança |
| Gerenciar contas de proprietários | Proprietário/ Time Sapron / CS proprietários |
| Gerenciar contas de parceiros | Parceiros / Time Sapron / Time de parcerias |
| Gerenciar contas de Franqueados (Anfitriões) | Franqueado/ Time Sapron / Time de franquias |