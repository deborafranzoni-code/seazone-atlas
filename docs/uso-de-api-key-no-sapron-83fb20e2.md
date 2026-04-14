<!-- title: Uso de API Key no Sapron | url: https://outline.seazone.com.br/doc/uso-de-api-key-no-sapron-wLkeU4sNKK | area: Tecnologia -->

# 🔐 Uso de API Key no Sapron

* [Link do épico no Jira](https://seazone.atlassian.net/browse/SAP-3013)

# TL;DR

Permitir que requisições HTTP sejam feitas para a API do Sapron através de uma API Key.

# Problema

Inicialmente, o Sapron foi criado de forma a atender apenas a aplicação de mesmo nome (sapron.com.br). Contudo, conforme a evolução dos produtos Seazone, diversas aplicações/automações surgiram, necessitando utilizar a API do Sapron. Para tal, é necessário criar um usuário (e-mail e senha), solicitar um *access token* através do endpoint `POST /account/login/token` e propagá-lo às requisições seguintes.

Com isso, toda automação/aplicação que deseja utilizar a API do Sapron deve previamente possuir uma conta (login e senha) e deve solicitar um *access token* antes de toda e qualquer requisição.

Além disso, não se tem uma visibilidade clara se um dado usuário criado está fazendo "requisições manuais" utilizando a aplicação ou "requisições programáticas" utilizando a API diretamente.

# Objetivo

Considerando os problemas supracitados, o objetivo desta RFC é, principalmente, permitir que automações/aplicações utilizem a API do Sapron sem a necessidade de autenticação utilizando e-mail e senha. Além disso, deve-se monitorar as requisições feitas utilizando API Key.

# Arquitetura (MVP)

Na versão inicial, a ideia é criar uma API Key que permita a **PERSONIFICAÇÃO** de um usuário da Seazone. Dessa forma, a API Key age como um *access token* "constante" e "pré-gerado", podendo ou não ter tempo de expiração. 

Isso permite a fácil integração da funcionalidade com o sistema, considerando que a API atual sabe lidar com usuários e suas relações.

## Banco de Dados

Em termos de persistência de dados, a ideia é criar a tabela `account_user_api_keys`, responsável por armazenar todas as API Keys criadas para os usuários que serão personificados no sistema:

 ![Imagem 1 - Schema da tabela account_user_api_keys](/api/attachments.redirect?id=652a93ee-79bc-4b0e-8063-81859ea1b19e " =1518x767")Abaixo, uma breve descrição das colunas que compõem a tabela `account_user_api_keys`:

| coluna | descrição |
|----|----|
| id | obrigatório; identificador único do registro |
| created_at | obrigatório; timestamp da criação |
| updated_at | obrigatório; timestamp da atualização |
| created_by_user_id | obrigatório; FK para account_user; identificador do usuário que criou a API Key (auditoria) |
| user_id | obrigatório; FK para account_user; identificador do usuário para o qual será criada a API Key |
| token | obrigatório; valor criptografado da API Key |
| is_active | obrigatório; sinaliza se uma dada API Key está ativa para uso |
| last_use_date | opcional; timestamp de quando a API Key foi utilizada pela última vez; se nunca foi utilizada, deve ser NULL |
| expiration_date | opcional; timestamp de quando a API Key deixará de ser válida; se não tem prazo de validade, deve ser NULL |

## Validação da API Key

No código, o seguinte fluxo para validação da API Key deverá ser implementado:

 ![Imagem 2 - Fluxo de validação da API Key](/api/attachments.redirect?id=5401d152-5806-4d37-85c2-abe60af9d5e8 " =1441x544")Na prática, os seguintes passos deverão ser codificados:

* A requisição recebida possui o HTTP Header `X-SAPRON-API-KEY`?
  * Se não, segue para o próximo middleware da cadeia;
  * Se sim, segue para o próximo passo.
* Faz o hash da API Key recebida;
* Verifica se o hash da API Key (`token_hash`) existe através da seguinte query:

  ```sql
  select auak.id
  from account_user_api_keys auak
  where auak.token = {token_hash} and auak.is_active and auak.expiration_date > now()
  ```
* A API Key existe?
  * Se não, responde a requisição com HTTP 401;
  * Se sim, segue para o próximo passo.
* Atualiza o campo `last_use_date` do registro encontrado (de forma atômica);
* Segue para o próximo middleware da cadeia.

## Gerenciamento de API Keys

Deve-se criar uma aplicação que gerencie as API Keys. Para tal, podemos utilizar o **Retool**.

> Idealmente, deve-se limitar o acesso à aplicação criada, bem como os endpoints utilizados.

A aplicação deve conter as seguintes funcionalidades:

* **Listagem de API Keys**:
  * Data de criação, data de atualização, usuário que criou, usuário quem personifica, está ativo, data de último uso e data de expiração;
* **Criação de API Key**:
  * Deve-se permitir a criação para um usuário já existente;
  * Deve-se permitir a criação para um usuário que ainda não existe (deve ser criado no mesmo fluxo);
  * Após criação, a API Key deve aparecer na tela uma única vez, informando ao usuário que a guarde com segurança.
* **Revogar/Restabelecer API Key**:
  * Mudar o valor de `is_active`;
* **Alterar data de expiração de API Key**:
  * Deve permitir valores vazios (sem prazo de expiração)

## Monitoramento

É de extrema importância que o uso das API Keys seja monitorado para que se tenha um controle e visibilidade do uso da API.

Para tal, é necessário que:

* Nos logs de request/response, deve-se adicionar a label `from_api_key=true|false` para que se tenha visibilidade do payload enviado/recebido pelas APIs;
* No grafana, exista um dashboards com:
  * RPM dos top K tokens em uso;
  * P90 dos endpoints em uso;
    * Será necessário criar novas métricas;
  * P50 dos endpoints em uso.
    * Será necessário criar novas métricas;

# Incrementos

## Rate limit por api key

TBD

## Escopo de uso

TBD