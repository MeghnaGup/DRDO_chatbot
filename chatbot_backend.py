from mistral_api import get_mistral_response
from faiss_utils import load_faiss_index  # your FAISS loading function

def get_chatbot_answer(query, user_id="guest"):
    # Load FAISS index and metadata
    index, metadata, model = load_faiss_index()

    # Encode the query into a vector
    query_vector = model.encode([query]).astype("float32")
    k = 5  # Number of top results to retrieve
    distances, indices = index.search(query_vector, k)

    # Prepare context from FAISS results
    context_docs = []
    for idx in indices[0]:
        if idx < len(metadata):  # safeguard for index overflow
            doc = f"Title: {metadata[idx]['title']}, URL: {metadata[idx]['url']}"
            context_docs.append(doc)

    context = "\n".join(context_docs)
    prompt = f"You are a chatbot trained on DRDO data.\nContext:\n{context}\n\nQuestion: {query}\nAnswer:"

    # Optionally log the query and user_id (for future use)
    # print(f"[{user_id}] Question: {query}")

    # Get answer string directly from Mistral API
    answer = get_mistral_response(prompt)
    return answer