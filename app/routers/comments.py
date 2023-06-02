from fastapi import (
    FastAPI,
    Response,
    status,
    HTTPException,
    APIRouter,
)
from fastapi.params import Depends
from .. import database, schemas, models, oauth2
from sqlalchemy.orm import Session

router = APIRouter(prefix="/comments", tags=["Comments"])


@router.post(
    "/",
    status_code=status.HTTP_200_OK,
    # response_model=schemas.CommentResponse,
)
def comment(
    comment: schemas.CommentBase,
    db: Session = Depends(database.get_db),
    current_user: int = Depends(oauth2.get_current_user),
):
    post = db.query(models.post).filter(models.post.id == comment.post_id).first()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post wit the id-{comment.post_id} does not exist",
        )

    new_comment = models.Comment(
        user_id=current_user.id, post_id=post.id, comment=comment.comment
    )

    db.add(new_comment)
    db.commit()
    db.refresh(new_comment)
    print(new_comment.__dict__)
    return new_comment
