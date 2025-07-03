from database import Base, engine, SessionLocal
from models.student import Student
from models.course import Course
from models.enrollment import Enrollment

# Create all tables
Base.metadata.create_all(bind=engine)

# Create session
session = SessionLocal()

# Create students and courses
student1 = Student(name="Alice")
student2 = Student(name="Bob")

course1 = Course(name="Math")
course2 = Course(name="Science")

# Enrollments with grades
enrollment1 = Enrollment(student=student1, course=course1, grade=3)
enrollment2 = Enrollment(student=student1, course=course2, grade=3.5)
enrollment3 = Enrollment(student=student2, course=course1, grade=3)

# Add everything to session
session.add_all([student1, student2, course1, course2, enrollment1, enrollment2, enrollment3])
session.commit()

# Query
students = session.query(Student).all()
for student in students:
    print(f"Student: {student.name}")
    for enrollment in student.enrollments:
        print(f"  Course: {enrollment.course.name}, Grade: {enrollment.grade}")

session.close()
