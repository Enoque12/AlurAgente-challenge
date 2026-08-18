import streamlit as st

st.set_page_config(
    page_title="AluraCorp AI",
    page_icon="🤖",
    layout="wide",
)

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

question = st.chat_input(
    "Digite sua pergunta..."
)

if question:
    with st.chat_message("user"):
        st.write(question)
        
    with st.chat_message("assistant"):
        st.write(
            "Ainda estou sendo configurado. "
            "Em breve poderei consultar os documentos corporativos."
        )
        