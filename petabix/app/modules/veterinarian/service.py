from pony.orm import db_session
from models.veterinarian import Veterinarian
from schemas.veterinarian import VeterinarianCreate, VeterinarianUpdate
from core.security import get_password_hash, verify_password, create_access_token
from fastapi import HTTPException

class VeterinarianService:
    @db_session
    async def register_veterinarian(self, vet: VeterinarianCreate):
        existing_vet = Veterinarian.get(username=vet.username)
        if existing_vet:
            raise HTTPException(status_code=400, detail="Username already registered")
        
        hashed_password = get_password_hash(vet.password)
        new_vet = Veterinarian(
            username=vet.username,
            hashed_password=hashed_password,
            email=vet.email,
            full_name=vet.full_name,
            license_number=vet.license_number,
            specialization=vet.specialization
        )
        return new_vet

    @db_session
    async def login_veterinarian(self, username: str, password: str):
        vet = Veterinarian.get(username=username)
        if not vet or not verify_password(password, vet.hashed_password):
            raise HTTPException(status_code=400, detail="Incorrect username or password")
        
        access_token = create_access_token(data={"sub": vet.username})
        return {"access_token": access_token, "token_type": "bearer"}

    @db_session
    async def get_veterinarian_profile(self, current_user: dict):
        vet = Veterinarian.get(username=current_user['sub'])
        if not vet:
            raise HTTPException(status_code=404, detail="Veterinarian not found")
        return vet

    @db_session
    async def update_veterinarian_profile(self, vet_data: VeterinarianUpdate, current_user: dict):
        vet = Veterinarian.get(username=current_user['sub'])
        if not vet:
            raise HTTPException(status_code=404, detail="Veterinarian not found")
        
        vet.email = vet_data.email
        vet.full_name = vet_data.full_name
        vet.specialization = vet_data.specialization
        return vet