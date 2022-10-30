from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from psycopg2.extras import RealDictCursor
from .config import settings
import psycopg2
import time

#psycopg2 is for hardcoding sql into the cursors for retrieving directly from database
while True:
    try: 
        conn = psycopg2.connect(host='localhost',database='fastapi_database',user='postgres',password='password', cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("Successfull Connection to Database")
        break
    except Exception as error:
        print("Failed Connection to database ")
        time.sleep(5)


SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}/{settings.database_name}'
engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()