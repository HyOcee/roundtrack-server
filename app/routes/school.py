from fastapi import APIRouter, Response, status, HTTPException, Depends

from ..schemas import school_schema
from .. import models, utils, db
from sqlalchemy.orm import Session
from typing import List

router = APIRouter(
    prefix="/schools",
    tags=['schools']
)

@router.get("/", response_model=List[school_schema.SchoolResponse])
def get_schools(db: Session = Depends(db.get_db)):
    # cursor.execute(""" SELECT * FROM schools """)
    # schools = cursor.fetchall()

    schools = db.query(models.School).all()
    return schools

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=school_schema.SchoolResponse)
def create_school(school: school_schema.CreateSchool, db: Session = Depends(db.get_db)):
    school.password = utils.hash_password(school.password)

    new_school = models.School(**school.dict())
    db.add(new_school)
    db.commit()
    db.refresh(new_school)

    return new_school

@router.get("/{id}", response_model=school_schema.SchoolResponse)
def get_school(id: str, db: Session = Depends(db.get_db)):

    school = db.query(models.School).filter(models.School.id == id).first()

    if not school:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"School with id: {id} was not found")
    
    return school

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_school(id: int, db: Session = Depends(db.get_db)):
    cursor.execute("""DELETE FROM schools WHERE id = %s RETURNING *""", (str(id)))
    deleted_school = cursor.fetchone()
    conn.commit()

    if deleted_school == None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"School with id: {id} does not exist")

    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/{id}", response_model=school_schema.SchoolResponse)
def update_school(id: int, school: school_schema.SchoolBase, db: Session = Depends(db.get_db)):
    cursor.execute("""UPDATE schools SET name = %s WHERE id = %s RETURNING *""", (school.name, str(id)))
    
    updated_school = cursor.fetchone()
    conn.commit()

    if updated_school == None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"School with id: {id} does not exist")

    return updated_school
