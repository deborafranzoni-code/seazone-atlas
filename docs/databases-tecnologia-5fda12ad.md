<!-- title: Databases Tecnologia | url: https://outline.seazone.com.br/doc/databases-tecnologia-zQEgVyU9x0 | area: Tecnologia -->

# Databases Tecnologia

Página destinada a organizar o modelo de permissionamento as tabelas dos bancos de tecnologia 

## O que cada permissão faz ? 

descrição breve das permissões que podemos aplicar nas tabelas 

| Permissão | O que faz  |
|----|----|
| SELECT | Ler dados da tabela (consultas |
| INSERT | Adicionar dados (novas linhas) |
| UPDATE | Modificar dados existentes |
| DELETE | Excluir dados da tabela |
| TRUNCATE | Excluir todos os dados da tabela rapidamente (sem gerar logs) |
| REFERENCES | Criar referências (chaves estrangeiras) a essa tabela |
| TRIGGER | Criar ou modificar gatilhos (ações automáticas) na tabela |

## Bancos de Web 

Padrão de permissões a ser seguido tabelas de bancos da parte de web 

| Role | Permissões nas tableas  | Permissões no schema |
|----|----|----|
| DBA | `SELECT, INSERT, UPDATE, DELETE, TRUNCATE, REFERENCES,TRIGGER` | `USAGE,CREATE` |
| Quality Assurance | `SELECT, INSERT, UPDATE, DELETE ` | `USAGE` |
| Tech Lead (supervisor) | `SELECT, INSERT, UPDATE, DELETE, REFERENCES, TRIGGER ` | `USAGE,CREATE` |
| Frontend | `SELECT` | `USAGE` |
| Backend | `SELECT, INSERT, UPDATE, REFERENCES`, `DELETE` | `USAGE` |
| Infra (SRE,Devops) | `SELECT` | `USAGE` |
| Applications | `SELECT, INSERT, UPDATE, DELETE ` | `USAGE` |


## Aplicações

Conforme mencionado anteriormente, criamos uma role chamada `applications`, destinada a ser utilizada por aplicações e serviços que necessitem de acesso aos bancos de dados. É importante destacar que essa role não deve conter login e senha. Em vez disso, deve-se criar um usuário com o nome da aplicação correspondente (`wallet_service`, por exemplo), e esse usuário herdará as permissões da role `applications`.Credenciais de aplicações devem ser mantidas no vault e não devem ser utilizadas para acesso individual 

## Bancos de tools

Padrão de permissões a ser seguido em bancos de ferramentas gerenciadas pelo time de infra  

| Role | Permissões |
|----|----|
| SRE/ Devops | `SELECT, INSERT, UPDATE, DELETE, TRUNCATE, REFERENCES,TRIGGER` |


## Usuários e papéis

| Usuário | Role |
|----|----|
| lucas_malagoli | back_end_dev |
| bruno_campos | back_end_dev |
| patrick_moreira | front_end_dev |
| isabel_karina | quality_assurance |
| fabio_harada | back_end_dev |
| roberto_campos | tech_lead |
| kaylan_argollo | front_end_dev |
| wallet_service | applications |
| felipe_ribeiro | back_end_dev |
| matheus_antunes | front_end_dev |
| karol_wojtyla | front_end_dev |
| carlos_cezar | front_end_dev |
| alysson_alcantara | front_end_dev |
| marcos_paulo | front_end_dev |
| bernardo_antonio | back_end_dev |
| maria_fernanda | back_end_dev |
| adama_sene | dba |