from fastapi import APIRouter
from datetime import datetime
from web.users.dao import UserDAO
from web.users.user_dto import UserRequestDto, UserResponseDto
from web.users.models import Users


router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/")
async def get_users_info():
    """
    Эндпоинт получения всех пользователей
    """
    return await UserDAO.get_all()


@router.get("user/{key}")
async def get_user_info(key: int) -> UserResponseDto:
    """
    Эндпоинт получения пользователя
    """
    
    return await UserDAO.get_by_id(key)


@router.post("/register")
async def registrate_user(dto: UserRequestDto):
    """
    Эндпоинт регистрации пользователя
    """

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
    )
    
    await UserDAO.add(**response.model_dump())
    
@router.delete("/delete")
async def delete_user(id: int):
    await UserDAO.delete(id)