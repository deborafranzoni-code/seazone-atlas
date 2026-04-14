<!-- title: Actions | url: https://outline.seazone.com.br/doc/actions-HKAngRvdPF | area: Tecnologia -->

# Actions

## Action Semantic Version

Ação para marcar commits automaticamente seguindo o Versionamento Semântico.

> Commits que contêm #patch, #minor ou #major no campo de mensagem acionarão o incremento correspondente da versão.

## Recursos

* **Versionamento Automatizado**: Garante um versionamento consistente baseado nas mensagens de commit.
* **Controle Específico por Branch**: Permite definir diferentes comportamentos de versionamento por branch.

## Melhorias

* **Padrão dos time**: O action apresenta o seu funcionamento próprio e difere de alguns casos como o do reservas que cria as versões de staging como pré-release. Poder se adaptar para casos como estes será importante para o funcionamento futuro do semantic version. (Isso porque atualmente não contamos com um padrão interno)

## Entradas

### branch

**Opcional** Especifica o tipo de branch usado para criar uma nova versão.

Valores possíveis:

* staging
* stage
* main
* master
* hotfix/\*
* develop

Se não for definido, a ação aplicará um incremento genérico de versão.

## Saídas

### version

A nova versão gerada.

## Requisitos

* Um repositório válido no GitHub com permissões de escrita para criar tags.
* GITHUB_TOKEN deve ser fornecido como um segredo para autenticar a marcação.
* As mensagens de commit devem conter #patch, #minor ou #major para acionar os incrementos de versão.

## Exemplo de Uso

```javascript
- name: Incrementar versão e criar tag
  id: gen-version
  uses: seazone/governanca-actions-semver@main
  env:
    GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
    REPO_OWNER: seazone
  with:
    branch: 'develop'
```

## Solução de Problemas

* Certifique-se de que o repositório tem as permissões corretas para criar tags.
* Verifique se as mensagens de commit contêm as palavras-chave corretas para versionamento.
* Confira os logs do GitHub Actions para erros de autenticação ou no fluxo de trabalho.


---

# Action Systems Manager

Action para importar as variáveis de ambiente do systems manager.

> A actions utiliza o aws-env-params para importar as variáveis e armezena elas em um arquivo .env no diretório da aplicação.

## Recursos

* **Build de clients**: Permite o build atualizado de clietes, uma vez que essas aplicações precisam das variáveis

## Melhorias

* **Automatizar Build**: A cada alteração de variável, é necessário rebuildar e refazer o deploy. O ideial seria um processo onde a alteração da variável fosse incluída direto no cluster, sem necessidade de interação do usuário ou github actions.

## Inputs

### `repository`

**Necessário**  Nome do repositório que representa o prefixo das variáveis que serão importadas

### `account_region`

**Necessário**  Nome da região da aws que o repositório está localizado.

### `account_id`

**Necessário**  Nome da conta da aws que o repositório está localizado.

### `deployment_role`

**Necessário**  Nome da role que será utilizado pela actions.

## Outputs

### `Variáveis de Ambiente`

Variáveis de Ambiente do repositório em um arquivo .env

## Requisitos

* Um repositório válido no GitHub com permissões de escrita para criar tags.
* GITHUB_TOKEN deve ser fornecido como um segredo para autenticar a marcação.

## Example Usage

```yaml
  - name: Get Envs From Ssm
    uses: seazone-tech/governanca-actions-ssm@main
    with:
      repository: ${{ env.APP_NAME }}
      account_region: ${{ secrets.account_region }}
      account_id: ${{ secrets.account_id }}
      deployment_role: ${{ secrets.deployment_role }}
```

## Troubleshooting

* Ensure the repository has the correct permissions to push tags.
* Verify commit messages contain the correct versioning keywords.
* Check GitHub Actions logs for authentication or workflow errors.


---


# Action Cluster Deploy

Action para interagir com o cluster a partir do github actions

> Futuramente esta action pode ser utilizada para interagir com o cluster de alguma outra forma. 

## Recursos

* **Deploy**: Permite fazer o deploy do helm da aplicação
* Reboot: Permite realizar o reboot caso o pod esteja travado

## Melhorias

* **ArgoCD**: Não há a necessidade de melhorar o processo em questão a substituação dele pelo argocd irá tratar muitos casos de erros que podemos ter e que não são interessantes para o desenvolvimento interno.

## Inputs

### `environment`

**Necessário**  Nome do ambiente que o deploy/reboot será realizado

### `app_name`

**Necessário**  Nome do serviço que a action irá interagir.

### `action`

**Necessário** Especifica a ação que será realizada pela action.

Valores possíveis:

* reboot
* deploy

### `account_region`

**Necessário**  Nome da região da aws que o repositório está localizado.

### `account_id`

**Necessário**  Nome da conta da aws que o repositório está localizado.

### `deployment_role`

**Necessário**  Nome da role que será utilizado pela actions.

## Outputs

### `Variáveis de Ambiente`

Variáveis de Ambiente do repositório em um arquivo .env

## Requisitos

* Um repositório válido no GitHub com permissões de escrita para criar tags.
* GITHUB_TOKEN deve ser fornecido como um segredo para autenticar a marcação.

## Example Usage

```yaml
  uses: seazone-tech/governanca-workflows-template/.github/workflows/app-deploy-helm.yaml@main
  with:
    environment: 'production'
    app_name: 'reservas'
    action: 'deploy'
  secrets:
    account_region: ${{ secrets.AWS_PRODUCTION_ACCOUNT_REGION }}
    account_id: ${{ secrets.AWS_PRODUCTION_ACCOUNT_ID }}
    deployment_role: ${{ secrets.AWS_PRODUCTION_DEPLOYMENT_ROLE }}
```

## Troubleshooting

* Ensure the repository has the correct permissions to push tags.
* Verify commit messages contain the correct versioning keywords.
* Check GitHub Actions logs for authentication or workflow errors.