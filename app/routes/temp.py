from typing import List
from fastapi import APIRouter, status, HTTPException, Depends
from ..schemas import subject_schema
from .. import models
from ..db import get_db
from sqlalchemy.orm import Session
from .. import utils

router = APIRouter(
    prefix="/temp",
    tags=['temp']
)

@router.get("/StudentRegisterSubject", response_model=List[subject_schema.RegisterSubjectForStudent])
def get_subjects_for_students(db: Session = Depends(get_db)):
    subjects_offered = db.query(models.SubjectOfferedByStudent).all()
    
    return subjects_offered

@router.post("/", status_code=status.HTTP_201_CREATED)
def create_subject(subject: subject_schema.RegisterSubjectForStudent, db: Session = Depends(get_db)):
    new_subject_offered = models.SubjectOfferedByStudent(**subject.dict())
    db.add(new_subject_offered)
    db.commit()
    db.refresh(new_subject_offered)

    return new_subject_offered

@router.post("/school_subject", status_code=status.HTTP_201_CREATED)
def create_subject(subject: subject_schema.RegisterSubjectForSchool, db: Session = Depends(get_db)):
    new_subject_offered = models.SubjectOfferedBySchool(**subject.dict())
    db.add(new_subject_offered)
    db.commit()
    db.refresh(new_subject_offered)

    return new_subject_offered

@router.post("/teacher_subject", status_code=status.HTTP_201_CREATED)
def create_subject(subject: subject_schema.RegisterSubjectForTeacher, db: Session = Depends(get_db)):
    new_subject_offered = models.SubjectTakenByTeacher(**subject.dict())
    db.add(new_subject_offered)
    db.commit()
    db.refresh(new_subject_offered)

    return new_subject_offered