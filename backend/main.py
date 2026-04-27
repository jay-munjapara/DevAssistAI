import os
import time
import shutil
from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from .db import init_db, save_log, get_logs
from .llm import ask_gemini
from .rag import ingest_document, answer_from_docs
from .schemas import PromptRequest, PromptResponse

app = FastAPI(title="DevAssistAI API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

init_db()
os.makedirs("data", exist_ok=True)


def timed_response(mode: str, prompt: str, handler):
    start = time.perf_counter()
    response = handler(prompt)
    latency_ms = round((time.perf_counter() - start) * 1000, 2)
    save_log(mode, prompt, response, latency_ms)
    return PromptResponse(response=response, latency_ms=latency_ms)

@app.get("/")
def root():
    return {"message": "DevAssistAI API is running"}

@app.post("/generate", response_model=PromptResponse)
def generate_code(request: PromptRequest):
    prompt = f"Generate clean, production-ready code for this request:\n{request.prompt}"
    return timed_response("code_generation", request.prompt, lambda _: ask_gemini(prompt))

@app.post("/debug", response_model=PromptResponse)
def debug_code(request: PromptRequest):
    prompt = f"Analyze this code or error log. Explain the root cause and provide a fix:\n{request.prompt}"
    return timed_response("debugging", request.prompt, lambda _: ask_gemini(prompt))

@app.post("/explain", response_model=PromptResponse)
def explain_code(request: PromptRequest):
    prompt = f"Explain this code in simple terms and mention time/space complexity if relevant:\n{request.prompt}"
    return timed_response("code_explanation", request.prompt, lambda _: ask_gemini(prompt))

@app.post("/rag/query", response_model=PromptResponse)
def rag_query(request: PromptRequest):
    return timed_response("document_qa", request.prompt, lambda q: answer_from_docs(q))

@app.post("/rag/upload")
def upload_document(file: UploadFile = File(...)):
    file_path = os.path.join("data", file.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    chunks = ingest_document(file_path)
    return {"filename": file.filename, "chunks_added": chunks}

@app.get("/logs")
def logs(limit: int = 20):
    rows = get_logs(limit)
    return [
        {
            "id": row.id,
            "mode": row.mode,
            "prompt": row.prompt[:120],
            "response": row.response[:180],
            "latency_ms": row.latency_ms,
            "created_at": row.created_at.isoformat(),
        }
        for row in rows
    ]
