<!-- title: n8n | url: https://outline.seazone.com.br/doc/n8n-ujEjkYewaz | area: Tecnologia -->

# n8n

# Documentação Técnica

## Introdução

Esta documentação descreve em detalhes a implementação e configuração do n8n utilizando um cluster Kubernetes através de Helm Charts, conforme implantado na infraestrutura da Seazone. O documento aborda conceitos fundamentais da ferramenta, arquitetura implementada, componentes do sistema e suas relações, configurações e estratégias de escalabilidade.

## O que é o n8n?

O n8n é uma plataforma de automação de fluxos de trabalho (workflow automation) de código aberto que permite criar, configurar e executar automações entre diferentes sistemas e aplicações. Diferente de ferramentas semelhantes como Zapier ou Make (Integromat), o n8n pode ser hospedado localmente, oferecendo maior controle sobre seus dados e possibilidades de personalização.

### Características Principais

* **Interface visual intuitiva**: Criação de fluxos de trabalho usando uma interface gráfica de "arrastar e soltar"
* **Código aberto**: Possibilidade de estender funcionalidades e auditar o código
* **Self-hosted**: Controle total sobre dados e infraestrutura
* **Mais de 300 integrações**: Conectores pré-construídos para diversos serviços e aplicações
* **Personalização avançada**: Suporte a JavaScript em nós de função para lógica personalizada
* **Webhooks**: Receber e processar eventos externos em tempo real
* **Execuções agendadas**: Automatizar tarefas com base em cronogramas específicos
* **Modo de fila (queue mode)**: Processamento assíncrono e distribuído para maior escalabilidade

### Referências e Links Oficiais

* [Site oficial do n8n](https://n8n.io/)
* [Documentação oficial](https://docs.n8n.io/)
* [Repositório GitHub](https://github.com/n8n-io/n8n)
* [Integrações disponíveis](https://n8n.io/integrations)

## Arquitetura do n8n em Modo de Fila

Nossa implementação do n8n utiliza uma arquitetura distribuída em modo de fila (queue mode), separando o sistema em três componentes principais para maior escalabilidade e resiliência.

### Visão Geral dos Componentes

 ![Arquitetura n8n](https://docs.n8n.io/assets/img/deployment_architecture-26a7d08f2637f80b10b4d70599a03213.png)

O n8n em nossa implementação é composto por três componentes principais, além de dois serviços de apoio:


1. **Editor**: Interface web para gerenciamento de workflows
2. **Webhook**: Componente responsável pelo recebimento de eventos HTTP
3. **Worker**: Responsável pela execução assíncrona dos workflows
4. **PostgreSQL**: Banco de dados para armazenamento persistente
5. **Redis**: Sistema de mensageria e cache para o modo de fila

### Como os Componentes se Relacionam

#### Editor (n8n-editor)

O Editor é a interface principal onde os usuários interagem com o n8n. Ele fornece:

* Interface web para criar, editar e gerenciar workflows
* Painel de controle para monitorar execuções
* Gerenciamento de credenciais e variáveis
* Acesso a logs e histórico de execuções

No modo de fila, o Editor não executa workflows em produção, delegando esta responsabilidade aos Workers. Em vez disso, ele:


1. Armazena definições de workflows no PostgreSQL
2. Permite execuções de teste diretamente na interface
3. Enfileira execuções para processamento pelos Workers via Redis
4. Oferece uma visão do estado das execuções em andamento e concluídas

#### Webhook (n8n-webhook)

O componente Webhook recebe e processa eventos HTTP externos que acionam workflows. Suas principais funções:

* Expor endpoints HTTP para receber requisições externas
* Validar e autenticar solicitações recebidas
* Enfileirar execuções para processamento pelos Workers
* Responder rapidamente aos chamadores externos

Este componente é otimizado para responder rapidamente a picos de tráfego, com políticas de escalabilidade agressivas para garantir alta disponibilidade dos endpoints de webhook.

#### Worker (n8n-worker)

Os Workers são responsáveis pelo processamento efetivo dos workflows. Eles:

* Consomem tarefas da fila Redis
* Executam os nós de workflow sequencialmente
* Processam execuções agendadas automaticamente
* Gerenciam execuções manuais iniciadas pelo usuário
* Armazenam resultados e logs no PostgreSQL

Os Workers são altamente escaláveis, permitindo processar múltiplas execuções simultaneamente conforme a carga aumenta.

#### Modo de Fila (Queue Mode)

O modo de fila é central para nossa arquitetura, permitindo:

* Separação de recepção (webhook) e processamento (worker)
* Execuções assíncronas distribuídas entre múltiplos workers
* Maior disponibilidade para receber webhooks, mesmo durante alta carga
* Balanceamento automático de carga entre workers
* Resiliência a falhas com processamento distribuído

O Redis atua como o backend da fila, gerenciando o estado das execuções e facilitando a comunicação entre os componentes.

## Implementação com Helm Chart

Nossa implementação do n8n utiliza Helm Charts para gerenciar a infraestrutura no Kubernetes. O chart inclui todos os recursos necessários para implantar e configurar o n8n em modo de fila.

### Componentes Implantados

#### Deployments


1. **n8n-editor.yaml**: UI principal para gerenciamento de workflows

   ```yaml
   replicas: 1
   autoscaling:
     minReplicas: 1
     maxReplicas: 3
     targetCPUUtilizationPercentage: 80
   ```
2. **n8n-webhook.yaml**: Endpoint para recebimento de eventos externos

   ```yaml
   replicas: 1
   autoscaling:
     minReplicas: 2
     maxReplicas: 8
     targetCPUUtilizationPercentage: 60
     targetMemoryUtilizationPercentage: 70
   ```
3. **n8n-worker.yaml**: Processamento assíncrono de workflows

   ```yaml
   replicas: 1
   autoscaling:
     minReplicas: 2
     maxReplicas: 12
     targetCPUUtilizationPercentage: 70
     targetMemoryUtilizationPercentage: 75
   ```
4. **postgres.yaml**: Banco de dados PostgreSQL para armazenamento persistente

   ```yaml
   image: postgres:14-alpine
   persistence:
     enabled: true
     size: 5Gi
   ```
5. **redis.yaml**: Cache e sistema de mensageria para o modo de fila

   ```yaml
   image: redis:7-alpine
   persistence:
     enabled: true
     size: 1Gi
   ```

#### Horizontal Pod Autoscaler (HPAs)

Cada componente do n8n possui seu próprio HPA com configurações específicas:


1. **n8n-editor-hpa.yaml**: Escalabilidade mais conservadora
   * Escala de 1-3 pods
   * Métrica de CPU em 80%
   * Janelas de estabilização longas para evitar oscilações
2. **n8n-webhook-hpa.yaml**: Resposta rápida a picos de tráfego
   * Escala de 2-8 pods
   * Métrica de CPU em 60% e memória em 70%
   * Políticas agressivas de escala para cima (50% a cada 30s)
   * Escala para baixo conservadora (10% a cada 60s)
3. **n8n-worker-hpa.yaml**: Alta capacidade para processamento intenso
   * Escala de 2-12 pods
   * Métrica de CPU em 70% e memória em 75%
   * Estratégia dupla de escala (% e número fixo de pods)
   * Janela de estabilização curta para escala para cima (30s)

#### Persistent Volume Claims (PVCs)


1. **n8n-pvc.yaml**: Persistência para o editor do n8n

   ```yaml
   size: 1Gi
   storageClass: standard-rwo
   ```
2. **postgres-pvc.yaml**: Armazenamento para o PostgreSQL

   ```yaml
   size: 5Gi
   storageClass: standard-rwo
   ```
3. **redis-pvc.yaml**: Persistência para o Redis

   ```yaml
   size: 1Gi
   storageClass: standard-rwo
   ```

#### Ingress e Roteamento

O roteamento é gerenciado por um IngressRoute do Traefik:

```yaml

apiVersion: traefik.io/v1alpha1

kind: IngressRoute

metadata:
  name: n8n-ingressroute

spec:
  entryPoints:
    - web  # Configurado para web (porta 80) para uso com Cloudflare em modo Flexível
  routes:
    - match: Host(`n8n.seazone.com.br`) && PathPrefix(`/webhook-test`)
      services:
        - name: n8n-editor
          port: 5678

    - match: Host(`n8n.seazone.com.br`) && PathPrefix(`/webhook`)
      services:
        - name: n8n-webhook
          port: 5678
      
    - match: Host(`n8n.seazone.com.br`) && PathPrefix(`/`)
      services:
        - name: n8n-editor
          port: 5678
```

Este modelo de roteamento:

* Direciona `/webhook` para o componente webhook
* Direciona `/webhook-test` para o editor
* Envia todo o restante do tráfego para o editor

#### Configurações e Variáveis de Ambiente

Cada componente do n8n compartilha variáveis de ambiente comuns, além de configurações específicas para sua função:


1. **Variáveis comuns a todos os componentes**:

   ```
   - DB_TYPE: "postgresdb"
   - DB_POSTGRESDB_HOST: "postgres-n8n"
   - EXECUTIONS_MODE: "queue"
   - QUEUE_BULL_REDIS_HOST: "redis-n8n"
   - N8N_METRICS: "true"
   - N8N_METRICS_INCLUDE_QUEUE_METRICS: "true"
   - QUEUE_HEALTH_CHECK_ACTIVE: "true"
   ```
2. **Variáveis específicas para o Editor**:

   ```
   - N8N_DISABLE_PRODUCTION_MAIN_PROCESS: "true"
   - N8N_TRUSTED_PROXIES: "*"
   ```
3. **Variáveis específicas para o Webhook**:

   ```
   - N8N_ENDPOINT_WEBHOOK: "webhook"
   - N8N_ENDPOINT_WEBHOOK_TEST: "webhook-test"
   ```
4. **Variáveis específicas para o Worker**:

   ```
   - N8N_CONCURRENCY_PRODUCTION_LIMIT: "20"
   ```

### Configuração de Segurança

O n8n é configurado com várias medidas de segurança:


1. **Secrets**:
   * `postgres-secret.yaml`: Armazena a senha do PostgreSQL e chave de criptografia
   * `n8n-secret.yaml`: Armazena configurações sensíveis como JWT secret
   * `smtp-secret.yaml`: Armazena credenciais de email para notificações
2. **Contexto de segurança**:

   ```yaml
   securityContext:
     fsGroup: 1000
     runAsUser: 1000
     runAsGroup: 1000
   ```
3. **Gerenciamento de usuários**:

   ```yaml
   userManagement:
     enabled: true
     jwtSecret: <secret>
     jwtDurationHours: 168  # 7 dias
   ```
4. **Integração com SMTP**:

   ```yaml
   smtp:
     enabled: true
     host: "smtp.gmail.com"
     port: 587
     secure: false
     startTLS: true
     sender: "n8n <governancatech@seazone.com.br>"
   ```
5. **Integração com Cloudflare**:
   * Configurado para usar Cloudflare em modo Flexível
   * TLS terminado no Cloudflare, comunicação interna via HTTP

## Estratégia de Escalabilidade

A estratégia de escalabilidade do n8n é baseada em:


1. **Arquitetura distribuída**: Separação de responsabilidades entre Editor, Webhook e Worker
2. **Modo de fila**: Processamento assíncrono via Redis
3. **HPAs configurados por componente**: Regras específicas para cada tipo de carga
4. **Gestão de persistência**: Persistência apenas onde necessária para permitir escala horizontal
5. **Configuração de recursos otimizada**:

   ```yaml
   resources:
     requests:
       memory: "256Mi"
       cpu: "100m"
     limits:
       memory: "512Mi"
       cpu: "500m"
   ```

### Considerações para Escala

* **PostgreSQL**: Pode se tornar um gargalo em alta escala. Considerar otimizações ou serviços gerenciados
* **Redis**: Essencial para o modo de fila. Monitorar utilização
* **Componente Webhook**: Escalado para responder rapidamente a picos de tráfego
* **Componente Worker**: Maior capacidade de escala para processamento de cargas intensas
* **Métricas**: Habilitar métricas para monitoramento detalhado

## Benchmark e Testes de Carga

O Helm Chart inclui funcionalidades para testar a capacidade e desempenho da instalação do n8n:

### Scripts de Benchmark

Localização: `/benchmark/scripts/`

* `webhook-basic.js`: Teste básico de carga em webhooks
* `webhook-patterns.js`: Testes de diferentes padrões de tráfego
* `webhook-hpa.js`: Teste para validar o comportamento do HPA

### Como Executar os Testes

```bash

cd helm-charts/prod/n8n-helm/benchmark

make basic      # Executa o teste básico

make patterns   # Executa o teste de padrões

make hpa        # Executa o teste de HPA

make all        # Executa todos os testes
```

### Métricas Importantes para Análise

* **Throughput**: Requisições por segundo processadas
* **Latência**: Tempo de resposta (p95, p99, média)
* **Taxa de erros**: Porcentagem de falhas
* **Uso de recursos**: Consumo de CPU e memória
* **Comportamento de escala**: Validação das políticas de HPA

## Manutenção e Resolução de Problemas

### Comandos comuns para gerenciamento

```bash
# Verificar status dos pods

kubectl get pods -n n8n

# Verificar logs do editor

kubectl logs -f -l app=n8n-editor -n n8n

# Verificar logs do webhook

kubectl logs -f -l app=n8n-webhook -n n8n

# Verificar logs dos workers

kubectl logs -f -l app=n8n-worker -n n8n

# Monitorar o autoscaling

kubectl get hpa -n n8n

# Acessar o shell de um pod

kubectl exec -it <nome-do-pod> -n n8n -- /bin/sh
```

### Problemas Comuns e Soluções


1. **Erro na conexão com o PostgreSQL**
   * Verificar se o StatefulSet do PostgreSQL está funcionando
   * Checar logs do PostgreSQL com `kubectl logs -f -l app=postgres -n n8n`
   * Validar credenciais e conectividade entre os serviços
2. **Erro na conexão com o Redis**
   * Verificar o status do Deployment do Redis
   * Checar logs do Redis com `kubectl logs -f -l app=redis -n n8n`
   * Validar conectividade na porta 6379
3. **IngressRoute não acessível**
   * Verificar configuração do Traefik
   * Validar DNS e configuração do Cloudflare
   * Testar conectividade interna com `kubectl port-forward`
4. **Execuções de workflow presas na fila**
   * Verificar logs dos Workers
   * Validar configuração de limites de concorrência
   * Checar estado do Redis e PostgreSQL

## Backup e Recuperação

Os dados críticos do n8n são armazenados em:


1. **PostgreSQL**: Contém workflows, credenciais, variáveis e histórico de execuções
2. **Redis**: Estado temporário das filas (menos crítico para backup)
3. **Volume Persistente do Editor**: Alguns dados locais do n8n

Recomendações para backup:

```bash
# Backup do PostgreSQL

kubectl exec -n n8n <postgres-pod> -- pg_dump -U postgres n8n > n8n_backup.sql

# Restauração do PostgreSQL

cat n8n_backup.sql | kubectl exec -i -n n8n <postgres-pod> -- psql -U postgres n8n
```

O GKE Backup para o namespace n8n também está configurado como parte da implementação.

## Conclusão

O n8n implementado através deste Helm Chart oferece uma plataforma de automação robusta, escalável e resiliente. A arquitetura distribuída em modo de fila permite processar grandes volumes de execuções de workflow, respondendo eficientemente a picos de carga.

### Recursos Adicionais

* [Documentação oficial do n8n](https://docs.n8n.io/)
* [GitHub do n8n](https://github.com/n8n-io/n8n)
* [Configuração de concorrência](https://docs.n8n.io/hosting/scaling/concurrency-control/)
* [Monitoramento e métricas](https://docs.n8n.io/hosting/metrics/)