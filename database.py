from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

engine = create_engine("postgresql://postgres:password@localhost/pizzadb",
                       echo=True)

Base = declarative_base()

Session = sessionmaker()
