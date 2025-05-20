from pymongo import MongoClient

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["drdo_chatbot"]
collection = db["chat_history"]

def get_chat_history(user_id="guest"):
    """
    Retrieves previous chat history for the given user_id.
    For public access (non-logged-in), use user_id="guest"
    """
    records = collection.find({"user_id": user_id}).sort("timestamp", -1)
    return list(records)