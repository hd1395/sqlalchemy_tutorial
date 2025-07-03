from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, relationship, mapped_column
from database import Base  # Import Base from database.py


class Thing(Base):
    __tablename__ = 'things'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(128), nullable=False)
    price: Mapped[float] = mapped_column(default=0)
    owner: Mapped[int] = mapped_column(ForeignKey('people.id'))
    person = relationship("Person", back_populates="things")
    
    def __repr__(self):
        return f"<Thing(id={self.id}, name='{self.name}', owner={self.owner})>"


# This block can be used for testing the model definition if needed
if __name__ == "__main__":
    print("Child class defined.")
