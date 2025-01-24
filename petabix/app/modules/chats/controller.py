from fastapi import APIRouter, Depends, HTTPException
from typing import List
from .service import ChatService
from schemas.chat import ChatCreate, ChatResponse, MessageCreate, MessageResponse
from core.auth import get_current_user

router = APIRouter()

@router.post("/", response_model=ChatResponse)
async def create_chat(
    chat: ChatCreate,
    current_user: dict = Depends(get_current_user),
    service: ChatService = Depends()
):
    return await service.create_chat(chat, current_user)

@router.get("/{chat_id}", response_model=ChatResponse)
async def get_chat(
    chat_id: int,
    current_user: dict = Depends(get_current_user),
    service: ChatService = Depends()
):
    return await service.get_chat(chat_id, current_user)

@router.get("/ai/{chat_id}", response_model=ChatResponse)
async def get_ai_chat(
    current_user: dict = Depends(get_current_user),
    service: ChatService = Depends()
):
    return await service.get_ai_chat(current_user)

@router.get("/", response_model=List[ChatResponse])
async def list_chats(
    current_user: dict = Depends(get_current_user),
    service: ChatService = Depends()
):
    return await service.list_chats(current_user)

@router.post("/{chat_id}/messages", response_model=MessageResponse)
async def send_message(
    chat_id: int,
    message: MessageCreate,
    current_user: dict = Depends(get_current_user),
    service: ChatService = Depends()
):
    return await service.send_message(chat_id, message, current_user)