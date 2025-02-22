from sqlalchemy.orm import Session
from app.models import Book, Author
from app.schemas import BookCreate
from app.enums import GenreEnum


def create_book(db: Session, book_data: BookCreate):
    author = db.query(Author).filter_by(name=book_data.author_name).first()
    if not author:
        author = Author(name=book_data.author_name)
        db.add(author)
        db.flush()

    book = Book(
        title=book_data.title,
        genre=book_data.genre.value,
        published_year=book_data.published_year,
        author_id=author.id,
    )
    db.add(book)
    db.commit()
    return book


def get_books(
    db: Session,
    title: str = None,
    author: str = None,
    genre: GenreEnum = None,
    min_year: int = None,
    max_year: int = None,
    skip: int = 0,
    limit: int = 10,
    sort_by: str = "title",
    order: str = "asc",
):
    query = db.query(Book).join(Author)

    if title:
        query = query.filter(Book.title.ilike(f"%{title}%"))
    if author:
        query = query.filter(Author.name == author)
    if genre:
        query = query.filter(Book.genre == genre)
    if min_year:
        query = query.filter(Book.published_year >= min_year)
    if max_year:
        query = query.filter(Book.published_year <= max_year)

    if sort_by != "author":
        order_by_field = getattr(Book, sort_by, Book.title)
    else:
        order_by_field = Author.name

    if order == "desc":
        order_by_field = order_by_field.desc()
    else:
        order_by_field = order_by_field.asc()

    books = query.order_by(order_by_field).offset(skip).limit(limit).all()

    return books
