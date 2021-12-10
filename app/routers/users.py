from fastapi import (
    FastAPI,
    Response,
    status,
    HTTPException,
    APIRouter,
)
from sqlalchemy.orm.session import Session
from .. import models, schemas, utils
from ..database import get_db
from fastapi.params import Body, Depends  # post data lere

# from pydantic import BaseModel  # schema Validation
from typing import Optional, List

router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/", response_model=schemas.UserResponse)
def create_user(user: schemas.CreateUser, db: Session = Depends(get_db)):
    hashed_password = utils.hash(user.password)
    user.password = hashed_password
    created_user = models.User(**user.dict())
    db.add(created_user)
    db.commit()
    db.refresh(created_user)
    return created_user


@router.get("/{id}", response_model=schemas.UserResponse)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if user == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User with id={id} does not exists",
        )
    return user
