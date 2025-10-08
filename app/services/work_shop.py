from fastapi import Depends, HTTPException
from app.models.work_shops import WorkShop
from app.services.security.security import oauth2_scheme, verify_token


def fake_decode_token(token):
    # Improved fake decode token function
    payload = verify_token(token)
    if payload is None:
        raise HTTPException(status_code=401, detail="Could not validate credentials")
    
    # Return a dictionary with the payload data instead of trying to create a WorkShop object
    return {
        "work_shop_name": payload.get("sub", "Unknown"),
        "email": payload.get("email", "unknown@example.com"),
        "full_name": payload.get("full_name", "Unknown User")
    }

async def get_current_work_shop(token: str = Depends(oauth2_scheme)):
    if not token:
        raise HTTPException(status_code=401, detail="Not authenticated")
    return fake_decode_token(token)