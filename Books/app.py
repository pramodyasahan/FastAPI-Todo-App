from fastapi import FastAPI, Body

app = FastAPI()

BOOKS = [
    {"title": "Title One", "author": "Author One", "category": "Science"},
    {"title": "Title Two", "author": "Author Two", "category": "Law"},
    {"title": "Title Three", "author": "Author Three", "category": "History"},
    {"title": "Title Four", "author": "Author Four", "category": "Maths"},
    {"title": "Title Five", "author": "Author Five", "category": "Arts"},
    {"title": "Title Six", "author": "Author Four", "category": "Physics"},
]


@app.get("/books")
async def read_all_books():
    return BOOKS


# Path Parameter Example
# {title} is a dynamic value in the URL, allowing users to request a book by its title.
# Example: A request to "/books/Title One" will pass "Title One" as the 'title' parameter.
@app.get("/books/{title}")
async def read_book(title: str):
    for book in BOOKS:
        if book.get("title").casefold() == title.casefold():
            return book


# Query Parameter Example
# Instead of a dynamic value in the URL path, query parameters are passed using the "?" symbol.
# Example: A request to "/books/?category=Maths" will pass "Maths" as the 'category' parameter.
@app.get("/books/")
async def read_category_by_query(category: str):
    books_by_category = []
    for book in BOOKS:
        if book.get("category").casefold() == category.casefold():
            books_by_category.append(book)

    return books_by_category


# Path and query parameters combined: filter books by author (path) and category (query).
@app.get("/books/{book_author}/")
async def read_author_category_by_query(book_author: str, category: str):
    books_by_author = []
    for book in BOOKS:
        if book.get("author").casefold() == book_author.casefold() \
                and book.get("category").casefold() == category.casefold():
            books_by_author.append(book)

    return books_by_author


# Adds a new book to the BOOKS list using a POST request.
@app.post("/books/create-book")
async def create_book(new_book=Body()):
    BOOKS.append(new_book)
    return new_book


# Updates an existing book in the BOOKS list using a PUT request.
@app.put("/books/update-book")
async def update_book(updated_book=Body()):
    for i in range(len(BOOKS)):
        if BOOKS[i].get("title").casefold() == updated_book.get("title").casefold():
            BOOKS[i] = updated_book
    return updated_book
