from fastapi import APIRouter, Depends, Query
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from db.database import get_db
from app.services.lead_export_service import LeadExportService

router = APIRouter(prefix="/export", tags=["Leads Export"])

@router.get("/leads/pdf")
def export_leads_pdf(
    duration: str = Query("1m", regex="^(1m|6m|1y)$"),
    db: Session = Depends(get_db),
):
    pdf_path = LeadExportService.export_leads_to_pdf(db, duration)
    return FileResponse(
        pdf_path,
        filename=f"leads_report_{duration}.pdf",
        media_type="application/pdf",
    )
