from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column
from database import Base  # Import Base from database.py

# This is the association object for the many-to-many relationship.
# It explicitly defines the join table.


class StudentCourseAssociation(Base):
    __tablename__ = 'student_course_association'

    student_id: Mapped[int] = mapped_column(ForeignKey('students.id'), primary_key=True)
    course_id: Mapped[int] = mapped_column(ForeignKey('courses.id'), primary_key=True)
    grade: Mapped[float] = mapped_column(nullable=False)

    # Optional: Define relationships to access the Student and Course objects directly
    # from the association object if needed for additional attributes on the link.
    # For a simple many-to-many, these aren't strictly necessary for the main relationship,
    # but they can be useful.
    student = relationship("Student", back_populates="student_associations")
    course = relationship("Course", back_populates="course_associations")

    def __repr__(self):
        return (f"<StudentCourseAssociation(student_id={self.student_id}, "
                f"course_id={self.course_id}, grade={self.grade})>")


if __name__ == "__main__":
    print("StudentCourseAssociation class defined.")