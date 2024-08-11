from fastapi import Depends, HTTPException
from shared.auth.jwt_handler import verify_access_token
from shared.auth.oauth2 import oauth2_scheme

def get_current_user(token: str = Depends(oauth2_scheme)):
    payload = verify_access_token(token)
    user_id: int = payload.get("user_id")
    if not user_id:
        raise HTTPException(status_code=401, detail="Invalid token")
    return user_id
