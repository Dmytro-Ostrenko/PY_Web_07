from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import func
from models import Student, Grade, Subject, Group, Lector

engine = create_engine('sqlite:///database_HW7.db')
Session = sessionmaker(bind=engine)
session = Session()

def select_1():
    # Знайти 5 студентів із найбільшим середнім балом з усіх предметів
    students = session.query(Student).all()
    student_grades = []
    for student in students:
        avg_grade = session.query(func.avg(Grade.grade)).filter(Grade.student_id == student.student_id).scalar()
        student_grades.append((student, avg_grade))
    top_students = sorted(student_grades, key=lambda x: x[1], reverse=True)[:5]
    return top_students

def select_2(subject_name):
    # Знайти студента із найвищим середнім балом з певного предмета
    subject = session.query(Subject).filter(Subject.name == subject_name).first()
    students = session.query(Student).all()
    student_grades = []
    for student in students:
        avg_grade = session.query(func.avg(Grade.grade)).filter(Grade.student_id == student.student_id, Grade.subject_id == subject.id).scalar()
        student_grades.append((student, avg_grade))
    top_student = max(student_grades, key=lambda x: x[1])
    return top_student

def select_3(subject_name):
    # Знайти середній бал у групах з певного предмета
    subject = session.query(Subject).filter(Subject.name == subject_name).first()
    groups = session.query(Group).all()
    group_grades = []
    for group in groups:
        avg_grade = session.query(func.avg(Grade.grade)).filter(Grade.subject_id == subject.id, Student.group_id == group.id).join(Student).scalar()
        group_grades.append((group, avg_grade))
    return group_grades

def select_4():
    # Знайти середній бал на потоці (по всій таблиці оцінок)
    avg_grade = session.query(func.avg(Grade.grade)).scalar()
    return avg_grade

def select_5(lector_name):
    # Знайти які курси читає певний викладач
    lector = session.query(Lector).filter(Lector.name == lector_name).first()
    subjects = session.query(Subject).filter(Subject.lector_id == lector.id).all()
    return subjects

def select_6(group_name):
    # Знайти список студентів у певній групі
    group = session.query(Group).filter(Group.name == group_name).first()
    students = session.query(Student).filter(Student.group_id == group.id).all()
    return students

def select_7(group_name, subject_name):
    # Знайти оцінки студентів у окремій групі з певного предмета
    group = session.query(Group).filter(Group.name == group_name).first()
    subject = session.query(Subject).filter(Subject.name == subject_name).first()
    students = session.query(Student).filter(Student.group_id == group.id).all()
    student_grades = []
    for student in students:
        grade = session.query(Grade).filter(Grade.student_id == student.id, Grade.subject_id == subject.id).all()
        student_grades.append((student, grade))
    return student_grades

def select_8(lector_name):
    # Знайти середній бал, який ставить певний викладач зі своїх предметів
    lector = session.query(Lector).filter(Lector.name == lector_name).first()
    subjects = session.query(Subject).filter(Subject.lector_id == lector.id).all()
    lector_grades = []
    for subject in subjects:
        avg_grade = session.query(func.avg(Grade.grade)).filter(Grade.subject_id == subject.id).scalar()
        lector_grades.append((subject, avg_grade))
    return lector_grades

def select_9(student_name):
    # Знайти список курсів, які відвідує студент
    student = session.query(Student).filter(Student.name == student_name).first()
    grades = session.query(Grade).filter(Grade.student_id == student.id).all()
    subjects = [grade.subject for grade in grades]
    return subjects

def select_10(student_name, lector_name):
    # Список курсів, які певному студенту читає певний викладач
    student = session.query(Student).filter(Student.name == student_name).first()
    lector = session.query(Lector).filter(Lector.name == lector_name).first()
    subjects = session.query(Subject).filter(Subject.lector_id == lector.id).all()
    student_subjects = []
    for subject in subjects:
        grade = session.query(Grade).filter(Grade.student_id == student.id, Grade.subject_id == subject.id).first()
        if grade:
            student_subjects.append(subject)
    return student_subjects

# Виклик функцій та виведення результатів
print(select_1())
print(select_2("Математика"))
print(select_3("Математика"))
print(select_4())
print(select_5("Викладач1"))
print(select_6("Group1"))
print(select_7("Group1", "Математика"))
print(select_8("Викладач1"))
print(select_9("Student1"))
print(select_10("Student1", "Викладач1"))

session.close()
engine.dispose()
