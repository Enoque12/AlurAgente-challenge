from app.ingestion.loader import load_documents
from app.ingestion.splitter import split_documents
from app.rag.vector_store import create_vector_store

def main():
    print("\n=== 1. Carregando Documentos ===\n")
    
    documents = load_documents()
    
    print(f"Documentos carregados: {len(documents)}")
    
    print("\n=== 2. Criando Chunks ===\n")
    
    chunks = split_documents(documents)
    
    print(f"Chunks criados: {len(chunks)}")
    
    print("\n=== 3. Criando vector store ===\n")
    
    vector_store = create_vector_store(chunks)
    
    print("Vector Store criado com sucesso!")
    
    print("\n=== 4. Testando Busca Semantica ===\n")
    
    question = "Com quanto tempo de antecedência devo pedir férias?"
    
    results = vector_store.similarity_search(
        question,
        k=3,
    )
    
    print(f"Pergunta: {question}")
    
    for index, result in enumerate(results):
        
        print("\n" + "=" * 70)
        
        print(f"RESULTADO {index + 1}")
        
        print("=" * 70)
        
        print(result.page_content)
        
        print("\nFonte:")
        
        print(result.metadata.get("source"))
        
if __name__ == "__main__":
    main()