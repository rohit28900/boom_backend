from sqlalchemy.orm import Session
from app.schema.lead_schema import LeadCreate
from app.repository.lead_repository import LeadRepository

def create_lead_service(db: Session, lead_data: LeadCreate):
    return LeadRepository.create(db, lead_data)

def get_leads_service(db: Session):
    return LeadRepository.get_all(db)

def update_lead_service(db: Session, lead_id: int, lead_data: LeadCreate):
    lead = LeadRepository.get_by_id(db, lead_id)
    if not lead:
        return None
    for key, value in lead_data.dict().items():
        setattr(lead, key, value)
    db.commit()
    db.refresh(lead)
    return lead

def delete_lead_service(db: Session, lead_id: int):
    lead = LeadRepository.get_by_id(db, lead_id)
    if not lead:
        return False
    LeadRepository.delete(db, lead)
    return True