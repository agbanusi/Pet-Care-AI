from pony.orm import db_session
from models.chat import Chat, ChatMessage
from models.customer import Customer
from models.veterinarian import Veterinarian
from schemas.chat import ChatCreate, MessageCreate
from fastapi import HTTPException
from customer_support_agent import CustomerSupportAgent
import os 



class ChatService:
    def __init__(self):
        self.support_agent = CustomerSupportAgent()
        ai = User.get(username='ai')
        if not ai:
            ai_user = User(
                username="ai",
                email="ai",
                hashed_password=os.getenv("AI_USER_PASSWORD"),
            )
            ai_user.flush()

    @db_session
    async def create_chat(self, chat: ChatCreate, current_user: dict):
        customer = Customer.get(user=current_user['id'])
        veterinarian = Veterinarian.get(id=chat.veterinarian_id) if chat.veterinarian_id else None
        
        new_chat = Chat(
            customer=customer,
            veterinarian=veterinarian,
            is_ai_chat=chat.is_ai_chat
        )
        return new_chat

    @db_session
    async def get_chat(self, chat_id: int, current_user: dict):
        chat = Chat.get(id=chat_id)
        if not chat or chat.customer.user.id != current_user['id']:
            raise HTTPException(status_code=404, detail="Chat not found")
        return chat

    @db_session
    async def get_ai_chat(self, current_user: dict):
        chat = Chat.get(is_ai_chat=True, customer=current_user['id'])
        if not chat or chat.customer.user.id != current_user['id']:
            raise HTTPException(status_code=404, detail="Chat not found")
        return chat

    @db_session
    async def list_chats(self, current_user: dict):
        customer = Customer.get(user=current_user['id'])
        return list(customer.chats)

    @db_session
    async def send_message(self, chat_id: int, message: MessageCreate, current_user: dict):
        chat = Chat.get(id=chat_id)
        ai = User.get(username='ai')
        if not chat or chat.customer.user.id != current_user['id']:
            raise HTTPException(status_code=404, detail="Chat not found")
        
        new_message = ChatMessage(
            chat=chat,
            sender=current_user['id'],
            content=message.content
        )

        chat.messages.add(new_message)

        if chat.is_ai_chat and ai:
            answer = self.support_agent.handle_query(message.content, user_id=chat.customer.user.id)
            ai_message = ChatMessage(
                chat=chat,
                sender=ai.id,
                content=answer
            )

            chat.messages.add(ai_message)

            return ai_message

        return new_message