from llama_index import SimpleDirectoryReader, VectorStoreIndex, LLMPredictor, PromptHelper
from langchain.chat_models import ChatOpenAI
import gradio as gr
import sys
import os
import redis
import json
from llama_index.prompts  import PromptTemplate
from llama_index.llms import ChatMessage, MessageRole
from dotenv import load_dotenv
load_dotenv()

# Initialize a Redis connection
redis_client = redis.StrictRedis(host='localhost', port=6379, db=0)

api_key = os.getenv("OPENAI_API_KEY")
index = None
user_id = 10

# gather data on dog breeds,
# gather data on dog care and grooming
# gather data on dog illness and common sickness
# gather data on dog training
# gather data on dog foods and stores
# gather data on dog behaviours
# do dame for cats

def construct_index(directory_path):
    documents = SimpleDirectoryReader(directory_path).load_data()
    indax = VectorStoreIndex.from_documents(documents)

    return indax

def serialize_chat_message(chat_message):
    return {"role": chat_message.role, "content": chat_message.content}

def deserialize_chat_message(data):
    content = data["content"]
    if (data["role"] == "USER"):
        return ChatMessage(role=MessageRole.USER, content=content)
    else:
        return ChatMessage(role=MessageRole.ASSISTANT, content=content)
    


# def pre_get_chatbot(input_text):
#     n_index = index.as_query_engine(verbose=True)  #.load_from_disk('index.json')
#     response = n_index.query(input_text)
#     return response.response

# def pre_chatbot(input_text):
#     pre_input = pre_get_chatbot(input_text)
#     n_index = index.as_chat_engine(verbose=True)
#     response = n_index.chat(f"explain further and give more details on this '{pre_input}'")
#     return response.response

def add_to_history(message,user_id, ai_or_human):
    context = None
    
    if (ai_or_human == "USER"):
       context = json.dumps({
                "role":MessageRole.USER, 
                "content":message
            
            })
    else:
        context = json.dumps({
                "role":MessageRole.ASSISTANT, 
                "content":message
            
            })    
    redis_client.rpush(f'conversation:{user_id}', context)

def clear_data():
    redis_client.delete(f'conversation:{user_id}')
    
def is_pet_related_query(index, query):
  custom_chat_history = redis_client.lrange(f'conversation:{user_id}', 0, -1)
  custom_chat_history = [deserialize_chat_message(json.loads(msg)) for msg in custom_chat_history]

  engine = index.as_query_engine(verbose=True, chat_history=custom_chat_history,)
  query_text = engine.query(query).response
  return query_text.find("I'm sorry, but") == -1

def generate_response(index, query, user_id):
  # Get the user's custom chat history
  custom_chat_history = redis_client.lrange(f'conversation:{user_id}', 0, -1)
  custom_chat_history = [deserialize_chat_message(json.loads(msg)) for msg in custom_chat_history]

  # Create a chat engine
  engine = index.as_query_engine(verbose=True, chat_history=custom_chat_history,)
  chat_engine = index.as_chat_engine(
      query_engine=engine,
      chat_mode='context',
      chat_history=custom_chat_history,
      verbose=True
  )

  # Generate a response
  response = chat_engine.chat(f" {query}").response
  # Add the response to the user's conversation history
  add_to_history(response, user_id,"AI")
  return response

def pre_update():
    #set up context for new convo, should only be called once
    add_to_history('Tell me about dogs generally', user_id, "USER")
    add_to_history("Dogs are domesticated mammals and are often referred to as man's best friend due to their close relationship with humans. They belong to the Canidae family and are descendants of wolves. Dogs come in a wide variety of breeds, each with its own unique characteristics, appearance, and temperament.", user_id, "AI")
    
def chatbot(input_text):
    add_to_history(input_text, user_id, "USER")
    if not is_pet_related_query(index,input_text):
      # If the query is not related to pets, return a default response
        response = "I'm sorry, but I can only answer questions about pets."
    else:
        # If the query is related to pets, generate a response using the chat engine
        response = generate_response(index, input_text, user_id)
    
    # engine = index.as_query_engine(verbose=True, similarity_top_k=1)
    
    # custom_chat_history = redis_client.lrange(f'conversation:{user_id}', 0, -1)
    # custom_chat_history = [deserialize_chat_message(json.loads(msg)) for msg in custom_chat_history]
    # add_to_history(input_text, user_id, "USER")
    # chat_engine = index.as_chat_engine(
    #     query_engine=engine, 
    #     chat_mode = 'best',
    #     chat_history=custom_chat_history,
    #     verbose=True
    # )
     
    # query_text = engine.query(input_text).response
    # print('first query',query_text)
    # #avoid non contextual inputs
    # if query_text.find("I'm sorry, but",0, 20) != -1:
    #     add_to_history(query_text, user_id,"AI")
    #     return query_text
    
    # response = chat_engine.chat(f" {input_text}").response #(f"I need you to act as a query system, if ${input_text} is similar to this text 'I'm sorry, but I don't have enough information to answer your query.' respond with 'I'm sorry, but I don't have enough information to answer your query.', otherwise, try as much to expatiate on this and give more details on the explanation '{input_text}', using previous context")
    # add_to_history(response, user_id,"AI")
    
    return response


iface = gr.Interface(fn=chatbot,
                     inputs=gr.components.Textbox(lines=7, label="Enter your text"),
                     outputs="text",
                     title="Custom-trained AI Chatbot On Pets")

index = construct_index("sources")
redis_client.flushall()
pre_update()
iface.launch(share=True)
