# auth_service/app/services/auth_service.py
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from app.models.user import User
from app.schemas import auth_schema
from app.utils.jwt_handler import create_access_token, verify_access_token, create_refresh_token, verify_refresh_token
from typing import Optional
from datetime import timedelta
from typing import Optional
import logging
from .send_email import send_email

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
logging.basicConfig(level=logging.DEBUG)

class AuthService:
    @staticmethod
    def get_user_by_email(db: Session, email: str):
        user = db.query(User).filter(User.email == email).first()
        logging.debug(f"Retrieved user: {user}")
        return user
    
    @staticmethod
    def get_user_by_email_or_username(db: Session, identifier: str):
        return db.query(User).filter((User.email == identifier) | (User.username == identifier)).first()

    @staticmethod
    def create_user(db: Session, user: auth_schema.UserCreate):
        hashed_password = pwd_context.hash(user.password)
        logging.debug(f"Hashed password: {hashed_password}")
        db_user = User(email=user.email, username=user.username, hashed_password=hashed_password)
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user

    @staticmethod
    def authenticate_user(db: Session, identifier: str, password: str):
        db_user = AuthService.get_user_by_email_or_username(db, identifier=identifier)
        if not db_user or not pwd_context.verify(password, db_user.hashed_password):
            return None
        return db_user
    
    @staticmethod
    def send_password_reset_email(db: Session, email: str):
        db_user = AuthService.get_user_by_email(db, email=email)
        if not db_user:
            raise None

        reset_token = AuthService.create_access_token(data={"sub": db_user.username, "email": db_user.email})
        body = f"Your password reset token is: {reset_token}"
        send_email(db_user.email, "Hivest Password Reset Token", body)
        return {"message": "Password reset email sent"}

    @staticmethod
    def reset_password(db: Session, token: str, new_password: str):
        payload = AuthService.verify_access_token(token)
        email = payload.get("email")
        if email is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
        
        db_user = AuthService.get_user_by_email(db, email=email)
        if not db_user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        
        hashed_password = pwd_context.hash(new_password)
        db_user.hashed_password = hashed_password
        db.commit()
        return {"message": "Password reset successful"}

    @staticmethod
    def change_password(db: Session, user: User, new_password: str):
        hashed_password = pwd_context.hash(new_password)
        user.hashed_password = hashed_password
        db.commit()
        return {"message": "Password changed successfully"}

    @staticmethod
    def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
        return create_access_token(data, expires_delta)
    
    @staticmethod
    def verify_access_token(token: str):
        return verify_access_token(token=token)
    
    @staticmethod
    def create_refresh_token(data: dict, expires_delta: Optional[timedelta] = None):
        return create_refresh_token(data, expires_delta)

    @staticmethod
    def verify_refresh_token(token: str):
        return verify_refresh_token(token)