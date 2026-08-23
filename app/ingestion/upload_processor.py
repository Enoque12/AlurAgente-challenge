from pathlib import Path
from tempfile import TemporaryDirectory

from langchain_core.documents import Document

from app.ingestion.loaders.multi_loader import load_file


def process_uploaded_files(
    uploaded_files,
) -> list[Document]:
    """
    Processa arquivos enviados pelo Streamlit utilizando
    os mesmos loaders da pipeline de ingestão.

    Mantém metadados importantes para identificação da fonte
    e do tipo de documento.
    """

    documents: list[Document] = []

    with TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)

        for uploaded_file in uploaded_files:
            # --------------------------------------------------
            # 1. Criar arquivo temporário
            # --------------------------------------------------
            file_path = temp_path / uploaded_file.name

            file_path.write_bytes(
                uploaded_file.getvalue()
            )

            # --------------------------------------------------
            # 2. Identificar extensão
            # --------------------------------------------------
            file_type = file_path.suffix.lower().lstrip(".")

            # --------------------------------------------------
            # 3. Processar utilizando o loader central
            # --------------------------------------------------
            loaded_documents = load_file(
                file_path
            )

            # --------------------------------------------------
            # 4. Normalizar metadados
            # --------------------------------------------------
            for document in loaded_documents:
                document.metadata["source"] = uploaded_file.name
                document.metadata["file_type"] = file_type

                documents.append(document)

    return documents