# user_management_service/app/schemas/user_profile_schema.py

from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class UserProfileBase(BaseModel):
    first_name: str
    last_name: str
    bio: Optional[str] = None
    profile_picture: Optional[str] = None
    user_type: str  # 'trader' or 'investor'

class UserProfileCreate(UserProfileBase):
    pass

class UserProfileUpdate(UserProfileBase):
    pass

class UserProfile(UserProfileBase):
    user_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        orm_mode = True
