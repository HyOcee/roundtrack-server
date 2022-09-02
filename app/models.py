from email.policy import default
from enum import unique
from time import timezone
from .db import Base
from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP

class School(Base):
    __tablename__ = "schools"

    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String, nullable=False)
    administrator_email = Column(String, nullable=False)
    verified = Column(Boolean, server_default='FALSE')
    password = Column(String, nullable = False)
    address = Column(String)
    created_at = Column(TIMESTAMP(timezone=True), server_default=text('now()'), nullable=False)

class Teacher(Base):
    __tablename__ = "teachers"

    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable = False)
    address = Column(String)
    created_at = Column(TIMESTAMP(timezone=True), server_default=text('now()'), nullable=False)
