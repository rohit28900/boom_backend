# from pydantic import BaseModel, EmailStr
# from typing import Optional

# class RoleOut(BaseModel):
#     id: int
#     name: str
#     class Config:
#         orm_mode = True

# class UserCreate(BaseModel):
#     email: EmailStr
#     password: str
#     role_name: Optional[str] = "admin"  # default role

# class UserLogin(BaseModel):
#     email: EmailStr
#     password: str

# class UserOut(BaseModel):
#     id: int
#     email: EmailStr
#     role: RoleOut
#     class Config:
#         orm_mode = True

# class ForgotPassword(BaseModel):
#     email: EmailStr

# class ResetPassword(BaseModel):
#     email: EmailStr
#     new_password: str

from pydantic import BaseModel, EmailStr, Field
from typing import Optional

# ----------------------
# Base User Schema
# ----------------------
class UserBase(BaseModel):
    name: Optional[str] = Field(None, example="John Doe")
    email: EmailStr = Field(..., example="john@example.com")

# ----------------------
# Signup Schema
# ----------------------
class SignupRequest(UserBase):
    password: str = Field(..., min_length=6, example="SecurePass123")
    role: Optional[str] = Field("viewer", example="viewer")

class SignupResponse(BaseModel):
    message: str = Field(..., example="User created successfully")

# ----------------------
# Login Schema
# ----------------------
class LoginRequest(BaseModel):
    email: EmailStr = Field(..., example="john@example.com")
    password: str = Field(..., example="SecurePass123")

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: dict

# ----------------------
# Forgot Password
# ----------------------
class ForgotPasswordResponse(BaseModel):
    message: str = Field(
        ...,
        example="Password resets are handled by the system administrator. Please contact support.",
    )

# ----------------------
# Admin Reset Password
# ----------------------
class AdminResetPasswordRequest(BaseModel):
    email: EmailStr
    new_password: str = Field(..., min_length=6, example="NewSecurePass123")

class AdminResetPasswordResponse(BaseModel):
    message: str

# ----------------------
# User Response
# ----------------------
class UserResponse(BaseModel):
    id: int
    name: Optional[str]
    email: EmailStr
    role: Optional[str]

    class Config:
        from_attributes = True
