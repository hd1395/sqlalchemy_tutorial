from sqlalchemy import create_engine, text
from sqlalchemy.orm import Session

engine = create_engine('sqlite:///dbfile.db', echo=True)
with engine.connect() as conn:
    conn.execute(text('CREATE TABLE IF NOT EXISTS people(name str, age int)'))
    conn.commit()

session = Session(engine)
session.execute(text('INSERT INTO people (name, age) VALUES("Hamad", 30);'))
session.commit()