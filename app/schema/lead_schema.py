from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional
import enum

class ConnectionType(str, enum.Enum):
    home = "home"
    business = "business"

class LeadStatus(str, enum.Enum):
    new = "new"
    contacted = "contacted"
    qualified = "qualified"
    lost = "lost"
    converted = "converted"

class LeadCreate(BaseModel):
    name: str
    state: Optional[str]
    phone_no: str
    email: EmailStr
    source: Optional[str]
    connection_type: ConnectionType
    status: Optional[LeadStatus] = LeadStatus.new

    class Config:
        from_attributes = True


class LeadResponse(LeadCreate):
    id: int
    date: datetime
