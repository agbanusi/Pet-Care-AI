from pydantic import BaseModel, constr
from typing import Optional

class CardCreate(BaseModel):
    card_number: constr(min_length=16, max_length=16)  # Card number (16 digits)
    cardholder_name: constr(min_length=1, max_length=100)  # Name of the cardholder
    expiration_date: constr(min_length=5, max_length=5) #constr(regex=r'^(0[1-9]|1[0-2])/[0-9]{2}$')  # Expiration date in MM/YY format
    cvv: constr(min_length=3, max_length=4)  # CVV code (3 or 4 digits)
    billing_address: constr(min_length=5, max_length=255)  # Billing address for the card

class CardUpdate(BaseModel):
    card_number: Optional[constr(min_length=16, max_length=16)]  # Optional field to update card number
    cardholder_name: Optional[constr(min_length=1, max_length=100)]  # Optional field to update cardholder name
    expiration_date: constr(min_length=5, max_length=5) #constr(regex=r'^(0[1-9]|1[0-2])/[0-9]{2}$')
    cvv: Optional[constr(min_length=3, max_length=4)]  # Optional field to update CVV
    billing_address: Optional[constr(min_length=5, max_length=255)]  # Optional field to update billing address

class CardResponse(BaseModel):
    id: int  # Unique identifier for the card
    card_number: str  # Card number (masked or unmasked based on your requirements)
    cardholder_name: str  # Name of the cardholder
    expiration_date: str  # Expiration date in MM/YY format
    billing_address: str  # Billing address for the card
    status: str  # Status of the card (e.g., active, inactive)

    class Config:
        orm_mode = True  # This allows Pydantic to work with ORM models