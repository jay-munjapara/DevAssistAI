import os
import requests
import streamlit as st
from dotenv import load_dotenv

load_dotenv()
BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")

st.set_page_config(page_title="DevAssistAI", page_icon="🤖", layout="wide")

st.markdown("""
<style>
.main-title {font-size: 38px; font-weight: 800; margin-bottom: 0px;}
.subtitle {font-size: 16px; color: #8a8f98; margin-top: 0px;}
.card {padding: 18px; border-radius: 14px; border: 1px solid #30363d; background: #111827;}
.small {color: #8a8f98; font-size: 13px;}
</style>
""", unsafe_allow_html=True)

st.markdown('<p class="main-title">DevAssistAI</p>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">GenAI-powered developer assistant for code generation, debugging, explanations, and document Q&A.</p>', unsafe_allow_html=True)

with st.sidebar:
    st.header("Workspace")
    mode = st.radio(
        "Choose a feature",
        ["Code Generator", "Debug Assistant", "Code Explainer", "Document Q&A", "Logs"],
    )
    st.markdown("---")
    st.caption("Built with FastAPI, Gemini API, ChromaDB, SQLite, Streamlit, Python, and AWS-ready architecture.")


def call_api(endpoint: str, prompt: str):
    try:
        response = requests.post(f"{BACKEND_URL}{endpoint}", json={"prompt": prompt}, timeout=120)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as exc:
        st.error(f"API error: {exc}")
        return None

if mode == "Code Generator":
    col1, col2 = st.columns([1, 1])
    with col1:
        st.subheader("Prompt")
        prompt = st.text_area("Describe the code you want", height=320, placeholder="Example: Build a Python function to validate email addresses...")
        run = st.button("Generate Code", type="primary")
    with col2:
        st.subheader("AI Output")
        if run and prompt.strip():
            result = call_api("/generate", prompt)
            if result:
                st.caption(f"Latency: {result['latency_ms']} ms")
                st.markdown(result["response"])

elif mode == "Debug Assistant":
    st.subheader("Paste Code or Error Log")
    prompt = st.text_area("Debug input", height=330, placeholder="Paste stack trace, failed test, or buggy code here...")
    if st.button("Debug", type="primary") and prompt.strip():
        result = call_api("/debug", prompt)
        if result:
            st.caption(f"Latency: {result['latency_ms']} ms")
            st.markdown(result["response"])

elif mode == "Code Explainer":
    st.subheader("Paste Code to Explain")
    prompt = st.text_area("Code", height=330, placeholder="Paste code here...")
    if st.button("Explain Code", type="primary") and prompt.strip():
        result = call_api("/explain", prompt)
        if result:
            st.caption(f"Latency: {result['latency_ms']} ms")
            st.markdown(result["response"])

elif mode == "Document Q&A":
    st.subheader("Upload Documents")
    uploaded_file = st.file_uploader("Upload PDF, TXT, MD, or code files", type=["pdf", "txt", "md", "py", "js", "ts", "java", "csv"])
    if uploaded_file and st.button("Ingest Document"):
        files = {"file": (uploaded_file.name, uploaded_file.getvalue())}
        try:
            response = requests.post(f"{BACKEND_URL}/rag/upload", files=files, timeout=120)
            response.raise_for_status()
            data = response.json()
            st.success(f"Ingested {data['filename']} with {data['chunks_added']} chunks.")
        except requests.exceptions.RequestException as exc:
            st.error(f"Upload failed: {exc}")

    st.subheader("Ask Questions From Documents")
    question = st.text_area("Question", height=160, placeholder="Example: What are the main requirements in this document?")
    if st.button("Ask Document", type="primary") and question.strip():
        result = call_api("/rag/query", question)
        if result:
            st.caption(f"Latency: {result['latency_ms']} ms")
            st.markdown(result["response"])

elif mode == "Logs":
    st.subheader("Query Logs & Latency Monitoring")
    try:
        response = requests.get(f"{BACKEND_URL}/logs", timeout=30)
        response.raise_for_status()
        logs = response.json()
        if not logs:
            st.info("No logs yet. Run a query first.")
        for item in logs:
            with st.expander(f"{item['mode']} | {item['latency_ms']} ms | {item['created_at']}"):
                st.write("Prompt:", item["prompt"])
                st.write("Response:", item["response"])
    except requests.exceptions.RequestException as exc:
        st.error(f"Could not load logs: {exc}")
