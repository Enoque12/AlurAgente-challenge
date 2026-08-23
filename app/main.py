import streamlit as st

from app.ui.uploader import upload_documents
from app.ingestion.upload_processor import process_uploaded_files


def main() -> None:

    st.set_page_config(
        page_title="NexusTech AI Agent",
        page_icon="🤖",
        layout="wide",
    )

    st.title("🤖 NexusTech AI Agent")

    st.markdown(
        """
        Assistente corporativo inteligente capaz de responder
        perguntas com base nos documentos de conhecimento da empresa.
        """
    )

    st.divider()

    st.subheader("📚 Documentos de conhecimento")

    uploaded_files = upload_documents()

    if uploaded_files:

        st.success(
            f"{len(uploaded_files)} documento(s) "
            "carregado(s) com sucesso."
        )

        # Processar documentos
        with st.spinner(
            "Processando documentos..."
        ):

            documents = process_uploaded_files(
                uploaded_files
            )

        st.success(
            f"{len(documents)} documento(s)/chunk(s) "
            "extraído(s) com sucesso."
        )

        st.markdown("### Arquivos selecionados")

        for file in uploaded_files:

            st.write(
                f"📄 **{file.name}** "
                f"({file.size / 1024:.1f} KB)"
            )

    else:

        st.info(
            "Adicione um ou mais documentos para começar."
        )


if __name__ == "__main__":
    main()