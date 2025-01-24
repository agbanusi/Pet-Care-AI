from pydantic import BaseModel, constr
from typing import Optional
from datetime import datetime

class CommentCreate(BaseModel):
    post_id: int  # ID of the post the comment is associated with
    content: constr(min_length=1, max_length=500)  # Content of the comment

class CommentUpdate(BaseModel):
    content: Optional[constr(min_length=1, max_length=500)]  # Optional field to update the content

class CommentResponse(BaseModel):
    id: int  # Unique identifier for the comment
    post_id: int  # ID of the post the comment is associated with
    content: str  # Content of the comment
    created_at: datetime  # Timestamp of when the comment was created
    updated_at: Optional[datetime] = None  # Timestamp of when the comment was last updated

    class Config:
        orm_mode = True  # This allows Pydantic to work with ORM models