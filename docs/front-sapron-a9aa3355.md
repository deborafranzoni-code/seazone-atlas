<!-- title: [FRONT] Sapron | url: https://outline.seazone.com.br/doc/front-sapron-09uWytOKsU | area: Tecnologia -->

# [FRONT] Sapron

**Pré-requisitos:**

> * Linux/WSL (desejável, mas não obrigatório)
> * Node 16+
> * Docker 
> * Docker Compose


1. Clone o repositório

   ```bash
   git clone https://github.com/seazone-tech/sapron-frontend.git
   
   ou
   
   git clone git@github.com:seazone-tech/sapron-frontend.git
   ```

   \
2. Crie um arquivo `.env` dentro de `/app`

   
:::info
   Esse arquivo contém as variáveis de ambiente necessárias para rodar o projeto. Basta pedir para qualquer dev encaminhar o arquivo atual.

   :::

   \
3. Inicie o servidor de desenvolvimento

   ```bash
   docker compose up front
   ```

   \
4. Acesse o servidor de desenvolvimento

   ```bash
   http://localhost:3000
   ```

   \
5. A tela esperada deve ser:

   ![](/api/attachments.redirect?id=b15e560c-9549-4bf7-8954-e110c8f4ffbd " =1509x778")

   
:::success
   Finalizamos por aqui **✅**

   :::