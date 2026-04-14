<!-- title: Custos com EC2 [Dez/2025] | url: https://outline.seazone.com.br/doc/custos-com-ec2-dez2025-7SE1Etyjsp | area: Tecnologia -->

# Custos com EC2 [Dez/2025]

## Problema inicial 

Identificamos um aumento anômalo nos custos relacionados às EC2 Instances a partir de 01 de dezembro. O gráfico mostra claramente a elevação, com a barra azul aumentando significativamente desde essa data. O custo diário médio passou de $10 para cerca de $50, uma variação abrupta de um dia para o outro.

 ![](/api/attachments.redirect?id=a0871fda-ecd7-4323-a9e9-a841ece2b307 " =1251x539")

Inicialmente, suspeitamos que o aumento fosse devido a algum novo workload no nosso cluster, algo que, por algum motivo, estivesse consumindo mais recursos e ativando mais nodes do que o usual. No entanto, ao analisar os dados relacionados aos nodes e recursos no cluster, não encontramos evidências desse pico. ![](/api/attachments.redirect?id=ef85d093-de81-4615-b000-3f441b2cb1b4 " =1159x324")

|  ![](/api/attachments.redirect?id=f20fb113-8724-4d9a-88ea-e820dfe179f7 " =342x95") |  ![](/api/attachments.redirect?id=66fffe75-1e62-47e7-bbc8-54296da00f2c " =342x118")   |
|----|----|


Ao analisar as imagens, é possível notar um aumento, que pode até ser esperado, considerando o crescimento constante de nossas aplicações em diversas áreas. No entanto, esse aumento não justifica um crescimento tão expressivo no uso de máquinas, como apresentado no início deste documento.

Após uma investigação mais detalhada, verificamos que no mês de novembro não houve cobranças relacionadas a EC2 Instances, como se estivéssemos isentos dessa cobrança. Na imagem abaixo, é possível observar que até o dia 30, os custos são exclusivamente relacionados à transferência de dados para fora (transfer out), sem registros de uso de máquinas. A partir do dia 30, as cobranças referentes ao uso das máquinas retornam.   

 ![](/api/attachments.redirect?id=dd3315f6-1f4c-4285-8fb7-4b32fa28b23a " =936x433")


Após investigações e conversas com a Dotted, entendemos que o período sem cobranças relacionadas a máquinas foi devido ao uso de créditos na AWS, os quais foram aplicados no mês de novembro. Isso explica o comportamento do billing, que volta a cobrar pelo uso das máquinas exatamente no primeiro dia de dezembro. ![](/api/attachments.redirect?id=28669bf3-d59b-4120-8207-4f96edf9faab " =936x433")


\
# Custos encontrados :rotating_light:

## Disperdício de Recursos no cluster

Após uma análise dos últimos 30 dias de uso de recursos no cluster e encontramos alguns serviços que estão disperdiçando uma quantidade relevante CPU ou memória, o que provavelmente está ocasionando custos excessivos, vou listá-los abaixo e pontuar os ajustes que podem ser feitos

dados retirados desse [dashboard](https://monitoring.seazone.com.br/d/k8s_views_pods/kubernetes-views-pods?orgId=1&from=2025-11-12T01:56:39.291Z&to=2025-12-12T01:56:39.291Z&timezone=browser&var-datasource=PBFA97CFB590B2093&var-cluster=&var-namespace=stg-apps&var-pod=$__all&var-resolution=30s&var-job=kube-state-metrics&refresh=30s&editPanel=38&viewPanel=panel-38)

**Tools**

| Componente | CPU em uso  | CPU solicitada | Memória em uso | Memória solicitada |
|----|----|----|----|----|
| Metabase | 0.2063 | 4.000 | 9.81 GiB | 8 GiB |

* Desperdício de cerca de 94,84% em relação a CPU,
* Memória em uso acima da memória solicitado, pode estar gerando disperdício visto que o karpenter pode subir mais máquinas que o necessário para lidar com esses 1.8GB que não estão configurados no valor de request 

**Keda**

| Componente | CPU em uso | CPU solicitada | Memória em uso | Memória solicitada |
|----|----|----|----|----|
| **keda-operator-metrics-apiserver** | 0.0086 | 0.2000 | 58.14 MiB | 200.00 MiB |
| **keda-operator** | 0.0037 | 0.2000 | 56.04 MiB | 200.00 MiB |
| **keda-admission-webhooks** | 0.0010 | 0.2000 | 23.65 MiB | 200.00 MiB |

* 95% de disperdício em CPU & 70% de memória no componente  `keda-operator-metrics-apiserver`
* 98% de disperdício em CPU & 71% de memória no componente  `keda-operator`
* 99%  de disperdício em CPU & 88% de memória no componente  `keda-admission-webhooks`

**Monitoramento**

| Componente | CPU em uso | CPU solicitada | Memória em uso | Memória solicitada |
|----|----|----|----|----|
| **metrics-generator** | 0.0148 | 0.4000 | 520.73 MiB | 1.00 GiB |
| **promtail** | 0.3298 | 2.1000 | 1.31 GiB | 1.31 GiB |
| **memcached** | 0.0050 | 1.1000 | 8.16 GiB | 11.05 GiB |
| **exporter** | 0.0073 | 0.0500 | 25.44 MiB | 64.00 MiB |
| **loki** | 0.3699 | 5.0000 | 4.86 GiB | 15.00 GiB |
| **ingester** | 0.0105 | 2.5000 | 934.15 MiB | 5.00 GiB |

* 96,3% de disperdício em CPU &  48% em memória no componente `**metrics-generator**`
* 84% de disperdício em CPU  `**promtail**`
* 99% de disperdício em CPU & 67% em memória no componente  `**loki**`
* 99% de disperdício em CPU & 81% em memória no componente  `**ingester**`

**Stg-Apps**

| Componente | CPU em uso | CPU solicitada | Memória em uso | Memória solicitada |
|----|----|----|----|----|
| opensearch | 0.6510 | 6.0000 | 16.84 GiB | 24.00 GiB |
| reservas-api | 0.0188 | 0.6000 | 574.63 MiB | 900.00 MiB |
| reservas-frontend | 0.2366 | 0.8000 | 601.75 MiB | 800.00 MiB |
| wallet-frontend | 0.0170 | 0.4000 | 212.41 MiB | 400.00 MiB |

* 99% de disperdício de CPU  & 29% de memória no componente `opensearch`
* 96% de disperdício de CPU & 36% de memória no componente `reservas-api`
* 70% de disperdício de CPU & 24% de memória no componente `reservas-frontend`
* 95% de disperdício de CPU &  47% de memória no componente `wallet-frontend`


**Prd-Apps**

| Componente | CPU em uso | CPU solicitada | Memória em uso | Memória solicitada |
|----|----|----|----|----|
| opensearch | 0.1161 | 18.0000 | 44.13 GiB | 72.00 GiB |
| reservas-worker | 0.2828 | 2.4000 | 1.20 GiB | 2.79 GiB |
| wallet-frontend | 0.0730 | 0.8000 | 503.30 MiB | 800.00 MiB |

* 99% de disperdício em CPU & 38% em memória no componente `opensearch`
* 88% de desperdício em CPU  & 56% em memória no componente `reservas-worker`
* 90% de disperdício em CPU & 37% em memória no componente `wallet-frontend`

Os insights levantados acima são grandes indicadores do por que estamos com um custo elevado de EC2 no cluster atual, isso fica ainda mais impactante quando olhamos para o disperdício geral de recursos no cluster nos útlimos 30 dias por exemplo : 

 ![](/api/attachments.redirect?id=9340bc9f-cbe4-4e68-b558-ac1785eabcda " =1339x215")

Ou mesmo pra alguns nodes específios que claramente estão extremamente subutilizados 

 ![](/api/attachments.redirect?id=97cff828-b205-4662-b59b-abfa6bce69a8 " =1348x541")

Na imagem é possível perceber mais de um caso onde há um disperdício de pelo menos 90% da quantidade de recurso disponível no node 

## Recomendações

Com base na análise do documento e nos dados apresentados, o cenário é claro: **o fim dos créditos AWS expôs uma ineficiência estrutural severa no dimensionamento do cluster.** Embora o retorno da cobrança fosse esperado, pagar preço cheio por recursos com 99% de ociosidade é injustificável.

Abaixo estão as recomendações incisivas para estancar o sangramento de custos, divididas por prioridade de impacto financeiro.


---

## 1. Ajuste Crítico de Workloads (Right-Sizing)

O foco aqui é reduzir o **CPU Request**. O Kubernetes reserva a máquina baseada no `Request`, não no uso real. Se você pede 18 vCPUs e usa 0.1, você paga por 18.

### **A. Os "Elefantes" (Maior Impacto Financeiro)**

Estes serviços estão segurando instâncias grandes (`c7g.4xlarge`, `m6g.2xlarge`) sozinhos desnecessariamente.

* **PRD - Opensearch** (Desperdício: 99% CPU | 38% Memória)
  * *Diagnóstico:* 18 vCPUs reservadas para usar 0.11 é um erro grosseiro de configuração.
  * **Ação:** Reduzir `CPU Request` de **18.0** para **2.0** (ainda deixando 20x de margem sobre o uso real).
  * **Ação:** Reduzir `Memory Request` de **72 GiB** para **50 GiB** (uso atual é 44GB).
  * *Impacto:* Liberação imediata de \~16 vCPUs e \~22GB de RAM (quase uma instância inteira).
* **STG - Opensearch** (Desperdício: 99% CPU)
  * *Diagnóstico:* Ambiente de Staging com 6 vCPUs reservadas para 0.6 de uso.
  * **Ação:** Reduzir `CPU Request` de **6.0** para **1.0**.
  * **Ação:** Reduzir `Memory Request` de **24 GiB** para **18 GiB**.
* **Monitoramento - Loki** (Desperdício: 99% CPU | 67% Memória)
  * *Diagnóstico:* 5 vCPUs reservadas, uso de 0.3.
  * **Ação:** Reduzir `CPU Request` de **5.0** para **1.0**.
  * **Ação:** Reduzir `Memory Request` de **15 GiB** para **6 GiB**.
* **Monitoramento - Promtail** (Desperdício: 84% CPU)
  * *Diagnóstico:* Agente de log consumindo recurso de aplicação.
  * **Ação:** Reduzir `CPU Request` de **2.1** para **0.5**.

### **B. Otimização de Aplicações e Ferramentas**

* **Metabase (Tools)**
  * *Atenção:* O uso de memória (9.8 GiB) é **maior** que o request (8 GiB). Isso é perigoso e pode causar OOM Kills ou instabilidade no nó.
  * **Ação:** **Aumentar** `Memory Request` para **11 GiB** (estabilidade).
  * **Ação:** **Reduzir** drásticamente `CPU Request` de **4.0** para **0.5** (Ociosidade de 95%).
* **KEDA (Todos os componentes)**
  * *Diagnóstico:* Estão superdimensionados em 10x ou mais.
  * **Ação:** Ajustar requests para valores de "sidecar".
    * CPU: de **0.2** para **0.05** (50m).
    * Memória: de **200 MiB** para **80 MiB**.
* **Stg/Prd Apps (Reservas & Wallet)**
  * **Ação:** Aplicar corte linear de 50% a 70% nos `CPU Requests` de todos os microserviços listados na tabela de desperdício acima de 90%.
    * Ex: *reservas-worker* (PRD) de **2.4** para **0.5**.


---

## 2. Otimização de Infraestrutura (Nodes & Karpenter)

Como os workloads diminuirão drasticamente seus `Requests` após as ações acima, os Nodes atuais ficarão "vazios" logicamente. O Karpenter precisa ser reconfigurado para aproveitar isso.

### **A. Consolidação (Bin-packing)**

Com a redução dos requests sugerida acima (liberando mais de 30 vCPUs no total), o cluster atual está extremamente fragmentado.

* **Ação:** Forçar uma "defragmentação" ou reciclagem dos nodes via Karpenter para que os Pods sejam agendados em menos máquinas.
* **Configuração:** Verificar se a flag de `consolidation` ou `disruption` do Karpenter está ativa e agressiva o suficiente para eliminar nodes subutilizados.

### **B. Diversificação de Instâncias**

* **Recomendação:** Se o gargalo da maioria das aplicações é memória (como visto no Metabase e Opensearch), instâncias da família `**r6g**` **ou** `**r7g**` **(Memory Optimized)** podem ser mais baratas proporcionalmente para a quantidade de RAM necessária, evitando subir CPUs caras que ficam ociosas apenas para atender requisitos de memória.
* **Ação:** Adicionar famílias `r` na lista de compatibilidade do Provisioner/NodePool do Karpenter.

### **C. Uso de Spot Instances (Ambiente STG)**

O namespace `stg-apps` e `tools` não deveriam rodar em On-Demand se o custo é uma preocupação.

* **Ação:** Configurar o NodePool do Karpenter para priorizar **100% Spot Instances** para workloads que não sejam de Produção. Isso reduz o custo da EC2 em \~60-70% imediatamente.


---

## 3. Governança e Prevenção (Definitivo)

Para evitar que esse relatório precise ser feito novamente mês que vem:


1. **Vertical Pod Autoscaler (VPA):**
   * Implementar o VPA em modo `Recommendation` em todos os deployments. Ele gera métricas dizendo exatamente quanto o pod deveria ter de request baseada no histórico real.
   * *Melhor:* Em Staging, configurar o VPA em modo `Auto` para ajustar os requests automaticamente.
2. **Resource Quotas por Namespace:**
   * Definir um teto (Quota) de CPU e Memória para os namespaces `stg-apps` e `tools`. Isso impede que deploys com configurações erradas (ex: 6 vCPUs em staging) sejam aceitos pelo cluster.

## **Resumo do Plano de Ataque:**


1. Criar tarefas de right-sizing para atarcamos pelo menos todas as aplicações e ferramentas que geram menos impacto (**Staging**,**Tools** & **alguns casos muito gritantes do monitoramento**), minha sugestão seria inclusive uma TF pra isso 
2. Ajustar affinitys para configurar serviços de  Staging  & Tools para utilizar Spot Instances.
3. Revisar configurações do karpenter para garantir que ele está removendo rapidamente nodes que não estão em uso