from app.ingestion.loader import load_documents
from app.ingestion.splitter import split_documents
from app.rag.vector_store import create_vector_store
from app.rag.llm import generate_answer


# Diferença máxima permitida em relação
# ao melhor resultado recuperado.
SCORE_MARGIN = 0.10

# Número máximo de documentos recuperados
# inicialmente pelo retriever.
RETRIEVAL_K = 5


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
):
    """
    Realiza busca semântica, filtra os resultados
    pouco relevantes e gera uma resposta baseada
    nos documentos selecionados.
    """

    results = vector_store.similarity_search_with_score(
        question,
        k=RETRIEVAL_K,
    )

    if not results:
        return (
            "Não encontrei informações suficientes "
            "nos documentos disponíveis.",
            [],
        )

    # O primeiro resultado possui o menor score
    # e é considerado o mais relevante.
    best_score = results[0][1]

    max_score = best_score + SCORE_MARGIN

    relevant_results = [
        (document, score)
        for document, score in results
        if score <= max_score
    ]

    # Garantir que pelo menos o melhor resultado
    # seja utilizado.
    if not relevant_results:
        relevant_results = [results[0]]

    context_parts = []
    sources = []

    for document, score in relevant_results:

        context_parts.append(
            document.page_content
        )

        source = document.metadata.get(
            "source"
        )

        if source and source not in sources:
            sources.append(source)

    context = "\n\n---\n\n".join(
        context_parts
    )

    answer = generate_answer(
        question,
        context,
    )

    return answer, sources