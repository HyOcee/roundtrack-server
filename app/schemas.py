from datetime import datetime
from pydantic import BaseModel, EmailStr
from typing import Optional

class SchoolBase(BaseModel):
    name: str
    administrator_email: str
    address: str

class CreateSchool(SchoolBase):
    password: str
    pass

class UpdateSchool(SchoolBase):
    pass

class SchoolResponse(SchoolBase):
    id: int
    created_at: datetime
    name: str
    administrator_email: str

    class Config:
        orm_mode = True
        
class TeacherCreate(BaseModel):
    email: str
    password: str
    name: str

class TeacherResponse(BaseModel):
    id: int
    email: str
    created_at: datetime
    name: str

    class Config:
        orm_mode = True

class Login(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[str] = None