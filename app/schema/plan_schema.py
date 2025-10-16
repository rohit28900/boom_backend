from pydantic import BaseModel
from typing import Optional

class InternetPlanBase(BaseModel):
    name: str
    price: float
    features: Optional[str] = None
    speed: str
    ott: bool = False
    live_tv: bool = False
    popular: bool = False

class InternetPlanCreate(InternetPlanBase):
    pass

class InternetPlanUpdate(InternetPlanBase):
    pass

class InternetPlanResponse(InternetPlanBase):
    id: int

    class Config:
        orm_mode = True
