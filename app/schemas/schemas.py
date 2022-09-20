from pydantic import BaseModel
from typing import Optional, List

class SchoolBase(BaseModel):
    name: str

    class Config:
        orm_mode = True

class TeacherBase(BaseModel):
    username: str
    firstName: str
    lastName: str

    class Config:
        orm_mode = True

class StudentBase(BaseModel):
    username: str
    firstName: str
    lastName: str
    school_id: str

    class Config:
        orm_mode = True

class AdminLogin(BaseModel):
    administrator_email: str
    password: str

class Login(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[str] = None