from sqlalchemy import String
from sqlalchemy.orm import Mapped, relationship, mapped_column
from database import Base  # Import Base from database.py


class Person(Base):
    __tablename__ = 'people'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(128), nullable=False)
    age: Mapped[int] = mapped_column(nullable=False)
    things = relationship("Thing", back_populates="person",
                          cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Person(id={self.id}, name='{self.name}')>"


# This block can be used for testing the model definition if needed
if __name__ == "__main__":
    print("Parent class defined.")
