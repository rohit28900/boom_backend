from sqlalchemy import Column, Integer, String, Boolean, Float
from app.db.database import Base

class InternetPlan(Base):
    __tablename__ = "internet_plans"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    features = Column(String)
    speed = Column(String, nullable=False)
    ott = Column(Boolean, default=False)
    live_tv = Column(Boolean, default=False)
    popular = Column(Boolean, default=False)
