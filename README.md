# 🤖 NexusTech AI Agent

> Assistente corporativo inteligente baseado em **Retrieval-Augmented Generation (RAG)**, desenvolvido para responder a perguntas utilizando informações presentes nos documentos de conhecimento de uma organização.

---

## 📌 Sobre o projecto

O **NexusTech AI Agent** é uma aplicação de Inteligência Artificial desenvolvida para facilitar o acesso a informações corporativas armazenadas em diferentes tipos de documentos.

A aplicação permite que o utilizador carregue documentos de conhecimento da organização e, posteriormente, faça perguntas em linguagem natural. O sistema processa os documentos, transforma o seu conteúdo em representações vectoriais (*embeddings*) e armazena essas representações numa base de conhecimento baseada em **FAISS**.

Quando uma pergunta é submetida, o sistema realiza uma **busca semântica**, identifica os conteúdos mais relevantes e envia o contexto recuperado para um **Large Language Model (LLM)**. O modelo utiliza esse contexto para gerar uma resposta fundamentada nas informações disponíveis nos documentos.

O projecto implementa, portanto, uma arquitectura baseada em **Retrieval-Augmented Generation (RAG)**, permitindo separar a recuperação de conhecimento da geração da resposta.

O principal objectivo é demonstrar a implementação de um **assistente corporativo baseado em RAG**, capaz de responder a perguntas utilizando como fonte de conhecimento documentos fornecidos pela organização.

---

## 🎯 Objectivos

O projecto foi desenvolvido com os seguintes objectivos:

- Permitir o carregamento de documentos corporativos;
- Suportar múltiplos formatos de documentos;
- Extrair automaticamente o conteúdo dos documentos;
- Normalizar o conteúdo extraído;
- Dividir documentos em *chunks* para melhorar a recuperação de informação;
- Gerar *embeddings* para os conteúdos processados;
- Criar uma base de conhecimento vectorial utilizando **FAISS**;
- Realizar pesquisas semânticas sobre os documentos;
- Recuperar os conteúdos mais relevantes para cada pergunta;
- Utilizar um **Large Language Model (LLM)** para gerar respostas;
- Fundamentar as respostas no contexto recuperado;
- Apresentar as fontes utilizadas na geração das respostas;
- Manter o histórico da conversa durante a sessão;
- Permitir perguntas de seguimento utilizando o contexto da conversa;
- Disponibilizar uma interface web através do **Streamlit**;
- Permitir execução local para desenvolvimento e testes;
- Permitir deployment da aplicação através do **Streamlit Community Cloud**.

---

# ✨ Funcionalidades

## 📚 Ingestão de documentos

A aplicação permite ao utilizador carregar um ou vários documentos de conhecimento simultaneamente.

Após o carregamento, os documentos são processados automaticamente através da pipeline de ingestão, que identifica o formato, utiliza o *loader* correspondente e transforma o conteúdo num formato compatível com a pipeline RAG.

### Formatos suportados

| Formato | Extensão | Descrição |
|---|---|---|
| PDF | `.pdf` | Documentos PDF |
| Microsoft Word | `.docx` | Documentos de texto |
| Microsoft Excel | `.xlsx` | Folhas de cálculo |
| Microsoft PowerPoint | `.pptx` | Apresentações |
| Markdown | `.md` | Documentação Markdown |
| CSV | `.csv` | Dados tabulares |
| JSON | `.json` | Dados estruturados |
| HTML | `.html` | Documentos/páginas HTML |
| Texto | `.txt` | Ficheiros de texto simples |

### Pipeline de ingestão

O processamento dos documentos segue, de forma geral, o seguinte fluxo:

```text
Documento
    │
    ▼
Identificação do formato
    │
    ▼
Loader específico
    │
    ▼
Extracção do conteúdo
    │
    ▼
Normalização
    │
    ▼
Divisão em chunks
    │
    ▼
Documentos processados
```

A aplicação utiliza diferentes *loaders* de acordo com o tipo de documento, permitindo que diferentes formatos sejam processados através de uma única pipeline de ingestão.

---

## 🔎 Busca semântica

O sistema não depende exclusivamente de correspondência exacta de palavras-chave.

Os documentos são transformados em representações vectoriais através de um modelo de *embeddings*. As perguntas submetidas pelo utilizador também são transformadas em vectores e comparadas com os conteúdos armazenados na base de conhecimento.

O projecto utiliza o seguinte modelo de *embeddings*:

```text
BAAI/bge-small-en-v1.5
```

As representações vectoriais são armazenadas numa base **FAISS (Facebook AI Similarity Search)**, permitindo realizar pesquisas de similaridade de forma eficiente.

O fluxo simplificado é:

```text
Pergunta do utilizador
        │
        ▼
      Embedding
        │
        ▼
Busca semântica no FAISS
        │
        ▼
Documentos/chunks relevantes
        │
        ▼
Contexto recuperado
        │
        ▼
       LLM
        │
        ▼
Resposta fundamentada
```

---

## 🧠 Retrieval-Augmented Generation (RAG)

O núcleo do sistema é baseado no paradigma **Retrieval-Augmented Generation (RAG)**.

Em vez de depender exclusivamente do conhecimento pré-existente do modelo de linguagem, o sistema primeiro recupera informações relevantes da base de conhecimento e utiliza essas informações como contexto para gerar a resposta.

A pipeline implementada pode ser representada da seguinte forma:

```text
┌──────────────────────┐
│ Documentos           │
│ corporativos         │
└──────────┬───────────┘
           │
           ▼
┌──────────────────────┐
│ Ingestão             │
│ e extracção          │
└──────────┬───────────┘
           │
           ▼
┌──────────────────────┐
│ Chunking             │
└──────────┬───────────┘
           │
           ▼
┌──────────────────────┐
│ Embeddings           │
│ BGE                  │
└──────────┬───────────┘
           │
           ▼
┌──────────────────────┐
│ FAISS                │
│ Vector Store         │
└──────────┬───────────┘
           │
           │
           │      Pergunta
           │         │
           │         ▼
           │   ┌─────────────┐
           └──►│ Similarity  │
               │ Search      │
               └──────┬──────┘
                      │
                      ▼
               ┌─────────────┐
               │ Contexto    │
               │ relevante   │
               └──────┬──────┘
                      │
                      ▼
               ┌─────────────┐
               │ Google      │
               │ Gemini      │
               └──────┬──────┘
                      │
                      ▼
               ┌─────────────┐
               │ Resposta    │
               │ + fontes    │
               └─────────────┘
```

---

## 📖 Respostas baseadas em fontes

Uma das características importantes do projecto é a apresentação das fontes utilizadas na recuperação da informação.

Para cada pergunta, o sistema identifica os documentos que contribuíram para a construção do contexto enviado ao modelo de linguagem.

Por exemplo:

```text
Pergunta:
Qual é o limite diário para alimentação durante viagens nacionais?

Resposta:
O limite máximo para despesas de alimentação durante viagens
nacionais de trabalho é de 1.500 MZN por dia.

Fontes:
📄 politica-despesas.md
```

As fontes permitem ao utilizador identificar a origem da informação utilizada pelo agente e aumentam a transparência do processo de geração da resposta.

---

## 💬 Conversação

A aplicação mantém o histórico das mensagens durante a sessão do utilizador.

As mensagens são armazenadas no estado da sessão do Streamlit e podem ser utilizadas como contexto adicional para perguntas subsequentes.

O histórico segue uma estrutura semelhante a:

```text
Utilizador
    │
    ├── Pergunta 1
    │
    ▼
Agente
    │
    ├── Resposta 1
    │
    ▼
Utilizador
    │
    ├── Pergunta 2
    │
    ▼
Agente
    │
    └── Resposta 2
```

Este mecanismo permite que o agente mantenha contexto entre perguntas relacionadas durante a mesma sessão.

---

## 🖥️ Interface Web

A interface da aplicação é desenvolvida utilizando **Streamlit**.

A interface disponibiliza:

- Área de carregamento de documentos;
- Gestão da base de conhecimento;
- Indicador do estado da base vectorial;
- Número de *chunks* processados;
- Área de conversação;
- Histórico das mensagens;
- Campo para submissão de perguntas;
- Respostas do agente;
- Identificação das fontes utilizadas;
- Opção para limpar a conversa;
- Opção para limpar a base de conhecimento.

A interface foi concebida para permitir que o utilizador interaja com o sistema sem necessidade de executar directamente os componentes internos da pipeline RAG.

---

## 🔬 Validação da ingestão multi-formato

O projecto inclui testes específicos para validar a capacidade de ingestão dos diferentes formatos suportados.

A execução do teste:

```bash
python -m scripts.test_multiformat
```

permite verificar os formatos processados e as respectivas fontes.

Exemplo de resultado:

```text
=== TESTE DE INGESTÃO MULTI-FORMATO ===

Documentos/chunks carregados: 16

=== FORMATOS ENCONTRADOS ===
csv: 3
docx: 1
html: 1
json: 1
md: 4
pdf: 1
pptx: 1
txt: 1
xlsx: 3
```

O teste também permite verificar as fontes identificadas pela pipeline:

```text
=== FONTES ENCONTRADAS ===

✓ documents\sample\beneficios.md
✓ documents\sample\politica-despesas.md
✓ documents\sample\politica-ferias.md
✓ documents\test\teste.csv
✓ documents\test\teste.docx
✓ documents\test\teste.html
✓ documents\test\teste.json
✓ documents\test\teste.md
✓ documents\test\teste.pdf
✓ documents\test\teste.pptx
✓ documents\test\teste.txt
✓ documents\test\teste.xlsx
```

Este teste confirma que a pipeline consegue processar os formatos previstos e produzir documentos/chunks utilizáveis pela camada de recuperação.

---

## 🧪 Testes da pipeline RAG

A pipeline RAG pode ser testada através do script:

```bash
python -m scripts.test_rag
```

O teste permite verificar:

1. Criação do vector store;
2. Recuperação semântica;
3. Scores dos resultados;
4. Documentos recuperados;
5. Geração da resposta;
6. Fontes utilizadas.

Exemplo:

```text
======================================================================
PERGUNTA
======================================================================
Com quanto tempo de antecedência devo solicitar férias?

======================================================================
DIAGNÓSTICO DA RECUPERAÇÃO
======================================================================
Pergunta: Com quanto tempo de antecedência devo solicitar férias?

Resultado 1: documents\sample\politica-ferias.md
Score: 0.4537

Resultado 2: documents\sample\politica-ferias.md
Score: 0.4582
```

Os resultados de recuperação são utilizados para seleccionar o contexto que será posteriormente enviado ao modelo de linguagem.

> **Nota:** A API do Google Gemini possui limites de utilização que podem afectar os testes de geração de respostas, especialmente em contas no plano gratuito. A recuperação vectorial e a ingestão de documentos podem continuar a ser testadas independentemente da disponibilidade da API de geração.


# 🏗️ Arquitectura do Sistema

O NexusTech AI Agent adopta uma arquitectura modular baseada no paradigma **Retrieval-Augmented Generation (RAG)**.

A aplicação está organizada em diferentes camadas, responsáveis pela interface, ingestão de documentos, processamento, recuperação semântica e geração das respostas.

## 🔄 Visão geral da arquitectura

A arquitectura pode ser representada da seguinte forma:

```text
┌───────────────────────────────────────────────────────────────┐
│                         UTILIZADOR                            │
│                                                               │
│              Upload de documentos + Perguntas                │
└───────────────────────────────┬───────────────────────────────┘
                                │
                                ▼
┌───────────────────────────────────────────────────────────────┐
│                    INTERFACE WEB                              │
│                       Streamlit                               │
│                                                               │
│  • Upload de documentos                                       │
│  • Gestão da base de conhecimento                             │
│  • Chat                                                       │
│  • Histórico da conversa                                      │
│  • Apresentação das fontes                                    │
└───────────────────────────────┬───────────────────────────────┘
                                │
                    ┌───────────┴───────────┐
                    │                       │
                    ▼                       ▼
┌───────────────────────────┐   ┌──────────────────────────────┐
│   PIPELINE DE INGESTÃO    │   │       PIPELINE DE RAG        │
│                           │   │                              │
│ • Identificação formato   │   │ • Recepção da pergunta      │
│ • Loaders                 │   │ • Embedding da pergunta     │
│ • Extracção               │   │ • Busca semântica           │
│ • Normalização            │   │ • Filtragem dos resultados  │
│ • Chunking                │   │ • Construção do contexto    │
└─────────────┬─────────────┘   └──────────────┬───────────────┘
              │                                │
              ▼                                ▼
┌───────────────────────────┐   ┌──────────────────────────────┐
│       DOCUMENTS           │   │         FAISS                │
│                           │   │      Vector Store            │
│ • page_content            │   │                              │
│ • metadata                │   │ • Vector embeddings          │
│ • source                  │   │ • Similarity search          │
└─────────────┬─────────────┘   └──────────────┬───────────────┘
              │                                │
              ▼                                │
┌───────────────────────────┐                   │
│      EMBEDDINGS           │◄──────────────────┘
│                           │
│ BAAI/bge-small-en-v1.5    │
└───────────────────────────┘

                                │
                                ▼
┌───────────────────────────────────────────────────────────────┐
│                     CONTEXTO RECUPERADO                       │
│                                                               │
│  Chunks relevantes + histórico da conversa + pergunta        │
└───────────────────────────────┬───────────────────────────────┘
                                │
                                ▼
┌───────────────────────────────────────────────────────────────┐
│                       LLM                                     │
│                    Google Gemini                              │
│                                                               │
│        Geração da resposta baseada no contexto                │
└───────────────────────────────┬───────────────────────────────┘
                                │
                                ▼
┌───────────────────────────────────────────────────────────────┐
│                         RESPOSTA                              │
│                                                               │
│  Resposta do agente + documentos utilizados como fontes      │
└───────────────────────────────────────────────────────────────┘
```
# 🛠️ Tecnologias utilizadas

O **NexusTech AI Agent** foi desenvolvido utilizando tecnologias e bibliotecas orientadas para a construção de aplicações de Inteligência Artificial, processamento de documentos e implementação de sistemas **Retrieval-Augmented Generation (RAG)**.

## Tecnologias principais

| Tecnologia | Utilização |
|---|---|
| **Python 3.14** | Linguagem principal do projecto |
| **Streamlit** | Desenvolvimento da interface web |
| **LangChain** | Orquestração da pipeline de processamento e RAG |
| **FAISS** | Armazenamento e pesquisa dos embeddings |
| **Google Gemini API** | Geração das respostas através de um Large Language Model |
| **Hugging Face** | Disponibilização do modelo de embeddings |
| **BAAI/bge-small-en-v1.5** | Geração de embeddings semânticos |
| **python-dotenv** | Carregamento das variáveis de ambiente |
| **Git / GitHub** | Controlo de versão e armazenamento do código |
| **Streamlit Community Cloud** | Deployment da aplicação |

---

## Inteligência Artificial e RAG

O projecto utiliza uma arquitectura baseada em **Retrieval-Augmented Generation (RAG)**.

O fluxo principal é composto pelas seguintes etapas:

```
Documentos
    │
    ▼
Ingestão
    │
    ▼
Extracção de conteúdo
    │
    ▼
Divisão em chunks
    │
    ▼
Geração de embeddings
    │
    ▼
FAISS Vector Store
    │
    │
    ▼
Pergunta do utilizador
    │
    ▼
Busca semântica
    │
    ▼
Recuperação dos conteúdos relevantes
    │
    ▼
Contexto + Pergunta
    │
    ▼
Google Gemini
    │
    ▼
Resposta fundamentada

┌─────────────────────────────────────────────┐
│             NexusTech AI Agent              │
├─────────────────────────────────────────────┤
│ Interface                                   │
│ └── Streamlit                               │
├─────────────────────────────────────────────┤
│ RAG / Orquestração                          │
│ ├── LangChain                               │
│ ├── LangChain Community                      │
│ ├── LangChain Text Splitters                 │
│ └── LangChain HuggingFace                    │
├─────────────────────────────────────────────┤
│ Embeddings                                  │
│ ├── Sentence Transformers                    │
│ └── BAAI/bge-small-en-v1.5                  │
├─────────────────────────────────────────────┤
│ Vector Store                                │
│ └── FAISS CPU                               │
├─────────────────────────────────────────────┤
│ Large Language Model                        │
│ └── Google Gemini API                       │
│     └── google-genai                        │
├─────────────────────────────────────────────┤
│ Ingestão Multi-formato                      │
│ ├── PDF → pypdf                             │
│ ├── DOCX → python-docx                     │
│ ├── XLSX → openpyxl                         │
│ ├── PPTX → python-pptx                      │
│ ├── HTML → BeautifulSoup4                   │
│ ├── Markdown → LangChain                    │
│ ├── CSV → Python / LangChain                │
│ ├── JSON → Python / LangChain               │
│ └── TXT → Python / LangChain                │
├─────────────────────────────────────────────┤
│ Geração / Documentos                        │
│ └── ReportLab                               │
├─────────────────────────────────────────────┤
│ Configuração                                │
│ └── python-dotenv                           │
├─────────────────────────────────────────────┤
│ Utilitários                                 │
│ └── tqdm                                     │
├─────────────────────────────────────────────┤
│ Versionamento                               │
│ └── Git / GitHub                            │
├─────────────────────────────────────────────┤
│ Deployment                                  │
│ └── Streamlit Community Cloud               │
└─────────────────────────────────────────────┘

# 📁 2. Estrutura de pastas

O projecto está organizado de forma modular, separando a interface da aplicação, a ingestão de documentos, o processamento da informação e os componentes responsáveis pela implementação do RAG.

A estrutura principal do projecto é a seguinte:

```text
aluragente/
│
├── app/
│   ├── __init__.py
│   │
│   ├── main.py
│   │
│   ├── ingestion/
│   │   ├── __init__.py
│   │   ├── loader.py
│   │   ├── splitter.py
│   │   ├── upload_processor.py
│   │   │
│   │   └── loaders/
│   │       ├── __init__.py
│   │       └── multi_loader.py
│   │
│   ├── rag/
│   │   ├── __init__.py
│   │   ├── rag_pipeline.py
│   │   ├── vector_store.py
│   │   └── llm.py
│   │
│   └── ui/
│       ├── __init__.py
│       └── uploader.py
│
├── documents/
│   ├── sample/
│   │   ├── beneficios.md
│   │   ├── politica-despesas.md
│   │   └── politica-ferias.md
│   │
│   └── test/
│       ├── teste.csv
│       ├── teste.docx
│       ├── teste.html
│       ├── teste.json
│       ├── teste.md
│       ├── teste.pdf
│       ├── teste.pptx
│       ├── teste.txt
│       └── teste.xlsx
│
├── scripts/
│   ├── create_test_documents.py
│   ├── test_ingestion.py
│   ├── test_multiformat.py
│   └── test_rag.py
│
├── .env
├── .gitignore
├── requirements.txt
└── README.md


```
# 📦 Requisitos e dependências

Antes de executar o projecto, certifique-se de que possui:

- Python 3.10 ou superior;
- Git;
- Conexão à Internet;
- Uma chave da **Google Gemini API**.

---

## 🚀 Passos para execução

### 1. Clonar o repositório

```bash
git clone <URL_DO_REPOSITORIO>
cd aluragente-challenge
```

### 2. Criar o ambiente virtual

**Windows**
```bash
python -m venv .venv
```

### 3. Activar o ambiente virtual

**Windows — Git Bash**
```bash
source .venv/Scripts/activate
```

**Windows — PowerShell**
```bash
.venv\Scripts\Activate.ps1
```

Após a activação, deverá aparecer algo semelhante a:

```
(.venv)
```

### 4. Instalar as dependências

```bash
pip install -r requirements.txt
```

### 5. Configurar a API do Gemini

Crie um ficheiro `.env` na raiz do projecto:

```env
GEMINI_API_KEY=sua_chave_api_aqui
```

### 6. Executar a aplicação

Com o ambiente virtual activo, execute:

```bash
python -m streamlit run app/main.py
```

A aplicação ficará disponível em:

```
http://localhost:8501
```

---

## 💬 Utilizar a aplicação

Após abrir a aplicação no navegador:

1. Carregue um ou mais documentos através da barra lateral;
2. Clique em **"Processar documentos"**;
3. Aguarde a criação da base de conhecimento;
4. Digite uma pergunta na área de chat;
5. Clique em **"Enviar pergunta"**;
6. Consulte a resposta e as fontes utilizadas pelo agente.

---

## ⏹️ Encerrar a aplicação

Para parar o servidor, pressione:

```
Ctrl + C
```

# 📸 Evidências e Screenshots

Esta secção apresenta evidências visuais do funcionamento do **NexusTech AI Agent**, demonstrando as principais funcionalidades implementadas no projecto.


---

## 🖥️ Interface principal

Screenshot da interface principal do NexusTech AI Agent, apresentando a área de conversação e a barra lateral com as funcionalidades de gestão da base de conhecimento.

**📷 Screenshot — Interface principal**

> **[INSERIR IMAGEM AQUI]**

## 📚 Upload de documentos

Evidência do carregamento de documentos de conhecimento através da interface da aplicação.

A aplicação permite seleccionar múltiplos ficheiros nos formatos suportados, que posteriormente são processados pela pipeline de ingestão.

**📷 Screenshot — Upload de documentos**

> **[INSERIR IMAGEM AQUI]**

## ⚙️ Processamento e criação da base de conhecimento

Evidência do processamento dos documentos carregados e da criação da base de conhecimento vectorial utilizando **FAISS**.

**📷 Screenshot — Base de conhecimento criada**

> **[INSERIR IMAGEM AQUI]**


## 💬 Conversação com o agente

Evidência da realização de uma pergunta em linguagem natural e da resposta gerada pelo agente com base nos documentos recuperados.

**Exemplo de pergunta:**

> Com quanto tempo de antecedência devo solicitar férias?

**📷 Screenshot — Pergunta e resposta**

> **[INSERIR IMAGEM AQUI]**


## 📖 Fontes consultadas

Evidência da apresentação das fontes utilizadas para gerar uma determinada resposta.

Esta funcionalidade permite ao utilizador identificar os documentos recuperados pela busca semântica utilizados como contexto para a geração da resposta.

**📷 Screenshot — Fontes consultadas**

> **[INSERIR IMAGEM AQUI]**

<!--
Sugestão de localização:
docs/images/fontes-consultadas.png
-->

---

## 📄 Teste de ingestão multi-formato

Evidência do teste realizado para validar o suporte aos diferentes formatos de documentos.

O teste confirmou a ingestão dos seguintes formatos:

- CSV
- DOCX
- HTML
- JSON
- Markdown
- PDF
- PPTX
- TXT
- XLSX

**📷 Screenshot — Resultado do teste multi-formato**

> **[INSERIR IMAGEM AQUI]**

<!--
Sugestão de localização:
docs/images/teste-multiformato.png
-->

---

## 🔎 Diagnóstico da recuperação semântica

Evidência dos testes realizados para verificar os resultados retornados pela busca semântica, incluindo os documentos recuperados e respectivos *scores* de distância.

**Exemplo de saída do diagnóstico:**

```text
======================================================================
DIAGNÓSTICO DA RECUPERAÇÃO
======================================================================
Pergunta: Com quanto tempo de antecedência devo solicitar férias?

Resultado 1: documents\sample\politica-ferias.md
Score: 0.4537

Resultado 2: documents\sample\politica-ferias.md
Score: 0.4582

Resultado 3: documents\test\teste.txt
Score: 0.5954