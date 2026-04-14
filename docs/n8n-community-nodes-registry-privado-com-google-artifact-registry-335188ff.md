<!-- title: n8n Community Nodes — Registry Privado com Google Artifact Registry | url: https://outline.seazone.com.br/doc/n8n-community-nodes-registry-privado-com-google-artifact-registry-hoLMody94J | area: Tecnologia -->

# n8n Community Nodes — Registry Privado com Google Artifact Registry

Guia de uso, publicação e operação da solução de registry privado para community nodes do n8n no cluster GKE da Seazone.

GAR com os community nodes: <https://console.cloud.google.com/artifacts/npm/tools-440117/us-central1/n8n-npm?project=tools-440117>


---

## Por que isso existe

O n8n roda com `N8N_REINSTALL_MISSING_PACKAGES=true` para sobreviver a restarts com PVC vazia. O efeito colateral: **toda versão instalada é a** `**latest**` **do npm público**. Quando o `@cardtunic/n8n-nodes-pipefy` recebeu uma atualização quebrada, o próximo restart do pod derrubou 30+ workflows.

A solução é um registry npm privado no **Google Artifact Registry** com versões pinadas, interceptando as chamadas do n8n antes de chegar ao npm público.


---

## Arquitetura

```mermaidjs
%%{init: {"theme": "dark", "themeVariables": {"primaryColor": "#1e293b", "primaryTextColor": "#e2e8f0", "primaryBorderColor": "#334155", "lineColor": "#64748b", "secondaryColor": "#0f172a", "tertiaryColor": "#1e293b", "clusterBkg": "#0f172a", "clusterBorder": "#334155", "edgeLabelBackground": "#1e293b", "fontFamily": "JetBrains Mono, monospace"}}}%%
graph TB
    subgraph GKE["☁️  GKE · us-central1-a"]
        direction TB

        subgraph dev["namespace: dev-n8n"]
            direction LR
            IC1["🔧 initContainer\nbusybox:1.36"] -->|"busca token WI\nescreve .npmrc\nescreve wrapper"| ED1["📁 emptyDir\n/custom-bin/"]
            ED1 -->|PATH prefixado| N1["⚡ n8n\nPATH=/custom-bin:…"]
        end

        subgraph prd["namespace: prd-n8n"]
            direction LR
            IC2["🔧 initContainer\nbusybox:1.36"] -->|"busca token WI\nescreve .npmrc\nescreve wrapper"| ED2["📁 emptyDir\n/custom-bin/"]
            ED2 -->|PATH prefixado| N2["⚡ n8n\nPATH=/custom-bin:…"]
        end

        N1 -->|interceptado| GAR
        N2 -->|interceptado| GAR
    end

    subgraph GAR["☁️  Google Artifact Registry · tools-440117"]
        direction LR
        VIRT["🔀 n8n-npm\nvirtual"] --> PIN["📦 n8n-npm-pinned\nstandard\nversões pinadas"]
        VIRT --> UP["🌐 n8n-npm-upstream\nremote\nproxy npmjs"]
    end

    UP -->|proxy deps transitivas| NPM["🌐 registry.npmjs.org"]

    style GKE fill:#0f172a,stroke:#334155,color:#94a3b8
    style GAR fill:#0f172a,stroke:#334155,color:#94a3b8
    style dev fill:#0c2a1a,stroke:#16a34a,color:#86efac
    style prd fill:#1c1917,stroke:#78716c,color:#d4d4d4
    style VIRT fill:#312e81,stroke:#4338ca,color:#c7d2fe
    style PIN fill:#1e3a5f,stroke:#2563eb,color:#bfdbfe
    style UP fill:#1e293b,stroke:#475569,color:#94a3b8
    style NPM fill:#1e293b,stroke:#475569,color:#94a3b8
```

### Fluxo completo no startup do pod

```mermaidjs
%%{init: {"theme": "dark", "themeVariables": {"primaryColor": "#1e293b", "primaryTextColor": "#e2e8f0", "primaryBorderColor": "#334155", "lineColor": "#64748b", "fontFamily": "JetBrains Mono, monospace", "actorBkg": "#1e293b", "actorBorder": "#475569", "actorTextColor": "#e2e8f0", "actorLineColor": "#64748b", "signalColor": "#94a3b8", "signalTextColor": "#e2e8f0", "labelBoxBkgColor": "#0f172a", "labelBoxBorderColor": "#334155", "labelTextColor": "#94a3b8", "noteBkgColor": "#1e293b", "noteTextColor": "#94a3b8", "noteBorderColor": "#334155", "loopTextColor": "#94a3b8", "activationBorderColor": "#64748b", "activationBkgColor": "#1e293b"}}}%%
sequenceDiagram
    participant IC as 🔧 initContainer
    participant Meta as 🔑 Metadata Server
    participant Vol as 📁 emptyDir
    participant N8N as ⚡ n8n
    participant Wrap as 🔀 wrapper /custom-bin/npm
    participant Real as 📦 npm real
    participant GAR as ☁️ GAR n8n-npm
    participant Pub as 🌐 npm público

    Note over IC,Vol: Phase 1 — bootstrap
    IC->>Meta: GET /instance/service-accounts/default/token
    Meta-->>IC: access_token (Workload Identity)
    IC->>Vol: escreve /custom-bin/.npmrc (token)
    IC->>Vol: escreve /custom-bin/npm (wrapper script)
    IC->>Vol: chmod +x

    Note over N8N,Wrap: Phase 2 — reinstall automático
    N8N->>Wrap: npm install @cardtunic/... --registry=https://registry.npmjs.org
    Wrap->>Wrap: 🔄 substitui --registry= + injeta --userconfig
    Wrap->>Real: npm install @cardtunic/... --registry=https://us-central1-npm.pkg.dev/tools-440117/n8n-npm/

    Note over Real,GAR: Phase 3 — resolução de pacotes
    Real->>GAR: GET /@cardtunic/n8n-nodes-pipefy
    GAR-->>Real: ✅ v0.1.5 (pinada — servida pelo n8n-npm-pinned)

    Real->>GAR: GET /dependência-transitiva
    GAR->>Pub: proxy → fetch (via n8n-npm-upstream)
    Pub-->>GAR: 200 OK
    GAR-->>Real: 200 (cached)

    Real-->>N8N: ✅ instalado v0.1.5

    Note over N8N: Packages reinstalled successfully 🎉
```


---

## Packages pinados

| Package | Versão pinada | Namespaces |
|----|----|----|
| `@cardtunic/n8n-nodes-pipefy` | `0.1.5` | dev-n8n, prd-n8n |
| `@mbakgun/n8n-nodes-slack-socket-mode` | `1.6.2` | dev-n8n, prd-n8n |
| `@splainez/n8n-nodes-phonenumber-parser` | `1.2.0` | dev-n8n, prd-n8n |


---

## Como publicar um novo package ou nova versão

### Pré-requisitos

Membro do grupo `cloud@seazone.com.br` (tem `artifactregistry.writer` no repo `n8n-npm-pinned`). Ferramentas necessárias: `gcloud`, `npm`.

### Passo a passo

```bash
# 1. Autenticar o npm no GAR
TOKEN=$(gcloud auth print-access-token)
npm config set "//us-central1-npm.pkg.dev/tools-440117/n8n-npm-pinned/:_authToken" "$TOKEN"

# 2. Baixar a versão específica do npm público
npm pack @cardtunic/n8n-nodes-pipefy@0.1.5

# 3. Publicar no GAR
npm publish cardtunic-n8n-nodes-pipefy-0.1.5.tgz \
  --registry https://us-central1-npm.pkg.dev/tools-440117/n8n-npm-pinned/ \
  --ignore-scripts

# 4. Validar
npm info @cardtunic/n8n-nodes-pipefy \
  --registry https://us-central1-npm.pkg.dev/tools-440117/n8n-npm/
```

> O token do `gcloud auth print-access-token` expira em \~1h. Se der `ENEEDAUTH`, refaça o step 1.


---

## Como adicionar um novo community node

```mermaidjs
%%{init: {"theme": "dark", "themeVariables": {"primaryColor": "#1e293b", "primaryTextColor": "#e2e8f0", "primaryBorderColor": "#334155", "lineColor": "#64748b", "fontFamily": "JetBrains Mono, monospace"}}}%%
flowchart TD
    A(["📦 novo node\nsolicitado"]) --> B["testar no dev-n8n\nvia UI do n8n"]
    B --> C{"funciona\ncorretamente?"}
    C -- não --> X(["❌ não adicionar\naté fix upstream"])
    C -- sim --> D["identificar versão\nexata que funciona"]
    D --> E["publicar no GAR\nveja seção anterior"]
    E --> F["adicionar package em\nN8N_COMMUNITY_PACKAGES_ALLOW_TOOL_USAGE\nno values.yaml dev-n8n"]
    F --> G["sincronizar ArgoCD\ndev-n8n"]
    G --> H{"validar no dev\nem produção simulada"}
    H -- ok --> I["replicar no\nvalues.yaml prd-n8n"]
    I --> J["sincronizar ArgoCD\nprd-n8n"]
    J --> K(["✅ node disponível\nno prod"])
    H -- falha --> L["investigar logs\ndo pod"]
    L --> E

    style A fill:#1e293b,stroke:#334155,color:#e2e8f0
    style X fill:#3b1212,stroke:#dc2626,color:#f87171
    style K fill:#14532d,stroke:#16a34a,color:#86efac
    style C fill:#1c1917,stroke:#78716c,color:#d4d4d4
    style H fill:#1c1917,stroke:#78716c,color:#d4d4d4
```


---

## Como atualizar a versão de um package existente

> **Regra de ouro:** nunca atualize diretamente em `prd-n8n`. Sempre valide em `dev-n8n` primeiro.

```mermaidjs
%%{init: {"theme": "dark", "themeVariables": {"primaryColor": "#1e293b", "primaryTextColor": "#e2e8f0", "primaryBorderColor": "#334155", "lineColor": "#64748b", "fontFamily": "JetBrains Mono, monospace"}}}%%
flowchart LR
    A(["nova versão\ndisponível upstream"]) --> B["ler changelog\ndo maintainer"]
    B --> C{"breaking\nchanges?"}
    C -- sim --> D["avaliar impacto\nnos workflows"]
    C -- não --> E["publicar nova versão\nno GAR"]
    D --> E
    E --> F["atualizar versão\nno values.yaml dev-n8n"]
    F --> G["sync ArgoCD + reiniciar pod\ndev-n8n"]
    G --> H{"workflows\nfuncionando?"}
    H -- não --> I["rollback:\nversão anterior já está no GAR"]
    H -- sim --> J["atualizar values.yaml\nprd-n8n"]
    I --> K(["🔄 rollback feito"])
    J --> L(["✅ atualizado em prod"])

    style A fill:#1e293b,stroke:#334155,color:#e2e8f0
    style K fill:#2d2208,stroke:#ca8a04,color:#fbbf24
    style L fill:#14532d,stroke:#16a34a,color:#86efac
    style C fill:#1c1917,stroke:#78716c,color:#d4d4d4
    style H fill:#1c1917,stroke:#78716c,color:#d4d4d4
```

### Rollback instantâneo

O GAR guarda todas as versões já publicadas. Rollback é só mudar a versão no `values.yaml` e sincronizar o ArgoCD  sem republicar.

```bash
# ver versões disponíveis no GAR
npm info @cardtunic/n8n-nodes-pipefy versions \
  --registry https://us-central1-npm.pkg.dev/tools-440117/n8n-npm/
```


---

## Operação e troubleshooting

### Verificar se o wrapper está ativo no pod

```bash
kubectl exec -n dev-n8n deploy/n8n-editor -- which npm
# esperado: /custom-bin/npm

kubectl exec -n dev-n8n deploy/n8n-editor -- cat /custom-bin/npm
```

### Verificar logs do initContainer

```bash
kubectl logs -n dev-n8n \
  $(kubectl get pod -n dev-n8n -l app.kubernetes.io/component=editor -o name | head -1) \
  -c npm-wrapper
# esperado: [npm-wrapper] token obtido via Workload Identity
```

### Verificar que o GAR está acessível e o package está lá

```bash
npm info @cardtunic/n8n-nodes-pipefy \
  --registry https://us-central1-npm.pkg.dev/tools-440117/n8n-npm/
```

### Árvore de diagnóstico  "node não instala"

```mermaidjs
%%{init: {"theme": "dark", "themeVariables": {"primaryColor": "#1e293b", "primaryTextColor": "#e2e8f0", "primaryBorderColor": "#334155", "lineColor": "#64748b", "fontFamily": "JetBrains Mono, monospace"}}}%%
flowchart TD
    E(["❌ erro ao instalar\ncommunity node"]) --> A{"wrapper\nexiste em\n/custom-bin/npm?"}
    A -- não --> B["initContainer falhou\n→ ver logs do npm-wrapper"]
    A -- sim --> C{"logs mostram\ntoken obtido?"}
    C -- não --> D["Workload Identity falhou\n→ checar SA annotation no pod"]
    C -- sim --> F{"package existe\nno GAR?"}
    F -- não --> G["publicar package\nveja seção anterior"]
    F -- sim --> H{"versão correta\nestá pinada?"}
    H -- não --> I["re-publicar com versão certa\n→ npm pack + npm publish"]
    H -- sim --> J["checar logs n8n\npor erros de dependência transitiva"]
    J --> K{"dep transitiva\nfaltando?"}
    K -- sim --> L["GAR faz proxy via n8n-npm-upstream\nchecar se upstream está ativo"]
    K -- não --> M["abrir issue com\nstack trace completo"]

    style E fill:#3b1212,stroke:#dc2626,color:#f87171
    style B fill:#2d2208,stroke:#ca8a04,color:#fbbf24
    style D fill:#2d2208,stroke:#ca8a04,color:#fbbf24
    style G fill:#1e293b,stroke:#334155,color:#e2e8f0
    style I fill:#1e293b,stroke:#334155,color:#e2e8f0
    style M fill:#3b1212,stroke:#dc2626,color:#f87171
```


---

## Boas práticas

### ✅ Faça sempre

* **Pin explícito de versão**,  nunca publique `latest` no GAR. Sempre `npm pack pkg@x.y.z` antes de publicar.
* **Teste em dev antes de prd**, o ciclo é: GAR → dev-n8n → validação → prd-n8n.
* **Atualize esta documentação** ao adicionar ou versionar qualquer package.
* **Valide com** `**npm info**` após cada publicação para confirmar que chegou corretamente.

### ❌ Nunca faça

* Não remova versões antigas do GAR, elas são o seu plano de rollback.
* Não atualize a versão no `values.yaml` de `prd-n8n` sem validar em `dev-n8n` antes.
* Não confie no changelog do maintainer sem testar — o incidente com o pipefy aconteceu justamente por atualização silenciosa.

### Sobre o wrapper

O wrapper intercepta o argumento `--registry=` e injeta o `.npmrc` com o token de autenticação. O token é gerado fresh a cada restart do pod via Workload Identity  sem segredos estáticos.

```sh
#!/bin/sh
# /custom-bin/npm — wrapper injetado pelo initContainer
REAL_NPM=$(ls /opt/nodejs/*/bin/npm 2>/dev/null | head -1)
GAR_URL="https://us-central1-npm.pkg.dev/tools-440117/n8n-npm/"

NEW_ARGS="--userconfig /custom-bin/.npmrc"
for arg in "$@"; do
  case "$arg" in
    --registry=*) NEW_ARGS="$NEW_ARGS --registry=$GAR_URL" ;;
    *)            NEW_ARGS="$NEW_ARGS $arg" ;;
  esac
done

exec $REAL_NPM $NEW_ARGS
```


---

## IAM

| Principal | Role | Repo |
|----|----|----|
| `n8n-dev-sa@tools-440117.iam.gserviceaccount.com` | `artifactregistry.reader` | `n8n-npm` |
| `n8n-prd-sa@tools-440117.iam.gserviceaccount.com` | `artifactregistry.reader` | `n8n-npm` |
| `cloud@seazone.com.br` | `artifactregistry.writer` | `n8n-npm-pinned` |
| `cloud@seazone.com.br` | `artifactregistry.reader` | `n8n-npm` |


---

## Referências

* [Google Artifact Registry — npm docs](https://cloud.google.com/artifact-registry/docs/nodejs)
* [n8n Community Nodes docs](https://docs.n8n.io/integrations/community-nodes/)
* [PR #127 — feat: add private npm registry](https://github.com/seazone-tech/gitops-governanca/pull/127)