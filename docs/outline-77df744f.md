<!-- title: outline | url: https://outline.seazone.com.br/doc/outline-6mf6d2gVh1 | area: Tecnologia -->

# outline

**Cluster de origem:** cluster-tools-prod-gke (us-central1-a) **Decisão:** Descontinuar o Outline e consolidar documentação no Notion/Canvas (já utilizado pela empresa) **Dependência:** Este passo pode ser executado independentemente das demais migrações de infraestrutura

> **Claude Code executa** toda a parte técnica: exportação via API, scripts bash, desligamento da Application ArgoCD e limpeza do namespace. O processo de importação no Notion/Canvas é trabalho humano e não muda.


---

## Sumário


1. [Inventário do Outline](#1-invent%C3%A1rio-do-outline)
2. [Exportação dos Documentos](#2-exporta%C3%A7%C3%A3o-dos-documentos)
3. [Importação no Notion/Canvas](#3-importa%C3%A7%C3%A3o-no-notioncanvas)
4. [Comunicação para os Usuários](#4-comunica%C3%A7%C3%A3o-para-os-usu%C3%A1rios)
5. [Ordem Recomendada de Execução](#5-ordem-recomendada-de-execu%C3%A7%C3%A3o)
6. [Desligamento do Outline](#6-desligamento-do-outline)
7. [Rollback — Restaurar o Outline](#7-rollback--restaurar-o-outline)


---

## 1. Inventário do Outline

Antes de exportar qualquer coisa, é essencial entender o volume e estrutura do conteúdo existente. Claude Code executa as chamadas de API e apresenta o resultado.

### 1.1 Acesso via API REST

A API do Outline usa autenticação via Bearer token. Gere um token em **Settings → API Tokens** no painel do Outline.

```bash

export OUTLINE_URL="https://outline.seazone.com.br"  # ajuste para a URL real

export OUTLINE_TOKEN="<seu-api-token>"
```

### 1.2 Listar todas as Collections

```bash

curl -s -X POST "$OUTLINE_URL/api/collections.list" \
  -H "Authorization: Bearer $OUTLINE_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"limit": 100, "offset": 0}' | jq '.data | length, [.[] | {id, name, documentsCount}]'
```

### 1.3 Contar total de documentos

```bash
# Total de documentos publicados

curl -s -X POST "$OUTLINE_URL/api/documents.list" \
  -H "Authorization: Bearer $OUTLINE_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"limit": 1}' | jq '.pagination.total'
```

```bash
# Documentos arquivados (não aparecem na listagem padrão)
curl -s -X POST "$OUTLINE_URL/api/documents.archived" \
  -H "Authorization: Bearer $OUTLINE_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"limit": 1}' | jq '.pagination.total'
```

### 1.4 Tabela de Inventário (preencher antes da migração)

| Métrica | Valor |
|----|----|
| Total de Collections | — |
| Total de Documentos publicados | — |
| Total de Documentos arquivados | — |
| Usuários ativos (últimos 30 dias) | — |
| Tamanho estimado (anexos/imagens) | — |
| Data do inventário | — |
| Responsável | — |

### 1.5 Listar usuários ativos

```bash

curl -s -X POST "$OUTLINE_URL/api/users.list" \
  -H "Authorization: Bearer $OUTLINE_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"limit": 100, "filter": "active"}' | jq '[.data[] | {name, email, lastActiveAt}]'
```


---

## 2. Exportação dos Documentos

Claude Code executa o script de exportação integralmente em minutos — não é trabalho prévio.

### 2.1 Formatos de Exportação Disponíveis

| Formato | Suporte | Adequado para Notion | Adequado para Canvas |
|----|----|----|----|
| **Markdown (.md)** | Nativo via API | Sim (importação direta) | Sim |
| **HTML (.html)** | Nativo via API | Parcial (perde formatação) | Parcial |
| **ZIP (collection)** | Export bulk via UI/API | Sim | Sim |

**Recomendação:** usar Markdown para Notion (suporte nativo) e ZIP para backup.

### 2.2 Exportação via Interface Web (mais simples)


1. Acesse o Outline como administrador
2. Vá em **Settings → Export**
3. Clique em **"Export all collections"** — gera um ZIP com todos os documentos em Markdown
4. Guarde o arquivo ZIP como backup offline antes de qualquer remoção

### 2.3 Exportação via API — Collection por Collection

Claude Code executa este script ao vivo e salva os ZIPs localmente:

```bash
#!/bin/bash
# export-outline.sh — exporta todas as collections em Markdown

export OUTLINE_URL="https://outline.seazone.com.br"
export OUTLINE_TOKEN="<seu-api-token>"
EXPORT_DIR="./outline-export-$(date +%Y%m%d)"
mkdir -p "$EXPORT_DIR"

# 1. Listar collections

COLLECTIONS=$(curl -s -X POST "$OUTLINE_URL/api/collections.list" \
  -H "Authorization: Bearer $OUTLINE_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"limit": 100}' | jq -r '.data[] | "\(.id) \(.name)"')

echo "Collections encontradas:"
echo "$COLLECTIONS"

# 2. Exportar cada collection

while IFS= read -r line; do
  COLLECTION_ID=$(echo "$line" | awk '{print $1}')
  COLLECTION_NAME=$(echo "$line" | awk '{$1=""; print $0}' | xargs)

  echo "Exportando: $COLLECTION_NAME ($COLLECTION_ID)"

  # Solicitar exportação
  EXPORT_RESPONSE=$(curl -s -X POST "$OUTLINE_URL/api/collections.export" \
    -H "Authorization: Bearer $OUTLINE_TOKEN" \
    -H "Content-Type: application/json" \
    -d "{\"id\": \"$COLLECTION_ID\", \"format\": \"markdown\"}")

  FILE_OPERATION_ID=$(echo "$EXPORT_RESPONSE" | jq -r '.data.fileOperation.id')

  # Aguardar conclusão
  echo "Aguardando exportação ($FILE_OPERATION_ID)..."
  for i in {1..30}; do
    STATUS=$(curl -s -X POST "$OUTLINE_URL/api/fileOperations.info" \
      -H "Authorization: Bearer $OUTLINE_TOKEN" \
      -H "Content-Type: application/json" \
      -d "{\"id\": \"$FILE_OPERATION_ID\"}" | jq -r '.data.state')
    if [ "$STATUS" = "complete" ]; then
      echo "Pronto!"
      break
    fi
    sleep 2
  done

  # Baixar arquivo
  curl -s -X POST "$OUTLINE_URL/api/fileOperations.redirect" \
    -H "Authorization: Bearer $OUTLINE_TOKEN" \
    -H "Content-Type: application/json" \
    -d "{\"id\": \"$FILE_OPERATION_ID\"}" \
    -o "$EXPORT_DIR/${COLLECTION_NAME}.zip" -L

done <<< "$COLLECTIONS"

echo "Exportação concluída em: $EXPORT_DIR"
```

### 2.4 Exportação de Documento Individual

```bash
# Exportar um documento específico em Markdown

curl -s -X POST "$OUTLINE_URL/api/documents.export" \
  -H "Authorization: Bearer $OUTLINE_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"id": "<document-id>"}' | jq -r '.data'
```

### 2.5 Validação da Exportação

```bash
# Verificar arquivos gerados

ls -lh $EXPORT_DIR/
unzip -l $EXPORT_DIR/*.zip | head -50

# Contar documentos exportados

find $EXPORT_DIR -name "*.md" | wc -l
```

**Checklist de validação:**

- [ ] Todos os ZIPs foram baixados sem erro (verificar tamanho > 0)
- [ ] Quantidade de documentos no export bate com o inventário
- [ ] Abrir amostra de 5-10 documentos e verificar conteúdo
- [ ] Verificar se imagens/anexos foram incluídos
- [ ] Guardar backup do ZIP em local seguro (S3, Google Drive, etc.)


---

## 3. Importação no Notion/Canvas

Esta etapa é trabalho humano — não há automação para substituir a revisão e organização dos documentos no destino.

### 3.1 Importação no Notion

O Notion suporta importação nativa de Markdown e de arquivos ZIP do Outline.

**Via interface:**


1. No Notion, clique em **"+ New page"** ou abra um workspace existente
2. Clique em **"Import"** (menu lateral esquerdo → `...` → Import)
3. Selecione **"Outline"** (se disponível) ou **"Markdown & CSV"**
4. Faça upload do arquivo ZIP gerado pelo Outline
5. O Notion cria automaticamente a hierarquia de páginas

**Limitações conhecidas:**

* Tabelas complexas podem perder formatação
* Blocos de código mantêm conteúdo mas podem perder syntax highlighting
* Imagens inline podem precisar de reupload manual
* Links internos entre documentos podem quebrar — verificar após importação

**Ferramenta auxiliar (para grandes volumes):**

```bash
# notion-import-cli (se disponível)
npm install -g @notionhq/client
# ou usar a API do Notion para upload programático
```

### 3.2 Importação no Canvas (Slack)

O Slack Canvas aceita conteúdo rich text mas não tem importação em lote de Markdown.

**Processo manual:**


1. Crie um Canvas no Slack para cada Collection do Outline
2. Copie o conteúdo Markdown e cole diretamente no Canvas (o Slack renderiza headers e listas)
3. Para documentos longos, divida em múltiplos Canvases ou use seções

**Ferramenta auxiliar via API do Slack:**

Consulte o arquivo `/docs/openclaw-criar-agente-slack.md` no repositório para referências de automação via API do Slack.

### 3.3 Priorização da Importação

| Prioridade | Tipo de Conteúdo | Destino Recomendado |
|----|----|----|
| Alta | Runbooks operacionais | Notion (equipe SRE) |
| Alta | Documentação de produto | Notion (equipes de produto) |
| Alta | Processos e políticas | Notion (RH/Ops) |
| Média | Atas de reunião | Notion ou Canvas |
| Baixa | Rascunhos e WIP | Notion (arquivar) |
| Baixa | Documentos desatualizados | Avaliar descarte |


---

## 4. Comunicação para os Usuários

O Outline é ferramenta interna — não há necessidade de aviso com semanas de antecedência. Dois dias são suficientes para que o time salve ou revise o que precisar.

### 4.1 Cronograma de Comunicação

| Quando | Canal | Mensagem |
|----|----|----|
| **D-2** (2 dias antes) | Slack #geral + email | Aviso inicial: Outline será descontinuado |
| **D-1** (1 dia antes) | Slack #geral | Lembrete + link para o Notion/Canvas já populado |
| **D-1** | Slack DM para usuários ativos | Aviso individual para quem usa ativamente |
| **D0** | Slack #geral | Outline desligado. Links alternativos: \[Notion\] |

### 4.2 Template de Mensagem (Slack)

```
:outline: *Migração do Outline → Notion*

Olá, time!

Estamos consolidando nossa documentação no Notion, que já usamos no dia a dia.
O Outline será desligado em *[DATA]*.

*O que você precisa fazer:*
• Verifique se seus documentos importantes estão no Notion
• Atualize links internos que apontam para o Outline
• Em caso de dúvidas, fale com [NOME_RESPONSAVEL] no canal #tech-infra

*Links úteis:*
• Notion: https://notion.so/seazone
• Notion do SRE/Infra: [link específico]

Caso precise de algum documento que não foi migrado, entre em contato antes de [DATA].

Obrigado! 🙏
```

### 4.3 Lista de Verificação de Comunicação

- [ ] Identificar owner do Outline (quem vai ser o ponto de contato)
- [ ] Listar todos os usuários ativos (ver seção 1.5)
- [ ] Enviar aviso D-2
- [ ] Confirmar que documentos críticos foram importados no Notion
- [ ] Enviar aviso D-1
- [ ] Coletar feedback: algum doc ficou faltando?
- [ ] Desligar o Outline no D0


---

## 5. Ordem Recomendada de Execução

```
[1] Inventário
    └─> Contar docs, collections, usuários ativos
        (Claude Code executa as chamadas de API)

[2] Exportação
    └─> Claude Code executa o script de export (~5 min)
    └─> Validar integridade da exportação

[3] Importação
    └─> Importar no Notion por ordem de prioridade (trabalho humano)
    └─> Validar links internos e imagens

[4] Comunicação (D-2)
    └─> Avisar usuários sobre a migração

[5] Período de validação (D-2 até D-1)
    └─> Usuários verificam e completam migração de conteúdo pessoal
    └─> SRE verifica que runbooks críticos estão no Notion

[6] Desligamento (D0) — ~10 min com Claude Code
    └─> ArgoCD: deletar Application do Outline
    └─> Deletar namespace
    └─> Confirmar no Slack
```


---

## 6. Desligamento do Outline

Claude Code executa todo o desligamento técnico em aproximadamente 10 minutos. O engenheiro acompanha e valida cada passo.

### 6.1 Pré-requisitos Obrigatórios

- [ ] Exportação completa validada (ZIP salvo em local seguro)
- [ ] Documentos críticos importados no Notion/Canvas
- [ ] Período de aviso concluído (mínimo D-1 com comunicação feita)
- [ ] Nenhum usuário reportou documento faltando

### 6.2 Identificar a Application ArgoCD do Outline

```bash
# No cluster GKE (certifique-se de estar com o kubeconfig apontando para o GKE)
kubectl config use-context <gke-context>

# Verificar namespace e pods

kubectl get pods -n outline

kubectl get pods -n outline -o wide

# Verificar a Application no ArgoCD

kubectl get application -n argocd | grep outline
```

### 6.3 Deletar via ArgoCD (método preferido)

```bash
# Deletar a Application ArgoCD (isso remove todos os recursos gerenciados)
argocd app delete outline --cascade --yes

# Verificar se foi removida

argocd app list | grep outline
```

### 6.4 Remover o Namespace

```bash
# Verificar recursos restantes no namespace

kubectl get all -n outline

# Deletar namespace (remove tudo dentro)
kubectl delete namespace outline

# Confirmar remoção

kubectl get namespace outline
# Esperado: Error from server (NotFound)
```

### 6.5 Limpeza do DNS e Certificados

```bash
# Verificar IngressRoute do Outline

kubectl get ingressroute -A | grep outline

kubectl get certificate -A | grep outline

# Remover IngressRoute se ainda existir (pode ser gerenciado por ArgoCD ou manual)
kubectl delete ingressroute outline -n outline  # ajuste o nome conforme necessário

# Remover entrada DNS no Cloudflare (via interface ou CLI)
# A entrada DNS para outline.seazone.com.br deve ser removida
```

### 6.6 Limpeza no AWS (S3 e RDS)

O Outline usa S3 para armazenamento de arquivos e PostgreSQL externo (RDS ou Cloud SQL).

```bash
# Identificar o bucket S3 usado pelo Outline
# (verificar a Application ArgoCD ou valores do Helm)
kubectl get secret -n outline -o yaml | grep -i s3

# Após confirmação de que todos os dados foram exportados:
# aws s3 ls s3://<bucket-do-outline>/
# aws s3 rb s3://<bucket-do-outline> --force  # CUIDADO: irreversível

# Para o banco de dados PostgreSQL:
# Tirar snapshot final antes de deletar
# aws rds create-db-snapshot --db-instance-identifier outline-db --db-snapshot-identifier outline-final-snapshot
```

**IMPORTANTE:** Não delete o bucket S3 nem o banco de dados antes de confirmar que a exportação está completa e validada.


---

## 7. Rollback — Restaurar o Outline

Se houver necessidade de restaurar o Outline após o desligamento:

### 7.1 Pré-condições para Rollback

* O backup ZIP da exportação deve estar disponível
* O banco de dados PostgreSQL não deve ter sido deletado (snapshots preservados)
* O bucket S3 não deve ter sido deletado

### 7.2 Procedimento de Rollback

```bash
# 1. Recriar o namespace

kubectl create namespace outline

# 2. Restaurar a Application ArgoCD
# Verificar o arquivo de Application no repositório GitOps (se ainda existir)
git log --all --oneline | grep outline  # verificar se foi commitado

# 3. Se o arquivo foi removido do Git, recriar manualmente:
kubectl apply -f - <<EOF

apiVersion: argoproj.io/v1alpha1

kind: Application

metadata:
  name: outline
  namespace: argocd

spec:
  # ... restaurar configuração original do Outline

EOF

# 4. Aguardar pods subirem

kubectl get pods -n outline -w
```

### 7.3 Janela de Rollback

| Período | Possibilidade de Rollback | Complexidade |
|----|----|----|
| Até 7 dias após desligamento | Total (DB + S3 intactos) | Baixa |
| 8-30 dias | Parcial (depende de snapshots) | Média |
| Após 30 dias | Apenas via exportação | Alta |

**Recomendação:** manter o snapshot do RDS por pelo menos 30 dias após o desligamento antes de deletar definitivamente.


---

*Documento criado em: 2026-03-26* *Responsável pela migração: Time SRE — Seazone*