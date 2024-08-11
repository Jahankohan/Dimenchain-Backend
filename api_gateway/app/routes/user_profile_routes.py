# api_gateway/app/routes/user_profile_routes.py

from fastapi import APIRouter, HTTPException, Depends, Request, status
import requests
from app.config import USER_MANAGEMENT_SERVICE_URL
from app.schemas import user_profile_schema
from shared.auth.dependencies import get_current_user

router = APIRouter()

@router.post("/profile/", response_model=user_profile_schema.UserProfile)
def create_user_profile(
    profile: user_profile_schema.UserProfileCreate, 
    user_id: str = Depends(get_current_user)
):
    
    response = requests.post(f"{USER_MANAGEMENT_SERVICE_URL}/profile/", json=profile.dict(), params={"user_id": user_id})
    
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=response.json())
    
    return response.json()

@router.get("/profile/", response_model=user_profile_schema.UserProfile)
def get_profile(user_id: int = Depends(get_current_user)):
    
    response = requests.get(f"{USER_MANAGEMENT_SERVICE_URL}/profile/", params={"user_id": user_id})
    
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=response.json())
    
    return response.json()

@router.put("/profile/", response_model=user_profile_schema.UserProfile)
def update_profile(
    user_profile: user_profile_schema.UserProfileUpdate, 
    user_id: int = Depends(get_current_user)
):
    
    response = requests.put(f"{USER_MANAGEMENT_SERVICE_URL}/profile/{user_id}", json=user_profile.dict())
    
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=response.json())
    
    return response.json()
