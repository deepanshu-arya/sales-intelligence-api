from fastapi import APIRouter, Depends
from app.billing.razorpay import create_order
from app.auth.security import get_current_user

router = APIRouter(prefix="/billing", tags=["Billing"])

@router.post("/create-order")
def create_payment_order(current_user = Depends(get_current_user)):
    order = create_order(current_user.id)
    return {
        "order_id": order["id"],
        "amount": order["amount"],
        "currency": order["currency"],
        "key": "RAZORPAY_KEY_ID"  # frontend uses this
    }
