'''
this file is going to act as the bridge between the FastAPI app and the PostgreSQL database.
every time FastAPI needs data it will go through database.py

NOTICE: important installation - pip install sqlalchemy psycopg2-binary python-dotenv

NOTICE: this file will be used to connect to the database and perform CRUD operations on the database
CRUD = Create, Read, Update, Delete(this will automate the process of adding, retrieving, updating and deleting data)
'''

import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
print(f"Database URL: {DATABASE_URL}")

if DATABASE_URL is None:
    raise ValueError("DATABASE_URL not found in .env file")

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)

Base = declarative_base()