from pathlib import Path
from tempfile import TemporaryDirectory

import streamlit as st


SUPPORTED_EXTENSIONS = [
    "pdf",
    "docx",
    "xlsx",
    "pptx",
    "md",
    "csv",
    "json",
    "html",
    "txt",
]


def upload_documents():
    """
    Interface para upload dos documentos
    utilizados pelo agente.
    """

    uploaded_files = st.file_uploader(
        "📎 Adicione os documentos de conhecimento",
        type=SUPPORTED_EXTENSIONS,
        accept_multiple_files=True,
        help=(
            "Formatos suportados: PDF, DOCX, XLSX, "
            "PPTX, Markdown, CSV, JSON, HTML e TXT."
        ),
    )

    return uploaded_files