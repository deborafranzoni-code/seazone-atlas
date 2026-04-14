<!-- title: Permissões nas rotas do Sapron | url: https://outline.seazone.com.br/doc/permissoes-nas-rotas-do-sapron-OfbBu1wCLk | area: Tecnologia -->

# Permissões nas rotas do Sapron

## Ajustes Necessários

### 1. Inserir rate limit nas rotas de atualização \[DONE\]

O objetivo dessa atividade é não permitir atualizações simultâneas de um mesmo usuário, o que poderia ocorrer caso o indivíduo utilizasse algum script.

PRs criadas:

* [sapron-backend:1188](https://github.com/seazone-tech/sapron-backend/pull/1188) 
* [sapron-frontend:1090](https://github.com/seazone-tech/sapron-frontend/pull/1090)

### 2. Adicionar logs em algumas rotas \[DONE\]

O objetivo dessa atividade seria adicionar mensagens de logs em algumas rotas de atualização que não possuem tabela de auditoria, para a gente salvar os dados antes e depois dos ajustes. Com isso, conseguiriamos fazer um rollback dos dados, se fosse necessário.

Adicionamos logs nas seguintes rotas:

* `PUT/PATCH /account/address/{id}/`
* `PUT/PATCH /properties/{id}/address/`
* `PUT/PATCH /account/partner/{id}/`

PRs criadas:

* [sapron-backend:1188](https://github.com/seazone-tech/sapron-backend/pull/1188) 

### 3. Ajustar rotas de atualização

Atualmente, as rotas do Sapron possuem um esquema de permissão baseado em roles, em que indicamos quais roles podem usar determinadas rotas. Porém, quando indicamos que uma role pode utilizar uma rota, a gente dá permissão total ao usuário que possui essa role.

Por exemplo, são quatro roles que podem utilizar a rota `PATCH /account/partner/{id}`: "Admin", "Partner", "Seazone" e "Attendant". Porém, ao meu ver, o usuário com a role "Partner" só deveria ser capaz de atualizar os dados dele próprio. Ele não deveria ser capaz de atualizar os dados de qualquer parceiro. Se um parceiro possui o ID 1000, ele só deveria atualizar os dados desse ID 1000. Os demais parceiros deveriam ser bloqueados. Somente os usuários Admin ou Seazone que deveriam de fato ter permissão para alterar os dados de todos os parceiros.

Portanto, precisamos ajustar todas as rotas de update para, a depender da role do usuário, permitir que ele só atualize os registros referentes ao seu usuário.

### 4. Inserir permissão para as rotas de endereço

As rotas `[PUT|PATCH] /account/address` e `[PUT|PATCH] /properties/{id}/address/` possuem somente a permissão "IsAuthenticated". Ou seja, para usar essas rotas, bastaria que o usuário estivesse autenticado para realizar ajustes nos endereços. Isso se agrava quando consideramos o problema descrito no caso 3, pois um usuário autenticado no Sapron consegue atualizar os endereços de qualquer outro usuário.

Portanto, o ideal é que essas rotas tenham outras roles. Como essas rotas são chamadas juntas com outras, para não termos problemas, o certo seria que essas rotas de endereço tivessem as seguintes roles:

* IsAdmin, IsSeazone, IsSeazoneOnboarding, IsOwner, IsPartner, IsAttendant

### 5. Revisar as colunas de permissões dos usuários no BD

Há 3 colunas na tabela `account_user` que dá algum tipo de permissão aos usuários:

* *main_role*: define a role do usuário, que pode ser: "Admin", "Attendant", "Guest", "Host", "Owner", "Partner" e "Seazone";
* *is_superuser*: quando esse campo é marcado como True, o usuário adquire a role "Admin";
* *is_staff*: quando esse campo é marcado como True, esse usuário consegue acessar a página administrativa do Django.

Na nossa Allow List, temos 38 usuários com permissão de update.

Temos atualmente 181 usuários ativos com permissões "Admin" ou "Seazone", que são roles com alta permissão no Backoffice:

* Usuários "Admin": 63
* Usuários "Seazone": 118

Entre os usuários "is_superuser", temos 16, sendo que nem todos estão na nossa allow list.

Entre os usuários com "is_staff" igual a True, temos 27 com role Admin, o que dá poderes a eles de alterar os dados dos usuários na plataforma do Django. Alguns desses usuários já não trabalham mais na Seazone.

Precisamos rever as permissões de todos esses usuários. Somente alguns poucos usuários deveriam ter permissão "Admin" ou "is_superuser". Os demais usuários "Admin" teriam que alterar a permissão para "Seazone".

### 6. Bloquear rotas de update para usuários "Seazone"

Bloquear as rotas de update para os usuários com main_role "Seazone" (usuário "Admin" estaria liberado). Só deixar usar as rotas de update os usuários "Seazone" com uma role específica. Por exemplo, liberar as rotas que estão bloqueadas hoje somente aos usuários "Seazone" que forem do departamento "Administrative".

A gente manteria a main_role "Seazone" para esses usuários. A ideia seria apenas diferenciar os usuários Seazone que podem fazer update daqueles que não podem.