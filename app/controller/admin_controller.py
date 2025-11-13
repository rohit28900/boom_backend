from fastapi import APIRouter, Depends
from app.core.security import decode_access_token, require_role

router = APIRouter(prefix="/admin", tags=["Admin"])

@router.get("/dashboard")
def admin_dashboard(current_admin=Depends(require_role(["admin"]))):
    return {"message": "Welcome Admin!", "user": current_admin}
# from fastapi import APIRouter, Depends
# from app.core.security import require_role

# router = APIRouter(prefix="/admin", tags=["Admin"])

# @router.get("/dashboard")
# def admin_dashboard(current_admin=Depends(require_role(["admin"]))):
#     # current_admin now contains: {"email": ..., "role": ..., "name": ...}
#     return {"message": f"Welcome {current_admin['name']}!", "user": current_admin}
