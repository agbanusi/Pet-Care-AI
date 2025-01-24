from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from pony.orm import Database, Required, Set, PrimaryKey
from jose import JWTError, jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta
from fastapi import FastAPI
from core.config import settings
import uvicorn
# from modules.users.controller import router as user_router
from modules.customer.controller import router as customer_router
from modules.location.controller import router as location_router
from modules.rider.controller import router as rider_router
from modules.veterinarian.controller import router as vet_router
from modules.transactions.controller import router as transaction_router
from modules.vendor.controller import router as vendor_router
from modules.wallet.controller import router as wallet_router
from modules.appointments.controller import router as appointment_router
from modules.cards.controller import router as card_router
from modules.carts.controller import router as cart_router
from modules.chats.controller import router as chat_router
from modules.comments.controller import router as comment_router
from modules.countries.controller import router as country_router
from modules.likes.controller import router as likes_router
from modules.order.controller import router as order_router
from modules.posts.controller import router as post_router
from modules.products.controller import router as product_router
from modules.reviews.controller import router as review_router
from modules.states.controller import router as state_router



app = FastAPI(title=settings.APP_NAME)

# Database setup
db = Database()
# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# OAuth2 scheme
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Middleware
@app.middleware("http")
async def verify_token(request, call_next):
    token = request.headers.get("Authorization")
    if token:
        token = token.split(" ")[1]
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
            request.state.current_user = payload.get("sub")
        except JWTError:
            raise HTTPException(status_code=401, detail="Invalid token")
    response = await call_next(request)
    return response

# Include all routers
# app.include_router(user_router, prefix=f"{settings.API_V1_STR}/users", tags=["users"])
app.include_router(customer_router, prefix=f"{settings.API_V1_STR}/customers", tags=["customers"])
app.include_router(location_router, prefix=f"{settings.API_V1_STR}/locations", tags=["locations"])
app.include_router(rider_router, prefix=f"{settings.API_V1_STR}/riders", tags=["riders"])
app.include_router(vet_router, prefix=f"{settings.API_V1_STR}/veterinarians", tags=["veterinarians"])
app.include_router(transaction_router, prefix=f"{settings.API_V1_STR}/transactions", tags=["transactions"])
app.include_router(vendor_router, prefix=f"{settings.API_V1_STR}/vendors", tags=["vendors"])
app.include_router(wallet_router, prefix=f"{settings.API_V1_STR}/wallets", tags=["wallets"])
app.include_router(order_router, prefix=f"{settings.API_V1_STR}/orders", tags=["orders"])
app.include_router(appointment_router, prefix=f"{settings.API_V1_STR}/appointments", tags=["appointments"])
app.include_router(card_router, prefix=f"{settings.API_V1_STR}/card", tags=["card"])
app.include_router(cart_router, prefix=f"{settings.API_V1_STR}/cart", tags=["cart"])
app.include_router(chat_router, prefix=f"{settings.API_V1_STR}/chat", tags=["chat"])
app.include_router(comment_router, prefix=f"{settings.API_V1_STR}/comment", tags=["comment"])
app.include_router(country_router, prefix=f"{settings.API_V1_STR}/country", tags=["country"])
app.include_router(likes_router, prefix=f"{settings.API_V1_STR}/likes", tags=["likes"])
app.include_router(post_router, prefix=f"{settings.API_V1_STR}/posts", tags=["posts"])
app.include_router(product_router, prefix=f"{settings.API_V1_STR}/products", tags=["products"])
app.include_router(review_router, prefix=f"{settings.API_V1_STR}/reviews", tags=["reviews"])
app.include_router(state_router, prefix=f"{settings.API_V1_STR}/state", tags=["state"])



@app.get("/")
async def root():
    return {"message": "Welcome to the Pet Care App API"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)


# TODO:
# add schemas for all models - 
# speech to speech with open ai
# speech to text and viceversa
# img interpretation
# daily feeding and training plan in calendar
# subscription to vendors and veterinarians ( pay weekly/monthly with rollover and buy any items you wish with overdraft)
# pay small small with trust scores
# AI vet booking for cheapest vet
# mobile app focus