from pydantic import BaseModel, constr
from typing import Optional
from datetime import datetime

class PostCreate(BaseModel):
    title: constr(min_length=1, max_length=100)  # Title of the post
    content: constr(min_length=1, max_length=5000)  # Content of the post
    tags: Optional[list[str]] = None  # Optional list of tags associated with the post

class PostUpdate(BaseModel):
    title: Optional[constr(min_length=1, max_length=100)]  # Optional field to update the title
    content: Optional[constr(min_length=1, max_length=5000)]  # Optional field to update the content
    tags: Optional[list[str]] = None  # Optional field to update the tags

class PostResponse(BaseModel):
    id: int  # Unique identifier for the post
    title: str  # Title of the post
    content: str  # Content of the post
    tags: Optional[list[str]] = None  # List of tags associated with the post
    created_at: datetime  # Timestamp of when the post was created
    updated_at: Optional[datetime] = None  # Timestamp of when the post was last updated

    class Config:
        orm_mode = True  # This allows Pydantic to work with ORM models