from pydantic import BaseModel, EmailStr
from typing import Optional, List
from app.schemas.schemas import StudentBase

class SubjectBase(BaseModel):
    name: str

    class Config:
        orm_mode = True

class SubjectSchoolAndTeacher(BaseModel):
    subject_name: str

    class Config:
        orm_mode = True

class RegisterSubjectForStudent(BaseModel):
    test_score: int
    exam_score: int
    subject_name: str
    school_id: str
    student_id: str

    class Config:
        orm_mode = True

class RegisterSubjectForSchool(BaseModel):
    subject_name: str
    school_id: str

    class Config:
        orm_mode = True

class RegisterSubjectForTeacher(BaseModel):
    subject_name: str
    school_id: str
    teacher_id: str

    class Config:
        orm_mode = True

class SubjectOffering(BaseModel):
    id: str
    test_score: int
    exam_score: int
    subject_name: str
    school_id: str
    student_id: str
    student: StudentBase

    class Config:
        orm_mode = True

class UploadResults(BaseModel):
    test_score: int
    exam_score: int
    student_id: str
    name: str 
    
    class Config:
        orm_mode = True