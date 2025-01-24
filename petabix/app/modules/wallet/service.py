from pony.orm import db_session
from models.wallet import Wallet
from models.transaction import Transaction
from fastapi import HTTPException

class WalletService:
    @db_session
    async def get_wallet_balance(self, current_user: dict):
        wallet = Wallet.get(user_id=current_user['id'])
        if not wallet:
            raise HTTPException(status_code=404, detail="Wallet not found")
        return wallet

    @db_session
    async def debit_wallet(self, amount: float, current_user: dict):
        wallet = Wallet.get(user_id=current_user['id'])
        if not wallet:
            raise HTTPException(status_code=404, detail="Wallet not found")
        
        if wallet.balance < amount:
            raise HTTPException(status_code=400, detail="Insufficient funds")
        
        wallet.balance -= amount
        Transaction(user_id=current_user['id'], amount=amount, type="debit", status="completed")
        return wallet

    @db_session
    async def credit_wallet(self, amount: float, current_user: dict):
        wallet = Wallet.get(user_id=current_user['id'])
        if not wallet:
            raise HTTPException(status_code=404, detail="Wallet not found")
        
        wallet.balance += amount
        Transaction(user_id=current_user['id'], amount=amount, type="credit", status="completed")
        return wallet

    @staticmethod
    @db_session
    def debit_wallet_for_order(user_id: int, amount: float):
        wallet = Wallet.get(user_id=user_id)
        if not wallet:
            raise HTTPException(status_code=404, detail="Wallet not found")
        
        if wallet.balance < amount:
            return False
        
        wallet.balance -= amount
        Transaction(user_id=user_id, amount=amount, type="debit", status="completed")
        return True

    @staticmethod
    @db_session
    def credit_wallet_by_admin(user_id: int, amount: float):
        wallet = Wallet.get(user_id=user_id)
        if not wallet:
            raise HTTPException(status_code=404, detail="Wallet not found")
        
        wallet.balance += amount
        Transaction(user_id=user_id, amount=amount, type="credit", status="completed")
        return True