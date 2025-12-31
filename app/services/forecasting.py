from sqlalchemy.orm import Session
from app.models import Sale
from sqlalchemy import func

def sales_forecast(db: Session, days: int = 7):
    daily = (
        db.query(
            Sale.date,
            func.sum(Sale.quantity).label("qty")
        )
        .group_by(Sale.date)
        .order_by(Sale.date)
        .all()
    )

    if len(daily) == 0:
        return {"forecast": []}

    avg = sum(d.qty for d in daily) / len(daily)

    forecast = []
    for i in range(1, days + 1):
        forecast.append({
            "day": f"Day +{i}",
            "expected_sales": round(avg, 2)
        })

    return forecast
