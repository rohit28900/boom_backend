from sqlalchemy import Column, Integer, String, DateTime, Enum
from sqlalchemy.sql import func
from app.db.database import Base
import enum

class ConnectionType(enum.Enum):
    home = "home"
    business = "business"

class LeadStatus(enum.Enum):
    new = "new"
    contacted = "contacted"
    qualified = "qualified"
    lost = "lost"
    converted = "converted"

class Lead(Base):
    __tablename__ = "leads"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    state = Column(String, nullable=True)
    phone_no = Column(String, nullable=False)
    email = Column(String, nullable=False)
    source = Column(String, nullable=True)
    connection_type = Column(Enum(ConnectionType), nullable=False, default=ConnectionType.home)
    date = Column(DateTime(timezone=True), server_default=func.now())
    status = Column(Enum(LeadStatus), nullable=False, default=LeadStatus.new)
