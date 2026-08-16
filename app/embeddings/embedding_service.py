
# TODO: Implement the embedding service
# TODO: Use HuggingFace BAAI model to generate embeddings from text
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("BAAI/bge-small-en")

def embed_text(text: str):
    embedding = model.encode(text)
    return embedding.tolist()

