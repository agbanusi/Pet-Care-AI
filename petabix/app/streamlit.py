import streamlit as st
import requests
import json

API_URL = "http://localhost:8000"  # Replace with your actual API URL

def login(email):
    response = requests.post(f"{API_URL}/login", json={"email": email})
    if response.status_code == 200:
        return response.json()["user_id"]
    else:
        st.error("Login failed. Please try again.")
        return None

def get_chat_history(user_id):
    response = requests.get(f"{API_URL}/chat_history/{user_id}")
    if response.status_code == 200:
        return response.json()["history"]
    else:
        st.error("Failed to retrieve chat history.")
        return []

def send_message(user_id, query):
    response = requests.post(f"{API_URL}/chat", json={"user_id": user_id, "query": query})
    if response.status_code == 200:
        return response.json()["answer"]
    else:
        st.error("Failed to send message. Please try again.")
        return None

def main():
    st.title("PetaBix AI")
    st.caption("PetaBix AI, A Customer Service Agent for Pets")

    if "user_id" not in st.session_state:
        st.session_state.user_id = None

    if not st.session_state.user_id:
        email = st.text_input("Please enter your email to login:")
        if st.button("Login"):
            user_id = login(email)
            if user_id:
                st.session_state.user_id = user_id
                st.rerun()

    if st.session_state.user_id:
        if "messages" not in st.session_state:
            st.session_state.messages = get_chat_history(st.session_state.user_id)

        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        query = st.chat_input("How can I assist you today?")

        if query:
            st.session_state.messages.append({"role": "user", "content": query})
            with st.chat_message("user"):
                st.markdown(query)

            with st.chat_message("assistant"):
                message_placeholder = st.empty()
                message_placeholder.markdown("Thinking...")
                answer = send_message(st.session_state.user_id, query)
                message_placeholder.markdown(answer)

            st.session_state.messages.append({"role": "assistant", "content": answer})

if __name__ == "__main__":
    main()