from sqlalchemy import Column, Integer, ForeignKey, Float
from sqlalchemy.orm import relationship
from database import Base

class Enrollment(Base):
    __tablename__ = 'enrollments'

    student_id = Column(Integer, ForeignKey('students.id'), primary_key=True)
    course_id = Column(Integer, ForeignKey('courses.id'), primary_key=True)
    grade = Column(Float)

    student = relationship("Student", back_populates="enrollments")
    course = relationship("Course", back_populates="enrollments")
