from pydantic import BaseModel, EmailStr, Field
from typing import Optional

# ------------------------------------------------------------------------------
# User Base Schema
# ------------------------------------------------------------------------------
class UserBase(BaseModel):
    name: Optional[str] = Field(None, example="John Doe")
    email: EmailStr = Field(..., example="john@example.com")

# ------------------------------------------------------------------------------
# Signup Schema
# ------------------------------------------------------------------------------
class SignupRequest(UserBase):
    password: str = Field(..., min_length=6, example="SecurePass123")
    role: Optional[str] = Field("viewer", example="viewer")

class SignupResponse(BaseModel):
    message: str = Field(..., example="User created successfully")

# ------------------------------------------------------------------------------
# Login Schema
# ------------------------------------------------------------------------------
class LoginRequest(BaseModel):
    email: EmailStr = Field(..., example="john@example.com")
    password: str = Field(..., example="SecurePass123")

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: dict

# ------------------------------------------------------------------------------
# Forgot Password (Info Only)
# ------------------------------------------------------------------------------
class ForgotPasswordResponse(BaseModel):
    message: str = Field(
        ...,
        example="Password resets are handled by the system administrator. Please contact support.",
    )

# ------------------------------------------------------------------------------
# Admin Password Reset Schema
# ------------------------------------------------------------------------------
class AdminResetPasswordRequest(BaseModel):
    email: EmailStr
    new_password: str = Field(..., min_length=6, example="NewSecurePass123")

class AdminResetPasswordResponse(BaseModel):
    message: str
