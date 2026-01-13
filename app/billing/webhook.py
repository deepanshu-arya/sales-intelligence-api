from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from datetime import datetime, timedelta

from app.database import get_db
from app.models import User
from app.config import SUBSCRIPTION_DAYS

router = APIRouter(prefix="/billing", tags=["Billing"])

@router.post("/webhook")
def razorpay_webhook(payload: dict, db: Session = Depends(get_db)):
    notes = payload.get("payload", {}).get("payment", {}).get("entity", {}).get("notes", {})
    user_id = notes.get("user_id")

    if not user_id:
        return {"status": "ignored"}

    user = db.query(User).filter(User.id == user_id).first()
    user.is_pro = True
    user.subscription_expires = datetime.utcnow() + timedelta(days=SUBSCRIPTION_DAYS)

    db.commit()
    return {"status": "subscription activated"}
