from fastapi import FastAPI
from contextlib import asynccontextmanager

from app.database import init_db
from app.routes import book_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield


app = FastAPI(lifespan=lifespan)

app.include_router(book_router, prefix="/api", tags=["Books"])


@app.get("/")
def read_root():
    return {"message": "Welcome to the Book Management System"}
