from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings


EMBEDDING_MODEL = "BAAI/bge-small-en-v1.5"


def create_vector_store(documents):
    """
    Cria um FAISS a partir dos documentos fornecidos.
    """

    if not documents:
        raise ValueError(
            "Nenhum documento foi fornecido para criar o vector store."
        )

    embeddings = HuggingFaceEmbeddings(
        model_name=EMBEDDING_MODEL,
        model_kwargs={
            "device": "cpu",
        },
        encode_kwargs={
            "normalize_embeddings": True,
        },
    )

    vector_store = FAISS.from_documents(
        documents,
        embeddings,
    )

    return vector_store