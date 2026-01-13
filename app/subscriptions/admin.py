from datetime import date, timedelta
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models import User

router = APIRouter(prefix="/admin", tags=["Admin"])

@router.post("/activate-pro/{user_id}")
def activate_pro(user_id: int, db: Session = Depends(get_db)):

    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user.is_pro = True
    user.subscription_expires = date.today() + timedelta(days=30)

    db.commit()

    return {"message": "User upgraded to Pro for 30 days"}



