from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.schema.content_schema import ContentCreate, ContentUpdate, ContentResponse
from app.services import content_service
from app.core.security import require_role

router = APIRouter(
    prefix="/contents",
    tags=["Contents"]
)

# ------------------------------
# Public: View all contents
# ------------------------------
@router.get("/", response_model=list[ContentResponse])
def get_contents(db: Session = Depends(get_db)):
    return content_service.ContentService.get_contents(db)

# ------------------------------
# Public: View single content
# ------------------------------
@router.get("/{content_id}", response_model=ContentResponse)
def get_content(content_id: int, db: Session = Depends(get_db)):
    result = content_service.ContentService.get_content(db, content_id)
    if not result:
        raise HTTPException(status_code=404, detail="Content not found")
    return result

# ------------------------------
# Admin/Editor only: Create content
# ------------------------------
@router.post("/", response_model=ContentResponse)
def create_content(
    content: ContentCreate,
    db: Session = Depends(get_db),
    current_user=Depends(require_role(["admin", "editor"]))
):
    return content_service.ContentService.create_content(db, content)

# ------------------------------
# Admin/Editor only: Update content
# ------------------------------
@router.put("/{content_id}", response_model=ContentResponse)
def update_content(
    content_id: int,
    content: ContentUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(require_role(["admin", "editor"]))
):
    result = content_service.ContentService.update_content(db, content_id, content)
    if not result:
        raise HTTPException(status_code=404, detail="Content not found")
    return result

# ------------------------------
# Admin only: Delete content
# ------------------------------
@router.delete("/{content_id}")
def delete_content(
    content_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(require_role(["admin"]))
):
    result = content_service.ContentService.delete_content(db, content_id)
    if not result:
        raise HTTPException(status_code=404, detail="Content not found")
    return {"detail": "Content deleted successfully"}
