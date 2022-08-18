from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import time 
import psycopg2
from psycopg2.extras import RealDictCursor 
from .config import settings as st 

SQLALCHEMY_DATABASE_URL = f'postgresql://{st.database_username}:{st.database_password}@{st.database_hostname}/{st.database_name}'

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db 
    finally:
        db.close()

# while True:
#     try:
#         conn = psycopg2.connect(host='localhost', database='fastapi', user='postgres', password='Mesfinmekoya@loveu19', cursor_factory=RealDictCursor)
#         cursor = conn.cursor()
#         print("Data base connection was successfu") 
#         break 
#     except Exception as e:
#         print("Unable to connect ", str(e))
#         time.sleep(3)
