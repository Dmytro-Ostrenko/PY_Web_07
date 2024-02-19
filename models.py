from sqlalchemy import create_engine, Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship, Mapped
from sqlalchemy.ext.declarative import declarative_base
import sqlite3
from faker import Faker
import random
import string
from datetime import datetime
import csv

# Підключення до бази даних
engine = create_engine('sqlite:///database_HW7.db', echo=True)
Base = declarative_base()

# Таблиця groups, де зберігатимуться П.І. студентів та приналежність їх до груп
class Group(Base):
    __tablename__ = 'groups'
    group_id = Column(Integer, primary_key=True)
    name = Column(String)
    students = relationship("Student", back_populates="group")

    def to_csv(self):
        return [self.group_id, self.name]
    
# Таблиця students, де зберігатимуться П.І. студентів та приналежність їх до груп
class Student(Base):
    __tablename__ = 'students'
    student_id = Column(Integer, primary_key=True)
    name = Column(String)
    group_id = Column(Integer, ForeignKey('groups.group_id'))
    group = relationship("Group", back_populates="students")
    grades = relationship("Grade", back_populates="student")

    def to_csv(self):
        return [self.student_id, self.name, self.group_id]
    
# Таблиця lectors, де зберігатимуться П.І. лекторів та приналежність їх до певного(-их) предметів
class Lector(Base):
    __tablename__ = 'lectors'
    lector_id = Column(Integer, primary_key=True)
    name = Column(String)
    subjects = relationship("Subject", back_populates="lector")

    def to_csv(self):
        return [self.lector_id, self.name]

# Таблиця subjects, де зберігатимуться назви предметів та лекторів, які їх читають
class Subject(Base):
    __tablename__ = 'subjects'
    subject_id = Column(Integer, primary_key=True)
    name = Column(String)
    lector_id = Column(Integer, ForeignKey('lectors.lector_id'))
    lector = relationship("Lector", back_populates="subjects")
    grades = relationship("Grade", back_populates="subject")

    def to_csv(self):
        return [self.subject_id, self.name, self.lector_id]

# Таблиця grades, де зберігатимуться оцынки студентыв за предметами
class Grade(Base):
    __tablename__ = 'grades'
    grade_id = Column(Integer, primary_key=True)
    student_id = Column(Integer, ForeignKey('students.student_id'))
    subject_id = Column(Integer, ForeignKey('subjects.subject_id'))
    grade = Column(Integer)
    date_received = Column(Date)
    student = relationship("Student", back_populates="grades")
    subject = relationship("Subject", back_populates="grades")

    def to_csv(self):
        return [self.grade_id, self.student_id, self.subject_id, self.grade, self.date_received]

Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

# Функція для збереження даних у CSV
def save_to_csv(data, filename):
    with open(filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        for item in data:
            writer.writerow(item.to_csv())

# Виклик функції save_to_csv для кожного типу об'єкту
groups = session.query(Group).all()
save_to_csv(groups, 'Groups.csv')

students = session.query(Student).all()
save_to_csv(students, 'Students.csv')

lectors = session.query(Lector).all()
save_to_csv(lectors, 'Lectors.csv')

subjects = session.query(Subject).all()
save_to_csv(subjects, 'Subjects.csv')

grades = session.query(Grade).all()
save_to_csv(grades, 'Grades.csv')

# Закриття сесії та розрішення ресурсів
session.close()
engine.dispose()