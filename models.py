from sqlalchemy import create_engine, Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime, timedelta
from sqlalchemy.sql.sqltypes import DateTime

Base = declarative_base()

class Group(Base):
    __tablename__ = 'groups'
    group_id = Column(Integer, primary_key=True)
    name = Column(String)
    students = relationship("Student", back_populates="group")

class Student(Base):
    __tablename__ = 'students'
    student_id = Column(Integer, primary_key=True)
    name = Column(String)
    group_id = Column(Integer, ForeignKey('groups.group_id'))
    group = relationship("Group", back_populates="students")
    grades = relationship("Grade", back_populates="student")

class Lector(Base):
    __tablename__ = 'lectors'
    lector_id = Column(Integer, primary_key=True)
    name = Column(String)
    subjects = relationship("Subject", back_populates="lector")
    

class Subject(Base):
    __tablename__ = 'subjects'
    subject_id = Column(Integer, primary_key=True)
    name = Column(String)
    lector_id = Column(Integer, ForeignKey('lectors.lector_id'))
    lector = relationship("Lector", back_populates="subjects")
    grades = relationship("Grade", back_populates="subject")

 
class Grade(Base):
    __tablename__ = 'grades'
    grade_id = Column(Integer, primary_key=True)
    student_id = Column(Integer, ForeignKey('students.student_id'))
    subject_id = Column(Integer, ForeignKey('subjects.subject_id'))
    grade = Column(Integer)
    date_received = Column(DateTime, default=datetime.now)  
    student = relationship("Student", back_populates="grades")
    subject = relationship("Subject", back_populates="grades")

# Підключення до бази даних
engine = create_engine('sqlite:///database_HW7.db', echo=True)
#Base.metadata.create_all(engine)
def create_tables():
    Base.metadata.drop_all(engine, checkfirst=True)
    Base.metadata.create_all(engine)
    Base.metadata.bind = engine

if __name__ == "__main__":
    create_tables()
