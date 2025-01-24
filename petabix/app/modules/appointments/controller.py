from fastapi import APIRouter, Depends, HTTPException
from typing import List
from .service import AppointmentService
from schemas.appointment import AppointmentCreate, AppointmentUpdate, AppointmentResponse
from core.auth import get_current_user

router = APIRouter()

@router.post("/", response_model=AppointmentResponse)
async def create_appointment(
    appointment: AppointmentCreate,
    current_user: dict = Depends(get_current_user),
    service: AppointmentService = Depends()
):
    return await service.create_appointment(appointment, current_user)

@router.get("/{appointment_id}", response_model=AppointmentResponse)
async def get_appointment(
    appointment_id: int,
    current_user: dict = Depends(get_current_user),
    service: AppointmentService = Depends()
):
    return await service.get_appointment(appointment_id, current_user)

@router.get("/", response_model=List[AppointmentResponse])
async def list_appointments(
    current_user: dict = Depends(get_current_user),
    service: AppointmentService = Depends()
):
    return await service.list_appointments(current_user)

@router.put("/{appointment_id}", response_model=AppointmentResponse)
async def update_appointment(
    appointment_id: int,
    appointment: AppointmentUpdate,
    current_user: dict = Depends(get_current_user),
    service: AppointmentService = Depends()
):
    return await service.update_appointment(appointment_id, appointment, current_user)

@router.delete("/{appointment_id}", response_model=bool)
async def delete_appointment(
    appointment_id: int,
    current_user: dict = Depends(get_current_user),
    service: AppointmentService = Depends()
):
    return await service.delete_appointment(appointment_id, current_user)
