from sqlalchemy.orm import Session
from datetime import datetime
from app.models.user_model import User
from app.models.role_model import Role
from app.core.security import hash_password



def get_user_by_email(db: Session, email: str):
    """Fetch user by email."""
    return db.query(User).filter(User.email == email).first()


def get_role_by_name(db: Session, name: str):
    """Fetch role by name."""
    return db.query(Role).filter(Role.name == name).first()

def create_role_if_not_exists(db: Session, name: str):
    """Create role if not exists."""
    role = get_role_by_name(db, name)
    if not role:
        role = Role(name=name)
        db.add(role)
        db.commit()
        db.refresh(role)
    return role


def create_user(db: Session, email: str, password: str, role_name: str, name: str):
    """Create new user with hashed password."""
    role = create_role_if_not_exists(db, role_name)
    user = User(
        name=name,
        email=email,
        hashed_password=hash_password(password),
        role=role.name,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user



def update_user_otp(db: Session, user: User, otp: str, expiry: datetime):
    """Save OTP and expiry time for password reset."""
    user.otp = otp
    user.otp_expiry = expiry
    db.commit()
    db.refresh(user)
    return user

def verify_user_otp(db: Session, email: str, otp: str):
    """Verify OTP and return user if valid."""
    user = get_user_by_email(db, email)
    if not user or user.otp != otp or not user.otp_expiry or user.otp_expiry < datetime.utcnow():
        return None
    return user

def reset_user_password(db: Session, user: User, new_password: str):
    """Reset user password securely after OTP verification."""
    user.hashed_password = hash_password(new_password)
    user.otp = None
    user.otp_expiry = None
    db.commit()
    db.refresh(user)
    return user
