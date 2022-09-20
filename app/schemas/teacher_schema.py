from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, EmailStr
from typing import Optional, List

from .subject_schema import SubjectBase, SubjectSchoolAndTeacher
from .schemas import SchoolBase, TeacherBase


class TeacherCreate(TeacherBase):
    school_id: str
    password: str

class AdminTeacherCreate(BaseModel):
    firstName: str
    lastName: str

    class Config:
        orm_mode = True

class TeacherResponse(TeacherBase):
    id: str
    created_at: datetime

    school: SchoolBase
    subjects: List[SubjectSchoolAndTeacher]

    class Config:
        orm_mode = True
