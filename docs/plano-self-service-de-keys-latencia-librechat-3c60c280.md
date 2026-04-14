<!-- title: Plano: Self-Service de Keys + Latencia LibreChat | url: https://outline.seazone.com.br/doc/plano-self-service-de-keys-latencia-librechat-pmLZbjNg6W | area: Tecnologia -->

# Plano: Self-Service de Keys + Latencia LibreChat

---

## Problema 1: Usuarios nao conseguem criar suas proprias keys

O LiteLLM OSS nao tem SSO. Quem tem SSO e o Enterprise (preco sob consulta, licenca por instalacao). Hoje so admin cria keys via master key.

### Opcoes

**A. Mini-app de self-service (recomendado)**

FastAPI/Express de \~150 linhas que:

* Autentica via Google OAuth (`@seazone.com.br`)
* Chama `POST /key/generate` do LiteLLM com a master key
* Retorna a key pro usuario
* Tela unica: login → gera key → copia

Pode rodar no mesmo Railway. Budget e team ja vem pre-configurados baseado no email/grupo.

**B.** `**UI_ACCESS_MODE=all**`

Env var do LiteLLM que abre a UI pra qualquer um criar key. Zero autenticacao — qualquer pessoa com a URL gera key. So funciona se o hub nao for publico.

Risco: se alguem descobre a URL, cria key sem controle.

**E. LiteLLM Enterprise**

SSO nativo (Google/Okta/Azure AD), self-serve keys, RBAC avancado, audit logs. Preco: sob consulta (nao publica, estimativa de mercado \~$300-500/mes). Nao recomendo no dia 1 — OSS + opcao A resolve.

D - Conta compartilhada sem ser ADM

### Recomendacao

Ir com **A** : mini-app de self-service pra devs que precisam de key.


---

## Problema 2: Latencia no LibreChat

### Onde esta a latencia

```
Browser → LibreChat (EC2) → LiteLLM (Railway, US) → Provider API → resposta
```

Dois gargalos provaveis:


1. **LibreChat → LiteLLM**: EC2 no Brasil, Railway nos EUA = \~150-200ms por hop
2. **LiteLLM → Provider**: depende do provider (MiniMax \~1-2s, Zhipu \~1-2s)

### Opcoes

**A. Colocar LibreChat na mesma rede do LiteLLM (maior impacto)**

Mover o LibreChat pro Railway (mesmo projeto do LiteLLM). Comunicacao interna via `litellm.railway.internal:4000` — elimina o hop internacional.

Impacto: -150-200ms por request. Streaming comeca a aparecer mais rapido.

**B. Garantir que streaming esta ativo**

No `librechat.yaml`, confirmar:

```yaml
endpoints:
  custom:
    - name: "Seazone Hub"
      apiURL: "http://litellm.railway.internal:4000/v1"  # interno se colocalizado
      apiKey: "${LITELLM_API_KEY}"
      stream: true
```

Se streaming estiver off, o usuario espera a resposta inteira antes de ver algo.

**C. Desativar features que adicionam overhead no LibreChat**

```env
SEARCH_ENABLED=false      # MeiliSearch desligado se nao usa
CHECK_BALANCE=false        # nao checar saldo a cada request
RAG_API_URL=               # desativar RAG se nao usa
```

**D. Ajustar LiteLLM**

```env
NUM_WORKERS=4                         # ja esta assim
LITELLM_TURN_OFF_TOKEN_COUNTING=True  # economia de CPU
```

O `proxy_batch_write_at: 60` no config ja agrupa writes no Postgres — bom.

**E. Trocar modelo default do LibreChat**

Se o modelo padrao no LibreChat e M2.7, a primeira resposta sempre leva \~2-5s (MiniMax e mais lento). Trocar pra `gemini-2.5-flash` ou `zhipu-glm4.5-flash` como default do chat pode dar sensacao de mais velocidade.

### Recomendacao

**A + B + E** dao o maior impacto com menor esforco:


1. Mover LibreChat pro Railway (ou pelo menos usar endpoint interno)
2. Confirmar streaming ativo
3. Default do chat = modelo mais rapido (Gemini Flash ou GLM-4.5 Flash)