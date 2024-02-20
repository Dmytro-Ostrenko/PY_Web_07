from faker import Faker
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, Student, Group, Lector, Subject, Grade
import random
from db import session
from datetime import datetime, timedelta
import string

# Підключення до бази даних PostgreSQL
fake = Faker()
# engine = create_engine('postgresql://Dmytro:1234@localhost:5432/database_HW7.db')
# Base.metadata.create_all(engine)
# Session = sessionmaker(bind=engine)
# session = Session()

# Очищення таблиць перед додаванням нових записів
session.query(Grade).delete()
session.query(Student).delete()
session.query(Subject).delete()
session.query(Lector).delete()
session.query(Group).delete()

# Генеруємо групи
group_names = ["A", "B", "C"]
students_per_group = 50
grades_range = range(60, 101)

for name in group_names:
    group = Group(name=f"Group {name}")
    session.add(group)

# Генеруємо студентів
for group_id in range(1, len(group_names) + 1):
    for _ in range(students_per_group):
        student = Student(name=fake.name(), group_id=group_id)
        session.add(student)

# Генеруємо викладачів
for _ in range(3):
    lector = Lector(name=fake.name())
    session.add(lector)

# Генеруємо предмети
subjects_list = ["Electrical engineering", "Mathematics", "Physics", "Programming", "Math modeling", "Alternative energy", "Automation"]
lectors = session.query(Lector).all()
for name in subjects_list:
    lector_id = random.randint(1, 3)
    subject = Subject(name=name, lector_id=lector_id)
    session.add(subject)

session.commit()

subjects = session.query(Subject).all() 

start_date = datetime(2023, 9, 1)
end_date = datetime.now()
time_difference = end_date - start_date

# Генеруємо оцінки для студентів за предмети
for student_id in range(1, students_per_group * len(group_names) + 1):
    num_grades = random.randint(5, 20)  # Випадкова кількість оцінок для кожного студента
    for _ in range(num_grades):
        subject = random.choice(subjects)
        grade = random.choice(grades_range)
        random_days_difference = random.randint(0, (end_date - start_date).days)
        timestamp = start_date + timedelta(days=random_days_difference)
        new_grade = Grade(grade=grade, date_received=timestamp, subject_id=subject.subject_id, student_id=student_id)
        session.add(new_grade)

session.commit()
session.close()

