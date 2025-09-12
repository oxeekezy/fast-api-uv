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

from fastapi_cache.decorator import cache


router = APIRouter(prefix="/users", tags=["Users"])

SECURITY = [Depends(get_bearer_token)]

@router.get("", dependencies=SECURITY)
@cache(expire=60)
async def get_users_info()-> Sequence[UserResponseDto]:
    """Эндпоинт получения всех пользователей

    Returns:
        Sequence[UserResponseDto]: список пользователей.
    """
    return await UserDAO.get_all()

@router.get("/get_by_params", dependencies=SECURITY)
async def get_users_info_by_params(user: Annotated[UserRequestByParamsDto, Query()]) -> Sequence[UserResponseDto]: 
    """Эндпоинт получения пользователей по указанным параметрам

    Args:
        user (Annotated[UserRequestByParamsDto, Query): заполенная модель поиска пользователя.

    Returns:
        Sequence[UserResponseDto]: список пользователей.
    """
    
    return await UserDAO.get_by_params(**user.model_dump(exclude_defaults=True, exclude_unset=True, exclude_none=True))


@router.get("/user/{key}", dependencies=SECURITY)
async def get_user_info(key: int) -> UserResponseDto:
    """Эндпоинт получения пользователя по id 

    Args:
        key (int): Уникальный идентификатор пользователя

    Returns:
        UserResponseDto: DTO объект пользователя
    """
    
    return await UserDAO.get_by_id(key)


@router.post("/register", status_code=201)
async def registrate_user(dto: UserRequestDto) -> UserResponseDto:
    """Эндпоинт регистрации пользователя

    Args:
        dto (UserRequestDto): DTO регестрируемого пользователя.

    Raises:
        UserExistException: Исключение, возникающее при регистрации существующего пользователя.

    Returns:
        UserResponseDto: DTO зарегестрированного пользователя.
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
    """Эндпоинт удаления пользователя

    Args:
        id (int): Уникальный идентификатор пользователя.
    """
    await UserDAO.delete(id)
    
@router.post("/login")
async def login(response: Response, dto: UserLoginRequestDto):
    """Эндпоинт авторизации пользователя

    Args:
        response (Response): объект httpResponse;
        dto (UserLoginRequestDto): DTO объект авторизации пользователя.

    Returns:
        Dict: словарь с ключом access_token в котором установлен JWT токен.
    """
    user = await auth_user(dto.email, dto.password)
    access_token = create_token({"sub": str(user.id)})
    response.set_cookie("access_token", access_token)

    return {"access_token": access_token}

@router.post("/me", dependencies=SECURITY)
async def get_user_from_token(user: str = Depends(get_user_from_token)) -> UserResponseDto:
    """Эндпоинт получения информации об авторизированном пользователе

    Args:
        user (str, optional): пользователь из токена. Зависимость от Depends(get_user_from_token).

    Returns:
        UserResponseDto: DTO объект пользователя.
    """
    return user
    
    