<!-- title: Documentação Técnica | url: https://outline.seazone.com.br/doc/documentacao-tecnica-2RpEcsdMcG | area: Tecnologia -->

# Documentação Técnica

## Visão Geral

Aplicação web para gerenciamento de regras de preços especiais de imóveis da Seazone. Permite criar, editar, excluir e simular regras que são sincronizadas com o backend via API AWS Lambda.

**Stack:** React 18 · TypeScript · Vite · Tailwind CSS · shadcn-ui · Supabase (auth)


---

## Arquitetura

```
┌─────────────┐      GET /read-input       ┌──────────────┐
│  React SPA  │  ◄──────────────────────►   │  AWS Lambda  │
│  (Frontend) │      POST /write-input      │  (Backend)   │
└──────┬──────┘                             └──────────────┘
       │
       │  Google OAuth
       ▼
┌─────────────┐
│  Supabase   │
│  (Auth)     │
└─────────────┘
```

A aplicação **não possui banco de dados próprio**. Os dados de regras são lidos e escritos via dois endpoints AWS Lambda:

* `read-input` — leitura
* `write-input` — escrita

A persistência final dos dados é responsabilidade do backend (Lambda). O frontend não conhece a camada de armazenamento.

O Supabase é usado exclusivamente para autenticação (Google OAuth, restrição de domínio `@seazone.com.br`).


---

## Endpoints da API

As URLs dos endpoints estão em variáveis de ambiente (`VITE_API_URL_READ` e `VITE_API_URL_WRITE`).

### `GET /read-input` — Leitura de regras

Retorna todas as regras cadastradas ou filtra por grupo.

**Headers obrigatórios:**

| Header | Valor |
|----|----|
| `Content-Type` | `application/json` |
| `x-api-key` | Valor de `VITE_API_KEY_READ` |

**Query params (opcionais):**

| Param | Descrição |
|----|----|
| `group` | Filtra regras de um grupo/imóvel específico (ex: `?group=CAT-PREMIUM`) |

**Formato da resposta:**

A resposta pode vir em dois formatos — a aplicação trata ambos:

* Array direto: `[ {...}, {...} ]`
* Envelope: `{ "body": "...", "data": [...] }`

Cada objeto no array tem a seguinte estrutura:

| Campo | Tipo | Descrição |
|----|----|----|
| `id_seazone` | `string` | Identificador do imóvel. Pode ser o ID original enviado ou o ID de um membro do grupo (expandido pela Lambda via `setup_groups`) |
| `source_group` | `string` | Valor original que o usuário enviou no campo `Grupo/Imóvel`. Preservado sem alteração pela Lambda |
| `start_date` | `string` | Data de início no formato `YYYY-MM-DD` |
| `end_date` | `string` | Data de fim no formato `YYYY-MM-DD` **(exclusiva — a regra NÃO vale neste dia)** |
| `price` | `number` | Valor do preço em R$ |
| `addition` | `number` | Percentual de acréscimo |
| `type` | `string` | Tipo da regra: `"Fixo"`, `"Mínimo"` ou `"Máximo"` |
| `comment` | `string` | Observação/comentário |
| `ignore_group_level` | `boolean` | Se `true`, a regra ignora a hierarquia de níveis |
| `comment_origin` | `string` | Origem da regra: `"Proprietario"`, `"RM"` ou `"Operacao"` |
| `origin` | `string` | Origem (campo auxiliar) |
| `group_level` | `number` | Nível hierárquico, vindo do bucket S3 `setup_groups` (0 se o imóvel não pertence a nenhum grupo) |
| `state` | `string` | Estado da regra |
| `timestamp` | `string` | Data/hora de criação |
| `event` | `string \| null` | Nome do evento (ex: `"Carnaval"`) ou `null` |
| `big_operations` | `boolean \| null` | Flag de grandes operações (apenas nível imóvel) |
| `region` | `string \| null` | Região: `"Norte"`, `"Sul"`, `"Nordeste"`, `"Sudeste"`, `"Centro-Oeste"` ou `null` |

**Exemplo de resposta:**

```json
[
  {
    "id_seazone": "SZ-12345",
    "source_group": "CAT-PREMIUM",
    "start_date": "2026-03-01",
    "end_date": "2026-03-15",
    "price": 450.00,
    "addition": 0.15,
    "type": "Fixo",
    "comment": "Preço para alta temporada",
    "ignore_group_level": false,
    "comment_origin": "RM",
    "origin": "user@seazone.com.br",
    "group_level": 2,
    "state": "active",
    "timestamp": "2026-02-28T10:30:00Z",
    "event": "Carnaval",
    "big_operations": null,
    "region": "Nordeste"
  }
]
```


---

### `POST /write-input` — Escrita de regras

Envia a lista completa de regras para o backend AWS. Cada chamada **substitui os dados anteriores** — a aplicação sempre envia o estado completo.

**Headers obrigatórios:**

| Header | Valor |
|----|----|
| `Content-Type` | `application/json` |
| `x-api-key` | Valor de `VITE_API_KEY_READ` |

**Corpo da requisição (JSON):**

```json
{
  "origin": "usuario@seazone.com.br",
  "source": "UI",
  "data": [
    {
      "Grupo/Imóvel": "SZ-12345",
      "Início": "2026-03-01",
      "Fim": "2026-03-15",
      "Valor": 450.00,
      "Acréscimo": 0.15,
      "Fixo / Mínimo / Máximo": "Fixo",
      "Observação": "Preço para alta temporada",
      "Ignorar Hierarquia": false,
      "Origem": "RM",
      "Evento": "Carnaval",
      "Grandes operações (nv. imóvel)": "",
      "Região": "Nordeste"
    }
  ]
}
```

**Estrutura do payload:**

| Campo (raiz) | Tipo | Descrição |
|----|----|----|
| `origin` | `string` | Email do usuário que está realizando a operação |
| `source` | `string` | Sempre `"UI"` (identifica que veio da interface web) |
| `data` | `array` | Lista de regras (ver campos abaixo) |

| Campo (dentro de `data[]`) | Tipo | Descrição |
|----|----|----|
| `Grupo/Imóvel` | `string` | Identificador do grupo ou imóvel |
| `Início` | `string` | Data de início (`YYYY-MM-DD`) |
| `Fim` | `string` | Data de fim (`YYYY-MM-DD`, exclusiva) |
| `Valor` | `number` | Preço em R$ |
| `Acréscimo` | `number` | Percentual de acréscimo (padrão: `0.15`) |
| `Fixo / Mínimo / Máximo` | `string` | Tipo: `"Fixo"`, `"Mínimo"` ou `"Máximo"` |
| `Observação` | `string` | Comentário (string vazia se não houver) |
| `Ignorar Hierarquia` | `boolean` | Se ignora o sistema de hierarquia |
| `Origem` | `string` | Quem solicitou: `"Proprietario"`, `"RM"` ou `"Operacao"` |
| `Evento` | `string` | Nome do evento ou `""` |
| `Grandes operações (nv. imóvel)` | `string` | `"Sim"`, `"Não"` ou `""` (só para nível imóvel) |
| `Região` | `string` | Região brasileira ou `""` |

**Observações importantes sobre a escrita:**

* A aplicação faz **deduplicação** antes de enviar: regras com mesmo `group`, `startDate`, `endDate`, `value` e `type` são enviadas apenas uma vez
* O campo `Grandes operações` é convertido de `boolean` para `string`: `true` → `"Sim"`, `false` → `"Não"`, `null` → `""`
* O campo `Acréscimo` tem fallback para `0.15` se não informado
* O payload pode opcionalmente incluir um campo `columns` na raiz (formato alternativo): `{ "columns": [...], "data": [[...], ...] }`

### Processamento da Lambda `write-input`

Ao receber o payload, a Lambda executa os seguintes passos:

```
1. Converte o payload em DataFrame (renomeia colunas pt-BR → en)
2. Salva source_group = id_seazone (preserva o valor original enviado pelo usuário)
3. Lê setup_groups do S3 (bucket de configuração)
   → Contém: id_seazone, group_name, group_level
4. Faz merge (outer join) com setup_groups:
   → Se o id_seazone pertence a um grupo, expande para os membros do grupo
   → id_seazone passa a ser o ID de cada membro
   → source_group mantém o valor original (nome do grupo)
   → group_level vem do setup_groups (0 se não encontrou grupo)
5. Salva no S3:
   → state=historic (append) — histórico de todas as escritas
   → state=current (overwrite) — estado atual das regras
6. Salva audit_log no S3 (usuário, timestamp, quantidade de regras, source)
7. Atualiza partições no Glue Catalog
```

**Origem dos campos na resposta do** `**read-input**`**:**

| Campo | Origem |
|----|----|
| `source_group` | Valor original enviado pelo usuário no campo `Grupo/Imóvel` |
| `id_seazone` | Pode ser o original ou expandido via `setup_groups` (membros do grupo) |
| `group_level` | Vem do S3 `setup_groups`. Se não encontrou grupo, é `0` (nível Imóvel) |
| `origin` | Email do usuário que fez a escrita |
| `timestamp` | Gerado pela Lambda no momento da escrita |
| Demais campos | Enviados pelo frontend sem alteração |


---

## Fluxo de Operações CRUD (Optimistic Update)

Todas as operações CRUD usam o padrão **optimistic update**: a interface atualiza instantaneamente com os dados locais, e a sincronização com a API acontece em background sem bloquear a UI.

### Criar regra

```
UI (instantâneo):
1. Usuário preenche formulário → addRule(regra)
2. Gera ID local com crypto.randomUUID()
3. Adiciona a regra à lista local (allRulesRef) → tabela atualiza na hora
4. Toast de sucesso

Backend (background):
5. GET /read-input → busca lista FRESCA do backend
6. Adiciona a nova regra à lista fresca
7. POST /write-input → envia lista completa
```

### Editar regra

```
UI (instantâneo):
1. Usuário edita no formulário → editRule(regra)
2. Substitui a regra na lista local (match por ID) → tabela atualiza na hora
3. Toast de sucesso

Backend (background):
4. GET /read-input → busca lista FRESCA do backend
5. Substitui a regra editada na lista fresca
6. POST /write-input → envia lista completa
```

### Excluir regra

```
UI (instantâneo):
1. Usuário confirma exclusão → removeRule(id)
2. Remove a regra da lista local (filter por ID) → tabela atualiza na hora
3. Toast de sucesso

Backend (background):
4. GET /read-input → busca lista FRESCA do backend
5. Remove a regra da lista fresca
6. POST /write-input → envia lista completa
```

### Por que buscar dados frescos antes de escrever?

O `POST /write-input` **substitui todos os dados** no backend. Se a escrita usasse apenas a lista local da UI, regras criadas por outros usuários ou sistemas seriam sobrescritas. Por isso, cada sync busca a lista atual do backend (`GET /read-input`) e aplica a alteração sobre ela.

**Exemplo — outro usuário adicionou a regra E enquanto você tinha a página aberta:**

O backend tem `[A, B, C, E]`, mas sua UI ainda mostra `[A, B, C]`. Você adiciona D:

```
UI (instantâneo):
  Lista local: [A, B, C] + D = [A, B, C, D]
  → Tabela mostra A, B, C, D (sem E, pois a UI não sabe do E)

Backend (background):
  1. GET /read-input → [A, B, C, E]       ← pega o E do outro usuário
  2. Adiciona D     → [A, B, C, E, D]
  3. POST /write-input                     ← envia tudo, E preservado
```

Backend fica com `[A, B, C, E, D]` — a regra E **não foi perdida**. A UI mostra `[A, B, C, D]` até o usuário dar F5, quando o `loadAllRules` traz `[A, B, C, D, E]`.

**Se NÃO buscasse dados frescos:**

```
  1. Pega lista LOCAL → [A, B, C, D]      ← sem o E
  2. POST /write-input                     ← regra E do outro usuário é APAGADA
```

### Funções internas do hook `useRules`

| Função | Responsabilidade |
|----|----|
| `updateLocal(list)` | Atualiza `allRulesRef`, `allRules` e `displayedRules` (re-aplica filtros ativos). É síncrona — a UI reflete a mudança imediatamente |
| `syncAddToApi(rule)` | Busca dados frescos via `GET /read-input`, adiciona a regra, envia via `POST /write-input`. Chamada sem `await` |
| `syncEditToApi(rule)` | Busca dados frescos via `GET /read-input`, substitui a regra, envia via `POST /write-input`. Chamada sem `await` |
| `syncDeleteToApi(id)` | Busca dados frescos via `GET /read-input`, remove a regra, envia via `POST /write-input`. Chamada sem `await` |
| `loadAllRules()` | `GET /read-input` — usado apenas no carregamento inicial da página |

### Consistência: UI vs Backend

O **backend é a fonte da verdade**. A UI pode ficar temporariamente desatualizada:

| Situação | UI | Backend | Resultado |
|----|----|----|----|
| Você salva uma regra | Atualiza na hora | Atualiza em background (com dados frescos) | Consistente |
| Outro usuário altera regras | Não reflete até recarregar | Já atualizado | UI desatualizada |
| Sync falha | Mostra dado optimistic | Não recebeu a alteração | Divergente até recarregar |

A UI **nunca sobrescreve** dados de outros usuários no backend (porque o sync sempre parte de dados frescos). Porém, o backend pode conter alterações que a UI ainda não mostra — para ver o estado real, o usuário deve **recarregar a página** (F5).

### Tratamento de erros

* Se o `POST /write-input` falhar em background, o usuário é notificado via toast de erro
* Os dados locais permanecem com o estado optimistic — ao recarregar a página, o `GET /read-input` traz o estado real do backend
* Não há rollback automático do optimistic update em caso de falha


---

## Tabela de Níveis Hierárquicos (`group_level`)

| group_level | Nome | Prioridade |
|:---:|----|:---:|
| 0 | Imóvel | Mais alta |
| 1 | Cluster | ↓ |
| 2 | Categoria | ↓ |
| 3 | Polígono | ↓ |
| 4 | Carteira | ↓ |
| 5 | Bairro | ↓ |
| 6 | Cidade | ↓ |
| 7 | Microrregião | ↓ |
| 8 | Estado | ↓ |
| 9 | Macrorregião | ↓ |
| 10 | Quartos | ↓ |
| 11 | Strata | ↓ |
| 12 | Padrão | Mais baixa |
| 99 | Inativo | — |

**Regra:** Menor `group_level` = maior prioridade. Uma regra de Imóvel (0) sempre vence uma de Categoria (2).

Na interface, os níveis são simplificados para o usuário:

* `group_level === 0` → "Imóvel"
* `group_level === 2` → "Categoria"
* `group_level >= 3` → "Região"


---

## Algoritmo de Resolução de Hierarquia

Quando múltiplas regras se aplicam ao mesmo imóvel/data, o sistema resolve o conflito em 3 etapas:

### Etapa 1 — Filtragem por data

```
filterByDate(regras, data_alvo)
→ Mantém apenas regras onde: start_date <= data_alvo < end_date
→ Se data_alvo for null, retorna todas
```

A data de fim é **exclusiva**: uma regra de `2026-03-01` a `2026-03-10` **não vale** no dia 10.

### Etapa 2 — Separação e seleção

```
resolveHierarchy(regras)
1. Separa em dois grupos:
   - overrides: regras com ignore_group_level = true
   - normals:   regras com ignore_group_level = false

2. Seleciona o melhor de cada grupo:
   - bestOverride: melhor entre os overrides (por compareRules)
   - bestNormal:   filtra pelo menor group_level, depois melhor por compareRules

3. Compara bestOverride vs bestNormal → vencedor final
```

### Etapa 3 — Comparação entre regras (`compareRules`)

**Mesmo tipo:**

| Tipo | Vence quem tem... |
|----|----|
| Fixo | Maior valor |
| Mínimo | Maior valor |
| Máximo | **Menor** valor |

**Tipos diferentes:** Vence quem tem o **maior valor**, independente da combinação.


---

## Agrupamento de Regras (leitura)

Ao ler do `read-input`, a aplicação agrupa regras individuais que pertencem ao mesmo grupo:

```
Chave de agrupamento: sourceGroup | inicio | fim | valor | tipo | origem
```

Se múltiplas regras compartilham a mesma chave e têm `groupLevel > 0`, são agrupadas em uma única regra com:

* `id`: `group-{sourceGroup}-{inicio}`
* `groupMembers`: lista dos `id_seazone` de cada membro

Regras com `groupLevel === 0` (nível imóvel) nunca são agrupadas.


---

## Mapeamento de Campos: API ↔ Frontend

### Leitura (read-input → Frontend)

| Campo da API | Campo no Frontend | Transformação |
|----|----|----|
| `id_seazone` | `grupoImovel` | Direto |
| `source_group` | `sourceGroup` | Fallback para `id_seazone` se vazio |
| `start_date` | `inicio` | Direto |
| `end_date` | `fim` | Direto |
| `price` | `valor` | Direto |
| `addition` | `acrescimo` | Direto |
| `type` | `tipo` | `"Fixo"` → `"fixo"`, `"Mínimo"` → `"minimo"`, `"Máximo"` → `"maximo"` |
| `comment` | `observacao` | Direto |
| `ignore_group_level` | `ignorarHierarquia` | Direto |
| `comment_origin` | `origem` | Cast para `RuleOrigem` |
| `group_level` | `groupLevel` + `nivel` | Direto + derivado: `0` → Imóvel, `2` → Categoria, `≥3` → Região |
| `event` | `evento` | `null` se vazio |
| `big_operations` | `grandesOperacoes` | `null` se vazio |
| `region` | `regiao` | Cast para `RuleRegiao`, `null` se vazio |
| — | `id` | Gerado: `{id_seazone}-{start_date}-{index}` |

### Escrita (Frontend → write-input)

| Campo no Frontend | Campo no Payload | Transformação |
|----|----|----|
| `sourceGroup` | `Grupo/Imóvel` | Fallback para `grupoImovel` se vazio |
| `inicio` | `Início` | Direto |
| `fim` | `Fim` | Direto |
| `valor` | `Valor` | Direto |
| `acrescimo` | `Acréscimo` | Fallback: `0.15` |
| `tipo` | `Fixo / Mínimo / Máximo` | `"fixo"` → `"Fixo"`, `"minimo"` → `"Mínimo"`, `"maximo"` → `"Máximo"` |
| `observacao` | `Observação` | `""` se vazio |
| `ignorarHierarquia` | `Ignorar Hierarquia` | Direto |
| `origem` | `Origem` | Direto |
| `evento` | `Evento` | `""` se `null` |
| `grandesOperacoes` | `Grandes operações (nv. imóvel)` | `true` → `"Sim"`, `false` → `"Não"`, `null` → `""` |
| `regiao` | `Região` | `""` se `null` |


---

## Autenticação

* **Provedor:** Google OAuth via Lovable Cloud Auth → Supabase
* **Restrição:** Apenas emails `@seazone.com.br`
* **Sessão:** JWT gerenciado pelo Supabase
* O email do usuário é enviado no campo `origin` do payload de escrita para auditoria


---

## Variáveis de Ambiente

| Variável | Descrição |
|----|----|
| `VITE_SUPABASE_URL` | URL do projeto Supabase |
| `VITE_SUPABASE_PUBLISHABLE_KEY` | Chave pública do Supabase |
| `VITE_SUPABASE_PROJECT_ID` | ID do projeto Supabase |
| `VITE_API_URL_READ` | URL do endpoint de leitura (`GET /read-input`) |
| `VITE_API_URL_WRITE` | URL do endpoint de escrita (`POST /write-input`) |
| `VITE_API_KEY_READ` | Chave de API (`x-api-key`) para autenticação nos endpoints Lambda |

Todas as variáveis com prefixo `VITE_` ficam no arquivo `.env` (que está no `.gitignore` e não vai para o repositório).


---

## Estrutura do Projeto

```
src/
├── pages/
│   ├── Index.tsx              → Página principal (abas Regras e Raio-X)
│   └── NotFound.tsx           → Página 404
├── components/
│   ├── Header.tsx             → Cabeçalho (Nova Regra, email, logout)
│   ├── FiltersBar.tsx         → Barra de filtros
│   ├── RulesTable.tsx         → Tabela de regras (50/página)
│   ├── RuleModal.tsx          → Modal de criar/editar com detecção de conflitos
│   ├── RaioXPanel.tsx         → Simulador de hierarquia
│   └── ui/                    → Componentes shadcn-ui
├── hooks/
│   ├── useAuth.tsx            → Autenticação Google/Supabase
│   ├── useRules.ts            → CRUD (optimistic update) + filtros + sync em background
│   └── useRaioXDropdown.ts    → Dados do dropdown do Raio-X
├── lib/
│   ├── specialPricesApi.ts    → POST /write-input (escrita)
│   ├── resolveHierarchy.ts    → Algoritmo de hierarquia
│   └── utils.ts               → Utilitários (cn helper)
├── services/
│   └── rulesService.ts        → GET /read-input (leitura)
├── types/
│   └── rule.ts                → Tipos TypeScript do modelo Rule
└── integrations/
    ├── supabase/              → Cliente Supabase
    └── lovable/               → Auth Lovable Cloud
```


---

## Scripts

| Comando | Descrição |
|----|----|
| `npm run dev` | Servidor de desenvolvimento (porta 8080) |
| `npm run build` | Build de produção |
| `npm run test` | Testes unitários (Vitest) |
| `npm run lint` | Lint com ESLint |