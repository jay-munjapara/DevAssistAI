import google.generativeai as genai
from .config import GEMINI_API_KEY, MODEL_NAME

SYSTEM_GUIDE = """
You are DevAssistAI, a helpful software engineering assistant.
Give clear, practical answers. For code, include concise explanations and safe best practices.
Do not invent document facts. If context is missing, say what is missing.
"""

if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)


def ask_gemini(prompt: str) -> str:
    if not GEMINI_API_KEY:
        return "Gemini API key is missing. Add GEMINI_API_KEY to your .env file."

    model = genai.GenerativeModel(MODEL_NAME)
    result = model.generate_content(f"{SYSTEM_GUIDE}\n\nUser request:\n{prompt}")
    return result.text or "No response generated."
