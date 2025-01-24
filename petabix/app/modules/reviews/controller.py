from fastapi import APIRouter, Depends, HTTPException
from typing import List
from .service import ReviewService
from schemas.review import ReviewCreate, ReviewUpdate, ReviewResponse
from core.auth import get_current_user

router = APIRouter()

@router.post("/", response_model=ReviewResponse)
async def create_review(
    review: ReviewCreate,
    current_user: dict = Depends(get_current_user),
    service: ReviewService = Depends()
):
    return await service.create_review(review, current_user)

@router.get("/{review_id}", response_model=ReviewResponse)
async def get_review(
    review_id: int,
    service: ReviewService = Depends()
):
    return await service.get_review(review_id)

@router.get("/product/{product_id}", response_model=List[ReviewResponse])
async def get_reviews_for_product(
    product_id: int,
    service: ReviewService = Depends()
):
    return await service.get_reviews_for_product(product_id)

@router.put("/{review_id}", response_model=ReviewResponse)
async def update_review(
    review_id: int,
    review: ReviewUpdate,
    current_user: dict = Depends(get_current_user),
    service: ReviewService = Depends()
):
    return await service.update_review(review_id, review, current_user)

@router.delete("/{review_id}", response_model=bool)
async def delete_review(
    review_id: int,
    current_user: dict = Depends(get_current_user),
    service: ReviewService = Depends()
):
    return await service.delete_review(review_id, current_user)
