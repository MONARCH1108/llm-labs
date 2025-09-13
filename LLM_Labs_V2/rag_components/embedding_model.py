import logging
from typing import List, Dict
import numpy as np
from langchain_huggingface import HuggingFaceEmbeddings
from huggingface_hub import list_models
from huggingface_hub.errors import HfHubHTTPError
from sklearn.metrics.pairwise import cosine_similarity, euclidean_distances

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 🔹 Fetch all sentence-transformer models
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

# 🔹 Initialize embeddings
def get_huggingface_embeddings(model_name: str):
    try:
        logger.info(f"Initializing HuggingFaceEmbeddings with model: {model_name}")
        embeddings = HuggingFaceEmbeddings(model_name=model_name)
        return embeddings
    except Exception as e:
        logger.error(f"Error initializing HuggingFaceEmbeddings: {e}")
        return None

# 🔹 Embed chunks into vectors
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

# 🔹 Compare embeddings for retrieval evaluation
def compare_embeddings(query: str, chunks: List[str], vectors: List[List[float]], model_name: str) -> List[Dict]:
    logger.info(f"Comparing embeddings for query: '{query}' using {model_name}")

    embedder = get_huggingface_embeddings(model_name)
    query_vec = np.array(embedder.embed_query(query)).reshape(1, -1)
    vectors_np = np.array(vectors)

    # Similarity measures
    cos_scores = cosine_similarity(query_vec, vectors_np)[0]
    euclidean_scores = -euclidean_distances(query_vec, vectors_np)[0]  # negate for ranking
    dot_scores = np.dot(vectors_np, query_vec.T).flatten()

    results = []
    for idx, chunk in enumerate(chunks):
        results.append({
            "chunk": chunk,
            "cosine": float(cos_scores[idx]),
            "euclidean": float(euclidean_scores[idx]),
            "dot": float(dot_scores[idx])
        })

    results_sorted = sorted(results, key=lambda x: x["cosine"], reverse=True)

    logger.info(f"Top retrieval results for {model_name}:")
    for r in results_sorted[:3]:
        logger.info(f"Chunk: {r['chunk'][:50]}... | Cos: {r['cosine']:.4f} | "
                    f"Euclid: {r['euclidean']:.4f} | Dot: {r['dot']:.4f}")

    return results_sorted
