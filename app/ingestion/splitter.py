from langchain_text_splitters import RecursiveCharacterTextSplitter

def split_documents(documents):
    """
    Divide os documentos em chunks menores
    para facilitar a recuperacao posterior.
    """
    
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        separators=[
            "\n## ",
            "\n### ",
            "\n\n",
            "\n",
            ". ",
            " ",
            "",
        ],
    )
    
    chunks = splitter.split_documents(documents)
    
    return chunks