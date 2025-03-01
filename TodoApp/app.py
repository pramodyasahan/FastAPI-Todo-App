from fastapi import FastAPI
import models
from routers import auth, todos, admin, user
from database import engine

app = FastAPI()

# Create tables in the database
models.Base.metadata.create_all(bind=engine)

app.include_router(auth.router)
app.include_router(todos.router)
app.include_router(admin.router)
app.include_router(user.router)