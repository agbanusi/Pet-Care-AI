import streamlit as st
from openai import OpenAI
from mem0 import Memory, MemoryClient
import os
import redis
import json
from datetime import datetime, timedelta
from dotenv import load_dotenv
load_dotenv()

# Initialize a Redis connection
# redis_client = redis.StrictRedis(host='localhost', port=6379, db=0)
open_ai_key = os.getenv("OPENAI_API_KEY")
mo_api_key = os.getenv("MEM0_API_KEY")
redis_host =  os.getenv("REDIS_HOST")
redis_pass =  os.getenv("REDIS_PASS")

st.title("A Customer Service Agent for Pets")
st.caption("Chat with a customer support assistant who remembers your past interactions")

class CustomerSupportAgent:
  def __init__(self):
    config = {
      "vector_store":{
        "provider":"qdrant",
        "config": {
          "collection_name": "pets_care",
          "host":"localhost",
          "port":6333
        }
      }
    }

    self.memory =  MemoryClient(api_key=mo_api_key) 
    # Memory.from_config(config)
    self.client = OpenAI()
    self.app_id = "pet-customer-support"
    self.redis = redis.StrictRedis(host=redis_host, port=18004, password=redis_pass, db=0)

  def handle_query(self, query, user_id=None):
    previous_memories = self.memory.search(query=query, user_id=user_id)
    # print(self.get_memories(user_id))
    # print("\n\n ------------------------------ \n\n")
    # print(previous_memories)
    context = "Relevant past information for context: \n"+"\n".join([f"- {mem['memory']}" for mem in previous_memories])

    full_prompt = f"Previous Context: {context}\nCustomer: {query}\n Agent:"

    
    response = self.client.chat.completions.create(
      model="gpt-4o-mini",
      messages=[
        {"role":"system", "content":"You are a customer support AI agent for Petabix, a pets care app and you're designed to only answer question on dogs, cats and snake pets, different breeds of dogs, cats and snakes that are good for pets, daily routine of pets, breeding advice for pets and peridoic care routine for pets."},
        {"role":"user","content":full_prompt}
      ]
    )

    answer = response.choices[0].message.content
    self.memory.add(query, user_id=user_id, metadata={"app_id":self.app_id, "role":"user", "content":query, "created_at":datetime.now().isoformat()})
    self.memory.add(answer, user_id=user_id, metadata={"app_id": self.app_id, "role":"assistant", "content":answer, "created_at":datetime.now().isoformat()})
    self.add_to_history(query, user_id, "user")
    self.add_to_history(answer, user_id, "assistant")

    return answer

  def get_memories(self, user_id=None):
    return self.memory.get_all(user_id=user_id)

  # def initialize_chat_history(self, customer_id):
  #   memories = self.get_memories(customer_id)
  #   filtered_messages  = [
  #       {**mem["metadata"], "created_at": mem["created_at"]} for mem in memories 
  #       if "content" in mem["metadata"] and "created_at" in mem and "role" in mem["metadata"] and mem["metadata"]["content"] is not None
  #   ]
  
  #   sorted_messages = sorted(
  #       filtered_messages,
  #       key=lambda x: datetime.fromisoformat(x["created_at"])
  #   )

  #   print(sorted_messages)
    
  #   return sorted_messages

  def initialize_chat_history(self, customer_id):
    memories = self.get_data(customer_id)
    filtered_messages  = [
        mem for mem in memories 
        if "content" in mem and "created_at" in mem and "role" in mem and mem["content"] is not None
    ]
  
    sorted_messages = sorted(
        filtered_messages,
        key=lambda x: datetime.fromisoformat(x["created_at"])
    )
    
    return sorted_messages

  def add_to_history(self, text, user_id, role):
    
    context = json.dumps({
        "role":role, 
        "content":text,
        "user_id":user_id,
        "app_id": self.app_id,
        "created_at":datetime.now().isoformat(),
        # "metadata":{"app_id":self.app_id, "role":"user", "content":query, "created_at":datetime.now().isoformat()}
    })
    self.redis.rpush(f'conversations:{user_id}', context)

  def clear_data(self,user_id):
    self.redis.delete(f'conversations:{user_id}')

  def get_data(self,user_id):
    custom_chat_history = self.redis.lrange(f'conversations:{user_id}', 0, -1)
    custom_chat_history = [json.loads(msg) for msg in custom_chat_history]
    return custom_chat_history

  
support_agent = CustomerSupportAgent()
st.sidebar.title("Enter your customer Id:")
customer_id = st.sidebar.text_input("Enter your Customer Id")
setup = False

if "messages" not in st.session_state:
  st.session_state.messages =[]

if "setup_complete" not in st.session_state:
  st.session_state.setup_complete = False

if(customer_id and not st.session_state.setup_complete):
  st.session_state.messages = support_agent.initialize_chat_history(customer_id)
  st.session_state.setup_complete = True

for message in st.session_state.messages:
  with st.chat_message(message["role"]):
    st.markdown(message["content"])

query = st.chat_input("How can I assist you today?")

if(query and customer_id):
  st.session_state.messages.append({"role":"user", "content":query})
  with st.chat_message("user"):
    st.markdown(query)

  answer = support_agent.handle_query(query, user_id=customer_id)

  st.session_state.messages.append({"role":"assistant", "content":answer})

  with st.chat_message("assistant"):
    st.markdown(answer)



# Give me ideas of training my dog on how to sit and roll over

# On the teaching my dog to rollover can you set a weekly training regimen that happened thrice a week, Monday, Wednesday and Saturday for the next four weeks and what to do on each training day

