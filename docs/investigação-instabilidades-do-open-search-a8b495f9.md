<!-- title: Investigação instabilidades do Open Search | url: https://outline.seazone.com.br/doc/investigacao-instabilidades-do-open-search-odGC9vKULE | area: Tecnologia -->

# Investigação instabilidades do Open Search

> **Relacionado a tarefa**: <https://seazone.atlassian.net/browse/SZRDEV-1062>

## Descrição do problema

***Recapitulando os problemas ocorridos….***


### **Problema #1**:**A Busca para de funcionar, não exibindo nenhum imóvel no site**

***Início em: 8 jan \~13h***\nA Busca havia para de funcionar, não exibindo nenhum imóvel no site, no entanto, a busca por destino funcionava.

A causa foi que estavam ocorrendo problemas de Timeout tanto na indexação quanto nas buscas que envolviam o OpenSearch. Mais especificamente na indexação/busca no index de Properties.

A causa raiz do problema inicialmente foi devido as máquinas onde estava a réplica que continha dados do index de propriedades ter caído, logo, as requisições falhavam. 

Isso foi corrigido ao replicar os indexes em mais réplicas (5 para cada indice) para que assim, caso um node caíssem, houvesse outra réplica com os dados daquele index pronto para responder. Essa solução foi baseada nessa documentação: <https://opensearch.org/blog/optimize-opensearch-index-shard-size/>

> `index.number_of_replicas` *(Integer): The number of replica shards each primary shard should have. For example, if you have 4 primary shards and set index.number_of_replicas to 3, the index has 12 replica shards. If not set, defaults to* `cluster.default_number_of_replicas` *(which is 1 by default).*\n**Fonte:** <https://opensearch.org/docs/latest/install-and-configure/configuring-opensearch/index-settings/#dynamic-index-level-index-settings>

 ![campo "number_of_replicas" alterado para 5 em cada um dos indices.](/api/attachments.redirect?id=fdef8a36-af0e-4fd6-bfac-b6e94957f589)


### Problema #2: **Novos erros de Timeout voltam ocorrer.**

**Novos erros de Timeout voltam ocorrer.** Mas não temos muitos detalhes pois foi resolvido em reunião entre as 23h até \~3h da madrugada do dia seguinte.\nA informação que tínhamos era que o index ficou unhealthy (yellow), porém as máquinas pareciam estar UP

 ![Uma das instâncias vai para para o status de "yellow"](/api/attachments.redirect?id=477c8a8b-cdfe-4ebf-8d3e-e74830e19453) ![Aparentemente as máquinas estavam "UP"](/api/attachments.redirect?id=7ed55ec7-95ed-44a3-b19d-bf812df7ae67)


\
### Problema #3: **Erros de** `upstream request timeout`

**Início em: 15 jan 13h40** \n**Erros de** `upstream request timeout` **começaram aparecer no site.** Ambas as aplicações (front e back) haviam caído e voltaram simultaneamente.

 ![Erro exibidos aos usuários "Upstream request timeout"](/api/attachments.redirect?id=33874419-adb3-4f13-b5f4-fdec135b1524)


1. Na investigação realizada pelo time junto com o time de governança, havia sido descoberto que houve uma **instabilidade de infra** que derrubou algumas máquinas e levou alguns minutos até as máquina subirem novamente.
2. A correção foi dada pelo time de governança que implementou medidas (?quais?) para resolver o problema e evitar que ocorra novamente.


### **Problema #4:** **Imóveis não sincronizando/Indexes desatualizados.**

**Início em: 15 jan 19h50**\nFoi  percebido que os imóveis buscado no site e/ou presente na home, ao buscar sem datas possuíam datas inválidas(indisponíveis), ou seja, os dados que estavam nos indexes do opensearch não estavam sendo corretamente atualizados pelo worker.


1. Ao investigar, foi visto que as tasks responsáveis pela atualização não estavam sendo executadas.
2. Ao investigar os webhooks da stays, foi visto que havia um erro na stays (na configuração do webhook) dizendo que havia erro de timeout ao enviar os eventos.![Erros de timeout exibidos nas configurações de webhooks da Stays](/api/attachments.redirect?id=9cde35fe-b112-4ea5-b62d-8b4e8afc63f7 " =549x335")
3. Logo, foi identificado que a causa da desatualização/dessincronização foi que paramos de receber os webhooks stays devido uma instabilidade que houve na API **(item 3)**, logo, a desatualização do OpenSearch foi uma consequência, não a causa dos problemas das buscas desatualizadas ou "falhas" de atualização.

   > Essa dessincronização da disponibilidade também gerou como consequência um bug no front em que não estava tratando corretamente a situação em que as datas não estavam disponíveis, por isso era exibida a tela preta com a mensagem **"**`upstream request timeout`**"**
4. A resolução se deu por criar um webhook temporário e comunicar o time da stays para reestabelecer o envio dos webhooks pelas credenciais "oficias). Isso voltou a atualizar os dados no opensearch sempre  que fosse recebido o webhook.\nAlém disso, também rodamos o sync manual para atualizar todos os imóveis.


## Investigação

Após recapitular os acontecimentos recentes de instabilidades, vimos que a principal causa e que está correlacionada foi a configuração de infra do cluster do OpenSearch, onde após a correção, o serviço foi reestabelecido. Onde a principal causa inicial (do primeiro incidente) foi devido a uma configuração faltante para replicar os dados em mais nodes para manter a disponibilidade do OpenSearch caso algum node/máquina caísse.


#### **Nosso tamanho/volume atual**

Atualmente somos muito pequenos (em relação a quantidade de dados) para ter problemas com relação a falta de storage ou pouca quantidade de `shards`, onde de acordo com a documentação:

> "By default, OpenSearch creates a *replica* shard for each *primary* shard. If you split your index into ten shards, for example, OpenSearch also creates ten replica shards. These replica shards act as backups in the event of a node failure—OpenSearch distributes replica shards to different nodes than their corresponding primary shards—but **they also improve the speed and rate** at which the cluster can process search requests. You might specify more than one replica per index for a search-heavy workload."
>
> \[…\]
>
> "**More shards is not necessarily better**. Splitting a 400 GB index into 1,000 shards, for example, would place needless strain on your cluster. A good rule of thumb is to keep shard size between 10–50 GB."\n***Fonte: ****<https://opensearch.org/docs/2.4/intro/#primary-and-replica-shards>*

Logo, se uma boa regra é manter os shards com tamanho entre 10-50GB (que também é afimado **[nesse blog post](https://opensearch.org/blog/optimize-opensearch-index-shard-size/#:\~:text=degrade%20OpenSearch%20performance.-,Ideal%20shard%20size(s),-OpenSearch%20indexes%20have)**) nosso tamanho é irrelevante para aplicar essa alteração, que em casos de grandes volumes dados, ajuda a processar de forma mais distribuída e manter a disponibilidade dos dados. No entanto, podemos pensar que assim podemos dividir nossos 3GB em mais shards, porém, é afirmado no blog post do OpenSearch que *"If you have too many small shards, you can exhaust memory storing metadata unnecessarily." (**[blog post opensearch](https://opensearch.org/blog/optimize-opensearch-index-shard-size/#:\~:text=degrade%20OpenSearch%20performance.-,Ideal%20shard%20size(s),-OpenSearch%20indexes%20have)**)*, logo, não é uma boa prática fazer isso também.


#### Mudanças recentes

Recentemente tivemos a ativação do fluxo de sincronização de Preço e Disponibilidade com o Google Hotels, o que aumentou a quantidade de requisições ao OpenSearch, onde no mínimo há **5-6 req/imovel para todos os imóveis ativos a cada 30min**. \nEssas requisições utilizam o endpoint `GET properties/_doc/{property_id` para obter algumas as informações daquele imóvel relacionada a disponibilidade e preço.

*TODO: Add gráfico aqui com a quantidade de requests a documentos*

*TODO: Add gráfico aqui com a quantidade de requests totais (incluindo post, put, get, search, )*


### Investigações adicionais

#### Erros de Conexão

Foi visto algumas vezes nos logs ocorrem erros de timeout ao tentar obter algum dado do OpenSearch devido a perda de conexão com o cluster. Abaixo estão alguns logs que mostram: 

```bash
requests.exceptions.ConnectionError: HTTPSConnectionPool(host='reservas.tools.svc.cluster.local', port=9200): Max retries exceeded with url: /properties/_doc/1559?_source_includes=_availability%2Cstatus%2Cguests_included%2Ccode (Caused by NewConnectionError('<urllib3.connection.HTTPSConnection object at 0x7f969ae210c0>: Failed to establish a new connection: [Errno -3] Lookup timed out'))
```

```bash
[2025-01-21 17:36:17,715: WARNING/MainProcess] GET https://reservas.tools.svc.cluster.local:9200/properties/_doc/1559?_source_includes=_availability%2Cstatus%2Cguests_included%2Ccode [status:N/A request:6.307s]
raise EAI_EAGAIN_ERROR
dns.resolver.LifetimeTimeout: The resolution lifetime expired after 5.160 seconds: Server Do53:10.0.0.10@53 answered The DNS operation timed out.
```

Olhando por cima, talvez em alguns momentos parece haver instabilidade no DNS interno onde o worker não conseguiu resposta do OpenSearch.


#### **Rejeição e repasse de request quando um node está sobrecarregado**

O OpenSearch possui várias features que tratam falhas. Lendo a doc encontrei essa **[Shard indexing backpressure](https://opensearch.org/docs/2.3/tuning-your-cluster/availability-and-recovery/shard-indexing-backpressure/)** que ativa um mecanismo que caso durante a indexação um node esteja sobrecarregado, ele rejeita e manda aquela requisição para um node que esteja mais tranquilo. Isso geralmente só é ativado quando o cluster está praticamente sem recursos (há parametros que ditam o "quando"), de acordo com a documentação.


#### **Carga de webhooks recebidos da stays (trigga indexação)**

TODO: add gráfico request ao endpoint `POST /stays/event` ultimos 30d

Vemos pelo gráfico de requests abaixo recebidos de webhooks da Stays, que na maior parte do tempo a quantidade de requests recebidos se manteve. Com exceção entre os dias 08 e 09 onde teve o dobro no aumento de webhooks, porém foi normalizado.

> Verificar o que houve de diferente nesse dia de diferente para o aumento. (

 ![](/api/attachments.redirect?id=184248ac-c819-4072-950d-4a5ea152250f)

#### Carga de leitura ao OpenSearch (search/get)

TODO: add gráfico request de buscas (search) ultimos 30d

 ![opensearch_index_get_count](/api/attachments.redirect?id=e763d427-464e-44e9-a27e-64d1ec111d1b)


#### Carga de escrita ao OpenSearch (indexação)

TODO: add gráfico request de indexações (PUT) ultimos 30d

 ![](/api/attachments.redirect?id=72a89330-8615-4fee-af93-f61d1b9ddf09)


#### Uso de recursos (percents)

**Memória RAM (OS)**


 ![](/api/attachments.redirect?id=9bc0e2fd-bb8f-483f-af41-dc0d5c01d7da)

*\* necessário entender se esse gráfico está na escala de 0-1 ou 0-100*


**Memória Heap**

 ![Source: https://grafana.seazone.com.br/d/22932e75-beee-42e7-b13f-2551ede7c0f2/opensearch-prometheus-kubernetes?orgId=1&from=now-30d&to=now](/api/attachments.redirect?id=477810b8-6a34-42ab-aafa-c1f9e7aa11c9)


**CPU\***

O uso de CPU alto de forma constante indica que o Cluster pode estar sub dimensionado.

*\*Seria necessário entender qual das métricas de CPU está correta e em qual* escala está.

 ![Source: https://grafana.seazone.com.br/d/X1WSwkF7k/opensearch-prometheus?orgId=1&from=now-30d&to=now](/api/attachments.redirect?id=84db6aa2-8711-42ff-bdd7-588f16bc1d9f)

 ![Source: https://grafana.seazone.com.br/d/22932e75-beee-42e7-b13f-2551ede7c0f2/opensearch-prometheus-kubernetes?orgId=1&from=now-30d&to=now](/api/attachments.redirect?id=4efbeb50-beb4-487f-935e-a8c26e908c34)


**Storage**

 ![Source: https://grafana.seazone.com.br/d/22932e75-beee-42e7-b13f-2551ede7c0f2/opensearch-prometheus-kubernetes?orgId=1&from=now-30d&to=now](/api/attachments.redirect?id=707ede64-faa0-442a-a7e2-c6f141fdeea8)


## Melhorias


### Monitoramento

Implementar melhorias no Monitoramento do cluster do OpenSearch para monitorar as principais métricas que mostram a saúde do Cluster e seus Nodes, bem como informações de latência e volume de dados para saber quando e o que escalar.

#### Exemplos de métricas:

* **Cluster Health Metrics**: Verificar saúde do cluster, nodes e shards estão operando como esperado.
* **Indexing Perfomance Metrics**: Métricas para entender a taxa de atualização/adição dos documentos no indice, verificando se a perfomance está degradada.
  * Indexing Rate e Latency (para verificar se está lenta a indexação)
  * Threads quantity para indexação
  * lantecia da rede
* **Search Latency:** a latência das buscas nos mostra quanto tempo que está levando para retornar os resultados das buscas (search)
* **Node Memory Usage:** A memória RAM do servidor que executa o OpenSearch é divida em Heap Memory ou Free Memory (usada pelo sistema operacional para Cache).
  * **Heap memory**: Ficar sem Heap memory é péssimo. Basicamente o OpenSearch irá crashar. 
    * Heap usage percent
    * Heap usage size
  * OS Cache (free memory - Non Heap)
* **Disk Usage:** Se o disco ficar cheio (>=95%), o opensearch ficará apenas read-only
  * Usage percent
  * Disk size and used size
* **CPU Usage:** Se o uso é constantemente alto indica que o Cluster está subestimado (precisa de upgrade)
* **Network latency**: Rede lenta reduz a perfomance
* **Segment merges latency**: latencias altas podem indicar que é necessário mais nodes ou melhora a política de merge.
* **Cache Evictions**: Se ocorre com muita frequência pode ser necessário aumentar a quantidade de cache. Ou fazer as queries usarem melhor os registros em cache.


#### **Sugestões de Alertas**

<https://docs.aws.amazon.com/opensearch-service/latest/developerguide/cloudwatch-alarms.html>


#### Sugestão de Implementação do Plugin **Performance Analyzer**

<https://opensearch.org/docs/latest/monitoring-your-cluster/pa/index/#example-api-query-and-response> 


### [Melhorias de Estabilidade](https://docs.aws.amazon.com/opensearch-service/latest/developerguide/bp.html#bp-stability)

#### Node Manager e Coordinator Dedicados

**Node Manager**

Atualmente, todos os 3 nodes master possuem a Role de Node Manager, porém, de acordo com as boas práticas o ideal é ter um Node Manager dedicado. Colocar essa role nos 3, não necessariamente quer dizer que os 3 serão, mas sim que dentre aqueles 3, um será eligido como Node manager.

Abaixo é explicado o que o Node Manager dedicado ajuda e qual o tamanho de máquina ideal dele baseado no tamanho dos 

> [Dedicated manager nodes](https://docs.aws.amazon.com/opensearch-service/latest/developerguide/managedomains-dedicatedmasternodes.html) improve cluster stability. A dedicated manager node performs cluster management tasks, but doesn't hold index data or respond to client requests. This offloading of cluster management tasks increases the stability of your domain and makes it possible for some [configuration changes](https://docs.aws.amazon.com/opensearch-service/latest/developerguide/managedomains-configuration-changes.html) to happen without downtime.
>
> Enable and use three dedicated manager nodes for optimal domain stability across three Availability Zones. Deploying with [Multi-AZ with Standby](https://docs.aws.amazon.com/opensearch-service/latest/developerguide/managedomains-multiaz.html#managedomains-za-standby) configures three dedicated manager nodes for you. For instance type recommendations, see [Choosing instance types for dedicated manager nodes](https://docs.aws.amazon.com/opensearch-service/latest/developerguide/managedomains-dedicatedmasternodes.html#dedicatedmasternodes-instance).


**Node Coordinator**

Assim como ter um Node Manager, também é interessante ter um Node Coordinator dedicado. O Node Coordinator é basicamente o responsável por rotear as requisições entre os nodes, ajudando a utilizar de forma eficiente os recursos melhorando o througput e perfomance de queries


**Sources:** 

* **<https://docs.aws.amazon.com/opensearch-service/latest/developerguide/Dedicated-coordinator-nodes.html>**
* <https://opensearch.org/docs/latest/getting-started/intro/#clusters-and-nodes>
* <https://opensearch.org/docs/latest/tuning-your-cluster/>


#### Verificar dimensionamento da máquina

**CPU/Mem**

Na documentação menciona que: 

> `r6g.large` *instances are an option for small production workloads (both as data nodes and as dedicated manager nodes).*

Logo, precisamos verificar se estamos atendendo os requisitos para rodar o OpenSearch para um ambiente de produção.


**Storage**

Além disso, há uma recomendação de utilizar armazenamento **gp3** que é o tipo de armazenamento mais recente da Amazon.


#### **Control ingest flow and buffering (a nível de código)**

Uma boa prática é utilizar um **_bulk** update ao invés de atualizar os documentos de 1 em 1. Envia um bulk com 5k de documentos, é melhor que 5k de requests atualizando um único documento por vez.

Podemos estudar como fazer essa melhoria em nosso código atual, onde possamos gerar batches de até 1000 docs, por exemplo.

> **Sources:**
>
> * <https://opensearch.org/docs/latest/getting-started/ingest-data/#bulk-indexing>
>
>
> * <https://opensearch.org/docs/latest/api-reference/document-apis/bulk/>


#### Eliminar dados desnecessários **(a nível de código)**

Evitar inserir documentos que não serão utilizados, como imóveis inativos, em draft ou ocultos. Isso vai diminuir o uso de storage além de não desperdiçar trabalho atua.

Além disso, é interessante remover do OpenSearch todos aqueles documentos/indices que não são mais utilizados.


## Conclusões

Em resumo nós ainda estamos MUITO pequenos para ter problemas de escalabilidade. Nas pesquisas realizadas, os problemas de escalabilidade começam aparecer quando possuímos vários GB de dados e Milhões de requisições.


Também há uma dificuldade ainda em conseguir puxar os dados de monitoramento do cluster do OpenSearch, onde está complicado de entender o que é cada métrica (e encontrar as que queremos) e em qual escala ela está. Exemplos: CPU, RAM Mem, Heap Mem, Cache Mem, Requests Rate e Lantência (Searches e Get single doc), Indexing Rate e Lantência.

Acredito que primeiro precisamos melhorar o monitoramento para entender melhor como está a saúde do cluster do opensearch, para que então possamos tomar ações para otimizar ele.

No entanto, há itens a nível de infra que seria interessante revisar, como: 

* Dimensionamento da máquina, verificando se está adequado com base no histórico de uso dos recursos (cpu, memória(os, heap), storage, network). *Verificar o nível de uso de recursos por Node também.*
* Dividir melhor a responsabilidade entre os nodes, definindo quem é o Node Manager e quem é o Node Coordinator, deixando eles especificamente para isso, e os demais Nodes, apenas como Data Nodes.


Além desses pontos, a nível de código podemos estudar melhorias no processo de indexação, como:

* Realizar _bulk update, atualizando vários documentos de uma vez, ao invés de realizar uma requisição para cada documento.
* Utilizar compressão nas requisições.
* Eliminar dos indices documentos inutilizados.