<!-- title: Workflow Reservas/Wallet | url: https://outline.seazone.com.br/doc/workflow-reservaswallet-MN0d1hX38Z | area: Tecnologia -->

# Workflow Reservas/Wallet

## Visão Geral

Este documento descreve o fluxo de trabalho para o gerenciamento de releases e implantação de aplicações utilizando um repositório normal (desenvolvimento) e um repositório GitOps.


 ![](/api/attachments.redirect?id=13c26fea-8c71-40b6-be8b-0ccf81dde44c)

## 1. Fluxo de Desenvolvimento

### 1.1 Commit na Branch de Desenvolvimento

* Desenvolvedores realizam commits em uma branch secundária (x/branch).
* As alterações são mescladas na branch develop.

### 1.2 Geração de Nova Release - Release Candidate (RC)

* Um arquivo semantic-version.yaml é atualizado para refletir a nova versão de release candidate (x.x.x-rc).
* O arquivo ci-staging.yaml é acionado para iniciar o build e disparar o fluxo do GitOps.

### 1.3 Atualização do Repositório GitOps

* Um workflow no GitOps é acionado através de repo-dispatch.yaml.
* Este workflow atualiza o arquivo values-staging.yaml com a nova versão.

### 1.4 Deploy no Cluster de Staging

* Um workflow deploy-stg.yaml é acionado para implantar a nova versão no cluster de staging.


---

## 2. Fluxo de Produção

### 2.1 Commit na Branch main

* Após a validação em develop, as alterações são mescladas na branch main.

### 2.2 Geração de Nova Release

* O arquivo semantic-version.yaml é atualizado para a nova versão oficial (x.x.x).
* O arquivo ci-main.yaml é acionado para iniciar o build e disparar o fluxo do GitOps.

### 2.3 Atualização do Repositório GitOps

* O workflow repo-dispatch.yaml é acionado para atualizar o arquivo values.yaml.

### 2.4 Deploy no Cluster de Produção

* Um workflow deploy.yaml é acionado para implantar a nova versão no cluster de produção.


---

## 3 - Considerações Finais

* O uso de GitOps garante que todas as alterações sejam refletidas automaticamente nos ambientes desejados.
* A utilização de semantic-version.yaml permite um controle de versão semântico eficiente.
* Este processo garante um fluxo seguro e automatizado para publicação de releases em staging e produção.