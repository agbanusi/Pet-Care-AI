from pydantic import BaseModel, constr
from typing import List, Optional

class OrderCreate(BaseModel):
    product_id: int  # ID of the product being ordered
    quantity: int  # Quantity of the product
    shipping_address: constr(min_length=5, max_length=255)  # Shipping address for the order
    special_instructions: Optional[constr(max_length=500)] = None  # Optional special instructions for the order

class OrderUpdate(BaseModel):
    quantity: Optional[int]  # Optional field to update the quantity
    shipping_address: Optional[constr(min_length=5, max_length=255)]  # Optional field to update the shipping address
    special_instructions: Optional[constr(max_length=500)] = None  # Optional field to update special instructions

class OrderResponse(BaseModel):
    id: int  # Unique identifier for the order
    product_id: int  # ID of the product being ordered
    quantity: int  # Quantity of the product
    shipping_address: str  # Shipping address for the order
    special_instructions: Optional[str] = None  # Optional special instructions for the order
    status: str  # Status of the order (e.g., pending, completed)

    class Config:
        orm_mode = True  # This allows Pydantic to work with ORM models