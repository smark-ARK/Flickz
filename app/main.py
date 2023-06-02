from fastapi import FastAPI
from sqlalchemy import engine
from . import models
from .database import engine
from .routers import users, posts, auth, votes, followers, comments
from fastapi.middleware.cors import CORSMiddleware
from google.cloud import storage


models.Base.metadata.create_all(bind=engine)


app = FastAPI()
origins = ["*"]

storage_client = storage.Client.from_service_account_json(
    "somple-social-ark-725ba2e57b95.json"
)
bucket = storage_client.get_bucket("simple-social-posts")

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(posts.router)
app.include_router(users.router)
app.include_router(auth.router)
app.include_router(votes.router)
app.include_router(comments.router)
app.include_router(followers.router)


# Started here 1
@app.get("/")
def root():
    return {"message": "Hello ARK!"}
