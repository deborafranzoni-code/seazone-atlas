<!-- title: [sapron-frontend] - Downtime por Incompatibilidade de Plataforma e Baixa Resiliência - 10/12/2025 | url: https://outline.seazone.com.br/doc/sapron-frontend-downtime-por-incompatibilidade-de-plataforma-e-baixa-resiliencia-10122025-Ka3sLVucFT | area: Tecnologia -->

# [sapron-frontend] - Downtime por Incompatibilidade de Plataforma e Baixa Resiliência - 10/12/2025

🕒 Data: 10/12/2025 e 11/12/2025

🌍 Ambiente: Produção (prd-apps)

☁️ Cluster / Conta AWS: general-cluster / 711387131913 (sa-east-1)

# 🚨 Descrição do Incidente

O serviço sapron-frontend apresentou múltiplos episódios de downtime em produção nos dias 10 e 11 de dezembro de 2025. O problema foi identificado através de:

* **Alertas de saúde**: Pods falhando ao iniciar
* **Logs de eventos**: Múltiplos erros de `ImagePullBackOff` e `ErrImagePull`
* **Impacto**: Downtime intermitente do serviço, afetando usuários finais
* **Sintomas observados**:
  * Pods não conseguiam iniciar em determinados nós
  * HPA reduzindo réplicas de 2 para 1, aumentando vulnerabilidade
  * Múltiplas tentativas de restart sem sucesso

## **Eventos críticos identificados:**

```
Warning: Failed to pull image "711387131913.dkr.ecr.sa-east-1.amazonaws.com/sapron-frontend:1.44.0": 
rpc error: code = NotFound desc = failed to pull and unpack image: 
no match for platform in manifest: not found
```

# 🧠 Causa Raiz

A causa raiz foi identificada como uma combinação de três fatores:


1. **Incompatibilidade de Plataforma (Principal)**:
   * A imagem Docker `sapron-frontend:1.44.0` não possui manifest para arquitetura ARM64 (aarch64)
   * O cluster possui nós com arquiteturas mistas (AMD64 e ARM64)
   * O `nodeAffinity` estava configurado como `preferredDuringSchedulingIgnoredDuringExecution`, permitindo que pods fossem agendados em nós ARM64 quando não havia nós AMD64 disponíveis
   * Quando pods eram agendados em nós ARM64, o kubelet falhava ao fazer pull da imagem, resultando em `ImagePullBackOff`
2. **Baixa Resiliência**:
   * HPA configurado com `minReplicas: 1`, permitindo que o serviço ficasse com apenas uma réplica
   * Com apenas 1 réplica, qualquer falha (incluindo preemptions ou falhas de pull) causava downtime imediato
   * PDB configurado com `minAvailable: 1`, mas com apenas 1 réplica, não havia margem para falhas
3. **Preemptions de Pods**:
   * Múltiplos pods foram preemptados por outros pods com maior prioridade
   * Isso causava interrupções temporárias durante rollouts e escalonamentos

## **Evidências técnicas:**

* Eventos mostraram falhas de pull em nós específicos (ip-10-0-47-123, ip-10-0-50-47) que são ARM64
* Pods que conseguiam iniciar estavam sempre em nós AMD64 (ip-10-0-4-123)
* HPA estava constantemente reduzindo réplicas para 1 devido a métricas baixas

🔧 Ações Corretivas Aplicadas

### 1. NodeAffinity Obrigatório

**Arquivo**: `helm/frontend/templates/deployment.yaml`

* Alterado de `preferredDuringSchedulingIgnoredDuringExecution` para `requiredDuringSchedulingIgnoredDuringExecution`
* Garante que pods só sejam agendados em nós do nodepool `general-karpenter-amd64`

```yaml

affinity:
  nodeAffinity:
    requiredDuringSchedulingIgnoredDuringExecution:
      nodeSelectorTerms:
        - matchExpressions:
            - key: karpenter.sh/nodepool
              operator: In
              values:
                - general-karpenter-amd64
```

### 2. Aumento de MinReplicas do HPA

**Arquivos**: `values.yaml`, `values-dev.yaml`, `values-stg.yaml`

* Produção: `minReplicas: 1 → 2`
* Desenvolvimento: `minReplicas: 1 → 2`
* Staging: `minReplicas: 1 → 2`

### 3. Ajuste de Réplicas Iniciais

**Arquivos**: `values-dev.yaml`, `values-stg.yaml`

* Desenvolvimento: `replicas: 1 → 2`
* Staging: `replicas: 1 → 2`
* Produção: já estava em 2 (mantido)

# ✅ Resultados

Após a aplicação das correções:

* ✅ **Eliminação de erros de ImagePullBackOff**: NodeAffinity obrigatório previne agendamento em nós incompatíveis
* ✅ **Melhoria na resiliência**: Com mínimo de 2 réplicas, o serviço pode tolerar falhas de um pod sem downtime
* ✅ **Consistência entre ambientes**: Todos os ambientes (dev, stg, prd) agora têm configuração consistente de alta disponibilidade
* ✅ **PDB efetivo**: Com 2 réplicas e `minAvailable: 1`, há margem para falhas durante manutenções

## **Validação realizada:**

* Verificado que pods são agendados apenas em nós AMD64
* Confirmado que HPA mantém mínimo de 2 réplicas
* Validado que PDB funciona corretamente com a nova configuração

🔎 Verificações

### Comandos de Validação Utilizados

```bash
# Verificar eventos de erro

kubectl get events -n prd-apps --field-selector involvedObject.name=sapron-frontend --sort-by='.lastTimestamp'

# Verificar arquitetura dos nós

kubectl get nodes -o jsonpath='{range .items[*]}{.metadata.name}{"\t"}{.status.nodeInfo.architecture}{"\n"}{end}'

# Verificar deployment atual

kubectl get deployment sapron-frontend -n prd-apps -o yaml

# Verificar PDB

kubectl get pdb sapron-frontend -n prd-apps -o yaml

# Verificar HPA

kubectl get hpa sapron-frontend -n prd-apps -o yaml

# Verificar pods e seus nós

kubectl get pods -n prd-apps -l app.kubernetes.io/name=sapron-frontend -o wide
```

### Validações Pós-Correção

- [x] NodeAffinity configurado como `required` no deployment
- [x] HPA com `minReplicas: 2` em todos os ambientes
- [x] Réplicas iniciais ajustadas para 2 em dev e stg
- [x] PDB mantém `minAvailable: 1` (adequado com 2 réplicas)
- [x] RollingUpdate mantido em 50% maxUnavailable (conforme solicitado)

# 📝 Recomendações Futuras

### Curto Prazo (Implementar)


1. **Monitoramento de Compatibilidade de Plataforma**
   * Adicionar alerta para detectar tentativas de pull de imagem em arquiteturas incompatíveis
   * Criar dashboard para monitorar distribuição de pods por arquitetura de nó
2. **Validação em CI/CD**
   * Adicionar verificação no pipeline de build para garantir que imagens sejam multi-arch (AMD64 + ARM64)
   * Validar nodeAffinity antes de fazer deploy em produção

### Médio Prazo (Planejar)


3. **Imagens Multi-Arch**
   * Modificar pipeline de build para publicar imagens com suporte a múltiplas arquiteturas
   * Usar `docker buildx` para criar manifests multi-platform
   * Benefício: Flexibilidade para usar qualquer tipo de nó no cluster
4. **Testes de Resiliência**
   * Implementar testes de chaos engineering para validar comportamento com falhas de nós
   * Testar cenários de preemption e eviction
5. **Documentação de Arquitetura**
   * Documentar requisitos de plataforma para cada serviço
   * Criar runbook para troubleshooting de problemas de compatibilidade

### Longo Prazo (Considerar)


6. **Automação de NodeAffinity**
   * Criar admission controller ou mutating webhook para aplicar nodeAffinity automaticamente baseado em labels da imagem
   * Reduzir chance de erro humano
7. **Review de Configurações de HA**
   * Revisar todos os serviços para garantir que tenham configuração adequada de alta disponibilidade
   * Padronizar minReplicas baseado em criticidade do serviço

> Pull request

<https://github.com/seazone-tech/gitops-sapron/pull/8>


👥 Responsáveis

@[John Paulo da Silva Paiva](mention://a2d9111b-9d3a-478d-b476-07eea5945ab3/user/fe961e04-fb16-4dab-b8b9-0d6428861ad2)