from typing import Annotated
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException, status, Path
from database import SessionLocal
from models import Todos, Users
from .auth import get_current_user
from passlib.context import CryptContext
from pydantic import BaseModel, Field

router = APIRouter(
    prefix="/user",
    tags=["User"]
)

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class UserVerification(BaseModel):
    password: str
    new_password: str = Field(min_length=6)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Annotate database dependency
db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]


@router.get("/", status_code=status.HTTP_200_OK)
async def read_all_info(user: user_dependency, db: db_dependency):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    user_info = db.query(Users).filter(Users.id == user.get('id')).first()
    return user_info


@router.put("/change-password", status_code=status.HTTP_204_NO_CONTENT)
async def change_password(user: user_dependency, db: db_dependency, user_verification: UserVerification):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    user_model = db.query(Users).filter(Users.id == user.get('id')).first()
    if user_model is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    if bcrypt_context.verify(user_verification.password, user_model.hashed_password):
        dcrypt_new_password = bcrypt_context.hash(user_verification.new_password)
        user_model.hashed_password = dcrypt_new_password
        db.add(user_model)
        db.commit()
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect password")
