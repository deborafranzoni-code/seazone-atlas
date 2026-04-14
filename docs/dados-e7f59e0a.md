<!-- title: Dados | url: https://outline.seazone.com.br/doc/dados-869NEGUgbP | area: Tecnologia -->

# Dados

Como são calculados os dados visualizados no Finops BI 

# AWS

## BUs

como estão sendo agregados os custos de BU na aws

## **Dados**

os custos agregados a essa BU são todos os custos advindos das contas abaixo que são as contas de dados 

* **aws-dev-sirius -** 234310247306
* **DEV-lake -** 568454860761
* **PRD - Data Backup -** 999971636885
* **PRD - Sirius -** 835316524622
* **PRD-Lake -** 011528361483
* **Seazone Technology -** 452791833956

em teoria hoje só deveriam haver recursos de dados nessas contas por isso é feito dessa forma 

obs : o objetivo é que futuramente possamos usar tags para mapear esses recursos assim como fazemos para web, foi feito dessa foma para acelerar o processo e termos alguma visualização dos dados 


## Comercial

* custo vindos da tag szn-bu:comercial no cost categories 
* custo vindos de recursos com a label BU:comercial no cluster kubernetes
* 25% dos valores compartilhados da conta `Applications`,  esses valores compartilhados incluem principalmente recursos que são usados por várias aplicações como o monitoramento e o metabase por exemplo

## Hospedagem

* custo vindos da tag szn-bu:hospedagem no cost categories 
* custo vindos de recursos com a label BU:hospedagem no cluster kubernetes
* 25% dos valores compartilhados da conta `Applications`,  esses valores compartilhados incluem principalmente recursos que são usados por várias aplicações como o monitoramento e o metabase por exemplo

## Reservas

* custo vindos da tag szn-bu:reservas no cost categories 
* custo vindos de recursos com a label BU:reservas no cluster kubernetes
* 25% dos valores compartilhados da conta `Applications`,  esses valores compartilhados incluem principalmente recursos que são usados por várias aplicações como o monitoramento e o metabase por exemplo

## Spots

* custo vindos da tag szn-bu:spots no cost categories 
* custo vindos de recursos com a label BU:spots no cluster kubernetes
* 25% dos valores compartilhados da conta `Applications`,  esses valores compartilhados incluem principalmente recursos que são usados por várias aplicações como o monitoramento e o metabase por exemplo

## Nekt

* Todo custo vindo da conta `nekt` (756554055315)

## Shared

Aqui basicamente estão os custos que são divididos por todos os recursos nas contas, como taxas e contas obrigatórias da AWS como de auditoria por exemplo, contas que compõe esses custos compartilhados : 

esses custos são somados e divididos de forma igualitária por todas as BUs entendendo que esses custos são compartilhados por todos os recursos da nossa cloud 

* **Sandbox** - 281246853146
* **Audit** - 591779690709
* **Log Archive** - 929403384210
* **seazone-commitments-sp** - 158832054336
* **seazone-commitments-cache** - 402360042716
* **Seazone-Manager** - 834181448060
* **seazone-commitments-rds** - 474876694828
* **seazone-commitments-sp2** - 800261073940
* **dotted-026090552812-sp** - 026090552812