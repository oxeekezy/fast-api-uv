from pydantic import BaseModel, EmailStr
from typing import Optional


class CourseRequestDto(BaseModel):
    name: str
    desc: Optional[str]
    duration: int
    teacher: str
    
    
class CourseResponseDto(BaseModel):
    id:int
    name: str
    desc: Optional[str]
    duration: int
    teacher: str
    
class LectorResponseDto(BaseModel):
    firstname: str
    lastname: str
    middlename: Optional[str]
    email: Optional[EmailStr]