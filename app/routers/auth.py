from fastapi import status, HTTPException, APIRouter, Response, Request
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm.session import Session
from fastapi.params import Body, Depends
from .. import schemas, models, utils, database, oauth2


router = APIRouter(tags=["Authentication"])


@router.post("/login", response_model=schemas.ResponseToken)
def login(
    response: Response,
    user_cred: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(database.get_db),
):
    user = db.query(models.User).filter(models.User.email == user_cred.username).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="invalid credentials"
        )
    if not utils.verify(user_cred.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="invalid credentials"
        )
    access_token = oauth2.create_access_token(data={"user_id": user.id})
    refresh_token = oauth2.create_refresh_token(data={"user_id": user.id})

    response.set_cookie(
        key="refresh_token", value=refresh_token, httponly=True
    )  # set HttpOnly cookie in response

    return {
        "access_token": access_token,
        # "refresh_token": refresh_token,
        "token_type": "bearer",
    }


@router.post("/refresh")
def refresh_token(request: Request, response: Response):
    refresh_token = request.cookies.get("refresh_token")
    if not refresh_token:
        raise HTTPException(status_code=400, detail="No refresh token found in cookies")

    payload = oauth2.verify_refresh_token(refresh_token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid or expired refresh token")

    new_access_token = oauth2.create_access_token(data=payload)
    refresh_token = oauth2.create_refresh_token(data={"user_id": payload})

    response.set_cookie(key="refresh_token", value=refresh_token, httponly=True)
    return {"access_token": new_access_token, "token_type": "bearer"}
