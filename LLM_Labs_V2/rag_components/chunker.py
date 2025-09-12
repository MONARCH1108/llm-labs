import logging
from langchain.text_splitter import (
    TokenTextSplitter, 
    CharacterTextSplitter, 
    RecursiveCharacterTextSplitter
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

def token_chunker(text: str, chunk_size: int = 256, chunk_overlap: int = 20, method_name: str = "TokenTextSplitter"):
    logging.info(f"User selected chunking method: {method_name}")
    try:
        splitter = TokenTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
        chunks = splitter.split_text(text)
        logging.info(f"[{method_name}] Generated {len(chunks)} chunks with chunk_size={chunk_size}, chunk_overlap={chunk_overlap}")
        return chunks
    except Exception as e:
        logging.error(f"[{method_name}] Error occurred: {e}")
        raise

def tiktoken_chunker(text: str, model_name: str = "gpt-3.5-turbo", chunk_size: int = 256, chunk_overlap: int = 20, method_name: str = "TiktokenChunker"):
    logging.info(f"User selected chunking method: {method_name}")
    try:
        splitter = CharacterTextSplitter.from_tiktoken_encoder(
            model_name=model_name,
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap
        )
        chunks = splitter.split_text(text)
        logging.info(f"[{method_name}] Generated {len(chunks)} chunks for model={model_name} with chunk_size={chunk_size}, chunk_overlap={chunk_overlap}")
        return chunks
    except Exception as e:
        logging.error(f"[{method_name}] Error occurred: {e}")
        raise

def char_chunker(text: str, chunk_size: int = 1000, chunk_overlap: int = 100, separator: str = "\n", method_name: str = "CharacterTextSplitter"):
    logging.info(f"User selected chunking method: {method_name}")
    try:
        splitter = CharacterTextSplitter(separator=separator, chunk_size=chunk_size, chunk_overlap=chunk_overlap)
        chunks = splitter.split_text(text)
        logging.info(f"[{method_name}] Generated {len(chunks)} chunks with chunk_size={chunk_size}, chunk_overlap={chunk_overlap}, separator='{separator}'")
        return chunks
    except Exception as e:
        logging.error(f"[{method_name}] Error occurred: {e}")
        raise

def recursive_char_chunker(text: str, chunk_size: int = 500, chunk_overlap: int = 50, separators: list = ["\n\n", "\n", " ", ""], method_name: str = "RecursiveCharacterTextSplitter"):
    logging.info(f"User selected chunking method: {method_name}")
    try:
        splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap, separators=separators)
        chunks = splitter.split_text(text)
        logging.info(f"[{method_name}] Generated {len(chunks)} chunks with chunk_size={chunk_size}, chunk_overlap={chunk_overlap}, separators={separators}")
        return chunks
    except Exception as e:
        logging.error(f"[{method_name}] Error occurred: {e}")
        raise

def sentence_chunker(text: str, chunk_size: int = 500, chunk_overlap: int = 50, separators: list = [". ", "! ", "? ", "\n"], method_name: str = "SentenceChunker"):
    logging.info(f"User selected chunking method: {method_name}")
    try:
        splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap, separators=separators)
        chunks = splitter.split_text(text)
        logging.info(f"[{method_name}] Generated {len(chunks)} chunks with chunk_size={chunk_size}, chunk_overlap={chunk_overlap}, separators={separators}")
        return chunks
    except Exception as e:
        logging.error(f"[{method_name}] Error occurred: {e}")
        raise
