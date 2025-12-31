from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.services.forecasting import sales_forecast

router = APIRouter(prefix="/forecast", tags=["Forecast"])

@router.get("/")
def forecast_root():
    return {"message": "Forecast router working"}

@router.get("/next-7-days")
def forecast_next_week(db: Session = Depends(get_db)):
    return sales_forecast(db)


