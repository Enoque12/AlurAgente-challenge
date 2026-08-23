from app.ingestion.loader import load_documents
from app.ingestion.splitter import split_documents
from app.rag.vector_store import create_vector_store
from app.rag.llm import generate_answer


MAX_DISTANCE = 0.55
MAX_CONTEXT_RESULTS = 3


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
    messages: list | None = None,
):
    """
    Realiza busca semântica, seleciona os documentos mais relevantes
    e gera uma resposta baseada no contexto recuperado.
    """

    # ============================================================
    # 1. BUSCA SEMÂNTICA
    # ============================================================

    results_with_scores = (
        vector_store.similarity_search_with_score(
            question,
            k=5,
        )
    )

    if not results_with_scores:
        return (
            "Não encontrei informações suficientes "
            "nos documentos disponíveis.",
            [],
        )

    # ============================================================
    # 2. DIAGNÓSTICO DA RECUPERAÇÃO
    # ============================================================

    print("\n" + "=" * 70)
    print("DIAGNÓSTICO DA RECUPERAÇÃO")
    print("=" * 70)
    print(f"Pergunta: {question}")

    for index, (document, score) in enumerate(
        results_with_scores,
        start=1,
    ):
        source = document.metadata.get(
            "source",
            "desconhecido",
        )

        print(f"\nResultado {index}: {source}")
        print(f"Score: {score:.4f}")

    # ============================================================
    # 3. FILTRAR RESULTADOS POR RELEVÂNCIA
    # ============================================================

    relevant_results = []

    for document, score in results_with_scores:
        if score <= MAX_DISTANCE:
            relevant_results.append(
                (document, score)
            )

    # ============================================================
    # 4. VERIFICAR SE EXISTEM RESULTADOS RELEVANTES
    # ============================================================

    if not relevant_results:
        return (
            "Não encontrei informações suficientes "
            "nos documentos disponíveis.",
            [],
        )

    # ============================================================
    # 5. REMOVER CHUNKS DUPLICADOS DA MESMA FONTE
    # ============================================================

    unique_results = []
    seen_sources = set()

    for document, score in relevant_results:
        source = document.metadata.get("source")

        if not source:
            continue

        normalized_source = source.replace("\\", "/")

        if normalized_source in seen_sources:
            continue

        seen_sources.add(normalized_source)

        unique_results.append(
            (document, score)
        )

        if len(unique_results) >= MAX_CONTEXT_RESULTS:
            break

    # ============================================================
    # 6. VERIFICAR NOVAMENTE SE EXISTEM FONTES
    # ============================================================

    if not unique_results:
        return (
            "Não encontrei informações suficientes "
            "nos documentos disponíveis.",
            [],
        )

    # ============================================================
    # 7. CONSTRUIR CONTEXTO
    # ============================================================

    context_parts = []
    sources = []

    for document, score in unique_results:

        context_parts.append(
            document.page_content
        )

        source = document.metadata.get("source")

        if source:
            normalized_source = source.replace(
                "\\",
                "/",
            )

            sources.append(
                normalized_source
            )

    context = "\n\n---\n\n".join(
        context_parts
    )

    # ============================================================
    # 8. HISTÓRICO DA CONVERSA
    # ============================================================

    conversation_history = ""

    if messages:
        history_parts = []

        for message in messages[-6:]:
            role = message.get("role")
            content = message.get("content")

            if not content:
                continue

            if role == "user":
                history_parts.append(
                    f"Colaborador: {content}"
                )

            elif role == "assistant":
                history_parts.append(
                    f"Agente: {content}"
                )

        conversation_history = "\n".join(
            history_parts
        )

    # ============================================================
    # 9. GERAR RESPOSTA
    # ============================================================

    answer = generate_answer(
        question=question,
        context=context,
        conversation_history=conversation_history,
    )

    # ============================================================
    # 10. REMOVER FONTES DUPLICADAS
    # ============================================================

    unique_sources = list(
        dict.fromkeys(sources)
    )

    return answer, unique_sources