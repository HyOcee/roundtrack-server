from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from . import models
from .db import engine
from .routes import teacher, school, auth, student, subject, temp, admin

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(teacher.router)
app.include_router(school.router)
app.include_router(student.router)
app.include_router(subject.router)
app.include_router(temp.router)
app.include_router(auth.router)
app.include_router(admin.router)

@app.get("/")
async def root():
    return {"message": "Hello World!"}