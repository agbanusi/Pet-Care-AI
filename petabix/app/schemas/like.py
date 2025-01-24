from pydantic import BaseModel
from typing import Optional

class LikeCreate(BaseModel):
    post_id: int  # ID of the post being liked

class LikeResponse(BaseModel):
    id: int  # Unique identifier for the like
    post_id: int  # ID of the post that is liked
    user_id: int  # ID of the user who liked the post

    class Config:
        orm_mode = True  # This allows Pydantic to work with ORM models