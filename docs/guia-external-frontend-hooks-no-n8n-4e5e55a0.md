<!-- title: Guia: External Frontend Hooks no n8n | url: https://outline.seazone.com.br/doc/guia-external-frontend-hooks-no-n8n-Naz3KFIScr | area: Tecnologia -->

# Guia: External Frontend Hooks no n8n

## O que são

O n8n suporta dois tipos de hooks externos:

| Tipo | Var de ambiente | Onde roda | Pode bloquear ação? |
|----|----|----|----|
| **Backend** | `EXTERNAL_HOOK_FILES` | Node.js dentro do pod | Sim (throw) |
| **Frontend** | `EXTERNAL_FRONTEND_HOOKS_URLS` | Browser do usuário | Não (só UI) |

O **frontend hook** é uma URL pública de arquivo `.js` que o n8n injeta como `<script src="...">` no HTML do editor. O browser baixa e executa esse script antes de renderizar a interface. Você usa isso para adicionar avisos visuais, interceptar ações de UI, ou qualquer coisa que caiba num script de browser.


---

## Arquitetura

```
Browser
  └── carrega editor do n8n
        └── n8n injeta <script src="https://seu-dominio/hooks/banner.js?v=N">
              └── seu script roda no contexto da página
                    ├── DOM manipulation (avisos, modais, barras)
                    └── MutationObserver (detecta mudanças de rota/modal)

Cluster Kubernetes
  ├── ConfigMap (banner.js)          ← conteúdo do script
  ├── Deployment nginx:alpine        ← serve o arquivo via HTTP
  ├── Service ClusterIP :80          ← expõe o nginx internamente
  └── IngressRoute (priority:200)   ← /hooks/ roteia para esse nginx
                                       (priority alta para não conflitar
                                        com rota catch-all do editor)
```


---

## Passo a passo: criar do zero

### 1. Escrever o script

O script é um IIFE (Immediately Invoked Function Expression) para não poluir o escopo global:

```javascript
(function () {
  // seu código aqui

  function init() {
    // chamado após DOMContentLoaded
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
```

Valide sintaxe antes de aplicar:

```bash
node /tmp/banner.js && echo "OK"
```

### 2. Criar os recursos Kubernetes (Se ainda não existirem)

Salve um `hooks.yaml` com:

```yaml
# ConfigMap com o conteúdo do script
apiVersion: v1
kind: ConfigMap
metadata:
  name: MEU-NAMESPACE-hooks-js
  namespace: MEU-NAMESPACE
data:
  banner.js: |
    (function () {
      /* conteúdo do script */
    })();

---
# ConfigMap com configuração do nginx
apiVersion: v1
kind: ConfigMap
metadata:
  name: MEU-NAMESPACE-hooks-nginx-conf
  namespace: MEU-NAMESPACE
data:
  default.conf: |
    server {
      listen 80;
      root /usr/share/nginx/html;
      location / {
        add_header Content-Type application/javascript;
        add_header Cache-Control "no-store";
      }
    }

---
# Deployment nginx para servir o script
apiVersion: apps/v1
kind: Deployment
metadata:
  name: MEU-NAMESPACE-hooks-server
  namespace: MEU-NAMESPACE
spec:
  replicas: 1
  selector:
    matchLabels:
      app: MEU-NAMESPACE-hooks-server
  template:
    metadata:
      labels:
        app: MEU-NAMESPACE-hooks-server
    spec:
      containers:
        - name: nginx
          image: nginx:alpine
          ports:
            - containerPort: 80
          volumeMounts:
            - name: js
              mountPath: /usr/share/nginx/html/banner.js
              subPath: banner.js
            - name: nginx-conf
              mountPath: /etc/nginx/conf.d/default.conf
              subPath: default.conf
      volumes:
        - name: js
          configMap:
            name: MEU-NAMESPACE-hooks-js
        - name: nginx-conf
          configMap:
            name: MEU-NAMESPACE-hooks-nginx-conf

---
# Service interno
apiVersion: v1
kind: Service
metadata:
  name: MEU-NAMESPACE-hooks-server
  namespace: MEU-NAMESPACE
spec:
  selector:
    app: MEU-NAMESPACE-hooks-server
  ports:
    - port: 80
      targetPort: 80

---
# IngressRoute Traefik — prioridade alta para /hooks/ não ir parar no editor
apiVersion: traefik.io/v1alpha1
kind: IngressRoute
metadata:
  name: MEU-NAMESPACE-hooks-server
  namespace: MEU-NAMESPACE
spec:
  entryPoints:
    - websecure
  routes:
    - match: Host(`seu-dominio.com.br`) && PathPrefix(`/hooks/`)
      kind: Rule
      priority: 200
      services:
        - name: MEU-NAMESPACE-hooks-server
          port: 80
  tls:
    certResolver: le
```

Aplique:

```bash
kubectl apply -f hooks.yaml
```

### 3. Apontar o n8n para o script

No ConfigMap de configuração do n8n (`n8n-config` ou equivalente):

```bash
kubectl patch configmap n8n-config -n MEU-NAMESPACE --type=merge \
  -p='{"data":{"EXTERNAL_FRONTEND_HOOKS_URLS":"https://seu-dominio.com.br/hooks/banner.js?v=1"}}'
```

O separador é `;` para múltiplas URLs (diferente do backend que usa `:`).

Reiniciar o editor para carregar a nova var:

```bash
kubectl rollout restart deployment/n8n-editor -n MEU-NAMESPACE
```

### 4. Verificar se está funcionando

```bash
# O arquivo está sendo servido como JS?
curl -si "https://seu-dominio.com.br/hooks/banner.js?v=1" | head -5
# Deve ter: content-type: application/javascript
# Se vier text/html: IngressRoute com prioridade insuficiente (ver troubleshooting)

# O <script> está no HTML do n8n?
kubectl port-forward svc/n8n-editor 18080:5678 -n MEU-NAMESPACE &
curl -s http://localhost:18080/ | grep "banner.js"
```


---

## Padrões para detecção de eventos no SPA

O n8n é uma SPA Vue.js. Não há recarregamento de página ao navegar ou abrir modais — o DOM é modificado dinamicamente.

### Detectar abertura de modal

Use `MutationObserver` com `subtree: true` e o padrão `wasVisible`:

```javascript
function setupModalHook() {
  var wasVisible = false;
  new MutationObserver(function () {
    var isVisible = !!document.querySelector('[data-test-id="NOME-DO-MODAL-modal"]');
    if (isVisible && !wasVisible) {
      wasVisible = true;
      // modal abriu
      showMeuAviso();
    } else if (!isVisible && wasVisible) {
      wasVisible = false;
      // modal fechou
      var el = document.getElementById('meu-aviso');
      if (el) el.parentElement.removeChild(el);
    }
  }).observe(document.body, { childList: true, subtree: true });
}
```

**Por que** `**subtree: true**`**?** Os modais do n8n usam Vue Teleport — são renderizados dentro de `.el-overlay` que é appended ao `<body>`, mas o conteúdo é nested. Sem `subtree`, o observer não detecta essas mudanças internas.

**Por que** `**wasVisible**` **e não debounce?** Vue faz mutações contínuas no DOM enquanto o modal está aberto. Um debounce seria resetado constantemente e nunca dispararia. O flag `wasVisible` garante que o hook só roda na transição `false → true`.

### Selectors confirmados (n8n 2.6.3 e 2.8.3)

| Modal/Elemento | `data-test-id` |
|----|----|
| Modal de publicar workflow | `workflowPublish-modal` |
| Modal de editar credencial | `editCredential-modal` |
| Menu de ações de card de workflow | `workflow-card-actions` |
| Menu de ações de card de credencial | `credential-card-actions` |

### Como descobrir um novo selector

O n8n não entrega data-test-ids no HTML inicial (é SPA). Para encontrá-los:

```bash
# 1. Entrar no pod
kubectl exec -it deployment/n8n-editor -n MEU-NAMESPACE -- sh

# 2. Buscar nos bundles compilados
grep -r 'data-test-id' /usr/local/lib/node_modules/n8n/node_modules/n8n-editor-ui/dist/assets/ \
  --include="*.js" -l

# 3. Grep para um elemento específico
grep -o '"[a-z-]*modal[a-z-]*"' /caminho/do/bundle.js | sort -u

# 4. Buscar constantes de modal key
grep 'MODAL_KEY\|_modal\b' /caminho/do/bundle.js | head -30
```

Alternativa: abrir o n8n no browser, inspecionar o elemento desejado via DevTools, e procurar o `data-test-id` no DOM.

### Interceptar clique em botão (capture phase)

Para interceptar ações antes do Vue processá-las, use `capture: true`:

```javascript
document.addEventListener('click', function (e) {
  var el = e.target;
  for (var i = 0; i < 6; i++) {
    if (!el || el === document.body) break;
    var text = (el.textContent || '').trim();
    var role = el.getAttribute('role') || '';
    if (text === 'Delete' && role === 'menuitem') {
      // verificar contexto (está em card de workflow/credencial?)
      var parent = el;
      for (var j = 0; j < 10; j++) {
        if (!parent) break;
        var pid = parent.getAttribute ? (parent.getAttribute('data-test-id') || '') : '';
        if (pid.indexOf('workflow-card') !== -1 || pid.indexOf('credential-card') !== -1) {
          e.stopImmediatePropagation();
          e.preventDefault();
          // mostrar modal de bloqueio
          return;
        }
        parent = parent.parentElement;
      }
    }
    el = el.parentElement;
  }
}, true); // true = capture phase
```


---

## Atualizar o script

### 1. Editar

```bash
# Baixar do cluster
kubectl get configmap MEU-NAMESPACE-hooks-js -n MEU-NAMESPACE \
  -o jsonpath='{.data.banner\.js}' > /tmp/banner.js

# Editar /tmp/banner.js ...

# Validar
node /tmp/banner.js && echo "OK"
```

### 2. Aplicar

**Sempre usar** `**--from-file**`**, nunca** `**--from-literal**` **com JS** (bash escapa `!` e outros chars em literals).

```bash
kubectl create configmap MEU-NAMESPACE-hooks-js \
  --from-file=banner.js=/tmp/banner.js \
  -n MEU-NAMESPACE --dry-run=client -o yaml | kubectl apply -f -

# Reiniciar nginx
kubectl rollout restart deployment/MEU-NAMESPACE-hooks-server -n MEU-NAMESPACE
```

### 3. Contornar cache do Cloudflare

O Cloudflare serve o banner.js com `max-age=31536000`. Incrementar `?v=N` na URL é obrigatório para garantir que os browsers (e o próprio n8n) busquem o arquivo novo:

```bash
# Incrementar versão
kubectl patch configmap n8n-config -n MEU-NAMESPACE --type=merge \
  -p='{"data":{"EXTERNAL_FRONTEND_HOOKS_URLS":"https://seu-dominio.com.br/hooks/banner.js?v=N"}}'

# Reiniciar editor para servir o novo <script src>
kubectl rollout restart deployment/n8n-editor -n MEU-NAMESPACE
```

**Atenção:** reiniciar apenas o nginx não é suficiente. O n8n editor precisa ser reiniciado para que o HTML renderizado inclua a nova URL com `?v=N`.


---

## Troubleshooting

### `content-type: text/html` ao acessar `/hooks/banner.js`

O Traefik está roteando a requisição para o editor do n8n (rota catch-all) em vez do nginx de hooks.

**Fix:** adicionar `priority: 200` no IngressRoute de hooks. A rota Host-only do editor tem prioridade automática \~32.

### Script não aparece no `<script>` do HTML

* Verificar se `EXTERNAL_FRONTEND_HOOKS_URLS` está no ConfigMap do n8n
* Verificar se o editor foi reiniciado após atualizar o ConfigMap (a var só é lida na inicialização do processo)
* Usar `kubectl port-forward` + `curl | grep banner.js` para confirmar

### Script carrega mas hook não roda

* Conferir erros no console do browser (F12)
* Verificar se o `document.body` já existe quando o script é executado (usar o padrão `readyState === 'loading'` → `DOMContentLoaded`)
* Testar com `document.querySelector` no console com a modal aberta para confirmar o selector

### Fetch do script retorna conteúdo antigo

```javascript
// Testar no console do browser com a modal aberta:
fetch('/hooks/banner.js?v=N').then(r => r.text()).then(t => console.log('tamanho:', t.length, t.slice(0,200)));
```

Se retornar tamanho diferente do arquivo atual: cache do Cloudflare. Incrementar `?v=N`.

### Pod em CrashLoopBackOff ao aplicar hook

O hook tem erro de sintaxe JS.

**Fix:** sempre rodar `node /tmp/banner.js && echo "OK"` antes de aplicar ao cluster.

### Rolling update travado em `Pending` (Insufficient cpu)

O nó não tem CPU para rodar dois pods simultaneamente durante o rolling update.

**Fix temporário:** usar estratégia `Recreate` (mata o pod antigo antes de criar o novo):

```bash
kubectl patch deployment n8n-editor -n MEU-NAMESPACE \
  -p='{"spec":{"strategy":{"type":"Recreate"}}}'
kubectl rollout restart deployment/n8n-editor -n MEU-NAMESPACE
# Depois de reiniciado, restaurar:
kubectl patch deployment n8n-editor -n MEU-NAMESPACE \
  -p='{"spec":{"strategy":{"type":"RollingUpdate"}}}'
```

### ConfigMap não atualiza (`unchanged`)

```bash
# Usar server-side apply com force-conflicts:
kubectl create configmap MEU-NAMESPACE-hooks-js \
  --from-file=banner.js=/tmp/banner.js \
  -n MEU-NAMESPACE --dry-run=client -o yaml \
  | kubectl apply --server-side --force-conflicts -f -
```

### MutationObserver dispara mas modal não é detectado

* Confirmar que o selector existe no DOM enquanto o modal está aberto (`document.querySelector('[data-test-id="X"]')` no console)
* Verificar se `subtree: true` está no `observe()` — sem ele, mudanças nested não disparam
* Conferir se o debounce está causando problema (substituir por `wasVisible` flag)


---