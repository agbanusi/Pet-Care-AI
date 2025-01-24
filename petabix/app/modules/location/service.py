from pony.orm import db_session
from models.location import Location
from schemas.location import LocationCreate, LocationUpdate
from fastapi import HTTPException

class LocationService:
    @db_session
    async def create_location(self, location: LocationCreate, current_user: dict):
        new_location = Location(
            name=location.name,
            address=location.address,
            latitude=location.latitude,
            longitude=location.longitude,
            user_id=current_user['id']
        )
        return new_location

    @db_session
    async def get_location(self, location_id: int, current_user: dict):
        location = Location.get(id=location_id, user_id=current_user['id'])
        if not location:
            raise HTTPException(status_code=404, detail="Location not found")
        return location

    @db_session
    async def update_location(self, location_id: int, location_data: LocationUpdate, current_user: dict):
        location = Location.get(id=location_id, user_id=current_user['id'])
        if not location:
            raise HTTPException(status_code=404, detail="Location not found")
        
        location.name = location_data.name
        location.address = location_data.address
        location.latitude = location_data.latitude
        location.longitude = location_data.longitude
        return location

    @db_session
    async def delete_location(self, location_id: int, current_user: dict):
        location = Location.get(id=location_id, user_id=current_user['id'])
        if not location:
            raise HTTPException(status_code=404, detail="Location not found")
        
        deleted_location = location.to_dict()
        location.delete()
        return deleted_location