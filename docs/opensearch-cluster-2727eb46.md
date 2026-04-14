<!-- title: Opensearch Cluster | url: https://outline.seazone.com.br/doc/opensearch-cluster-grAqFemp0k | area: Tecnologia -->

# Opensearch Cluster

O opensearch foi instalado com o [operator](https://github.com/opensearch-project/opensearch-k8s-operator) do opensearch disponibilizado pelo próprio [opensearch-project](https://github.com/opensearch-project/opensearch-k8s-operator).

O operator do opensearch facilita o desenvolvimento e implementação dos seus componentes dentro do cluster, uma vez que para implementar cada componente (nodePools) seria necessário fazer o deploy de um novo helm.


Após fazer o deploy do operador a o controle do cluster passa a ser pelo arquivo de configuração yaml do tipo OpenSearchCluster. Exemplos de como utilizar o OpenSearchCluster podem ser encontrados no [link](https://github.com/opensearch-project/opensearch-k8s-operator/blob/main/opensearch-operator/examples/2.x/opensearch-cluster.yaml).

## Nossa Configuração


A configuração de nodePools que utilizamos hoje é constituída em 2 componentes:

| Componente | Role | Replicas | disk size  |
|----|----|----|----|
| Node | data | 3 | 30Gb |
| Master | data/cluster_manager | 3 | 30Gb |


## Configuração de Shard dos Indexes

O número default de indexes é uma primary (read/write) e uma replica (read). Atualmente realizamos alterações nos 2 indexes que o reservas utiliza, o properties e o destinations. Para realizar esta alteração utilizamos os seguintes passos:


:::warning
Para realizar o passo a passo abaixo é necessário realizar um port-forward no service do opensearch. (k port-forward svc/reservas 8003:9200 -n tools)

:::


1. Validar os status do index

   <https://localhost:8003/destinations/_search_shards>![](/api/attachments.redirect?id=be71841b-6379-466e-bd62-4bf81afe6eae)
2. Aplicar alteração no index:

```bash
curl -u admin:admin --location --request PUT 'https://localhost:8003/destinations/_settings' --insecure \         
--header 'Content-Type: application/json' \                                                           
--data '{
  "index" : {
    "number_of_replicas": 5
  }
}'
```