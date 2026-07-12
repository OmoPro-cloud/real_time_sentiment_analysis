'''
this file is going to act as the bridge between the FastAPI app and the PostgreSQL database.
every time FastAPI needs data it will go through database.py

NOTICE: important installation - pip install sqlalchemy psycopg2-binary python-dotenv

NOTICE: this file will be used to connect to the database and perform CRUD operations on the database
CRUD = Create, Read, Update, Delete(this will automate the process of adding, retrieving, updating and deleting data)
'''