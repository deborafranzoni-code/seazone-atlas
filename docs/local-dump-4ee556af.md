<!-- title: Local (dump) | url: https://outline.seazone.com.br/doc/local-dump-dUbZ6a3vdN | area: Tecnologia -->

# Local (dump)

**Pré-requisitos:**

> * Linux/WSL (desejável, mas não obrigatório)
> * **[Docker ↗️](https://docs.docker.com/get-docker/)**
> * **[Docker Compose ↗️](https://docs.docker.com/compose/install/)**
> * Configuração do banco de **staging** feita e aceitando conexões (@[STG/PRD](mention://6b49dfe3-8f52-4f59-9f79-b3abf0199d1d/document/86b7a2f3-2e2b-4e49-8f44-36f73a12507a))

Essa seção descreve como gerar um **dump local do banco de staging**, para uso em desenvolvimento e testes. O processo é simples e garante que você trabalhe com uma base atualizada, sem afetar dados reais.


---

## ⚙️ Setup


1. **Execute o script do banco de staging**

   Antes de tudo, rode o script do banco de staging, alterando a variável `LOCAL_PORT` para **uma porta diferente de 5432** (por exemplo, 5433).

   ```bash
   ./script.sh
   ```

Isso garante que o túnel para o banco remoto fique ativo sem conflitar com o banco local.


---


2. **Crie o script de dump**

   Na raiz do projeto, crie um novo arquivo chamado `dump_sapron.sh` (ou o nome que preferir) e cole o conteúdo abaixo:

   \
   [dump_sapron.sh 1377](/api/attachments.redirect?id=947b75d1-1a7a-4904-a391-c67e6d11e738)

   \
   > 💡 Esse script é responsável por gerar o dump completo do banco remoto e salvá-lo em um arquivo `.sql` local.


---


3. **Dê permissão de execução ao script**

   ```bash
   chmod +x dump_sapron.sh
   ```


---


4. **Execute o script**

   ```bash
   ./dump_sapron.sh
   ```

   
:::info
   Em algum momento, o sistema pode solicitar sua senha de usuário — fique atento e digite-a quando solicitado.

   :::

   Agora é só aguardar o dump finalizar. O processo pode levar alguns minutos, dependendo da sua conexão de rede.

   
:::info
   Caso seja necessário, rode o `./dump_sapron.sh` pelo WSL e se der erro, execute o comando `sudo apt install postgresql-client ``[docker.io](http://docker.io)`` pv` 

   :::


---


5. **Suba o banco local**

   Após o dump ser concluído, rode o comando abaixo para inicializar o container do banco local:

   ```bash
   docker compose up sapron_db
   ```


---


6. **Conecte-se com um cliente SQL (DBeaver / Beekeeper / etc.)**

   Quando o container estiver em execução, configure seu cliente de banco com as credenciais abaixo:

   ```
   PORT=5432
   HOST=localhost
   DB_NAME=seazone
   USER=seazone
   PASSWORD=seazone
   ```

   
:::tip
   Após conectar, você já poderá explorar o banco local restaurado e trabalhar normalmente com os dados do ambiente de staging.

   :::


---


:::success
Finalizamos por aqui

:::