# ORM Object Relational Mapping


# Core Library modules
import os
from typing import List

# Third party modules
import sqlalchemy
from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()


def db_connection(f):
    """
    Supply the decorated function with a database connection.
    Commit/rollback and close the connection after the function call.
    """

    def with_connection_(*args, **kwargs):
        # https://martin-thoma.com/sql-connection-strings/
        engine = create_engine(f"mysql+pymysql://root:password@localhost/customers_db")
        Session = sessionmaker(bind=engine)
        session = Session()
        try:
            rv = f(session, *args, **kwargs)
        except Exception:
            session.rollback()
            raise
        else:
            session.commit()
        finally:
            session.close()

        return rv

    return with_connection_


class Customer(Base):
    __tablename__ = "customers_info"
    name = Column(String, primary_key=True)
    email = Column(String)
    balance = Column(Integer)


@db_connection
def get_customers_email(session, balance: int) -> List[str]:
    customers = session.query(Customer).filter(Customer.balance == balance).all()
    return [customer.email for customer in customers]


if __name__ == "__main__":
    print(get_customers_email(1))
