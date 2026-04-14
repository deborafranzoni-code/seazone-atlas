<!-- title: [Outline] - Falha por Depreciação de Imagens Bitnami Redis - 09/10/2025 | url: https://outline.seazone.com.br/doc/outline-falha-por-depreciacao-de-imagens-bitnami-redis-09102025-sjJqrh3ENZ | area: Tecnologia -->

# [Outline] - Falha por Depreciação de Imagens Bitnami Redis - 09/10/2025

## 🕒 Data

09/10/2025 - inicio do incidente

10/10/2025 - solução do problema

## 🌍 Ambiente

Produção GCP

## ☁️ Cluster / Conta GCP

tools-440117 / GKE Cluster tools-prod

## 🚨 Descrição do Incidente

O serviço Outline ficou indisponível no namespace `tools`, com todos os pods apresentando status `ImagePullBackOff`. O erro indicava que a imagem `docker.io/bitnami/redis:6.2.6-debian-10-r0` não estava mais disponível, causando falha na inicialização do Redis interno do Outline.

**Impacto:**

* Serviço Outline completamente indisponível
* Usuários não conseguiam acessar `https://outline.seazone.com.br/`
* 4 pods com status `ImagePullBackOff`

**Logs de erro:**

```
Failed to pull image "docker.io/bitnami/redis:6.2.6-debian-10-r0": 
rpc error: code = NotFound desc = failed to pull and unpack image 
"docker.io/bitnami/redis:6.2.6-debian-10-r0": not found
```

## 🧠 Causa Raiz

**Depreciação de imagens gratuitas do Bitnami**: A Bitnami descontinuou o fornecimento gratuito de imagens Docker, migrando para um modelo pago. As imagens antigas foram removidas do Docker Hub, causando falha no pull das imagens Redis necessárias para o funcionamento do Outline.

**Referência:** [Bitnami Deprecates Free Images - Migration Steps](https://northflank.com/blog/bitnami-deprecates-free-images-migration-steps-and-alternatives)

## 🔧 Ações Corretivas Aplicadas

### 1. Criação de Redis Gerenciado no GCP

```bash
# Verificação do projeto e região

gcloud config get-value project
# Output: tools-440117

gcloud config get-value compute/region
# Output: us-central1

# Ativação da API Redis

gcloud services enable redis.googleapis.com

# Criação da instância Redis

gcloud redis instances create redis-tools \
    --region=us-central1 \
    --tier=basic \
    --size=1 \
    --redis-version=redis_7_0 \
    --network=tools-network-prod \
    --connect-mode=private-service-access \
    --project=tools-440117 \
    --display-name="Redis for Tools Application"
```

**Resultado:**

```
Created instance [redis-tools].
IP: 10.23.1.3:6379
```

### 2. Configuração do Outline para Redis Externo

**Modificações no** `**values.yaml**`**:**

```yaml
# Desabilitação do Redis interno

redis:
  enabled: false
  replica:
    enabled: false
  sentinel:
    enabled: false
  metrics:
    enabled: false

# Configuração do Redis externo

externalRedis:
  host: "10.23.1.3"
  port: 6379
  existingSecret: "outline-redis"
  usernameSecretKey: "redis-username"
  passwordSecretKey: "redis-password"
```

**Criação do Secret:**

```yaml

apiVersion: v1

kind: Secret

metadata:
  name: outline-redis
  namespace: tools

data:
  redis-username: ZGVmYXVsdA==  # "default" em base64
  redis-password: ""             # Senha vazia (sem autenticação)
```

### 3. Correção do Chart Helm

**Problema identificado:** O chart estava incompleto, faltando o arquivo `files/entrypoint.sh` necessário para configuração do Redis externo.

**Solução:**

```bash
# Download do chart oficial

helm repo add community-charts https://community-charts.github.io/helm-charts

helm repo update

helm pull community-charts/outline --untar

# Cópia do arquivo entrypoint.sh

cp outline/files/entrypoint.sh /path/to/outline/files/entrypoint.sh

chmod +x /path/to/outline/files/entrypoint.sh
```

**Conteúdo do** `**entrypoint.sh**`**:**

```bash
#!/bin/bash
# Constrói JSON com host, porta, username e password do Redis

JSON=$(printf '{"host":"%s","port":%d,"username":"%s","password":"%s"}' \
  "$REDIS_HOST" "$REDIS_PORT" "$REDIS_USERNAME" "$REDIS_PASSWORD")

# Codifica em base64

BASE64_JSON=$(echo -n "$JSON" | base64)

# Define REDIS_URL no formato ioredis://
export REDIS_URL="ioredis://$BASE64_JSON"

# Executa yarn start

exec yarn start
```

### 4. Remoção do Chart Redis Bitnami

```bash
# Remoção do sub-chart Redis desnecessário

rm charts/redis.15.4.1.tgz
```

## ✅ Resultados

* **Outline restaurado**: 4/4 pods com status `Running`
* **Redis externo funcionando**: Conectividade estabelecida com GCP Memorystore
* **Acesso externo**: Serviço acessível via `https://outline.seazone.com.br/`
* **Port-forward funcionando**: `kubectl port-forward service/outline 8080:80` retorna HTTP 200 OK
* **Logs limpos**: Sem erros de conexão Redis

**Logs de sucesso:**

```
{"label":"lifecycle","level":"info","message":"Starting collaboration service"}
{"label":"lifecycle","level":"info","message":"Starting websockets service"}
{"label":"lifecycle","level":"info","message":"Starting worker service"}
{"label":"lifecycle","level":"info","message":"Starting web service"}
{"label":"lifecycle","level":"info","message":"Listening on http://localhost:3000 / https://outline.seazone.com.br"}
```

## 🔎 Verificações

```bash
# Status dos pods

kubectl get pods -n tools | grep outline
# Output: 4/4 Running

# Teste de conectividade

kubectl port-forward service/outline 8080:80 -n tools &
curl -I http://localhost:8080
# Output: HTTP/1.1 200 OK

# Verificação do serviço

kubectl get service outline -n tools
# Output: ClusterIP 10.17.2.138:80

# Verificação dos endpoints

kubectl get endpoints outline -n tools
# Output: 4 pods conectados corretamente
```

## 📝 Ações a serem tomadas


1. **Checar serviços que dependem de imagens Bitnami**: Validar se existem serviços que dependem de imagens Bitnami.

## 🏷️ Tags

\#outline #redis #bitnami #gcp #memorystore #helm #deprecation

## 👥 Responsáveis

[john.paiva@seazone.com.br](mailto:john.paiva@seazone.com.br)