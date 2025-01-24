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
            # instructions="The user has a premium account."
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

    def add_to_history(self, text, user_id, role):
        context = json.dumps({
            "role": role,
            "content": text,
            "user_id": user_id,
            "app_id": self.app_id,
            "created_at": datetime.now().isoformat(),
        })
        self.redis.rpush(f'conversations:{user_id}', context)

    def get_data(self, user_id):
        custom_chat_history = self.redis.lrange(f'conversations:{user_id}', 0, -1)
        return [json.loads(msg) for msg in custom_chat_history]