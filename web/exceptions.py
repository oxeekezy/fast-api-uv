from fastapi import HTTPException, status


class BaseException(HTTPException):
    status_code = 500
    detail = ""
    
    def __init__(self):
      super().__init__(status_code=self.status_code, detail=self.detail)

class UserExistException(BaseException):
    status_code = status.HTTP_409_CONFLICT
    detail="Пользователь уже существует"
    
class UserAuthFailed(BaseException):
    status_code = status.HTTP_400_BAD_REQUEST
    detail="Неправильный логин или пароль"
    
class TokenExpired(BaseException):
    status_code = status.HTTP_400_BAD_REQUEST
    detail="Время жизни JWT токена истекло или он отсутствует"

class UserNotAuth(BaseException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail="Пользователь не авторизован"
    
class TokenDecodeExcept(BaseException):
    status_code = status.HTTP_400_BAD_REQUEST
    detail="Проблема вовремя декодирования токена"