from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceBgeEmbeddings

MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"

def create_embeddings():
    """
    Cria o modelo responsavel por transformar
    textos em vetores numericos.
    """
    
    embeddings = HuggingFaceBgeEmbeddings(
        model_name=MODEL_NAME,
    )
    
    return embeddings

def create_vector_store(documents):
    """
    Cria um indice FAISS a partir dos documentos/chunks.
    """
    
    embeddings = create_embeddings()
    
    vector_store = FAISS.from_documents(
        documents,
        embeddings,
    )
    
    return vector_store

    
    