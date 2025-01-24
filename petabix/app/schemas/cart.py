from pydantic import BaseModel, constr
from typing import List, Optional

class CartItemCreate(BaseModel):
    product_id: int  # ID of the product to add to the cart
    quantity: int  # Quantity of the product to add

class CartItemUpdate(BaseModel):
    quantity: Optional[int]  # Optional field to update the quantity

class CartResponse(BaseModel):
    items: List[dict]  # List of items in the cart, can be a list of dictionaries or a specific item schema
    total_quantity: int  # Total quantity of items in the cart
    total_price: float  # Total price of all items in the cart

    class Config:
        orm_mode = True  # This allows Pydantic to work with ORM models