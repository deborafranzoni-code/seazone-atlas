"""
Streamlit chat UI for the Seazone RAG knowledge base.

Run:  streamlit run app.py
"""

from __future__ import annotations

import os
from pathlib import Path

import streamlit as st
from anthropic import Anthropic
from dotenv import load_dotenv

from retrieval import retrieve

load_dotenv()

# Auto-ingest if the collection isn't usable yet (missing dir, empty dir, or
# collection never created because a previous ingest crashed partway).
import chromadb
from chromadb.errors import NotFoundError

_db_path = Path(__file__).parent / "chroma_db"
_needs_ingest = not _db_path.exists() or not any(_db_path.iterdir())
if not _needs_ingest:
    try:
        chromadb.PersistentClient(path=str(_db_path)).get_collection("seazone_kb")
    except (NotFoundError, ValueError):
        _needs_ingest = True
if _needs_ingest:
    with st.spinner("Primeira execucao: indexando documentos... isso pode levar alguns minutos."):
        import ingest
        ingest.main()

MODEL = os.getenv("LLM_MODEL", "claude-sonnet-4-6")

SYSTEM_PROMPT = """Você é o assistente interno da Seazone. Responde perguntas sobre
processos internos consultando a base de conhecimento (Outline).

Regras rígidas:
1. Responda APENAS com base nos trechos fornecidos abaixo.
2. Se a resposta não estiver clara nos trechos, NÃO invente. Siga OBRIGATORIAMENTE esta ordem:
   a) PRIMEIRO: identifique qual área o assunto pertence usando este mapa:
      - Nota fiscal, pagamento, fechamento, conciliação, repasse → Administrativo Financeiro
      - IA, hub, claude, plataforma, dados, automação → Tecnologia
      - Plano de saúde, benefícios, ausências, day off, gympass → People
      - Suporte, vistoria, implantação, franquias, hóspede → Operacao
      Se a área do assunto for DIFERENTE da área filtrada pelo usuário, diga:
      "Esse assunto pertence à área [ÁREA]. Selecione essa área no filtro lateral e refaça a busca."
   b) DEPOIS: se mesmo na área correta não encontrar, direcione pro canal de Slack (tabela abaixo).
3. NÃO cite fontes, links ou referências no corpo da resposta. As fontes são exibidas automaticamente pela interface. Apenas responda a pergunta.
4. Seja direto. Sem "Com base nos trechos...", sem "Fonte:", sem "Referência:". Apenas a resposta.
5. Se houver conflito entre trechos, aponte explicitamente.
6. Use EXCLUSIVAMENTE português brasileiro. Nunca misture espanhol, inglês ou outros idiomas.
7. Use apenas caracteres do alfabeto latino. Nunca inclua caracteres CJK, cirílicos ou de outros scripts.

Mapa de canais de Slack (use pra direcionar quando não encontrar na base):

Tecnologia / IA / Dados:
- IA, LLM, agentes → #suporte-ia
- Hub, LiteLLM, Claude Code, infra de IA → #suporte-plataforma
- Automações, planilhas, formulários, n8n → #suporte-bizops
- Entrega de dados, BigQuery, lake → #suporte-dados
- Web, site externo → #suporte-tech-web

Administrativo Financeiro:
- Fechamento, conciliação, financeiro geral → #suporte-financeiro
- Contabilização, NF, impostos → #suportes-contabilizacao
- Obra/financeiro de obras → #suporte-obra-financeiro

Outras áreas (se a pergunta fugir das duas acima):
- Operação, hospedagem, reservas → #suporte-operacao, #suporte-bu-hospedagem, #suporte-bu-reservas
- Atendimento, CS proprietários → #suporte-atendimento, #suporte-cs-proprietarios
- Gestão de contas → #suporte-gestao-de-contas
- Comercial, franquias → #suporte-comercial, #suporte-franquias
- RH / People → #suporte-people
- Jurídico → #suporte-juridico

Se não tiver certeza qual canal sugerir, use o mais genérico da área mais próxima.
"""

st.set_page_config(page_title="Seazone Atlas", page_icon="favicon.png", layout="centered")

# Lupa piscando no canto ao processar
st.markdown("""<style>
[data-testid="stStatusWidget"] { visibility: hidden; position: relative; }
[data-testid="stStatusWidget"]::after {
    content: "\\1F50D"; visibility: visible; position: absolute;
    top: 0; right: 0; font-size: 1.4rem;
    animation: blink 1s ease-in-out infinite;
}
@keyframes blink { 0%, 100% { opacity: 1; } 50% { opacity: 0.2; } }
.block-container { padding-top: 2.5rem !important; }
</style>""", unsafe_allow_html=True)

# Header
col_logo, col_title = st.columns([0.7, 5])
with col_logo:
    st.image("seazone_icon_bright.png", width=65)
with col_title:
    st.markdown("<h1 style='margin:0; padding-top:0.3rem;'>Seazone Atlas</h1>", unsafe_allow_html=True)
st.caption("Pergunte sobre processos internos. Respostas com fonte citada.")

AREAS = ["Tecnologia", "Administrativo Financeiro", "Operacao", "People"]

with st.sidebar:
    st.markdown("<p style='font-size:1.1rem; font-weight:600; margin-bottom:0.3rem;'>Consultar areas:</p>", unsafe_allow_html=True)
    areas_selecionadas = st.multiselect("Consultar areas:", AREAS, default=[], placeholder="Selecione as areas...", label_visibility="collapsed")
    if not areas_selecionadas:
        st.warning("Selecione pelo menos uma area para buscar.")
    top_k = st.slider("Trechos consultados", 3, 15, 8)
    if top_k > 10:
        st.warning("Busca mais abrangente, porem mais lenta.")
    elif top_k < 5:
        st.info("Resposta mais rapida, porem pode perder informacoes.")
    st.markdown("---")
    if st.button("Limpar conversa", type="primary", use_container_width=True):
        st.session_state.messages = []
        st.session_state.pop("pending_retry", None)
        st.rerun()

# Build area filter for retrieval
if not areas_selecionadas or len(areas_selecionadas) == len(AREAS):
    area = "Todas"
elif len(areas_selecionadas) == 1:
    area = areas_selecionadas[0]
else:
    area = areas_selecionadas  # list of areas

if "messages" not in st.session_state:
    st.session_state.messages = []

if "client" not in st.session_state:
    st.session_state.client = Anthropic(
        timeout=30.0,
        max_retries=1,
    )


def _format_source(s: dict) -> str:
    """Format a source for display. Outline links are clickable, Slack shows label only."""
    src = s.get("source", "Outro")
    title = s["title"]
    area = s["area"]
    # Remove [Slack]/[Outline] prefix from title if already there (avoid duplication)
    for prefix in ("[Slack] ", "[Outline] ", "[Local] "):
        title = title.removeprefix(prefix)
    if src == "Outline":
        return f"- `[Outline]` [{title}]({s['url']}) — _{area}_"
    elif src == "Slack":
        return f"- `[Slack]` [{title}]({s['url']}) — _{area}_"
    else:
        return f"- `[{src}]` {title} — _{area}_"


# Render history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        if msg.get("sources"):
            with st.expander(f"Fontes consultadas ({len(msg['sources'])})"):
                for s in msg["sources"]:
                    st.markdown(_format_source(s))


def stream_answer(question: str, context: str, filtered_areas: list[str] | None = None):
    """Yield text chunks from Claude with prompt caching on system prompt."""
    area_info = ""
    if filtered_areas:
        area_info = f"\n\nO usuário filtrou a busca por: {', '.join(filtered_areas)}. Os trechos abaixo são APENAS dessa(s) área(s). IMPORTANTE: só sugira trocar o filtro se o assunto claramente NÃO pertence a nenhuma das áreas filtradas. Se o assunto pertence à área já filtrada mas você não encontrou a resposta nos trechos, NÃO diga 'esse assunto pertence à área X' — vá direto para a sugestão de canal do Slack."
    with st.session_state.client.messages.stream(
        model=MODEL,
        max_tokens=16000,
        system=[
            {"type": "text", "text": SYSTEM_PROMPT, "cache_control": {"type": "ephemeral"}}
        ],
        messages=[
            {
                "role": "user",
                "content": (
                    f"Trechos da base de conhecimento:\n\n{context}\n\n"
                    f"---{area_info}\n\nPergunta: {question}"
                ),
            }
        ],
    ) as stream:
        for text in stream.text_stream:
            yield text


# Show retry button if there's a previous user question and area may have changed
_last_user_msg = None
for m in reversed(st.session_state.messages):
    if m["role"] == "user":
        _last_user_msg = m["content"]
        break

_area_label = ", ".join(areas_selecionadas) if areas_selecionadas else "Todas"
if _last_user_msg and st.button(f"Refazer busca em: {_area_label}", type="primary"):
    st.session_state.pending_retry = _last_user_msg

# Determine which prompt to process (new input or retry)
_new_prompt = st.chat_input("Como funciona o processo de vistoria?")
_prompt_to_run = st.session_state.pop("pending_retry", None) or _new_prompt

if _prompt_to_run:
    if not areas_selecionadas:
        st.error("Selecione pelo menos uma area no menu lateral antes de buscar.")
        st.stop()
    # Only add to history if it's a new question (not a retry)
    if _new_prompt:
        st.session_state.messages.append({"role": "user", "content": _prompt_to_run})
    with st.chat_message("user"):
        st.markdown(_prompt_to_run)

    with st.chat_message("assistant"):
        with st.spinner("Buscando nos documentos..."):
            context, sources = retrieve(_prompt_to_run, area=area, top_k=top_k)

        placeholder = st.empty()
        placeholder.markdown("Analisando trechos encontrados... aguarde")
        full = ""
        started = False
        try:
            for chunk in stream_answer(_prompt_to_run, context, areas_selecionadas):
                full += chunk
                if full.strip():
                    started = True
                if started:
                    placeholder.markdown(full + " ▌")
            placeholder.markdown(full)
        except Exception as e:
            err_name = type(e).__name__
            if "Timeout" in err_name or "timeout" in str(e).lower():
                placeholder.markdown("O servidor de IA esta temporariamente indisponivel. Tente novamente em alguns segundos.")
            else:
                placeholder.markdown(f"Ocorreu um erro ao processar sua pergunta. Tente novamente.")
            full = ""
            sources = []

        if sources:
            with st.expander(f"Fontes consultadas ({len(sources)})"):
                for s in sources:
                    st.markdown(_format_source(s))

    st.session_state.messages.append(
        {"role": "assistant", "content": full, "sources": sources}
    )
