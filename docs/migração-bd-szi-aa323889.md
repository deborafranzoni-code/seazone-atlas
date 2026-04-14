<!-- title: Migração BD SZI | url: https://outline.seazone.com.br/doc/migracao-bd-szi-JBQ4Y7Kk3R | area: Tecnologia -->

# Migração BD SZI

# TL;DR

Migrar os dados do BD SZI (MySQL, GCP) para o BD Sapron (PostgreSQL, AWS).

# Objetivo

Unificar a base de dados para centralizar custos e tecnologia.

# Etapas da migração

## Criação das tabelas no BD Sapron

Para organização em domínios, devemos criar um novo schema `szi` dentro do BD Sapron. As tabelas encontram-se [neste link](https://lucid.app/lucidchart/0f999830-7d9d-4c31-aec5-10fec791f65a/edit?invitationId=inv_e21b8c78-09ca-4142-a01e-2422591f521e&page=0_0#) (login no Lucid; para acesso, solicitar a @[Francisco Oliveira da Silva Filho](mention://2fa9ed3f-fbe1-4333-90b0-c9eb4276ad59/user/ed358268-7f1e-4490-9fff-b0aa608d820b)).

Abaixo, segue o diagrama das tabelas que serão migradas (verde) em conjunto com as tabelas existentes (cinza):

 ![Imagem 1 - Tabelas SZI](/api/attachments.redirect?id=a9cf0fad-1fa1-4be3-9444-aa9920137263 " =5831x3672")


\

\
### Nova role `Investidor`

De forma a adequar a tabela `investidores` para o BD Sapron, devemos criar a tabela `account_investor` que referencia a tabela `account_user`. Com isso, uma nova role `Investidor` será criada.

 ![](/api/attachments.redirect?id=d1d67745-66ff-48f8-bd4c-34ebb9f52b34 " =1064x827")


## Fluxo de sincronização de SPOT deve consultar BD Sapron

Na atualização de um deal no funil de comercialização de SPOT no pipedrive, a unidade em questão tem seu status atualizado dependendo de qual estágio do funil ela se encontra.

Devemos ajustar esse fluxo de tal forma que as leituras/escritas sejam feitas nas tabelas armazenadas no BD Sapron, e não mais no BD SZI. Para tal, deve-se utilizar uma feature flag que faça o *switch* entre a escrita/leitura do BD Sapron e SZI.

A feature flag só poderá ser ligada (escrita/leitura no BD Sapron) quando o dump do BD for feito.

## Dump do BD

Deve-se migrar todos os dados hoje contidos no BD SZI para o BD Sapron. Um script deve ser feito para tal, uma vez que o nome das tabelas e colunas são divergentes.

Após o dump ser concluído com sucesso, deve-se ligar a feature flag que permite a escrita/leitura no BD Sapron.