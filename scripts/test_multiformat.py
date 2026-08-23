from collections import Counter

from app.ingestion.loader import load_documents


def main():

    print("\n=== TESTE DE INGESTÃO MULTI-FORMATO ===\n")

    documents = load_documents()

    print(
        f"Documentos/chunks carregados: {len(documents)}"
    )

    # Contagem por formato
    types = Counter(
        document.metadata.get(
            "file_type",
            "unknown",
        )
        for document in documents
    )

    print("\n=== FORMATOS ENCONTRADOS ===")

    for file_type, count in sorted(types.items()):
        print(
            f"{file_type}: {count}"
        )

    print("\n=== FONTES ENCONTRADAS ===")

    sources = sorted(
        {
            document.metadata.get(
                "source",
                "unknown",
            )
            for document in documents
        }
    )

    for source in sources:
        print(f"✓ {source}")


if __name__ == "__main__":
    main()