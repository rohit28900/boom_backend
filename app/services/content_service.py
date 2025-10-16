from sqlalchemy.orm import Session
from app.repository.content_repository import ContentRepository
from app.schema.content_schema import ContentCreate, ContentUpdate

class ContentService:
    @staticmethod
    def create_content(db: Session, content: ContentCreate):
        return ContentRepository.create(db, content)

    @staticmethod
    def get_contents(db: Session):
        return ContentRepository.get_all(db)

    @staticmethod
    def get_content(db: Session, content_id: int):
        return ContentRepository.get_by_id(db, content_id)

    @staticmethod
    def update_content(db: Session, content_id: int, content: ContentUpdate):
        return ContentRepository.update(db, content_id, content)

    @staticmethod
    def delete_content(db: Session, content_id: int):
        return ContentRepository.delete(db, content_id)
