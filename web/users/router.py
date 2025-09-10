from typing import Any, Sequence, Annotated
from fastapi import APIRouter, Depends, Query, Request, Response
from datetime import datetime

from web.auth.scheme import get_bearer_token
from web.users.dao import UserDAO
from web.users.user_dto import UserLoginRequestDto, UserRequestByParamsDto, UserRequestDto, UserResponseDto
from web.users.models import UserModel
from web.exceptions import UserExistException

from web.users.auth import auth_user, create_token, get_password_hash
from web.users.deps import get_user_from_token


router = APIRouter(prefix="/users", tags=["Users"])

SECURITY = [Depends(get_bearer_token)]

@router.get("/", dependencies=SECURITY)
async def get_users_info()-> Sequence[UserResponseDto]:
    """
    Эндпоинт получения всех пользователей
    """
    return await UserDAO.get_all()

@router.get("/get_by_params", dependencies=SECURITY)
async def get_users_info_by_params(user: Annotated[UserRequestByParamsDto, Query()]) -> Sequence[UserResponseDto]: 
    """
    Эндпоинт получения пользователей  по параметрам
    """
    
    return await UserDAO.get_by_params(**user.model_dump(exclude_defaults=True, exclude_unset=True, exclude_none=True))


@router.get("/user/{key}", dependencies=SECURITY)
async def get_user_info(key: int) -> UserResponseDto:
    """
    Эндпоинт получения пользователя
    """
    
    return await UserDAO.get_by_id(key)


@router.post("/register", status_code=201)
async def registrate_user(dto: UserRequestDto) -> UserResponseDto:
    """
    Эндпоинт регистрации пользователя
    """
    
    exsited = await UserDAO.get_by_params(email=dto.email)
    if exsited:
        raise UserExistException
    
    #TODO: Убрать response dto из add. Тогда можно будет избавиться от пароля в response
    hashed_pwd = get_password_hash(dto.password)
    
    response = UserResponseDto(
        firstname=dto.firstname,
        lastname=dto.lastname,
        middlename=dto.middlename,
        email=dto.email,
        tel=dto.tel,
        birthday=dto.birthday,
        login=dto.login,
        age=dto.age,
        reg_date=datetime.now(),
        password=hashed_pwd
    )
    
    await UserDAO.add(**response.model_dump())
    return response
    
@router.delete("/delete", status_code=200, dependencies=SECURITY)
async def delete_user(id: int):
    await UserDAO.delete(id)
    
@router.post("/login")
async def login(response: Response, dto: UserLoginRequestDto):
    user = await auth_user(dto.email, dto.password)
    access_token = create_token({"sub": str(user.id)})
    response.set_cookie("access_token", access_token)

    return {"access_token": access_token}

@router.post("/me", dependencies=SECURITY)
async def get_user_from_token(user: str = Depends(get_user_from_token)) -> UserResponseDto:
    return user
    
    