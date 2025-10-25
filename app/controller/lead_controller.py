from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.schema.lead_schema import LeadCreate, LeadResponse
from app.services import lead_service
from app.utils.pagination import PaginatedResponse, PaginationParams
from app.core.security import require_role  # import your role checker

router = APIRouter(prefix="/leads", tags=["Leads"])

# Only admin, editor can create leads
# @router.post("/", response_model=LeadResponse, dependencies=[Depends(require_role(["admin", "editor"]))])
@router.post("/", response_model=LeadResponse)
def create_lead(lead_data: LeadCreate, db: Session = Depends(get_db)):
    return lead_service.create_lead_service(db, lead_data)

# Get paginated leads - Any logged-in user can view leads
@router.get("/", response_model=PaginatedResponse[LeadResponse])
def get_leads(
    page: int = Query(1, ge=1, description="Page number (starts from 1)"),
    page_size: int = Query(10, ge=1, le=100, description="Number of items per page (max 100)"),
    db: Session = Depends(get_db)
):
    """
    Get paginated list of leads
    
    Query Parameters:
    - **page**: Page number (default: 1)
    - **page_size**: Items per page (default: 10, max: 100)
    
    Returns:
    - **items**: List of leads for current page
    - **total**: Total number of leads
    - **page**: Current page number
    - **page_size**: Items per page
    - **total_pages**: Total number of pages
    - **has_next**: Whether there's a next page
    - **has_prev**: Whether there's a previous page
    """
    params = PaginationParams(page=page, page_size=page_size)
    return lead_service.get_leads_paginated_service(db, params)

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