from sqlalchemy import create_engine, Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship, Mapped
from faker import Faker
import sqlite3
import random
import datetime
import string
import csv
from models import Base, Group, Student, Lector, Subject, Grade

engine = create_engine('sqlite:///database_HW7.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

fake = Faker()

sub = 7  # кількість предметів
group = 3  # кількість груп
students_per_group = 50  # кількість студентів у групі
quantity_lector = 10  # кількість викладачів
min_grade = 60  # мінімальна оцінка
max_grade = 100  # максимальна оцінка

# Створення груп
for _ in range(group):
    group_name = 'Group ' + ''.join(random.choices(string.ascii_uppercase + string.digits, k=2))
    session.add(Group(name=group_name))
session.commit()

# Створення студентів для кожної групи
for group in session.query(Group):
    for _ in range(students_per_group):
        name = fake.name()
        session.add(Student(name=name, group_id=group.group_id))
session.commit()

# Створення викладачів
for _ in range(quantity_lector):
    session.add(Lector(name=fake.name()))
session.commit()

# Створення предметів для кожного викладача
for lector in session.query(Lector):
    for _ in range(sub // quantity_lector):
        subject_name = fake.job()
        session.add(Subject(name=subject_name, lector_id=lector.lector_id))
session.commit()

# Створення оцінок для студентів
start_date = datetime.date(2023, 9, 1)  # Початкова дата
for student in session.query(Student):
    for _ in range(random.randint(5, 20)):
        lector = random.choice(session.query(Lector).all())
        subjects_for_lector = session.query(Subject).filter_by(lector_id=lector.lector_id).all()
        if subjects_for_lector:  # Перевірка, чи є предмети для даного викладача
            subject = random.choice(subjects_for_lector)
            grade = random.randint(min_grade, max_grade)
            date_received = fake.date_between(start_date=start_date, end_date='today')
            session.add(Grade(student_id=student.student_id, subject_id=subject.subject_id, grade=grade, date_received=date_received))
session.commit()


session.close()
engine.dispose()

