from pydantic import BaseModel, constr
from typing import Optional
from datetime import datetime

class AppointmentCreate(BaseModel):
    date: datetime  # Date and time of the appointment
    location_id: int  # ID of the location for the appointment
    veterinarian_id: int  # ID of the veterinarian for the appointment
    notes: Optional[constr(max_length=500)] = None  # Optional notes for the appointment

class AppointmentUpdate(BaseModel):
    date: Optional[datetime]  # Optional field to update the date and time
    location_id: Optional[int]  # Optional field to update the location ID
    veterinarian_id: Optional[int]  # Optional field to update the veterinarian ID
    notes: Optional[constr(max_length=500)] = None  # Optional field to update notes

class AppointmentResponse(BaseModel):
    id: int  # Unique identifier for the appointment
    date: datetime  # Date and time of the appointment
    location_id: int  # ID of the location for the appointment
    veterinarian_id: int  # ID of the veterinarian for the appointment
    notes: Optional[str] = None  # Optional notes for the appointment
    status: str  # Status of the appointment (e.g., scheduled, completed, canceled)

    class Config:
        orm_mode = True  # This allows Pydantic to work with ORM models