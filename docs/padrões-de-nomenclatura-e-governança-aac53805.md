<!-- title: Padrões de Nomenclatura e Governança | url: https://outline.seazone.com.br/doc/padroes-de-nomenclatura-e-governanca-qWQKb0DFge | area: Tecnologia -->

# Padrões de Nomenclatura e Governança

> Como organizamos senhas, pastas e grupos no Cofre Seazone. Este documento é a referência oficial — qualquer mudança na estrutura deve seguir estes padrões.


---

## Visão Geral da Estrutura

O cofre é organizado em três níveis: **pastas**, **grupos** e **permissões**. A ideia é simples: cada time grande tem sua pasta e seu grupo. Dentro, sub-times organizam suas credenciais em sub-pastas.

```mermaidjs
flowchart TD
    ROOT(["COFRE SEAZONE"])
    ROOT --> SRE["SRE"]
    ROOT --> RES["RESERVAS"]
    ROOT --> WAL["WALLET"]
    ROOT --> HOS["HOSPEDAGEM"]
    ROOT --> COM["COMERCIAL"]

    SRE --> SRE1["AWS"]
    SRE --> SRE2["GCP"]
    SRE --> SRE3["FERRAMENTAS"]

    RES --> RES1["BACKEND"]
    RES --> RES2["BANCO DE DADOS"]

    style ROOT fill:#1e40af,color:#fff,stroke:none
    style SRE fill:#1e293b,color:#e2e8f0,stroke:#475569
    style RES fill:#1e293b,color:#e2e8f0,stroke:#475569
    style WAL fill:#1e293b,color:#e2e8f0,stroke:#475569
    style HOS fill:#1e293b,color:#e2e8f0,stroke:#475569
    style COM fill:#1e293b,color:#e2e8f0,stroke:#475569
```


---

## Regras de Nomenclatura

### Pastas

| Regra | Exemplo |
|----|----|
| Sempre em **MAIÚSCULO** | `SRE`, `RESERVAS`, `WALLET` |
| Sem acentos ou caracteres especiais | `COMERCIAL` (não "COMERCIAL!") |
| Sub-pastas seguem o mesmo padrão | `SRE / AWS / PRODUÇÃO` |
| Nome deve refletir o time ou contexto | `FERRAMENTAS`, `BANCO DE DADOS` |

### Grupos

| Regra | Exemplo |
|----|----|
| Nome do time em **minúsculo** | `sre`, `reservas`, `wallet` |
| Sub-times com prefixo do time pai | `sre-infra`, `reservas-backend` |
| Grupo admin fixo: `admin` | Nunca renomear ou remover |

### Senhas (recursos)

| Regra | Exemplo |
|----|----|
| Nome descritivo com contexto | `aceso_AWS Console — Produção` |
| Incluir ambiente quando relevante | `RDS Reservas — STG`, `GCP Console — PRD` |
| Separador: travessão com espaço (`—`) | Não usar `/`, `\|`, ou `:` |
| URI sempre preenchida | `https://console.aws.amazon.com` |
| Incluit descrição como boa prática | Essa senha é x do time x e faz x |


---

## Modelo de Permissões

```mermaidjs
flowchart LR
    subgraph admin["Grupo: admin"]
        A["Acesso total\na TODAS as pastas"]
    end

    subgraph time["Grupo: sre"]
        B["Acesso à pasta SRE\ne sub-pastas"]
    end

    subgraph sub["Grupo: sre-infra"]
        C["Acesso à sub-pasta\nSRE / AWS"]
    end

    admin ---|"é dono"| TUDO["Todas as pastas"]
    time ---|"pode ler/editar"| PASTA["Pasta do time"]
    sub ---|"pode ler/editar"| SUB["Sub-pasta específica"]

    style admin fill:#7f1d1d22,stroke:#ef4444
    style time fill:#1e40af22,stroke:#3b82f6
    style sub fill:#16653422,stroke:#22c55e
```

### Regras de ouro


1. **O grupo** `**admin**` **é dono de todas as pastas** — sempre. Isso garante que o time de governança nunca perde acesso, mesmo que um membro saia.
2. **Cada time grande tem um grupo** — `sre`, `reservas`, `wallet`, `hospedagem`, `comercial`. O grupo tem permissão na pasta raiz do time.
3. **Sub-times herdam do grupo pai** — membros de `sre-infra` também devem estar no grupo `sre`. A hierarquia garante acesso em cascata.
4. **Senhas compartilhadas entre times** ficam numa pasta `FERRAMENTAS` na raiz, acessível pelos grupos envolvidos.
5. **Senhas pessoais** (não compartilhadas) ficam no espaço individual de cada usuário — sem pasta obrigatória.


---

## Ciclo de Vida

### Novo time ou sub-time

```mermaidjs
flowchart LR
    A["Admin cria\no grupo"] --> B["Admin cria\na pasta (MAIÚSCULO)"]
    B --> C["Compartilha pasta\ncom o grupo"]
    C --> D["Adiciona membros\nao grupo"]

    style A fill:#1e40af,color:#fff,stroke:none
    style D fill:#166534,color:#fff,stroke:none
```


1. Criar o grupo no painel **Usuários → Grupos**
2. Criar a pasta com nome em MAIÚSCULO
3. Compartilhar a pasta com o grupo (permissão: **pode editar**)
4. Compartilhar a pasta com o grupo `admin` (permissão: **é dono**)
5. Adicionar os membros ao grupo

### Membro saiu do time


1. Remover o membro do grupo correspondente
2. As senhas compartilhadas continuam acessíveis para o restante do time
3. Se saiu da empresa: desabilitar ou deletar o usuário (ver doc de Administração)

### Time deixou de existir


1. Mover senhas relevantes para os times que absorveram as responsabilidades
2. Remover membros do grupo
3. Deletar o grupo
4. Deletar a pasta (o grupo `admin` mantém backup via acesso de dono)


---

## Checklist para Auditoria Periódica

A cada **trimestre**, o admin deve verificar:

- [ ] Todos os grupos ainda refletem a estrutura real dos times?
- [ ] O grupo `admin` é dono de todas as pastas?
- [ ] Existem usuários inativos que deveriam ser desabilitados?
- [ ] Existem senhas sem dono (owner saiu da empresa)?
- [ ] A nomenclatura das pastas segue o padrão MAIÚSCULO?
- [ ] Senhas compartilhadas entre times estão na pasta `COMPARTILHADO`?