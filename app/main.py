from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import psycopg2
from  psycopg2.extras import RealDictCursor
import time
from . import models
from .db import engine
from .routes import teacher, school, auth

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

while True:
    try:
        conn = psycopg2.connect(host='localhost', database='round_track_database', user='postgres',
                         password='Jie10000', cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("Connected to the database successfully...")
        break
    except Exception as error:
        print("Error connecting to the database", error)
        time.sleep(5)

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(teacher.router)
app.include_router(school.router)
app.include_router(auth.router)

@app.get("/")
async def root():
    return {"message": "Hello World!"}
