from typing import Optional
from pydantic import BaseModel

class SEOBase(BaseModel):
    page_name: str
    title: str
    description: Optional[str] = None
    keywords: Optional[str] = None

class SEOCreate(SEOBase):
    pass

class SEOUpdate(SEOBase):
    pass

class SEOResponse(SEOBase):
    id: int

    class Config:
        from_attributes = True
