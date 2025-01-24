# from fastapi import APIRouter, Depends, HTTPException
# from typing import List
# from .service import UserService
# from schemas.user import UserCreate, UserUpdate, UserResponse
# from core.auth import get_current_user

# router = APIRouter()

# @router.post("/", response_model=UserResponse)
# async def create_user(
#     user: UserCreate,
#     service: UserService = Depends()
# ):
#     return await service.create_user(user)

# @router.get("/me", response_model=UserResponse)
# async def get_current_user_info(
#     current_user: dict = Depends(get_current_user),
#     service: UserService = Depends()
# ):
#     return await service.get_user(current_user['id'])

# @router.put("/me", response_model=UserResponse)
# async def update_current_user(
#     user: UserUpdate,
#     current_user: dict = Depends(get_current_user),
#     service: UserService = Depends()
# ):
#     return await service.update_user(current_user['id'], user)

# @router.delete("/me", response_model=bool)
# async def delete_current_user(
#     current_user: dict = Depends(get_current_user),
#     service: UserService = Depends()
# ):
#     return await service.delete_user(current_user['id'])
