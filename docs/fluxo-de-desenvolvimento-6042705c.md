<!-- title: Fluxo de desenvolvimento | url: https://outline.seazone.com.br/doc/fluxo-de-desenvolvimento-7guAwmIGtr | area: Tecnologia -->

# Fluxo de desenvolvimento

# TL;DR

Esta RFC tem como objetivo propor um novo fluxo de desenvolvimento que mitigue o bloqueio de deploy em produção por conta de features não preparadas para produção (production-ready).

# Problema atual

Temos diversos repositórios com diversas alterações sendo realizadas diariamente. Conforme as alterações são aprovadas pelo QA e PM, elas precisam ser integradas em produção para que agreguem valor ao cliente.

Os seguintes passos são executados para integrar alterações ao produto (em seguida, uma imagem descrevendo visualmente os passos abaixo):

* Bob (desenvolvedor) cria uma nova branch (`nova-branch`, por exemplo) a partir da `staging` (ou `develop`);
* Bob commita as alterações necessárias em `nova-branch`;
* Bob faz o merge de `nova-branch` em `staging` (ou `develop`);
* Bob informa ao QA/PM que as alterações estão prontas para validação;
* Após aprovação do QA/PM, Bob integra suas alterações em produção fazendo o merge de `staging` (ou `develop`) em `main`.

 ![Fluxo atual de desenvolvimento](/api/attachments.redirect?id=a3a42081-fd64-429e-afce-dc307326c87b " =798x480")

Neste fluxo, acontece casos em que uma funcionalidade X, que foi aprovada, é impedida de ser integrada em produção por conta de uma refatoração Y que altera um fluxo sensível e ainda não foi aprovada. Integrar X em produção significa também integrar Y com o risco de quebrar um fluxo crítico dos clientes. Dessa forma, a entrega da funcionalidade X é atrasada por conta de alterações alheias, fato que não deve acontecer.

## Solução atual

De forma a mitigar o problema descrito, utilizamos feature flags que habilitam/desabilitam as alterações. Isso permite que ambas alterações X e Y possam ser integradas em produção, mas que Y não esteja disponível até que a aprovação seja feita.

Contudo, o uso de feature flags não é uma solução escalável: é necessário integrá-las em cada feature, além de ser necessário construir o código com lógica condicional baseado na feature flag. Após validação, a feature flag deve ser removida.

# Proposta de nova solução

Como solução, podemos seguir o fluxo de desenvolvimento descrito abaixo (e mostrado visualmente em imagem):

* Bob (desenvolvedor) cria uma nova branch (`nova-branch`, por exemplo) a partir da `main`;
* Bob commita as alterações necessárias em `nova-branch`;
* Bob faz o merge de `nova-branch` em `staging` (ou `develop`);
* Bob informa ao QA/PM que as alterações estão prontas para validação;
* Após aprovação do QA/PM, Bob integra suas alterações em produção fazendo o merge de `nova-branch` em `main`;
* Após o merge em `main`, Bob faz o merge da `main` em `staging` (ou `develop`), sincronizando commits de merge/squash-and-merge.

 ![Proposta de nova solução](/api/attachments.redirect?id=16a0be61-3ee1-4b66-9f20-b532269a6124 " =798x465")

Com esse fluxo de desenvolvimento, garantimos que código não aprovado só seja integrado em produção quando estiver aprovado, além de não bloquear a integração de alterações alheias.

Contudo, introduz novas características que devem ser entendidas e integradas no cotidiano.

## Branch com alterações deve existir até o merge com a main

O propósito da solução é segregar as alterações em branches individuais. Com isso, elas podem ser integradas individualmente nos diversos ambientes.

Portanto, é de extrema importância que a branch não seja apagada até que as alterações sejam integradas em produção. Caso contrário, serão perdidas.

## Resolução de conflitos

Com essa solução, a ocorrência de conflitos de código quando integrados em `staging`/`develop` tende a aumentar. O motivo é simples: sua branch não possui as mudanças contidas nessas branches (e não deve ter).

É extremamente importante que a sua branch contenha **APENAS** as suas alterações com base no código que está em produção (`main`). Caso contrário, a solução proposta falha.

Dessa forma, a resolução de conflitos deve ser feita em uma **branch de merge** (merge-branch), mantendo a branch original "limpa", ou seja, apenas com as mudanças que serão integradas em produção. O objetivo dessa branch é apenas resolver os conflitos de suas alterações com `staging`/`develop` e integrá-las no ambiente. Após a integração, a branch pode ser excluída.

Note que a branch de merge é apenas necessária quando for integrada em `staging`/`develop`. Se, ao integrar em produção (`main`) existir conflitos, deverão ser resolvidos na própria branch, garantindo que você está atuando em cima das mudanças mais recentes de produção e evitando conflitos desnecessários.

Em suma:

* Bob (desenvolvedor) faz diversas alterações em uma branch (`nova-branch`);
* Ao tentar fazer o merge de `nova-branch` em `staging` (ou `develop`), o Git informa que existem conflitos que devem ser resolvidos;
* Bob cria uma branch de merge (`merge-staging-nova-branch`) a partir de `nova-branch`;
* Bob faz o merge de `staging` (ou `develop`) na branch `merge-staging-nova-branch`, resolvendo os conflitos;
* Após resolução dos conflitos, Bob faz o merge da branch `merge-staging-nova-branch` em `staging` (ou `develop`);
* Ao tentar fazer o merge de `nova-branch` em `main`, o Git informa que existem conflitos que devem ser resolvidos;
* Bob faz o merge de `main` na branch `nova-branch`, resolvendo os conflitos;

 ![Resolução de conflitos](/api/attachments.redirect?id=dec8d25d-6f10-4c47-8ee4-af6292e54167 " =710x297")


## Constante atualização das branches com a main

Para que se atue em cima das alterações mais recentes de produção, é necessário que todas as branches estejam sincronizadas com a `main`. Isso se refere tanto às mudanças de código quanto ao histórico de commits.

Portanto, após fazer o merge das suas alterações em produção, é preciso sincronizar a `main` com `staging`/`develop` para que o histórico de commits seja o mesmo entre os ambientes. Isso evita a resolução de conflitos que já foram resolvidos, mas que o Git indica que ainda não foram por conta de divergência no histórico de commits.

# Problemas das migrações do Django

…

## Propostas de solução

### Solução 1

### Solução 2

### Solução 3