<!-- title: [Metabase] - Evicções por Falta de Recursos e Instabilidade no NodePool - 23/04/2025 | url: https://outline.seazone.com.br/doc/metabase-eviccoes-por-falta-de-recursos-e-instabilidade-no-nodepool-23042025-uAyclHnUOf | area: Tecnologia -->

# [Metabase] - Evicções por Falta de Recursos e Instabilidade no NodePool - 23/04/2025

**🕒 Data:** 23/04/2025

**🌍 Ambiente:** Produção

**☁️ Cluster / Conta AWS:** tools / seazone-prod

## 🚨 Descrição do Incidente

O Metabase apresentou instabilidade em produção, com pods sendo frequentemente reiniciados ou evictados. O HPA não estava atuando corretamente e o serviço apresentava lentidão ou falhas de acesso. A causa estava relacionada à ausência de definição de recursos nos pods, instâncias inadequadas no NodePool e problemas de disponibilidade.

## 📊 Evidências do Problema

### Eventos de Evicção Devido à Pressão de Memória

**Comando executado:**

```bash
kubectl get events -n tools --sort-by='.lastTimestamp' | grep -E 'Evicted|FailedScheduling|MemoryPressure|Unhealthy'
```

**Resultado:**

```
Warning   Evicted   pod/metabase-9d847c4bb-ss74q   The node had condition: [MemoryPressure].
Warning   Evicted   pod/metabase-9d847c4bb-jwxvd   The node had condition: [MemoryPressure].
Warning   Evicted   pod/metabase-9d847c4bb-lgtr7   The node had condition: [MemoryPressure].
Warning   Evicted   pod/metabase-9d847c4bb-84sjp   The node had condition: [MemoryPressure].
Warning   Evicted   pod/metabase-9d847c4bb-pd62d   The node had condition: [MemoryPressure].
```

Estes eventos mostram que múltiplos pods do Metabase estão sendo expulsos (evicted) devido à condição de `MemoryPressure` nos nós, causando interrupções no serviço.

### Falha no Agendamento

**Comando executado:**

```bash
kubectl get events -n tools --sort-by='.lastTimestamp' | grep FailedScheduling
```

**Resultado:**

```
Warning   FailedScheduling   pod/metabase-9d847c4bb-lvlvs   0/17 nodes are available: 1 node(s) had untolerated taint {node.kubernetes.io/memory-pressure: }, 1 node(s) had untolerated taint {node.kubernetes.io/unreachable: }, 15 node(s) didn't match Pod's node affinity/selector.
```

Este evento mostra que novos pods não conseguiam ser agendados porque não havia nós disponíveis com recursos suficientes.

### Consumo Real de Memória

**Comando executado:**

```bash
kubectl top pods -n tools | grep metabase
```

**Resultado:**

```
metabase-9d847c4bb-hz759   3m   667Mi           
metabase-9d847c4bb-kvbt9   3m   690Mi           
metabase-9d847c4bb-lvlvs   4m   747Mi  
```

Cada instância do Metabase consumia aproximadamente 700MB de memória, mas como não havia limites definidos, o Kubernetes não reservava este espaço com antecedência.

### Recursos Não Definidos

**Comando executado:**

```bash
kubectl get deploy metabase -n tools -o yaml | grep -A15 resources
```

**Resultado:**

```yaml
resources: {}
terminationMessagePath: /dev/termination-log

terminationMessagePolicy: File
```

Não havia requisitos de recursos definidos para o Metabase, o que impedia o Kubernetes de fazer um planejamento adequado.

### NodePool com Apenas 1 Nó de Budget

**Comando executado:**

```bash
kubectl get nodepool tools -o yaml
```

**Resultado:**

```yaml

spec:
  disruption:
    budgets:
    - nodes: "1"
    consolidationPolicy: WhenUnderutilized
    expireAfter: 720h
```

A configuração do NodePool permitia apenas 1 nó de budget, insuficiente para manter a disponibilidade quando um nó precisava ser substituído.

### Tamanho Inadequado das Instâncias

**Comando executado:**

```bash
kubectl get nodeclaims | grep tools
```

**Resultado:**

```
tools-tztfk   t3.small     us-west-2c   ip-205-0-3-199.us-west-2.compute.internal   True    52m

tools-lvkzr   t3.medium    us-west-2c   ip-205-0-3-193.us-west-2.compute.internal   True    106m

tools-xczcv   t3.medium    us-west-2a   ip-205-0-1-100.us-west-2.compute.internal   True    34h
```

O Karpenter estava provisionando algumas instâncias t3.small, que têm apenas 2GB de RAM - insuficientes para executar múltiplas instâncias do Metabase, cada uma consumindo \~700MB.

### Falha no HPA

**Comando executado:**

```bash
kubectl describe hpa metabase -n tools | grep -A10 "Metrics:"
```

**Resultado:**

```
Metrics:                                                  ( current / target )
resource memory on pods  (as a percentage of request):  <unknown> / 80%
resource cpu on pods  (as a percentage of request):     <unknown> / 80%
Min replicas:                                             3

Max replicas:                                             5

Deployment pods:                                          3 current / 3 desired

Conditions:
  Type           Status  Reason                   Message
  ----           ------  ------                   -------
  AbleToScale    True    SucceededGetScale        the HPA controller was able to get the target's current scale
  ScalingActive  False   FailedGetResourceMetric  the HPA was unable to compute the replica count: failed to get memory utilization: missing request for memory in container metabase
```

O HPA não conseguia escalar porque não havia requisitos de recursos definidos, impedindo o cálculo da utilização relativa aos limites.


## 🧠 Causa Raiz


1. O deployment do Metabase não possuía `requests` e `limits` definidos, o que resultava em QoS BestEffort e evicções constantes. Cada pod do Metabase consumia aproximadamente 700MB de memória, mas como não havia recursos definidos, o Kubernetes não conseguia planejar adequadamente onde agendar esses pods.
2. O NodePool estava configurado com apenas 1 nó de budget e instâncias do tipo t3.small (2GB RAM), insuficientes para suportar os recursos exigidos pelo Metabase. Com cada pod consumindo \~700MB, uma instância t3.small não conseguia acomodar várias réplicas, especialmente considerando o overhead do sistema e outros componentes.
3. As probes de liveness/readiness tinham tempos inadequados, causando reinicializações desnecessárias. Nos logs, foi observado que o Metabase levava aproximadamente 30-40 segundos para inicializar completamente e realizar migrações de banco de dados, mas as probes estavam verificando a saúde antes desse tempo.
4. Afinidades de nó utilizavam labels depreciados `beta.kubernetes.io/arch` (Apesar de não estar totalmente relacionado ao problema, apresentava warnings nos logs e foi corrigido em conjunto).
5. O HPA não conseguia escalar porque não havia requisitos de recursos definidos, o que impedia o cálculo da utilização relativa aos limites.

## 🔧 Ações Corretivas Aplicadas


1. Adicionados `requests` e `limits` ao container do Metabase:

```yaml
requests:
  memory: "512Mi"
  cpu: "300m"
limits:
  memory: "1Gi"
  cpu: "500m"
```


2. Atualizado `NodePoolTools.yaml` para:
   * Definir mínimo de 2 nós
   * Restringir instâncias para: t3.large, t3.xlarge, m5.large, m8g.large, t4g.large

```yaml
spec:
  template:
    spec:
      requirements:
      - key: "node.kubernetes.io/instance-type"
        operator: In
        values: ["t3.large", "t3.xlarge", "m5.large", "m8g.large", "t4g.large"]
  disruption:
    budgets:
      nodes: 2
    consolidationPolicy: WhenUnderutilized
    expireAfter: 720h
```


3. Ajustadas as probes:

```yaml
livenessProbe:
  initialDelaySeconds: 180
  timeoutSeconds: 30
  periodSeconds: 15

readinessProbe:
  initialDelaySeconds: 60
  timeoutSeconds: 5
  periodSeconds: 10
```


4. Forçada a remoção de pods stuck em Terminating, tinha mais de 80 nessa situação:

```bash
kubectl delete pods -n tools $(kubectl get pods -n tools | grep "Terminating" | awk '{print $1}') --force
```

## ✅ Resultados:

* O HPA passou a escalar corretamente com base na memória (de 3 → 5 pods).
* Nenhuma evicção registrada após as alterações.
* Metabase estável e responsivo.
* Probes permitem inicialização adequada.
* O NodePool mantém no mínimo dois nós ativos e resistentes a falhas spot.

## 🔎 Verificações:

```bash
# Verificar que pods têm recursos definidos

kubectl get pod -n tools -o json | jq '.items[] | select(.metadata.name | startswith("metabase")) | {name: .metadata.name, resources: .spec.containers[0].resources}'

# Verificar nós do nodepool tools

kubectl get nodeclaims | grep tools

# Verificar que o HPA está funcionando

kubectl describe hpa metabase -n tools

# Verificar eventos (não deve haver evicções)
kubectl get events -n tools | grep -i evict

# Recursos definidos no pod:
kubectl get pods -n tools -l app=metabase -o jsonpath="{.items[0].spec.containers[0].resources}"

# Estado do HPA:
kubectl get hpa -n tools metabase

# Probes:
kubectl get deployments.apps -n tools metabase -o yaml | grep -A10 livenessProbe

# Tipos de instância:
kubectl describe nodepool tools | grep -A10 "instance-type"
```

## 📝 Recomendações Futuras:


1. Criar alertas para evicções e uso de memória excessivo.
2. Monitorar o comportamento do HPA e ajustar thresholds se necessário.
3. Garantir que todos os novos deployments definam requests e limits mínimos.
4. Rodar exercícios de DR simulando remoção de instâncias spot.
5. Considerar uso de instâncias on-demand para workloads críticos como o Metabase.
6. Revisar periodicamente a configuração dos NodePools para garantir que estejam adequados às necessidades atuais.
7. Criação do helm chart do metabase para versionamento e visualização das configurações atuais

## 🏷️ Tags:

\#metabase #hpa #karpenter #probes #eviction #infra #eks #aws #qualityofservice #nodepools #kubernetes

## 👥 Responsáveis:

@[John Paulo da Silva Paiva](mention://752dcffe-e399-406b-af0e-9fcdebe2963f/user/65c61c86-6a76-426e-8af9-6f1dd54caf65)