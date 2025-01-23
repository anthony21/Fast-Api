from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from psycopg2.extras import RealDictCursor
from .config import settings
from dotenv import load_dotenv
import psycopg2
import time

load_dotenv()
database_username =os.getenv('DATABASE_USERNAME')
database_password =os.getenv('DATABASE_PASSWORD')

while True:
    try:
        conn = psycopg2.connect(host='localhost',database='fastapi_database',user=database_username,password=database_password, cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("Successfull Connection to Database")
        break
    expect Exception as error:
        print("Failed Connection to Database")
        time.sleep(5)
