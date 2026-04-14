<!-- title: MCP Grafana | url: https://outline.seazone.com.br/doc/mcp-grafana-IBP3GRGLFH | area: Tecnologia -->

# MCP Grafana

# Configuração do Grafana MCP Server no Claude Code

Token do grafana no vault : 

<https://vault.seazone.com.br/ui/vault/secrets/secret/kv/Ferramentas%2Fgrafana_sa_token/details?version=1>

Pré-requisitos

* Claude Code instalado
* Acesso ao Grafana

## Passo 1 — Criar Service Account no Grafana


1. Acesse o Grafana → **Administration → Service Accounts (Ou caso não for ADM, usar a SA do vault)** 
2. Clique em **Add service account**
3. Nome: `claude-code` | Role: **Editor**
4. Clique em **Create**
5. Na página do service account, clique em **Add service account token**
6. Copie e guarde o token gerado (aparece apenas uma vez)

## Passo 2 — Configurar o MCP Server

Edite (ou crie) o arquivo `~/.claude/settings.json`:

```json
{
  "mcpServers": {
    "grafana": {
      "command": "npx",
      "args": ["-y", "@grafana/mcp-server"],
      "env": {
        "GRAFANA_URL": "https://monitoring.seazone.com.br",
        "GRAFANA_API_KEY": "<token-do-service-account>"
      }
    }
  }
}
```

> Substitua `<token-do-service-account>` pelo token gerado no Passo 1.

## Passo 3 — Reiniciar o Claude Code

Feche e abra novamente o Claude Code para que o MCP server seja carregado.

## Passo 4 — Validar a conexão

Após reiniciar, peça ao Claude:

> "Liste os datasources disponíveis no Grafana"

Se retornar a lista de datasources, a conexão está funcionando.

## O que o Claude consegue fazer com essa integração

* Criar e editar dashboards
* Listar datasources, dashboards e folders
* Consultar métricas disponíveis
* Gerar painéis com queries prontas (Prometheus, ClickHouse, Loki, etc.)