from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import func, distinct
from models import Student, Grade, Subject, Group, Lector

engine = create_engine('sqlite:///database_HW7.db')
Session = sessionmaker(bind=engine)
session = Session()

def select_1(): #Знайти 5 студентів із найбільшим середнім балом з усіх предметів.
    students = session.query(Student).all()
    student_grades = []
    for student in students:
        avg_grade = session.query(func.avg(Grade.grade)).filter(Grade.student_id == student.student_id).scalar()
        student_grades.append((student.name, round(avg_grade, 2) if avg_grade else None))
    top_students = sorted(student_grades, key=lambda x: x[1], reverse=True)[:5]
    return top_students

def select_2(subject_name): #Знайти студента із найвищим середнім балом з певного предмета.
    subject = session.query(Subject).filter(Subject.name == subject_name).first()
    students = session.query(Student).all()
    student_grades = []
    for student in students:
        avg_grade = session.query(func.avg(Grade.grade)).filter(Grade.student_id == student.student_id, Grade.subject_id == subject.subject_id).scalar()
        student_grades.append((student.name, round(avg_grade, 2) if avg_grade else None))
    top_students = [student for student in student_grades if student[1] is not None]  # oбрати лише тих студентів у яких є середній бал
    if top_students:
        top_student = max(top_students, key=lambda x: x[1])
    else:
        top_student = None
    return top_student

def select_3(subject_name): #Знайти середній бал у групах з певного предмета.
    subject = session.query(Subject).filter(Subject.name == subject_name).first()
    groups = session.query(Group).all()
    group_grades = []
    for group in groups:
        avg_grade = session.query(func.avg(Grade.grade)).filter(Grade.subject_id == subject.subject_id, Student.group_id == group.group_id).join(Student).scalar()
        group_grades.append((group.name, round(avg_grade, 2) if avg_grade else None))
    return group_grades

def select_4(): #Знайти середній бал на потоці (по всій таблиці оцінок).
    avg_grade = session.query(func.avg(Grade.grade)).scalar()
    return round(avg_grade, 2) if avg_grade else None

def select_5(lector_name): #Знайти які курси читає певний викладач.
    lector = session.query(Lector).filter(Lector.name == lector_name).first()
    subjects = session.query(Subject).filter(Subject.lector == lector).all()
    return [subject.name for subject in subjects]

def select_6(group_name): #Знайти список студентів у певній групі.
    group = session.query(Group).filter(Group.name == group_name).first()
    students = session.query(Student).filter(Student.group == group).all()
    return [student.name for student in students]

def select_7(group_name, subject_name): #Знайти оцінки студентів у окремій групі з певного предмета.
    group = session.query(Group).filter(Group.name == group_name).first()
    subject = session.query(Subject).filter(Subject.name == subject_name).first()
    students = session.query(Student).filter(Student.group == group).all()
    results = []
    for student in students:
        for grade in student.grades:
            if grade.subject == subject:
                results.append((student.name, grade.grade))
    return results

def select_8(lector_name): #Знайти середній бал, який ставить певний викладач зі своїх предметів.
    lector = session.query(Lector).filter(Lector.name == lector_name).first()
    subjects = session.query(Subject).filter(Subject.lector == lector).all()
    average_grades = []
    for subject in subjects:
        grades = [grade.grade for grade in subject.grades]
        average_grade = round(sum(grades) / len(grades), 2) if grades else 0
        average_grades.append((subject.name, average_grade))
    return average_grades


def select_9(student_name): #Знайти список курсів, які відвідує певний студент.
    student = session.query(Student).filter(Student.name == student_name).first()
    if student:
        courses = session.query(Subject.name).\
            join(Grade, Subject.subject_id == Grade.subject_id).\
            filter(Grade.student == student).\
            distinct().all()
        return [course[0] for course in courses]
    else:
        return "Student not found"

def select_10(student_name, lector_name): #Список курсів, які певному студенту читає певний викладач.
    student = session.query(Student).filter(Student.name == student_name).first()
    lector = session.query(Lector).filter(Lector.name == lector_name).first()
    if student and lector:
        student_courses = []
        for grade in student.grades:
            if grade.subject.lector == lector:
                student_courses.append(grade.subject.name)
        return list(set(student_courses))
    else:
        return "Student or lector not found"

# Виклик та РЕЗУЛЬТАТИ
print(f"Запит№1:{select_1()}")
print(f"Запит№2:{select_2('Math modeling')}")
print(f"Запит№3:{select_3('Mathematics')}")
print(f"Запит№4:{select_4()}")
print(f"Запит№5:{select_5('Samantha Young')}")
print(f"Запит№6:{select_6('Group A')}")
print(f"Запит№7:{select_7('Group B', 'Mathematics')}")
print(f"Запит№8:{select_8('Ian Jordan')}")
print(f"Запит№9:{select_9('Debbie Miller')}")
print(f"Запит№10:{select_10('Debbie Miller', 'Ian Jordan')}")

session.close()
engine.dispose()
