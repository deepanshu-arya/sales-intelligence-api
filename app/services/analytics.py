from sqlalchemy.orm import Session
from app.models import Sale
from sqlalchemy import func

def daily_sales_summary(db: Session):
    results = (
        db.query(
            Sale.date,
            func.sum(Sale.quantity * Sale.price).label("total_revenue")
        )
        .group_by(Sale.date)
        .order_by(Sale.date)
        .all()
    )

    return [
        {"date": r.date, "revenue": r.total_revenue}
        for r in results
    ]


def product_performance(db: Session):
    results = (
        db.query(
            Sale.product,
            func.sum(Sale.quantity).label("qty"),
            func.sum(Sale.quantity * Sale.price).label("revenue")
        )
        .group_by(Sale.product)
        .order_by(func.sum(Sale.quantity * Sale.price).desc())
        .all()
    )

    return [
        {
            "product": r.product,
            "quantity_sold": r.qty,
            "revenue": r.revenue
        }
        for r in results
    ]
