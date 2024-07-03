# auth_service/app/services/auth_service.py
from sqlalchemy.orm import Session
from jose import JWTError, jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta
from app.models import user
from app.schemas import auth_schema
from typing import Optional
from app.utils.jwt_handler import create_access_token

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class AuthService:

    @staticmethod
    def get_user_by_email(db: Session, email: str):
        return db.query(user.User).filter(user.User.email == email).first()
    
    @staticmethod
    def create_user(db: Session, user: auth_schema.UserCreate):
        hashed_password = pwd_context.hash(user.password)
        db_user = user.User(email=user.email, username=user.username, hashed_password=hashed_password)
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
    
    @staticmethod
    def authenticate_user(db: Session, email: str, password: str):
        db_user = AuthService.get_user_by_email(db, email=email)
        if not db_user or not pwd_context.verify(password, db_user.hashed_password):
            return None
        return db_user
    
    @staticmethod
    def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
        return create_access_token(data, expires_delta)