from web.database import Base
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import mapped_column, Mapped, relationship


class CourseModel(Base):
    __tablename__="course"
    
    id = Column(Integer, primary_key=True)
    
    name = Column(String, nullable=False, unique=True)
    desc = Column(String, nullable=True)
    duration = Column(Integer, nullable=False)
    teacher = Column(String, nullable=False)
    
    course_lector = relationship("CourseLectors", uselist=True, back_populates="course")
    
class CourseLectors(Base):
    __tablename__="course_lectors"
    id = Column(Integer, primary_key=True)
    
    course_id = Column(Integer, ForeignKey('course.id'))
    course = relationship("CourseModel", back_populates="course_lector")
    
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship("UserModel", back_populates="course_lector")
    