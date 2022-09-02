from fastapi import APIRouter, status, HTTPException, Depends
from .. import models, schemas
from ..db import get_db
from sqlalchemy.orm import Session
from .. import utils

router = APIRouter(
    prefix="/teachers",
    tags=['teachers']
)

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.TeacherResponse)
def create_teacher(teacher: schemas.TeacherCreate, db: Session = Depends(get_db)):
    
    #hash the password
    teacher.password = utils.hash_password(teacher.password)
    
    new_teacher = models.Teacher(**teacher.dict())
    db.add(new_teacher)
    db.commit()
    db.refresh(new_teacher)

    return new_teacher

@router.get("/{id}", response_model=schemas.TeacherResponse)
def get_teacher(id: int, db: Session = Depends(get_db)):
    user = db.query(models.Teacher).filter(models.Teacher.id == id).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User teacher with id: {id} does not exist")

    return user