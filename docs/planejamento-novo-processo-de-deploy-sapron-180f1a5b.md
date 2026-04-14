<!-- title: Planejamento Novo Processo de Deploy Sapron | url: https://outline.seazone.com.br/doc/planejamento-novo-processo-de-deploy-sapron-WxhrqTntEA | area: Tecnologia -->

# Planejamento Novo Processo de Deploy Sapron

## O que buscamos resolver?


---

Como podemos melhorar e automatizar o processo de deploy para que qualquer pessoa consiga realizar?

## Como?


---

* Método 1

  **1.** Altera o manifest.json manualmente e commita na `develop`;

  **2.** Fazer o merge da branch de `develop` → `staging` ao gerar uma **Pre-release;** Starta Workflow de Staging

  **3.** Fazer o merge da branch de `staging` → `production` ao gerar um **Release.** Starta Workflow de Production

  
---

  **Desvantagem:** manifest.json precisará ser alterado manualmente

  **Vantagem:** Quase todo processo é automatizado, basta apenas alterar o manifest.json e depois gerar as tags de releases.

  
---
  * Implementação

    
---

    Here's a possible implementation:

    
    1. Create your `develop`, `staging`, and `production` branches.
    2. Set up branch protections for `staging` and `production` to require pull requests for changes and require reviews before merging.
    3. Set up a GitHub Action that listens for pre-release creation and merges `develop` into `staging`. The action should be triggered when a new tag is created and checks if the tag is a pre-release (`if: startsWith(github.ref, 'refs/tags/v') && contains(github.ref, '-pre.')`). If it is, the action can run a script that checks out the `staging` branch, pulls in the latest `develop` changes (`git pull origin develop`), and commits the changes. This script should then push the changes to the `staging` branch (`git push origin staging`).
    4. Set up another GitHub Action that listens for release creation and merges `staging` into `production`. This action should be triggered when a new tag is created and checks if the tag is a release (`if: startsWith(github.ref, 'refs/tags/v') && !contains(github.ref, '-pre.')`). If it is, the action can run a script that checks out the `production` branch, pulls in the latest `staging` changes (`git pull origin staging`), and commits the changes. This script should then push the changes to the `production` branch (`git push origin production`).
    * Here's an example workflow file for the first action

      ```yaml
      name: Merge develop into staging on pre-release
      
      on:
        create:
          tags:
            - 'v*-pre.*'
      
      jobs:
        merge-develop-into-staging:
          runs-on: ubuntu-latest
          steps:
            - name: Checkout code
              uses: actions/checkout@v2
            - name: Merge develop into staging
              run: |
                git config user.name "Your Name"
                git config user.email "your-email@example.com"
                git checkout staging
                git pull origin develop
                git push origin staging
      ```
    * And here's an example workflow file for the second action

      ```yaml
      name: Merge staging into production on release
      
      on:
        create:
          tags:
            - 'v*'
      
      jobs:
        merge-staging-into-production:
          runs-on: ubuntu-latest
          steps:
            - name: Checkout code
              uses: actions/checkout@v2
            - name: Merge staging into production
              run: |
                git config user.name "Your Name"
                git config user.email "your-email@example.com"
                git checkout production
                git pull origin staging
                git push origin production
      ```

    Make sure to adjust the branch names and email/name configuration to match your setup. Also, keep in mind that automatic merges can have risks, so it's important to test and verify the changes before releasing to production.
* Método 2

  **1.** Ao gerar uma **Pre-release:** Altera o manifest.json manualmente e commita na `develop`;

  **1.1.** Faz o merge da branch de `develop` → `staging`**;** Starta Workflow de Staging

  **2.** Ao gerar um **Release:** Faz o merge da branch de `staging` → `production`**.** Starta Workflow de Production

  
---

  **Desvantagem:** O nome da tag gerada vai para o manifest.json (geralmente pre-release carre o sufixo "`-pre`". **v2.3.4-pre**

  **Vantagem:** Todo processo é automatizado, basta apenas gerar as tags de releases

  
---
  * Implementação

    
---

    To automatically update the version in a `manifest.json` file when creating a new release on GitHub, you can use a GitHub Action. The following steps will guide you through the process:

    
    1. Create a new GitHub Action that listens for release creation events. You can use the `on` keyword to specify the event trigger:
       * **code**

         ```yaml
         on:
           release:
             types: [created]
         ```
    2. Set up the `jobs` section of the workflow file to check out the code, update the version in the `manifest.json` file, commit the changes, and push the changes back to the repository. Here's an example script that uses `jq` to update the `version` field:
       * **code**

         ```yaml
         jobs:
           update-manifest-version:
             runs-on: ubuntu-latest
             steps:
             - name: Checkout code
               uses: actions/checkout@v2
             - name: Update version
               run: |
                 NEW_VERSION=$(echo "${{ github.ref }}" | sed 's/refs\/tags\/v//')
                 jq ".version = \"${NEW_VERSION}\"" manifest.json > manifest.json.tmp
                 mv manifest.json.tmp manifest.json
             - name: Commit changes
               run: |
                 git config user.name "Your Name"
                 git config user.email "your-email@example.com"
                 git commit -a -m "Update manifest version to ${NEW_VERSION}"
             - name: Push changes
               uses: ad-m/github-push-action@v0.6.0
               with:
                 github_token: ${{ secrets.GITHUB_TOKEN }}
                 branch: ${{ github.ref }}
         ```

       In this example, the `NEW_VERSION` variable is set to the version number specified in the tag that triggered the release. The `jq` command updates the `version` field in the `manifest.json` file with the new version number. The changes are then committed to the repository with a commit message that includes the new version number. Finally, the changes are pushed back to the branch that triggered the release using the `ad-m/github-push-action` GitHub Action.

       Make sure to adjust the `manifest.json` file path and the email/name configuration to match your setup. Also, keep in mind that this approach assumes that the `version` field in the `manifest.json` file is a string and not an object or an array. If your `version` field is not a string, you will need to modify the `jq` command accordingly.

### **Desenho da solução**

> [Link do desenho no Lucid](https://lucid.app/lucidchart/cf25a6ec-6e67-46f2-a1d4-3d77cd36ee33/edit?invitationId=inv_f5334fba-c490-4202-982b-bdfd534aedb0&page=CF9xNFGUbTwT#)

* **Método 1**

  ![Mural do Sapron - Deploy.png](/api/attachments.redirect?id=72d49b66-e173-415a-99da-fc7475c3d324)
* **Método 2**

  ![Mural do Sapron - Deploy (1).png](Planejamento%20Novo%20Processo%20de%20Deploy%20Sapron%20d11e288fb1b94bc8a12ccaef1ae7ef30/Mural_do_Sapron_-_Deploy_(1).png)