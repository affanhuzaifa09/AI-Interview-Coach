# utils/embeddings.py
# This file sets up the embedding model used to convert text into vectors.
# We use all-MiniLM-L6-v2 - a fast, lightweight and accurate embedding model.

from langchain_huggingface import HuggingFaceEmbeddings

def get_embedding_model():
    """
    Returns the HuggingFace embedding model.

    Model: all-MiniLM-L6-v2
    - Small and fast (only 22MB)
    - 384 dimensional embeddings
    - Great for semantic search tasks
    - Runs locally, no API key needed

    Returns:
        HuggingFaceEmbeddings object ready to use
    """

    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2",
        model_kwargs={"device": "cpu"},  # Use CPU (no GPU required)
        encode_kwargs={"normalize_embeddings": True}  # Normalize for better similarity search
    )

    return embeddings