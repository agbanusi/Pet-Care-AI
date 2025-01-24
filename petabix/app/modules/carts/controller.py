from fastapi import APIRouter, Depends, HTTPException
from typing import List
from .service import CartService
from schemas.cart import CartItemCreate, CartItemUpdate, CartResponse
from core.auth import get_current_user

router = APIRouter()

@router.post("/items", response_model=CartResponse)
async def add_to_cart(
    item: CartItemCreate,
    current_user: dict = Depends(get_current_user),
    service: CartService = Depends()
):
    return await service.add_to_cart(item, current_user)

@router.get("/", response_model=CartResponse)
async def get_cart(
    current_user: dict = Depends(get_current_user),
    service: CartService = Depends()
):
    return await service.get_cart(current_user)

@router.put("/items/{item_id}", response_model=CartResponse)
async def update_cart_item(
    item_id: int,
    item: CartItemUpdate,
    current_user: dict = Depends(get_current_user),
    service: CartService = Depends()
):
    return await service.update_cart_item(item_id, item, current_user)

@router.delete("/items/{item_id}", response_model=CartResponse)
async def remove_from_cart(
    item_id: int,
    current_user: dict = Depends(get_current_user),
    service: CartService = Depends()
):
    return await service.remove_from_cart(item_id, current_user)

