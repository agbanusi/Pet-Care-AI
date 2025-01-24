from fastapi import APIRouter, Depends, HTTPException
from typing import List
from .service import WalletService
from schemas.wallet import WalletResponse, WalletTransaction
from core.auth import get_current_user

router = APIRouter()

@router.get("/balance", response_model=WalletResponse)
async def get_wallet_balance(
    current_user: dict = Depends(get_current_user),
    service: WalletService = Depends()
):
    return await service.get_wallet_balance(current_user)

@router.post("/debit", response_model=WalletResponse)
async def debit_wallet(
    transaction: WalletTransaction,
    current_user: dict = Depends(get_current_user),
    service: WalletService = Depends()
):
    return await service.debit_wallet(transaction.amount, current_user)

@router.post("/credit", response_model=WalletResponse)
async def credit_wallet(
    transaction: WalletTransaction,
    current_user: dict = Depends(get_current_user),
    service: WalletService = Depends()
):
    return await service.credit_wallet(transaction.amount, current_user)
