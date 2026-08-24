import sys
from pathlib import Path

import streamlit as st


# Garante que a raiz do projecto está disponível no Python path.
PROJECT_ROOT = Path(__file__).resolve().parent.parent

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from app.ingestion.upload_processor import process_uploaded_files
from app.rag.rag_pipeline import ask_question
from app.rag.vector_store import create_vector_store
from app.ui.uploader import upload_documents


# ============================================================
# CONFIGURAÇÃO
# ============================================================

PAGE_TITLE = "NexusTech AI Agent"
PAGE_ICON = "🤖"


# ============================================================
# SESSION STATE
# ============================================================

def initialize_session_state() -> None:
    """Inicializa o estado persistente da aplicação."""

    if "vector_store" not in st.session_state:
        st.session_state.vector_store = None

    if "documents" not in st.session_state:
        st.session_state.documents = []

    if "uploaded_files" not in st.session_state:
        st.session_state.uploaded_files = []

    if "messages" not in st.session_state:
        st.session_state.messages = []


# ============================================================
# UTILITÁRIOS
# ============================================================

def get_filename(source: str | None) -> str | None:
    """Obtém apenas o nome do arquivo a partir da fonte."""

    if not source:
        return None

    return Path(
        str(source).replace("\\", "/")
    ).name


def get_unique_sources(
    sources: list[str] | None,
) -> list[str]:
    """Remove fontes duplicadas."""

    if not sources:
        return []

    unique_sources: list[str] = []

    for source in sources:
        filename = get_filename(source)

        if filename and filename not in unique_sources:
            unique_sources.append(filename)

    return unique_sources


# ============================================================
# BASE DE CONHECIMENTO
# ============================================================

def clear_knowledge_base() -> None:
    """Limpa a base de conhecimento."""

    st.session_state.vector_store = None
    st.session_state.documents = []
    st.session_state.uploaded_files = []


def process_documents() -> None:
    """Processa os documentos e cria a base vetorial."""

    if not st.session_state.uploaded_files:
        st.warning(
            "Selecione pelo menos um documento antes de processar."
        )
        return

    try:

        with st.spinner("📄 Processando documentos..."):
            documents = process_uploaded_files(
                st.session_state.uploaded_files
            )

        if not documents:
            st.error(
                "Não foi possível extrair conteúdo "
                "dos documentos selecionados."
            )
            return

        st.session_state.documents = documents

        with st.spinner(
            "🧠 Criando base de conhecimento..."
        ):
            vector_store = create_vector_store(
                documents
            )

        st.session_state.vector_store = vector_store

        st.success(
            "✅ Base de conhecimento criada com sucesso."
        )

    except Exception:
        st.error(
            "❌ Não foi possível processar os documentos."
        )


# ============================================================
# SIDEBAR
# ============================================================

def render_sidebar() -> None:
    """Renderiza a barra lateral."""

    with st.sidebar:

        st.title("🤖 NexusTech AI")

        st.caption(
            "Assistente corporativo baseado "
            "em documentos internos."
        )

        st.divider()

        st.subheader("📚 Base de conhecimento")

        uploaded_files = upload_documents()

        if uploaded_files:
            st.session_state.uploaded_files = uploaded_files

        if st.session_state.uploaded_files:

            st.write(
                f"**{len(st.session_state.uploaded_files)} "
                f"arquivo(s) selecionado(s)**"
            )

            with st.expander(
                "📂 Ver arquivos",
                expanded=False,
            ):

                for file in st.session_state.uploaded_files:

                    size_kb = file.size / 1024

                    st.caption(
                        f"📄 {file.name} "
                        f"({size_kb:.1f} KB)"
                    )

            if st.button(
                "⚡ Processar documentos",
                use_container_width=True,
                type="primary",
            ):

                process_documents()

                st.rerun()

        st.divider()

        st.subheader("📊 Estado da base")

        if st.session_state.vector_store is not None:

            st.success(
                "🟢 Base de conhecimento ativa"
            )

            st.metric(
                "Chunks indexados",
                len(st.session_state.documents),
            )

        else:

            st.info(
                "⚪ Nenhuma base de conhecimento ativa."
            )

        st.divider()

        if st.session_state.vector_store is not None:

            if st.button(
                "🗑️ Limpar base",
                use_container_width=True,
            ):

                clear_knowledge_base()

                st.rerun()

        if st.session_state.messages:

            if st.button(
                "🧹 Limpar conversa",
                use_container_width=True,
            ):

                st.session_state.messages = []

                st.rerun()


# ============================================================
# CHAT HEADER
# ============================================================

def render_chat_header() -> None:
    """Renderiza o cabeçalho da área de chat."""

    st.title("💬 Conversa")

    st.caption(
        "Faça perguntas sobre os documentos "
        "da base de conhecimento."
    )

    st.divider()


# ============================================================
# CHAT HISTORY
# ============================================================

def render_chat_history() -> None:
    """Renderiza o histórico da conversa."""

    if not st.session_state.messages:

        st.markdown(
            """
            <div style="
                text-align: center;
                padding: 80px 20px;
                opacity: 0.7;
            ">
                <div style="font-size: 52px;">🤖</div>

                Como posso ajudar?
                
                Faça uma pergunta sobre os documentos
                disponíveis na base de conhecimento.
            </div>
            """,
            unsafe_allow_html=True,
        )

        return

    for message in st.session_state.messages:

        role = message.get("role")

        content = message.get(
            "content",
            "",
        )

        if role not in (
            "user",
            "assistant",
        ):
            continue

        with st.chat_message(role):

            st.markdown(content)

            if (
                role == "assistant"
                and message.get("sources")
            ):

                sources = get_unique_sources(
                    message["sources"]
                )

                if sources:

                    with st.expander(
                        "📚 Fontes consultadas"
                    ):

                        for source in sources:

                            st.caption(
                                f"📄 {source}"
                            )


# ============================================================
# QUESTION INPUT
# ============================================================

def render_question_input() -> None:
    """Renderiza a barra de pergunta no rodapé."""

    if st.session_state.vector_store is None:

        st.info(
            "👈 Carregue e processe documentos "
            "para começar a conversar."
        )

        return

    st.markdown(
        """
        <div style="
            height: 12px;
        "></div>
        """,
        unsafe_allow_html=True,
    )

    # --------------------------------------------------------
    # Formulário
    # --------------------------------------------------------

    with st.form(
        "question_form",
        clear_on_submit=True,
        border=False,
    ):

        col_input, col_button = st.columns(
            [8, 1],
            vertical_alignment="bottom",
        )

        with col_input:

            question = st.text_input(
                "Pergunta",
                placeholder=(
                    "Digite a sua pergunta..."
                ),
                label_visibility="collapsed",
            )

        with col_button:

            submitted = st.form_submit_button(
                "➤",
                use_container_width=True,
                type="primary",
            )

    if not submitted:
        return

    question = question.strip()

    if not question:

        st.warning(
            "Digite uma pergunta antes de enviar."
        )

        return

    process_question(question)


# ============================================================
# PROCESSAR PERGUNTA
# ============================================================

def process_question(
    question: str,
) -> None:
    """Processa uma pergunta utilizando o RAG."""

    # --------------------------------------------------------
    # Guardar histórico anterior
    # --------------------------------------------------------

    conversation_history = (
        st.session_state.messages.copy()
    )

    # --------------------------------------------------------
    # Guardar pergunta
    # --------------------------------------------------------

    st.session_state.messages.append(
        {
            "role": "user",
            "content": question,
        }
    )

    # --------------------------------------------------------
    # Consultar RAG
    # --------------------------------------------------------

    try:

        with st.spinner(
            "🔎 Consultando a base de conhecimento..."
        ):

            answer, sources = ask_question(
                st.session_state.vector_store,
                question,
                conversation_history,
            )

        unique_sources = get_unique_sources(
            sources
        )

        # ----------------------------------------------------
        # Guardar resposta
        # ----------------------------------------------------

        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": answer,
                "sources": unique_sources,
            }
        )

        st.rerun()

    except Exception as error:

        error_text = str(error)

        # ----------------------------------------------------
        # Quota Gemini
        # ----------------------------------------------------

        if (
            "429" in error_text
            or "RESOURCE_EXHAUSTED" in error_text
            or "quota" in error_text.lower()
        ):

            answer = (
                "⚠️ O serviço de IA atingiu temporariamente "
                "o limite de utilização disponível. "
                "A recuperação dos documentos está funcional, "
                "mas a geração da resposta está temporariamente "
                "indisponível. Tente novamente mais tarde."
            )

        else:

            answer = (
                "⚠️ Não foi possível gerar uma resposta "
                "neste momento. Verifique a configuração "
                "do serviço de IA e tente novamente."
            )

        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": answer,
                "sources": [],
            }
        )

        st.rerun()


# ============================================================
# MAIN
# ============================================================

def main() -> None:
    """Ponto de entrada da aplicação."""

    st.set_page_config(
        page_title=PAGE_TITLE,
        page_icon=PAGE_ICON,
        layout="wide",
    )

    initialize_session_state()

    # --------------------------------------------------------
    # Sidebar
    # --------------------------------------------------------

    render_sidebar()

    # --------------------------------------------------------
    # Área principal
    # --------------------------------------------------------

    render_chat_header()

    render_chat_history()

    # --------------------------------------------------------
    # Input
    # --------------------------------------------------------

    render_question_input()


# ============================================================
# ENTRY POINT
# ============================================================

if __name__ == "__main__":
    main()