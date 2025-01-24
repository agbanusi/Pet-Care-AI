from fastapi import APIRouter, Depends, HTTPException
from typing import List
from .service import PostService
from schemas.post import PostCreate, PostUpdate, PostResponse
from core.auth import get_current_user

router = APIRouter()

@router.post("/", response_model=PostResponse)
async def create_post(
    post: PostCreate,
    current_user: dict = Depends(get_current_user),
    service: PostService = Depends()
):
    return await service.create_post(post, current_user)

@router.get("/{post_id}", response_model=PostResponse)
async def get_post(
    post_id: int,
    service: PostService = Depends()
):
    return await service.get_post(post_id)

@router.get("/", response_model=List[PostResponse])
async def list_posts(
    skip: int = 0,
    limit: int = 100,
    service: PostService = Depends()
):
    return await service.list_posts(skip, limit)

@router.put("/{post_id}", response_model=PostResponse)
async def update_post(
    post_id: int,
    post: PostUpdate,
    current_user: dict = Depends(get_current_user),
    service: PostService = Depends()
):
    return await service.update_post(post_id, post, current_user)

@router.delete("/{post_id}", response_model=bool)
async def delete_post(
    post_id: int,
    current_user: dict = Depends(get_current_user),
    service: PostService = Depends()
):
    return await service.delete_post(post_id, current_user)
