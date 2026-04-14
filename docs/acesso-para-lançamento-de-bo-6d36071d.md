<!-- title: Acesso para Lançamento de BO | url: https://outline.seazone.com.br/doc/acesso-para-lancamento-de-bo-iScScA4XLl | area: Tecnologia -->

# Acesso para Lançamento de BO

### Criar ou liberar acessos para visualização de BOs

Para que um Seazoner visualize, busque e adicione BOs, ele precisa ser um usuário com `main_role` = Seazone ou Attendant. 


Então para que o Seazoner tenha acesso a esta página, seu usuário deve está ativo na `account_user` e possuir registro nas tabelas que definem sua role. 

**Por exemplo:** Se ele for `main_role = Seazone`, ele deve conter registro na tabela `account_seazone` com o atributo `department = Administrative`.


Se o usuário existir na `account_user` e não possuir registro na `account_seazone`, você pode adicionar de forma manual pelo DBeaver ou com a query abaixo, substituíndo a "`?`" pelo `user_id` do Seazoner:

`***insert into*** *account_seazone (id, created_at, updated_at, department, user_id)* ***values*** *(****default****,* ***now****(),* ***now****(), 'Administrative', ?);*`

> **Obs:** se o usuário não existir, a criação é feita [==via Django==](https://api.sapron.com.br/admin/account/user/): depois de criar a conta, verifique se a `main_role = Seazone` e adicione um registro na `account_seazone` referenciando o usuário recém criado.


\
### Combinações que consegue acessar a opção de Hospede > Lançamento de BO 

| **mainRole** | **Department** |
|----|----|
| Attendant | Null |
| Attendant | Onboarding |