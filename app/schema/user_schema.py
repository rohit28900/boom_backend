from pydantic import BaseModel, EmailStr
from typing import Optional

class RoleOut(BaseModel):
    id: int
    name: str
    class Config:
        orm_mode = True

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    role_name: Optional[str] = "admin"  # default role

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserOut(BaseModel):
    id: int
    email: EmailStr
    role: RoleOut
    class Config:
        orm_mode = True

class ForgotPassword(BaseModel):
    email: EmailStr

class ResetPassword(BaseModel):
    email: EmailStr
    new_password: str
