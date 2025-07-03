from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database import Base  # Import Base from database.py
from association import StudentCourseAssociation  # Import the association table


class Student(Base):
    __tablename__ = "students"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(128), index=True)
    email: Mapped[str] = mapped_column(String(128), unique=True, index=True)

    # Define the many-to-many relationship to Course
    # using the association object (StudentCourseAssociation)
    courses = relationship(
        "Course",
        secondary=StudentCourseAssociation.__table__, # Use the association table directly
        back_populates="students"
    )

    # Optional: Relationship to the association object itself
    student_associations = relationship(
        "StudentCourseAssociation",
        back_populates="student",
        cascade="all, delete-orphan"  # If a student is deleted, their associations are deleted
    )

    def __repr__(self):
        return f"<Student(id={self.id}, name='{self.name}', email='{self.email}')>"


if __name__ == "__main__":
    print("Student class defined.")