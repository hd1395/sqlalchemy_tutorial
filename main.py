from database import engine, Base, SessionLocal
from person import Person
from thing import Thing


def create_tables():
    """Creates all defined tables in the database."""
    print("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    print("Tables created.")


def create_data():
    """Creates sample Person and Thing data."""
    db = SessionLocal()
    try:
        # Create People
        person1 = Person(name="Alice", age=30)
        person2 = Person(name="Bob", age=40)

        db.add_all([person1, person2])
        db.commit()

        db.refresh(person1)  # Refresh to get IDs
        db.refresh(person2)

        print(f"Created People: {person1}, {person2}")

        # Create Things and link them to People
        thing1 = Thing(name="T1", price=100, person=person1)
        thing2 = Thing(name="T2", price=120, person=person1)
        thing3 = Thing(name="T3", price=80, person=person2)

        db.add_all([thing1, thing2, thing3])
        db.commit()

        db.refresh(thing1)
        db.refresh(thing2)
        db.refresh(thing3)

        print(f"Created Things: {thing1}, {thing2}, {thing3}")

    finally:
        db.close()


def query_data():
    """Queries and prints Person and Thing data."""
    db = SessionLocal()
    try:
        print("\n--- Querying Data ---")

        # Query all people and their things
        people = db.query(Person).all()
        for person in people:
            print(f"Person: {person.name} (ID: {person.id})")
            for thing in person.things:
                print(f"  Thing: {thing.name} (ID: {thing.id}, Person ID: {thing.owner})")

        # Query all things and their people
        things = db.query(Thing).all()
        for thing in things:
            print(f"Thing: {thing.name} (ID: {thing.id}, Person: {thing.person.name if thing.person else 'N/A'})")

        # Query a specific person and their things
        alice = db.query(Person).filter(Person.name == "Alice").first()
        if alice:
            print(f"\nAlice's Things:")
            for thing in alice.things:
                print(f"  - {thing.name}")

    finally:
        db.close()


def update_data():
    """Updates existing data."""
    db = SessionLocal()
    try:
        print("\n--- Updating Data ---")
        # Find a thing and change their name
        thing_to_update = db.query(Thing).filter(Thing.name == "t1").first()
        if thing_to_update:
            original_name = thing_to_update.name
            thing_to_update.name = "T1"
            db.commit()
            db.refresh(thing_to_update)
            print(f"Updated thing from '{original_name}' to '{thing_to_update.name}'")
    finally:
        db.close()


def delete_data():
    """Deletes data, demonstrating cascade."""
    db = SessionLocal()
    try:
        print("\n--- Deleting Data ---")
        # Find a person to delete (which should also delete their things due to cascade="all, delete-orphan")
        person_to_delete = db.query(Person).filter(Person.name == "Alice").first()
        if person_to_delete:
            person_name = person_to_delete.name
            num_children = len(person_to_delete.things)
            db.delete(person_to_delete)
            db.commit()
            print(f"Deleted Person '{person_name}' and their {num_children} things.")

            # Verify deletion
            remaining_persons = db.query(Person).all()
            print(f"Remaining People: {[p.name for p in remaining_persons]}")
            remaining_children = db.query(Thing).all()
            print(f"Remaining Things: {[c.name for c in remaining_children]}")
    finally:
        db.close()


if __name__ == "__main__":
    create_tables()
    create_data()
    query_data()
    update_data()
    delete_data()