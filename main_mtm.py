from database import engine, Base, SessionLocal
from student import Student
from course import Course
from association import StudentCourseAssociation  # Import the association class


def create_tables():
    """Creates all defined tables in the database."""
    print("Creating database tables (students, courses, and association table with grade)...")
    Base.metadata.create_all(bind=engine)
    print("Tables created.")


def create_data():
    """Creates sample Student and Course data and establishes relationships with grades."""
    db = SessionLocal()
    try:
        # Create Courses
        course_math = Course(title="Mathematics I", credits=3)
        course_physics = Course(title="Physics I", credits=4)
        course_cs = Course(title="Computer Science Intro", credits=3)

        db.add_all([course_math, course_physics, course_cs])
        db.commit()
        """ db.refresh(course_math)
        db.refresh(course_physics)
        db.refresh(course_cs) """
        print(f"Created Courses: {course_math}, {course_physics}, {course_cs}")

        # Create Students
        student_alice = Student(name="Alice Smith", email="alice@example.com")
        student_bob = Student(name="Bob Johnson", email="bob@example.com")
        student_charlie = Student(name="Charlie Brown", email="charlie@example.com")

        db.add_all([student_alice, student_bob, student_charlie])
        db.commit()
        """ db.refresh(student_alice)
        db.refresh(student_bob)
        db.refresh(student_charlie) """
        print(f"Created Students: {student_alice}, {student_bob}, {student_charlie}")

        # Enroll students in courses and assign grades using the association object
        # Alice's enrollments
        alice_math_assoc = StudentCourseAssociation(student=student_alice, course=course_math, grade=85.5)
        alice_cs_assoc = StudentCourseAssociation(student=student_alice, course=course_cs, grade=92.0)
        db.add_all([alice_math_assoc, alice_cs_assoc])

        # Bob's enrollments
        bob_physics_assoc = StudentCourseAssociation(student=student_bob, course=course_physics, grade=78.0)
        bob_cs_assoc = StudentCourseAssociation(student=student_bob, course=course_cs, grade=88.5)
        db.add_all([bob_physics_assoc, bob_cs_assoc])

        # Charlie's enrollments
        charlie_math_assoc = StudentCourseAssociation(student=student_charlie, course=course_math, grade=70.0)
        charlie_physics_assoc = StudentCourseAssociation(student=student_charlie, course=course_physics, grade=65.0)
        db.add_all([charlie_math_assoc, charlie_physics_assoc])

        db.commit()
        print("\nEnrolled students in courses with grades.")

    finally:
        db.close()


def query_data():
    """Queries and prints Student and Course data with their relationships and grades."""
    db = SessionLocal()
    try:
        print("\n--- Querying Data (with Grades) ---")

        # Query all students and their enrolled courses with grades
        students = db.query(Student).all()
        for student in students:
            print(f"Student: {student.name} (Email: {student.email})")
            if student.student_associations: # Use course_associations to get grades
                print("  Enrolled in Courses:")
                for assoc in student.student_associations:
                    print(f"    - {assoc.course.title} (Credits: {assoc.course.credits}) - Grade: {assoc.grade}")
            else:
                print("  Not enrolled in any courses.")

        print("-" * 30)

        # Query all courses and their enrolled students with grades
        courses = db.query(Course).all()
        for course in courses:
            print(f"Course: {course.title} (Credits: {course.credits})")
            if course.course_associations: # Use student_associations to get grades
                print("  Enrolled Students:")
                for assoc in course.course_associations:
                    print(f"    - {assoc.student.name} - Grade: {assoc.grade}")
            else:
                print("  No students enrolled.")

        print("-" * 30)

        # Query a specific student and their courses with grades
        alice = db.query(Student).filter(Student.name == "Alice Smith").first()
        if alice:
            print(f"\nAlice's Courses (with Grades):")
            for assoc in alice.student_associations:
                print(f"  - {assoc.course.title}: Grade {assoc.grade}")

    finally:
        db.close()


def update_data():
    """Updates existing data, specifically changing a grade."""
    db = SessionLocal()
    try:
        print("\n--- Updating Data ---")

        # Find Alice and her Math course association to update her grade
        alice = db.query(Student).filter(Student.name == "Alice Smith").first()
        math_course = db.query(Course).filter(Course.title == "Mathematics I").first()

        if alice and math_course:
            # Find the specific association
            assoc_to_update = db.query(StudentCourseAssociation).filter(
                StudentCourseAssociation.student == alice,
                StudentCourseAssociation.course == math_course
            ).first()

            if assoc_to_update:
                old_grade = assoc_to_update.grade
                assoc_to_update.grade = 90.0 # Update the grade
                db.commit()
                db.refresh(assoc_to_update)
                print(f"Updated Alice's grade in '{math_course.title}' from {old_grade} to {assoc_to_update.grade}")
            else:
                print(f"Alice is not enrolled in '{math_course.title}'.")

        # Enroll Bob in Math with a grade
        bob = db.query(Student).filter(Student.name == "Bob Johnson").first()
        if bob and math_course:
            existing_assoc = db.query(StudentCourseAssociation).filter_by(student=bob, course=math_course).first()
            if not existing_assoc:
                new_assoc = StudentCourseAssociation(student=bob, course=math_course, grade=75.0)
                db.add(new_assoc)
                db.commit()
                db.refresh(new_assoc)
                print(f"Bob newly enrolled in '{math_course.title}' with grade {new_assoc.grade}")
            else:
                print(f"Bob is already enrolled in '{math_course.title}'.")

    finally:
        db.close()


def delete_data():
    """Deletes data, demonstrating how associations are handled with the grade."""
    db = SessionLocal()
    try:
        print("\n--- Deleting Data ---")

        # Delete a specific enrollment (association)
        alice = db.query(Student).filter(Student.name == "Alice Smith").first()
        cs_course = db.query(Course).filter(Course.title == "Computer Science Intro").first()

        if alice and cs_course:
            assoc_to_delete = db.query(StudentCourseAssociation).filter(
                StudentCourseAssociation.student == alice,
                StudentCourseAssociation.course == cs_course
            ).first()
            if assoc_to_delete:
                db.delete(assoc_to_delete)
                db.commit()
                print(f"Deleted Alice's enrollment in '{cs_course.title}'.")
            else:
                print(f"Alice is not enrolled in '{cs_course.title}'.")


        # Delete a student (their associations and grades should also be deleted due to cascade)
        student_to_delete = db.query(Student).filter(Student.name == "Charlie Brown").first()
        if student_to_delete:
            student_name = student_to_delete.name
            db.delete(student_to_delete)
            db.commit()
            print(f"Deleted Student '{student_name}'. Their course enrollments (with grades) are also removed.")

        print("\n--- Remaining Data After Deletion ---")
        query_data() # Show remaining data

    finally:
        db.close()


if __name__ == "__main__":
    # IMPORTANT: Delete 'my_many_to_many_database.db' before running if it exists from previous runs!
    # This ensures the 'grade' column is created.
    create_tables()
    create_data()
    query_data()
    update_data()
    delete_data()