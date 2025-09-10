from passlib.context import CryptContext
from pydantic import EmailStr

from web.exceptions import UserAuthFailed
from web.users.dao import UserDAO

from jose import jwt
from web.settings import settings
from datetime import datetime, timedelta


pwd_context=CryptContext(schemes=settings.PASS_CRYPT_SCHEMES, deprecated="auto")


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)
    
def verify_password(secret: str, hashed: str):
    return pwd_context.verify(secret=secret, hash=hashed)

async def auth_user(email: EmailStr, password: str):
    user = await UserDAO.get_user_by_email(email=email)
    
    if not (user and verify_password(password, user.password)):
        raise UserAuthFailed
    
    return user

def create_token(data: dict)->str:
    to_encode = data.copy()
    expire = datetime.now() + timedelta(minutes=20)
    to_encode.update({"exp": expire})
    
    token = jwt.encode(
        to_encode,
        settings.SECRET_KEY, 
        settings.JWT_ALG
    )
    
    return token
    