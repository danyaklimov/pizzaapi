from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
import os

DB_URL = os.environ['DB_URL']

engine = create_engine(DB_URL, echo=True)

Base = declarative_base()

Session = sessionmaker()

