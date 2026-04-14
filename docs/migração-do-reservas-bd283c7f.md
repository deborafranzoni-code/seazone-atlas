<!-- title: Migração do Reservas | url: https://outline.seazone.com.br/doc/migracao-do-reservas-ZR8o2q7HQp | area: Tecnologia -->

# Migração do Reservas

Esta documentação irá abordar os passos que foram realizados para migrar o workload do reservas para o cluster.


Ferramentas utilizadas:

* Terraform
* Helm
* Terragrunt
* Aws Ssm
* Github Actions
* Docker


## Sobre a Aplicação do Reservas

O Serviço do Reservas é composto por 4 serviços, onde um é uma api que recebe os requests, dois são workers que realizam os trabalhos e o último é um scheduler que cuida das tasks que precisam rodar em um determinado horário.

## Criando Dockerfile

Para criar o dockerfile do Reservas primeiro é necessário criar a imagem base com a automação para puxar as variáveis de ambiente do ssm. As imagens estão no repositório [governanca-dockerfiles](https://github.com/seazone-tech/governanca-dockerfiles) e lá também estão todas as imagens que utilizamos atualmente.


Após criar o dockerfile com a imagem base Seazone, serão necessários 2 dockerfiles no repo da aplicação para buildar conforme o ambiente, por conta da imagem base estar nas duas contas. Dessa forma, nos casos de build em produção, o ci não precisa das credênciais das duas contas (staging e produção) somente o do ambiente que será buildado.


## Aplicando o CI


Para fazer o deploy no cluster o CI precisou dos seguintes arquivos no repositório :

| Repositório | Arquivo | Descrição |
|----|----|----|
| seazone-reservas-api | main.yaml | Faz o build, armazena a imagem e trigga o gitops de prod |
|    | staging.yaml | Faz o build, armazena a imagem e trigga o gitops de staging |
|    | semantic-version.yaml | Cria uma nova versão conforme a branch |
| gitops-seazone-reservas-api | deploy.yaml | Faz o deploy no cluster de produção |
|    | deploy-stg.yaml | Faz o deploy no cluster de staging |
|    | rebootPrd.yaml | Reinicia os pods desta aplicação em produção |
|    | rebootStg.yaml | Reinicia os pods desta aplicação em staging |
|    | repo-dispatch.yaml | Recebe o trigger do repo normal e altera o values.yaml |


:::warning
Reboot prod e stg

:::


Como o workflow do ci ainda não esta finalizado, por conta da priorização da migração antes do OKR do CI/CD, alguns ci precisam de variáveis por exemplo o main.yaml que precisa o app_name:

 ![](/api/attachments.redirect?id=a58ab12d-814e-49a0-a7bd-f14c2fe2d7dc)


:::info
Fique atento as variáveis que os arquivos acima podem solicitar para o funcionamento correto.

:::


## Variáveis no Systems Manager 

O Ssm é o centralizador de variáveis que estamos utilizando nas aplicações. Ele vai ser responsável por fornecer as variáveis de ambiente para as aplicações quando solicitado. Para inserir novas variáveis e manter o funcionamento correto é necessário que o a variável inserida no ssm tenha o prefixo do nome da aplicação. Por exemplo se a variável adicionada for a "EMAIL_SMTP_PASSWORD" e o nome do serviço for "*seazone-reservas-api*" a variável inserida será:

```bash
/seazone-reservas-api/EMAIL_SMTP_PASSWORD
```


Nos casos dos serviços que são do "frontend" ou precisam das variáveis no momento do build será necessário rodar o ci para buildar novamente em cada alteração de variável. Já para os serviços que não precisam das variáveis para buildar o dockerfile irá importar as variáveis sempre que for reiniciado.


## Gitops do Reservas

O workflow atual do Reservas possui uma integração com o gitops, nele é possível consultar as informações do helm, adicionar arquivos relacionados ao template do helm, ver as dependencias que foram criadas com terraform para este repositório e também alterar o values.yaml.


:::warning
Alterar o values.yaml realiza o deploy no cluster e altera as informações que estão no cluster. Logo esta alteraçã́o deve ser realizada com muito cuidado porque isso impacta diretamente o cliente final.

:::


## Criando O Helm 

Como temos um monolito que é divido em quatro, para criar o helm foi necessário criar 4 deployments diferentes que reutilizam a mesma imagem, assim temos a mesma informação porem em deployments distintos, alterando somente o comando de inicialização conforme o arquivo [run.sh](https://github.com/seazone-tech/seazone-reservas-api/blob/develop/run.sh). 


:::warning
O deployment do scheduler só pode conter um pod, isso se da porque cada pod do scheduler irá triggar as tasks conforme o seu conograma, logo se a mais um pod, esta task irá ser iniciada duas vezes.  

:::


## Componentes do Terraform do Reservas

O diretório /terraformApps contém os arquivos terraform de staging e produção. Nele estão as dependências que são específicas desta aplicação, facilitando a alteração e aumentando o controle dos times sobre as suas responsabilidades.

Dependências do Reservas que estão no Terraform de prod do gitops:

| Resource | Name |    |
|----|----|----|
| cloudflare_record | api |    |
| aws_ecr_repository | seazone-reservas-api |    |
| aws_s3_bucket | seazone-reservas-properties-ranking-prd |    |
| aws_s3_bucket | seazone-reservas-seo-page-info-prd |    |
| aws_s3_bucket | seazone-reservas-google-hotels-properties-feed-prd |    |
| aws_s3_bucket | seazone-reservas-referral-acommodations-prd |    |
| aws_iam_policy | seazoneReservas |    |
| aws_iam_role | reservas |    |
| aws_ses_domain_identity | seazone.com.br |    |
| aws_ses_domain_mail_from | no-reply-web |    |
| aws_ses_domain_dkim | - |    |
| rds | seazone-reservas |    |