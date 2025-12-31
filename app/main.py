from fastapi import FastAPI
from app.database import engine, Base, init_db
from app.routers import sales, analytics, forecast, dashboard
from app.auth import auth
from fastapi.middleware.cors import CORSMiddleware

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Sales Intelligence API")

app.include_router(auth.router)
app.include_router(sales.router, prefix="/sales", tags=["Sales"])
app.include_router(analytics.router, prefix="/analytics", tags=["Analytics"])
app.include_router(forecast.router, prefix="/forecast", tags=["Forecast"])
app.include_router(dashboard.router, prefix="/dashboard", tags=["Dashboard"])

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "Sales Intelligence API running"}

@app.on_event("startup")
def startup():
    init_db()

@app.get("/sales/weekly")
def get_weekly_sales():
    return [
        {"day": "Mon", "sales": 120},
        {"day": "Tue", "sales": 210},
        {"day": "Wed", "sales": 150},
        {"day": "Thu", "sales": 300},
        {"day": "Fri", "sales": 280},
        {"day": "Sat", "sales": 350},
        {"day": "Sun", "sales": 410},
    ]

@app.get("/sales/kpis")
def get_sales_kpis():
    weekly_sales = [
        {"day": "Mon", "sales": 120},
        {"day": "Tue", "sales": 210},
        {"day": "Wed", "sales": 150},
        {"day": "Thu", "sales": 300},
        {"day": "Fri", "sales": 280},
        {"day": "Sat", "sales": 350},
        {"day": "Sun", "sales": 410},
    ]

    total = sum(d["sales"] for d in weekly_sales)
    avg = total / len(weekly_sales)
    best = max(weekly_sales, key=lambda x: x["sales"])
    worst = min(weekly_sales, key=lambda x: x["sales"])

    return {
        "total_sales": total,
        "average_sales": round(avg, 2),
        "best_day": best["day"],
        "best_day_sales": best["sales"],
        "worst_day": worst["day"],
        "worst_day_sales": worst["sales"]
    }

