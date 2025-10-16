from pydantic import BaseModel

class ContentBase(BaseModel):
    content_type: str
    title: str
    description: str | None = None
    banner_url: str | None = None
    banner_heading: str | None = None

class ContentCreate(ContentBase):
    pass

class ContentUpdate(ContentBase):
    pass

class ContentResponse(ContentBase):
    id: int

    class Config:
        from_attributes = True
