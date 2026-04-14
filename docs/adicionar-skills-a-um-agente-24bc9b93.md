<!-- title: Adicionar Skills a um Agente | url: https://outline.seazone.com.br/doc/adicionar-skills-a-um-agente-5Gnpofy62g | area: Tecnologia -->

# Adicionar Skills a um Agente

# Adicionar Skills a um Agente

Skills são capacidades que equipam o agente com ferramentas e comportamentos específicos. Cada skill é uma pasta contendo um arquivo `SKILL.md` com instruções e metadados.

**Referência oficial:** [docs.openclaw.ai/tools/skills](https://docs.openclaw.ai/tools/skills)


---

## Conceitos Básicos

| Conceito | Descrição |
|----|----|
| **Skill** | Pasta com um `SKILL.md` que define uma capacidade do agente |
| **ClawHub** | Marketplace oficial de skills ([clawhub.com](https://clawhub.com)) — 13.700+ skills disponíveis |
| **Plugin** | Pacote que pode conter múltiplas skills e ferramentas |
| **Workspace skills** | Skills específicas de um agente (maior prioridade) |
| **Managed skills** | Skills compartilhadas entre todos os agentes da máquina |


---

## Prioridade de Carregamento

As skills são carregadas nesta ordem de prioridade (maior → menor):


1. **Workspace skills** — `<workspace>/skills/` (ex: `~/.openclaw/workspaces/meu-agente/skills/`)
2. **Managed/local skills** — `~/.openclaw/skills/` (compartilhadas entre agentes)
3. **Bundled skills** — incluídas na instalação do OpenClaw

> Quando há conflito de nomes, a skill do workspace sobrescreve as demais.

Diretórios adicionais podem ser configurados via `skills.load.extraDirs` no `openclaw.json`.


---

## Adicionar Skills via CLI

### Pré-requisito: conectar na EC2

```bash
# Via AWS Console: EC2 > Instances > openclaw (i-05a410435fcca3183) > Connect > Session Manager
# Ou via terminal:
aws ssm start-session --target i-05a410435fcca3183 --region sa-east-1

# Entrar no container
sudo docker exec -it openclaw-gateway sh
```

### Buscar skills no marketplace

```bash
openclaw skills search <palavra-chave>
```

### Instalar uma skill do ClawHub

```bash
# Instala no workspace do agente ativo
openclaw skills install <skill-slug>

# Instalar versão específica
openclaw skills install <skill-slug>@<version>

# Instalar via plugin (pacote com múltiplas skills)
openclaw plugins install clawhub:<package-name>
```

### Atualizar skills instaladas

```bash
openclaw skills update --all
```

### Listar skills carregadas

```bash
openclaw skills list
```


---

## Criar uma Skill Customizada (CLI)

### 1. Skill específica de um agente

Crie uma pasta dentro do workspace do agente:

```bash
mkdir -p ~/.openclaw/workspaces/meu-agente/skills/minha-skill
```

Crie o arquivo `SKILL.md` com frontmatter YAML:

```markdown
---
name: minha-skill
description: Descrição breve do que a skill faz
user-invocable: true
---

## Instruções

Aqui vão as instruções que o agente seguirá quando esta skill for ativada.

Você pode usar `{baseDir}` para referenciar o diretório da skill.
```

A skill será carregada automaticamente na próxima sessão do agente.

### 2. Skill compartilhada (todos os agentes)

```bash
mkdir -p ~/.openclaw/skills/skill-compartilhada

cat > ~/.openclaw/skills/skill-compartilhada/SKILL.md << 'EOF'
---
name: skill-compartilhada
description: Skill disponível para todos os agentes da máquina
user-invocable: true
---

Instruções da skill aqui.
EOF
```


---

## Formato do SKILL.md

### Campos do Frontmatter

| Campo | Tipo | Default | Descrição |
|----|----|----|----|
| `name` | string | — | Identificador único da skill (obrigatório) |
| `description` | string | — | Descrição breve — aparece na listagem e na UI (obrigatório) |
| `user-invocable` | boolean | `true` | Expõe a skill como slash command (`/nome-da-skill`) |
| `disable-model-invocation` | boolean | `false` | Remove do prompt do modelo (skill só é chamada explicitamente) |
| `command-dispatch` | string | — | `tool` para dispatch direto sem passar pelo modelo |
| `command-tool` | string | — | Nome da tool para dispatch direto |
| `command-arg-mode` | string | `raw` | Como os argumentos são passados |
| `homepage` | string | — | URL exibida como "Website" na UI |
| `metadata` | JSON | — | Objeto JSON inline para gating e configuração |

### Exemplo mínimo

```markdown
---
name: status-check
description: Verifica status das aplicações no ArgoCD
---

Quando o usuário pedir status, liste todas as aplicações ArgoCD e seu estado de sync.
```

### Exemplo com metadata (gating por dependências)

O campo `metadata` permite controlar quando a skill é carregada:

```markdown
---
name: deploy-checker
description: Verifica status de deploys no ArgoCD
metadata: {"openclaw":{"requires":{"bins":["kubectl","argocd"]},"emoji":"🚀"}}
---

Instruções para verificar status de deploys...
```

### Opções de gating disponíveis

```json
{
  "openclaw": {
    "always": true,
    "emoji": "🚀",
    "os": ["darwin", "linux", "win32"],
    "requires": {
      "bins": ["binary1", "binary2"],
      "anyBins": ["bin1", "bin2"],
      "env": ["ENV_VAR_OBRIGATORIA"],
      "config": ["openclaw.json.paths"]
    },
    "primaryEnv": "API_KEY_ENV_VAR"
  }
}
```

| Opção | Descrição |
|----|----|
| `always: true` | Ignora todos os filtros — sempre carrega |
| `os` | Restringe a plataformas específicas |
| `requires.bins` | Todos os binários listados devem existir no PATH |
| `requires.anyBins` | Pelo menos um deve existir |
| `requires.env` | Variáveis de ambiente obrigatórias |
| `requires.config` | Paths no openclaw.json que devem ser truthy |
| `primaryEnv` | Vincula a `skills.entries.<name>.apiKey` no config |


---

## Configurar Skills no openclaw.json

Para habilitar/desabilitar skills, injetar variáveis de ambiente ou API keys, edite `/opt/openclaw/config/openclaw.json`:

```json
{
  "skills": {
    "entries": {
      "minha-skill": {
        "enabled": true,
        "apiKey": {
          "source": "env",
          "provider": "default",
          "id": "API_KEY_VAR"
        },
        "env": {
          "API_URL": "https://api.exemplo.com"
        },
        "config": {
          "customKey": "valor"
        }
      }
    },
    "load": {
      "extraDirs": ["/caminho/para/skills-extras"],
      "watch": true,
      "watchDebounceMs": 250
    }
  }
}
```

| Campo | Descrição |
|----|----|
| `enabled: false` | Desabilita a skill (mesmo bundled) |
| `env` | Injeta variáveis de ambiente (só se não existirem) |
| `apiKey` | Conveniência para `primaryEnv` no metadata |
| `config` | Campos customizados acessíveis pela skill |
| `load.extraDirs` | Diretórios adicionais para buscar skills |
| `load.watch` | Hot reload — recarrega skills ao editar `SKILL.md` |

> **Nota:** Variáveis injetadas via `env` são scoped ao runtime do agente, não afetam o shell global.


---

## Adicionar Skills via UI

A interface web do OpenClaw permite gerenciar skills de forma visual:


1. Acesse [garra.seazone.com.br](https://garra.seazone.com.br)
2. Navegue até o agente desejado
3. Na seção **Skills**, você pode:
   * **Buscar** skills disponíveis no ClawHub
   * **Instalar** com um clique
   * **Habilitar/desabilitar** skills individuais
   * **Configurar** variáveis de ambiente e API keys por skill

> Alterações feitas pela UI são salvas no `openclaw.json` e no workspace do agente — equivalente aos comandos CLI.


---

## Exemplo Prático: Adicionando Skills SRE ao Garra

```bash
# 1. Conectar na EC2 e entrar no container
sudo docker exec -it openclaw-gateway sh

# 2. Instalar plugin de skills SRE da Seazone via marketplace
openclaw plugins install clawhub:sre@seazone-skills

# 3. Verificar que as skills foram carregadas
openclaw skills list

# 4. Reiniciar para aplicar (se watch não estiver habilitado)
openclaw gateway restart
```

### Alternativa: criar skill SRE manualmente

```bash
mkdir -p ~/.openclaw/workspaces/garra/skills/sre-deploy

cat > ~/.openclaw/workspaces/garra/skills/sre-deploy/SKILL.md << 'EOF'
---
name: sre-deploy
description: Deploy de aplicações ArgoCD seguindo padrões Seazone
user-invocable: true
metadata: {"openclaw":{"requires":{"bins":["kubectl"]},"emoji":"🚀"}}
---

## Instruções

Ao receber um pedido de deploy, siga o padrão App-of-Apps da Seazone:

1. Pergunte: nome da app, chart Helm, namespace, cluster (EKS ou GKE)
2. Crie application.yaml com multi-source pattern
3. Inclua labels de custo obrigatórias (cluster, region, product, BU)
4. Configure ExternalSecret se necessário
5. Registre no app-of-apps correspondente (cluster-services, monitoring ou tools)
EOF
```


---

## Estrutura de Skills no Workspace

```
~/.openclaw/workspaces/meu-agente/
├── AGENTS.md
├── SOUL.md
├── USER.md
├── IDENTITY.md
├── TOOLS.md
└── skills/
    ├── skill-do-clawhub/           ← instalada via CLI/UI
    │   └── SKILL.md
    └── minha-skill-customizada/    ← criada manualmente
        ├── SKILL.md
        └── scripts/                ← (opcional) scripts auxiliares
            └── helper.sh
```

Skills compartilhadas ficam em:

```
~/.openclaw/skills/
├── skill-compartilhada-a/
│   └── SKILL.md
└── skill-compartilhada-b/
    └── SKILL.md
```


---

## Segurança

* Sempre **revise o conteúdo** de skills de terceiros antes de instalar
* O ClawHub faz scan automático de `SKILL.md` e scripts para padrões suspeitos
* Skills de workspace/extra-dir são validadas — o realpath deve permanecer dentro dos roots configurados
* Variáveis em `skills.entries.*.env` e `apiKey` injetam secrets no processo do agente — mantenha fora de prompts/logs
* Para agentes em sandbox, binários requeridos devem existir no container via `setupCommand`


---

## Referência Rápida de Comandos

| Comando | Descrição |
|----|----|
| `openclaw skills search <termo>` | Buscar skills no ClawHub |
| `openclaw skills install <slug>` | Instalar skill no workspace ativo |
| `openclaw skills install <slug>@<ver>` | Instalar versão específica |
| `openclaw skills update --all` | Atualizar todas as skills |
| `openclaw skills list` | Listar skills carregadas |
| `openclaw plugins install clawhub:<pkg>` | Instalar plugin do marketplace |
| `openclaw gateway restart` | Reiniciar gateway (aplicar mudanças) |