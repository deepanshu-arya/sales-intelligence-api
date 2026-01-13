import os
from dotenv import load_dotenv

load_dotenv()

RAZORPAY_KEY_ID = os.getenv("RAZORPAY_KEY_ID")
RAZORPAY_KEY_SECRET = os.getenv("RAZORPAY_KEY_SECRET")
PRO_PRICE = int(os.getenv("PRO_PRICE", 999))
SUBSCRIPTION_DAYS = int(os.getenv("SUBSCRIPTION_DAYS", 30))
