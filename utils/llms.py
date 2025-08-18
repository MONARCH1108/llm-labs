import os
from groq import Groq
import google.generativeai as genai
from ollama import Client as OllamaClient
from dotenv import load_dotenv

load_dotenv()

def query_groq_llm(user_input: str, model: str, prompt: str) -> str:
    client = Groq(api_key=os.getenv("GROQ_API_KEY"))
    full_prompt = prompt + "\n" + user_input
    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": full_prompt}]
    )
    return response.choices[0].message.content.strip()

def query_gemini_llm(user_input: str, model: str, prompt: str) -> str:
    genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
    model = genai.GenerativeModel(model)
    full_prompt = prompt + "\n" + user_input
    response = model.generate_content(full_prompt)
    return response.text.strip()

def query_ollama_llm(user_input: str, model: str, prompt: str) -> str:
    client = OllamaClient()
    full_prompt = prompt + "\n" + user_input
    response = client.chat(
        model=model,
        messages=[{"role": "user", "content": full_prompt}]
    )
    return response['message']['content'].strip()