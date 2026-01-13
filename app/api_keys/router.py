from fastapi import APIRouter, Depends, Header, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.api_keys.model import APIKey
from app.api_keys.service import generate_api_key
from app.models import User

router = APIRouter(prefix="/api-keys", tags=["API Keys"])

@router.post("/")
def create_api_key(
    db: Session = Depends(get_db)
):
    api_key = APIKey(
        key=generate_api_key(),
        user_id=current_user.id
    )
    db.add(api_key)
    db.commit()
    db.refresh(api_key)

    return {"api_key": api_key.key}
