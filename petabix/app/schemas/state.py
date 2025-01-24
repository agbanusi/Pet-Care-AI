from pydantic import BaseModel, constr
from typing import Optional

class StateCreate(BaseModel):
    name: constr(min_length=1, max_length=100)  # Name of the state
    country_id: int  # ID of the country the state belongs to

class StateUpdate(BaseModel):
    name: Optional[constr(min_length=1, max_length=100)]  # Optional field to update the state name
    country_id: Optional[int]  # Optional field to update the country ID

class StateResponse(BaseModel):
    id: int  # Unique identifier for the state
    name: str  # Name of the state
    country_id: int  # ID of the country the state belongs to

    class Config:
        orm_mode = True  # This allows Pydantic to work with ORM models