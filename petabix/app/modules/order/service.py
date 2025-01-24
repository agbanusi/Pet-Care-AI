from pony.orm import db_session
from models.order import Order
from schemas.order import OrderCreate, OrderUpdate
from modules.wallet.service import WalletService
from modules.transactions.service import TransactionService
from fastapi import HTTPException

class OrderService:
    @db_session
    async def create_order(self, order: OrderCreate, current_user: dict):
        # Check if user has sufficient balance
        if not WalletService.debit_wallet_for_order(current_user['id'], order.total_amount):
            raise HTTPException(status_code=400, detail="Insufficient funds")

        new_order = Order(
            user_id=current_user['id'],
            total_amount=order.total_amount,
            status="pending"
        )

        # Create a transaction for this order
        TransactionService.add_transaction(current_user['id'], order.total_amount, "order_payment")

        return new_order

    @db_session
    async def get_order(self, order_id: int, current_user: dict):
        order = Order.get(id=order_id, user_id=current_user['id'])
        if not order:
            raise HTTPException(status_code=404, detail="Order not found")
        return order

    @db_session
    async def update_order(self, order_id: int, order_data: OrderUpdate, current_user: dict):
        order = Order.get(id=order_id, user_id=current_user['id'])
        if not order:
            raise HTTPException(status_code=404, detail="Order not found")
        
        order.status = order_data.status
        return order

    @db_session
    async def list_orders(self, current_user: dict):
        return Order.select(lambda o: o.user_id == current_user['id'])
