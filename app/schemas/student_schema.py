from datetime import datetime
from typing import List
from .schemas import SchoolBase, StudentBase
from .subject_schema import RegisterSubjectForStudent
from pydantic import BaseModel

class StudentCreate(StudentBase):
    password: str

    class Config:
        orm_mode = True

class AdminStudentCreate(BaseModel):
    firstName: str
    lastName: str

    class Config:
        orm_mode = True

class StudentResponse(StudentBase):
    id: str
    created_at: datetime

    school: SchoolBase
    subjects: List[RegisterSubjectForStudent]

    class Config:
        orm_mode = True