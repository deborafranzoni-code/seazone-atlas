<!-- title: AWS | url: https://outline.seazone.com.br/doc/aws-RuXshp0bJ1 | area: Tecnologia -->

# AWS

>  💡
>
> A AWS (Amazon Web Services) é uma plataforma de serviços em nuvem oferecida pela Amazon. Ela fornece uma ampla gama de serviços, incluindo armazenamento, computação, banco de dados, redes, análise de dados, inteligência artificial e muito mais. Empresas e desenvolvedores usam a AWS para hospedar aplicações, gerenciar dados, criar infraestruturas escaláveis e implementar soluções tecnológicas de forma eficiente e segura na nuvem.


## Princípio do Menor Privilégio 🤏

Esse conceito rega que cada usuário, processo ou sistema deve ter apenas as permissões e acessos necessários para realizar suas funções específicas, e nada mais. Isso minimiza o risco de abuso de privilégios, erros ou explorações de segurança, limitando o alcance de qualquer ação maliciosa ou acidental, e esse é um conceito que devemos sempre tentar aplicar aqui na AWS

## Como funcionam as políticas da AWS 🛡️

No IAM (Identity and Access Management) da AWS, as políticas são declarações que definem permissões e são aplicadas a usuários, grupos e funções.

### Managed Policies

Essas são políticas pré-criadas pela AWS que podem ser aplicadas diretamente a usuários, grupos ou funções. Elas são mantidas pela AWS e são atualizadas automaticamente para incluir novos serviços ou recursos.

**Como Funcionam:**

As políticas gerenciadas são úteis para fornecer permissões comuns, como "AdministratorAccess", "ReadOnlyAccess", ou permissões específicas para serviços, como "AmazonS3FullAccess".


---

### Customer Managed Policies

Essas são políticas personalizadas criadas e gerenciadas por você. Elas permitem flexibilidade total para definir permissões de acordo com as necessidades específicas da sua organização.

**Como Funcionam:**

Você pode criar uma política que permite ou nega ações específicas em recursos específicos, ajustando as permissões exatamente como você deseja.


---

### Políticas In-line

Políticas in-line são políticas diretamente associadas a um único usuário, grupo ou função, e não podem ser reutilizadas em outros objetos. São úteis para permissões altamente específicas e restritas.

**Como Funcionam:**

Elas são criadas para situações onde uma permissão deve ser concedida apenas a uma entidade específica, sem possibilidade de reutilização.

# Tutoriais administrativos ✅

<aside> 💡

Segue uma lista de tutoriais que podem ser úteis pra quem está administrando a aws

</aside>

### Criar conta na AWS

<aside> 🚨 Lembrando que todo os usuários da AWS tem que ativar a 2FA após fazer o login

</aside>

1️⃣ Acesse a conta **[Seazone-Manager](https://d-926761dadf.awsapps.com/start/#/console?account_id=834181448060&role_name=AdministratorAccess&referrer=accessPortal)**

 ![Captura de tela 2024-06-18 195316.png](/api/attachments.redirect?id=20ca18bd-6872-4375-a9f3-c351d45a425f)

2️⃣ Acesse o IAM identity center

 ![Captura de tela 2024-06-18 195419.png](/api/attachments.redirect?id=b72cf1c2-8c6c-4ebb-b29c-645de84347b0)

3️⃣ Dentro do IAM selecione na barra lateral a opção de **users**

4️⃣ Clique em **add user** no canto superior direito

 ![Captura de tela 2024-06-18 195649.png](/api/attachments.redirect?id=78f54978-fba4-4553-b5dd-b4f7c15c564e)

5️⃣ Adicione as informações do usuário e clique em **continuar**

> Geralmente escolhemos a primeira opção para a definição de senha , onde é enviada uma senha provisória no email do usuário

 ![Captura de tela 2024-06-18 195743.png](/api/attachments.redirect?id=bc77e3fc-d46e-446a-b6b1-7cc304e0898a)

### Adicionar usuários em contas

1️⃣ Na conta [manager](https://d-926761dadf.awsapps.com/start/#/console?account_id=834181448060&role_name=AdministratorAccess&referrer=accessPortal) , acesse o IAM identity center

 ![Captura de tela 2024-06-18 200333.png](/api/attachments.redirect?id=bb5ddcad-7939-441a-8f4f-7284c4492cbe)

2️⃣ Na aba lateral selecione a opção **AWS accounts**

3️⃣ Escolha a conta desejada , pra saber o que tem em cada conta olhe o tópico de **Contas** nessa página

4️⃣ Acesse a conta e no canto superior direito clique em **assign user or groups**

 ![Captura de tela 2024-06-18 200705.png](/api/attachments.redirect?id=566f807e-6678-4746-ad25-c0e03cb5e3a5)

5️⃣ Na aba **users** selecione o usuário que você adicionará na conta e as permissões que ele terá

 ![Captura de tela 2024-06-18 201032.png](/api/attachments.redirect?id=83dcd965-32b7-4b56-bcef-d1a753bdf556)

### Remover usuários

1️⃣ Acesse o **IAM identity center dentro da conta [manager](https://d-926761dadf.awsapps.com/start/#/console?account_id=834181448060&role_name=AdministratorAccess&referrer=accessPortal)**

2️⃣ Selecione o usuário a ser removido

 ![Captura de tela 2024-06-18 212620.png](/api/attachments.redirect?id=909727f1-1ca2-4fb7-b7c6-6e1de21affdf)

3️⃣ clique em **delete users** no canto superior direito

 ![Captura de tela 2024-06-18 212708.png](/api/attachments.redirect?id=144ee6aa-32d8-41ba-a180-ffe47e2d5607)

### Recuperar contas de usuários

1️⃣ Acesse o **IAM identity center** dentro da conta **[manager](https://d-926761dadf.awsapps.com/start/#/console?account_id=834181448060&role_name=AdministratorAccess&referrer=accessPortal)**

2️⃣ abra o perfil do usuário desejado

 ![Captura de tela 2024-06-18 213153.png](/api/attachments.redirect?id=fe46feab-0098-41c9-8e15-e1e53df26512)

3️⃣ No canto superior direito clique em **reset password**

 ![Captura de tela 2024-06-18 213231.png](/api/attachments.redirect?id=38139000-2f75-47c8-8dba-a82eccdde779)

### Configurar 2FA

1️⃣ Acesse o [painel](https://d-926761dadf.awsapps.com/start/#/?tab=accounts)

 ![Captura de tela 2024-06-19 171129.png](/api/attachments.redirect?id=f3352a40-911d-4223-954f-110167d7de36)

2️⃣ Clique na opção MFA devices

 ![Captura de tela 2024-06-19 171256.png](/api/attachments.redirect?id=f68d74f8-1982-4d7d-b3ba-a20f3df1bdcd)

3️⃣ clique em register device

 ![Captura de tela 2024-06-19 171730.png](/api/attachments.redirect?id=4db5c573-ba4f-4416-8b9c-9b898bfa4625)

### Criar conta na AWS

<aside> 🚨 Lembrando que todos os usuários da AWS tem que ativar a 2FA após fazer o primeiro login

</aside>

1️⃣ Acesse a conta **[Seazone-Manager](https://d-926761dadf.awsapps.com/start/#/console?account_id=834181448060&role_name=AdministratorAccess&referrer=accessPortal)**

 ![Captura de tela 2024-06-18 195316.png](/api/attachments.redirect?id=20ca18bd-6872-4375-a9f3-c351d45a425f)

2️⃣  Acesse o IAM identity center

 ![Captura de tela 2024-06-18 195419.png](/api/attachments.redirect?id=b72cf1c2-8c6c-4ebb-b29c-645de84347b0)

3️⃣ Dentro do IAM selecione na barra lateral a opção de **users**

4️⃣ Clique em **add user** no canto superior direito

 ![Captura de tela 2024-06-18 195649.png](/api/attachments.redirect?id=78f54978-fba4-4553-b5dd-b4f7c15c564e)

5️⃣ Adicione as informações do usuário e clique em **continuar**

> Geralmente escolhemos a primeira opção para a definição de senha , onde é enviada uma senha provisória no email do usuário

 ![Captura de tela 2024-06-18 195743.png](/api/attachments.redirect?id=bc77e3fc-d46e-446a-b6b1-7cc304e0898a)

### Adicionar usuários em contas

1️⃣ Na conta [manager](https://d-926761dadf.awsapps.com/start/#/console?account_id=834181448060&role_name=AdministratorAccess&referrer=accessPortal) , acesse o IAM identity center

 ![Captura de tela 2024-06-18 200333.png](/api/attachments.redirect?id=bb5ddcad-7939-441a-8f4f-7284c4492cbe)

2️⃣  Na aba lateral selecione a opção **AWS accounts**

3️⃣ Escolha a conta desejada , pra saber o que tem em cada conta olhe o tópico de **Contas** nessa página

4️⃣ Acesse a conta e no canto superior direito clique em **assign user or groups**

 ![Captura de tela 2024-06-18 200705.png](/api/attachments.redirect?id=566f807e-6678-4746-ad25-c0e03cb5e3a5)

5️⃣  Na aba **users** selecione o usuário que você adicionará na conta e as permissões que ele terá

 ![Captura de tela 2024-06-18 201032.png](/api/attachments.redirect?id=83dcd965-32b7-4b56-bcef-d1a753bdf556)

### Remover usuários

1️⃣ Acesse o **IAM identity center dentro da conta [manager](https://d-926761dadf.awsapps.com/start/#/console?account_id=834181448060&role_name=AdministratorAccess&referrer=accessPortal)**

2️⃣  Selecione o usuário a ser removido

 ![Captura de tela 2024-06-18 212620.png](/api/attachments.redirect?id=909727f1-1ca2-4fb7-b7c6-6e1de21affdf)

3️⃣ clique em **delete users** no canto superior direito

 ![Captura de tela 2024-06-18 212708.png](/api/attachments.redirect?id=144ee6aa-32d8-41ba-a180-ffe47e2d5607)

### Recuperar contas de usuários

1️⃣ Acesse o **IAM identity center** dentro da conta **[manager](https://d-926761dadf.awsapps.com/start/#/console?account_id=834181448060&role_name=AdministratorAccess&referrer=accessPortal)**

2️⃣ abra o perfil do usuário desejado

 ![Captura de tela 2024-06-18 213153.png](/api/attachments.redirect?id=fe46feab-0098-41c9-8e15-e1e53df26512)

3️⃣ No canto superior direito clique em **reset password**

 ![Captura de tela 2024-06-18 213231.png](/api/attachments.redirect?id=38139000-2f75-47c8-8dba-a82eccdde779)

### Configurar 2FA

1️⃣ Acesse o [painel](https://d-926761dadf.awsapps.com/start/#/?tab=accounts)

 ![Captura de tela 2024-06-19 171129.png](/api/attachments.redirect?id=f3352a40-911d-4223-954f-110167d7de36)

2️⃣  Clique na opção MFA devices

 ![Captura de tela 2024-06-19 171256.png](/api/attachments.redirect?id=f68d74f8-1982-4d7d-b3ba-a20f3df1bdcd)

3️⃣ clique em register device

 ![Captura de tela 2024-06-19 171730.png](/api/attachments.redirect?id=4db5c573-ba4f-4416-8b9c-9b898bfa4625)

### Criar grupos de usuários

1️⃣ Acesse o **IAM identity center**

 ![Captura de tela 2024-08-29 172920.png](/api/attachments.redirect?id=a3a93df4-e403-42a7-b4f8-807f6156e39b)

2️⃣ Selecione a seção **groups**

 ![Captura de tela 2024-08-29 173118.png](/api/attachments.redirect?id=c216117b-021a-4ff5-83e6-ef0d5d1350b5)

3️⃣ Clique em **create group**

 ![Captura de tela 2024-08-29 173208.png](/api/attachments.redirect?id=abbee6d7-5871-4f8a-9f5e-fb5c7f57ebf2)

4️⃣ Configure as informações do grupo e os membros que vão participar do mesmo

### Dar permissões a grupos

1️⃣  Acesse o **IAM identity center**

 ![Captura de tela 2024-08-29 172920.png](/api/attachments.redirect?id=a3a93df4-e403-42a7-b4f8-807f6156e39b)

2️⃣ Selecione a opção **aws accounts**

 ![image.png](/api/attachments.redirect?id=27fcdaf0-d275-4563-8dc8-846994a8118f)

3️⃣ Escolha a conta desejada

4️⃣Na aba **users and groups** selecione o grupo desejado e clique em **change permission sets**

 ![Captura de tela 2024-08-29 175648.png](/api/attachments.redirect?id=f1447cce-0f8d-42e6-a17e-eb5c7abd222b)

# Contas 🗣️

💡 Temos algumas contas dentro da nossa organização na AWS , como cada conta tem sua própria função para a tech e para a seazone como um todo , dedicidimos listar cada conta aqui e o que há dentro dela para que a solicitação de acessos e própria navegação na nossa AWS fique mais simples


### Audit

*Essa conta está configurada para desempenhar a função de auditoria no AWS Control Tower, possuindo os recursos necessários para esta função(Cloud Trail, SNS, AWS Config e CloudWatch), configurados através do Cloud Formation*

### Data Backup

*A conta de backup na AWS permite que se gerencie os backups de forma centralizada, garantindo   a   segurança   dos   dados,   na   Seazone   essa   conta   está   com   dois   buckets  que armazenam dados de backup do Data Lake, totalizando 1.5TB, armazenados no S3 Standard*

### DEV-lake

*Essa conta está configurada como ambiente de desenvolvimento utilizado pela Seazone, para testes e desenvolvimento de novas funcionalidades no Data Lake principal, tendo como recursos utilizados pela conta o Glue, S3, Sagemaker, Athena, EFS, Lambda e Step Functions.*

### DEV-Sirius

*Essa conta está configurada como ambiente de desenvolvimento utilizado pela Seazone, para testes e desenvolvimento de novas funcionalidades no Data Lake Sirius, que é utilizado para precificação de hospedagens, tendo como recursos AWS principais o Glue, S3, Athena, Lambda e Step Functions*

### Log Archive

*Essa   conta   é  dedicada   à  ingestão   e   arquivamento   de   todos   os   registros   e   backups relacionados à segurança. Com registros centralizados, que podem ser utilizados para monitorar,auditar e alertar sobre o acesso a objetos do S3, atividades não autorizadas, mudanças na política do IAM e outras atividades críticas realizadas em recursos confidenciais.*

### PRD-Lake House

*Essa conta está sendo utilizada para um novo projeto, que irá hospedar e centralizar todos os dados e repositórios produtivos de um novo Data Lake que utiliza fontes de dados internos da Seazone. Até o momento estão sendo utilizados o AWS S3 para repositório e o AWS Glue, como catálogo de dados.*

### PRD-Sapron

Essa conta hospeda o ambiente de homologação, juntamente com o site produtivo que é utilizado pelos usuários para realização de reservas de imóveis na Seazone. Dentre os principais serviços utilizados, temos: Application Load Balancers, clusters ECS, instâncias EC2 e RDS. A conta também hospeda diversos certificados digitais utilizados pela Seazone.

### PRD-Sapron Fechamento

*Essa conta hospeda o módulo do Sapron, responsável por processar o fechamento fiscal da Seazone,  para   isto,   ela   possui   um   Data   Lake   gerenciado   pelo   AWS   Glue,   com   alguns microserviços em Lambda, que são orquestrados pelo AWS EventBridge e StepFunctions.*

### PRD-Sirius

*Essa conta hospeda o workload responsável pela realização da precificação dos imóveis gerenciados pela Seazone, a aplicação utiliza um Data Lake próprio que é gerenciado pelo AWS Glue, com alguns microserviços em Lambda, que são orquestrados pelo AWS EventBridge e StepFunctions. O workload possui integrações externas com a GCP, que se comunicam através de API Gateway.*

### PRD-Lake

*Essa conta está configurada para suportar o workload produtivo do Data Lake principal da Seazone, tendo como principais recursos da conta o AWS Glue, S3, Sagemaker, Lambda, Event Bridge, Step Functions, Firehose, API Gateway, SQS e SNS.*

### Sandbox

*Essa conta hospeda o ambiente de Sandbox da Seazone, utilizado como um ambiente isolado e seguro destinado ao desenvolvimento, teste e experimentação de aplicações  e serviços, para não afetar os sistemas de produção. Dentre os serviços configurados nesta conta, temos o AWS Glue, Athena e Lambda.*

### STG-Sapron Fechamento

*Essa conta hospeda o stagging do módulo Sapron Fechamento, responsável por processar o fechamento fiscal da Seazone, ela possui um Data Lake gerenciado pelo AWS Glue, com alguns microserviços em Lambda, que são orquestrados pelo AWS EventBridge e StepFunctions.*

### Production

*Atualmente, esta é nossa conta de produção, onde temos um [cluster EKS](https://docs.aws.amazon.com/pt_br/eks/latest/userguide/clusters.html) em operação além do RDS para nossas tools que são ferramentas de apoio para nossos processos. Já alocamos algumas ferramentas e recursos nela, e o plano é migrar todos os nossos serviços e ferramentas de produção para essa conta ao longo do tempo.*

### Staging

*Esta é nossa conta de staging, onde também temos um [cluster EKS](https://docs.aws.amazon.com/pt_br/eks/latest/userguide/clusters.html) em operação. O objetivo é alocar os ambientes de staging de todos os nossos recursos atuais nesta conta.*

### Seazone Manager

Essa é a nossa **conta main** da organização, a base central de gerenciamento de todas as atividades administrativas. Por meio dela, podemos **criar e gerenciar contas novas**, além de administrar **usuários, grupos e permissões** de forma eficiente em todas as demais contas associadas. É um recurso essencial para garantir a **organização**, **segurança** e **controle centralizado** das operações. É importante lembrar que o acesso a essa conta deve ser restrito e utilizado com cautela, seguindo as melhores práticas de segurança.

# Organização de contas 

Atualmente temos uma organização de contas entre organization units, a ideia dessa organização é facilitar a visualização de contas e também facilitar a aplicação de regras para ambientes específicos na  org

Atualmente nossas contas e organization units estão dessa forma : 

## Root

### Sandbox

Esta é a nossa unidade organizacional sandbox, ideal para laboratórios e atividades correlatas.

**Contas da OU** :arrow_down:

* `Sandbox`

### Security

Esta é nossa Unidade Organizacional (OU) de segurança, que abriga contas dedicadas à coleta e arquivamento de registros de segurança. Esses registros podem ser usados posteriormente para monitorar e auditar atividades suspeitas.

**Contas da OU ⬇️**

* `Audit`
* `Log Archive`

### Workloads

Esta agrupa nossas Unidades Organizacionais (OUs) de fluxo de trabalho, que representam as divisões dos nossos ambientes.

**Development**

Development é onde estão alocados nossos ambientes de desenvolvimento, incluindo as contas atualmente ativas nesses ambientes.

* `aws-dev-sirius`
* `DEV-lake`

**Staging**

Aqui estão alocadas nossas contas de staging. Atualmente, as seguintes contas estão incluídas nesta Unidade Organizacional (OU):

* `Staging`
* `STG - Sapron Fechamento`

**Production**

Aqui estão todas as nossas contas que abrigam os ambientes de produção. Atualmente, as seguintes contas estão incluídas nesta Unidade Organizacional (OU):

* `PRD - Data backup`


* `PRD - LakeHouse`
* `PRD- Sapron` 
* `PRD - Sapron Fechamento`
* `PRD - Sirius` 
* `PRD - Lake`
* `Production`
* `Seazone Technology`


 ![](/api/attachments.redirect?id=8cf5cf6c-cb70-48b6-9380-12b29d2be211 " =804x519")


\