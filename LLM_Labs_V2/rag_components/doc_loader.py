from langchain_community.document_loaders import PyPDFLoader
from langchain_community.document_loaders import Docx2txtLoader
from langchain_community.document_loaders import TextLoader
import os
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def load_pdf(file_path: str) -> str:
    try:
        logger.info(f"Loading PDF document: {file_path}")
        loader = PyPDFLoader(file_path)
        docs = loader.load()
        contents = [doc.page_content for doc in docs]
        return "\n".join(contents).strip()
    except Exception as e:
        logger.error(f"Error loading PDF: {e}")
        raise RuntimeError("Error loading PDF: " + str(e))

def load_docx(file_path: str) -> str:
    try:
        logger.info(f"Loading DOCX document: {file_path}")
        loader = Docx2txtLoader(file_path)
        docs = loader.load()
        contents = [doc.page_content for doc in docs]
        return "\n".join(contents).strip()
    except Exception as e:
        logger.error(f"Error loading DOCX: {e}")
        raise RuntimeError("Error loading DOCX: " + str(e))

def load_txt(file_path: str) -> str:
    try:
        logger.info(f"Loading TXT document: {file_path}")
        loader = TextLoader(file_path, encoding="utf-8")
        docs = loader.load()
        contents = [doc.page_content for doc in docs]
        return "\n".join(contents).strip()
    except Exception as e:
        logger.error(f"Error loading TXT: {e}")
        raise RuntimeError("Error loading TXT: " + str(e))

def load_document(file_path: str) -> str:
    ext = os.path.splitext(file_path)[-1].lower()
    logger.info(f"Detected file extension: {ext}")
    if ext == ".pdf":
        return load_pdf(file_path)
    elif ext == ".docx":
        return load_docx(file_path)
    elif ext == ".txt":
        return load_txt(file_path)
    else:
        logger.error(f"Unsupported file format: {ext}")
        raise ValueError(f"Unsupported file format: {ext}")
