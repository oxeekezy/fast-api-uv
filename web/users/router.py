from fastapi import APIRouter
from datetime import datetime
from web.users.user_dto import UserRequestDto, UserResponseDto


router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/{key}")
def get_user_info(key: int) -> UserResponseDto:
    """
    Эндпоинт получения пользователя
    """

    response = UserResponseDto(
        firstname="testov",
        lastname="test",
        middlename=None,
        email="test.api@api.com",
        tel="+7-981-555-45-17",
        birthday=datetime(1990, 3, 10),
        login=f"testov_{key}",
        age=25,
        reg_date=datetime(9999, 3, 10),
    )

    return response


@router.post("/")
def registrate_user(dto: UserRequestDto) -> UserResponseDto:
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

    return response
