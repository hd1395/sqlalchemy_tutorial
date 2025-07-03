from database import Base, engine, SessionLocal
from models.parent import Parent
from models.child import Child

# Create all tables
Base.metadata.create_all(bind=engine)

# Create session
session = SessionLocal()

# Create a parent
new_parent = Parent(name="John Doe")

# Add children
child1 = Child(name="Anna", parent=new_parent)
child2 = Child(name="Ben", parent=new_parent)

# Add to session
session.add(new_parent)
session.commit()

# Query
parents = session.query(Parent).all()
for parent in parents:
    print(f"Parent: {parent.name}")
    for child in parent.children:
        print(f"  Child: {child.name}")

session.close()
