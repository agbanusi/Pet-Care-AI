from fastapi import APIRouter, Depends, HTTPException
from typing import List
from .service import LocationService
from schemas.location import LocationCreate, LocationUpdate, LocationResponse
from core.auth import get_current_user

router = APIRouter()

@router.post("/", response_model=LocationResponse)
async def create_location(
    location: LocationCreate,
    current_user: dict = Depends(get_current_user),
    service: LocationService = Depends()
):
    return await service.create_location(location, current_user)

@router.get("/{location_id}", response_model=LocationResponse)
async def get_location(
    location_id: int,
    current_user: dict = Depends(get_current_user),
    service: LocationService = Depends()
):
    return await service.get_location(location_id, current_user)

@router.put("/{location_id}", response_model=LocationResponse)
async def update_location(
    location_id: int,
    location: LocationUpdate,
    current_user: dict = Depends(get_current_user),
    service: LocationService = Depends()
):
    return await service.update_location(location_id, location, current_user)

@router.delete("/{location_id}", response_model=LocationResponse)
async def delete_location(
    location_id: int,
    current_user: dict = Depends(get_current_user),
    service: LocationService = Depends()
):
    return await service.delete_location(location_id, current_user)