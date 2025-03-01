from typing import Annotated
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends
from pydantic import BaseModel
from models import Users
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordRequestForm
from database import SessionLocal
from starlette import status

router = APIRouter()
bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Annotate database dependency
db_dependency = Annotated[Session, Depends(get_db)]


class CreateUserSchema(BaseModel):
    username: str
    email: str
    firstname: str
    lastname: str
    password: str
    role: str


def authenticate_user(username: str, password: str, db):
    user = db.query(Users).filter(Users.username == username).first()
    if not user:
        return False
    if not bcrypt_context.verify(password, user.hashed_password):
        return False
    return True


@router.post("/auth", status_code=status.HTTP_201_CREATED)
async def create_user(db: db_dependency,
                      create_user_request: CreateUserSchema):
    create_user_model = Users(
        username=create_user_request.username,
        email=create_user_request.email,
        firstname=create_user_request.firstname,
        lastname=create_user_request.lastname,
        hashed_password=bcrypt_context.hash(create_user_request.password),
        role=create_user_request.role,
        is_active=True
    )

    db.add(create_user_model)
    db.commit()


@router.post("/token")
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
                                 db: db_dependency):
    user = authenticate_user(
        username=form_data.username, password=form_data.password, db=db
    )
    if not user:
        return "Failed to Authenticate"
    return "You are successfully authenticated"
