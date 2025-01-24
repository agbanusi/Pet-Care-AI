from pony.orm import db_session
from models.transaction import Transaction
from schemas.transaction import TransactionCreate, TransactionUpdate
from fastapi import HTTPException

class TransactionService:
    @db_session
    async def create_transaction(self, transaction: TransactionCreate, current_user: dict):
        new_transaction = Transaction(
            amount=transaction.amount,
            type=transaction.type,
            status="pending",
            user_id=current_user['id']
        )
        return new_transaction

    @db_session
    async def get_transaction(self, transaction_id: int, current_user: dict):
        transaction = Transaction.get(id=transaction_id, user_id=current_user['id'])
        if not transaction:
            raise HTTPException(status_code=404, detail="Transaction not found")
        return transaction

    @db_session
    async def update_transaction_status(self, transaction_id: int, status: str, current_user: dict):
        transaction = Transaction.get(id=transaction_id, user_id=current_user['id'])
        if not transaction:
            raise HTTPException(status_code=404, detail="Transaction not found")
        
        transaction.status = status
        return transaction

    @staticmethod
    @db_session
    def add_transaction(user_id: int, amount: float, transaction_type: str):
        new_transaction = Transaction(
            user_id=user_id,
            amount=amount,
            type=transaction_type,
            status="pending"
        )
        return new_transaction

    @staticmethod
    @db_session
    def confirm_transaction(transaction_id: int):
        transaction = Transaction.get(id=transaction_id)
        if not transaction:
            raise HTTPException(status_code=404, detail="Transaction not found")
        transaction.status = "completed"
        return transaction