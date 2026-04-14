<!-- title: Ring | url: https://outline.seazone.com.br/doc/ring-BBheaVdT0J | area: Tecnologia -->

# Ring

## O que é um Hash Ring na Stack Grafana?

Na **Stack Grafana** um **hash ring** é um mecanismo de **hashing consistente** usado para **distribuir o trabalho entre vários nós**. Ele garante alta disponibilidade, escalabilidade e tolerância a falhas em um sistema distribuído.

No contexto da Stack Grafana, o hash ring é frequentemente utilizado no **Grafana Agent**, **Loki (logs)**, **Tempo (traces)** e **Cortex (métricas)** para:


1. **Distribuir dados ou requisições entre diferentes nós ou réplicas**.
2. **Minimizar o impacto quando novos nós são adicionados ou removidos**.
3. **Evitar perda de dados e reduzir a sobrecarga de consultas em um único nó**.


## Problema Que Tivemos Com O Ring

Caso haja algum problema dentro do ring, seja uma pod não respondendo o healtcheck ou uma instância com inconsistência, o ring não funciona até que ele seja resolvido.


### Too many unhealthy instances in the Ring

Este erro se trata exatamente do ponto onde o ring esta sendo executado com muitas instâncias que não respondem o healtcheck, gerando assim uma parada repentina do envio de métricas recebidas pelo distributor. Neste caso há inúmeras possibilidades que possam ter deixada este pod unhealthy, porém na maior parte das vezes na nossa experiência com esta ferramenta as opções eram:


1. Estouro de memória, com um alto número de requests
2. Pod sendo realocado em outra máquina
3. Pod reiniciando ou indisponível por node estar quebrado (Muitas vezes por conta de alto consumo de ingester do tempo,mimir e loki)


 ![](/api/attachments.redirect?id=d3341b73-5d9c-4f4e-b588-af0fa4e0a63e)

As soluções para resolver este problema de instâncias no ring foram:


* Alterar configurações padrão do ring
  * \

| Configuração | Descrição | default | Alteração |
|----|----|----|----|
| left_ingesters_timeout | Tempo para manter ingesters mortos no ring | 5m | 0s |
| leave_timeout | Tempo para manter ingester marcados como leave | 5s | 0s |
| heartbeat_period | Tempo para fazer o healtcheck | 15s | 5s |
| heartbeat_timeout | Tempo limite para executar um healtcheck | 1m | 15s |

    \
  * As opções default faziam com que o pod não saudável tivesse tempo suficiente para ficar saudável novamente e responder um healthcheck assim mantendo o ciclo onde a aplicação ficava morrendo e consequentemente parando o ring até ser consertada.
* Aumentar os recursos alocados para os pods mais críticos
  * Neste workload de monitoramento alguns pods requerem um número maior de recursos do que o padrão sugerido pela stack.
    * \

| Deployment | Quantidade de Pods | Cpu Req | Mem Req | Cpu Limit | Mem Limit |
|----|----|----|----|----|----|
| Grafana-mimir-ingester | 6 | 200m | 2000Mi | 500m | 3000Mi |
| Grafana-mimir-compactor | 2 | 100m | 512Mi | - | - |
| loki-ingester | 4 | 200m | 1400Mi | 600m | 2000Mi |
| loki-querier | 4 | 250m | 1500Mi | 400m | 2000Mi |
| loki-compactor | 1 | 200m | 1400Mi | 600m | 2000Mi |
| Grafana-tempo-ingester | 6 | 100m | 1G | 350m | 8G |
| Grafana-tempo-metrics-generator | 3 | 100m | 510Mi | 400m | 800Mi |
| Grafana-tempo-compactor | 1 | 100m | 500Mi | 600m | 1400Mi |
| Grafana-tempo-querier | 4 | 100m | 500Mi | 600m | 1400Mi |
| Grafana-tempo-querier-frontend | 3 | 100m | 500Mi | 100m | 1000Mi |
  * Após estas alterações, o número de reinicializações e estouro de memória diminuiram drásticamente.
* Escalar o workload verticalmente
  * Anteriormente tinhamos um total de 13 máquinas com configurações de 4 cpu e 8 de memória, porém com o aumento do uso do workload de monitoramento e o número crescente de crashs por conta de memória a configuração definida foi manter os 4 de cpu porém com 32 GB de memória e totalizando 4 máquinas. Esta opção não só aumenta o número de Gb de memória, que era o problema inicial, mas também diminui consideravelmente o workload processado, haja visto que para cada node há uma média de 7 pods, dos quais não criam mais dados que precisam ser metrificados.
* Labels


\