from pony.orm import db_session
from models.customer import Customer
from schemas.customer import CustomerCreate, CustomerUpdate
from core.security import get_password_hash, verify_password, create_access_token
from fastapi import HTTPException

class CustomerService:
    @db_session
    async def register_customer(self, customer: CustomerCreate):
        existing_customer = Customer.get(username=customer.username)
        if existing_customer:
            raise HTTPException(status_code=400, detail="Username already registered")
        
        hashed_password = get_password_hash(customer.password)
        new_customer = Customer(username=customer.username, hashed_password=hashed_password, email=customer.email)
        return new_customer

    @db_session
    async def login_customer(self, username: str, password: str):
        customer = Customer.get(username=username)
        if not customer or not verify_password(password, customer.hashed_password):
            raise HTTPException(status_code=400, detail="Incorrect username or password")
        
        access_token = create_access_token(data={"sub": customer.username})
        return {"access_token": access_token, "token_type": "bearer"}

    @db_session
    async def get_customer_profile(self, current_user: dict):
        customer = Customer.get(username=current_user['sub'])
        if not customer:
            raise HTTPException(status_code=404, detail="Customer not found")
        return customer

    @db_session
    async def update_customer_profile(self, customer_data: CustomerUpdate, current_user: dict):
        customer = Customer.get(username=current_user['sub'])
        if not customer:
            raise HTTPException(status_code=404, detail="Customer not found")
        
        customer.email = customer_data.email
        customer.phone = customer_data.phone
        return customer