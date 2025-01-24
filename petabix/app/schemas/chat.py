from pydantic import BaseModel, constr
from typing import List, Optional
from datetime import datetime

class ChatCreate(BaseModel):
    title: constr(min_length=1, max_length=100)  # Title of the chat
    participants: List[int]  # List of user IDs participating in the chat

class ChatResponse(BaseModel):
    id: int  # Unique identifier for the chat
    title: str  # Title of the chat
    participants: List[int]  # List of user IDs participating in the chat
    created_at: datetime  # Timestamp of when the chat was created

    class Config:
        orm_mode = True  # This allows Pydantic to work with ORM models

class MessageCreate(BaseModel):
    content: constr(min_length=1, max_length=500)  # Content of the message
    sender_id: int  # ID of the user sending the message

class MessageResponse(BaseModel):
    id: int  # Unique identifier for the message
    content: str  # Content of the message
    sender_id: int  # ID of the user who sent the message
    chat_id: int  # ID of the chat the message belongs to
    timestamp: datetime  # Timestamp of when the message was sent

    class Config:
        orm_mode = True  # This allows Pydantic to work with ORM models