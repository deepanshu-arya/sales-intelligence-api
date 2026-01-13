from fastapi import Security, HTTPException, status
from fastapi.security.api_key import APIKeyHeader

API_KEY = "test-api-key-123"  # later put in env

api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)

def validate_api_key(api_key: str = Security(api_key_header)):
    if api_key != API_KEY:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid or missing API Key"
        )
    return api_key
