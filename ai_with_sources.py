import streamlit as st
from openai import OpenAI
from mem0 import Memory
import os
import redis
import json
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

class CustomerSupportAgent:
    def __init__(self):
        self.open_ai_key = os.getenv("OPENAI_API_KEY")
        self.mo_api_key = os.getenv("MEM0_API_KEY")
        self.redis_host = os.getenv("REDIS_HOST")
        self.redis_pass = os.getenv("REDIS_PASS")
        self.assistant_id = os.getenv("OPENAI_ASST_ID")
        self.app_id = "pet-customer-support"

        config = {
            "vector_store": {
                "provider": "qdrant",
                "config": {
                    "collection_name": "pets_care",
                    "host": "localhost",
                    "port": 6333
                }
            }
        }

        self.memory = Memory.from_config(config)
        self.client = OpenAI()
        self.redis = redis.StrictRedis(host=self.redis_host, port=18004, password=self.redis_pass, db=0)

    def handle_query(self, query, user_id=None):
        previous_memories = self.memory.search(query=query, user_id=user_id)
        thread_id = self.get_user_thread(user_id)

        context = "Relevant past information for context: \n" + "\n".join([f"- {mem['memory']}" for mem in previous_memories])
        full_prompt = f"Previous Context: {context}\n\n {query}\n" if previous_memories else query

        message = self.client.beta.threads.messages.create(
            thread_id=thread_id,
            role="user",
            content=full_prompt
        )

        run = self.client.beta.threads.runs.create_and_poll(
            thread_id=thread_id,
            assistant_id=self.assistant_id,
            instructions="The user has a premium account."
        )

        if run.status == 'completed':
            messages = self.client.beta.threads.messages.list(thread_id=thread_id)
            answer = messages.data[0].content[0].text.value
            
            self.memory.add(query, user_id=user_id, metadata={"app_id": self.app_id, "role": "user", "content": query, "created_at": datetime.now().isoformat()})
            self.memory.add(answer, user_id=user_id, metadata={"app_id": self.app_id, "role": "assistant", "content": answer, "created_at": datetime.now().isoformat()})
            self.add_to_history(query, user_id, "user")
            self.add_to_history(answer, user_id, "assistant")

            return answer
        else:
            return f"Server is down, please try again: {run.status}"

    def get_user_thread(self, user_id=None):
        thread = self.redis.get(f'thread:{user_id}')
        if thread is not None:
            thread = thread.decode('utf-8')
        if not thread:
            thread_data = self.client.beta.threads.create()
            thread = thread_data.id
            self.redis.set(f'thread:{user_id}', thread)
        return thread

    def initialize_chat_history(self, customer_id):
        memories = self.get_data(customer_id)
        return sorted(
            [mem for mem in memories if all(key in mem for key in ["content", "created_at", "role"]) and mem["content"] is not None],
            key=lambda x: datetime.fromisoformat(x["created_at"])
        )

    def add_to_history(self, text, user_id, role):
        context = json.dumps({
            "role": role,
            "content": text,
            "user_id": user_id,
            "app_id": self.app_id,
            "created_at": datetime.now().isoformat(),
        })
        self.redis.rpush(f'conversations:{user_id}', context)

    def clear_data(self, user_id):
        self.redis.delete(f'conversations:{user_id}')

    def get_data(self, user_id):
        custom_chat_history = self.redis.lrange(f'conversations:{user_id}', 0, -1)
        return [json.loads(msg) for msg in custom_chat_history]

def main():
    st.title("Petabix AI")
    st.caption("Chat with PetaBix AI, A Customer Service Agent for Pets")

    support_agent = CustomerSupportAgent()
    
    st.sidebar.title("Enter your customer Id:")
    customer_id = st.sidebar.text_input("Enter your Customer Id")

    if "messages" not in st.session_state:
        st.session_state.messages = []

    if "setup_complete" not in st.session_state:
        st.session_state.setup_complete = False

    if customer_id and not st.session_state.setup_complete:
        st.session_state.messages = support_agent.initialize_chat_history(customer_id)
        st.session_state.setup_complete = True

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    query = st.chat_input("How can I assist you today?")

    if query and customer_id:
        st.session_state.messages.append({"role": "user", "content": query})
        with st.chat_message("user"):
            st.markdown(query)

        answer = support_agent.handle_query(query, user_id=customer_id)

        st.session_state.messages.append({"role": "assistant", "content": answer})
        with st.chat_message("assistant"):
            st.markdown(answer)

if __name__ == "__main__":
    main()