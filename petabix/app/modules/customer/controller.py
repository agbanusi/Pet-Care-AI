from fastapi import APIRouter, Depends, HTTPException
from typing import List
from .service import CustomerService
from schemas.customer import CustomerCreate, CustomerUpdate, CustomerResponse
from core.auth import get_current_user

router = APIRouter()

@router.post("/register", response_model=CustomerResponse)
async def register_customer(
    customer: CustomerCreate,
    service: CustomerService = Depends()
):
    return await service.register_customer(customer)

@router.post("/login")
async def login_customer(
    username: str,
    password: str,
    service: CustomerService = Depends()
):
    return await service.login_customer(username, password)

@router.get("/profile", response_model=CustomerResponse)
async def get_customer_profile(
    current_user: dict = Depends(get_current_user),
    service: CustomerService = Depends()
):
    return await service.get_customer_profile(current_user)

@router.put("/profile", response_model=CustomerResponse)
async def update_customer_profile(
    customer: CustomerUpdate,
    current_user: dict = Depends(get_current_user),
    service: CustomerService = Depends()
):
    return await service.update_customer_profile(customer, current_user)
