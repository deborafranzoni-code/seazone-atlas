<!-- title: Ferramentas do Cluster | url: https://outline.seazone.com.br/doc/ferramentas-do-cluster-2b0IsrcoaU | area: Tecnologia -->

# Ferramentas do Cluster

Para fazer o deploy no cluster utlizamos o helm, terraform e o terragrunt.


Atualmente estas são as ferramentas que temos no cluster:



| Chart | Provider | Version | Namespace | NodeClass |
|----|----|----|----|----|
| grafana | grafana | 11.1.5 | monitoring | monitoring |
| loki-distributed | grafana | 2.9.10 | monitoring | monitoring |
| kube-prometheus-stack | prometheus-community | v0.78.1 | monitoring | monitoring |
| tempo-distributed | grafana | 2.6.0 | monitoring | monitoring |
| promtail | grafana | 3.0.0 | monitoring | monitoring |
| grafana-mimir | grafana | 2.14.0 | monitoring | monitoring |
| opentelemetry-collector | grafana | 0.110.0 | monitoring | monitoring |
| traefik | traefik | v3.2.0 | traefik | aws auto-scaling |
| karpenter | karpenter | 0.37.0 | karpenter | aws auto-scaling |
| metabase | metabase | v0.49.12 | tools | tools |
| opensearch-operator | opensearch | 2.7.0 | tools | tools |
| outline | outline | - | tools | tools |
| reservas | seazone | 1.0.0 | apps | apps |
| wallet | seazone | 1.0.0 | apps | apps |
| wallet-bff | seazone | 1.0.0 | apps | apps |


---

## Como fazer alterações nas ferramentas do cluster:

### Requisitos para alterar:

* Helm
* Terraform
* Terragrunt


### Validar o values.yaml: 

Para alterar as configurações dos helms você precisa utilizar o values.yaml da ferramenta que irá alterar que esta no repositório [terraform](https://github.com/seazone-tech/terraform). Após clonar o repositório, execute o commando diff para validar que as informações do values.yaml estão iguais ao que esta no cluster.


 ![](/api/attachments.redirect?id=f14e70dc-b3df-434b-8164-dd3ca85950eb)

Caso o retorno seja nulo, as informações do values.yaml estão identicas no cluster e você pode seguir para alterações com segurança. Se o retorno for as diferenças entre o values.yaml e o que esta presente no cluster, altere o seu values.yaml e siga com as alterações.



:::warning
É muito importante manter o values.yaml sempre fiel ao que esta aplicado no cluster. Ele irá ajudar a manter a organização e funcionamento do fluxo de trabalho do time. Por isso sempre faça o commit das alterações para o github 

:::


### Aplicar as configurações: 

Após alterar as informações necessárias no values.yaml, você pode executar os comandos citados no readme que utilizam o makefile para automatizar os processos. Exemplo do uso do makefile do loki de produção:


O comando a seguir irá aplicar o terraform e listar os pods de monitoramento:

```bash
make applyTerraform
```


Após listar as alterações do terraform o terminal irá perguntar se pode seguir com a alteração e após digitar yes irá aplicar.


 ![](/api/attachments.redirect?id=a1217291-5056-4957-80ee-a97514d5c1a8)

Finalizado o processo, o terragrunt irá armezenar o estado do terraform no bucket s3 appversion-control-production (ou appversion-control-staging)

 ![](/api/attachments.redirect?id=05f6bfcc-c166-47fe-ad41-bd37ec516dd7)



:::info
Minha sugestão é trabalhar somente com o helm até concluir o processo e validar que a alterações estão corretas, pois o terraform pode ser um pouco mais demorado para aplicar e tambḿe não mostra algumas informações. De qualquer forma aplicar o terraform no final do processo é imprescindível para manter o controle e organização das ferramentas no cluster 

:::