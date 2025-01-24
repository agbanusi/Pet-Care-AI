from fastapi import APIRouter, Depends, HTTPException
from typing import List
from .service import RiderService
from schemas.rider import RiderCreate, RiderUpdate, RiderResponse
from core.auth import get_current_user

router = APIRouter()

@router.post("/register", response_model=RiderResponse)
async def register_rider(
    rider: RiderCreate,
    service: RiderService = Depends()
):
    return await service.register_rider(rider)

@router.post("/login")
async def login_rider(
    username: str,
    password: str,
    service: RiderService = Depends()
):
    return await service.login_rider(username, password)

@router.get("/profile", response_model=RiderResponse)
async def get_rider_profile(
    current_user: dict = Depends(get_current_user),
    service: RiderService = Depends()
):
    return await service.get_rider_profile(current_user)

@router.put("/profile", response_model=RiderResponse)
async def update_rider_profile(
    rider: RiderUpdate,
    current_user: dict = Depends(get_current_user),
    service: RiderService = Depends()
):
    return await service.update_rider_profile(rider, current_user)