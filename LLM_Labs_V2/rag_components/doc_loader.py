from langchain_community.document_loaders import PyPDFLoader
from langchain_community.document_loaders import Docx2txtLoader
from langchain_community.document_loaders import TextLoader
import os

def load_pdf(file_path: str) -> str:
    try:
        loader = PyPDFLoader(file_path)
        docs = loader.load()
        contents = [doc.page_content for doc in docs]
        return "\n".join(contents).strip()
    except Exception as e:
        raise RuntimeError("Error loading PDF: " + str(e))

def load_docx(file_path: str) -> str:
    try:
        loader = Docx2txtLoader(file_path)
        docs = loader.load()
        contents = [doc.page_content for doc in docs]
        return "\n".join(contents).strip()
    except Exception as e:
        raise RuntimeError("Error loading DOCX: " + str(e))

def load_txt(file_path: str) -> str:
    try:
        loader = TextLoader(file_path, encoding="utf-8")
        docs = loader.load()
        contents = [doc.page_content for doc in docs]
        return "\n".join(contents).strip()
    except Exception as e:
        raise RuntimeError("Error loading TXT: " + str(e))

def load_document(file_path: str) -> str:
    ext = os.path.splitext(file_path)[-1].lower()  
    if ext == ".pdf":
        return load_pdf(file_path)
    elif ext == ".docx":
        return load_docx(file_path)
    elif ext == ".txt":
        return load_txt(file_path)
    else:
        raise ValueError(f"Unsupported file format: {ext}")
    
