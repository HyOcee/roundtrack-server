from email.policy import default
from enum import unique
from time import timezone
from .db import Base
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, inspect
from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP
import uuid

def generate_uuid():
    return str(uuid.uuid4())

def object_as_dict(obj):
    return {c.key: getattr(obj, c.key)
            for c in inspect(obj).mapper.column_attrs}

class School(Base):
    __tablename__ = "schools"

    id = Column(String, primary_key=True, default=generate_uuid)
    name = Column(String, nullable=False, unique=True)
    administrator_email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable = False)
    verified = Column(Boolean, server_default='FALSE')
    address = Column(String)
    created_at = Column(TIMESTAMP(timezone=True), server_default=text('now()'), nullable=False)

    teachers = relationship("Teacher", backref="school_teachers", lazy="joined")
    students = relationship("Student", backref="school_students", lazy="joined")
    subjects = relationship("SubjectOfferedBySchool", lazy="joined")

class Teacher(Base):
    __tablename__ = "teachers"

    id = Column(String, primary_key=True, default=generate_uuid)
    firstName = Column(String, nullable=False)
    lastName = Column(String, nullable=False)
    username = Column(String, nullable=False, unique=True)
    password = Column(String, nullable = False)
    address = Column(String)
    created_at = Column(TIMESTAMP(timezone=True), server_default=text('now()'), nullable=False)
    school_id = Column(String, ForeignKey("schools.id", ondelete="CASCADE"), nullable=False)

    school = relationship("School")
    subjects = relationship("SubjectTakenByTeacher", lazy="joined")

class Student(Base):
    __tablename__ = "students"

    id = Column(String, primary_key=True, default=generate_uuid)
    firstName = Column(String, nullable=False)
    lastName = Column(String, nullable=False)
    username = Column(String, nullable=False, unique=True)
    password = Column(String, nullable = False)
    address = Column(String)
    created_at = Column(TIMESTAMP(timezone=True), server_default=text('now()'), nullable=False)
    school_id = Column(String, ForeignKey("schools.id", ondelete="CASCADE"), nullable=False)

    school = relationship("School")
    subjects = relationship("SubjectOfferedByStudent", lazy="joined")

class Subject(Base):
    __tablename__ = "subjects"
    
    name = Column(String, nullable=False, primary_key=True)

class SubjectOfferedBySchool(Base):
    __tablename__ = "subjects_offered_by_school"

    id = Column(String, primary_key=True, default=generate_uuid)
    subject_name= Column(String, ForeignKey("subjects.name", ondelete="CASCADE"), nullable=False)
    school_id = Column(String, ForeignKey("schools.id", ondelete="CASCADE"), nullable=False)

class SubjectTakenByTeacher(Base):
    __tablename__ = "subjects_taken_by_teacher"

    id = Column(String, primary_key=True, default=generate_uuid)
    subject_name= Column(String, ForeignKey("subjects.name", ondelete="CASCADE"), nullable=False)
    teacher_id = Column(String, ForeignKey("teachers.id", ondelete="CASCADE"), nullable=False)
    school_id = Column(String, ForeignKey("schools.id", ondelete="CASCADE"), nullable=False)

class SubjectOfferedByStudent(Base):
    __tablename__ = "subjects_offered_by_student"

    id = Column(String, primary_key=True, default=generate_uuid)
    test_score = Column(Integer, default=0)
    exam_score = Column(Integer, default=0)
    subject_name = Column(String, ForeignKey("subjects.name", ondelete="CASCADE"), nullable=False)
    school_id = Column(String, ForeignKey("schools.id", ondelete="CASCADE"), nullable=False)
    student_id = Column(String, ForeignKey("students.id", ondelete="CASCADE"), nullable=False)
    
    student = relationship("Student")