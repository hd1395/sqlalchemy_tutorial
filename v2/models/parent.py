from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from database import Base

class Parent(Base):
    __tablename__ = 'parents'

    id = Column(Integer, primary_key=True)
    name = Column(String(30), nullable=False)

    children = relationship("Child", back_populates="parent", cascade="all, delete-orphan")
