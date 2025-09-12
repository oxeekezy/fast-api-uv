from sqlalchemy import insert, select
from web.dao.base import BaseDAO
from web.courses.models import CourseLectors, CourseModel
from web.database import ASYNC_SESSION_MAKER
from web.exceptions import CouseNotExistException, UserNotExistException
from web.users.dao import UserDAO
from sqlalchemy.orm import selectinload


class CourseDAO(BaseDAO):
    model = CourseModel
    
class CourseLectorsDAO(BaseDAO):
    model = CourseLectors
    
    @classmethod
    async def add_lector(cls, course_id: int, lector_id: int):
        async with ASYNC_SESSION_MAKER() as session:
            course_query = await CourseDAO.get_by_id(course_id)
            if not course_query:
                raise CouseNotExistException
            
            user_query = await UserDAO.get_by_id(lector_id)
            if not user_query:
                raise UserNotExistException
            
            
            query = insert(cls.model).values(course_id=course_id, user_id=lector_id)
            await session.execute(query)
            await session.commit()
    
    @classmethod
    async def get_lectors_for_course(cls, course_id: int):
        async with ASYNC_SESSION_MAKER() as session:
            query = select(cls.model).filter_by(course_id=course_id).options(selectinload(cls.model.user))
            result = await session.execute(query)
            lectors = [x.user for x in result.scalars().all()]

            return lectors
        

    @classmethod
    async def get_courses_for_lector(cls, lector_id:int):
        async with ASYNC_SESSION_MAKER() as session:
            query = select(cls.model).filter_by(user_id=lector_id).options(selectinload(cls.model.course))
            result = await session.execute(query)
            courses = [x.course for x in result.scalars().all()]
            
            return courses