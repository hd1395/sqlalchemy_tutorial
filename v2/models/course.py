from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from database import Base

class Course(Base):
    __tablename__ = 'courses'

    id = Column(Integer, primary_key=True)
    name = Column(String(30), nullable=False)

    enrollments = relationship("Enrollment", back_populates="course", cascade="all, delete-orphan")
