from pathlib import Path

from langchain_community.document_loaders import (
    DirectoryLoader,
    TextLoader,
)

DOCUMENTS_PATH = Path("documents/sample")

def load_documents():
    """
    Carrega os documentos Markdown disponiveis na pasta de documentos.
    """
    
    loader = DirectoryLoader(
        str(DOCUMENTS_PATH),
        glob="**/*.md",
        loader_cls=TextLoader,
        loader_kwargs={
            "encoding": "utf-8",
        },
        show_progress=True,
    )
    
    documents = loader.load()
    
    return documents