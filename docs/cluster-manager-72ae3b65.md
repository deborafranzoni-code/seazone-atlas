<!-- title: Cluster Manager | url: https://outline.seazone.com.br/doc/cluster-manager-furUdN6Hd6 | area: Tecnologia -->

# Cluster Manager

# Cluster Manager — System Price

> **Branch:** `feature/cluster-system-price` · **Repo:** `seazone-tech/gcp-data-resources`


---

## Visão Geral

Antes desta feature, a atribuição de uma categoria de imóvel a um cluster do System Price era feita manualmente: alguém do time precisava saber de cabeça (ou perguntar) qual cluster fazia sentido para uma nova categoria. Isso criava gargalo de conhecimento e risco de atribuições inconsistentes.

Esta feature entrega dois avanços:


1. **Sugestão ML de cluster** — um modelo GMM analisa o comportamento histórico de preços da categoria (posicionamento competitivo frente a concorrentes) e sugere qual cluster ela mais se assemelha, com score de probabilidade.
2. **Interface web de gestão** — uma UI completa para visualizar, editar e auditar a tabela `cluster_category` do System Price, com histórico de alterações e acionamento do recálculo direto pelo browser.


---

## O que foi adicionado

| Componente | Tipo | Responsabilidade |
|----|----|----|
| `compute-cluster-features` | Cloud Function (HTTP) | Pipeline mensal de features competitivas de preço por categoria |
| `suggest-cluster` | Cloud Run (HTTP) | Sugere cluster via GMM com base nas features calculadas |
| `list-clusters` | Cloud Run (HTTP) | Lista todos os clusters e suas categorias |
| `list-valid-categories` | Cloud Run (HTTP) | Lista categorias disponíveis com status de saúde e eligibilidade |
| `list-cluster-history` | Cloud Run (HTTP) | Lista e restaura snapshots históricos do `cluster_category` |
| `cluster-manager-ui` | Cloud Run (Next.js) | Interface web de gestão com autenticação Google OAuth |


---

## Arquitetura

```
[Cloud Scheduler — mensal]
        │
        ▼
compute-cluster-features
   (Athena: pricingdata, competitorsdata, inputdata)
        │ WRITE_TRUNCATE
        ▼
BigQuery: system_price.cluster_category_features
        │
        └──────────────────────────────────────┐
                                               ▼
                                        suggest-cluster
                                     (GMM — PCA + RobustScaler)
                                               │
                                        ┌──────▼──────┐
                                        │             │
                                   list-clusters  list-valid-categories
                                        │             │
                                        └──────┬──────┘
                                               ▼
                                      cluster-manager-ui
                                    (Next.js — Google OAuth)
                                               │
                                    ┌──────────▼──────────┐
                                    │                     │
                              upsert-cluster    list-cluster-history
                              (já existia)      (snapshots no GCS)
                                    │
                                    ▼
                        calculate-aggressiveness-prices
                           (recálculo do System Price)
```

**Dados que fluem:**

* `compute-cluster-features` lê 12 meses de preços internos (`last_offered_price`) e de concorrentes (`daily_revenue_competitors`) do Athena, calcula o percentil competitivo de preço por categoria e salva em BigQuery.
* `suggest-cluster` lê essas features + saúde de cluster do BigQuery, treina um GMM on-the-fly e retorna scores de probabilidade por cluster.
* A UI consome todos os endpoints de leitura e aciona `upsert-cluster` (gravação) e `calculate-aggressiveness-prices` (recálculo) via API Gateway.


---

## Serviços Novos

### `compute-cluster-features`

**O que faz:** Pipeline mensal que calcula o posicionamento competitivo de preços de cada categoria. Para cada categoria sazonal, compara o preço médio Seazone com a distribuição de preços dos concorrentes (separando dias de semana, fim de semana, feriados e eventos) e calcula estatísticas de percentil.

**Trigger:** HTTP — deve ser acionado mensalmente via Cloud Scheduler ou manualmente.

**Fontes de dados (Athena):**

* `inputdata.climate` — categorias ativas e sazonalidade
* `pricingdata.last_offered_price` — preços Seazone (últimos 12 meses)
* `competitorsdata.daily_revenue_competitors` — preços de concorrentes ativos
* `inputdata.holidays` — feriados e eventos por categoria

**Output:** Tabela `system_price.cluster_category_features` no BigQuery (WRITE_TRUNCATE a cada execução).

**Variáveis de ambiente obrigatórias:**

| Variável | Descrição |
|----|----|
| `PROJECT_ID` | ID do projeto GCP |
| `AWS_ACCESS_KEY_ID` | Chave de acesso AWS |
| `AWS_SECRET_ACCESS_KEY` | Secret AWS |
| `DB_PRICING` | Database Athena do pricing (ex: `pricingdata-xxxxx`) |
| `DB_COMPETITORS` | Database Athena dos competidores |
| `DB_INPUT` | Database Athena do input |
| `ATHENA_WORKGROUP` | Workgroup Athena (padrão: `primary`) |
| `WEBHOOK_URL` | Webhook Slack para alertas de erro |

> **Atenção:** Os databases Athena têm sufixos aleatórios do CloudFormation — nunca hardcodar. Usar sempre variáveis de ambiente.

**Critério de inclusão:** Somente categorias com ao menos 9 meses de dados históricos de preço são incluídas no output.

**Categorias excluídas (não-sazonais):** `Não sazonal`, categorias de Goiânia, Brasília e São Paulo/Pinheiros definidas como não-sazonais no `climate`.


---

### `suggest-cluster`

**O que faz:** Dado o nome de uma categoria, retorna uma lista de clusters ordenados por score de similaridade. O modelo é um GMM (Gaussian Mixture Model) treinado on-the-fly com as categorias já atribuídas a clusters.

**Trigger:** HTTP GET — `?category=<nome_da_categoria>`

**Lógica:**


1. Busca todos os clusters existentes com features do BigQuery (ricas + básicas).
2. Determina a sazonalidade da categoria-alvo.
3. Filtra apenas clusters com o mesmo perfil de sazonalidade (sazonais vs não-sazonais por maioria).
4. Constrói matriz de features: `health_score`, `qtd_concorrentes`, `perc_preco_incompativel`, strata, tipo e quartos (extraídos do nome da categoria) + features de percentil do `cluster_category_features` se disponíveis.
5. Aplica `SimpleImputer` + `RobustScaler` + `PCA` (redução para 95% da variância, somente com features ricas).
6. Treina GMM com tantos componentes quantos clusters existentes.
7. Retorna probabilidade de pertencimento a cada cluster.

**Resposta:**

```json
{
  "category": "Clima-Floripa-Centro-apartamento-SUP-2Q",
  "model": "GMM",
  "has_rich_features": true,
  "sazonal": true,
  "suggestions": [
    { "cluster": "cluster_A", "score": 68.3, "num_categories": 12 },
    { "cluster": "cluster_B", "score": 21.1, "num_categories": 8 }
  ]
}
```

**Fallback:** Se `cluster_category_features` não estiver disponível, o modelo roda com features básicas apenas (score menos preciso).

**Variáveis de ambiente:**

| Variável | Descrição |
|----|----|
| `PROJECT_ID` | ID do projeto GCP |
| `ALLOWED_ORIGINS` | Origens CORS permitidas (separadas por vírgula) |
| `WEBHOOK_URL` | Webhook Slack |


---

### `list-clusters`

**O que faz:** Lista todos os clusters com suas categorias agrupadas e flag de sazonalidade.

**Trigger:** HTTP GET — sem parâmetros.

**Resposta:**

```json
{
  "clusters": [
    {
      "cluster": "cluster_A",
      "categories": ["Cat-1", "Cat-2"],
      "sazonal": true,
      "mixed": false
    }
  ],
  "total_categories": 42
}
```

O campo `mixed: true` indica que o cluster tem categorias sazonais e não-sazonais misturadas (situação a ser corrigida).


---

### `list-valid-categories`

**O que faz:** Lista categorias disponíveis para atribuição a clusters, com informações de eligibilidade e saúde.

**Trigger:** HTTP GET — parâmetro opcional `?search=<termo>` filtra por nome de categoria (ILIKE).

**Resposta:**

```json
{
  "categories": [
    {
      "category": "Clima-Floripa-Centro-apartamento-SUP-2Q",
      "eligible": true,
      "has_matrix": true,
      "status": "verde",
      "qtd_concorrentes": 24,
      "sazonal": true
    }
  ]
}
```

**Campos de status:** `verde`, `amarelo`, `vermelho` (health score do cluster de concorrentes) ou `sem_dados`.


---

### `list-cluster-history`

**O que faz:** Lista ou restaura snapshots históricos da tabela `cluster_category`, salvos no GCS como Parquet a cada `upsert-cluster`.

**Trigger:** HTTP GET

* **Sem parâmetros** → retorna lista de entradas do histórico (timestamp, tamanho, data de atualização) lidas via metadata do GCS (sem abrir os Parquets).
* **Com** `**?timestamp=<ts>**` → retorna o snapshot completo daquele momento.

**Resposta (lista):**

```json
{
  "history": [
    {
      "timestamp": "2026-04-09T14:23:00",
      "updated_by": "user@seazone.com.br",
      "total_categories": 45
    }
  ]
}
```

Os snapshots ficam no GCS em `gs://<BUCKET_SYSTEM_PRICE>/cluster_category/timestamp=<ts>/`.


---

## Interface Web — `cluster-manager-ui`

**O que é:** Aplicação Next.js 16 (TypeScript + Tailwind) para gerenciar a tabela `cluster_category` do System Price de forma visual.

**Acesso:** Cloud Run — autenticação obrigatória via Google OAuth (NextAuth). Somente usuários autenticados conseguem fazer alterações.

**O que a UI permite fazer:**

| Ação | Descrição |
|----|----|
| Visualizar clusters | Tabela agrupada por cluster com todas as categorias |
| Adicionar categoria | Adiciona uma categoria existente a um cluster, com sugestão ML |
| Criar novo cluster | Cria um cluster novo e já atribui categorias iniciais |
| Remover categoria | Remove uma categoria de um cluster (via menu de contexto) |
| Ver sugestão de cluster | Para qualquer categoria, exibe os scores do GMM antes de confirmar |
| Histórico | Drawer lateral com lista de snapshots; permite visualizar qualquer versão anterior |
| Recalcular preços | Botão que aciona `calculate-aggressiveness-prices` diretamente da UI |
| Dark/Light mode | Toggle de tema |

**Arquitetura do frontend:**

```
Browser
  └── Next.js App Router
        ├── /api/auth/[...nextauth]  — OAuth Google
        └── /api/proxy/[...path]    — Proxy server-side para API Gateway
                                      (API key nunca vai ao browser)
```

Em produção, todas as chamadas aos serviços passam pelo proxy `/api/proxy/*`, que injeta a `API_KEY` server-side. Em desenvolvimento, é possível apontar `NEXT_PUBLIC_API_*` diretamente para os Cloud Run services (sem proxy).

**Variáveis de ambiente (**`**.env**`**):**

| Variável | Descrição |
|----|----|
| `API_BASE_URL` | URL do API Gateway (ex: `https://gt-system-price-xxxxx.uc.gateway.dev`) |
| `API_KEY` | x-api-key do API Gateway |
| `GOOGLE_CLIENT_ID` | Client ID do OAuth Google |
| `GOOGLE_CLIENT_SECRET` | Secret do OAuth Google |
| `NEXTAUTH_URL` | URL pública da aplicação |
| `NEXTAUTH_SECRET` | Secret aleatório para JWT do NextAuth |


---

## Tabelas BigQuery criadas

### `system_price.cluster_category_features`

Criada e mantida pelo `compute-cluster-features`. Atualizada mensalmente com WRITE_TRUNCATE.

| Coluna | Tipo | Descrição |
|----|----|----|
| `category` | STRING | Nome da categoria |
| `media_precos_ocupados` | FLOAT | Média do percentil do preço Seazone vs concorrentes ocupados |
| `media_precos_mix` | FLOAT | Média do percentil vs todos os concorrentes |
| `mediana_precos_ocupados` | FLOAT | Mediana do percentil vs ocupados |
| `mediana_precos_mix` | FLOAT | Mediana do percentil vs todos |
| `std_precos_ocupados` | FLOAT | Desvio padrão do percentil vs ocupados |
| `std_precos_mix` | FLOAT | Desvio padrão do percentil vs todos |
| `coef_var_std_precos_ocupados` | FLOAT | Coeficiente de variação (std/média) — ocupados |
| `coef_var_std_precos_mix` | FLOAT | Coeficiente de variação (std/média) — mix |
| `updated_at` | TIMESTAMP | Timestamp da última atualização |

> **Interpretação:** Um percentil alto (ex: 80) significa que o preço Seazone está acima de 80% dos concorrentes. Features próximas a 50 indicam posicionamento neutro no mercado.


---

## Deploy

### Cloud Functions / Cloud Run

Todos os serviços novos seguem o mesmo padrão de deploy manual via `gcloud`.

**Cloud Functions** (`compute-cluster-features`):

```bash
gcloud functions deploy compute-cluster-features \
  --runtime python311 \
  --trigger-http \
  --region us-central1 \
  --project data-resources-448418 \
  --entry-point main \
  --source cloud-functions/system-price/compute-cluster-features/ \
  --set-env-vars PROJECT_ID=data-resources-448418,DB_PRICING=pricingdata-XXXXX,...
```

**Cloud Run** (`suggest-cluster`, `list-clusters`, `list-valid-categories`, `list-cluster-history`):

```bash
# Build e push
docker build -t us-central1-docker.pkg.dev/data-resources-448418/<repo>/<service>:latest \
  cloud-functions/system-price/<service>/

docker push us-central1-docker.pkg.dev/data-resources-448418/<repo>/<service>:latest

# Deploy
gcloud run deploy <service> \
  --image us-central1-docker.pkg.dev/data-resources-448418/<repo>/<service>:latest \
  --region us-central1 \
  --project data-resources-448418
```

**cluster-manager-ui:**

```bash
docker build -t us-central1-docker.pkg.dev/data-resources-448418/<repo>/cluster-manager-ui:latest \
  cluster-manager-ui/

docker push us-central1-docker.pkg.dev/data-resources-448418/<repo>/cluster-manager-ui:latest

gcloud run deploy cluster-manager-ui \
  --image us-central1-docker.pkg.dev/data-resources-448418/<repo>/cluster-manager-ui:latest \
  --region us-central1 \
  --project data-resources-448418 \
  --set-env-vars API_BASE_URL=...,NEXTAUTH_URL=...
```

### API Gateway

Os novos endpoints de leitura (`list-clusters`, `list-valid-categories`, `list-cluster-history`, `suggest-cluster`) precisam ser adicionados ao `api-gateway/system-price/config-data-resources.yaml` e o gateway republicado:

```bash
gcloud api-gateway api-configs create <nova-config> \
  --api=system-price-gateway \
  --openapi-spec=api-gateway/system-price/config-data-resources.yaml \
  --project=data-resources-448418

gcloud api-gateway gateways update system-price-gateway \
  --api-config=<nova-config> \
  --location=us-central1 \
  --project=data-resources-448418
```