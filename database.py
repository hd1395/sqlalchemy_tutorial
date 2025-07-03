from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Define the SQLite database file
DATABASE_URL = "mysql+pymysql://root:Hamad_1395@localhost/sqlalchemy_tut?charset=utf8mb4"

# Create a SQLAlchemy engine
engine = create_engine(DATABASE_URL, echo=True)
# echo=True for logging SQL statements

# Create a declarative base for our models
Base = declarative_base()

# Create a configured "Session" class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    """Dependency for getting a database session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


if __name__ == "__main__":
    print(f"Database engine created for: {DATABASE_URL}")
    print("Run this script directly to ensure database.py is correctly configured.")