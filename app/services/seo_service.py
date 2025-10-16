from sqlalchemy.orm import Session
from app.models.seo_model import SEO
from app.schema.seo_schema import SEOCreate, SEOUpdate
from app.repository.seo_repository import SEORepository

class SEOService:

    @staticmethod
    def create_seo(db: Session, seo_data: SEOCreate):
        seo = SEO(**seo_data.dict())
        return SEORepository.create(db, seo)

    @staticmethod
    def get_seos(db: Session):
        return SEORepository.get_all(db)

    @staticmethod
    def update_seo(db: Session, seo_id: int, seo_data: SEOUpdate):
        seo = SEORepository.get_by_id(db, seo_id)
        if seo:
            return SEORepository.update(db, seo, seo_data.dict(exclude_unset=True))
        return None

    @staticmethod
    def delete_seo(db: Session, seo_id: int):
        seo = SEORepository.get_by_id(db, seo_id)
        if seo:
            SEORepository.delete(db, seo)
            return True
        return False
