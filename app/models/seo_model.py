from sqlalchemy import Column, Integer, String, Text
from app.db.database import Base

class SEO(Base):
    __tablename__ = "seo"

    id = Column(Integer, primary_key=True, index=True)
    page_name = Column(String, nullable=False)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    keywords = Column(Text, nullable=True)
