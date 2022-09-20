import re
from typing import List
from fastapi import APIRouter, status, HTTPException, Depends

from app.oauth2 import get_current_teacher
from ..schemas import teacher_schema, subject_schema
from .. import models
from ..db import get_db
from sqlalchemy import func
from sqlalchemy.orm import Session
from .. import utils

router = APIRouter(
    prefix="/teachers",
    tags=['teachers']
)

@router.get("/", response_model=List[teacher_schema.TeacherResponse])
def get_teachers(db: Session = Depends(get_db)):
    teachers = db.query(models.Teacher).all()
    print(teachers)
    
    return teachers

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=teacher_schema.TeacherResponse)
def create_teacher(teacher: teacher_schema.TeacherCreate, db: Session = Depends(get_db)):
    
    #hash the password
    teacher.password = utils.hash_password(teacher.password)
    
    new_teacher = models.Teacher(**teacher.dict())
    db.add(new_teacher)
    db.commit()
    db.refresh(new_teacher)

    return new_teacher

@router.post("/AdminCreateTeacher", status_code=status.HTTP_201_CREATED, response_model=teacher_schema.TeacherResponse)
def create_teacher(teacher: teacher_schema.AdminTeacherCreate, db: Session = Depends(get_db)):
    teacher_dict = teacher.dict()
    #hash the password
    teacher_dict.password = utils.hash_password(teacher_dict.password)

    subjects = teacher_dict['subjects']
    del teacher_dict['subjects']
    
    new_teacher = models.Teacher(**teacher_dict)
    db.add(new_teacher)
    db.commit()
    db.refresh(new_teacher)

    new_teacher_dict = models.object_as_dict(new_teacher)
    for subject in subjects:
        new_subject_offered = models.SubjectTakenByTeacher(
                subject_name = subject,
                teacher_id = new_teacher_dict["id"],
                school_id = teacher_dict["school_id"]
                )
        db.add(new_subject_offered)
        db.commit()
        db.refresh(new_subject_offered)

    return new_teacher

"""
    get a teacher within the teacher dashboard
    by passing only the access token
"""
@router.get("/GetTeacher", response_model=teacher_schema.TeacherResponse)
def get_teacher(db: Session = Depends(get_db), current_user: str = Depends(get_current_teacher)):
    id = current_user.dict()['id']
    teacher = db.query(models.Teacher).filter(models.Teacher.id == id).first()

    if not teacher:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Teacher with id: {id} does not exist")

    return teacher

@router.get("/ViewClassroom/{subject_name}", response_model= List[subject_schema.SubjectOffering])
def get_students_for_teacher(subject_name: str, db: Session = Depends(get_db), 
        current_user: str = Depends(get_current_teacher)):

    id = current_user.dict()['id']

    teacher = models.object_as_dict(db.query(models.Teacher).filter(models.Teacher.id == id).first())
    
    classroom = db.query(models.SubjectOfferedByStudent).filter(
            models.SubjectOfferedByStudent.school_id == teacher['school_id'], 
            models.SubjectOfferedByStudent.subject_name == subject_name).all()

    subjects_dict = []
    print(classroom)
    # for subject in classroom:
    #     subject = models.object_as_dict(subject)
    #     subjects_dict.append(subject)

    return classroom


@router.patch("/UploadResults/{subject_name}")
def upload_results(subject_name: str, results: List[subject_schema.UploadResults], 
        db: Session = Depends(get_db), 
        current_user: str = Depends(get_current_teacher)):
    id = current_user.dict()['id']

    for result in results:
        result = result.dict()

        result_in_db = db.query(models.SubjectOfferedByStudent).filter(
            models.SubjectOfferedByStudent.student_id == result['student_id'],
            models.SubjectOfferedByStudent.subject_name == subject_name).first()

        # print(models.object_as_dict(result_in_db))

        result_in_db.test_score = result['test_score']
        result_in_db.exam_score = result['exam_score']
        db.commit()
        db.refresh(result_in_db)
        print(models.object_as_dict(result_in_db))

    teacher = models.object_as_dict(db.query(models.Teacher).filter(models.Teacher.id == id).first())
    
    classroom = db.query(models.SubjectOfferedByStudent).filter(
            models.SubjectOfferedByStudent.school_id == teacher['school_id'], 
            models.SubjectOfferedByStudent.subject_name == subject_name).all()

    return classroom

    

@router.get("/{id}", response_model=teacher_schema.TeacherResponse)
def get_teacher(id: str, db: Session = Depends(get_db)):
    user = db.query(models.Teacher).filter(models.Teacher.id == id).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User teacher with id: {id} does not exist")

    return user
