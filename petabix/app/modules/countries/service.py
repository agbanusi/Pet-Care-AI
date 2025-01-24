from pony.orm import db_session
from models.country import Country
from fastapi import HTTPException

class CountryService:
    @db_session
    async def list_countries(self):
        return list(Country.select())

    @db_session
    async def get_country(self, country_id: int):
        country = Country.get(id=country_id)
        if not country:
            raise HTTPException(status_code=404, detail="Country not found")
        return country