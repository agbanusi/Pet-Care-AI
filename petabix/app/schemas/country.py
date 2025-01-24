from pydantic import BaseModel, constr
from typing import Optional

class CountryCreate(BaseModel):
    name: constr(min_length=1, max_length=100)  # Name of the country
    code: constr(min_length=2, max_length=3)  # Country code (ISO format)

class CountryUpdate(BaseModel):
    name: Optional[constr(min_length=1, max_length=100)]  # Optional field to update the country name
    code: Optional[constr(min_length=2, max_length=3)]  # Optional field to update the country code

class CountryResponse(BaseModel):
    id: int  # Unique identifier for the country
    name: str  # Name of the country
    code: str  # Country code (ISO format)

    class Config:
        orm_mode = True  # This allows Pydantic to work with ORM models