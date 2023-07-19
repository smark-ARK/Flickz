from fastapi import FastAPI
from sqlalchemy import engine
from . import models
from .database import engine
from .routers import users, posts, auth, votes, followers, comments, chat
from fastapi.middleware.cors import CORSMiddleware
from google.cloud import storage

# from socketio import AsyncServer
from fastapi_socketio import SocketManager


models.Base.metadata.create_all(bind=engine)


app = FastAPI()

origins = [
    "http://localhost:5173",
    "http://localhost:3000",
    "https://*",
    "http://127.0.0.1:8000",
]

sio = SocketManager(app=app, cors_allowed_origins=origins)
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
app.include_router(chat.router)


# Started here 1
@app.get("/")
def root():
    return {"message": "Hello ARK!"}
