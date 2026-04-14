<!-- title: Imóveis | url: https://outline.seazone.com.br/doc/imoveis-O3GUtACXfc | area: Tecnologia -->

# Imóveis

Atualmente importamos da Stays todos os imóveis que há lá. A task `stays.pull_properties` no Celery é responsável por fazer essa sincronização rodando a cada:

* `30 minutos` no ambiente de Produção
* `2 vezes` ao dia em **Staging**

**API utilizada:** `GET /external/v1/content/listings`. Também é importado do BD do Sapron, informações dos imóveis.

Além de criar os novos imóveis inseridos na Stays, ela também atualiza os imóveis existentes com os dados que estão na Stays.

**Importante:** Se alterarmos alguma informação manualmente, vai **sobrescrever** com o que vem da Stays quando o processo de atualização/importação rodar. Se quisermos ignorar alguma informação que vem da Stays para alguns campos, temos que implementar algo nesse sentido. Se quisermos alterar alguma informação de imóvel, esta deve ser alterada na Stays para que seja sincronizado pelo site na próxima vez que a task do celery rodar.


---

### Como rodar a **Sincronização de imóveis** manualmente?

⚠️ **Requisito: Ter role de admin no auth0. [Como adicionar a role "Admin" a um usuário?](/doc/auth0-PsX5OvzmUU)**

Passo a Passo:


1. Realize sua autenticação com o swagger: **[Como se autenticar no Swagger?](/doc/swagger-c7QA28YdX3)**
2. Clique na API **PUT /tasks/sync_properties**
3. Clique em **Try it out** > **Execute**
4. Se tudo tiver dado certo você irá receber um "ok" como response. Caso tenha recebido um erro 403 "forbiden", significa que você não possui permissão de **Admin** para essa API. Para isso, siga esses passos de  [Como adicionar a role "Admin" a um usuário?](/doc/auth0-PsX5OvzmUU)