from typing import List
from fastapi import APIRouter, status, HTTPException, Depends
from ..schemas import subject_schema
from .. import models
from ..db import get_db
from sqlalchemy.orm import Session
from .. import utils

router = APIRouter(
    prefix="/subjects",
    tags=['subjects']
)

@router.get("/", response_model=List[subject_schema.SubjectBase])
def get_subjects(db: Session = Depends(get_db)):
    subjects = db.query(models.Subject).all()
    
    return subjects

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=subject_schema.SubjectBase)
def create_subject(subject: subject_schema.SubjectBase, db: Session = Depends(get_db)):
    
    new_subject = models.Subject(**subject.dict())
    db.add(new_subject)
    db.commit()
    db.refresh(new_subject)

    return new_subject
