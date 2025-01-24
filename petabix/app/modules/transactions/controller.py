from fastapi import APIRouter, Depends, HTTPException
from typing import List
from .service import TransactionService
from schemas.transaction import TransactionCreate, TransactionUpdate, TransactionResponse
from core.auth import get_current_user

router = APIRouter()

# @router.post("/", response_model=TransactionResponse)
# async def create_transaction(
#     transaction: TransactionCreate,
#     current_user: dict = Depends(get_current_user),
#     service: TransactionService = Depends()
# ):
#     return await service.create_transaction(transaction, current_user)

@router.get("/{transaction_id}", response_model=TransactionResponse)
async def get_transaction(
    transaction_id: int,
    current_user: dict = Depends(get_current_user),
    service: TransactionService = Depends()
):
    return await service.get_transaction(transaction_id, current_user)

@router.put("/{transaction_id}/status", response_model=TransactionResponse)
async def update_transaction_status(
    transaction_id: int,
    status: str,
    current_user: dict = Depends(get_current_user),
    service: TransactionService = Depends()
):
    return await service.update_transaction_status(transaction_id, status, current_user)
