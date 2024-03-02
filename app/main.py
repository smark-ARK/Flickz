from fastapi import FastAPI
from sqlalchemy import engine
from . import models
from .database import engine
from .routers import users, posts, auth, votes, followers, comments, chat
from fastapi.middleware.cors import CORSMiddleware
from google.cloud import storage
import json


from fastapi_socketio import SocketManager


models.Base.metadata.create_all(bind=engine)


app = FastAPI()

origins = [
    "http://localhost:5173",
    "http://localhost:3000",
    "https://flickz.vercel.app",
]

sio = SocketManager(app=app)


@sio.on("setup")
async def setup_handler(sid, data):
    data = json.loads(data)

    await sio.enter_room(sid, data["user_id"])
    await sio.emit(f"connection_established", room=data["user_id"])


@sio.on("start_typing")
async def start_typing_handler(sid, data):
    data = json.loads(data)
    await sio.emit("start_typing", data, room=data["chat_id"])


@sio.on("stop_typing")
async def start_typing_handler(sid, data):
    data = json.loads(data)
    await sio.emit("stop_typing", data, room=data["chat_id"])


@sio.on("join_chat")
async def join_chat_handler(sid, data):
    data = json.loads(data)
    await sio.enter_room(sid=sid, room=data["chat_id"])
    print(f'user with sid: {sid} joined room {data["chat_id"]}')


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
