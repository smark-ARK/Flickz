from fastapi import status, HTTPException, APIRouter
from sqlalchemy import func
from sqlalchemy.orm.session import Session
from .. import models, schemas, utils
from ..database import get_db
from fastapi.params import Body, Depends


from typing import Optional, List


from app import oauth2, main
from .. import models, schemas
from ..database import get_db
from fastapi.params import Depends


router = APIRouter(prefix="/chat", tags=["Chat"])


@router.post("/{user_id}")
def create_chat(
    user_id: int,
    current_user: int = Depends(oauth2.get_current_user),
    db: Session = Depends(get_db),
):
    user_ids = [current_user.id, user_id]
    chat = (
        db.query(models.Chat.id)
        .filter(
            models.Chat.users.any(models.User.id == current_user.id),
            models.Chat.users.any(models.User.id == user_id),
        )
        .group_by(models.Chat.id)
        .scalar()
    )
    # print(chat)
    if chat:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Chat between these users already exists",
        )

    users = db.query(models.User).filter(models.User.id.in_(user_ids)).all()
    if None in users:
        raise HTTPException(status_code=400, detail="invalid user")
    new_chat = models.Chat()
    for i in users:
        new_chat.users.append(i)
    db.add(new_chat)
    db.commit()
    db.refresh(new_chat)

    return new_chat


@router.get("/", response_model=List[schemas.ChatResponse])
def get_chats(
    db: Session = Depends(get_db), current_user=Depends(oauth2.get_current_user)
):
    chats = (
        db.query(models.Chat)
        .filter(models.Chat.users.any(models.User.id == current_user.id))
        .all()
    )
    # print(chats[0].users)
    return chats


@router.post("/messages/", response_model=schemas.MessageResponse)
def send_message(
    message: schemas.MessageBase,
    db: Session = Depends(get_db),
    current_user=Depends(oauth2.get_current_user),
):
    print("hello")
    new_message = models.Message(
        chat_id=message.chat_id, content=message.content, sender_id=current_user.id
    )
    print(new_message)
    db.add(new_message)
    db.commit()
    db.refresh(new_message)
    return new_message
