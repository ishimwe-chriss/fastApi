from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings


engine = create_engine(settings.sql_alchemy_database_url)

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
#         conn = psycopg2.connect(host='localhost',
#                                 database='fastApi',
#                                 user='postgres',
#                                 password='123456',
#                                 cursor_factory=RealDictCursor)
#         cursor = conn.cursor()
#         print("Database Connection was successful")
#         break
#     except Exception as error:
#         print("Failed to connect to Database")
#         print("Error: ", error)
#         time.sleep(4)
