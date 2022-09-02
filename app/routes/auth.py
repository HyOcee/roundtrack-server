from fastapi import APIRouter, Response, status, HTTPException, Depends
from .. import models, schemas, db, utils, oauth2
from sqlalchemy.orm import Session
from typing import List

router = APIRouter(
    tags=['Authentication']
)

@router.post('/login')
def login(login_credentials: schemas.Login, db: Session = Depends(db.get_db)):
    user = db.query(models.Teacher).filter(models.Teacher.email == login_credentials.email).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid login credentials")

    if not utils.verify_password(login_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid login credentials")


    access_token = oauth2.create_access_token(data = {"user_id": user.id})
    return {"access_token": access_token, "token_type": "bearer"}