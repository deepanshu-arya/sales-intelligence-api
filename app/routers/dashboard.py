from fastapi import APIRouter

router = APIRouter()

@router.get("/")
def dashboard_root():
    return {"message": "Dashboard router working"}
