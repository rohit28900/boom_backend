from typing import Optional
from pydantic import BaseModel

class ContentBase(BaseModel):
    content_type: str
    title: str
    description: Optional[str] = None
    banner_url: Optional[str] = None
    banner_heading: Optional[str] = None

class ContentCreate(ContentBase):
    pass

class ContentUpdate(ContentBase):
    pass

class ContentResponse(ContentBase):
    id: int

    class Config:
        from_attributes = True
