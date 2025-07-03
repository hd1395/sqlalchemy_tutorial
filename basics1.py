from sqlalchemy import create_engine, MetaData, ForeignKey
from sqlalchemy import Column, Table, Integer, String, Float

engine = create_engine('sqlite:///dbfile.db', echo=True)
meta = MetaData()
people = Table(
    "people",
    meta,
    Column('id', Integer, primary_key=True),
    Column('name', String, nullable=False),
    Column('age', Integer, default=1)
)
things = Table(
    "things",
    meta,
    Column('id', Integer, primary_key=True),
    Column('name', String, nullable=False),
    Column('price', Float, default=0.0),
    Column('owner', Integer, ForeignKey('people.id'))
)
meta.create_all(engine)
with engine.connect() as conn:
    conn.execute(things.delete())
    conn.commit()
    insert_stmt = things.insert().values([
        {'name': 't1', 'price': 30, 'owner': 1},
        {'name': 't2', 'price': 40, 'owner': 4},
        {'name': 't3', 'price': 60, 'owner': 1},
        {'name': 't4', 'price': 100, 'owner': 6},
        {'name': 't5', 'price': 55.50, 'owner': 6},
        {'name': 't6', 'price': 90, 'owner': 6},
        {'name': 't7', 'price': 130, 'owner': 1},
    ])

    conn.execute(insert_stmt)
    conn.commit()
    
    join_stmt = people.join(things, people.c.id == things.c.owner)
    select_stmt = people.select().with_only_columns(
        people.c.id,
        people.c.name,
        things.c.name,
        things.c.owner
        ).order_by(people.c.id).select_from(join_stmt)
    result = conn.execute(select_stmt)
    for row in result.fetchall():
        print(row)

    """     insert_stmt = people.insert().values(name="Nasser", age=50)
        result = conn.execute(insert_stmt)
        conn.commit()

        select_stmt = people.select().where(people.c.age <= 40)
        result = conn.execute(select_stmt)
        conn.commit()

        for row in result.fetchall():
            print(row)
        update_stmt = people.update().where(
            people.c.id == 3).values(
                name="Nasser", age=44)
        result = conn.execute(update_stmt)
        conn.commit()

        delete_stmt = people.delete().where(people.c.age == 50)
        conn.execute(delete_stmt)
        conn.commit()
    """