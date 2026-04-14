# Seazone Atlas

## O que é

O Seazone Atlas é um assistente interno de conhecimento que responde perguntas sobre processos da Seazone consultando automaticamente múltiplas fontes de dados. Ele utiliza RAG (Retrieval-Augmented Generation) para buscar trechos relevantes na base de documentos e gerar respostas fundamentadas, com fonte citada e link para o documento original.

**Link de acesso:** https://seazone-atlas-lxobpggftxuq7tu2cryhjh.streamlit.app/

---

## Fontes de Dados

O Atlas consulta 3 tipos de fonte, totalizando **2.093 documentos**:

| Fonte | Quantidade | Conteúdo |
| --- | --- | --- |
| Outline | 2.081 docs | Documentação formal de todas as áreas |
| Slack Canvases | 10 docs | Processos curados de canais de suporte (Operação, Financeiro, People) |
| Slack FAQ | 2 docs | Perguntas e respostas extraídas de conversas reais dos canais #suporte-financeiro e #suporte-people |

---

## Áreas Cobertas

- **Tecnologia** — Hub de IA, LiteLLM, Claude Code, plataformas, automações, dados
- **Administrativo Financeiro** — Fechamento, conciliação, repasses, NFs, pagamentos, franquias
- **Operação** — Suporte unificado (4 subáreas: Implantação, Franquias, Hóspede, Proprietários), SLAs
- **People** — Plano de saúde, benefícios (Gympass), ausências, day off, políticas internas

---

## Como Usar

### 1. Selecionar áreas

No menu lateral, selecione uma ou mais áreas onde deseja buscar. Selecionar uma área específica traz resultados mais precisos. Selecionar várias áreas faz uma busca mais ampla — útil quando não se sabe onde a informação está.

### 2. Ajustar a régua de trechos

A régua "Trechos consultados" define quantos trechos da base o sistema analisa antes de responder:
- **Valor baixo (3-5):** resposta mais rápida e focada, pode perder informações
- **Valor padrão (8):** equilíbrio entre precisão e velocidade
- **Valor alto (10-15):** busca mais abrangente, porém mais lenta

### 3. Fazer a pergunta

Digite sua pergunta no campo de chat. Exemplos:
- "Qual o prazo pra enviar a nota fiscal?"
- "Como funciona o processo de conciliação?"
- "Como solicito o day off?"
- "Como abro um suporte de operação?"

### 4. Consultar as fontes

Cada resposta tem um bloco expansível "Fontes consultadas" com os documentos usados:
- **[Outline]** — link clicável que abre o doc no Outline
- **[Slack]** — link clicável que abre o canvas no Slack (requer login)
- **[Slack FAQ]** — baseado em conversas reais, com link para a conversa original

### 5. Refazer busca

Se o sistema sugerir trocar a área, altere o filtro no menu lateral e clique no botão "Refazer busca" — ele repete a última pergunta na nova área sem precisar digitar novamente.

---

## Comportamentos Inteligentes

**Fallback honesto:** Quando não encontra a resposta na área filtrada, o Atlas não inventa. Ele:
1. Identifica se o assunto pertence a outra área e sugere trocar o filtro
2. Só depois sugere o canal de Slack mais adequado ao tema

**Mapa de canais:** O sistema tem mais de 50 canais de suporte da Seazone mapeados e direciona para o canal correto conforme o tema da pergunta.

**Aviso em FAQs:** Respostas baseadas em conversas do Slack incluem aviso de que podem conter simplificações e link para a conversa original, permitindo verificar o contexto completo.

---

## Stack Técnica

| Componente | Tecnologia |
| --- | --- |
| Embeddings | paraphrase-multilingual-MiniLM-L12-v2 (suporte a português) |
| Vector Store | ChromaDB (local, persistente) |
| LLM | Claude Sonnet via Hub Seazone (LiteLLM) |
| Interface | Streamlit (dark theme, branding Seazone) |
| Deploy | Streamlit Community Cloud |
| Ingestão | Scripts Python para Outline API e Slack MCP |

---

## Roadmap — Oportunidades de Melhoria

### Novas Fontes de Dados

- **Notion:** A integração está preparada (MCP conectado), mas aguarda permissão do admin do workspace `comercialseazone` para acessar os documentos. Com essa permissão, os docs do Notion seriam ingeridos automaticamente.
- **Google Drive:** Script de exportação já existe (`export_gdrive.py`). Falta apenas configurar OAuth para pastas específicas com procedimentos.
- **Mensagens fixadas (pinned) do Slack:** Mensagens fixadas em canais de suporte costumam ser respostas definitivas para dúvidas recorrentes. Alta qualidade, baixo ruído.
- **Organograma da empresa:** Ingerir o organograma da Seazone para que o Atlas saiba quem é responsável por cada área, time e processo. Isso permitiria respostas como "quem é o responsável pelo time de Fechamento?" ou "a quem devo escalar um problema de repasse?" — conectando processos a pessoas.

### Apuração de FAQ dos Canais de Suporte

Atualmente os FAQs foram extraídos manualmente de conversas dos canais #suporte-financeiro e #suporte-people. O próximo passo é:
- **Automatizar a extração:** Criar pipeline que periodicamente varre os canais de suporte, identifica threads com perguntas respondidas, e extrai os pares P&R automaticamente
- **Curadoria por IA:** Usar LLM para filtrar ruído (mensagens curtas, "obrigado", tickets específicos) e consolidar apenas conhecimento reutilizável
- **Quebra individual:** Separar cada P&R em arquivo individual para melhorar o retrieval (hoje um FAQ com múltiplas perguntas dilui o sinal semântico)

### Melhorias Técnicas

- **Reranker:** Adicionar um modelo de reranking (Cohere ou Voyage) após o retrieval para melhorar a precisão do top-k
- **Ingestão incremental:** Hoje o ingest recria o índice do zero. Implementar upsert para adicionar docs novos sem reprocessar tudo
- **Atualização automática:** Cron diário que puxa novos docs do Outline e novos canvases do Slack automaticamente
- **Notion como fonte nativa:** Assim que a permissão for concedida, adicionar como 4ª fonte com prefixo [Notion] nas citações

### Melhorias de UX

- **Histórico persistente:** Salvar conversas anteriores para o usuário poder revisitar
- **Feedback do usuário:** Botões de "útil / não útil" em cada resposta para melhorar o sistema ao longo do tempo
- **Sugestões de perguntas:** Mostrar perguntas frequentes por área ao abrir o app

---

## Construído por

Débora Franzoni — Time de Fechamento — Hackathon AI First Seazone 2026
