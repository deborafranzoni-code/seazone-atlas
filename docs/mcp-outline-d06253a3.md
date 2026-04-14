<!-- title: MCP Outline | url: https://outline.seazone.com.br/doc/mcp-outline-fLR1WxYbjw | area: Tecnologia -->

# MCP Outline

# Configuração do Outline MCP Server no Claude Code

Permite ao Claude Code pesquisar, ler, criar e editar documentos diretamente na wiki interna (Outline).

## Pré-requisitos

* Claude Code instalado
* Conta ativa no Outline da Seazone
* Python 3.10+ com `uv` instalado ([docs de instalação](https://docs.astral.sh/uv/getting-started/installation/))

## Passo 1 — Gerar API Key no Outline


1. Acesse https://outline.seazone.com.br/settings/api
2. Clique em **New API Key**
3. Copie e guarde o token gerado (formato: `ol_api_...`)

## Passo 2 — Configurar o MCP Server

Execute o comando abaixo no terminal para registrar o MCP server globalmente no Claude Code:

```bash
claude mcp add --global outline \
  -e OUTLINE_API_KEY="ol_api_SEU_TOKEN_AQUI" \
  -e OUTLINE_API_URL="https://outline.seazone.com.br/api" \
  -- uvx mcp-outline
```

> Substitua `ol_api_SEU_TOKEN_AQUI` pelo token gerado no Passo 1.

Isso adiciona a seguinte entrada no `~/.claude.json`:

```json
{
  "mcpServers": {
    "outline": {
      "type": "stdio",
      "command": "uvx",
      "args": ["mcp-outline"],
      "env": {
        "OUTLINE_API_KEY": "ol_api_SEU_TOKEN_AQUI",
        "OUTLINE_API_URL": "https://outline.seazone.com.br/api"
      }
    }
  }
}
```

## Passo 3 — Reiniciar o Claude Code

Feche e abra novamente o Claude Code para que o MCP server seja carregado.

## Passo 4 — Validar a conexão


1. Digite `/mcp` no Claude Code — o Outline deve aparecer na lista com status **connected**
2. Peça ao Claude:

> "Liste as collections disponíveis no Outline"

Se retornar a lista de collections, a conexão está funcionando.

## O que o Claude consegue fazer com essa integração

| Ferramenta | Descrição |
|----|----|
| `search_documents` | Pesquisar documentos por palavras-chave |
| `read_document` | Ler conteúdo completo de um documento |
| `create_document` | Criar novo documento em uma collection |
| `update_document` | Editar documento existente |
| `list_collections` | Listar todas as collections do workspace |
| `get_collection_structure` | Ver hierarquia de documentos de uma collection |
| `add_comment` | Adicionar comentário a um documento |
| `archive_document` / `delete_document` | Arquivar ou deletar documentos |
| `move_document` | Mover documento entre collections |
| `ask_ai_about_documents` | Perguntar sobre documentos usando IA do Outline |

## Exemplos de uso no Claude Code

```
Pesquise no Outline documentos sobre runbooks de incidente
Crie um documento no Outline com o post-mortem do incidente de hoje
Atualize a página de onboarding no Outline com as novas instruções
Qual a estrutura de documentos dentro da collection de Tecnologia?
```

## Troubleshooting

| Problema | Solução |
|----|----|
| Status **disconnected** no `/mcp` | Verifique se `uvx` está no PATH (`which uvx`) |
| Erro de autenticação (401/403) | Regenere a API Key em https://outline.seazone.com.br/settings/api |
| Timeout na conexão | Verifique se a URL da API está correta (`https://outline.seazone.com.br/api`) |
| Pacote não encontrado | Execute `uv tool install mcp-outline` para instalar manualmente |

Para testar manualmente se o pacote funciona:

```bash
uvx mcp-outline
# Deve iniciar sem erros e aguardar input via stdin (ctrl+c para sair)
```

## Referências

* Pacote: [mcp-outline no PyPI](https://pypi.org/project/mcp-outline/)
* Repositório: [github.com/nichochar/mcp-outline](https://github.com/nichochar/mcp-outline)
* API do Outline: https://outline.seazone.com.br/api