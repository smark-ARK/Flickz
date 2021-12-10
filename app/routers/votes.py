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

router = APIRouter(prefix="/votes", tags=["Votes"])


@router.post("/", status_code=status.HTTP_200_OK)
def vote(
    vote: schemas.Vote,
    db: Session = Depends(database.get_db),
    current_user: int = Depends(oauth2.get_current_user),
):
    post = db.query(models.post).filter(models.post.id == vote.post_id).first()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post wit the id-{vote.post_id} does not exist",
        )
    vote_query = db.query(models.Votes).filter(
        models.Votes.post_id == vote.post_id, models.Votes.user_id == current_user.id
    )
    found_vote = vote_query.first()
    if vote.dir == 1:
        if found_vote:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"post-{vote.post_id} is already liked",
            )
        new_vote = models.Votes(user_id=current_user.id, post_id=vote.post_id)
        db.add(new_vote)
        db.commit()
        return {"message": "Succesfully added a vote"}

    else:
        if not found_vote:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"post-{vote.post_id} is not liked",
            )
        vote_query.delete()
        db.commit()
        return {"message": "Succesfully removed a vote"}
