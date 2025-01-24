from fastapi import APIRouter, Depends, HTTPException
from typing import List
from .service import VeterinarianService
from schemas.veterinarian import VeterinarianCreate, VeterinarianUpdate, VeterinarianResponse
from core.auth import get_current_user

router = APIRouter()

@router.post("/register", response_model=VeterinarianResponse)
async def register_veterinarian(
    vet: VeterinarianCreate,
    service: VeterinarianService = Depends()
):
    return await service.register_veterinarian(vet)

@router.post("/login")
async def login_veterinarian(
    username: str,
    password: str,
    service: VeterinarianService = Depends()
):
    return await service.login_veterinarian(username, password)

@router.get("/profile", response_model=VeterinarianResponse)
async def get_veterinarian_profile(
    current_user: dict = Depends(get_current_user),
    service: VeterinarianService = Depends()
):
    return await service.get_veterinarian_profile(current_user)

@router.put("/profile", response_model=VeterinarianResponse)
async def update_veterinarian_profile(
    vet: VeterinarianUpdate,
    current_user: dict = Depends(get_current_user),
    service: VeterinarianService = Depends()
):
    return await service.update_veterinarian_profile(vet, current_user)
