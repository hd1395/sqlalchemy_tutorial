from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class Child(Base):
    __tablename__ = 'children'

    id = Column(Integer, primary_key=True)
    name = Column(String(30), nullable=False)
    parent_id = Column(Integer, ForeignKey('parents.id'))

    parent = relationship("Parent", back_populates="children")
