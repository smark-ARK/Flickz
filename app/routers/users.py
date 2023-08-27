from fastapi import (
    FastAPI,
    Response,
    status,
    HTTPException,
    APIRouter,
)
from sqlalchemy import func
from sqlalchemy.orm.session import Session
from .. import models, schemas, utils, oauth2
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


@router.get("/{id}", response_model=schemas.Profile)
def get_user(
    id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(oauth2.get_current_user),
):
    user = (
        db.query(
            models.User,
            func.count(models.Followers.following_id)
            .filter(models.Followers.follower_id == models.User.id)
            .label("following_count"),
            func.count(models.Followers.follower_id)
            .filter(models.Followers.following_id == models.User.id)
            .label("followers_count"),
            models.User.id.in_(
                db.query(models.Followers.following_id).filter(
                    models.Followers.follower_id == current_user.id
                )
            ).label("is_followed_by_viewer"),
        )
        .filter(models.User.id == id)
        .group_by(models.User.id)
        .first()
    )
    if user == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User with id={id} does not exists",
        )

    return user


@router.get("/", response_model=List[schemas.UserResponse])
async def get_all_users(
    db: Session = Depends(get_db),
    # current_user: int = Depends(oauth2.get_current_user),
    limit: int = 10,
    skip: int = 0,
    username_search: Optional[str] = "",
    fullname_search: Optional[str] = "",
):
    res = (
        db.query(models.User)
        .filter(
            models.User.username.contains(username_search),
            models.User.full_name.contains(fullname_search),
        )
        .limit(limit=limit)
        .offset(skip)
        .all()
    )

    return res
