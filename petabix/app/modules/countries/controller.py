from fastapi import APIRouter, Depends
from typing import List
from .service import CountryService
from schemas.country import CountryResponse

router = APIRouter()

@router.get("/", response_model=List[CountryResponse])
async def list_countries(
    service: CountryService = Depends()
):
    return await service.list_countries()

@router.get("/{country_id}", response_model=CountryResponse)
async def get_country(
    country_id: int,
    service: CountryService = Depends()
):
    return await service.get_country(country_id)