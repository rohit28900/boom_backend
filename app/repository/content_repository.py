from sqlalchemy.orm import Session
from app.models.content_model import Content
from app.schema.content_schema import ContentCreate, ContentUpdate

class ContentRepository:
    @staticmethod
    def create(db: Session, content: ContentCreate):
        db_content = Content(**content.dict())
        db.add(db_content)
        db.commit()
        db.refresh(db_content)
        return db_content

    @staticmethod
    def get_all(db: Session):
        return db.query(Content).all()

    @staticmethod
    def get_by_id(db: Session, content_id: int):
        return db.query(Content).filter(Content.id == content_id).first()

    @staticmethod
    def update(db: Session, content_id: int, content: ContentUpdate):
        db_content = db.query(Content).filter(Content.id == content_id).first()
        if db_content:
            for key, value in content.dict(exclude_unset=True).items():
                setattr(db_content, key, value)
            db.commit()
            db.refresh(db_content)
        return db_content

    @staticmethod
    def delete(db: Session, content_id: int):
        db_content = db.query(Content).filter(Content.id == content_id).first()
        if db_content:
            db.delete(db_content)
            db.commit()
        return db_content
