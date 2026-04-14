<!-- title: Login de teste para o Atendimento em Staging | url: https://outline.seazone.com.br/doc/login-de-teste-para-o-atendimento-em-staging-PqwPbpnJm3 | area: Tecnologia -->

# Login de teste para o Atendimento em Staging

**Observações**

Para conseguir resolver esse suporte é preciso ter acesso ao **Banco de Dados do Sapron de Staging  e acesso ao Admin do Django em Staging**.

**Contexto**

Nesse contexto de suporte, o que aconteceu  foi que quando o banco de dados de Produção foi  clonado para Staging, as contas de teste com perfil de Proprietário que o pessoal usava para mostrar aos possíveis proprietários, foram excluídas, e alguém abriu suporte dizendo que não estava conseguindo entrar com a conta de teste em Staging.

**Possível Solução**

1 - Criar uma conta de usuário na tabela `user` através do Admin do Django  para o e-mail que a pessoa que criou o suporte enviou, depois adicionar esse usuário criado na tabela a qual role ele pertence, podendo ser `Attendants , Host , Owner , Partners`

2 - Para completar  o suporte quando o perfil de teste é para ser usado como forma de mostrar aos possíveis clientes, é preciso associar à esse perfil algum imóvel, para que os valores dele seja refletido no Sapron.

O mode de fazer isso é:


1. Identificar quais imóveis(códigos do imóvel) serão associados ao perfil. Ex: JBV222, VLR401…
2. Depois ir no Dbeaver na tabela de Propriedade `property_proverty`   e fazer uma pesquisa pelo código do  imóvel para pegar o ID único . EX:  code = 'VLR401'
3. Vamos precisar pegar o ID do usuário pelo Dbeaver  na tabela de `account_user`  para isso vamos pesquisar pelo e-mail do perfil. EX: email = 'prop.teste@seazone.com.br'
4. Agora vamos identificar o ID do usuário  na tabela de role dele, nesse caso de suporte a role do perfil de usuário era a de  OWNER, pra  pegar o ID dele  vá no Dbeaver na tabela de `account_owner`  e pesquise pelo ID no usuário. Ex: user_id = 50411
5. Com esses IDs(ID da propriedade/imóvel e ID do perfil na tabela de role) em mãos, vamos agora última tabela no Dbeaver, que é a tabela de `property_property_owners` . Pesquise pelo ID no imóvel, na linha do resultado terá a coluna `owner_id`  clique duas vezes para editar e  coloque o ID do perfil encontrado na tabela da role do perfil.
6. Faça isso para associar quantos imóveis forem precisos.
7. Por fim, entre na conta de perfil de teste que criou e veja se os imóveis que você adicionou  estão aparecendo.

**Entenda mais  esse contexto lendo a conversa  do suporte**: [https://seazone-fund.slack.com/archives/C02H5GM0VB5/p1683899405927859](https://seazone-fund.slack.com/archives/C02H5GM0VB5/p1684788575577909)

**Algumas informações importantes para conseguir realizar o suporte:**

* E-mail  e senha de teste
* Imóveis que serão associado á conta de teste

 ![Untitled](/api/attachments.redirect?id=dd67364a-daec-4bc1-977c-abe2800e862b)

 ![Untitled](/api/attachments.redirect?id=aa3c073c-2b15-4a95-990c-0d971bed8ec2)

 ![Untitled](/api/attachments.redirect?id=0b5f467c-54ae-4d8f-9f81-dfd877676e75)

 ![Untitled](/api/attachments.redirect?id=67ff9c25-7a40-46b5-8c54-80abab4f73bf)

 ![Untitled](/api/attachments.redirect?id=5aa50ca4-6267-48a6-81f9-84cdcdc63523)