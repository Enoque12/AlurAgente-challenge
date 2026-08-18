from app.ingestion.loader import load_documents
from app.ingestion.splitter import split_documents
from app.rag.vector_store import create_vector_store
from app.rag.llm import generate_answer


def create_rag_pipeline():
    """
    Cria o pipeline RAG completo.
    """

    documents = load_documents()

    chunks = split_documents(documents)

    vector_store = create_vector_store(chunks)

    return vector_store


def ask_question(
    vector_store,
    question: str,
    k: int = 3,
):
    """
    Recupera os chunks mais relevantes e
    gera uma resposta baseada neles.
    """

    results = vector_store.similarity_search(
        question,
        k=k,
    )

    context = "\n\n".join(
        document.page_content
        for document in results
    )

    answer = generate_answer(
        question,
        context,
    )

    sources = [
        document.metadata.get("source")
        for document in results
    ]

    return answer, sources