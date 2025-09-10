from fastapi import Depends, Request
from jose import jwt, JWTError
from web.exceptions import TokenExpired, TokenDecodeExcept
from web.settings import settings
from web.users.dao import UserDAO


def get_token_from_request(request: Request):
    token = request.cookies.get("access_token")
    if not token:
        raise TokenExpired
    return token

async def get_user_from_token(token: str = Depends(get_token_from_request)):
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            settings.JWT_ALG
        )
    except JWTError:
        raise TokenDecodeExcept
        
    user_id: int = int(payload.get("sub"))
    user = await UserDAO.get_by_id(user_id)
    
    return user