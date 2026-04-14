<!-- title: Permissões | url: https://outline.seazone.com.br/doc/permissoes-5sV9GFXrfu | area: Tecnologia -->

# Permissões

O objetivo dessa documentação é mapear por time dentro da tecnologia quais são os recursos utilizados em cada conta que o time acessa, a ideia é diminuir o número de permissões abrangentes como a PowerUser que temos aplicada as vários times atualmente 


# Data Ops

`DataOps` é o permission set do time de Ops dentro de dados, atualmente ele é composto pelas seguintes policies :

`IAMTeamAdminAccess` 

A política customizada foi projetada para permitir certas ações de gerenciamento e escrita no IAM. Ela é mais granular que a IAMFullAccess e tem como objetivo aderir ao princípio do privilégio mínimo. Esta política concede permissões específicas para cada conta e pode ser modificada pelo IAM da conta em questão.

`OpsTeamAcess`

A política personalizada foi desenvolvida para conceder acesso a todos os recursos identificados pelo time de `DataOps` como necessários. O objetivo é monitorar e atualizar essa política ao longo do tempo, garantindo que ela atenda estritamente às necessidades reais da equipe. Esta política possui permissões específicas por conta e pode ser ajustada por meio do IAM da conta em que as permissões precisam ser atualizadas.

### Contas acessadas **⬇️**

### aws-dev-sirius

**Recursos Utilizados :** 

*  AWS Service Catalog
* AWS Organizations
  * DescribeOrganization
* IAM
* EC2
* S3
* Athena 
* Glue

  \
  \

### DEV-lake

**Recursos utilizados :** 

* AWS Glue
* AWS User Notifications
* Amazon EC2
* AWS Service Catalog
* AWS Billing and Cost management
* Amazon S3
* IAM
* Amazon Athena
* Amazon DataZone
* Amazon Cloudwatch
* AWS CloudFormation
* AWS Lambda
* Amazon EventBridge 
* Amazon EC2 Auto Scaling
* Amazon Redshift
* Amazon OpenSearch Ingestion
* AWS Application Auto Scaling
* Amazon DynamoDB
* Amazon SQS
* Amazon SNS
* AWS CloudTrail
* AWS Step Functions

  \

### PRD - Sirius	

**Recursos utilizados :** 

* AWS Service Catalog
* Amazon EC2
* AWS Glue
* AWS User Notifications
* Amazon S3
* Amazon Athena
* Amazon DataZone
* Billing and Cost Management 
* IAM 
* AWS CloudTrail
* AWS Lambda
* AWS Key Management Service
* AWS Step Functions
* AWS Resource Explorer
* AWS CloudFormation
* Amazon CloudWatch
* Amazon EventBridge

### PRD-Lake

**Recursos utilizados :** 

* Amazon Athena
* AWS Glue
* Amazon DataZone
* AWS Service Catalog
* AWS billing and cost management
* AWS Lambda
* AWS Key Management Service
* IAM
* AWS Compute Optimizer
* Amazon EventBridge
* AWS CloudFormation
* Amazon SQS
* Amazon CloudWatch
* AWS Security Hub
* Amazon CloudWatch 
* AWS Resource Explorer
* Amazon SNS
* AWS CloudTrail
* Amazon SageMaker
* AWS Step Functions
* Amazon DynamoDB
* Amazon EC2 Auto Scaling
* AWS Application Auto Scaling
* Amazon Redshift
* Amazon Kinesis Firehose
* Amazon OpenSearch Ingestion

### Seazone Technology

**Recursos utilizados :** 

* Amazon Elastic Container Service
* AWS CloudFormation
* AWS Glue
* Amazon SNS
* Amazon EC2
* Amazon S3
* IAM
* AWS Step Functions
* AWS Systems Manager
* AWS CloudWatch
* AWS Compute Optimizer
* Elastic Load Balancing
* Amazon EC2 Auto Scaling
* AWS Application Auto Scaling
* AWS Resource Explorer
* Amazon EventBridge
* Amazon SQS
* AWS Resource Groups
* AWS Lambda
* Amazon Athena

# Data Solutions

`DataSolutions `é o permission set do time de Solutions dentro de dados, atualmente ele é composto pelas seguintes policies :

`IAMTeamAdminAccess` 

A política customizada foi projetada para permitir certas ações de gerenciamento e escrita no IAM. Ela é mais granular que a IAMFullAccess e tem como objetivo aderir ao princípio do privilégio mínimo. Esta política concede permissões específicas para cada conta e pode ser modificada pelo IAM da conta em questão.

`SolutionsTeamAcess`

A política personalizada foi desenvolvida para conceder acesso a todos os recursos identificados pelo time de `DataSolutions` como necessários. O objetivo é monitorar e atualizar essa política ao longo do tempo, garantindo que ela atenda estritamente às necessidades reais da equipe. Esta política possui permissões específicas por conta e pode ser ajustada por meio do IAM da conta em que as permissões precisam ser atualizadas.

### **Contas acessadas ⬇️**

### aws-dev-sirius

**Recursos utilizados :** 

* IAM
* AWS Resource Explorer
* Billing 
* AWS Service Catalog
* Amazon EC2
* Amazon S3
* Amazon Athena
* AWS Glue
* AWS Lambda
* AWS Key Management Service
* Amazon EventBridge 
* AWS CloudFormation
* Amazon DataZone
* AWS Compute Optimizer
* AWS Systems Manager
* AWS CloudTrail
* Amazon SNS
* AWS Security Hub
* Amazon CloudWatch
* AWS Step Functions
* Amazon SQS
* Elastic Load Balancing
* Amazon EC2 Auto Scaling

### DEV-lake

**Recursos utilizados :** 

* AWS Organizations
* Amazon EC2
* AWS Service Catalog
* AWS Lambda
* AWS Key Management Service
* Billing
* Amazon EventBridge 
* AWS CloudFormation
* AWS Glue
* Amazon S3
* Amazon DataZone
* Amazon Athena
* AWS Resource Explorer
* AWS Compute Optimizer
* AWS Security Hub

### PRD - Sirius

**Recursos utilizados :** 

* AWS CloudFormation
* AWS User Notifications
* AWS Resource Explorer
* AWS Lambda
* Amazon EventBridge 
* AWS Key Management Service
* IAM
* AWS Compute Optimizer
* AWS Step Functions
* Amazon EC2
* AWS Service Catalog
* Amazon S3
* Amazon Athena
* AWS Glue
* Amazon DataZone
* AWS Security Hub
* AWS Systems Manager
* Amazon CloudWatch
* Amazon SQS
* Amazon EC2 Auto Scaling
* Elastic Load Balancing
* Amazon SNS
* Amazon SageMaker

### PRD-Lake

**Recursos utilizados :** 

* Amazon S3
* Amazon Athena
* AWS Glue
* AWS User Notifications
* Amazon DataZone
* Amazon EC2
* AWS Service Catalog
* AWS Cost Explorer Service
* AWS Security Hub
* AWS Lambda
* AWS Key Management Service
* AWS Resource Explorer
* AWS Security Token Service
* Amazon EventBridge
* AWS CloudFormation
* Amazon CloudWatch
* AWS Resource Groups
* AWS Compute Optimizer
* AWS Systems Manager
* Elastic Load Balancing
* Amazon EC2 Auto Scaling
* Amazon Redshift
* Amazon Route 53 Resolver
* Amazon AppFlow
* AWS Step Functions
* Amazon SageMaker
* Amazon SNS 

### Seazone Technology

**Recursos utilizados :** 

* Amazon EC2
* Amazon CloudWatch
* Elastic Load Balancing
* Amazon EC2 Auto Scaling
* AWS Service Catalog
* billing
* Amazon CloudWatch 
* AWS Systems Manager
* IAM
* AWS Compute Optimizer
* AWS Key Management Service
* AWS Resource Explorer
* AWS Resource Groups
* Amazon CloudWatch 
* Amazon Elastic Container Service
* Amazon S3


# Reservas 

`Reservas`é o permission set do nosso time que cuida do site de reservas , atualmente ele é composto pelas seguintes policies :

`ReservasTeamAcess`

A política personalizada foi desenvolvida para conceder acesso a todos os recursos identificados pelo time de `Reservas`como necessários. O objetivo é monitorar e atualizar essa política ao longo do tempo, garantindo que ela atenda estritamente às necessidades reais da equipe. Esta política possui permissões específicas por conta e pode ser ajustada por meio do IAM da conta em que as permissões precisam ser atualizadas.

### Contas **⬇️**

### PRD - Sapron

**Recursos utilizados :** 

* Amazon Elastic Container Service
* Amazon CloudWatch 
* Amazon EC2 Auto Scaling
* Amazon EC2
* AWS Service Catalog
* AWS Security Hub
* Elastic Load Balancing
* AWS Resource Explorer
* AWS Systems Manager
* AWS Compute Optimizer
* AWS CloudFormation
* IAM
* Amazon Elastic Container Registry
* Amazon S3
* Amazon SES
* Amazon SQS
* AWS Resource Groups
* AWS Performance Insights
* Amazon DevOps Guru
* Amazon RDS
* AWS Key Management Service
* Amazon GuardDuty
* AWS Certificate Manager
* Amazon EventBridge
* AWS CloudTrail
* AWS Glue
* Amazon Athena

# Sapron 

`Sapron` é o permission set do nosso time que cuida do site de reservas , atualmente ele é composto pelas seguintes policies :

`SapronTeamAcess`

A política personalizada foi desenvolvida para conceder acesso a todos os recursos identificados pelo time de `SapronTeamAcess` como necessários. O objetivo é monitorar e atualizar essa política ao longo do tempo, garantindo que ela atenda estritamente às necessidades reais da equipe. Esta política possui permissões específicas por conta e pode ser ajustada por meio do IAM da conta em que as permissões precisam ser atualizadas.

**Contas Acessadas ⬇️**

### Seazone Technology

* Amazon EC2
* ~~AWS Service Catalog~~
* Billing
* IAM
* AWS CloudFormation
* Amazon Elastic Container Service
* Amazon CloudWatch
* Elastic Load Balancing
* Amazon SQS
* Amazon EC2 Auto Scaling
* AWS Organizations
* Amazon Elastic Container Registry
* AWS Systems Manager
* ~~Amazon DynamoDB~~
* Amazon RDS
* Amazon Elastic Kubernetes Service
* ~~Amazon MQ~~
* Amazon S3
* ~~AWS Cloud9~~
* ~~Amazon GuardDuty~~
* AWS CloudTrail
* AWS Key Management Service
* ~~Amazon DevOps Guru~~
* ~~Amazon EventBridge~~
* Amazon Route 53
* AWS Resource Groups
* AWS Lambda

### PRD - Sapron Fechamento

* Amazon S3
* Amazon Elastic Container Service
* Amazon EC2
* Amazon SQS
* AWS Resource Explorer
* ~~AWS Service Catalog~~
* Billing
* IAM 
* AWS Lambda
* AWS Key Management Service
* Amazon CloudWatch
* ~~Amazon EventBridge~~ 
* AWS CloudFormation
* AWS Step Functions
* Amazon SNS
* Elastic Load Balancing
* Amazon EC2 Auto Scaling
* Amazon RDS


\