from fastapi import APIRouter, Response, status, HTTPException, Depends

from ..schemas import schemas
from .. import models, db, utils, oauth2
from sqlalchemy.orm import Session
from typing import List

router = APIRouter(
    prefix="/auth",
    tags=['Authentication']
)

@router.post('/schoolAdminLogin')
def login(login_credentials: schemas.AdminLogin, db: Session = Depends(db.get_db)):
    school = db.query(models.School).filter(models.School.administrator_email == login_credentials.administrator_email).first()

    if not school:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid login credentials")

    if not utils.verify_password(login_credentials.password, school.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid login credentials")


    access_token = oauth2.create_access_token(data = {"school_id": school.id})
    return {"access_token": access_token, "token_type": "bearer"}

@router.post('/teacherLogin')
def login(login_credentials: schemas.Login, db: Session = Depends(db.get_db)):
    teacher = db.query(models.Teacher).filter(models.Teacher.username == login_credentials.username).first()

    if not teacher:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid login credentials")

    if not utils.verify_password(login_credentials.password, teacher.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid login credentials")


    access_token = oauth2.create_access_token(data = {"teacher_id": teacher.id})
    return {"access_token": access_token, "token_type": "bearer"}

@router.post('/studentLogin')
def login(login_credentials: schemas.Login, db: Session = Depends(db.get_db)):
    student = db.query(models.Student).filter(models.Student.username == login_credentials.username).first()

    if not student:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid login credentials")

    if not utils.verify_password(login_credentials.password, student.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid login credentials")


    access_token = oauth2.create_access_token(data = {"student_id": student.id})
    return {"access_token": access_token, "token_type": "bearer"}