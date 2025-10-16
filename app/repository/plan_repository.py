from sqlalchemy.orm import Session
from app.models.plan_model import InternetPlan
from app.schema.plan_schema import InternetPlanCreate, InternetPlanUpdate

def get_all_plans(db: Session):
    return db.query(InternetPlan).all()

def get_plan_by_id(db: Session, plan_id: int):
    return db.query(InternetPlan).filter(InternetPlan.id == plan_id).first()

def create_plan(db: Session, plan_data: InternetPlanCreate):
    plan = InternetPlan(**plan_data.dict())
    db.add(plan)
    db.commit()
    db.refresh(plan)
    return plan

def update_plan(db: Session, plan_id: int, plan_data: InternetPlanUpdate):
    plan = get_plan_by_id(db, plan_id)
    if not plan:
        return None
    for key, value in plan_data.dict().items():
        setattr(plan, key, value)
    db.commit()
    db.refresh(plan)
    return plan

def delete_plan(db: Session, plan_id: int):
    plan = get_plan_by_id(db, plan_id)
    if plan:
        db.delete(plan)
        db.commit()
        return True
    return False
