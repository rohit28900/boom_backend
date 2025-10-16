from sqlalchemy import Column, Integer, String
from app.db.database import Base

class Content(Base):
    __tablename__ = "contents"

    id = Column(Integer, primary_key=True, index=True)
    content_type = Column(String, nullable=False)  # e.g., "plan" or "banner"
    title = Column(String, nullable=False)
    description = Column(String, nullable=True)
    banner_url = Column(String, nullable=True)  # URL to banner image
    banner_heading = Column(String, nullable=True)
