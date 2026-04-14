<!-- title: Growthbook | url: https://outline.seazone.com.br/doc/growthbook-FCHwQQfCg8 | area: Tecnologia -->

# Growthbook

# Documentação Técnica: GrowthBook

Este documento descreve a implementação técnica do [GrowthBook](https://www.growthbook.io/) no cluster Kubernetes da Seazone. O GrowthBook é nossa plataforma de *Feature Flags* e Experimentação (A/B Testing).

## Visão Geral

O GrowthBook foi implantado utilizando uma arquitetura de microsserviços, separando o Frontend e o Backend, ambos gerenciados via GitOps com ArgoCD. A persistência de dados é realizada em um cluster MongoDB compartilhado (MongoDB Tools) e o tráfego é gerenciado pelo Traefik.

### Links Importantes

* **Acesso Web:** <https://ff.seazone.com.br>
* **API Endpoint:** <https://api-ff.seazone.com.br>
* **Repositório de Manifestos:** [seazone-tech/gitops-governanca](https://github.com/seazone-tech/gitops-governanca)
* **Repositório de Charts:** [seazone-tech/helm-charts](https://github.com/seazone-tech/helm-charts) (referência para componentes auxiliares)

## Arquitetura

O diagrama abaixo ilustra os componentes e o fluxo de comunicação do GrowthBook no cluster:

 ![](/api/attachments.redirect?id=974315f7-2336-409e-b7cd-37e351667f4f " =1024x1024")


## Detalhes da Implementação

### 1. ArgoCD Application

A aplicação é gerenciada pelo ArgoCD e definida em `gitops-governanca/argocd/applications/growthbook`. Ela utiliza o padrão "Multiple Sources":


1. **Chart Oficial:** `ghcr.io/growthbook/charts` (Versão 4.1.0).
2. **Values Customizados:** Arquivo `values.yaml` no repositório `gitops-governanca`.
3. **Manifestos Extras:** `external-secret.yaml` e `ingressroute.yaml` no mesmo repositório.

### 2. Configuração (Values)

O arquivo `values.yaml` define as seguintes configurações principais:

* **Frontend:**
  * Réplicas: 2 (min) a 4 (max) com HPA (CPU 75%).
  * Recursos: Requests (100m/256Mi), Limits (500m/512Mi).
* **Backend:**
  * Réplicas: 8 (min) a 16 (max) com HPA (CPU 70%).
  * Recursos: Requests (200m/512Mi), Limits (1000m/2Gi).
  * MongoDB embutido no chart: **Desabilitado** (`mongodb.enabled: false`).
* **Variáveis de Ambiente:**
  * Integração com S3, Email e Banco de Dados via secrets.

### 3. Segredos (External Secrets)

Utilizamos o **External Secrets Operator** para sincronizar segredos da AWS (SSM Parameter Store) para o Kubernetes.

* **Origem AWS:** `/sre/growthbook/production/*`
* **Secret Gerada:** `growthbook-secrets`
* **Chaves Sincronizadas:**
  * `JWT_SECRET`, `ENCRYPTION_KEY`
  * `MONGODB_URI` (Connection string para o MongoDB Tools)
  * Credenciais de Email (`EMAIL_HOST`, `EMAIL_USER`, etc.)
  * Configuração S3 (`S3_BUCKET`)

### 4. Ingress (Traefik)

O acesso externo não é configurado pelo Ingress padrão do chart, mas sim via recursos `IngressRoute` do Traefik definidos em `ingressroute.yaml`.

* **Frontend:** Roteia `ff.seazone.com.br` para o service `growthbook-frontend` na porta 3000.
* **Backend:** Roteia `api-ff.seazone.com.br` para o service `growthbook-backend` na porta 3100.

## Dependências

* **MongoDB Tools:** O GrowthBook depende estritamente do serviço `mongodb-tools` rodando no mesmo namespace (`tools`). Veja a documentação específica do MongoDB Tools para mais detalhes.

## Manutenção e Operação

Para atualizar a versão do GrowthBook ou alterar configurações:


1. Edite o arquivo `argocd/applications/growthbook/application.yaml` (para versão do chart) ou `values.yaml` no repositório `gitops-governanca`.
2. O ArgoCD aplicará as mudanças automaticamente.