from fastapi import APIRouter, Depends, HTTPException
from typing import List
from .service import VendorService
from schemas.vendor import VendorCreate, VendorUpdate, VendorResponse
from core.auth import get_current_user

router = APIRouter()

@router.post("/register", response_model=VendorResponse)
async def register_vendor(
    vendor: VendorCreate,
    service: VendorService = Depends()
):
    return await service.register_vendor(vendor)

@router.post("/login")
async def login_vendor(
    username: str,
    password: str,
    service: VendorService = Depends()
):
    return await service.login_vendor(username, password)

@router.get("/profile", response_model=VendorResponse)
async def get_vendor_profile(
    current_user: dict = Depends(get_current_user),
    service: VendorService = Depends()
):
    return await service.get_vendor_profile(current_user)

@router.put("/profile", response_model=VendorResponse)
async def update_vendor_profile(
    vendor: VendorUpdate,
    current_user: dict = Depends(get_current_user),
    service: VendorService = Depends()
):
    return await service.update_vendor_profile(vendor, current_user)
