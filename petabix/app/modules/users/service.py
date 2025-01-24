# from pony.orm import db_session
# from models.user import User
# from schemas.user import UserCreate, UserUpdate
# from fastapi import HTTPException
# from core.security import get_password_hash

# class UserService:
#     @db_session
#     async def create_user(self, user: UserCreate):
#         existing_user = User.get(username=user.username) or User.get(email=user.email)
#         if existing_user:
#             raise HTTPException(status_code=400, detail="Username or email already registered")
        
#         hashed_password = get_password_hash(user.password)
#         new_user = User(
#             username=user.username,
#             email=user.email,
#             hashed_password=hashed_password
#         )
#         return new_user

#     @db_session
#     async def get_user(self, user_id: int):
#         user = User.get(id=user_id)
#         if not user:
#             raise HTTPException(status_code=404, detail="User not found")
#         return user

#     @db_session
#     async def update_user(self, user_id: int, user_data: UserUpdate):
#         user = User.get(id=user_id)
#         if not user:
#             raise HTTPException(status_code=404, detail="User not found")
        
#         if user_data.username:
#             existing_user = User.get(username=user_data.username)
#             if existing_user and existing_user.id != user_id:
#                 raise HTTPException(status_code=400, detail="Username already taken")
#             user.username = user_data.username
        
#         if user_data.email:
#             existing_user = User.get(email=user_data.email)
#             if existing_user and existing_user.id != user_id:
#                 raise HTTPException(status_code=400, detail="Email already registered")
#             user.email = user_data.email
        
#         if user_data.password:
#             user.hashed_password = get_password_hash(user_data.password)
        
#         return user

#     @db_session
#     async def delete_user(self, user_id: int):
#         user = User.get(id=user_id)
#         if not user:
#             raise HTTPException(status_code=404, detail="User not found")
        
#         user.delete()
#         return {"message": "User deleted successfully"}