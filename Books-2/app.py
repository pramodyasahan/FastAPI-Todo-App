from typing import Optional
from fastapi import FastAPI, Path, Query, HTTPException
from pydantic import BaseModel, Field
from starlette import status

app = FastAPI()


class Book:
    id: int
    title: str
    author: str
    description: str
    rating: int
    published_date: int

    def __init__(self, id, title, author, description, rating, published_date):
        self.id = id
        self.title = title
        self.author = author
        self.description = description
        self.rating = rating
        self.published_date = published_date


class BooksSchema(BaseModel):
    id: Optional[int] = Field(description="ID is not needed on create", default=None)
    title: str = Field(min_length=4)
    author: str = Field(min_length=2)
    description: str = Field(min_length=1, max_length=200)
    rating: int = Field(gt=-1, lt=6)
    published_date: int = Field(gt=1800, lt=2025)

    model_config = {
        "json_schema_extra": {
            "example": {
                "title": "A new book",
                "author": "Name of the Author",
                "description": "Description of the book",
                "rating": 5,
                "published_date": 2025,
            }
        }
    }


BOOKS = [
    Book(1, "The Great Gatsby", "F. Scott Fitzgerald", "A novel about the American dream and its discontents.", 5,
         1998),
    Book(2, "1984", "George Orwell", "A dystopian novel exploring surveillance and totalitarianism.", 5, 2020),
    Book(3, "To Kill a Mockingbird", "Harper Lee", "A story of racial injustice in the American South.", 5, 2007),
    Book(4, "Pride and Prejudice", "Jane Austen", "A classic romance that critiques social class and expectations.",
         4, 1975),
    Book(5, "Moby Dick", "Herman Melville", "An epic tale of obsession and the sea.", 4, 2016),
    Book(6, "The Catcher in the Rye", "J.D. Salinger", "A narrative about teenage angst and alienation.", 4, 2020)
]


# GET /books - Retrieve a list of all books
@app.get("/books", status_code=status.HTTP_200_OK)
async def read_all_books():
    return BOOKS


# GET /books/{book_id} - Retrieve a specific book by its ID
@app.get("/books/{book_id}", status_code=status.HTTP_200_OK)
async def read_book(book_id: int = Path(gt=0)):
    for book in BOOKS:
        if book.id == book_id:
            return book
    raise HTTPException(status_code=404, detail="Book not found")


# GET /books/publish/?publish_date=<date> - Retrieve books by their published date
@app.get("/books/publish/", status_code=status.HTTP_200_OK)
async def read_book_by_published_date(publish_date: int = Query(gt=1800, lt=2025)):
    book_list = []
    for book in BOOKS:
        if book.published_date == publish_date:
            book_list.append(book)
    return book_list


# GET /books/?book_rating=<rating> - Retrieve books by their rating
@app.get("/books/", status_code=status.HTTP_200_OK)
async def read_book_by_rating(book_rating: int = Query(gt=-1, lt=6)):
    book_list = []
    for book in BOOKS:
        if book.rating == book_rating:
            book_list.append(book)
    return book_list


# POST /create-book - Create a new book entry and add it to the BOOKS list
@app.post("/create-book", status_code=status.HTTP_201_CREATED)
async def create_book(book: BooksSchema):
    new_book = Book(**book.model_dump())
    BOOKS.append(find_book_id(new_book))


# Utility function to assign an ID to a new book
def find_book_id(book: Book):
    book.id = 1 if len(BOOKS) == 0 else BOOKS[-1].id + 1
    return book


# PUT /books/update-book - Update an existing book based on its ID
@app.put("books/update-book", status_code=status.HTTP_204_NO_CONTENT)
async def update_book(book: BooksSchema):
    is_book_changed = False
    for i in range(len(BOOKS)):
        if BOOKS[i].id == book.id:
            BOOKS[i] = book
            is_book_changed = True

    if not is_book_changed:
        raise HTTPException(status_code=404, detail="Book not found")


# DELETE /books/{book_id} - Delete a book from the list by its ID
@app.delete("/books/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(book_id: int = Path(gt=0)):
    is_book_deleted = False
    for i in range(len(BOOKS)):
        if BOOKS[i].id == book_id:
            BOOKS.pop(i)
            is_book_deleted = True
            break

    if not is_book_deleted:
        raise HTTPException(status_code=404, detail="Book not found")
