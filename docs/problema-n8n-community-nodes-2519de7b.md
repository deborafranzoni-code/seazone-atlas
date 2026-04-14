<!-- title: Problema: n8n Community Nodes | url: https://outline.seazone.com.br/doc/problema-n8n-community-nodes-CAK5ODHsBA | area: Tecnologia -->

# Problema: n8n Community Nodes

---

## O problema

O n8n roda com `N8N_REINSTALL_MISSING_PACKAGES=true`, necessário porque a PVC pode estar vazia em deploys novos. O lado ruim: toda vez que o pod sobe, ele instala a versão **latest** de cada community node direto do npm público, sem fixar versão.

O `@cardtunic/n8n-nodes-pipefy` recebeu uma atualização quebrada. No próximo restart, o n8n puxou o latest automaticamente e **30+ workflows foram a baixo**.

A solução óbvia: um registry privado com versões pinadas. Assim o reinstall automático passa a buscar de lá, e só atualizo quando eu decidir não quando o maintainer empurrar algo quebrado.

```mermaidjs
sequenceDiagram
    participant Pod as n8n Pod
    participant NPM as npm público

    Note over Pod: N8N_REINSTALL_MISSING_PACKAGES=true
    Pod->>NPM: npm install @cardtunic/n8n-nodes-pipefy@latest
    NPM-->>Pod: v0.2.x 💥 (quebrada)
    Pod->>Pod: workflows quebrados
```


---

## Opções investigadas

```mermaidjs
flowchart TD
    P([n8n sempre busca latest do npm público]) --> O1 & O2 & O3 & O4 & O5

    O1["① N8N_COMMUNITY_PACKAGES_REGISTRY"]
    O1 -- "requer licença paga\nfeat:communityNodes:customRegistry" --> F1([❌ descartado])

    O2["② NPM_CONFIG_REGISTRY env var"]
    O2 -- "n8n passa --registry= via CLI\nsobrescreve qualquer env var" --> F2([❌ descartado])

    O3["③ Rewrite DNS via CoreDNS"]
    O3 -- "GKE usa kube-dns + dnsmasq\nsem suporte a rewrite rules" --> F3([❌ descartado])

    O4["④ Custom Docker Image"]
    O4 -- "pipeline CI/CD + nova imagem\ncomplexidade alta demais" --> F4([⚠️ reserva])

    O5["⑤ npm wrapper via initContainer"]
    O5 -- "sem licença · sem imagem · sem permissões extras" --> OK([✅ escolhida])

    style OK fill:#14532d,color:#fff
    style F1 fill:#3b1212,color:#f87171
    style F2 fill:#3b1212,color:#f87171
    style F3 fill:#3b1212,color:#f87171
    style F4 fill:#2d2208,color:#fbbf24
```

### ① `N8N_COMMUNITY_PACKAGES_REGISTRY`

Variável oficial do n8n para apontar um registry customizado, parecia perfeita. Mas está travada atrás de `feat:communityNodes:customRegistry`, feature exclusiva de licença paga. Confirmei no source code, descartei.

### ② `NPM_CONFIG_REGISTRY` (env var)

Todo cliente npm lê essa variável para saber qual registry usar. Exceto que o n8n passa `--registry=https://registry.npmjs.org` explicitamente como argumento de CLI, o que sobrescreve qualquer env var. Confirmado em `npm-utils.js`:

```js
return [...NPM_COMMON_ARGS, ...NPM_INSTALL_ARGS, `--registry=${this.getNpmRegistry()}`]
```

Ineficaz.

### ③ Rewrite DNS via CoreDNS

A ideia era redirecionar `registry.npmjs.org` para o Verdaccio no DNS do cluster. O GKE usa `kube-dns` com `dnsmasq`,  sem suporte a rewrite rules sem customizações pesadas.

### ④ Custom Docker Image

Substituir o binário npm na imagem. Funcionaria, mas exigiria pipeline de build, repositório no Artifact Registry e atualização do `values.yaml` no ArgoCD a cada nova versão do n8n. Complexidade desproporcional ao problema.


---

## Solução escolhida → npm wrapper via initContainer

A ideia: injetar um script wrapper no `PATH` do container **em runtime**, sem tocar na imagem. O wrapper intercepta qualquer chamada `npm install` e substitui o argumento `--registry=` antes de repassar para o npm real.

Junto com isso, subi um **Verdaccio** no namespace verdaccio com as versões pinadas dos três community nodes publicadas manualmente.

### Como funciona no startup do pod

```mermaidjs
sequenceDiagram
    participant IC as initContainer (busybox)
    participant Vol as emptyDir /custom-bin
    participant N8N as n8n container
    participant Wrap as /custom-bin/npm
    participant Real as npm real (/opt/nodejs/...)
    participant V as Verdaccio (namespace verdaccio)
    participant NPM as npm público

    IC->>Vol: escreve wrapper script + chmod +x
    IC-->>N8N: volume montado

    Note over N8N: PATH=/custom-bin:...
    N8N->>Wrap: npm install @cardtunic/... --registry=https://registry.npmjs.org
    Wrap->>Wrap: substitui --registry=
    Wrap->>Real: npm install @cardtunic/... --registry=http://verdaccio.tools.svc.cluster.local:4873

    Real->>V: GET /@cardtunic/n8n-nodes-pipefy
    V-->>Real: v0.1.5 ✅ (pinada)

    Real->>V: GET /dependência-transitiva
    V->>NPM: proxy → fetch
    NPM-->>V: 200
    V-->>Real: 200 (cached)

    Real-->>N8N: instalado v0.1.5 ✅
```

### Arquitetura no cluster

```mermaidjs
graph LR
    subgraph GKE["GKE · us-central1-a"]
        subgraph tools["namespace: verdaccio"]
            V["Verdaccio\n:4873\nversões pinadas"]
        end

        subgraph devn8n["namespace: dev-n8n ✅"]
            subgraph pod1["Pod"]
                IC1["initContainer\nbusybox:1.36"] --> EB1["emptyDir\n/custom-bin/npm"] --> N1["n8n\nPATH=/custom-bin:..."]
            end
        end

        subgraph prdn8n["namespace: prd-n8n ⏳"]
            subgraph pod2["Pod"]
                IC2["initContainer\nbusybox:1.36"] --> EB2["emptyDir\n/custom-bin/npm"] --> N2["n8n\nPATH=/custom-bin:..."]
            end
        end

        N1 -- "interceptado → Verdaccio" --> V
        N2 -- "interceptado → Verdaccio" --> V
        V -- "proxy para deps transitivas" --> PUB["registry.npmjs.org"]
    end
```

### O wrapper

```sh
#!/bin/sh
REAL_NPM=$(ls /opt/nodejs/*/bin/npm 2>/dev/null | head -1)
VERDACCIO_URL="http://verdaccio.verdaccio.svc.cluster.local:4873"

for arg in "$@"; do
  case "$arg" in
    --registry=*) NEW_ARGS="$NEW_ARGS --registry=$VERDACCIO_URL" ;;
    *)            NEW_ARGS="$NEW_ARGS $arg" ;;
  esac
done

exec $REAL_NPM $NEW_ARGS
```

### Packages publicados no Verdaccio com versão pinada

| Package | Versão pinada |
|----|----|
| `@cardtunic/n8n-nodes-pipefy` | `0.1.5` |
| `@mbakgun/n8n-nodes-slack-socket-mode` | `1.6.2` |
| `@splainez/n8n-nodes-phonenumber-parser` | `1.2.0` |


---

## Resultado dos testes (dev-n8n)

Testei com PVC zerada, simula deploy fresh / disaster recovery.

* initContainer escreve o wrapper corretamente
* `execFile('npm')` do Node.js resolve para `/custom-bin/npm` via PATH
* Wrapper intercepta `--registry=https://registry.npmjs.org` e substitui por Verdaccio
* Verdaccio serve as versões pinadas; deps transitivas proxiadas do npm público
* n8n loga `Packages reinstalled successfully` e sobe normalmente
* Versões instaladas confirmadas: `0.1.5` / `1.6.2` / `1.2.0` — não latest


---

##