import streamlit as st

from app.rag.rag_pipeline import (
    create_rag_pipeline,
    ask_question,
)

st.set_page_config(
    page_title="AluraCorp AI",
    page_icon="🤖",
    layout="wide",
)

with st.sidebar:
    
    st.title("🧠 AluraCorp AI")
    st.markdown(
        """
        **Assistente corporativo de conhecimento**

        Consulte políticas, benefícios,
        processos e outros documentos
        internos da organização.
        """
    )

    st.divider()

    st.markdown("### 📚 Base de conhecimento")

    st.write("Documentos carregados:")

    st.write("• Política de férias")
    st.write("• Política de despesas")
    st.write("• Benefícios corporativos")

    st.divider()

    st.caption(
        "AlurAgente Challenge"
    )

@st.cache_resource
def load_rag():
    """
    Cria o vector store apenas uma vez 
    durante a execução da aplicação
    """
    
    return create_rag_pipeline()
    
def main():
    
    st.title("🤖 AluraCorp AI")

    st.caption(
        "Assistente inteligente de conhecimento corporativo"
    )

    st.markdown(
        """
            ### Bem-vindo ao AluraCorp AI
            
            Faça perguntas sobre os documentos corporativos
            disponíveis na base de conhecimento.
        """
    )
    
    st.divider()
    
    #Iniciliza o RAG
    with st.spinner("Carregando base de conhecimento..."):
        vector_store = load_rag()
        
    # Historico da Conversa
    if "messages" not in st.session_state:
        st.session_state.messages = []
        
    # Exibe mensagens anteriores
    for message in st.session_state.messages:
        
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
            
            if message.get("sources"):
                st.caption("📚 Fontes")
                
                for source in message["sources"]:
                    st.caption(f"- {source}")
    
    # Campo de pergunta
    question = st.chat_input(
        "Faça uma pergunta sobre os documentos..."
    )
    
    if question:
        
        # Mensagem do usuario
        st.session_state.messages.append(
            {
                "role" : "user",
                "content" : question,
            }
        )
        
        with st.chat_message("user"):
            st.markdown(question)
            
        #Geracao da resposta
        with st.chat_message("assistant"):
            
            with st.spinner("Consultando documentos..."):
                
                answer, sources = ask_question(
                    vector_store,
                    question,
                )
            
            st.markdown(answer)
            
            if sources:
                
                st.caption("📚 Fontes")
                
                        
                for source in sources:
                    filename = source.replace("\\", "/").split("/")[-1]
                    
                    st.caption(f"📄 {filename}")
        
        # Salva resposta no historico
        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": answer,
                "sources": sources, 
            }
        )
                
if __name__ == "__main__":
    main()