from sqlalchemy.orm import Session
from app.models.lead_model import Lead
from app.schema.lead_schema import LeadCreate
from app.utils.pagination import Pagination, PaginationParams

class LeadRepository:

    @staticmethod
    def get_all_paginated(db: Session, params: PaginationParams):
        """
        Get paginated leads using Pagination utility
        
        Args:
            db: Database session
            params: PaginationParams object
        
        Returns:
            PaginatedResponse with leads
        """
        query = db.query(Lead)
        return Pagination.paginate_and_respond(query, params)
    
    @staticmethod
    def get_all(db: Session):
        """Get all leads without pagination"""
        return db.query(Lead).all()

    @staticmethod
    def get_by_id(db: Session, lead_id: int):
        return db.query(Lead).filter(Lead.id == lead_id).first()

    @staticmethod
    def create(db: Session, lead_data: LeadCreate):
        lead = Lead(
            name=lead_data.name,
            state=lead_data.state,
            phone_no=lead_data.phone_no,
            email=lead_data.email,
            source=lead_data.source,
            connection_type=lead_data.connection_type,
            status=lead_data.status
        )
        db.add(lead)
        db.commit()
        db.refresh(lead)
        return lead

    @staticmethod
    def update(db: Session, lead: Lead, data: dict):
        for key, value in data.items():
            setattr(lead, key, value)
        db.commit()
        db.refresh(lead)
        return lead

    @staticmethod
    def delete(db: Session, lead: Lead):
        db.delete(lead)
        db.commit()