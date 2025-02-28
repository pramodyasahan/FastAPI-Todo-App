from typing import Annotated
from sqlalchemy.orm import Session
from fastapi import FastAPI, Depends, HTTPException, status, Path
import models
from models import Todos
from database import engine, SessionLocal
from pydantic import BaseModel, Field

app = FastAPI()

# Create tables in the database
models.Base.metadata.create_all(bind=engine)


# Dependency function to get a database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Annotate database dependency
db_dependency = Annotated[Session, Depends(get_db)]


# Pydantic schema for request validation
class TodoSchema(BaseModel):
    title: str = Field(min_length=3)  # Title must be at least 3 characters long
    description: str = Field(min_length=3)  # Description must be at least 3 characters long
    priority: int = Field(gt=0, lt=6)  # Priority must be between 1 and 5
    complete: bool = Field(default=False)  # Default value for completion status


# Route to get all todos
@app.get("/", status_code=status.HTTP_200_OK)
async def read_all(db: db_dependency):
    return db.query(Todos).all()


# Route to get a single todo by ID
@app.get("/todo/{todo_id}", status_code=status.HTTP_200_OK)
async def read_todo_by_id(db: db_dependency, todo_id: int = Path(gt=0)):
    todo_model = db.query(Todos).filter(Todos.id == todo_id).first()
    if todo_model is not None:
        return todo_model
    raise HTTPException(status_code=404, detail="Todo not found")


# Route to create a new todo
@app.post('/todo/create', status_code=status.HTTP_201_CREATED)
async def create_todo(db: db_dependency, todo_request: TodoSchema):
    todo_model = Todos(**todo_request.model_dump())
    db.add(todo_model)
    db.commit()


# Route to update a todo by ID
@app.put("/todo/update/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_todo(db: db_dependency, todo_request: TodoSchema, todo_id: int = Path(gt=0)):
    todo_model = db.query(Todos).filter(Todos.id == todo_id).first()
    if todo_model is None:
        raise HTTPException(status_code=404, detail="Todo not found.")

    # Update todo fields
    todo_model.title = todo_request.title
    todo_model.description = todo_request.description
    todo_model.priority = todo_request.priority
    todo_model.complete = todo_request.complete

    db.add(todo_model)
    db.commit()


# Route to delete a todo by ID
@app.delete("/todo/delete/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(db: db_dependency, todo_id: int = Path(gt=0)):
    todo_model = db.query(Todos).filter(Todos.id == todo_id).first()
    if todo_model is None:
        raise HTTPException(status_code=404, detail="Todo not found.")

    db.query(Todos).filter(Todos.id == todo_id).delete()
    db.commit()
