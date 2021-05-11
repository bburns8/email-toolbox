import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey
from sqlalchemy import inspect
from sqlalchemy.sql import text

# Database's Modeled Table
metadata = MetaData()
customers = Table('customer', metadata,
                  Column('name', String(255), primary_key=True),
                  Column('email', String(255)),
                  Column('balance', Integer),
                  )
# Database connection string
engine = create_engine('mysql://root:password@localhost/customers_db')
metadata.create_all(engine)

inspector = inspect(engine)
inspector.get_columns('customer')

# Using the Text Module
with engine.connect() as con:
    data = ({"name": "Blake Burns", "email": "test@smartCDR.com", "balance": 140000},
            {"name": "John Ross", "email": "test@smartCDR.com", "balance": 450000}
            )
    statement = text("""INSERT INTO customer(name, email, balance) VALUES(:name, :email, :balance)""")

    for line in data:
        con.execute(statement, **line)
