# Project_1/attendance_service/app/database.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker,declarative_base

DARABASE_URL = "sqlite:///./attendance.db"

engine = create_engine(DARABASE_URL,connect_args={"check_same_thread":False})

SessionLocal =sessionmaker(autocommit=False,autoflush=False,bind=engine)

Base = declarative_base()


from typing import Generator

def get_db() -> Generator:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()