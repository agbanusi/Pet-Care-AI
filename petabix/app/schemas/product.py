from pydantic import BaseModel, constr, condecimal
from typing import Optional

class ProductCreate(BaseModel):
    name: constr(min_length=1, max_length=100)  # Name of the product
    description: Optional[constr(max_length=500)] = None  # Optional description of the product
    price: condecimal(gt=0)  # Price of the product, must be greater than 0
    stock: int  # Quantity of the product in stock
    category_id: int  # ID of the category the product belongs to

class ProductUpdate(BaseModel):
    name: Optional[constr(min_length=1, max_length=100)]  # Optional field to update the product name
    description: Optional[constr(max_length=500)] = None  # Optional field to update the description
    price: Optional[condecimal(gt=0)]  # Optional field to update the price
    stock: Optional[int]  # Optional field to update the stock quantity
    category_id: Optional[int]  # Optional field to update the category ID

class ProductResponse(BaseModel):
    id: int  # Unique identifier for the product
    name: str  # Name of the product
    description: Optional[str] = None  # Description of the product
    price: float  # Price of the product
    stock: int  # Quantity of the product in stock
    category_id: int  # ID of the category the product belongs to

    class Config:
        orm_mode = True  # This allows Pydantic to work with ORM models