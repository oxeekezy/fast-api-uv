from pydantic import BaseModel
from typing import Optional


class CourseRequestDto(BaseModel):
    name: str
    desc: Optional[str]
    duration: int
    teacher: str
    
    
class CourseResponseDto(BaseModel):
    name: str
    desc: Optional[str]
    duration: int
    teacher: str