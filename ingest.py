
# TODO: Implement logic to ingest documents from the docs/ folder
# TODO: Generate embeddings for each document using the embedding service
# TODO: Store the embeddings in the vector database
import os
import json
from sentence_transformers import SentenceTransformer
from PyPDF2 import PdfReader

# تحميل الموديل
model = SentenceTransformer("BAAI/bge-small-en")

def split_text(text, chunk_size=500):
    return [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]

def embed_text(text):
    vector = model.encode(text)
    return vector.tolist()

def save_embedding(chunk, vector, file_path="embeddings.json"):
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except FileNotFoundError:
        data = []

    data.append({"chunk": chunk, "vector": vector})

    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def extract_text(file_path):
    text = ""
    if file_path.endswith(".pdf"):
        reader = PdfReader(file_path)
        for page in reader.pages:
            text += page.extract_text() + "\n"
    elif file_path.endswith(".txt"):
        with open(file_path, "r", encoding="utf-8") as f:
            text = f.read()
    else:
        raise ValueError("❌ Unsupported file format. Use PDF or TXT.")

    return text

def ingest_file(file_path):
    text = extract_text(file_path)
    chunks = split_text(text)
    print(f"📄 File: {os.path.basename(file_path)}")
    print(f"🔹 Total chunks: {len(chunks)}")

    # preview أول 2 chunks
    for i, chunk in enumerate(chunks[:2]):
        print(f"\n--- Chunk {i+1} ---\n{chunk[:500]}")

    for i, chunk in enumerate(chunks):
        vector = embed_text(chunk)
        save_embedding(chunk, vector, file_path="C:/Users/saram/Downloads/embeddings1.json")
        print(f"✅ Saved chunk {i+1}/{len(chunks)}")

if __name__ == "__main__":
    ingest_file("C:/Users/saram/Downloads/chatbot/AMIT_RAG_Chatbot/docs/data.pdf")


