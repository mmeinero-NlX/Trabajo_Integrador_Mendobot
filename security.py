from fastapi import Depends, HTTPException
from fastapi.security import APIKeyHeader

API_KEY = "test-key-2026"
header = APIKeyHeader(name="X-API-Key")


def verify_api_key(key: str = Depends(header)):
    if key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API key")