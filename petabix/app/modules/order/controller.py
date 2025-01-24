from fastapi import APIRouter, Depends, HTTPException
from typing import List
from .service import OrderService
from schemas.order import OrderCreate, OrderUpdate, OrderResponse
from core.auth import get_current_user

router = APIRouter()

@router.post("/", response_model=OrderResponse)
async def create_order(
    order: OrderCreate,
    current_user: dict = Depends(get_current_user),
    service: OrderService = Depends()
):
    return await service.create_order(order, current_user)

@router.get("/{order_id}", response_model=OrderResponse)
async def get_order(
    order_id: int,
    current_user: dict = Depends(get_current_user),
    service: OrderService = Depends()
):
    return await service.get_order(order_id, current_user)

@router.put("/{order_id}", response_model=OrderResponse)
async def update_order(
    order_id: int,
    order: OrderUpdate,
    current_user: dict = Depends(get_current_user),
    service: OrderService = Depends()
):
    return await service.update_order(order_id, order, current_user)

@router.get("/", response_model=List[OrderResponse])
async def list_orders(
    current_user: dict = Depends(get_current_user),
    service: OrderService = Depends()
):
    return await service.list_orders(current_user)
