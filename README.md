# DevAssistAI

DevAssistAI is a GenAI-powered developer assistant that supports code generation, debugging, code explanation, and document-based Q&A using RAG.

## Tech Stack

- Backend: FastAPI, Python
- LLM: Gemini API
- RAG: ChromaDB, LangChain-ready architecture
- Database: SQLite for query and latency logging
- Frontend: Streamlit
- Deployment-ready: AWS-compatible backend structure

## Features

- Generate production-style code from natural language prompts
- Debug code snippets and error logs
- Explain unfamiliar code in simple language
- Upload documents and ask grounded questions using RAG
- Store query logs and latency metrics in SQLite
- Clean Streamlit UI for quick demos

## Project Structure

```text
DevAssistAI/
├── backend/
│   ├── main.py
│   ├── llm.py
│   ├── rag.py
│   ├── db.py
│   ├── config.py
│   └── schemas.py
├── frontend/
│   └── app.py
├── data/
├── tests/
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md
```

## Setup

### 1. Clone the repo

```bash
git clone https://github.com/YOUR_USERNAME/DevAssistAI.git
cd DevAssistAI
```

### 2. Create virtual environment

```bash
python -m venv .venv
source .venv/bin/activate
```

For Windows:

```bash
.venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Add environment variables

```bash
cp .env.example .env
```

Then edit `.env`:

```env
GEMINI_API_KEY=your_gemini_api_key_here
DATABASE_URL=sqlite:///./devassist.db
CHROMA_DIR=./chromadb_store
MODEL_NAME=gemini-1.5-flash
BACKEND_URL=http://localhost:8000
```

## Run the App

### Start FastAPI backend

```bash
uvicorn backend.main:app --reload
```

Backend will run at:

```text
http://localhost:8000
```

API docs:

```text
http://localhost:8000/docs
```

### Start Streamlit frontend

Open a new terminal:

```bash
source .venv/bin/activate
streamlit run frontend/app.py
```

Frontend will run at:

```text
http://localhost:8501
```

## API Endpoints

| Endpoint | Method | Purpose |
|---|---|---|
| `/generate` | POST | Generate code from a prompt |
| `/debug` | POST | Debug code or error logs |
| `/explain` | POST | Explain code |
| `/rag/upload` | POST | Upload and ingest documents |
| `/rag/query` | POST | Ask questions from uploaded documents |
| `/logs` | GET | View query logs and latency |

## Resume Bullet

```text
DevAssistAI | FastAPI, Gemini API, LangChain, ChromaDB, SQLite, Streamlit, Python, AWS | GitHub

◦ Built a GenAI-powered developer assistant using Gemini API, LangChain, and RAG to generate code, debug errors, explain snippets, and answer document-based queries, with ChromaDB semantic retrieval, prompt engineering, SQLite logging, latency monitoring, and AWS-ready FastAPI deployment.
```

## Future Improvements

- Add authentication with JWT
- Add AWS deployment using EC2 or Lambda
- Add prompt comparison playground
- Add unit tests for all endpoints
- Add Dockerfile and GitHub Actions CI/CD
