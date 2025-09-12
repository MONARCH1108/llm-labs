from langchain.text_splitter import TokenTextSplitter
from langchain.text_splitter import CharacterTextSplitter
from langchain.text_splitter import RecursiveCharacterTextSplitter

def token_chunker(text: str, chunk_size: int = 256, chunk_overlap: int = 20):
    splitter = TokenTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap
    )
    return splitter.split_text(text)

def tiktoken_chunker(text: str, model_name: str = "gpt-3.5-turbo", chunk_size: int = 256, chunk_overlap: int = 20):
    splitter = CharacterTextSplitter.from_tiktoken_encoder(
        model_name=model_name,
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap
    )
    return splitter.split_text(text)

def char_chunker(text: str, chunk_size: int = 1000, chunk_overlap: int = 100, separator: str = "\n"):
    splitter = CharacterTextSplitter(
        separator=separator,
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap
    )
    return splitter.split_text(text)

def recursive_char_chunker(text: str, chunk_size: int = 500, chunk_overlap: int = 50, separators: list = ["\n\n", "\n", " ", ""]):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=separators
    )
    return splitter.split_text(text)

def sentence_chunker(text: str, chunk_size: int = 500, chunk_overlap: int = 50, separators: list = [". ", "! ", "? ", "\n"]):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=separators
    )
    return splitter.split_text(text)


