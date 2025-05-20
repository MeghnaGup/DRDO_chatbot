import faiss
import numpy as np
import json
from sentence_transformers import SentenceTransformer

# Load your sentence transformer model here or pass as an argument
model = SentenceTransformer("all-MiniLM-L6-v2")

def create_faiss_index(embeddings, data, index_file="drdo_faiss.index", metadata_file="drdo_metadata.json"):
    """
    Creates a FAISS index from embeddings and saves index & metadata files.
    
    embeddings: list or np.array of vectors
    data: list of dicts with keys like 'title' and 'url'
    """
    embedding_array = np.array(embeddings).astype("float32")

    index = faiss.IndexFlatL2(embedding_array.shape[1])
    index.add(embedding_array)

    faiss.write_index(index, index_file)

    metadata = [{"title": d.get("title", ""), "url": d.get("url", "")} for d in data]
    with open(metadata_file, "w", encoding="utf-8") as f:
        json.dump(metadata, f, indent=2, ensure_ascii=False)
    
    print(f"FAISS index and metadata saved: {index_file}, {metadata_file}")

def load_faiss_index(index_file="drdo_faiss.index", metadata_file="drdo_metadata.json"):
    """
    Loads a FAISS index and metadata from disk.
    """
    index = faiss.read_index(index_file)
    with open(metadata_file, "r", encoding="utf-8") as f:
        metadata = json.load(f)
    return index, metadata, model

def search_faiss(query, index, metadata, k=5):
    """
    Search the FAISS index for top k similar documents to the query.
    """
    query_vec = model.encode([query]).astype("float32")
    distances, indices = index.search(query_vec, k)

    results = []
    for idx in indices[0]:
        results.append({
            "title": metadata[idx]["title"],
            "url": metadata[idx]["url"]
        })
    return results