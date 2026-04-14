<!-- title: [Reservas API] - Redis Migration Lock Blocking Application Startup - 17/09/2025 | url: https://outline.seazone.com.br/doc/reservas-api-redis-migration-lock-blocking-application-startup-17092025-xy7abE1hlZ | area: Tecnologia -->

# [Reservas API] - Redis Migration Lock Blocking Application Startup - 17/09/2025

### 🕒 Data

17/09/2025

### 🌍 Ambiente

Staging

### ☁️ Cluster / Conta AWS

Cluster: arn:aws:eks:sa-east-1:711387131913:cluster/general-cluster

Namespace: stg-apps

### 🚨 Descrição do Incidente

A API do reservas estava em estado de CrashLoopBackOff com todos os pods falhando durante o startup. O problema foi identificado quando os pods ficavam travados na etapa "Running alembic upgrade" e eventualmente eram mortos pelo Kubernetes devido a falhas nos health checks (liveness/readiness probes).

**Sintomas observados:**

* 4 pods em CrashLoopBackOff
* Exit code 137 (SIGKILL)
* Logs mostravam travamento em "Running alembic upgrade"
* Health checks falhando com "connection refused" na porta 8001
* Workers e scheduler funcionando normalmente

**Impacto:**

* API do reservas indisponível para requisições externas
* Funcionalidades dependentes da API afetadas
* Workers e scheduler continuaram funcionando (sem impacto nos jobs background)

### 🧠 Causa Raiz

A aplicação foi encerrada abruptamente sem limpar adequadamente a chave de lock `db_migration` no Redis. Essa chave é utilizada pelo sistema para garantir que apenas uma instância execute migrações de banco simultaneamente.

Quando os novos pods tentavam inicializar, o alembic upgrade ficava esperando indefinidamente pela liberação do lock que nunca aconteceria, resultando no travamento da aplicação.

**Sequência do Problema:**


1. Pods novos iniciam e ficam travados no `alembic upgrade` aguardando o lock Redis
2. Após 60s (`initialDelaySeconds`), Kubernetes inicia liveness probes em `/health` (porta 8001)
3. Aplicação não responde pois está travada no alembic
4. Após 3 falhas consecutivas em \~90s (`failureThreshold: 3`), Kubernetes mata o pod com SIGKILL (exit code 137)
5. Ciclo se repete indefinidamente (CrashLoopBackOff)

**Sobre o SIGKILL 137:**

* **NÃO foi OOMKilled** (falta de memória)
* **Foi liveness probe failure**: Kubernetes matou o pod porque não conseguiu acessar `/health`
* **Timeline**: \~60s (initial delay) + \~90s (3 failed probes) = \~150s até SIGKILL
* **Recursos**: 300Mi request / 1000Mi limit - suficientes

### 🔧 Ações Corretivas Aplicadas


1. **Diagnóstico inicial:**

   ```bash
   kubectl get pods -n stg-apps | grep reservas-api
   kubectl logs -n stg-apps <pod-name>
   kubectl describe pod -n stg-apps <pod-name>
   ```
2. **Verificação da conectividade do banco:**

   ```bash
   kubectl exec -n stg-apps bastion-staging-xxx -- nc -zv stg-postgres.cbwcm8my4qns.sa-east-1.rds.amazonaws.com 5432
   ```
3. **Limpeza da chave de lock no Redis:**

   ```bash
   kubectl run redis-fix --image=redis:7-alpine -n stg-apps --restart=Never --command -- redis-cli -h reservas-valkey-stg-001.cm03pm.0001.sae1.cache.amazonaws.com -p 6379 DEL db_migration
   ```
4. **Reinício do deployment:**

   ```bash
   kubectl rollout restart deployment/reservas-api -n stg-apps
   ```

### ✅ Resultados

* ✅ Pods iniciaram corretamente
* ✅ Alembic upgrade executado com sucesso
* ✅ API respondendo na porta 8001
* ✅ Health checks funcionando
* ✅ Requisições sendo processadas normalmente
* ✅ Índices do OpenSearch criados automaticamente

### 🔎 Verificações

```bash
# Verificar status dos pods

kubectl get pods -n stg-apps | grep reservas-api

# Acompanhar logs de inicialização

kubectl logs -n stg-apps reservas-api-58ff7ddcf6-wccjb -f

# Verificar health check

curl -I http://stg-api.seazone.com.br/health

# Confirmar que o lock foi removido

redis-cli -h reservas-valkey-stg-001.cm03pm.0001.sae1.cache.amazonaws.com -p 6379 GET db_migration
```

### 📝 Recomendações Futuras


1. **Implementar timeout no lock de migração**: Adicionar TTL automático na chave `db_migration` para evitar locks órfãos
2. **Melhorar graceful shutdown**: Garantir que a aplicação limpe adequadamente os locks durante o processo de shutdown
3. **Adicionar monitoramento específico**:
   * Alert quando pods ficam mais de X minutos em "Running" sem passar nos health checks
   * Monitorar presença de chaves de lock no Redis
4. **Documentar troubleshooting**: Criar runbook específico para esse tipo de problema recorrente
5. **Considerar usar PostgreSQL advisory locks**: Alternativa mais robusta que locks no Redis para controle de migrações
6. **Automação**: Script ou job que verifica e limpa locks órfãos automaticamente

### 🏷️ Tags

\#redis #alembic #migration #lock

### 👥 Responsáveis

* [john.paiva@seazone.com.br](mailto:john.paiva@seazone.com.br)
* [bernardo.ribeiro@seazone.com.br](mailto:bernardo.ribeiro@seazone.com.br)
* [patrick.moreira@seazone.com.br](mailto:patrick.moreira@seazone.com.br)