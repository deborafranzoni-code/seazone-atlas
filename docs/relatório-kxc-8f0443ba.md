<!-- title: Relatório KXC | url: https://outline.seazone.com.br/doc/relatorio-kxc-UUUS2uCnvC | area: Tecnologia -->

# Relatório KXC

Devolutiva baseado nos pontos levantados pela KXC nesse documento : 

[https://docs.google.com/spreadsheets/d/1rzuUanjshSufgDbcvUV0JiRTGCJFgKx-kbh9KLUD0KI/edit?gid=818397319#gid=818397319](https://docs.google.com/spreadsheets/d/1rzuUanjshSufgDbcvUV0JiRTGCJFgKx-kbh9KLUD0KI/edit?gid=818397319#gid=818397319)


### Verificar a necessidade de ter mais de 1 NAT Gateway em São Paulo

O objetivo de ter dois NATs é seguir a recomendação de resiliência da AWS é garantir que, se houver a indisponibilidade do NAT em alguma AZ, nem todo tráfego de saída será comprometido. Como descobrimos que os custos altos de NAT tem mais relação com a sincronização do Google, manteria os dois.

<https://docs.aws.amazon.com/pt_br/vpc/latest/userguide/nat-gateway-scenarios.html?utm_source=chatgpt.com#private-nat-overlapping-networks>


### Verificar a necessidade de ter mais de 1 NAT Gateway em Oregon

Percebi que ainda tínhamos o NAT da VPC de Oregon funcionando. Não temos nenhum motivo para mantê-lo, então procedi com a remoção.

 ![](/api/attachments.redirect?id=2193f2b3-cc0f-40ea-ad39-9cbee77f8f62 " =1027x97")


### Atualizar instâncias T2 para T3 ou T4G 

instâncias encontradas (aproveitei também pra trazer t3 que poderiam ser t3a ou t4g) : 

| Nome (ID) | Conta  | Descrição |
|----|----|----|
| bastion([i-08cf3d9c12b8c3eeb](https://sa-east-1.console.aws.amazon.com/ec2/home?region=sa-east-1#InstanceDetails:instanceId=i-08cf3d9c12b8c3eeb)) | Applications | Máquina do bastion utilizado para acessar as máquinas  |
| Khanto PowerBI Cluster([i-07af5380b1e66a656](https://us-west-2.console.aws.amazon.com/ec2/home?region=us-west-2#InstanceDetails:instanceId=i-07af5380b1e66a656)) | Seazone Technology | máquina onde está o gateway do powerBI |
| KhantoBi-0([i-0e3bad243c5a106e7](https://us-west-2.console.aws.amazon.com/ec2/home?region=us-west-2#InstanceDetails:instanceId=i-0e3bad243c5a106e7)) | Seazone Technology | máquina onde está o gateway do powerBI (sim temos duas, é uma espécia de cluster) |

**Cards para atualização dos BIs criado, entendendo que pode não ser tão trivial, o bastion será adicionado como pendência a ser feita :** 

* Máquinas do BI - <https://seazone.atlassian.net/browse/GOV-3814>


### Atualizar todos os discos para gp3 

* Identifiquei volumes EBS do tipo **gp2** na conta de *applications* na região de Oregon, remanescentes da migração. Considerando que não há justificativa para mantê-los ativos, procedi com a remoção de todos. 
* obs: removi os gp3 de lá também entendendo que só precisamos do que está em São Paulo![](/api/attachments.redirect?id=5b4daa69-29a9-43fb-b92e-0285a6e21597 " =1089x345")
* encontrado GP2 na conta PRD-Lake com o id [vol-010bdb2ca06cfe90e](https://us-west-2.console.aws.amazon.com/ec2/home?region=us-west-2#VolumeDetails:volumeId=vol-010bdb2ca06cfe90e) 

### Verificar possibilidade de utilizar outros níveis de armazenamento no S3

Este é um pouco mais complexo. Acredito que seria necessário realizar uma análise dos dados armazenados no bucket ou, até mesmo, avaliar se vale a pena ativar alguma ferramenta para isso, como o [AWS S3 Storage Lens](https://aws.amazon.com/s3/storage-lens/).

### Compreender o que gera custo de data transfer 

Já foi resolvido, identificamos que está relacionado com um sync que fazemos com o google hotels, diminuimos a frequência do sync e estamos analisando se faz sentido manter essa OTA 

### Verificar as configurações e cobertura de savings plans

Acho que isso realmente poderia gerar uma economia interessante, principalmente na parte de dados. Porém, me parece ser algo que demanda uma análise mais aprofundada. Vou adicionar como uma pendência para investigação, a fim de avaliar se vale a pena considerar essa opção e, posteriormente, analisar como seriam esses savings plans

### Verificar configurações e uso de IPv4 publicos 

Isso está principalmente relacionado ao workload do time de dados, hoje não temos uma solução pra questão e pelo menos no momento entendemos que é um custo esperado

###  Possibilidades de redução de custos com estratégia de cache no GLUE

A estratégia de cache pode ser uma sugestão para o time de dados

### Verificar a necessidade de uso de RDS Multi-AZ

Pelo que confirmei na nova região não temos bancos multi-AZ 

### Verificar utilização de alertas e logs do Cloudwatch

Realmente, vale a pena investigar para entendermos se precisamos do monitoramento do CloudWatch para nossos recursos. Acredito que, atualmente, utilizamos apenas nos bancos, quando algo inesperado acontece relacionado ao database 

### Atualizar EKS

A versão atual do nosso cluster vai até 28 de julho de 2026, creio que não seja uma prioridade pra o momento 

### Diminuir quantidade de loadbalancers

* Removido loadbalancer de oregon, tinhamos mantido pra comparar com o novo ambiente, agora a remoção foi feita completamente, era o unico loadbalancer pendente, o outro que temos está sendo utilizado pelo cluster de SP ![](/api/attachments.redirect?id=2d928474-857f-4df9-9845-8761290c90a7 " =974x81")

### Investigar uso do quicksight 

Não consegui encontrar onde estão os dois usuários que constaram no billing, talvez ja tenham sido removidos 

### Verificar Hosted Zones do Route53

Atualmente temos 6 hosted zones no Route53 : 

* sapron.com.br
* usealfred.com.br
* reservaseazone.cf
* stagingnextsapron.cf
* local
* seazone-backend-staging-dev

  Entendo que o único que precisamos manter até migramos os cloudfront do sapron é o sapron.com.br, o resto será confirmado com o time e se fizer sentido serão removidos

## Pendências da análise 

- [ ] Atualizar máquina do bastion para t3a || t4g
- [ ] Atualizar volume encontrado na PRD-lake ([vol-010bdb2ca06cfe90e](https://us-west-2.console.aws.amazon.com/ec2/home?region=us-west-2#VolumeDetails:volumeId=vol-010bdb2ca06cfe90e) ) para GP3
- [ ] avaliar se vamos focar em otimização de S3 agora 
- [ ] avaliar possibilidade de compute savings plans para fargate 
- [ ] investigar utilização do cloudwatch 
- [ ] validar uso do quicksight
- [ ] indicar time de dados possibilidades de redução de custos com estratégia de cache no GLUE
- [ ] validar hosted zones na technology
- [x] Remover NAT de oregon na applications