from sqlalchemy.orm import Session
from app.models.seo_model import SEO

class SEORepository:

    @staticmethod
    def get_all(db: Session):
        return db.query(SEO).all()

    @staticmethod
    def get_by_id(db: Session, seo_id: int):
        return db.query(SEO).filter(SEO.id == seo_id).first()

    @staticmethod
    def create(db: Session, seo: SEO):
        db.add(seo)
        db.commit()
        db.refresh(seo)
        return seo

    @staticmethod
    def update(db: Session, seo: SEO, data: dict):
        for key, value in data.items():
            setattr(seo, key, value)
        db.commit()
        db.refresh(seo)
        return seo

    @staticmethod
    def delete(db: Session, seo: SEO):
        db.delete(seo)
        db.commit()
