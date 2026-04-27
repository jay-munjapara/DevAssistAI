import os
import uuid
from typing import List
import chromadb
from pypdf import PdfReader
from .config import CHROMA_DIR
from .llm import ask_gemini

client = chromadb.PersistentClient(path=CHROMA_DIR)
collection = client.get_or_create_collection(name="devassist_docs")


def chunk_text(text: str, chunk_size: int = 900, overlap: int = 120) -> List[str]:
    text = " ".join(text.split())
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start = end - overlap
    return [chunk for chunk in chunks if chunk.strip()]


def read_file_text(file_path: str) -> str:
    if file_path.lower().endswith(".pdf"):
        reader = PdfReader(file_path)
        return "\n".join(page.extract_text() or "" for page in reader.pages)
    with open(file_path, "r", encoding="utf-8", errors="ignore") as file:
        return file.read()


def ingest_document(file_path: str) -> int:
    text = read_file_text(file_path)
    chunks = chunk_text(text)
    ids = [str(uuid.uuid4()) for _ in chunks]
    metadatas = [{"source": os.path.basename(file_path)} for _ in chunks]
    if chunks:
        collection.add(ids=ids, documents=chunks, metadatas=metadatas)
    return len(chunks)


def answer_from_docs(question: str, top_k: int = 4) -> str:
    results = collection.query(query_texts=[question], n_results=top_k)
    docs = results.get("documents", [[]])[0]
    context = "\n\n".join(docs)

    prompt = f"""
Answer the question using only the document context below.
If the context does not contain the answer, say that the uploaded documents do not provide enough information.

Context:
{context}

Question:
{question}
"""
    return ask_gemini(prompt)
