import os
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./devassist.db")
CHROMA_DIR = os.getenv("CHROMA_DIR", "./chromadb_store")
MODEL_NAME = os.getenv("MODEL_NAME", "gemini-1.5-flash")
