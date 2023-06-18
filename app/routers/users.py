from fastapi import (
    FastAPI,
    Response,
    status,
    HTTPException,
    APIRouter,
)
from sqlalchemy import func
from sqlalchemy.orm.session import Session
from .. import models, schemas, utils
from ..database import get_db
from fastapi.params import Body, Depends  # post data lere

# from pydantic import BaseModel  # schema Validation
from typing import Optional, List

router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/")
def create_user(user: schemas.CreateUser, db: Session = Depends(get_db)):
    hashed_password = utils.hash(user.password)
    user.password = hashed_password
    created_user = models.User(**user.dict())
    db.add(created_user)
    db.commit()
    db.refresh(created_user)
    return {"message": "registered succesfully"}


@router.get("/{id}", response_model=schemas.UserResponse)
def get_user(id: int, db: Session = Depends(get_db)):
    user = (
        db.query(
            models.User,
            func.count(models.User.followers).label("followers_count"),
            func.count(models.User.following).label("following_count"),
        )
        .filter(models.User.id == id)
        .group_by(models.User.id)
        .first()
        # .outerjoin(models.Followers, models.User.id == models.Followers.following_id)
        # .with_entities(
        #     models.User,
        #     func.count(models.Followers.follower_id).label("followers_count"),
        #     func.count(models.Followers.following_id).label("following_count"),
        # )
        # .group_by(models.User.id)
    )
    print(user[0].__dict__)
    print(user.followers_count)
    print(user.following_count)
    if user == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User with id={id} does not exists",
        )
    return user[0]
