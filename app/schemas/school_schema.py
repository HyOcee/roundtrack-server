from datetime import datetime
from typing import List

from .subject_schema import SubjectSchoolAndTeacher
from .schemas import SchoolBase, StudentBase, TeacherBase

class CreateSchool(SchoolBase):
    administrator_email: str
    password: str
    pass

class UpdateSchool(SchoolBase):
    administrator_email: str
    password: str
    address: str
    pass

class SchoolResponse(SchoolBase):
    id: str
    created_at: datetime
    administrator_email: str
    teachers: List[TeacherBase]
    students: List[StudentBase]
    subjects: List[SubjectSchoolAndTeacher]

    class Config:
        orm_mode = True