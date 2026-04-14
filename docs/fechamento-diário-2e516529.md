<!-- title: Fechamento Diário | url: https://outline.seazone.com.br/doc/fechamento-diario-oT0KKyjyuy | area: Tecnologia -->

# Fechamento Diário

### Sobre a utilização

De forma geral, o método desenvolvimento do projeto pode ser visto no seguinte vídeo


De forma resumida, é necessário realizar a autenticação via SSO, como pode ser visto aqui:

[IAM Identity Center credential provider - AWS SDKs and Tools](https://docs.aws.amazon.com/sdkref/latest/guide/feature-sso-credentials.html)

Após, pode-se realizar o deploy com os comandos

```bash
sam build --template financeiro/master-stack.yaml --region us-west-2 --use-container --profile NOME_PROFILE
```

```bash
sam deploy --stack-name NOME_DA_STACK --region us-west-2 --s3-bucket BUCKET_ARTEFATOS --no-fail-on-empty-changeset --role-arn ARN_DA_ROLE_DO_CF --profile NOME_PROFILE
```


---

### Sobre a Autenticação

O workflow do Github utiliza uma autenticação via Identity Provider. Com isso, utilizamos uma role para realizar a criação dos recursos, diferente de usar um usuário com senha.

[Use IAM roles to connect GitHub Actions to actions in AWS | Amazon Web Services](https://aws.amazon.com/pt/blogs/security/use-iam-roles-to-connect-github-actions-to-actions-in-aws/)


---

### Sobre Conta e Roles

É recomendado que o projeto seja separado em pelo menos duas contas, uma conta de produção e uma conta de desenvolvimento. Na primeira, apenas a stack de produção, advinda da branch *main,* enquanto na segunda, ficarão as stacks das branches *dev* e \*features/\*\*.

Assim como serão duas contas, deverão ser criadas uma role para cada conta, que serão usadas pelo SAM para realizar o deploy dos recursos. A configuração dessa role está nas variáveis de ambiente do workflow.

<aside> ⚠️ Recomenda-se a criação das Roles dos serviços por fora e passá-las como parâmetros para o template. Assim, o CI/CD e a sua role não terão IAM_CAPABILITIES, o que pode ajudar na segurança, já que o pipeline não terá acesso para criar novas roles.

</aside>


---

### Estrutura do projeto e organização dados

O projeto utiliza o Step Functions da AWS para gerenciar as lambdas, definindo ordem de execução, paralelismo e até inputs e outputs dentro do workflow. Essa estrutura está definida dentro de um arquivo de configuração .yaml no repositório e é deployado pelo Git Actions junto com o AWS SAM.

Os dados processados pelas lambdas serão armazenados em buckets dentro da S3. Podemos definir 3 etapas de processamento de dados até ter o dados finais consolidados. Primeiro os dados são ingeridos do RDS de Sapron. Na primeira etapa os dados ***raws*** são salvos em buckets da forma que vêm do RDS. Em uma segunda etapa, é processado a receita diário de cada propriedade, para então por fim a terceira etapa processar a receita diária de proprietários e anfitriões. Uma 4 etapa pode ser adicionada para agrupar as receitas por semanas, meses ou anos. Para entender melhor o step functions e discussões a respeito da estrutura de dados no S3, a reunião gravada logo abaixo aborda um overview sobre esses pontos:



---

### Parâmetros e Configurações

A parte de parametrização no Git Actions pode ser feito utilizando as variáveis de ambiente do workflow ou utilizando as variáveis dos "Environments" do Github. Além disso, para o template e em outros lugares do código, pode-se utilizar o Parameter Store, parte do recurso AWS Systems Manager.

Geralmente o Parameter Store guarda apenas um valor por vez para facilitar o "resolve", como pode ser visto no exemplo:

[Using dynamic references to specify template values - AWS CloudFormation](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/dynamic-references.html)

* Método workaround

  Outra forma de realizar esse processo, é guardar todas as informações importantes em apenas um parâmetro, no formato JSON. Com esse valor, é possível lê-lo e passá-lo como parâmetro no sam deploy, com o parâmetro —parameter-override.

  [sam deploy - AWS Serverless Application Model](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/sam-cli-command-reference-sam-deploy.html)

<aside> 💡 Cuidado com chaves e informações importantes em referências dinâmicas no SAM

</aside>


---

### Sobre Testes

Os testes são ferramentas muito úteis no desenvolvimento de software. Dentro da área de dados, podem ser um pouco mais complexos de serem feitos. No caso desse projeto, além de utilizar ferramentas de *lint,* seria possível construir algumas ferramentas de data quality na AWS, assegurando a qualidade do dado presente no S3.

## Sobre criação de novos recursos

O template SAM é o responsável pela criação dos recursos na AWS. Como o objetivo é criar a infraestrutura como se fosse um código modificável (IaC), pode-se incorrer em problemas parecidos com os que encontramos na construção de código: nomenclaturas, organização etc. Para isso, podemos sugerir algumas práticas.

### Dos nomes dos recursos

Os recursos da AWS contém dois identificadores, um físico e um lógico. O nome físico, é o nome que será o nome do recurso na AWS, enquanto o lógico, será o nome a ser referenciado dentro do template. O nome lógico sempre será necessário na criação do recurso, mas o nome físico pode ser omitido. Isso é **desejável**, visto que definir os nomes dos recursos pode levar a conflitos de nomes físicos (dois recursos na AWS com o mesmo nome), falta de padronização, entre outros.

### Da organização

Conforme a arquitetura cresce, é desejável que as stacks sejam organizadas em módulos, para serem mais facilmente modificáveis e organizados.  Como estamos trabalhando com recursos Serverless, o SAM nos fornece algumas capacidades extras, não presentes no CloudFormation::Stack. Isso é feito utilizando AWS::Serverless::Application. No fundo, ele cria uma nested stack utilizando o CloudFormation::Stack e nos dá a possibilidade de referênciar artefatos locais, assim como é feito com os códigos do AWS::Serverless::Function.

<aside> 💡 Quando o sam package e deploy é feito na master stack, as nested stacks são automaticamente contempladas.

</aside>

[AWS::Serverless::Application - AWS Serverless Application Model](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/sam-resource-application.html)

Então a ideia é que exista uma Master Stack que implementa várias nested stacks, como se fossem módulos de uma aplicação.

Exemplo:

Master Stack:

* Nested Stack 1: recursos da layer raw
* Nested Stack 2: recursos da layer stage
* Nested Stack 3: recursos da layer enriched

Como cada stack é criada individualmente, é possível enviar parâmetros específicos para cada stack e também usar tags específicas.

É possível usar a seção "Outputs" do template para passar retornar parâmetros para a master stack.

[Outputs - AWS CloudFormation](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/outputs-section-structure.html)


---

# Como visualizar os dados

Os buckets foram dividos conforme a necessidade dos dados,

* [fechamento-diario-dados-raw](https://s3.console.aws.amazon.com/s3/buckets/fechamento-diario-dados-raw?region=us-west-2): todos os dados raw ingeridos do RDS;
* [fechamento-diario-dados-propriedades](https://s3.console.aws.amazon.com/s3/buckets/fechamento-diario-dados-propriedades?region=us-west-2): segunda camada, após processamento das propriedades, particionado por property_id;
* [fechamento-diario-dados-owner](https://s3.console.aws.amazon.com/s3/buckets/fechamento-diario-dados-owner?region=us-west-2): camada com dados do owner, particionado por owner_id;
* [fechamento-diario-dados-host](https://s3.console.aws.amazon.com/s3/buckets/fechamento-diario-dados-host?region=us-west-2): camada com dados do host, particionado por host_id;

Vídeo sobre a explicação dessa seção:


### Método Simples direto no S3

**Prós**: método mais fácil e rápido.

**Contras**: apenas um arquivo por vez, dificultando também uma validação de queries mais complexas.

O método mais fácil e rápido para visualizar os dados gerados, é utilizar o S3 Select direto no S3. Selecione o dado que deseja visualizar, vá em "Actions" e "Query With S3 Select".

 ![Untitled](Fechamento%20Dia%CC%81rio%200ba09fe59fbb4d589045f550b577bdcd/Untitled.png)

É recomendado visualizar como JSON, que geralmente representa melhor os dados em relação as colunas.

Na parte inferior é possível executar queries SQL como se fosse no AWS Athena.

 ![Untitled](Fechamento%20Dia%CC%81rio%200ba09fe59fbb4d589045f550b577bdcd/Untitled%201.png)

### Método via Jupyter Notebook

**Prós**: oferece suporte para leitura de prefixos inteiros, inclusive particionados.

**Contras**: custo de provisionar um sagemaker notebook.

No serviço AWS Sagemaker, procure "Notebooks" e inicie o notebook.

<aside> ⚠️ O notebook é pago por hora, então desligue-o quando não for utilizá-lo.

</aside>

O notebook funciona como um jupyter notebook local ou como o Google Colab. Se tiver dúvidas da sua utilização, siga o guia:

[How to Use Jupyter Notebook in 2020: A Beginner's Tutorial](https://www.dataquest.io/blog/jupyter-notebook-tutorial/)

Dentro de um notebook é possível escrever códigos em Python que interagem com todo o ambiente da AWS sem nenhum downside, custo ou necessidade de autenticação específica. Podemos utilizar a ferramenta AWSWrangler para realizar a leitura dos arquivos em parquet.

[Quick Start — AWS SDK for pandas 3.2.1 documentation](https://aws-sdk-pandas.readthedocs.io/en/stable/)

Note que essa ferramenta não funciona apenas para parquet, mas para vários serviços, bem como RDS, Redshift, DynamoDB, Athena, entre outros.

Desse modo, é possível ler prefixos (tabelas) particionados como mostra a imagem:

 ![Untitled](Fechamento%20Dia%CC%81rio%200ba09fe59fbb4d589045f550b577bdcd/Untitled%202.png)

<aside> ⚠️ Sempre que estivermos trabalhando com tabelas particionadas ou tabelas que sejam representadas por mais do que um arquivo parquet, é necessário usar a keyword "dataset".

</aside>

### Método via Jupyter Notebook