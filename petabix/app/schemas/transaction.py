from pydantic import BaseModel, constr
from typing import Optional

class TransactionCreate(BaseModel):
    amount: float  # Amount for the transaction
    transaction_type: constr(min_length=1, max_length=50)  # Type of transaction (e.g., credit, debit)
    description: Optional[constr(max_length=255)] = None  # Optional description of the transaction
    user_id: int  # ID of the user associated with the transaction

class TransactionUpdate(BaseModel):
    amount: Optional[float]  # Optional field to update the amount
    transaction_type: Optional[constr(min_length=1, max_length=50)]  # Optional field to update the type
    description: Optional[constr(max_length=255)] = None  # Optional field to update the description
    status: Optional[constr(min_length=1, max_length=50)] = None  # Optional field to update the status

class TransactionResponse(BaseModel):
    id: int  # Unique identifier for the transaction
    amount: float  # Amount for the transaction
    transaction_type: str  # Type of transaction
    description: Optional[str] = None  # Optional description of the transaction
    user_id: int  # ID of the user associated with the transaction
    status: str  # Status of the transaction (e.g., completed, pending)

    class Config:
        orm_mode = True  # This allows Pydantic to work with ORM models