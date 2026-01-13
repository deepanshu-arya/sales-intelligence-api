import razorpay
from app.config import RAZORPAY_KEY_ID, RAZORPAY_KEY_SECRET, PRO_PRICE

client = razorpay.Client(
    auth=(RAZORPAY_KEY_ID, RAZORPAY_KEY_SECRET)
)

def create_order(user_id: int):
    return client.order.create({
        "amount": PRO_PRICE * 100,  # paise
        "currency": "INR",
        "payment_capture": 1,
        "notes": {
            "user_id": user_id,
            "plan": "pro"
        }
    })
