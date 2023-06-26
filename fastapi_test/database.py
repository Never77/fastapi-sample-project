from fastapi_test.config import settings
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine(settings.database_url, connect_args={"check_same_thread": False})

SessionLocal= sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_database():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()