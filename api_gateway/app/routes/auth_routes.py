# api_gateway/app/routes/auth_routes.py
from fastapi import APIRouter, HTTPException, Depends
from app.schemas import auth_schema
import requests
from app.config import AUTH_SERVICE_URL

router = APIRouter()

@router.post("/register/", response_model=auth_schema.User)
def register_user(user: auth_schema.UserCreate):
    response = requests.post(f"{AUTH_SERVICE_URL}/register/", json=user.dict())
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=response.json())
    return response.json()

@router.post("/login/", response_model=auth_schema.Token)
def login_user(form_data: auth_schema.UserCreate):
    response = requests.post(f"{AUTH_SERVICE_URL}/login/", json=form_data.dict())
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=response.json())
    return response.json()
