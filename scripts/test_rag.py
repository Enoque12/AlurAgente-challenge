from app.rag.rag_pipeline import (
    create_rag_pipeline,
    ask_question,
)

def main():

    print("\n=== CRIANDO RAG ===\n")

    vector_store = create_rag_pipeline()

    print("RAG criado com sucesso!")

    questions = [
        "Com quanto tempo de antecedência devo solicitar férias?",
        "Qual é o limite diário para alimentação durante viagens nacionais?",
        "A empresa oferece seguro de saúde?",
        "Qual é o valor do subsídio de transporte?",
    ]

    for question in questions:

        print("\n" + "=" * 70)
        print("PERGUNTA")
        print("=" * 70)

        print(question)

        answer, sources = ask_question(
            vector_store,
            question,
        )

        print("\nRESPOSTA")
        print("-" * 70)

        print(answer)

        print("\nFONTES")
        print("-" * 70)

        for source in sources:
            print(source)

if __name__ == "__main__":
    main()