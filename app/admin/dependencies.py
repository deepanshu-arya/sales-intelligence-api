from fastapi import Header, HTTPException
import os

def verify_admin(x_admin_key: str = Header(...)):
    if x_admin_key != os.getenv("ADMIN_API_KEY"):
        raise HTTPException(status_code=403, detail="Admin access denied")
