<!-- title: [Kube-prometheus-stack] CrashLoopBackOff por OOMKilled na Réplica 0 - 11/12/2025 | url: https://outline.seazone.com.br/doc/kube-prometheus-stack-crashloopbackoff-por-oomkilled-na-replica-0-11122025-KzLPLMf7oF | area: Tecnologia -->

# [Kube-prometheus-stack] CrashLoopBackOff por OOMKilled na Réplica 0 - 11/12/2025

🕒 Data

11/12/2025

🌍 Ambiente

Produção (monitoring)

☁️ Cluster / Conta AWS

general-cluster / 711387131913 (sa-east-1)

🚨 Descrição do Incidente

A réplica 0 do Prometheus (`prometheus-kps-prometheus-0`) entrou em estado de `CrashLoopBackOff` por mais de 21 horas, causando:

* **Status**: Pod com 184 restarts, container sendo morto continuamente
* **Sintoma**: Container `prometheus` em estado `Waiting` com `Reason: CrashLoopBackOff`
* **Impacto**:
  * Perda de capacidade de coleta de métricas (1/3 das réplicas indisponível)
  * Possível impacto na disponibilidade de dados históricos
  * Alertas e dashboards podem ter sido afetados pela redução de capacidade

**Eventos observados:**

```
Last State: Terminated
  Reason: OOMKilled
  Exit Code: 137
```

**Logs do container:**

* Container iniciando normalmente
* Carregando blocos TSDB existentes
* Iniciando replay do WAL (Write-Ahead Log)
* Processo sendo morto durante o replay do WAL (segmentos 6677-9797)
* Loop de restart sem conseguir completar o startup

🧠 Causa Raiz

A causa raiz foi identificada como **consumo excessivo de memória durante o replay do WAL**:


1. **WAL Excessivamente Grande**:
   * O WAL da réplica 0 tinha **1.6GB** de dados não compactados
   * Durante o startup, o Prometheus precisa fazer replay completo do WAL na memória
   * O processo de replay de 9797 segmentos WAL consumia mais memória do que o limite configurado
2. **Limite de Memória Insuficiente para Startup**:
   * Limite configurado: **8Gi**
   * Consumo em steady-state das outras réplicas: \~4.2-4.4 GiB (funcionando normalmente)
   * Durante replay do WAL: consumo excedia 8Gi, causando OOMKilled
   * O `GOMEMLIMIT` estava configurado em \~7.7GB, mas o processo ainda excedia durante o replay
3. **Diferença entre Réplicas**:
   * Réplicas 1 e 2 estavam funcionando normalmente há 23 dias
   * Réplica 0 tinha WAL significativamente maior, possivelmente devido a:
     * Diferentes padrões de ingestão de métricas
     * Falhas anteriores que impediram compactação adequada
     * Maior volume de dados não compactados
4. **Retenção de Dados**:
   * Retenção configurada: **10 dias**
   * Com alta ingestão de métricas, isso resulta em WAL grande e muitos blocos TSDB
   * Head chunks também ocupavam \~212MB

**Evidências técnicas:**

```bash
# Tamanho do WAL na réplica problemática
/prometheus/prometheus-db/wal: 1.6G
/prometheus/prometheus-db/chunks_head: 212.0M

# Consumo de memória das réplicas saudáveis

prometheus-kps-prometheus-1: 4258Mi (4.2 GiB)
prometheus-kps-prometheus-2: 4407Mi (4.4 GiB)

# Limite configurado

memory: 8Gi
```

🔧 Ações Corretivas Aplicadas

### 1. Limpeza do WAL da Réplica 0

**Ação**: Remoção do conteúdo do WAL para permitir startup limpo

```bash
# Criar pod auxiliar montando o PVC da réplica 0

kubectl run wal-cleaner --restart=Never --image=busybox -n monitoring \
  --overrides='{"spec":{"volumes":[{"name":"promdata","persistentVolumeClaim":{"claimName":"prometheus-kps-prometheus-db-prometheus-kps-prometheus-0"}}],"containers":[{"name":"wal-cleaner","image":"busybox","command":["sleep","3600"],"volumeMounts":[{"name":"promdata","mountPath":"/prometheus"}]}]}}'

# Remover conteúdo do WAL

kubectl exec -n monitoring wal-cleaner -- rm -rf /prometheus/prometheus-db/wal

kubectl exec -n monitoring wal-cleaner -- mkdir /prometheus/prometheus-db/wal

# Corrigir permissões

kubectl exec -n monitoring wal-cleaner -- chown -R 65534:65534 /prometheus/prometheus-db
```

### 2. Correção de Permissões

**Problema identificado**: Após limpeza, o Prometheus não conseguia criar novos arquivos WAL devido a permissões incorretas **Solução**: Ajuste de ownership para `nobody:nobody` (UID 65534)

### 3. Restart do Pod

**Ação**: Deletar o pod para forçar recriação com WAL limpo

```bash

kubectl delete pod prometheus-kps-prometheus-0 -n monitoring
```

### 4. Validação Pós-Correção

**Resultado**: Pod iniciou com sucesso, consumindo \~706 MiB de memória inicialmente

✅ Resultados

Após a aplicação das correções:

* ✅ **Pod recuperado**: Réplica 0 iniciou com sucesso após limpeza do WAL
* ✅ **Memória normalizada**: Consumo inicial de \~706 MiB, dentro dos limites
* ✅ **Startup completo**: Prometheus conseguiu completar o processo de inicialização
* ✅ **Permissões corrigidas**: Pod consegue escrever no WAL novamente

**Status final:**

* Réplica 0: Running, 0 restarts após correção
* Réplicas 1 e 2: Continuaram funcionando normalmente durante todo o incidente
* Todas as 3 réplicas: Operacionais

**Observação importante**:

* A limpeza do WAL resultou em perda de dados não compactados da réplica 0
* Dados já compactados em blocos TSDB foram preservados
* Outras réplicas mantiveram seus dados intactos

🔎 Verificações

### Comandos de Diagnóstico Utilizados

```bash
# Verificar status do pod

kubectl get pod prometheus-kps-prometheus-0 -n monitoring

# Descrever pod para ver último estado

kubectl describe pod prometheus-kps-prometheus-0 -n monitoring

# Ver logs do container

kubectl logs prometheus-kps-prometheus-0 -n monitoring -c prometheus --previous

kubectl logs prometheus-kps-prometheus-0 -n monitoring -c prometheus

# Verificar consumo de recursos das réplicas saudáveis

kubectl top pod -n monitoring prometheus-kps-prometheus-1 --containers

kubectl top pod -n monitoring prometheus-kps-prometheus-2 --containers

# Verificar tamanho do WAL

kubectl exec -n monitoring wal-cleaner -- du -sh /prometheus/prometheus-db/wal

kubectl exec -n monitoring wal-cleaner -- du -sh /prometheus/prometheus-db/chunks_head

# Verificar permissões

kubectl exec -n monitoring wal-cleaner -- ls -ld /prometheus/prometheus-db/wal
```

### Validações Pós-Correção

- [x] Pod iniciou com sucesso (status: Running)
- [x] Container prometheus em estado Running (não mais CrashLoopBackOff)
- [x] Consumo de memória dentro dos limites
- [x] WAL sendo criado corretamente com permissões adequadas
- [x] Réplicas 1 e 2 continuaram operacionais

📝 Recomendações Futuras

### Curto Prazo (Implementar Imediatamente)


1. **Ajuste de Retenção**
   * Reduzir retenção de **10d para 7d** no `values.yaml`
   * Benefício: Reduz tamanho do WAL e head chunks, diminuindo consumo de memória
   * Arquivo: `gitops/gitops-governanca/argocd/applications/monitoring/kube-prometheus/values.yaml`

   ```yaml
   prometheusSpec:
     retention: 7d  # Reduzir de 10d
   ```
2. **Aumento de Limite de Memória (Opcional)**
   * Considerar aumentar limite de memória para **10-12 Gi** se retenção de 10d for necessária
   * Benefício: Margem maior para replay de WAL durante startup
   * Trade-off: Maior consumo de recursos
3. **Monitoramento de WAL**
   * Adicionar alerta para tamanho do WAL por réplica
   * Alertar quando WAL > 1GB para permitir ação preventiva
   * Exemplo de query PromQL:

     ```promql
     sum(container_fs_usage_bytes{container="prometheus", mountpoint="/prometheus"}) by (pod)
     ```

### Médio Prazo (Planejar)


4. **Otimização de Remote Write**
   * Revisar configuração de `remoteWrite` para reduzir backlog
   * Considerar reduzir `maxShards` de 60 para 20-30
   * Reduzir `capacity` de 30000 se apropriado
   * Benefício: Menor consumo de memória para filas de remote write
5. **Compaction Mais Frequente**
   * Verificar configuração de compactação do TSDB
   * Garantir que compactação está ocorrendo regularmente
   * WAL grande indica possível problema na compactação
6. **Health Checks Melhorados**
   * Adicionar probe para verificar saúde do TSDB
   * Monitorar métricas de WAL replay durante startup
   * Alertar quando replay demora mais que X minutos

### Longo Prazo (Considerar)


 7. **Arquitetura de Retenção**
    * Considerar usar Thanos ou Cortex para retenção longa
    * Prometheus local com retenção curta (3-7 dias)
    * Benefício: Reduz carga no Prometheus, mantém dados históricos
 8. **Automação de Limpeza**
    * Script automatizado para limpar WAL quando muito grande
    * Executar antes que cause OOM
    * Integrar com alertas de tamanho de WAL
 9. **Testes de Carga**
    * Simular crescimento de WAL para validar limites
    * Testar comportamento com diferentes volumes de métricas
    * Validar que limites de memória são adequados
10. **Documentação de Troubleshooting**
    * Criar runbook para problemas de OOM no Prometheus
    * Documentar procedimento de limpeza de WAL
    * Incluir comandos de diagnóstico

### Ações Preventivas


11. **Review de Configurações**
    * Revisar periodicamente tamanho de WAL de todas as réplicas
    * Comparar tamanhos entre réplicas para identificar anomalias
    * Ajustar recursos baseado em uso real
12. **Alertas Proativos**
    * Alertar quando consumo de memória > 80% do limite
    * Alertar quando WAL replay demora > 5 minutos
    * Alertar quando número de restarts > 10 em 1 hora

🏷️ Tags

\#aws #eks #prometheus #oom #crashloopbackoff #wal #tsdb #monitoring #memory #kubernetes #kube-prometheus-stack

👥 Responsáveis

@[John Paulo da Silva Paiva](mention://e9ff71d3-8467-429f-a3a2-b183dc209467/user/fe961e04-fb16-4dab-b8b9-0d6428861ad2)