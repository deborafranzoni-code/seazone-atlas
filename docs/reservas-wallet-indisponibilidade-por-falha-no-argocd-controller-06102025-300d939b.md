<!-- title: [Reservas, Wallet] - Indisponibilidade por Falha no ArgoCD Controller - 06/10/2025 | url: https://outline.seazone.com.br/doc/reservas-wallet-indisponibilidade-por-falha-no-argocd-controller-06102025-s5kvhk65DR | area: Tecnologia -->

# [Reservas, Wallet] - Indisponibilidade por Falha no ArgoCD Controller - 06/10/2025

# 📌 Reservas, Wallet - Indisponibilidade por Falha no ArgoCD Controller - 06/10/2025

## 🕒 Data

06/10/2025

## 🌍 Ambiente

Produção

## ☁️ Cluster / Conta AWS

General Cluster/Production

## 🚨 Descrição do Incidente

O site principal do Reservas e Wallet apresentou erro 404 (página não encontrada) para os usuários finais, resultando em indisponibilidade completa do serviço.

**Como foi percebido:**

* Alerta inicial no Kuma indicando que o site [reservas](https://seazone.com.br) estava inacessível, Seguido pelo mesmo alerta para o [Wallet](https://wallet.seazone.com.br/sign-in) alguns minutos após.

**Investigação inicial:** A equipe começou investigando os pods em produção via `prd-apps` e identificou estouro de memória em alguns pods. Análise dos logs via Lens mostrou que os logs dos serviços Wallet e Reservas estavam aparentemente normais. Verificação ([Lens](https://k8slens.dev), `kubectl get events`) não mostrou anomalias nos eventos do sistema (criação/deleção de containers, health checks).

A verificação do [Traefik](https://nerdexpert.com.br/entendendo-o-traefik/) (proxy reverso e encaminhador de tráfego) indicou que os pods estavam operacionais. Porém, ao analisar o ArgoCD, foi identificado que estava sincronizando infinitamente (loop de sincronização) e apresentando múltiplos restarts no [ArgoCD Controller](https://argo-cd.readthedocs.io/en/release-2.8/operator-manual/server-commands/argocd-application-controller/), que estava morrendo continuamente.

**Impacto:**

* Serviços afetados: Wallet e Reservas
* Usuários impactados: Todos os usuários tentando acessar os sites durante o período
* Duração: Aproxinadamente 10 a 13 minutos

## 🧠 Causa Raiz

O ArgoCD Controller (componente responsável por monitorar o estado desejado das aplicações no Git, comparar com o estado atual no cluster e aplicar mudanças necessárias) estava configurado com limite de memória insuficiente.

**O problema:**


1. Ao tentar sincronizar duas novas aplicações simultaneamente, o Controller excedeu o limite de memória configurado
2. O Kubernetes matou o processo (OOMKilled - Out Of Memory Killed)
3. O Controller reiniciava automaticamente, mas voltava a morrer ao tentar sincronizar novamente
4. Isso gerou um loop infinito de restart

**Impacto na infraestrutura:** As [IngressRoutes](https://doc.traefik.io/traefik/reference/routing-configuration/kubernetes/crd/http/ingressroute/) (rotas de entrada do Traefik) estavam sendo recriadas, mas o estado das aplicações não conseguia ser sincronizado completamente. Como o IngressRoute não estava sendo criado/atualizado corretamente pelo ArgoCD, o Traefik não conseguia rotear as requisições corretamente, resultando em erro 404.

**Fluxo quebrado:**

```mermaidjs

graph LR
    A[Usuário] -->|Requisição HTTPS| B[Cloudflare]
    B -->|Proxy| C[Traefik]
    C -->|Busca rota| D[IngressRoute ❌ QUEBRADO]
    D -.->|404 - Rota não encontrada| E[Pods]
    
    style D fill:#ff6b6b,stroke:#c92a2a,stroke-width:3px,color:#fff
    style A fill:#4dabf7,stroke:#1971c2,stroke-width:2px
    style B fill:#51cf66,stroke:#2f9e44,stroke-width:2px
    style C fill:#ffd43b,stroke:#fab005,stroke-width:2px
    style E fill:#dee2e6,stroke:#868e96,stroke-width:2px
```

> Nota: Aplicações que não dependiam de sincronização de novos IngressRoutes no momento continuaram funcionando normalmente.

## 🔧 Ações Corretivas Aplicadas

**1. Aumento do limite de memória do ArgoCD Controller**

```bash

kubectl edit deployment argocd-application-controller -n argocd
```

Alteração aplicada no deployment:

```yaml

resources:
  limits:
    memory: 2Gi  # Aumentado para 2GB
  requests:
    memory: 1Gi
```

**2. Forçar sincronização manual das aplicações**

```bash

argocd app sync <nome-da-aplicacao> --force
```

**3. Validação da recriação dos IngressRoutes**

```bash

kubectl get ingressroute -n prd-apps

kubectl get pods -n argocd
```

## ✅ Resultados

Após a aplicação das correções:

* ArgoCD Controller estabilizado sem mais restarts
* Sincronização normalizada com todas as aplicações sincronizadas com sucesso
* IngressRoutes criados e rotas de tráfego restabelecidas
* Serviços Wallet e Reservas restaurados

## 🔎 Verificações

Comandos utilizados para validar a resolução:

```bash
# Verificar saúde do ArgoCD Controller

kubectl get pods -n argocd

kubectl top pod -n argocd

# Confirmar sincronização das aplicações

argocd app list

argocd app get <nome-da-aplicacao>

# Validar IngressRoutes

kubectl get ingressroute -A

# Testar acesso aos sites

curl -I https://seazone.com.br

curl -I https://wallet.seazone.com.br/sign-in
```

## 📝 Recomendações Futuras



1. Configurar alertas no Prometheus/Grafana para uso de memória do ArgoCD Controller com threshold de alerta em 80% do limite
2. Auditar limites (requests/limits) dos componentes críticos da infraestrutura
3. Configurar sincronização de aplicações em lotes menores e implementar rate limiting no ArgoCD para evitar sobrecarga
4. Implementar tracing distribuído para correlacionar eventos entre ArgoCD, Traefik e aplicações

## 🏷️ Tags

> ==#argocd== ==#kubernetes== ==#ingress== ==#traefik== ==#gitop==s ==#infra== ==#production==

## 👥 Responsáveis

[john.paiva@seazone.com.br](mailto:john.paiva@seazone.com.br) 

[guilherme.santos@seazone.com.br](mailto:guilherme.santos@seazone.com.br)