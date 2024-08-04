from fastapi import APIRouter, HTTPException, Body, Depends
from app.schemas import auth_schema
import requests
from app.config import AUTH_SERVICE_URL
from fastapi.security import OAuth2PasswordBearer

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

@router.post("/register/", response_model=auth_schema.User)
def register_user(user: auth_schema.UserCreate):
    response = requests.post(f"{AUTH_SERVICE_URL}/register/", json=user.dict())
    if response.status_code != 200:
        try:
            raise HTTPException(status_code=response.status_code, detail=response.json())
        except ValueError:
            raise HTTPException(status_code=response.status_code, detail=response.text)
    return response.json()

@router.post("/login/", response_model=auth_schema.Token)
def login_user(form_data: auth_schema.UserLogin):
    response = requests.post(f"{AUTH_SERVICE_URL}/login/", json=form_data.dict())
    if response.status_code != 200:
        try:
            raise HTTPException(status_code=response.status_code, detail=response.json())
        except ValueError:
            raise HTTPException(status_code=response.status_code, detail=response.text)
    return response.json()

@router.post("/refresh/", response_model=auth_schema.Token)
def refresh_token(refresh_token: auth_schema.RefreshTokenRequest):
    response = requests.post(f"{AUTH_SERVICE_URL}/refresh/", json=refresh_token.dict())
    if response.status_code != 200:
        try:
            raise HTTPException(status_code=response.status_code, detail=response.json())
        except ValueError:
            raise HTTPException(status_code=response.status_code, detail=response.text)
    return response.json()

@router.post("/verify-email/")
def verify_email(email_verification_request: auth_schema.EmailVerificationRequest, token: str = Depends(oauth2_scheme)):
    print(f"Code: {email_verification_request.code}")
    print(f"Bearer: {token}")
    response = requests.post(f"{AUTH_SERVICE_URL}/verify-email/", json=email_verification_request.dict(), headers={"Authorization": f"Bearer {token}"})
    if response.status_code != 200:
        try:
            raise HTTPException(status_code=response.status_code, detail=response.json())
        except ValueError:
            raise HTTPException(status_code=response.status_code, detail=response.text)
    return response.json()

@router.post("/resend-email-verification/")
def resend_email_verification(token: str = Depends(oauth2_scheme)):
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.post(f"{AUTH_SERVICE_URL}/resend-email-verification/", headers=headers)
    if response.status_code != 200:
        try:
            raise HTTPException(status_code=response.status_code, detail=response.json())
        except ValueError:
            raise HTTPException(status_code=response.status_code, detail=response.text)
    return response.json()

@router.post("/forgot-password/")
def forgot_password(forget_password_req: auth_schema.ForgotPasswordRequest):
    response = requests.post(f"{AUTH_SERVICE_URL}/forgot-password/", json=forget_password_req.dict())
    if response.status_code != 200:
        try:
            raise HTTPException(status_code=response.status_code, detail=response.json())
        except ValueError:
            raise HTTPException(status_code=response.status_code, detail=response.text)
    return response.json()

@router.post("/reset-password/")
def reset_password(reset_password_req: auth_schema.ResetPasswordRequest):
    response = requests.post(f"{AUTH_SERVICE_URL}/reset-password/", json=reset_password_req.dict())
    if response.status_code != 200:
        try:
            raise HTTPException(status_code=response.status_code, detail=response.json())
        except ValueError:
            raise HTTPException(status_code=response.status_code, detail=response.text)
    return response.json()

@router.post("/change-password/")
def change_password(change_password_req: auth_schema.ChangePasswordRequest, token: str = Depends(oauth2_scheme)):
    response = requests.post(
        f"{AUTH_SERVICE_URL}/change-password/", 
        json=change_password_req.dict(), 
        headers={"Authorization": f"Bearer {token}"}
    )
    if response.status_code != 200:
        try:
            raise HTTPException(status_code=response.status_code, detail=response.json())
        except ValueError:
            raise HTTPException(status_code=response.status_code, detail=response.text)
    return response.json()

