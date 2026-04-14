<!-- title: Sistema de Avisos | url: https://outline.seazone.com.br/doc/sistema-de-avisos-hPuz7NAv0r | area: Tecnologia -->

# Sistema de Avisos

Bem-vindo à documentação do Sistema de Avisos. Este sistema foi concebido com o objetivo de proporcionar uma resposta ágil e organizada a eventos adversos, garantindo a eficiência operacional.

## **Estrutura do Sistema**

O Sistema de Avisos adota uma abordagem unificada para Step Functions e Lambdas, implementando estratégias específicas para cada componente. Como podemos ver na  figura a seguir.

 ![Sistemas de Avisos.png](/api/attachments.redirect?id=d551b864-cf9f-4784-9e06-2a2160e10c23)

### **Step Functions**

Quando um estado de um Step Function falha, existe uma captura do erro e encaminhamento para o fluxo de publicação no tópico do Simple Notification Service (SNS) configurado, finalizando a execução em estado de erro.

### **Lambdas**

No contexto das Lambdas, o Sistema de Avisos incorpora um mecanismo de tratamento de exceções. Caso ocorra uma exceção, a mensagem de erro é enviada no tópico SNS. Importante frisar que não é qualquer erro, mas um erro não mapeado ou uma quebra repentina do processo.

## **Integrações**

O sistema de avisos funciona no modelo Pub-Sub (Publish-Subscribe), implementado via tópicos SNS. Atualmente, as Lambdas e Step Functions são os "Publishers" e existe um Lambda de avisos que é o "Subscriber". Este Lambda é triggado pela publicação no tópico SNS, e envia mensagens formatadas para um canal designado no Slack. Essa integração proporciona uma visibilidade imediata e contextualizada das falhas, permitindo uma resposta eficiente por parte das equipes responsáveis.

# Modificações no Sistema de Avisos

Nesta seção, abordaremos em detalhes as modificações essenciais no código existente para integrar e operacionalizar o Sistema de Alertas. Seja através de ajustes nas funções Lambda ou na configuração da Step Function.

### Lambda

Para integrar o sistema ao Lambda, é implementada uma estratégia de `try` e `except` na seção de execução do código. Dessa forma, em caso de qualquer erro durante a execução, o bloco `except` será acionado, enviando uma mensagem para o tópico SNS associado. O exemplo abaixo ilustra o que deve ser adicionado ao código:

```python
import boto3
import json

client_sns = boto3.client('sns')

SNS_ERROR_TOPIC = os.environ['SNS_ERROR_TOPIC']

def lambda_handler(event, context):
    try:
				#funções de execução do código

		except Exception as err:
        message = {'Source': context.invoked_function_arn, 'Cause':  f'{err}'}
        client_sns.publish(TopicArn = SNS_ERROR_TOPIC, Message = json.dumps(message))
        raise err
```

É crucial lembrar de, na seção de Infraestrutura como Código (IaC), passar o valor de `SNS_ERROR_TOPIC` como uma variável de ambiente para garantir a correta configuração da comunicação com o tópico SNS.

# Infraestrutura como código

Exploraremos passo a passo como definir e gerenciar toda a infraestrutura necessária para o funcionamento eficaz do sistema. Cada serviço terá sua explicação e no final mostraremos como fazer a integração entre os serviços, permissões e politicas.

### Tópico SNS

Essa representação em YAML está definindo um recurso AWS CloudFormation para criar um Tópico (Topic) no serviço Simple Notification Service (SNS).

```yaml
SNSErrorExecution:
    Type: AWS::SNS::Topic
    Properties:
      Tags:
        - Key: product
          Value: revenue_management
        - Key: project
          Value: sirius
        - Key: module
          Value: supervisorio
```

* **SNSErrorExecution:** Isso representa o nome lógico do recurso, que é usado para referenciá-lo dentro do modelo CloudFormation.
* **Type: AWS::SNS::Topic:** Define o tipo de recurso como um Tópico no Simple Notification Service.
* **Properties:** Aqui estão as propriedades específicas para configurar o Tópico:
  * **Tags:** Um conjunto de tags associadas ao Tópico. As tags são metadados que ajudam a organizar e identificar os recursos. No exemplo fornecido, três tags estão sendo definidas.

### Lambda de Integração SNS - SLACK

A seção a seguir descreve a configuração da função Lambda chamada "LambdaErrorExecutionReport". Essa função desempenha um papel crucial no relatório de execuções com erros no sistema. Aqui estão os detalhes essenciais:

```yaml
LambdaErrorExecutionReport:
  Type: AWS::Serverless::Function
  Properties:
    CodeUri: ./report/error_execution
    Handler: lambda_function.lambda_handler
    Runtime: python3.9
    Timeout: 360
    MemorySize: 128
    Role: !Ref LambdaErrorExecutionReportRole
    Layers:
      - "arn:aws:lambda:us-west-2:336392948345:layer:AWSSDKPandas-Python39:7"
      - !Ref SlackLayer
    Events:
      SNSEvent:
        Type: SNS
        Properties:
          Topic: !Ref SNSErrorExecution
    Tags:
      product: revenue_management
      project: sirius
      module: supervisorio
    Environment:
      Variables:
        ENVIRONMENT: !If [IsProduction, prod, dev]
        SLACK_CHANNEL: !If [IsProduction, C0659SV0WQP, C05HUM2KGP4]
```

* **Type: AWS::Serverless::Function:** Define o tipo de recurso como uma função serverless na AWS Lambda.
* **Properties:** Configurações específicas para a função Lambda:
  * **CodeUri:** O diretório que contém o código-fonte da função.
  * **Handler:** O ponto de entrada da função (função específica que será invocada).
  * **Runtime:** A versão do ambiente de execução Python (python3.9 neste caso).
  * **Timeout:** O tempo máximo de execução da função em segundos.
  * **MemorySize:** O tamanho da memória alocada para a função.
  * **Role:** A referência para a função de IAM (LambdaErrorExecutionReportRole) que concede permissões necessárias à função.
  * **Layers:** Camadas adicionais associadas à função, incluindo uma camada AWS SDK Pandas e a camada SlackLayer.
  * **Events:** Configuração do evento que aciona a função. Neste caso, a função é acionada quando uma mensagem é publicada no tópico SNS referenciado (SNSErrorExecution).
  * **Tags:** Tags associadas à função para fins de organização e identificação.
  * **Environment:** Configuração das variáveis de ambiente necessárias para a função, incluindo o ambiente (prod ou dev) e o canal Slack associado.

### Parâmetros passados pelo SSM Parameter

A seção a seguir descreve a configuração do parâmetro do AWS Systems Manager (SSM) denominado "SNSErrorExecutionConfig". Esse parâmetro é fundamental para armazenar o Amazon Resource Name (ARN) do Tópico SNS associado aos erros de execução. Devido à existência de várias stacks no sistema, todas compartilhando o mesmo tópico SNS para acionar a função Lambda, empregamos o SSM Parameter para transmitir os valores entre essas diferentes stacks. O padrão utilizado para essa comunicação pode ser visualizado abaixo:

```yaml
SNSErrorExecutionConfig:
    Type : AWS::SSM::Parameter
    Properties:
      Description: Arn of SNS
      Name: !Sub /Supervisorio/${Environment}/Config/SNSErrorExecution
      Type: String
      Value: !Sub SNSErrorExecutionArn=${SNSErrorExecution}
      Tags:
        product: revenue_management
        project: sirius
        module: supervisorio
```

* **Type: AWS::SSM::Parameter:** Define o tipo de recurso como um parâmetro no AWS Systems Manager (SSM).
* **Properties:** Configurações específicas para o parâmetro:
  * **Description:** Uma descrição breve do parâmetro, indicando que ele armazena o ARN do Tópico SNS associado aos erros de execução.
  * **Name:** O nome hierárquico do parâmetro, composto pelo caminho `/Supervisorio/${Environment}/Config/SNSErrorExecution`. O `${Environment}` é uma variável que será substituída dinamicamente com o valor do ambiente (prod ou dev).
  * **Type:** O tipo de dado do parâmetro (String neste caso).
  * **Value:** O valor do parâmetro, que é um ARN de tópico SNS obtido da variável `SNSErrorExecution`.
  * **Tags:** Tags associadas ao parâmetro para fins de organização e identificação.

# Permissões e Políticas

## Implementação No Sirius

## Implementação no DataLake