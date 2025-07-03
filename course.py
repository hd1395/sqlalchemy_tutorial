from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database import Base  # Import Base from database.py
from association import StudentCourseAssociation  # Import the association table


class Course(Base):
    __tablename__ = "courses"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(128), unique=True, index=True)
    credits: Mapped[int]

    # Define the many-to-many relationship to Student
    # using the association object (StudentCourseAssociation)
    students = relationship(
        "Student",
        secondary=StudentCourseAssociation.__table__, # Use the association table directly
        back_populates="courses"
    )

    # Optional: Relationship to the association object itself, if you need
    # to store extra data on the link (e.g., student's grade in this course)
    course_associations = relationship(
        "StudentCourseAssociation",
        back_populates="course",
        cascade="all, delete-orphan" # If a course is deleted, its associations are deleted
    )

    def __repr__(self):
        return f"<Course(id={self.id}, title='{self.title}', credits={self.credits})>"


if __name__ == "__main__":
    print("Course class defined.")