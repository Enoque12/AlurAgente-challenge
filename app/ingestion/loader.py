from pathlib import Path

from langchain_core.documents import Document

from app.ingestion.loaders.multi_loader import load_file


DOCUMENTS_DIR = Path("documents")


def load_documents() -> list[Document]:
    """
    Carrega todos os documentos suportados
    encontrados no diretório documents/.
    """

    documents: list[Document] = []

    for file_path in DOCUMENTS_DIR.rglob("*"):

        if not file_path.is_file():
            continue

        try:

            loaded = load_file(file_path)

            documents.extend(loaded)

        except ValueError:
            # Ignora formatos não suportados.
            continue

    return documents