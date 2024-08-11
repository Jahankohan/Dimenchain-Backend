# auth_service/app/routes/auth_routes.py
from fastapi import APIRouter, Depends, HTTPException, Body, status
from sqlalchemy.orm import Session
from app.schemas import auth_schema
from app.services.auth_service import AuthService
from app.services.send_email import send_email
from datetime import datetime, timezone
from app.database import get_db
from fastapi.security import OAuth2PasswordBearer

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

@router.post("/register/", response_model=auth_schema.User)
def register_user(user: auth_schema.UserCreate, db: Session = Depends(get_db)):
    db_user = AuthService.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered!")
    new_user = AuthService.create_user(db=db, user=user)
    new_user.set_verification_code()
    db.commit()
    body = f"Your verification code is: {new_user.verification_code}"
    send_email(new_user.email, "Hivest Verification Code", body)
    return new_user

@router.post("/login/", response_model=auth_schema.Token)
def login_user(form_data: auth_schema.UserLogin, db: Session = Depends(get_db)):
    user = AuthService.authenticate_user(db, identifier=form_data.identifier, password=form_data.password)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect email/username or password")
    access_token, expires_in = AuthService.create_access_token(data={"sub": user.username, "email": user.email, "user_id": user.id})
    refresh_token = AuthService.create_refresh_token(data={"sub": user.username, "email": user.email, "user_id": user.id})
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "refresh_token": refresh_token,
        "expires_in": expires_in
    }

@router.post("/refresh/", response_model=auth_schema.Token)
def refresh_token(refresh_token: auth_schema.RefreshTokenRequest):
    payload = AuthService.verify_refresh_token(refresh_token.refresh_token)
    access_token, expires_in = AuthService.create_access_token(data={"sub": payload.username, "email": payload.email, "user_id": payload.user_id})
    new_refresh_token = AuthService.create_refresh_token(data={"sub": payload.username, "email": payload.email, "user_id": payload.user_id})
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "refresh_token": new_refresh_token,
        "expires_in": expires_in
    }

@router.post("/verify-email/")
def verify_email(email_verification_request: auth_schema.EmailVerificationRequest, token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    code = email_verification_request.code
    payload = AuthService.verify_access_token(token)
    email = payload.get("email")
    if email is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    
    db_user = AuthService.get_user_by_email(db, email=email)
    if not db_user:
        raise HTTPException(status_code=400, detail="User not found")
    
    if db_user.verification_code != code or datetime.now(timezone.utc) > db_user.verification_code_expiry.replace(tzinfo=timezone.utc):
        raise HTTPException(status_code=400, detail="Invalid or expired verification code")
    
    db_user.verification_code = None
    db_user.verification_code_expiry = None
    db.commit()
    return {"message": "Email verified successfully"}

@router.post("/resend-email-verification/")
def resend_email_verification(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    payload = AuthService.verify_access_token(token)
    email = payload.get("email")
    if email is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    
    db_user = AuthService.get_user_by_email(db, email=email)
    if not db_user:
        raise HTTPException(status_code=400, detail="User not found")
    
    db_user.set_verification_code()  # Set a new verification code and expiry
    db.commit()
    
    body = f"Your verification code is: {db_user.verification_code}"
    send_email(db_user.email, "Hivest Verification Code", body)
    return {"message": "Verification email resent successfully"}

@router.post("/forgot-password/")
def forgot_password(forget_password_req: auth_schema.ForgotPasswordRequest, db: Session = Depends(get_db)):
    return AuthService.send_password_reset_email(db=db, email=forget_password_req.email)

@router.post("/reset-password/")
def reset_password(reset_password_req: auth_schema.ResetPasswordRequest, db: Session = Depends(get_db)):
    return AuthService.reset_password(db=db, token=reset_password_req.token, new_password=reset_password_req.new_password)

@router.post("/change-password/")
def change_password(change_password_req: auth_schema.ChangePasswordRequest, token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    payload = AuthService.verify_access_token(token)
    email = payload.get("email")
    if email is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    
    db_user = AuthService.get_user_by_email(db, email=email)
    if not db_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
    return AuthService.change_password(db=db, user=db_user, new_password=change_password_req.new_password)