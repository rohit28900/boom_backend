from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.schema.plan_schema import InternetPlanCreate, InternetPlanResponse, InternetPlanUpdate
from app.repository import plan_repository
from app.core.security import require_role  # your role-based dependency

router = APIRouter(
    prefix="/plans",
    tags=["Plans"]
)

# ------------------------------
# 👀 Public: View all plans
# ------------------------------
@router.get("/", response_model=list[InternetPlanResponse])
def get_plans(db: Session = Depends(get_db)):
    return plan_repository.get_all_plans(db)

# ------------------------------
# 👀 Public: View single plan
# ------------------------------
@router.get("/{plan_id}", response_model=InternetPlanResponse)
def get_plan(plan_id: int, db: Session = Depends(get_db)):
    plan = plan_repository.get_plan_by_id(db, plan_id)
    if not plan:
        raise HTTPException(status_code=404, detail="Plan not found")
    return plan

# ------------------------------
# 🔐 Admin/Editor only: Create plan
# ------------------------------
@router.post("/", response_model=InternetPlanResponse)
def create_plan(
    plan_data: InternetPlanCreate,
    db: Session = Depends(get_db),
    current_user=Depends(require_role(["admin", "editor"]))
):
    return plan_repository.create_plan(db, plan_data)

# ------------------------------
# 🔐 Admin/Editor only: Update plan
# ------------------------------
@router.put("/{plan_id}", response_model=InternetPlanResponse)
def update_plan(
    plan_id: int,
    plan_data: InternetPlanUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(require_role(["admin", "editor"]))
):
    plan = plan_repository.update_plan(db, plan_id, plan_data)
    if not plan:
        raise HTTPException(status_code=404, detail="Plan not found")
    return plan

# ------------------------------
# 🔐 Admin only: Delete plan
# ------------------------------
@router.delete("/{plan_id}")
def delete_plan(
    plan_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(require_role(["admin"]))
):
    success = plan_repository.delete_plan(db, plan_id)
    if not success:
        raise HTTPException(status_code=404, detail="Plan not found")
    return {"message": "Plan deleted successfully"}
