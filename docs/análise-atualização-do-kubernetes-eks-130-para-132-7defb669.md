<!-- title: Análise Atualização do Kubernetes EKS 1.30 para 1.32 | url: https://outline.seazone.com.br/doc/analise-atualizacao-do-kubernetes-eks-130-para-132-Punp5s6JGt | area: Tecnologia -->

# Análise Atualização do Kubernetes EKS 1.30 para 1.32

## Contexto

O cluster Kubernetes EKS em ambiente de produção opera atualmente na versão 1.30.10-eks-bc803b4, conforme verificado no levantamento do ambiente. Para manter a compatibilidade, suporte e segurança, é necessário planejar a atualização para a versão 1.32, passando pela versão intermediária 1.31.

## Situação Atual do Ambiente

O ambiente apresenta a seguinte configuração:

* **Versão do Control Plane:** v1.30.10-eks-bc803b4
* **Componentes do Kubernetes:** Todos os componentes principais (scheduler, controller-manager, etcd-0) estão em estado saudável
* **Nodes:** 11 nós em operação, todos na versão v1.30
* **CNI:** amazon-k8s-cni:v1.18.0-eksbuild.1
* **CoreDNS:** v1.11.1-eksbuild.8
* **Kube-proxy:** v1.30.3-minimal-eksbuild.5

## Conceito: Ciclo de Vida das Versões EKS

O Amazon EKS segue um ciclo de suporte para versões do Kubernetes:

* **Suporte Standard:** Aproximadamente 14 meses após o lançamento
* **Suporte Extended:** 12 meses adicionais após o período standard (com custo adicional)
* **Fim de Suporte:** Após o período extended, a versão se torna completamente obsoleta

Baseado na documentação oficial da AWS:

| Versão | Lançamento | Fim do Suporte Standard | Fim do Suporte Extended |
|----|----|----|----|
| 1.30 | 23/05/2024 | 23/07/2025 | 23/07/2026 |
| 1.31 | 26/09/2024 | 26/11/2025 | 26/11/2026 |
| 1.32 | 23/01/2025 | 23/03/2026 | 23/03/2027 |

A versão 1.30 terá seu suporte standard encerrado pela AWS em julho de 2025, entrando em suporte extended com custos adicionais.

## O Problema: Fim do Suporte para a Versão Atual

A continuidade na versão atual apresenta os seguintes riscos:

* Ausência de patches de segurança para vulnerabilidades recém-descobertas
* Falta de suporte técnico oficial para problemas relacionados à versão
* Incompatibilidade com novos recursos e ferramentas do ecossistema Kubernetes
* Potenciais cobranças adicionais pela AWS para continuar usando uma versão fora do suporte standard
* Maior complexidade operacional para manter clusters em versões não suportadas

## Análise Comparativa das Versões

### Kubernetes 1.30 vs 1.31 vs 1.32

| Aspecto | Kubernetes 1.30 | Kubernetes 1.31 | Kubernetes 1.32 | Impacto na Atualização |
|----|----|----|----|----|
| **Suporte AWS** | Termina em julho/2025 | Até novembro/2025 | Até março/2026 | Extensão progressiva de suporte |
| **APIs Deprecadas** | Várias APIs beta suportadas | Remoção de in-tree cloud providers | Mais APIs beta removidas | Migração gradual para APIs estáveis |
| **Plugins kubectl** | Beta | GA | GA | Melhor suporte para extensões de CLI |
| **Storage CSI** | Beta para alguns recursos | CSI Inline Volume GA | Storage Capacity Tracking GA | Melhorias graduais em armazenamento |
| **Job Management** | Recursos básicos | API Batch aprimorada | Job Indexing GA | Melhor suporte para workloads batch |
| **Windows Support** | Limitado | Containers privilegiados | Graceful shutdown | Melhorias para workloads Windows |
| **Topologia** | Alpha/Beta | Melhorias incrementais | Topology GA | Distribuição otimizada de workloads |
| **Validação** | Limitada | Validação de campos melhorada | CRD Validation Rules GA | Melhor prevenção de erros |
| **HPA** | v2beta2 disponível | HPA v2 aprimorado | Container Resource-based HPA GA | Escalonamento mais sofisticado |
| **Segurança** | Recursos básicos | AppArmor GA | Bound service token improvements | Segurança progressivamente aprimorada |
| **Recursos Dinâmicos** | Limitado | VolumeAttributesClass | Dynamic Resource Allocation GA | Melhor suporte para recursos especiais |
| **Observabilidade** | Básica | Melhorias incrementais | Status.hostIPs para Pods | Diagnóstico facilitado |
| **Estabilidade** | Boa | Melhorada | Ainda mais robusta | Menos bugs e problemas |

## Principais Funcionalidades Introduzidas nas Novas Versões

### Kubernetes 1.31 - Principais Recursos


1. **AppArmor Support GA:**
   * Suporte a políticas AppArmor para segurança de containers
   * Melhora o isolamento de segurança e controle de acesso
   * Protege contra comprometimento de containers
2. **Plugins kubectl GA:**
   * O framework de plugins para kubectl foi promovido para Generally Available (GA)
   * Permite estender as funcionalidades do kubectl com plugins personalizados
   * Facilita a criação de comandos personalizados para interagir com o cluster
3. **Containers Windows privilegiados:**
   * Suporte aprimorado para containers Windows com privilégios elevados
   * Melhoria na execução de operações que exigem permissões especiais
   * Importante para workloads específicas que necessitam de acesso privilegiado
4. **Remoção de in-tree cloud providers:**
   * Movimento para usar exclusivamente provedores externos
   * Promove um Kubernetes mais neutro em relação a vendors
   * Melhora a manutenção e separação de responsabilidades
5. **VolumeAttributesClass:**
   * Nova API para gerenciar atributos de volumes
   * Possibilita modificações em volumes persistentes sem recriá-los
   * Oferece mais flexibilidade na gestão de armazenamento
6. **Memory Swap Support GA:**
   * Suporte oficial para troca de memória (swap) no nível do nó
   * Melhora o gerenciamento de recursos para cargas de trabalho com picos de memória
   * Evita terminações de pods por falta de memória
7. **PersistentVolume Phase Transition Time:**
   * Rastreamento de quando os volumes mudam de estado
   * Facilita o diagnóstico de problemas com volumes persistentes
   * Melhora a observabilidade e auditoria
8. **Node-to-Node Connectivity:**
   * Melhorias na confiabilidade da comunicação entre nós
   * Melhor detecção e recuperação de falhas de rede
   * Reduz problemas em migrações e atualizações de nós

### Kubernetes 1.32 - Principais Recursos


1. **Auto-removal de PVCs para StatefulSets GA:**
   * Remoção automática de PVCs (PersistentVolumeClaims) criados por StatefulSets
   * Simplifica o gerenciamento do ciclo de vida dos dados
   * Reduz a necessidade de limpeza manual
2. **Windows Node Graceful Shutdown:**
   * Desligamento mais elegante de nós Windows
   * Permite que pods migrem corretamente antes do desligamento
   * Melhora a confiabilidade em ambientes mistos Windows/Linux
3. **Field Selectors para Custom Resources:**
   * Suporte a seletores de campo para recursos personalizados
   * Facilita filtragem e consulta de objetos CRD
   * Melhora o desempenho de consultas em grandes clusters
4. **Memory-Backed Volumes Sizing:**
   * Controle preciso sobre tamanho dos volumes baseados em memória
   * Melhora previsibilidade para cargas de trabalho que dependem de armazenamento em memória
   * Melhor alocação de recursos para aplicações sensíveis à latência
5. **Bound Service Account Token Improvements:**
   * Melhorias nos tokens de conta de serviço vinculados
   * Informações aprimoradas sobre o nó nos tokens
   * Maior segurança para comunicações pod-a-pod
6. **Recovery from Volume Expansion Failure:**
   * Mecanismos para recuperação de falhas em expansão de volumes
   * Reduz a necessidade de intervenção manual em caso de problemas
   * Aumenta a resiliência de sistemas de armazenamento
7. **VolumeGroupSnapshot API (Beta):**
   * API para realizar snapshots consistentes de múltiplos volumes
   * Importante para aplicações que usam vários volumes interconectados
   * Melhora a consistência de backups e recuperações
8. **Status.hostIPs para Pods:**
   * Nova informação sobre todos os endereços IP do host onde o pod está executando
   * Melhor visibilidade para diagnóstico de problemas de rede
   * Útil para topologias de rede complexas

## Pontos de Atenção na Atualização

### 1. Compatibilidade de APIs

A verificação do ambiente não detectou uso de APIs deprecadas, porém é necessário especial atenção aos seguintes componentes:

* **Ingress Resources:** O cluster possui recursos Ingress que podem ser impactados pela remoção do Ingress v1beta1 na versão 1.31
* **Custom Resources:** Há 46 CRDs instaladas no cluster que precisam ser verificadas quanto à compatibilidade com as novas versões
* **In-tree Cloud Providers:** Verificar se há dependências do código in-tree de cloud providers que foi removido no 1.31

### 2. Pod Disruption Budgets (PDBs)

Foram identificados 10 PDBs no cluster:

* 8 deles estão configurados com maxUnavailable=1
* Deve-se observar o comportamento dos PDBs na versão 1.32, que pode ter mudanças na interpretação dessas configurações

### 3. Componentes do Plano de Dados

O cluster utiliza:

* CoreDNS v1.11.1-eksbuild.8
* Kube-proxy v1.30.3-minimal-eksbuild.5
* amazon-k8s-cni v1.18.0-eksbuild.1

Todos precisarão de atualização para versões compatíveis com Kubernetes 1.31 e 1.32, conforme disponibilizado pela AWS para cada plataforma.

### 4. Workloads Específicos

Os workloads atuais incluem:

* Serviços em namespaces como "apps", "tools" e "monitoring"
* Componentes críticos como cluster autoscaler (Karpenter)
* Services como Loki, OpenSearch e PostgreSQL

É importante verificar a compatibilidade desses componentes com as novas versões de Kubernetes.

## Componentes a Serem Verificados Antes da Atualização

### 1. Componentes Principais

* **Karpenter:** Verificar compatibilidade da versão atual com Kubernetes 1.32
* **EBS CSI Controller:** Confirmar suporte para versão 1.32, especialmente com as mudanças em storage
* **CoreDNS:** Verificar versão compatível com 1.32
* **AWS VPC CNI:** Confirmar compatibilidade com novo Kubernetes
* **Kube-proxy:** Avaliar impacto das melhorias na conectividade entre nós

### 2. Aplicações e Serviços

* **Traefik/NGINX Ingress Controller:** Validar suporte à versão 1.32
* **Prometheus Operator:** Verificar compatibilidade com novas APIs
* **ArgoCD/Workflows:** Confirmar que todas as features usadas são compatíveis
* **Loki:** Verificar necessidade de atualização junto com K8s
* **OpenSearch:** Validar compatibilidade da CRDs com a nova versão

### 3. Configurações e Políticas

* **AppArmor Profiles:** Verificar possibilidade de implementar como recurso estável
* **Network Policies:** Confirmar que as políticas existentes continuarão funcionando
* **SecurityGroupPolicies:** Validar compatibilidade com novas versões
* **StatefulSets:** Avaliar impacto da limpeza automática de PVCs

## Diferenças e Funcionalidades Principais

### Melhorias de Estabilidade

* Melhor gerenciamento de recursos computacionais
* APIs mais estáveis com menos recursos beta
* Aumento da resiliência durante disrupções de nós
* Melhor suporte para operações em grande escala

### Aprimoramentos de Segurança

* Suporte avançado para AppArmor em ambientes containerizados
* Melhorias nos tokens de conta de serviço
* Proteções adicionais contra privilege escalation
* Isolamento aprimorado entre workloads

### Melhorias Operacionais

* Recuperação de falhas de expansão de volume
* Validação aprimorada de recursos para identificar problemas mais cedo
* Melhor observabilidade do cluster com Status.hostIPs
* Capacidades expandidas de autoscaling

### Benefícios de Armazenamento

* Snapshots de grupo de volumes para backups consistentes
* Melhor acompanhamento do uso de capacidade
* Mecanismos avançados para expansão de volumes
* Suporte aprimorado para volumes baseados em memória

## Impacto Técnico da Atualização

### Operações do Cluster

* Durante a atualização do control plane: Possível indisponibilidade breve da API
* Durante a atualização dos nós: Reagendamento de pods entre nós
* Potencial necessidade de ajustes em recursos como PDBs e taints/tolerations
* Ajustes em configurações de monitoramento para novos endpoints

### Aplicações e Workloads

* Impacto mínimo esperado para aplicações que utilizam APIs estáveis
* Possível necessidade de ajustes em aplicações que usam recursos beta
* Atenção especial a workloads com requisitos de alta disponibilidade
* Ajustes em liveness/readiness probes podem ser necessários

### Integrações com AWS

* Transição para cloud-providers externos ao invés dos in-tree
* Ajustes em políticas IAM para novos recursos ou recursos modificados
* Verificação de compatibilidade com features da AWS integradas ao EKS
* Validação de integrações personalizadas entre serviços AWS e Kubernetes

## Considerações Finais

A atualização do Kubernetes EKS de 1.30 para 1.32 representa uma evolução significativa em estabilidade, segurança e funcionalidades. O ambiente atual já está na versão 1.30.10-eks-bc803b4, o que facilita o processo de atualização para as versões mais recentes.

É fundamental realizar testes abrangentes em ambiente de staging, seguindo a abordagem incremental recomendada (1.30 → 1.31 → 1.32) para minimizar riscos. A verificação de compatibilidade de todos os componentes instalados, incluindo CRDs e operadores, é essencial para uma transição bem-sucedida.

Os benefícios da atualização incluem acesso a novas funcionalidades como VolumeGroupSnapshot, storage capacity tracking, melhor recuperação de falhas de expansão de volume, e desligamento gracioso de nós Windows, além de maior segurança com AppArmor e tokens de conta de serviço aprimorados. Com o planejamento adequado e seguindo as melhores práticas, a atualização pode ser realizada com impacto mínimo nas operações.

## Recursos removidos 

Algumas apis foram removidas nas versões 1.31 e 1.32 do K8S , além de algumas que se tornaram depreciadas, vamos apontá-las logo abaixo 

### **1.31**

* **flowcontrol.apiserver.k8s.io/v1beta1** → usar **v1**
* `storage.k8s.io/v1beta1` (CSI Storage Capacity) → usar `v1`

  \

### 1.32

* **batch/v1beta1** (CronJob) → migrar para **batch/v1**
* **discovery.k8s.io/v1beta1** (EndpointSlice) → usar **discovery.k8s.io/v1**
* **events.k8s.io/v1beta1** → usar **events.k8s.io/v1**

## Referências

* [Documentação oficial do Kubernetes sobre v1.31](https://kubernetes.io/blog/2024/08/13/kubernetes-v1-31-release/)
* [Documentação oficial do Kubernetes sobre v1.32](https://kubernetes.io/blog/2024/12/11/kubernetes-v1-32-release/)
* [Versões do Kubernetes no EKS](https://docs.aws.amazon.com/pt_br/eks/latest/userguide/kubernetes-versions.html)
* [Versões de plataforma EKS 1.30](https://docs.aws.amazon.com/pt_br/eks/latest/userguide/platform-versions.html#platform-versions-1-30)
* [Versões de plataforma EKS 1.31](https://docs.aws.amazon.com/pt_br/eks/latest/userguide/platform-versions.html#platform-versions-1-31)
* [Versões de plataforma EKS 1.32](https://docs.aws.amazon.com/pt_br/eks/latest/userguide/platform-versions.html#platform-versions-1-32)
* [Ciclo de vida do Kubernetes no EKS](https://docs.aws.amazon.com/pt_br/eks/latest/userguide/kubernetes-versions-standard.html)
* [Novidades do Kubernetes 1.31 (Sysdig)](https://sysdig.com/blog/whats-new-kubernetes-1-31/)
* [Novidades do Kubernetes 1.32 (Sysdig)](https://sysdig.com/blog/kubernetes-1-32-whats-new/)
* [Novidades na versão 1.31 (Linkedin)](https://pt.linkedin.com/pulse/novidades-na-vers%C3%A3o-131-do-kubernetes-traz-v%C3%A1rias-e-em-nascimento-isulf)
* [Medium: Kubernetes 1.31 new features](https://medium.com/@platform.engineers/kubernetes-1-31-new-features-and-changes-6e7ec041acad)
* [Kubicast 152 - Kubernetes 1.32 (GetUp)](https://getup.io/blog/kubicast-152)
* [Kubernetes 1.32 Penelope (NerdExpert)](https://nerdexpert.com.br/kubernetes-1-32-penelope-novidades-e-avancos-na-orquestracao-de-containers/)