from pony.orm import db_session
from models.vendor import Vendor
from schemas.vendor import VendorCreate, VendorUpdate
from core.security import get_password_hash, verify_password, create_access_token
from fastapi import HTTPException

class VendorService:
    @db_session
    async def register_vendor(self, vendor: VendorCreate):
        existing_vendor = Vendor.get(username=vendor.username)
        if existing_vendor:
            raise HTTPException(status_code=400, detail="Username already registered")
        
        hashed_password = get_password_hash(vendor.password)
        new_vendor = Vendor(
            username=vendor.username,
            hashed_password=hashed_password,
            email=vendor.email,
            company_name=vendor.company_name,
            business_type=vendor.business_type
        )
        return new_vendor

    @db_session
    async def login_vendor(self, username: str, password: str):
        vendor = Vendor.get(username=username)
        if not vendor or not verify_password(password, vendor.hashed_password):
            raise HTTPException(status_code=400, detail="Incorrect username or password")
        
        access_token = create_access_token(data={"sub": vendor.username})
        return {"access_token": access_token, "token_type": "bearer"}

    @db_session
    async def get_vendor_profile(self, current_user: dict):
        vendor = Vendor.get(username=current_user['sub'])
        if not vendor:
            raise HTTPException(status_code=404, detail="Vendor not found")
        return vendor

    @db_session
    async def update_vendor_profile(self, vendor_data: VendorUpdate, current_user: dict):
        vendor = Vendor.get(username=current_user['sub'])
        if not vendor:
            raise HTTPException(status_code=404, detail="Vendor not found")
        
        vendor.email = vendor_data.email
        vendor.company_name = vendor_data.company_name
        vendor.business_type = vendor_data.business_type
        return vendor
