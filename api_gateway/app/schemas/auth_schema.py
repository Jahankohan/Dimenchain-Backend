# api_gateway/app/schemas/auth_schema.py
from pydantic import BaseModel, EmailStr

class UserBase(BaseModel):
    username: str
    email: EmailStr

class UserCreate(UserBase):
    password: str

class UserLogin(BaseModel):
    identifier: str
    password: str

class User(UserBase):
    id: int
    is_active: bool
    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token: str
    refresh_token: str
    expires_in: int
    token_type: str

class RefreshTokenRequest(BaseModel):
    refresh_token: str

class EmailVerificationRequest(BaseModel):
    code: str

class ForgotPasswordRequest(BaseModel):
    email: EmailStr

class ResetPasswordRequest(BaseModel):
    token: str
    new_password: str

class ChangePasswordRequest(BaseModel):
    new_password: str
