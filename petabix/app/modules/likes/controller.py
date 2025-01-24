from fastapi import APIRouter, Depends, HTTPException
from typing import List
from .service import LikeService
from schemas.like import LikeCreate, LikeResponse
from core.auth import get_current_user

router = APIRouter()

@router.post("/", response_model=LikeResponse)
async def create_like(
    like: LikeCreate,
    current_user: dict = Depends(get_current_user),
    service: LikeService = Depends()
):
    return await service.create_like(like, current_user)

@router.get("/post/{post_id}", response_model=List[LikeResponse])
async def get_likes_for_post(
    post_id: int,
    service: LikeService = Depends()
):
    return await service.get_likes_for_post(post_id)

@router.delete("/{post_id}", response_model=bool)
async def remove_like(
    post_id: int,
    current_user: dict = Depends(get_current_user),
    service: LikeService = Depends()
):
    return await service.remove_like(post_id, current_user)
