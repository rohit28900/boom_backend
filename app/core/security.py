# app/security.py

from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

# ------------------------------------------------------------------------------
# 🔐 Configuration
# ------------------------------------------------------------------------------
SECRET_KEY = "supersecretkey123"  # ⚠️ Replace with environment variable in prod
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24  # 24 hours

# ------------------------------------------------------------------------------
# 🔑 Password Hashing with Argon2
# ------------------------------------------------------------------------------
pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

def hash_password(password: str) -> str:
    """Return a hashed version of the password using Argon2."""
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify plain password against its hash."""
    return pwd_context.verify(plain_password, hashed_password)

# ------------------------------------------------------------------------------
# 🧾 JWT Token Helpers
# ------------------------------------------------------------------------------
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Create a JWT access token."""
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# ------------------------------------------------------------------------------
# 🔒 HTTP Bearer Token (for Swagger)
# ------------------------------------------------------------------------------
bearer_scheme = HTTPBearer()

def decode_access_token(credentials: HTTPAuthorizationCredentials = Security(bearer_scheme)):
    """Decode JWT token and return payload."""
    token = credentials.credentials
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        role: str = payload.get("role")
        name: str = payload.get("name") 
        if email is None or role is None:
            raise HTTPException(status_code=401, detail="Invalid token payload")
        return {"email": email, "role": role}
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

# ------------------------------------------------------------------------------
# 🧩 Role-Based Access
# ------------------------------------------------------------------------------
def require_role(allowed_roles: list[str]):
    """Dependency to restrict route access based on role."""
    def role_checker(current_user=Depends(decode_access_token)):
        if current_user["role"] not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have permission to access this resource.",
            )
        return current_user
    return role_checker

# app/core/security.py

def get_current_user(credentials: HTTPAuthorizationCredentials = Security(bearer_scheme)):
    """Get current logged-in user info from JWT."""
    token = credentials.credentials
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        role: str = payload.get("role")
        name: str = payload.get("name")
        if email is None:
            raise HTTPException(status_code=401, detail="Invalid token payload")
        return {"email": email, "role": role, "name": name}
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
