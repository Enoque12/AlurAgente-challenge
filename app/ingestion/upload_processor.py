from pathlib import Path
from tempfile import TemporaryDirectory

from langchain_core.documents import Document

from app.ingestion.loaders.multi_loader import load_file


def process_uploaded_files(
    uploaded_files,
) -> list[Document]:
    """
    Processa arquivos enviados pelo Streamlit
    utilizando os mesmos loaders da pipeline.
    """

    documents: list[Document] = []

    with TemporaryDirectory() as temp_dir:

        temp_path = Path(temp_dir)

        for uploaded_file in uploaded_files:

            file_path = temp_path / uploaded_file.name

            file_path.write_bytes(
                uploaded_file.getvalue()
            )

            loaded_documents = load_file(
                file_path
            )

            # Manter o nome original do arquivo
            # como fonte para exibição posterior.
            for document in loaded_documents:

                document.metadata[
                    "source"
                ] = uploaded_file.name

                documents.append(document)

    return documents