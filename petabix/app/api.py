from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, EmailStr
from pymongo import MongoClient
from bson import ObjectId
import os
from dotenv import load_dotenv
from customer_support_agent import CustomerSupportAgent

load_dotenv()

app = FastAPI()

# MongoDB setup
mongo_url = os.getenv("MONGO_URL")
client = MongoClient(mongo_url)
db = client["pet_support_db"]
users_collection = db.users

# Initialize CustomerSupportAgent
support_agent = CustomerSupportAgent()

class User(BaseModel):
    email: EmailStr

class Query(BaseModel):
    user_id: str
    query: str

@app.post("/login")
async def login(user: User):
    existing_user = users_collection.find_one({"email": user.email})
    if not existing_user:
      users_collection.insert_one({"email": user.email})
        
    user = users_collection.find_one({"email": user.email})
    return {"user_id": str(user["_id"])}

@app.post("/chat")
async def chat(query: Query):
    answer = support_agent.handle_query(query.query, user_id=query.user_id)
    return {"answer": answer}

@app.get("/chat_history/{user_id}")
async def get_chat_history(user_id: str):
    history = support_agent.get_data(user_id)
    return {"history": history}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)