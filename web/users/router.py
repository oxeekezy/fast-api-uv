from typing import Any, Sequence, Annotated
from fastapi import APIRouter, Query
from datetime import datetime

from web.users.dao import UserDAO
from web.users.user_dto import UserRequestByParamsDto, UserRequestDto, UserResponseDto
from web.users.models import Users
from web.exceptions import UserExistException


router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/")
async def get_users_info()-> Sequence[UserResponseDto]:
    """
    Эндпоинт получения всех пользователей
    """
    return await UserDAO.get_all()

@router.get("/get_by_params")
async def get_users_info_by_params(user: Annotated[UserRequestByParamsDto, Query()] ) -> Sequence[UserResponseDto]: 
    """
    Эндпоинт получения пользователей  по параметрам
    """
    
    return await UserDAO.get_by_params(**user.model_dump(exclude_defaults=True, exclude_unset=True, exclude_none=True))


@router.get("/user/{key}")
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
        password=dto.password
    )
    
    await UserDAO.add(**response.model_dump())
    return response
    
@router.delete("/delete")
async def delete_user(id: int):
    await UserDAO.delete(id)