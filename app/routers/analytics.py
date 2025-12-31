from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.database import get_db
from app.models import Sale
from app.services.analytics import daily_sales_summary, product_performance

router = APIRouter(prefix="/analytics", tags=["Analytics"])

@router.get("/")
def analytics_root():
    return {"message": "Sales analytics ready"}

@router.get("/top-products")
def top_products(db: Session = Depends(get_db)):
    results = (
        db.query(
            SalesRecord.product,
            func.sum(SalesRecord.quantity).label("total_quantity"),
            func.sum(SalesRecord.quantity * SalesRecord.price).label("revenue")
        )
        .group_by(SalesRecord.product)
        .order_by(func.sum(SalesRecord.quantity).desc())
        .limit(5)
        .all()
    )

    return [
        {
            "product": r.product,
            "quantity_sold": r.total_quantity,
            "revenue": r.revenue
        }
        for r in results
    ]

@router.get("/decline-trends")
def decline_trends(db: Session = Depends(get_db)):
    results = (
        db.query(
            SalesRecord.product,
            func.sum(SalesRecord.quantity).label("total_quantity")
        )
        .group_by(SalesRecord.product)
        .having(func.sum(SalesRecord.quantity) < 10)
        .all()
    )

    return [
        {
            "product": r.product,
            "status": "declining",
            "total_quantity": r.total_quantity
        }
        for r in results
    ]

@router.get("/daily-sales")
def daily_sales(db: Session = Depends(get_db)):
    return daily_sales_summary(db)


@router.get("/product-performance")
def product_stats(db: Session = Depends(get_db)):
    return product_performance(db)

