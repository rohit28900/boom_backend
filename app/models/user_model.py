from sqlalchemy import Column, Integer, String, Enum, DateTime
from app.db.database import Base
import enum
from datetime import datetime


class UserRole(enum.Enum):
    admin = "admin"
    editor = "editor"
    viewer = "viewer"


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)  # hashed password
    role = Column(Enum(UserRole), default=UserRole.viewer)

    
    # otp = Column(String(6), nullable=True)  # store 6-digit OTP
    # otp_expiry = Column(DateTime, nullable=True)  # expiration timestamp

    # # Optional: convenience method to check if OTP is valid
    # def is_otp_valid(self, otp_code: str) -> bool:
    #     if not self.otp or not self.otp_expiry:
    #         return False
    #     return self.otp == otp_code and self.otp_expiry > datetime.utcnow()
