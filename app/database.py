from sqlalchemy import create_engine, inspect
from sqlalchemy_utils import database_exists, create_database
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.config import DATABASE_URL

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def init_db() -> None:
    if not database_exists(engine.url):
        print("Database doesn't exist")
        create_database(engine.url)
        print("Database created successfully.")

        inspector = inspect(engine)
        tables = inspector.get_table_names()

        if not tables:
            print("No tables found. Please run the migrations.")
        else:
            print(f"Tables {tables} exist.")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
