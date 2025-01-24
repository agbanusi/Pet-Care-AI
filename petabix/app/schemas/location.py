from pydantic import BaseModel, constr
from typing import Optional

class LocationCreate(BaseModel):
    name: constr(min_length=1, max_length=100)  # Name of the location
    address: constr(min_length=5, max_length=255)  # Address of the location
    latitude: float  # Latitude coordinate
    longitude: float  # Longitude coordinate
    description: Optional[constr(max_length=500)] = None  # Optional description of the location

class LocationUpdate(BaseModel):
    name: Optional[constr(min_length=1, max_length=100)]  # Optional field
    address: Optional[constr(min_length=5, max_length=255)]  # Optional field
    latitude: Optional[float]  # Optional field
    longitude: Optional[float]  # Optional field
    description: Optional[constr(max_length=500)] = None  # Optional field

class LocationResponse(BaseModel):
    id: int  # Unique identifier for the location
    name: str  # Name of the location
    address: str  # Address of the location
    latitude: float  # Latitude coordinate
    longitude: float  # Longitude coordinate
    description: Optional[str] = None  # Optional description of the location

    class Config:
        orm_mode = True  # This allows Pydantic to work with ORM models