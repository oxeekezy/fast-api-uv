from typing import Optional
from fastapi import Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from web.exceptions import UserNotAuth
from web.settings import settings


known_tokens = {
    settings.BEARER_TOKEN,
    }

async def get_bearer_token(
    auth: Optional[HTTPAuthorizationCredentials] = Depends(HTTPBearer(auto_error=False))
    )->str:
    if auth is None or (token := auth.credentials) not in known_tokens:
        raise UserNotAuth
    return token