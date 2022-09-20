from typing import List
from fastapi import APIRouter, status, HTTPException, Depends

from app.oauth2 import get_current_student
from ..schemas import student_schema
from .. import models
from ..db import get_db
from sqlalchemy.orm import Session
from .. import utils

router = APIRouter(
    prefix="/students",
    tags=['students']
)

@router.get("/", response_model=List[student_schema.StudentResponse])
def get_students(db: Session = Depends(get_db)):
    students = db.query(models.Student).all()
    
    return students

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=student_schema.StudentResponse)
def create_student(student: student_schema.StudentCreate, db: Session = Depends(get_db)):
    
    #hash the password
    student.password = utils.hash_password(student.password)
    
    new_student = models.Student(**student.dict())
    db.add(new_student)
    db.commit()
    db.refresh(new_student)

    return new_student

"""
    get a student info within the student dashboard
    by passing only the access token
"""
@router.get("/GetStudent", response_model=student_schema.StudentResponse)
def get_student(db: Session = Depends(get_db), current_user: str = Depends(get_current_student)):
    id = current_user.dict()['id']
    print(id)
    student = db.query(models.Student).filter(models.Student.id == id).first()

    if not student:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Student with id: {id} does not exist")

    return student

@router.get("/{id}", response_model=student_schema.StudentResponse)
def get_student(id: str, db: Session = Depends(get_db)):
    student = db.query(models.Student).filter(models.Student.id == id).first()

    if not student:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Student with id: {id} does not exist")

    return student