from fastapi import APIRouter, Depends
from typing import List
from .service import StateService
from schemas.state import StateResponse

router = APIRouter()

@router.get("/", response_model=List[StateResponse])
async def list_states(
    country_id: int,
    service: StateService = Depends()
):
    return await service.list_states(country_id)

@router.get("/{state_id}", response_model=StateResponse)
async def get_state(
    state_id: int,
    service: StateService = Depends()
):
    return await service.get_state(state_id)