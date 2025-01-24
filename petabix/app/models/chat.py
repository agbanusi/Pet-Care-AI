from pony.orm import Required, Optional, Set
from .base import Base_Model
from datetime import datetime

class ChatMessage(Base_Model):
    _table_ = 'chat_messages'
    chat = Required('Chat')
    sender = Required('User')
    content = Required(str)
    timestamp = Required(datetime, default=lambda: datetime.utcnow())

class Chat(Base_Model):
    _table_ = 'chats'
    chat_customer = Required('Customer')
    chat_veterinarian = Optional('Veterinarian')
    is_ai_chat = Required(bool, default=False)
    messages = Set('ChatMessage')