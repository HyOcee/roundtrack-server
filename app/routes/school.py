from fastapi import APIRouter, Response, status, HTTPException, Depends
from .. import models, schemas, utils, db
from sqlalchemy.orm import Session
from typing import List

router = APIRouter(
    prefix="/schools",
    tags=['schools']
)

@router.get("/", response_model=List[schemas.SchoolResponse])
def get_schools(db: Session = Depends(db.get_db)):
    # cursor.execute(""" SELECT * FROM schools """)
    # schools = cursor.fetchall()

    schools = db.query(models.School).all()
    return schools

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.SchoolResponse)
def create_school(school: schemas.CreateSchool, db: Session = Depends(db.get_db)):
    # school_dict = school.dict()
    # school_dict['id'] = randrange(0,10000000)
    # schools.append(school_dict)

    # cursor.execute("""INSERT INTO schools (name, administrator_email) VALUES (%s,%s) RETURNING *""", (school.name, school.administrator_email))
    # new_school = cursor.fetchone()
    # conn.commit()
    #hash the password
    school.password = utils.hash_password(school.password)

    new_school = models.School(**school.dict())
    db.add(new_school)
    db.commit()
    db.refresh(new_school)

    return new_school

@router.get("/{id}", response_model=schemas.SchoolResponse)
def get_school(id: int):
    # school = find_school(id)
    cursor.execute("""SELECT * FROM schools where id = %s""", (str(id)))
    school = cursor.fetchone()

    if not school:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"School with id: {id} was not found")
    
    return school

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_school(id: int):
    cursor.execute("""DELETE FROM schools WHERE id = %s RETURNING *""", (str(id)))
    deleted_school = cursor.fetchone()
    conn.commit()

    if deleted_school == None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"School with id: {id} does not exist")

    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/{id}", response_model=schemas.SchoolResponse)
def update_school(id: int, school: schemas.SchoolBase):
    cursor.execute("""UPDATE schools SET name = %s WHERE id = %s RETURNING *""", (school.name, str(id)))
    
    updated_school = cursor.fetchone()
    conn.commit()

    if updated_school == None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"School with id: {id} does not exist")

    return updated_school
