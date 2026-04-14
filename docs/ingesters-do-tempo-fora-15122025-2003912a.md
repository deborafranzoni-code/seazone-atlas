<!-- title: Ingesters do tempo fora 15/12/2025 | url: https://outline.seazone.com.br/doc/ingesters-do-tempo-fora-15122025-scS7rtldkM | area: Tecnologia -->

# Ingesters do tempo fora 15/12/2025

# Relatório Técnico: Correção de Ingesters UNHEALTHY no Tempo

 ![](/api/attachments.redirect?id=37056d89-6049-490f-9d78-57b8f9874c91 " =1041x124")

Log encontrado : 

```javascript
found an existing instance(s) with a problem in the ring, this instance cannot become ready until this problem is resolved. The /ring http endpoint on the distributor (or single binary) provides visibility into the ring." ring=ingester err="instance 10.0.24.12:9095 past heartbeat timeout"
```

**Objetivo:** Restabelecer a operação normal do cluster Tempo removendo manualmente instâncias de ingester bloqueadas no estado `UNHEALTHY` do **ring** (anel de descoberta de serviços).

## Situação Inicial e Problema

O cluster apresentava instâncias de **ingester** (componente responsável por receber e armazenar temporariamente os traces) marcadas como `UNHEALTHY` no **ring**. O ring é um mecanismo de consenso distribuído (baseado em hash consistente) que todos os componentes do Tempo (Distributor, Ingester, Querier) consultam para saber onde os dados estão e para quem encaminhar novas escritas.

Quando um ingester fica `UNHEALTHY`, ele para de receber dados, mas seus **tokens** (posições virtuais no anel que determinam quais dados ele gerencia) não são liberados. Isso cria um bloqueio: o sistema não escreve naquela partição de dados, prejudicando a ingestão.

## Ação Corretiva Executada

A correção foi realizada através de uma intervenção manual na API de administração do ring, contornando a indisponibilidade da UI.


1. **Acesso à API do Ring:** Foi criado um Pod temporário com `curl` para acessar diretamente o endpoint interno do **distributor** (componente que recebe as escritas e as encaminha para os ingesters corretos).
   * **Comando:** `curl -H "Accept: application/json" http://tempo-distributor.monitoring.svc.cluster.local:3200/ingester/ring`
   * **Significado:** Este comando `GET` buscou o estado atual do ring de ingesters no formato JSON, listando todos os membros e seus estados (`ACTIVE`, `UNHEALTHY`, `PENDING`).
2. **Identificação dos Nós Problemáticos:** A saída JSON foi filtrada para localizar as entradas onde `"state": "UNHEALTHY"` e extrair seus IDs únicos (ex: `tempo-ingester-1:9095`).
3. **Remoção Manual do Ring (Forget):** Para cada ID identificado, foi enviado um comando de `forget` via `HTTP POST` para a mesma API.
   * **Comando:** `curl -X POST "http://.../ingester/ring?forget=tempo-ingester-1:9095"`
   * **Significado:** Este é o comando administrativo crucial. A operação `forget` remove a instância defeituosa do mapa do ring. Como consequência principal, os **tokens** que ela detinha são imediatamente redistribuídos entre as instâncias `ACTIVE` restantes. Isso desbloqueia a partição de dados e permite que o cluster opere normalmente, mesmo que a instância física ainda esteia inicializando.


## Ação preventiva 

O evento ocorreu novamente e, ao investigar, observamos que o ingester apresenta picos de memória constantes, frequentemente ultrapassando o valor requested de forma abrupta. Minha hipótese é que, embora o componente consiga iniciar com a quantidade de memória alocada atualmente, ele não consegue escalar a tempo de atender à demanda de recursos.

Acredito que a memória alocada (request) não seja suficiente durante os picos, e, nesses momentos, os pods, embora não falhem, ficam intermitentes, o que provavelmente está gerando o estado "unhealthy" no ring. As ações que tomei incluem aumentar ligeiramente a memória request e ajustar o HPA para torná-lo mais sensível e ágil ao detectar o aumento do uso de memória. A ideia é que o scaling ocorra rapidamente para evitar falhas.

 ![](/api/attachments.redirect?id=0f166251-161b-4e50-90b0-363360d241c8 " =1390x519")

## Resultado

A intervenção forçou a reconciliação do estado do ring com o estado real da infraestrutura. Após o `forget`, os Pods de ingester subjacentes (gerenciados pelo Kubernetes) puderam completar seu ciclo de reinicialização e se registrar novamente no ring como instâncias novas e saudáveis (`ACTIVE`), restaurando a capacidade total de ingestão do cluster. A ação corrigiu o **sintoma** (ring inconsistente), enquanto o Kubernetes tratou da **causa** (recuperação do contêiner).

**Observação :** Não conseguimos encontrar a real causa dessas instâncias serem marcadas como unhealthy, geralmente isso está relacionado a quebrar por recursos, mas fazendo algumas querys ali que trazem dados de uso do próprio componenente do ingester não consegui localizar um pico que chegasse a ponto de derrubar algum pod por recursos

```promql
sum by(pod) (
  process_resident_memory_bytes{namespace="monitoring", service="tempo-ingester"}
)
```

```promql
sum by(pod) (
  rate(
    process_cpu_seconds_total{namespace="monitoring", service="tempo-ingester"}[5m]
  )
)
```

## Ações

* Alertas de recursos para pods dos ingesters (quando bater 90% de memória || CPU)
* Alertas para quando recebermos logs apontando algum ingester como unhealthy 
* ```javascript
  found an existing instance(s) with a problem in the ring, this instance cannot become ready until this problem is resolved. The /ring http endpoint on the distributor (or single binary) provides visibility into the ring." ring=ingester err="instance 10.0.24.12:9095 past heartbeat timeout"
  ```