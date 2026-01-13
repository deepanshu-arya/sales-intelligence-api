from fastapi import HTTPException
from app.api_keys.model import APIKey
from app.models import User

PLAN_LIMITS = {
    "free": 100,
    "pro": 10000,
    "enterprise": 10**9
}

def enforce_subscription(api_key: APIKey, user: User):
    limit = PLAN_LIMITS.get(user.plan, 0)

    if api_key.usage_count >= limit:
        raise HTTPException(
            status_code=402,
            detail="API limit exceeded. Please upgrade your plan."
        )
