from pydantic import BaseModel, constr
from typing import Optional

class WalletTransaction(BaseModel):
    amount: float  # Amount for the transaction
    description: Optional[constr(max_length=255)] = None  # Optional description of the transaction

class WalletResponse(BaseModel):
    balance: float  # Current balance in the wallet
    transactions: Optional[list[WalletTransaction]] = None  # List of transactions (optional)

    class Config:
        orm_mode = True  # This allows Pydantic to work with ORM models