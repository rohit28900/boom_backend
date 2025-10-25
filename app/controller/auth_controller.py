from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi import Form
from app.db.database import get_db
from app.services.auth_service import (
    signup_service,
    login_service,
    forgot_password_service,
    admin_reset_password_service,
)
from app.schema.auth_schema import (  # <-- make sure folder is 'schemas'
    SignupRequest,
    SignupResponse,
    LoginRequest,
    TokenResponse,
    ForgotPasswordResponse,
    AdminResetPasswordRequest,
    AdminResetPasswordResponse,
)
from app.core.security import require_role


auth_router = APIRouter(prefix="/auth", tags=["Auth"])

# ------------------------------------------------------------------------------
# 🧍 Signup
# ------------------------------------------------------------------------------
@auth_router.post("/signup", response_model=SignupResponse, status_code=status.HTTP_201_CREATED)
def signup(payload: SignupRequest, db: Session = Depends(get_db)):
    result = signup_service(db, payload.name, payload.email, payload.password, payload.role)
    if "error" in result:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=result["error"])
    return result

# ------------------------------------------------------------------------------
# 🔐 Login
# ------------------------------------------------------------------------------
@auth_router.post("/login", response_model=TokenResponse)
def login(login_data: LoginRequest, db: Session = Depends(get_db)):
    """
    Login using JSON payload:
    {
        "username": "manoj@gmail.com",
        "password": "test123"
    }
    """
    result = login_service(db, login_data.email, login_data.password)
    if "error" in result:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=result["error"])
    return result


@auth_router.post("/forgot-password", response_model=ForgotPasswordResponse)
def forgot_password():
    return forgot_password_service("")

# ------------------------------------------------------------------------------
# 🛠️ Admin Reset Password (Admin-only)
# ------------------------------------------------------------------------------
@auth_router.post("/admin-reset-password", response_model=AdminResetPasswordResponse)
def admin_reset_password(
    payload: AdminResetPasswordRequest,
    db: Session = Depends(get_db),
    current_user=Depends(require_role(["admin"])),
):
    result = admin_reset_password_service(db, payload.email, payload.new_password)
    if "error" in result:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=result["error"])
    return result


