# user_management_service/app/routes/profile_routes.py

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user_profile import UserProfile as UserProfileModel
from app.schemas.user_profile_schema import UserProfileCreate, UserProfileUpdate, UserProfile
from app.services.profile_service import ProfileService

router = APIRouter()

@router.post("/profile/", response_model=UserProfile)
def create_user_profile(
    user_id: int,
    profile: UserProfileCreate, 
    db: Session = Depends(get_db)
):
    db_profile = db.query(UserProfileModel).filter(UserProfileModel.user_id == user_id).first()
    if db_profile:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User profile already exists")
    
    new_profile = UserProfileModel(user_id=user_id, **profile.dict())
    db.add(new_profile)
    db.commit()
    db.refresh(new_profile)
    return new_profile

@router.get("/profile/", response_model=UserProfile)
def get_profile(user_id: int, db: Session = Depends(get_db)):
    db_user_profile = ProfileService.get_user_profile(db=db, user_id=user_id)
    if db_user_profile is None:
        raise HTTPException(status_code=404, detail="User profile not found")
    return db_user_profile

@router.put("/profile/{user_id}/", response_model=UserProfile)
def update_profile(
    user_id: int,
    user_profile: UserProfileUpdate, 
    db: Session = Depends(get_db),
):
    db_user_profile = ProfileService.update_user_profile(db=db, user_id=user_id, user_profile=user_profile)
    if db_user_profile is None:
        raise HTTPException(status_code=404, detail="User profile not found")
    return db_user_profile
