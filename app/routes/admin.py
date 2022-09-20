from fastapi import APIRouter, Response, status, HTTPException, Depends
from ..schemas import school_schema, teacher_schema, student_schema
from .. import models, utils, db
from sqlalchemy.orm import Session
from typing import List
from ..oauth2 import get_current_school_admin

router = APIRouter(
    prefix="/admin",
    tags=['admin']
)

@router.get("/GetSchoolInfo", response_model=school_schema.SchoolResponse)
def get_school_info(db: Session = Depends(db.get_db), current_user: str = Depends(get_current_school_admin)):
    id = current_user.dict()['id']
    school = db.query(models.School).filter(models.School.id == id).first()

    if not school:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"School with id: {id} does not exist")
    
    return school

@router.get("/GetAllTeachers", response_model=List[teacher_schema.TeacherResponse])
def get_teachers( db: Session = Depends(db.get_db), current_user: str = Depends(get_current_school_admin)):
    id = current_user.dict()['id']
    teachers = db.query(models.Teacher).filter(models.Teacher.school_id == id).all()

    return teachers

@router.get("/GetAllStudents", response_model=List[student_schema.StudentResponse])
def get_students( db: Session = Depends(db.get_db), current_user: str = Depends(get_current_school_admin)):
    id = current_user.dict()['id']
    students = db.query(models.Student).filter(models.Student.school_id == id).all()

    return students

"""
    method receives an array of students data then and also utilizes the
    bearer token (get the school_id after authorization) then set default 
    username and password for students while adding to the database
"""
@router.post("/CreateStudents", response_model=List[student_schema.StudentResponse])
def create_students( students: List[student_schema.AdminStudentCreate], db: Session = Depends(db.get_db), current_user: str = Depends(get_current_school_admin)):
    id = current_user.dict()['id']
    for student in students:
        student = student.dict()
        
        new_student = models.Student(
            firstName = student['firstName'],
            lastName = student['lastName'],
            username = student['firstName'].lower(),
            password = utils.hash_password(student['lastName'].lower()),
            school_id = id
                )
        db.add(new_student)
        db.commit()

    students = db.query(models.Student).filter(models.Student.school_id == id).all()

    return students

"""
    method receives an array of teachers data then and also utilizes the
    bearer token (get the school_id after authorization) then set default 
    username and password for teachers while adding to the database
"""
@router.post("/CreateTeachers", response_model=List[teacher_schema.TeacherResponse])
def create_teachers( teachers: List[teacher_schema.AdminTeacherCreate], db: Session = Depends(db.get_db), current_user: str = Depends(get_current_school_admin)):
    id = current_user.dict()['id']
    for teacher in teachers:
        teacher = teacher.dict()
        
        new_teacher = models.Teacher(
            firstName = teacher['firstName'],
            lastName = teacher['lastName'],
            username = teacher['firstName'].lower(),
            password = utils.hash_password(teacher['lastName'].lower()),
            school_id = id
                )
        db.add(new_teacher)
        db.commit()

    teachers = db.query(models.Teacher).filter(models.Teacher.school_id == id).all()

    return teachers