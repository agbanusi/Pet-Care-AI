from fastapi import APIRouter, Depends, HTTPException
from typing import List
from .service import CommentService
from schemas.comment import CommentCreate, CommentUpdate, CommentResponse
from core.auth import get_current_user

router = APIRouter()

@router.post("/", response_model=CommentResponse)
async def create_comment(
    comment: CommentCreate,
    current_user: dict = Depends(get_current_user),
    service: CommentService = Depends()
):
    return await service.create_comment(comment, current_user)

@router.get("/{comment_id}", response_model=CommentResponse)
async def get_comment(
    comment_id: int,
    service: CommentService = Depends()
):
    return await service.get_comment(comment_id)

@router.get("/post/{post_id}", response_model=List[CommentResponse])
async def get_comments_for_post(
    post_id: int,
    service: CommentService = Depends()
):
    return await service.get_comments_for_post(post_id)

@router.put("/{comment_id}", response_model=CommentResponse)
async def update_comment(
    comment_id: int,
    comment: CommentUpdate,
    current_user: dict = Depends(get_current_user),
    service: CommentService = Depends()
):
    return await service.update_comment(comment_id, comment, current_user)

@router.delete("/{comment_id}", response_model=bool)
async def delete_comment(
    comment_id: int,
    current_user: dict = Depends(get_current_user),
    service: CommentService = Depends()
):
    return await service.delete_comment(comment_id, current_user)
