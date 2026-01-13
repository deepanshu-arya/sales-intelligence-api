from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware
from fastapi.responses import JSONResponse
from fastapi import FastAPI, Request
from app.database import engine, Base, init_db
from app.routers import sales, analytics, forecast, dashboard
from app.auth import auth
from fastapi.middleware.cors import CORSMiddleware
from app.api_keys.router import router as api_key_router
from app.billing.webhook import router as billing_webhook
from app.admin.router import router as admin_router
from app.billing.router import router as billing_router
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Sales Intelligence API")

templates = Jinja2Templates(directory="app/templates")
app.mount("/static", StaticFiles(directory="app/static"), name="static")

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_middleware(SlowAPIMiddleware)


app.include_router(auth.router)
app.include_router(sales.router, prefix="/sales", tags=["Sales"])
app.include_router(analytics.router, prefix="/analytics", tags=["Analytics"])
app.include_router(forecast.router, prefix="/forecast", tags=["Forecast"])
app.include_router(dashboard.router, prefix="/dashboard", tags=["Dashboard"])
app.include_router(api_key_router)
app.include_router(billing_webhook)
app.include_router(admin_router)
app.include_router(billing_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.exception_handler(RateLimitExceeded)
def rate_limit_handler(request, exc):
    return JSONResponse(
        status_code=429,
        content={"detail": "Rate limit exceeded"}
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

@app.get("/_page")
def landing_page(request: Request):
    return templates.TemplateResponse(
        "index.html",
        {"request": request}
    )

@app.get("/__debug")
def debug():
    return {"app": "THIS IS MY FASTAPI APP"}


