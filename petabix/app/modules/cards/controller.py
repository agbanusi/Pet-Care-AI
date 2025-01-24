from fastapi import APIRouter, Depends, HTTPException
from typing import List
from .service import CardService
from schemas.card import CardCreate, CardUpdate, CardResponse
from core.auth import get_current_user

router = APIRouter()

@router.post("/", response_model=CardResponse)
async def create_card(
    card: CardCreate,
    current_user: dict = Depends(get_current_user),
    service: CardService = Depends()
):
    return await service.create_card(card, current_user)

@router.get("/{card_id}", response_model=CardResponse)
async def get_card(
    card_id: int,
    current_user: dict = Depends(get_current_user),
    service: CardService = Depends()
):
    return await service.get_card(card_id, current_user)

@router.get("/", response_model=List[CardResponse])
async def list_cards(
    current_user: dict = Depends(get_current_user),
    service: CardService = Depends()
):
    return await service.list_cards(current_user)

@router.put("/{card_id}", response_model=CardResponse)
async def update_card(
    card_id: int,
    card: CardUpdate,
    current_user: dict = Depends(get_current_user),
    service: CardService = Depends()
):
    return await service.update_card(card_id, card, current_user)

@router.delete("/{card_id}", response_model=bool)
async def delete_card(
    card_id: int,
    current_user: dict = Depends(get_current_user),
    service: CardService = Depends()
):
    return await service.delete_card(card_id, current_user)
