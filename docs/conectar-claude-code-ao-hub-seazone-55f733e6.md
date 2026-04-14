<!-- title: Conectar Claude Code ao Hub Seazone | url: https://outline.seazone.com.br/doc/conectar-claude-code-ao-hub-seazone-TrceLrU6Ql | area: Tecnologia -->

# Conectar Claude Code ao Hub Seazone

Pré-requisito: ter uma API key do hub com compatibilidade Claude Code habilitada. Crie em https://ai-portal.seazone.properties (aba Nova Key, marque "Habilitar compatibilidade com Claude Code").


---

## Linux / macOS

```bash
# 1. Deslogar da conta Anthropic (se estiver logado)
claude logout

# 2. Configurar (zsh — padrão no macOS)
echo 'export ANTHROPIC_BASE_URL="https://hub.seazone.dev"' >> ~/.zshrc
echo 'export ANTHROPIC_API_KEY="sk-sz-SUA-KEY"' >> ~/.zshrc
echo 'export CLAUDE_CODE_SKIP_LOGIN=1' >> ~/.zshrc
source ~/.zshrc

# Se usa bash ao invés de zsh, troque ~/.zshrc por ~/.bashrc

# 3. Testar
claude
```

## Windows

```powershell
# 1. Deslogar da conta Anthropic (se estiver logado)
claude logout

# 2. Configurar (PowerShell)
[System.Environment]::SetEnvironmentVariable("ANTHROPIC_BASE_URL", "https://hub.seazone.dev", "User")
[System.Environment]::SetEnvironmentVariable("ANTHROPIC_API_KEY", "sk-sz-SUA-KEY", "User")
[System.Environment]::SetEnvironmentVariable("CLAUDE_CODE_SKIP_LOGIN", "1", "User")

# 3. Fechar e reabrir o terminal

# 4. Testar
claude
```

## Reverter (voltar pra conta Anthropic)

Linux/macOS:

```bash
# Remover as linhas do ~/.zshrc ou ~/.bashrc manualmente, depois:
unset ANTHROPIC_BASE_URL ANTHROPIC_API_KEY CLAUDE_CODE_SKIP_LOGIN
claude login
```

Windows:

```powershell
[System.Environment]::SetEnvironmentVariable("ANTHROPIC_BASE_URL", $null, "User")
[System.Environment]::SetEnvironmentVariable("ANTHROPIC_API_KEY", $null, "User")
[System.Environment]::SetEnvironmentVariable("CLAUDE_CODE_SKIP_LOGIN", $null, "User")
# Fechar e reabrir o terminal
claude login
```