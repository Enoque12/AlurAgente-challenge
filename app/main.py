import streamlit as st

from app.ingestion.upload_processor import process_uploaded_files
from app.rag.rag_pipeline import ask_question
from app.rag.vector_store import create_vector_store
from app.ui.uploader import upload_documents


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


def clear_knowledge_base() -> None:
    """Limpa a base de conhecimento e os documentos carregados."""

    st.session_state.vector_store = None
    st.session_state.documents = []
    st.session_state.uploaded_files = []


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
                "arquivo(s) selecionado(s)**"
            )

            if st.button(
                "⚡ Processar documentos",
                use_container_width=True,
            ):

                with st.spinner(
                    "Processando documentos..."
                ):
                    documents = process_uploaded_files(
                        st.session_state.uploaded_files
                    )

                st.session_state.documents = documents

                with st.spinner(
                    "Criando base de conhecimento..."
                ):
                    vector_store = create_vector_store(
                        documents
                    )

                st.session_state.vector_store = vector_store

                st.success(
                    "Base de conhecimento criada com sucesso."
                )

                st.rerun()

        st.divider()

        # Estado da base
        if st.session_state.vector_store is not None:

            st.success(
                "🟢 Base de conhecimento ativa"
            )

            st.metric(
                "Chunks",
                len(st.session_state.documents),
            )

        else:

            st.info(
                "Nenhuma base de conhecimento ativa."
            )

        st.divider()

        # Limpar base
        if st.session_state.vector_store is not None:

            if st.button(
                "🗑️ Limpar base",
                use_container_width=True,
            ):

                clear_knowledge_base()

                st.rerun()

        # Limpar conversa
        if st.session_state.messages:

            if st.button(
                "🧹 Limpar conversa",
                use_container_width=True,
            ):

                st.session_state.messages = []

                st.rerun()


def render_chat_history() -> None:
    """Renderiza o histórico da conversa."""

    for message in st.session_state.messages:

        role = message["role"]

        with st.chat_message(role):

            st.markdown(
                message["content"]
            )

            # Mostrar fontes somente para respostas
            # do agente.
            if (
                role == "assistant"
                and message.get("sources")
            ):

                with st.expander(
                    "📚 Fontes consultadas"
                ):

                    for source in message["sources"]:

                        filename = (
                            source
                            .replace("\\", "/")
                            .split("/")[-1]
                        )

                        st.caption(
                            f"📄 {filename}"
                        )


def render_question_form() -> None:
    """Renderiza o formulário de perguntas."""

    if st.session_state.vector_store is None:

        st.info(
            "👈 Carregue e processe documentos "
            "para começar a conversar com o agente."
        )

        return

    st.divider()

    with st.form(
        "question_form",
        clear_on_submit=True,
    ):

        question = st.text_area(
            "Digite sua pergunta",
            placeholder=(
                "Ex.: Com quanto tempo de antecedência "
                "devo solicitar férias?"
            ),
            height=100,
            label_visibility="collapsed",
        )

        submitted = st.form_submit_button(
            "📤 Enviar pergunta",
            use_container_width=True,
        )

    if not submitted:
        return

    question = question.strip()

    if not question:
        st.warning(
            "Digite uma pergunta antes de enviar."
        )

        return

    # Guardar pergunta imediatamente.
    st.session_state.messages.append(
        {
            "role": "user",
            "content": question,
        }
    )

    # Mostrar pergunta antes de processar.
    with st.chat_message("user"):

        st.markdown(question)

    # Consultar RAG.
    with st.chat_message("assistant"):

        with st.spinner(
            "🔎 Consultando documentos..."
        ):

            answer, sources = ask_question(
                st.session_state.vector_store,
                question,
            )

        st.markdown(answer)

        if sources:

            with st.expander(
                "📚 Fontes consultadas"
            ):

                for source in sources:

                    filename = (
                        source
                        .replace("\\", "/")
                        .split("/")[-1]
                    )

                    st.caption(
                        f"📄 {filename}"
                    )

    # Guardar resposta.
    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": answer,
            "sources": sources,
        }
    )


def main() -> None:

    st.set_page_config(
        page_title="NexusTech AI Agent",
        page_icon="🤖",
        layout="wide",
    )

    initialize_session_state()

    render_sidebar()

    # ============================================================
    # HEADER
    # ============================================================

    st.title("🤖 NexusTech AI Agent")

    st.markdown(
        """
        Assistente corporativo inteligente capaz de responder
        perguntas com base nos documentos de conhecimento da empresa.
        """
    )

    # ============================================================
    # HISTÓRICO
    # ============================================================

    render_chat_history()

    # ============================================================
    # FORMULÁRIO
    # ============================================================

    render_question_form()


if __name__ == "__main__":
    main()