from fastapi import (
    FastAPI,
    Response,
    status,
    HTTPException,
    APIRouter,
    UploadFile,
    Form,
    File,
)

# from ..main import s3
import boto3
from sqlalchemy.orm.session import Session
from sqlalchemy.sql.expression import label
from sqlalchemy.sql.functions import count, func

from app import oauth2, main
from .. import models, schemas
from ..database import get_db
from fastapi.params import Depends  # post data lere

# from pydantic import BaseModel  # schema Validation
from typing import Optional, List

from google.cloud import storage

router = APIRouter(prefix="/posts", tags=["Posts"])


@router.get("/", response_model=List[schemas.Postwith])  # 2
def get_posts(
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user),
    post_limit: int = 10,
    skip: int = 0,
    search: Optional[str] = "",
):
    """posts = (
        db.query(models.post)
        .filter(models.post.title.contains(search))
        .limit(post_limit)
        .offset(skip)
        .all()
    )"""
    # SELECT posts.*, COUNT(votes.post_id) AS votes FROM posts LEFT JOIN votes ON posts.id=votes.post_id GROUP BY posts.id;
    result = (
        db.query(models.post, func.count(models.Votes.post_id).label("votes"))
        .join(models.Votes, models.Votes.user_id == models.post.id, isouter=True)
        .group_by(models.post.id)
        .filter(models.post.title.contains(search))
        .limit(post_limit)
        .offset(skip)
        .all()
    )

    return result


@router.post(
    "/upload-image",
    status_code=status.HTTP_201_CREATED,
    response_model=schemas.UploadImageRes,
)
async def upload_image(
    image: UploadFile = File(...),
):
    # storage_client = storage.Client.from_service_account_json(
    #     "somple-social-ark-725ba2e57b95.json"
    # )
    # bucket = storage_client.get_bucket("simple-social-posts")

    blob = main.bucket.blob(image.filename)
    blob.upload_from_string(await image.read())
    return {
        "image_url": f"https://storage.googleapis.com/{main.bucket.name}/{image.filename}"
    }


@router.post(
    "/", status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse
)  # 3,10 Adding a 201 status code for created post
def create_posts(
    post: schemas.PostCreate,
    # image: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user),
):
    created_post = models.post(owner_id=current_user.id, **post.dict())
    db.add(created_post)
    db.commit()
    db.refresh(created_post)

    return created_post


@router.get("/{id}", response_model=schemas.Postwith)
def get_post(
    id: int,
    response: Response,
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user),
):  # 7 get post using id (id is initially str and is converted to an int), 8.5 Added Response to parameter
    post = (
        db.query(models.post, func.count(models.Votes.post_id).label("votes"))
        .join(models.Votes, models.Votes.user_id == models.post.id, isouter=True)
        .group_by(models.post.id)
        .filter(models.post.id == id)
        .first()
    )
    if not post:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND, f"post with id:{id} was not found"
        )
        """ response.status_code = status.HTTP_404_NOT_FOUND
        return {"message": f"post with id:{id} was not found"} """
    return post


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(
    id: int,
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user),
):
    post = db.query(models.post).filter(models.post.id == id)
    if post.first() == None:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND, f"No content with specified id:{id}"
        )
    if post.first().owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not allowed to perform the requested action",
        )

    post.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}", response_model=schemas.PostResponse)
def update_post(
    id: int,
    updated_post: schemas.PostCreate,
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user),
):
    query = db.query(models.post).filter(models.post.id == id)
    post = query.first()
    if post == None:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND, f"No content with specified id:{id}"
        )
    if post.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not allowed to perform the requested action",
        )
    updated_post = query.update(updated_post.dict(), synchronize_session=False)
    db.commit()

    return query.first()
