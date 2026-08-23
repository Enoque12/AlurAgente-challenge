import os

from dotenv import load_dotenv
from google import genai


# ============================================================
# CONFIGURAÇÃO
# ============================================================

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise RuntimeError(
        "GEMINI_API_KEY não encontrada. "
        "Verifique o arquivo .env."
    )


MODEL_NAME = "gemini-3.6-flash"


client = genai.Client(
    api_key=API_KEY
)


# ============================================================
# GERAÇÃO DA RESPOSTA
# ============================================================

def generate_answer(
    question: str,
    context: str,
    conversation_history: str = "",
) -> str:
    """
    Gera uma resposta utilizando os documentos recuperados
    e o histórico da conversa.
    """

    prompt = f"""
Você é o NexusTech AI Agent, um assistente corporativo
especializado em responder perguntas com base nos documentos
internos da empresa.

REGRAS:

1. Responda utilizando exclusivamente as informações
   presentes nos documentos fornecidos.

2. Não invente informações.

3. Se os documentos não contiverem informação suficiente
   para responder à pergunta, diga:

   "Não encontrei informações suficientes nos documentos disponíveis."

4. Utilize o histórico da conversa para compreender
   perguntas de seguimento e referências como:
   "isso", "esse valor", "ele", "ela", "esse benefício",
   "e no caso de...", etc.

5. O histórico serve para compreender o contexto da pergunta,
   mas os documentos recuperados são a fonte de verdade.

6. Responda sempre em português.

7. Seja objetivo, claro e profissional.

HISTÓRICO DA CONVERSA:
{conversation_history if conversation_history else "Nenhuma conversa anterior."}

DOCUMENTOS RECUPERADOS:
{context}

PERGUNTA ATUAL:
{question}

RESPOSTA:
"""

    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=prompt,
    )

    if response.text is None:
        return (
            "Não foi possível gerar uma resposta "
            "com base nos documentos disponíveis."
        )

    return response.text.strip()