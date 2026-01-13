from fastapi import APIRouter, Depends, HTTPException, Header
from sqlalchemy.orm import Session
from app.admin.dependencies import verify_admin
from app.database import get_db
from app.api_keys.model import APIKey
from app.models import User
from datetime import timedelta, date

router = APIRouter(prefix="/admin", tags=["Admin"] )

ADMIN_API_KEY = "super-secret-admin-key"

@router.get("/users")
def list_users(db: Session = Depends(get_db)):
    return db.query(User).all()

@router.get("/api-keys")
def list_api_keys(db: Session = Depends(get_db)):
    return db.query(APIKey).all()

@router.post("/block-api-key/{key_id}")
def block_api_key(key_id: int, db: Session = Depends(get_db)):
    api_key = db.query(APIKey).filter(APIKey.id == key_id).first()
    if not api_key:
        raise HTTPException(status_code=404, detail="API key not found")

    api_key.is_active = False
    db.commit()
    return {"status": "blocked"}

@router.post("/upgrade-user/{user_id}")
def upgrade_user_plan(user_id: int, plan: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user.plan = plan
    db.commit()
    return {"status": f"user upgraded to {plan}"}

@router.get("/analytics/revenue")
def total_revenue(db: Session = Depends(get_db)):
    PRO_PRICE = 999  # monthly

    paid_users = db.query(User).filter(User.plan == "pro").count()
    revenue = paid_users * PRO_PRICE

    return {
        "paid_users": paid_users,
        "monthly_revenue": revenue
    }

@router.get("/analytics/top-users")
def top_users(db: Session = Depends(get_db)):
    keys = (
        db.query(APIKey)
        .order_by(APIKey.usage_count.desc())
        .limit(5)
        .all()
    )

    return [
        {
            "user_id": key.user_id,
            "usage": key.usage_count
        }
        for key in keys
    ]

@router.get("/analytics/overview")
def system_overview(db: Session = Depends(get_db)):
    return {
        "total_users": db.query(User).count(),
        "active_subscriptions": db.query(User).filter(User.plan == "pro").count(),
        "api_keys": db.query(APIKey).count()
    }

@router.get("/metrics")
def admin_metrics():
    return {
        "total_users": 3,
        "paid_users": 1,
        "active_subscriptions": 1,
        "monthly_revenue_estimate": 999,
        "csv_uploads_today": 5,
        "top_customers": []
    }

@router.post("/activate-pro/{user_id}")
def activate_pro(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user.is_pro = True
    user.subscription_expires = date.today() + timedelta(days=30)

    db.commit()

    return {
        "message": "User upgraded to PRO",
        "expires_on": user.subscription_expires
    }


