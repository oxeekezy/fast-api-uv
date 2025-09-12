from typing import Sequence
from fastapi import APIRouter, Depends
from web.auth.scheme import get_bearer_token
from web.courses.course_dto import CourseRequestDto, CourseResponseDto, LectorResponseDto
from web.courses.dao import CourseDAO, CourseLectorsDAO
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
    
    
@router.post("/add_lector", status_code=201)
async def add_lector_to_course(
    course_id: int, 
    lector_id: int):
    
    await CourseLectorsDAO.add_lector(course_id=course_id, lector_id=lector_id)
    
    
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
    

@router.get("/lectors/{course_id}")
async def get_course_lectors(course_id: int) -> Sequence[LectorResponseDto] | None:
    """Эндпоинт получения всех курсов

    Returns:
        Sequence[CourseResponseDto]: Список курсов.
    """
    return await CourseLectorsDAO.get_lectors_for_course(course_id=course_id)

@router.get("/lector/{lector_id}")
async def get_course_lectors(lector_id: int) -> Sequence[CourseResponseDto] | None:
    """Эндпоинт получения всех курсов

    Returns:
        Sequence[CourseResponseDto]: Список курсов.
    """
    return await CourseLectorsDAO.get_courses_for_lector(lector_id=lector_id)
    
