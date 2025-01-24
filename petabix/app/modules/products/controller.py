from fastapi import APIRouter, Depends, HTTPException
from typing import List
from .service import ProductService
from schemas.product import ProductCreate, ProductUpdate, ProductResponse
from core.auth import get_current_user

router = APIRouter()

@router.post("/", response_model=ProductResponse)
async def create_product(
    product: ProductCreate,
    current_user: dict = Depends(get_current_user),
    service: ProductService = Depends()
):
    return await service.create_product(product, current_user)

@router.get("/{product_id}", response_model=ProductResponse)
async def get_product(
    product_id: int,
    service: ProductService = Depends()
):
    return await service.get_product(product_id)

@router.get("/", response_model=List[ProductResponse])
async def list_products(
    skip: int = 0,
    limit: int = 100,
    service: ProductService = Depends()
):
    return await service.list_products(skip, limit)

@router.put("/{product_id}", response_model=ProductResponse)
async def update_product(
    product_id: int,
    product: ProductUpdate,
    current_user: dict = Depends(get_current_user),
    service: ProductService = Depends()
):
    return await service.update_product(product_id, product, current_user)

@router.delete("/{product_id}", response_model=bool)
async def delete_product(
    product_id: int,
    current_user: dict = Depends(get_current_user),
    service: ProductService = Depends()
):
    return await service.delete_product(product_id, current_user)
