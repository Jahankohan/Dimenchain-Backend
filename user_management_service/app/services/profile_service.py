# user_management_service/app/services/profile_service.py

from sqlalchemy.orm import Session
from app.models.user_profile import UserProfile
from app.schemas.user_profile_schema import UserProfileCreate, UserProfileUpdate

class ProfileService:

    @staticmethod
    def create_user_profile(db: Session, user_profile: UserProfileCreate):
        db_user_profile = UserProfile(**user_profile.dict())
        db.add(db_user_profile)
        db.commit()
        db.refresh(db_user_profile)
        return db_user_profile

    @staticmethod
    def get_user_profile(db: Session, user_id: int):
        return db.query(UserProfile).filter(UserProfile.user_id == user_id).first()

    @staticmethod
    def update_user_profile(db: Session, user_id: int, user_profile: UserProfileUpdate):
        db_user_profile = db.query(UserProfile).filter(UserProfile.user_id == user_id).first()
        if db_user_profile:
            for key, value in user_profile.dict(exclude_unset=True).items():
                setattr(db_user_profile, key, value)
            db.commit()
            db.refresh(db_user_profile)
        return db_user_profile
