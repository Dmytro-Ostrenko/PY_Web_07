from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import func
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

def select_2(subject_name):
    subject = session.query(Subject).filter(Subject.name == subject_name).first()
    students = session.query(Student).all()
    student_grades = []
    for student in students:
        avg_grade = session.query(func.avg(Grade.grade)).filter(Grade.student_id == student.student_id, Grade.subject_id == subject.subject_id).scalar()
        student_grades.append((student.name, round(avg_grade, 2) if avg_grade else None))
    top_students = [student for student in student_grades if student[1] is not None]  # Вибрати лише тих студентів, у яких є середній бал
    if top_students:
        top_student = max(top_students, key=lambda x: x[1])
    else:
        top_student = None
    return top_student

def select_3(subject_name):
    subject = session.query(Subject).filter(Subject.name == subject_name).first()
    groups = session.query(Group).all()
    group_grades = []
    for group in groups:
        avg_grade = session.query(func.avg(Grade.grade)).filter(Grade.subject_id == subject.subject_id, Student.group_id == group.group_id).join(Student).scalar()
        group_grades.append((group.name, round(avg_grade, 2) if avg_grade else None))
    return group_grades

def select_4():
    avg_grade = session.query(func.avg(Grade.grade)).scalar()
    return round(avg_grade, 2) if avg_grade else None

def select_5(lector_name):
    lector = session.query(Lector).filter(Lector.name == lector_name).first()
    subjects = session.query(Subject).filter(Subject.lector == lector).all()
    return [subject.name for subject in subjects]

def select_6(group_name):
    group = session.query(Group).filter(Group.name == group_name).first()
    students = session.query(Student).filter(Student.group == group).all()
    return [student.name for student in students]

def select_7(group_name, subject_name):
    group = session.query(Group).filter(Group.name == group_name).first()
    subject = session.query(Subject).filter(Subject.name == subject_name).first()
    students = session.query(Student).filter(Student.group == group, Student.grades.any(Grade.subject == subject)).all()
    return [student.name for student in students]

def select_8(lector_name):
    lector = session.query(Lector).filter(Lector.name == lector_name).first()
    subjects = session.query(Subject).filter(Subject.lector == lector).all()
    return [subject.name for subject in subjects]

def select_9(student_name):
    student = session.query(Student).filter(Student.name == student_name).first()
    if student:
        grades = session.query(Grade).filter(Grade.student == student).all()
        return [(grade.subject.name, grade.grade) for grade in grades]
    else:
        return "Student not found"

def select_10(student_name, lector_name):
    student = session.query(Student).filter(Student.name == student_name).first()
    if student:
        lector = session.query(Lector).filter(Lector.name == lector_name).first()
        if lector:
            grades = session.query(Grade).join(Subject).filter(Grade.student == student, Subject.lector_id == lector.lector_id).all()
            return [(grade.subject.name, grade.grade) for grade in grades]
        else:
            return "Lector not found"
    else:
        return "Student not found"


# Виклик функцій та виведення результатів
print(select_1())
print(select_2("Programming"))
print(select_3("Mathematics"))
print(select_4())
print(select_5("Samantha Young"))
print(select_6("Group A"))
print(select_7("Group B", "Mathematics"))
print(select_8("Ian Jordan"))
print(select_9("Debbie Miller"))
print(select_10("Debbie Miller", "Ian Jordan"))

session.close()
engine.dispose()
