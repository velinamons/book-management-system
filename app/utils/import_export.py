import csv
import json
from io import StringIO
from app.schemas import BookCreate
from app.crud.book import create_book
from sqlalchemy.orm import Session
from fastapi import HTTPException


def import_books_from_json(file_content: str, db: Session):
    try:
        books_data = json.loads(file_content)
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Invalid JSON format")

    for book_data in books_data:
        book_schema = BookCreate(**book_data)
        create_book(db, book_schema)

    return len(books_data)


def import_books_from_csv(file_content: str, db: Session):
    reader = csv.DictReader(StringIO(file_content))
    books_data = list(reader)

    for book_data in books_data:
        book_schema = BookCreate(**book_data)
        create_book(db, book_schema)

    return len(books_data)
