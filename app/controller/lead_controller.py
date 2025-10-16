from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.schema.lead_schema import LeadCreate, LeadResponse
from app.services import lead_service
from app.core.security import require_role  # import your role checker

router = APIRouter(prefix="/leads", tags=["Leads"])

# Only admin, editor can create leads
# @router.post("/", response_model=LeadResponse, dependencies=[Depends(require_role(["admin", "editor"]))])
@router.post("/", response_model=LeadResponse)
def create_lead(lead_data: LeadCreate, db: Session = Depends(get_db)):
    return lead_service.create_lead_service(db, lead_data)

# Any logged-in user can view leads
@router.get("/", response_model=list[LeadResponse])
def get_leads(db: Session = Depends(get_db)):
    return lead_service.get_leads_service(db)

# Only admin, editor can update leads
# @router.put("/{lead_id}", response_model=LeadResponse, dependencies=[Depends(require_role(["admin", "editor"]))])
@router.put("/{lead_id}", response_model=LeadResponse)
def update_lead(lead_id: int, lead_data: LeadCreate, db: Session = Depends(get_db)):
    updated_lead = lead_service.update_lead_service(db, lead_id, lead_data)
    if not updated_lead:
        raise HTTPException(status_code=404, detail="Lead not found")
    return updated_lead

# Only admin can delete leads
# @router.delete("/{lead_id}", dependencies=[Depends(require_role(["admin"]))])
@router.delete("/{lead_id}")
def delete_lead(lead_id: int, db: Session = Depends(get_db)):
    deleted = lead_service.delete_lead_service(db, lead_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Lead not found")
    return {"message": "Lead deleted successfully"}
