from fastapi import status, HTTPException, APIRouter, Response

from sqlalchemy.orm.session import Session

from app import models, schemas, utils, oauth2
from ..database import get_db
from fastapi.params import Body, Depends  # post data lere
from app.utils import send_event


from typing import Optional, List


router = APIRouter(prefix="/followers", tags=["Followers"])


@router.post("/follow/{following_id}")
async def follow(
    following_id: int,
    current_user: int = Depends(oauth2.get_current_user),
    db: Session = Depends(get_db),
):
    followed = models.Followers(follower_id=current_user.id, following_id=following_id)
    db.add(followed)
    db.commit()
    db.refresh(followed)
    print(followed, followed.__dict__, followed.follower)
    await send_event(
        f"followed-{following_id}",
        {
            "follower": {
                "id": current_user.id,
                "username": current_user.username,
                "profile_photo": current_user.profile_photo,
            }
        },
    )
    return followed


@router.post("/unfollow/{following_id}")
async def unfollow(
    following_id: int,
    current_user: int = Depends(oauth2.get_current_user),
    db: Session = Depends(get_db),
):
    follower = db.query(models.Followers).filter(
        models.Followers.following_id == following_id
    )
    if follower.first() == None:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND, f"No content with specified id:{id}"
        )
    if follower.first().follower_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not allowed to perform the requested action",
        )

    follower.delete(synchronize_session=False)
    db.commit()
    await send_event(
        f"unfollowed-{following_id}",
        {
            "unfollower": {
                "id": current_user.id,
                "username": current_user.username,
                "profile_photo": current_user.profile_photo,
            }
        },
    )
    return Response(status_code=status.HTTP_204_NO_CONTENT)
