from fastapi import FastAPI
from sqlalchemy import engine
from . import models
from .database import engine
from .routers import users, posts, auth, votes

models.Base.metadata.create_all(bind=engine)


app = FastAPI()


app.include_router(posts.router)
app.include_router(users.router)
app.include_router(auth.router)
app.include_router(votes.router)

# Started here 1
@app.get("/")
def root():
    return {"message": "Hello ARK!"}
