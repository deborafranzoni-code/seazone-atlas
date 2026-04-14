<!-- title: [Opensearch] - Instabilidade | url: https://outline.seazone.com.br/doc/opensearch-instabilidade-BhKgroLILg | area: Tecnologia -->

# [Opensearch] - Instabilidade

**Data:** 05/05/2025

**🌍 Ambiente:** Produção (inferido, não explicitamente declarado nos logs)

**☁️ Cluster / Conta AWS:** tools / seazone-prod (inferido, baseado no namespace e exemplo Metabase)

## 🚨 Descrição do Incidente

O Opensearch `reservas` no namespace `tools` apresentou indisponibilidade entre aproximadamente 2025-05-06T01:00:00Z e 2025-05-06T02:20:00Z. A instabilidade manifestou-se através de falhas na inicialização de pods Opensearch (masters e nodes) durante um processo de `rolling restart` orquestrado pelo `containerset-controller`.

## 📊 Evidências do Problema

### Falhas de Comunicação Interna Precedendo o Restart Principal

Nos logs internos dos pods Opensearch, foram observadas falhas de conexão entre nós do cluster pouco antes da sequência de reinicializações que levou à indisponibilidade. Especificamente, o pod `reservas-nodes-2` registrou tentativas falhas de conexão com `reservas-nodes-1` na porta de transporte (9300):

```
[2025-05-06T01:35:50,687][WARN ][o.o.c.NodeConnectionsService] [reservas-nodes-2] failed to connect to {reservas-nodes-1}{...}{205.0.3.207:9300} (tried [1] times)
org.opensearch.transport.ConnectTransportException: [reservas-nodes-1][205.0.3.207:9300] connect_exception
Caused by: io.netty.channel.AbstractChannel$AnnotatedConnectException: Connection refused: reservas-nodes-1/205.0.3.207:9300
	... (stacktrace omitido para brevidade)
```

Este evento, ocorrido às `01:35:50Z`, sugere uma instabilidade latente ou problemas de comunicação na camada de transporte do Opensearch que podem ter contribuído para as falhas subsequentes.

### Falhas de Startup Probe Durante o Rolling Restart

Durante o processo de `rolling restart`, múltiplos pods do Opensearch falharam em seus `StartupProbes`. Os eventos do Kubernetes indicam que os pods não se tornaram acessíveis na porta HTTP (9200) dentro do tempo esperado. Exemplos dessas falhas incluem:

Para `reservas-masters-2` (primeira falha registrada para este pod no ciclo):

```
2025-05-06 01:44:59Z Warning Startup probe failed: dial tcp 205.0.3.112:9200: connect: connection refused
```

Para `reservas-nodes-2` (primeira falha registrada para este pod no ciclo):

```
2025-05-06 01:44:59Z Warning Startup probe failed: dial tcp 205.0.3.178:9200: connect: connection refused
```

Essas falhas de probe se repetiram para os pods `reservas-masters-1`, `reservas-nodes-1`, `reservas-masters-2` e `reservas-nodes-2` em ciclos subsequentes de reinicialização, conforme os eventos:

Para `reservas-masters-1`:

```
2025-05-06 01:48:24Z Warning Startup probe failed: dial tcp 205.0.3.115:9200: connect: connection refused
```

Para `reservas-nodes-1`:

```
2025-05-06 01:48:23Z Warning Startup probe failed: dial tcp 205.0.3.21:9200: connect: connection refused
```

E novamente para `reservas-masters-2` e `reservas-nodes-2` após serem recriados:

```
2025-05-06 01:51:07Z Warning Startup probe failed: dial tcp 205.0.3.134:9200: connect: connection refused (reservas-masters-2)
2025-05-06 01:51:07Z Warning Startup probe failed: dial tcp 205.0.3.160:9200: connect: connection refused (reservas-nodes-2)
```

### Orquestração do Rolling Restart pelo `containerset-controller`

O evento final que marca a conclusão da atividade de reinicialização dos pods é:

```
2025-05-06 01:51:58Z Normal Rolling restart completed (object reservas, namespace tools, source containerset-controller)
```

Este evento confirma que um `containerset-controller` foi o responsável por orquestrar o `rolling restart` do conjunto de aplicações `reservas`.

### Estratégia de Atualização dos StatefulSets

A configuração dos StatefulSets `reservas-masters` e `reservas-nodes` utiliza a estratégia de atualização `OnDelete`:

```yaml
# Saída de kubectl get statefulset reservas-masters -n tools -o yaml | yq ".spec.updateStrategy"
spec:
  updateStrategy:
    type: OnDelete
```

Isso implica que as atualizações de configuração nos templates dos pods dos StatefulSets não disparam automaticamente um rolling update. Os pods são atualizados apenas quando suas instâncias antigas são explicitamente deletadas, o que reforça que o `rolling restart` foi uma ação deliberada e orquestrada por um mecanismo externo ao controle padrão do StatefulSet,  o `containerset-controller`.

## 🧠 Causa Raiz


1. **Gatilho do Incidente:** O incidente foi iniciado por um `rolling restart` do cluster Opensearch `reservas`, orquestrado pelo `containerset-controller`. Embora a sequência de reinicialização seja clara, a razão específica que levou o `containerset-controller` a iniciar este restart ( *aplicação de nova configuração, atualização de versão, manutenção planejada*) não pôde ser determinada com as evidências analisadas. Pelos logs, o `containerset-controller` é o componente identificado como o orquestrador desta operação.
2. **Falha na Inicialização dos Pods:** Durante o `rolling restart`, múltiplos pods Opensearch (masters e nodes) falharam consistentemente em seus `StartupProbes`. As mensagens `connect: connection refused` na porta 9200 indicam que o serviço Opensearch dentro dos containers não se tornou operacional e acessível dentro do tempo configurado pelas probes (aproximadamente 210 segundos de tolerância para o startup probe: `initialDelaySeconds: 10`, `periodSeconds: 20`, `timeoutSeconds: 5`, `failureThreshold: 10`).
3. **Problemas de Comunicação Interna Preexistentes:** Logs dos pods Opensearch indicam falhas de conexão na porta de transporte (9300) entre nós do cluster (`reservas-nodes-2` para `reservas-nodes-1`) aproximadamente 20 minutos *antes* do início da sequência principal de falhas de startup probe. Isso sugere uma instabilidade subjacente ou problemas de comunicação na rede do cluster Opensearch que podem ter exacerbado as dificuldades de inicialização durante o `rolling restart`.

   \

Em resumo, o `rolling restart` expôs uma incapacidade dos pods Opensearch de iniciarem e formarem um cluster saudável de forma consistente, provavelmente devido a uma combinação de fatores incluindo a configuração das probes, possíveis problemas de comunicação interna preexistentes e a natureza da orquestração do restart pelo `containerset-controller`.


## Queda em Staging


1. **Problema**\nNa terça-feira desta semana, detectamos um problema no OpenSearch de staging. Através do monitoramento, percebemos que os pods responsáveis pelos nós do OpenSearch estavam com uso excessivo de recursos. Isso fazia com que os pods caíssem, resultando em um erro no OpenSearch Controller, que não conseguia mais se comunicar com os nós.
2. **Solução**\nPara resolver, aumentamos os recursos dos nós, tanto os masters quanto os non-masters, para que conseguissem lidar com a carga de trabalho. Agora, os pods estão rodando com cerca de 60% a 70% do limite máximo de recursos. Deixamos essa margem de folga, pois ainda não sabemos ao certo o que causou esse aumento no workload e se isso pode acontecer novamente.
3. **Configuração de Recursos**\nAs alterações feitas nas configurações de recursos foram:\nMemória: Aumentamos o limite máximo de memória de 2Gi para 3Gi (pouco mais de 3GB).\nCPU: O limite máximo de CPU foi ajustado de 500m para 600m (60% de um núcleo de CPU).
4. **Conclusão**\nVale acompanhar o uso de recursos de perto para garantir que os valores não estejam superprovisionados. Fizemos esse ajuste para restaurar a operação, mas seria bom revisar os dados de monitoramento depois para determinar os valores mais adequados.\nAlém disso, precisamos entender se o aumento de workload é algo esperado ou se alguma mudança recente na aplicação fez com que o consumo de recursos aumentasse. Se esse aumento for esperado, tudo bem, mas se não for, o aumento de custos pode ser um problema. E, claro, se isso for levado para o ambiente de produção sem os ajustes certos, podemos ter o mesmo tipo de problema por lá.