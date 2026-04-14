<!-- title: Dia 1 - GUIA | url: https://outline.seazone.com.br/doc/dia-1-guia-gDaYeHBCLq | area: Tecnologia -->

# Dia 1 - GUIA

* **Setup do ambiente**
  * **Linux**
    * **[Download Ubuntu - Site oficial](https://ubuntu.com/download/desktop)**
    * [Tutorial sobre ](https://www.youtube.com/watch?v=6D6L9Wml1oY)**[DUAL BOOT](https://www.youtube.com/watch?v=6D6L9Wml1oY)**
  * **Git**
    * **[Download GIT - Site oficial](https://git-scm.com/download/linux)**

    ```bash
    # Instalação do git no Ubuntu
    sudo apt-get install git
    
    # Configurações gerais do git
    git config --global user.email **example@gmail.com**
    git config --global user.name **username-example**
    git config --global core.editor **vscode**
    ```
  * **Docker e docker-compose**
    * **Docker**
      * **[Download Docker - Site oficial](https://docs.docker.com/desktop/linux/install/ubuntu/)**

      ```bash
      # Passo 1 - Guia rápido de instalação do Docker no Ubuntu
      
      1°. sudo apt-get update
      
      2°. sudo apt-get install  apt-transport-https  ca-certificates  curl  gnupg-agent software-properties-common
      
      3°. curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
      
      4°. sudo apt-key fingerprint 0EBFCD88
      
      5°. sudo add-apt-repository  "deb[arch=amd64]https://download.docker.com/linux/ubuntu  $(lsb_release -cs)  stable" (OBS: Se der erro rodar isso: sudo sed -i '52s/^/#/' /etc/apt/sources.list)
      
      6°. sudo apt-get update
      
      7°. sudo apt-get install docker-ce docker-ce-cli containerd.io
      
      ### NAO PRECISA RODAR O COMANDO ABAIXO, APENAS SE O **7°** COMANDO RETORNAR ERRO ###
      8°. sudo apt-get install docker-ce=5:18.09.1~3-0~ubuntu-xenial docker-ce-cli=5:18.09.1~3-0~ubuntu-xenial containerd.io
      
      #___#
      
      # Passo 2 - Configuração de superusuário
      1°. sudo groupadd docker
      2°. sudo usermod -aG docker $USER
      ```
    * **docker-compose**
      * **[Download docker-compose - Site oficial](https://docs.docker.com/compose/install/)**

      ```bash
      # Guia rápido de instalação do docker-compose no Ubuntu
      
      1°. sudo curl -L "https://github.com/docker/compose/releases/download/1.28.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
      
      2°. sudo chmod +x /usr/local/bin/docker-compose
      ```
  * **Make**

    ```bash
    # Instalação do make no Ubuntu
    sudo apt-get install make
    ```
  * **Editor de código**
    * **Instalação do** **vscode**
      * **[Download vscode - Site oficial](https://code.visualstudio.com/download)**
    * **Configurações do vscode**

      Abra o arquivos **settings.json:**

      1°. Tecle **CTRL + Shift + p**

      2°. Clique na opção ***Preferences: Open Settings (JSON)***

      ![Untitled](/api/attachments.redirect?id=4b5bfa6a-6939-41ad-81ec-444766d96839)

      3°. Copie o conteúdo do **JSON** abaixo e cole no lugar do conteúdo do ***settings.json*** do vscode:

      ```json
      {
          "workbench.iconTheme": "material-icon-theme",
          "workbench.startupEditor": "newUntitledFile",
          "workbench.editor.labelFormat": "short",
          "workbench.colorTheme": "Omni",
          
          "terminal.integrated.fontSize": 10,
          "terminal.integrated.shell.linux": "/bin/zsh",
          "terminal.integrated.rendererType": "canvas",
          "vsintellicode.modify.editor.suggestSelection": "automaticallyOverrodeDefaultValue",
          "[markdown]": {},
          "git.autofetch": true,
        
          // "editor.fontFamily": "'Fira Code",
          "editor.fontLigatures": true,
          "editor.fontSize": 12,
          "editor.lineHeight": 18,
          "editor.parameterHints.enabled": false,
          "editor.formatOnSave": false,
          "editor.rulers": [100,140],
          "editor.tabSize": 2,
          "editor.suggestSelection": "first",
          "editor.renderLineHighlight": "gutter",
          "editor.multiCursorModifier": "alt",
        
          "emmet.syntaxProfiles": {
              "javascript": "jsx",
          },
          "emmet.includeLanguages": {
              "javascript": "javascriptreact"
          },
          "javascript.suggest.autoImports": true,
          "javascript.updateImportsOnFileMove.enabled": "never",
          "typescript.suggest.autoImports": true,
          
          "breadcrumbs.enabled": true,
          
          "explorer.confirmDragAndDrop": false,
          "explorer.confirmDelete": false,
          
          "editor.codeActionsOnSave": {
            "source.fixAll.eslint": true,
            "source.fixAll.tslint": true,
            "source.fixAll.stylelint": true
          },
          "eslint.autoFixOnSave": true,
          "eslint.validate": [
              {
                  "language": "javascript",
                  "autoFix": true,
              },
              {
                  "language": "javascriptreact",
                  "autoFix": true,
              },
              {
                  "language": "typescript",
                  "autoFix": true,
              },
              {
                  "language": "typescriptreact",
                  "autoFix": true,
              },        
          ],
          "files.associations": {
          },
          "typescript.updateImportsOnFileMove.enabled": "always",
          "[javascript]": {
              "editor.defaultFormatter": "esbenp.prettier-vscode"
          },
          "[typescriptreact]": {
              "editor.defaultFormatter": "esbenp.prettier-vscode"
          }
        }
      ```
    * **Extensões do vscode**

      ![Untitled](/api/attachments.redirect?id=fbb00070-e60b-44c8-b08c-08ed22db093e)
  * **Customizações do** **terminal** (Opcional, mas recomendado para aumentar a produtividade no desenvolvimento das tasks)

    ```bash
    Guia rápido ATUALIZADO (2022):
    
    #instala o zsh
    sudo apt install zsh
    #reinicie o terminal
    
    #instala o ohmyzsh
    sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"
    #reinicie o terminal
    
    #instala a fonte FiraCode
    sudo apt install fonts-firacode
    
    #instala o spaceship
    git clone https://github.com/denysdovhan/spaceship-prompt.git "$ZSH_CUSTOM/themes/spaceship-prompt"
    
    ln -s "$ZSH_CUSTOM/themes/spaceship-prompt/spaceship.zsh-theme" "$ZSH_CUSTOM/themes/spaceship.zsh-theme"
    
    #configura o spaceship no .zshrc
    ZSH_THEME="spaceship"
    #reinicie o terminal
    
    #instala o zinit
    bash -c "$(curl --fail --show-error --silent --location https://raw.githubusercontent.com/zdharma-continuum/zinit/HEAD/scripts/install.sh)"
    #reinicie o terminal
    
    #usar esse comando
    zinit self-update
    
    # adicione no finaldo arquivo .zshrc
    # End of ZInit's installer chunk
    zinit light zdharma/fast-syntax-highlighting
    zinit light zsh-users/zsh-autosuggestions
    zinit light zsh-users/zsh-completions
    
    #reinicie o terminal
    ```

    [\*\*Tutorial Rocketseat - Terminal com Oh My Zsh, Spaceship, Dracula e mais](https://blog.rocketseat.com.br/terminal-com-oh-my-zsh-spaceship-dracula-e-mais/)\*\*

    **Link .zshrc:** <https://gist.github.com/diego3g/b0513d5ff6d9d983c48bed3fd8f10cdb>
* **Setup do projeto**
  * **Clonar repositório do Sapron do Github para o repositório local**
    * **Clonar via HTTPS**

      ```bash
      # Passo 1 - Abra o terminal em alguma pasta de sua preferência
      
      # Passo 2 - Rode o seguinte comando para clonar o repositório do Sapron
      git clone https://github.com/billbenettiSeazone/sapron-pms-web.git
      ```
      * **Comandos:**
    * **Clonar via SSH**

      > **OBS:** para clonar o projeto via SSH é preciso **[configurar as chaves SSH](https://docs.github.com/pt/authentication/connecting-to-github-with-ssh/adding-a-new-ssh-key-to-your-github-account)** no seu computador e adicionar a chave pública no Github.

      **Referências:** **[Clonar URLs de SSH](https://docs.github.com/pt/get-started/getting-started-with-git/about-remote-repositories#cloning-with-ssh-urls)** | **[Adicionar uma nova chave SSH à sua conta do GitHub](https://docs.github.com/pt/authentication/connecting-to-github-with-ssh/adding-a-new-ssh-key-to-your-github-account)**

      ```bash
      # Passo 1 - Abra o terminal em alguma pasta de sua preferência
      
      # Passo 2 - Rode o seguinte comando para clonar o repositório do Sapron
      git clone git@github.com:billbenettiSeazone/sapron-pms-web.git
      ```
  * **Definir variáveis ambiente (database, backend e frontend)**

    \*\*\* Obs:\*\* Algumas variáveis de ambiente estão com valores que não são reais pois estes não podem ser expostos no repositório remoto. Para utilizar algumas funcionalidades, como popular o banco de dados local, será necessário falar com algum administrador do projeto para que os dados reais sejam fornecidos.
  * **Executar o projeto**

    ```bash
    # Passo 1 - Comando para upar todos os containers do projeto
    sudo make setup
    
    # Passo 2 - Clonar o bd local com o bd da produção
    Seguir o passo a passo de 1 a 5:
    ```

    ![Untitled](/api/attachments.redirect?id=654b3835-56ae-4575-8792-428bd9df36a4)
    * Se tudo funcionou corretamente ao executar os comandos descritos nos Passos 1 e 2, já é possível acessar o [\*\*servidor do frontend do Sapron](http://localhost:3000/)\*\* em ambiente de desenvolvimento
  * **React DevTools**

    **[Download Extensão React Developer Tools - Google Chrome](https://chrome.google.com/webstore/detail/react-developer-tools/fmkadmapgofadopljbjfkapdkoienihi)**