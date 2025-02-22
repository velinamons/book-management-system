from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.utils import import_books_from_json, import_books_from_csv
from app.schemas import BookResponse
from app.crud.book import get_books
from typing import List

router = APIRouter()


@router.post("/books/import", status_code=201)
async def import_books(file: UploadFile = File(...), db: Session = Depends(get_db)):
    content = await file.read()

    if file.filename.endswith(".json"):
        imported_count = import_books_from_json(content.decode("utf-8"), db)
    elif file.filename.endswith(".csv"):
        imported_count = import_books_from_csv(content.decode("utf-8"), db)
    else:
        raise HTTPException(status_code=400, detail="Unsupported file format")

    return {"message": f"Successfully imported {imported_count} books"}


@router.get("/books", response_model=List[BookResponse])
def get_books(
    db: Session = Depends(get_db),
    title: str = None,
    author: str = None,
    genre: str = None,
    min_year: int = None,
    max_year: int = None,
    skip: int = 0,
    limit: int = 10,
    sort_by: str = "title",
    order: str = "asc",
):
    books = get_books(
        db,
        title=title,
        author=author,
        genre=genre,
        min_year=min_year,
        max_year=max_year,
        skip=skip,
        limit=limit,
        sort_by=sort_by,
        order=order,
    )
    return books
