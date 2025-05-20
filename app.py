import streamlit as st
from chatbot_backend import get_chatbot_answer
from mongo_utils import get_chat_history  # optional for viewing history

st.set_page_config(page_title="DRDO Chatbot", page_icon="🤖")
st.title("DRDO Chatbot Interface")
st.markdown("Ask any question based on DRDO content scraped and indexed.")

# Set a default user ID
if "user_id" not in st.session_state:
    st.session_state.user_id = "guest"

# Load chat history for the user
if "chat_history" not in st.session_state:
    st.session_state.chat_history = get_chat_history(st.session_state.user_id)

# Display existing chat history
for chat in st.session_state.chat_history:
    st.chat_message("user").markdown(chat["question"])
    st.chat_message("assistant").markdown(chat["answer"])

# Chat input
query = st.chat_input("Ask a question...")

if query:
    # Display user query
    st.chat_message("user").markdown(query)

    # Get chatbot answer with user_id passed
    try:
        answer = get_chatbot_answer(query, user_id=st.session_state.user_id)
    except Exception as e:
        answer = f"⚠️ An error occurred: {str(e)}"

    # Display bot response
    st.chat_message("assistant").markdown(answer)

    # Save conversation in session
    st.session_state.chat_history.append({"question": query, "answer": answer})
