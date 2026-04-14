<!-- title: Novo fluxo de Deploy | url: https://outline.seazone.com.br/doc/novo-fluxo-de-deploy-JftJ2XDP9c | area: Tecnologia -->

# Novo fluxo de Deploy

# Estrutura

Com o novo fluxo de deploy, teremos a seguinte estrutura de branches:

* `staging`: ativa o deploy para staging
* `develop`: branch base
* `main`: ativa o deploy para produção

# Etapas

→ Desenvolver código e testar localmente;

→ Enviar código para a Staging:

Rodar locamente os seguintes comandos (esses comandos devem ser rodados ***sempre*** que algo novo for enviado para Staging:

* `git branch -D staging`: apaga branch de staging local
* `git fetch origin staging`: busca branch de staging atualizada
* `git checkout staging` : troca para a branch staging
* `git merge {nome-da-sua-branch}`: faz o merge com a branch desenvolvida
* `git commit {nome-do-commit}`: faz o commit para a staging
* `git push -f`: atualiza a branch staging no repositório remoto (Github)

*OBS*: é possível rodar os 3 primeiros comandos juntos: `git branch -D staging && git fetch origin staging && git checkout staging`

→ Abrir PR do ambiente local para a branch `develop`

* Fazer review do código;
* Fazer o merge quando estiver aprovado e pronto para ir para produção.

→ Enviar código para Producão:

* Abrir PR da branch `develop` para a branch `main`;
* Aprovar PR.

# Fluxograma

# Fluxograma

 ![novo-fluxo-deploy.jpg](/api/attachments.redirect?id=6520ab37-1506-4fcb-92f4-d5524aea4e74)