from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.schema.seo_schema import SEOCreate, SEOResponse, SEOUpdate
from app.services import seo_service
from app.core.security import require_role

router = APIRouter(
    prefix="/seo",
    tags=["SEO"]
)


@router.get("/", response_model=list[SEOResponse])
def get_seos(db: Session = Depends(get_db)):
    return seo_service.SEOService.get_seos(db)


@router.post("/", response_model=SEOResponse)
def create_seo(
    seo_data: SEOCreate,
    db: Session = Depends(get_db),
    current_user=Depends(require_role(["admin", "editor"]))
):
    return seo_service.SEOService.create_seo(db, seo_data)


@router.put("/{seo_id}", response_model=SEOResponse)
def update_seo(
    seo_id: int,
    seo_data: SEOUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(require_role(["admin", "editor"]))
):
    seo = seo_service.SEOService.update_seo(db, seo_id, seo_data)
    if not seo:
        raise HTTPException(status_code=404, detail="SEO record not found")
    return seo


@router.delete("/{seo_id}")
def delete_seo(
    seo_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(require_role(["admin"]))
):
    deleted = seo_service.SEOService.delete_seo(db, seo_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="SEO record not found")
    return {"detail": "SEO record deleted successfully"}
