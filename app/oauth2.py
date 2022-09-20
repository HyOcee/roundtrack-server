from datetime import datetime, timedelta
from jose import JWTError, jwt
from .schemas import schemas
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from .config import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')

SECRET_KEY = settings.token_secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.token_expiry_minutes

def create_access_token(data: dict):
    data_copy = data.copy()
    expiry_time = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    data_copy.update({"exp": expiry_time})
    return jwt.encode(data_copy, SECRET_KEY, algorithm=ALGORITHM)

def verify_access_token(token: str, credentials_exception, accountType: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        
        if accountType == "admin":
            id: str = payload.get("school_id")

        if accountType == "teacher":
            id: str = payload.get("teacher_id")

        if accountType == "student":
            id: str = payload.get("student_id")

        if id is None:
            raise credentials_exception

        token_data = schemas.TokenData(id=id)
    except JWTError:
        raise credentials_exception
        
    return token_data

def get_current_school_admin(token: str= Depends(oauth2_scheme)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Could not validate credentials", headers={"WWW_Authenticate": "Bearer"})
    return verify_access_token(token, credentials_exception, "admin")

def get_current_teacher(token: str= Depends(oauth2_scheme)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Could not validate credentials", headers={"WWW_Authenticate": "Bearer"})
    return verify_access_token(token, credentials_exception, "teacher")

def get_current_student(token: str= Depends(oauth2_scheme)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Could not validate credentials", headers={"WWW_Authenticate": "Bearer"})
    return verify_access_token(token, credentials_exception, "student")