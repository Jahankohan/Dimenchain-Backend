# api_gateway/app/main.py
from fastapi import FastAPI
from app.routes import auth_routes, user_profile_routes

app = FastAPI()

app.include_router(auth_routes.router, prefix="/auth", tags=["auth"])
app.include_router(user_profile_routes.router, prefix="/users", tags=["Users"])
