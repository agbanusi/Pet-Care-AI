from pony.orm import db_session
from models.rider import Rider
from schemas.rider import RiderCreate, RiderUpdate
from core.security import get_password_hash, verify_password, create_access_token
from fastapi import HTTPException

class RiderService:
    @db_session
    async def register_rider(self, rider: RiderCreate):
        existing_rider = Rider.get(username=rider.username)
        if existing_rider:
            raise HTTPException(status_code=400, detail="Username already registered")
        
        hashed_password = get_password_hash(rider.password)
        new_rider = Rider(username=rider.username, hashed_password=hashed_password, email=rider.email)
        return new_rider

    @db_session
    async def login_rider(self, username: str, password: str):
        rider = Rider.get(username=username)
        if not rider or not verify_password(password, rider.hashed_password):
            raise HTTPException(status_code=400, detail="Incorrect username or password")
        
        access_token = create_access_token(data={"sub": rider.username})
        return {"access_token": access_token, "token_type": "bearer"}

    @db_session
    async def get_rider_profile(self, current_user: dict):
        rider = Rider.get(username=current_user['sub'])
        if not rider:
            raise HTTPException(status_code=404, detail="Rider not found")
        return rider

    @db_session
    async def update_rider_profile(self, rider_data: RiderUpdate, current_user: dict):
        rider = Rider.get(username=current_user['sub'])
        if not rider:
            raise HTTPException(status_code=404, detail="Rider not found")
        
        rider.email = rider_data.email
        rider.phone = rider_data.phone
        rider.vehicle_type = rider_data.vehicle_type
        return rider