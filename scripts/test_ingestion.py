from app.ingestion.loader import load_documents
from app.ingestion.splitter import split_documents

def main():
    print("\n=== Carregando Documentos ===\n")
    
    documents = load_documents()
    
    print(f"\nDocumentos carregados: {len(documents)}")
    
    for document in documents:
        print("\nArquivo:")
        print(document.metadata.get("source"))
    
    print("\n=== Dividindo Documentos ===\n")
    
    chunks = split_documents(documents)
    
    print(f"Total de chunks: {len(chunks)}")
    
    for index, chunk in enumerate(chunks[:5]):
        print("\n" + "=" * 60)
        print(f"CHUNK {index + 1}")
        print("=" * 60)
        
        print(chunk.page_content)
        
        print("\nMetadata:")
        print(chunk.metadata)
        
if __name__ == "__main__":
    main()