<!-- title: Estratégia NodePools e Custos (EKS) | url: https://outline.seazone.com.br/doc/estrategia-nodepools-e-custos-eks-rlvn6KFPoC | area: Tecnologia -->

# Estratégia NodePools e Custos (EKS)

# Estratégia Recomendada para NodePools e Custos (EKS)

Este documento detalha a estratégia consolidada de provisionamento e otimização de custos para o cluster `general-cluster`. Esta arquitetura foi desenhada para maximizar a economia usando Spot Instances e Processadores ARM64 (Graviton), mantendo a estabilidade e governança necessárias através de segregação por ambiente.

## 1. Visão Geral da Estratégia

A nova arquitetura simplifica o gerenciamento utilizando apenas **4 NodePools Estratégicos** e uma **EC2NodeClass Unificada**. A complexidade de selecionar a arquitetura (ARM vs x86) e o tamanho da instância é delegada ao Karpenter, que escolhe sempre a opção mais barata compatível com o workload.

### Diagrama de Estrutura dos NodePools

```mermaidjs

graph TD
    subgraph "Cluster EKS: general-cluster"
        UnifiedClass["EC2NodeClass: Unified (Gerencia SGs, Subnets, IAM)"]
        
        subgraph "NodePools"
            Staging["Staging: 100% Spot, Consolidação Rápida"]
            Prod["Prod: Spot Prioritário + OD, Híbrido"]
            System["System: Spot + OD, Core Services"]
            Data["Data: 100% On-Demand, Estabilidade Garantida"]
        end
        
        UnifiedClass --> Staging
        UnifiedClass --> Prod
        UnifiedClass --> System
        UnifiedClass --> Data
    end

    classDef spot fill:#0077b1,stroke:#0077b6,stroke-width:2px;
    classDef od fill:#e85d40,stroke:#e85d04,stroke-width:2px;
    classDef hybrid fill:#55630d,stroke:#55a630,stroke-width:2px;

    class Staging spot;
    class Data od;
    class Prod,System hybrid;
```

## 2. Detalhamento dos NodePools

A estratégia segrega workloads baseada em **Criticidade** e **Estabilidade**, não apenas por tipo de aplicação.

| NodePool | Perfil de Workload | Pricing Strategy | Arquitetura | Consolidação |
|:---|:---|:---|:---|:---|
| `**general-karpenter-staging**` | Aplicações de Staging e Teste | **100% Spot** | Híbrida (ARM/AMD) | **Agressiva (30s)**: Foco total em custo. |
| `**general-karpenter-prod**` | Aplicações Stateless de Produção | **Híbrido (Spot > OD)** | Híbrida (ARM/AMD) | **Moderada (1m)**: Equilibra custo e estabilidade. |
| `**general-karpenter-data**` | StatefulSets (OpenSearch, DBs) | **100% On-Demand** | **ARM64 Only** | **Conservadora (1h)**: Evita interrupções em dados. |
| `**general-karpenter-system**` | Core System (Keda, Argo, Ingress) | **Híbrido** | Híbrida (ARM/AMD) | **Padrão (5m)**: Garante que o plano de controle não dispute recursos. |

### Fluxo de Decisão de Agendamento

O diagrama abaixo ilustra como o Karpenter decide onde colocar cada Pod baseado nas configurações de `nodeSelector` e `tolerations`.

```mermaidjs

flowchart TD
    Pod["Novo Pod Criado"] --> CheckLabel{"Tem label node-pool?"}
    
    CheckLabel -- "Sim: staging" --> PoolStaging["Pool: Staging"]
    CheckLabel -- "Sim: prod" --> PoolProd["Pool: Prod"]
    CheckLabel -- "Sim: data" --> CheckToleration{"Tem toleration stateful?"}
    
    CheckToleration -- Sim --> PoolData["Pool: Data"]
    CheckToleration -- Não --> Pending["Pod Pending (Falta Toleration)"]
    
    CheckLabel -- "Não (Padrão)" --> DefaultLogic["Cai no Pool Prod (se configurado como default)"]
    
    subgraph "Decisão de Instância (Karpenter)"
        PoolProd --> CheckArch{"Pod pede arch: amd64?"}
        CheckArch -- Sim --> ProvAMD["Provisiona Nó AMD64 (c6a, m6a, t3a)"]
        CheckArch -- Não --> ProvBest["Provisiona Mais Barato (Geralmente ARM64 c7g/m7g)"]
    end
```

## 3. Arquitetura Híbrida e EC2NodeClass Unificada

Para evitar a gestão de múltiplos arquivos de configuração para cada arquitetura (ARM/AMD), utilizamos uma abordagem unificada.

### Como funciona a EC2NodeClass Unificada?

Em vez de especificar uma AMI ID fixa (que é diferente para ARM e AMD), usamos `**amiSelectorTerms**` com aliases. Isso permite que o Karpenter resolva a AMI correta dinamicamente baseada na arquitetura da instância que ele decidiu provisionar.

```yaml
amiSelectorTerms:
  - alias: al2023@latest
```

* Se o Karpenter escolher uma `c7g.large` (ARM), ele usará a AMI AL2023 ARM64.
* Se o Karpenter escolher uma `c6a.large` (AMD) devido a um requisito de pod, ele usará a AMI AL2023 AMD64.

### Workloads "AMD-Only"

Para aplicações legadas que não suportam ARM64, basta adicionar o seletor no Deployment. O Karpenter provisionará um nó x86 dentro do mesmo NodePool (Prod ou Staging), mantendo a governança de ambiente mas respeitando o requisito técnico.

```yaml
nodeSelector:
  kubernetes.io/arch: amd64
```

## 4. Estratégia FinOps: Spot, RIs e Savings Plans

A combinação de modelos de compra é essencial para atingir a meta de redução de custos.

```mermaidjs

pie title Distribuição Ideal de Custos
    "Spot (Staging + Prod Stateless)" : 60
    "Savings Plan (Data + System + Baseline Prod)" : 30
    "On-Demand (Picos não cobertos)" : 10
```

### Recomendações de Cobertura (Commitment)


1. **Compute Savings Plan (Recomendado)**: Oferece a maior flexibilidade, permitindo mudança de família (ex: `r6g` para `r7g`) e região.
   * **Cobertura Alvo**: 100% dos nós rodando no pool **Data** e **System**.
   * **Prod Baseline**: Cobrir apenas a carga base de produção que *precisa* ser On-Demand ou que tem uso estável 24/7.
   * **Não Cobrir**: Staging (que é 100% Spot) e cargas elásticas de Produção.
2. **Uso de Spot Instances**:
   * **Staging**: 100% de adoção. O risco de interrupção é aceitável para ambientes de teste.
   * **Prod**: Utilizado como "Primeira Opção". O NodePool tenta provisionar Spot; se não houver capacidade disponível na AWS, faz fallback para On-Demand. Isso garante disponibilidade com o menor custo possível.

### Tabela de Famílias de Instância Prioritárias

O Karpenter é configurado para priorizar as famílias mais eficientes.

| Família | Uso Principal | Características |
|:---|:---|:---|
| **c7g / c6g** | Apps Stateless, APIs | Computação otimizada, melhor custo-benefício (ARM64). |
| **m7g / m6g** | General Purpose | Equilíbrio para apps padrão. |
| **r7g / r6g** | Data, OpenSearch, Monitoramento | Memória otimizada. Essencial para bancos de dados. |
| **t4g** | Staging, Apps pequenos | Burstable, custo muito baixo para cargas leves. |
| **c6a / m6a / t3a** | Legacy Apps | Opções AMD64 modernas para compatibilidade x86. |

## 5. Resumo da Implementação

Para adotar esta estratégia, siga o fluxo:


1. **Infraestrutura**: Aplique a `EC2NodeClass` unificada e os 4 novos `NodePools`.
2. **Migração**:
   * Mova workloads de dados (OpenSearch) para `general-karpenter-data`.
   * Mova workloads de staging para `general-karpenter-staging`.
   * Mova workloads de produção para `general-karpenter-prod`.
3. **Limpeza**: Remova os NodePools antigos (`default`, `amd64`, `arm64`, `opensearch`).
4. **Monitoramento**: Acompanhe a eficiência do *bin-packing* e a taxa de uso de Spot vs On-Demand nos dashboards do Grafana/Kubecost.