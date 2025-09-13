import logging
from langchain_huggingface import HuggingFaceEmbeddings
from typing import List
from huggingface_hub import list_models
from huggingface_hub.errors import HfHubHTTPError 

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_all_sentence_transformer_models() -> List[str]:
    try:
        logger.info("Fetching all sentence-transformer models from Hugging Face Hub...")
        models = list_models(search="sentence-transformers/")
        model_ids = [model.id for model in models if model.id.startswith("sentence-transformers/")]
        logger.info(f"Found {len(model_ids)} models.")
        return model_ids
    except HfHubHTTPError as e:
        logger.error(f"HTTP error while fetching models: {e}")
        return []
    except Exception as e:
        logger.error(f"Unexpected error while fetching models: {e}")
        return []

AVAILABLE_MODELS = get_all_sentence_transformer_models()

def get_huggingface_embeddings(model_name: str):
    try:
        logger.info(f"Initializing HuggingFaceEmbeddings with model: {model_name}")
        embeddings = HuggingFaceEmbeddings(model_name=model_name)
        return embeddings
    except Exception as e:
        logger.error(f"Error initializing HuggingFaceEmbeddings: {e}")
        return None

def embed_chunks(chunks: List[str], model_name: str):
    logger.info(f"Embedding {len(chunks)} chunks using model: {model_name}")
    embedder = get_huggingface_embeddings(model_name)
    if embedder is None:
        logger.error("Embedder initialization failed. Cannot embed chunks.")
        return []
    try:
        vectors = embedder.embed_documents(chunks)
        logger.info(f"Generated {len(vectors)} embeddings.")
        return vectors
    except Exception as e:
        logger.error(f"Error during embedding: {e}")
        return []
