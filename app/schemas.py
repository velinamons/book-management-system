from pydantic import BaseModel, Field
from datetime import datetime
from app.enums import GenreEnum


class AuthorResponse(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True


class BookBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=255)
    genre: GenreEnum
    published_year: int = Field(..., ge=1800, le=datetime.now().year)


class BookCreate(BookBase):
    author_name: str = Field(..., min_length=1, max_length=255)


class BookUpdate(BaseModel):
    title: str | None = Field(None, min_length=1, max_length=255)
    genre: GenreEnum | None = None
    published_year: int | None = Field(None, ge=1800, le=datetime.now().year)


class BookResponse(BookBase):
    id: int
    author: AuthorResponse

    class Config:
        from_attributes = True
