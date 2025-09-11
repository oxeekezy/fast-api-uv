from typing import Sequence
from fastapi import APIRouter, Depends
from web.auth.scheme import get_bearer_token
from web.courses.course_dto import CourseRequestDto, CourseResponseDto
from web.courses.dao import CourseDAO
from web.exceptions import CouseAlreadyExistException, CouseNotExistException


router = APIRouter(prefix="/courses", tags=["Courses"])

SECURITY = [Depends(get_bearer_token)]


@router.get("")
async def get_all() -> Sequence[CourseResponseDto]:
    """Эндпоинт получения всех курсов

    Returns:
        Sequence[CourseResponseDto]: Список курсов.
    """
    return await CourseDAO.get_all()

@router.get("/{id}")
async def get_by_id(id: int) -> CourseResponseDto | None:
    """Эндпоинт получения всех курсов

    Returns:
        Sequence[CourseResponseDto]: Список курсов.
    """
    return await CourseDAO.get_by_id(id)

@router.post("/add", status_code=201)
async def add_course(dto: CourseRequestDto):
    """Эндпоинт добавления курса

    Args:
        dto (CourseRequestDto): DTO добавляемого курса (request объект).

    Raises:
        CouseAlreadyExistException: Исключение, возникающее при добавлении 
        уже существующего курса.
    """
    existed = await CourseDAO.get_by_params(name=dto.name)
    
    if existed:
        raise CouseAlreadyExistException
    
    await CourseDAO.add(**dto.model_dump())
    
    
@router.delete("/delete", status_code=200)
async def delete_course(id: int):
    """"Эндпоинт удаления курса

    Args:
        id (int): идентификатор курса.
    """
    await CourseDAO.delete(id)
    

@router.put("/edit")
async def edit_course(id: int, dto: CourseRequestDto):
    """Эндпоинт редактирования курса

    Args:
        id (int): идентификатор курса;
        dto (CourseRequestDto): DTO c обновленными записями.

    Raises:
        CouseNotExistException: Исключение, возникающее при редактировании несуществующей 
        записи.
    """
    course = await CourseDAO.get_by_id(id)
    if not course:
        raise CouseNotExistException
    
    await CourseDAO.update(id, **dto.model_dump())
    
