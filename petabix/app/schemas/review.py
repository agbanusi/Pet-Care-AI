from pydantic import BaseModel, constr
from typing import Optional
from datetime import datetime

class ReviewCreate(BaseModel):
    product_id: int  # ID of the product being reviewed
    rating: int  # Rating given by the user (e.g., 1 to 5)
    content: constr(min_length=1, max_length=1000)  # Content of the review

class ReviewUpdate(BaseModel):
    rating: Optional[int]  # Optional field to update the rating
    content: Optional[constr(min_length=1, max_length=1000)]  # Optional field to update the content

class ReviewResponse(BaseModel):
    id: int  # Unique identifier for the review
    product_id: int  # ID of the product being reviewed
    rating: int  # Rating given by the user
    content: str  # Content of the review
    created_at: datetime  # Timestamp of when the review was created
    updated_at: Optional[datetime] = None  # Timestamp of when the review was last updated

    class Config:
        orm_mode = True  # This allows Pydantic to work with ORM models