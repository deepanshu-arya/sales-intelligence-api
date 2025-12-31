from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from sqlalchemy.orm import Session
import pandas as pd
from datetime import datetime

from app.database import get_db
from app.models import Sale   # ✅ CORRECT MODEL

router = APIRouter(prefix="/sales", tags=["Sales"])


def parse_date(date_str: str):
    for fmt in ("%Y-%m-%d", "%d-%m-%Y"):
        try:
            return datetime.strptime(date_str, fmt).date()
        except ValueError:
            continue
    raise ValueError(f"Invalid date format: {date_str}")


@router.post("/upload")
def upload_sales_csv(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    if not file.filename.endswith(".csv"):
        raise HTTPException(status_code=400, detail="Only CSV files allowed")

    try:
        df = pd.read_csv(file.file)

        required_columns = {"date", "product", "quantity", "price"}
        if not required_columns.issubset(df.columns):
            raise HTTPException(
                status_code=400,
                detail=f"CSV must contain columns: {required_columns}"
            )

        records_added = 0

        for _, row in df.iterrows():
            total_amount = float(row["quantity"]) * float(row["price"])

            sale = Sale(   # ✅ FIXED HERE
                date=parse_date(str(row["date"])),
                product=str(row["product"]),
                quantity=int(row["quantity"]),
                price=float(row["price"]),
                total_amount=total_amount
            )

            db.add(sale)
            records_added += 1

        db.commit()

        return {
            "status": "success",
            "records_inserted": records_added
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/weekly")
def weekly_sales():
    return [
        {"day": "Mon", "amount": 120},
        {"day": "Tue", "amount": 210},
        {"day": "Wed", "amount": 150},
        {"day": "Thu", "amount": 300},
        {"day": "Fri", "amount": 280},
        {"day": "Sat", "amount": 350},
        {"day": "Sun", "amount": 410},
    ]
