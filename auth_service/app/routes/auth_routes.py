# auth_service/app/routes/auth_routes.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.schemas import auth_schema
from app.services.auth_service import AuthService
from app.database import get_db

router = APIRouter()

@router.post("/register/", response_model=auth_schema.User)
def register_user(user: auth_schema.UserCreate, db: Session = Depends(get_db)):
    db_user = AuthService.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered!")
    return AuthService.create_user(db=db, user=user)

@router.post("/login/", response_model=auth_schema.Token)
def login_user(form_data: auth_schema.UserCreate, db: Session = Depends(get_db)):
    user = AuthService.authenticate_user(db, email=form_data.email, password=form_data.password)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    access_token = AuthService.create_access_token(data={"sub": user.username})
    return {"access token": access_token, "token_type": "bearer"}

