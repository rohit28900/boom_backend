from sqlalchemy.orm import Session
from app.repository.user_repository import get_user_by_email, create_user
from app.core.security import hash_password, verify_password, create_access_token

# --------------------------------------------------------------------------
# 1️⃣ Signup Service
# --------------------------------------------------------------------------
def signup_service(db: Session, name: str, email: str, password: str, role: str = "viewer"):
    existing_user = get_user_by_email(db, email)
    if existing_user:
        return {"error": "User already exists"}

    create_user(db, email=email, password=password, role_name=role, name=name)
    return {"message": "User created successfully"}

# --------------------------------------------------------------------------
# 2️⃣ Login Service
# --------------------------------------------------------------------------
def login_service(db: Session, email: str, password: str):
    user = get_user_by_email(db, email)
    if not user or not verify_password(password, user.hashed_password):
        return {"error": "Invalid email or password"}

    token = create_access_token({"sub": user.email, "role": user.role.value})
    return {
        "access_token": token,
        "token_type": "bearer",
        "user": {
            "name": user.name,
            "email": user.email,
            "role": user.role.value,
        },
    }

# --------------------------------------------------------------------------
# 3️⃣ Forgot Password Service (Info Only)
# --------------------------------------------------------------------------
def forgot_password_service(email: str):
    # Inform user that only admins can reset passwords
    return {
        "message": "Password resets are handled by the system administrator. Please contact support."
    }

# --------------------------------------------------------------------------
# 4️⃣ Admin Reset Password Service (Admin-only)
# --------------------------------------------------------------------------
def admin_reset_password_service(db: Session, email: str, new_password: str):
    user = get_user_by_email(db, email)
    if not user:
        return {"error": "User not found"}

    user.hashed_password = hash_password(new_password)
    db.commit()
    return {"message": f"Password successfully reset for {email}"}
