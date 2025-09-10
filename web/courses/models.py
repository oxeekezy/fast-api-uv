from web.database import Base
from sqlalchemy import Column, Integer, String


class CourseModel(Base):
    __tablename__="course"
    
    id = Column(Integer, primary_key=True)
    
    name = Column(String, nullable=False, unique=True)
    desc = Column(String, nullable=True)
    duration = Column(Integer, nullable=False)
    teacher = Column(String, nullable=False)