<!-- title: STG/PRD | url: https://outline.seazone.com.br/doc/stgprd-V4aWZEnZEb | area: Tecnologia -->

# STG/PRD

**Pré-requisitos:**

> * Linux/WSL (desejável, mas não obrigatório)
> * **[Kubectl ↗️](https://kubernetes.io/docs/tasks/tools/install-kubectl-linux/)**
> * [AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html)
> * Acessos garantidos à AWS (@[Permissões](mention://6867f973-1af4-4523-b4ed-9f38278925b3/document/391621f5-9ada-471e-9530-ceff794bb7ae) )
> * Credenciais pessoais criadas em stg e prd (@[Permissões](mention://f5c587bc-67fc-4ffb-9b4d-a488cc552b8d/document/391621f5-9ada-471e-9530-ceff794bb7ae) )

O setup do banco de staging ou produção, atualmente, funciona através de um RDS Bastion, que, basicamente sobe um pod local que se conecta 

## 🎥 Vídeo de apoio (não oficial, mas funcional)

[https://drive.google.com/file/d/1Ys5prJvcKVHAwrVJ4OyTEilT2emdpmm-/view?usp=drivesdk](https://drive.google.com/file/d/1Ys5prJvcKVHAwrVJ4OyTEilT2emdpmm-/view?usp=drivesdk)

## ⚙️ Setup


1. **Configure o SSO da AWS**

   No terminal, execute:

   ```bash
   aws configure sso
   ```

   Em seguida, preencha o diálogo conforme abaixo:

   ```
   SSO session name (Recommended): default  
   SSO start URL (None): https://d-926761dadf.awsapps.com/start/#  
   SSO region (None): us-west-2  
   SSO registration scopes [sso:account:access]: [pressione Enter]
   ```

   Será exibido um link no terminal, algo como:

   ```
   https://oidc.us-west-2.amazonaws.com/authorize?...
   ```

   Se não abrir automaticamente, clique no link — ele abrirá o login **OIDC da AWS**.

   > 🪟 Ao aparecer o popup, clique em **"Allow Access"**.
   >
   > ![](/api/attachments.redirect?id=f2e72bc9-1406-46ae-8029-e311adf75f23 " =1007x521")
   >
   > Depois disso, feche a janela e volte ao terminal.

   No terminal, selecione a conta:

   ```
   Applications (aws-production@seazone.com.br)
   ```
2. \
3. E, em seguida, preencha o segundo diálogo:

   ```
   Default client Region [None]: us-west-1  
   CLI default output format [None]: json  
   Profile name: default
   ```


---


2. **Atualize o contexto do EKS**

   Execute o comando abaixo para vincular o cluster:

   ```bash
   aws eks update-kubeconfig --region sa-east-1 --name general-cluster
   ```

   *Output esperado:*

   ```
   Added new context arn:aws:eks:...
   ```


---


3. **Verifique a conexão com o cluster**

   ```bash
   kubectl get pods -n prd-apps
   ```

   *Output esperado:* uma lista extensa com todos os pods da conta.

   > 
   > 3. Caso o kubectl não esteja instalado execute:
   >
   >    ```javascript
   >    sudo snap install kubectl --classic
   >    ```


---


4. **Crie o script de conexão temporária**

   Crie um arquivo `script.sh` (ou qualquer outro nome que preferir) na raiz do sistema e cole o conteúdo abaixo (ou faça download, copie e cole):

   \
   [script.sh 6899](/api/attachments.redirect?id=059424a7-e4e7-4339-8ab5-749297e9406b)

   \
   
:::tip
   💡 Para cada ambiente do banco (**stg**/**prd**), é necessário alterar os valores das variáveis `NAMESPACE` e `RDS_HOST`.

   :::


---


5. **Dê permissão de execução ao script**

   ```bash
   chmod +x script.sh
   ```


---


6. **Execute o script**

   ```bash
   ./script.sh
   ```

   Após rodar o comando, um **pod temporário** será construído para permitir a conexão segura com o banco de dados.


---


7. **Conecte-se com seu cliente SQL (DBeaver / Beekeeper / etc.)**

   Após o pod temporário estar rodando (ele faz o túnel para o RDS), configure seu cliente de banco com os dados locais abaixo:

   ```
   PORT=5432
   HOST=localhost
   DB_NAME=sapron-api
   USER=seu_user
   PASSWORD=sua_senha
   ```
   * No DBeaver/Beekeeper escolha **PostgreSQL** como tipo de conexão e preencha os campos acima.
   * Use o `USER`/`PASSWORD` fornecido por governança para acesso ao RDS via bastion (evite usar credenciais de produção sem permissão).


---


:::success
Finalizamos por aqui **✅**

:::