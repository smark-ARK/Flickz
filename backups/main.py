from app import (
    FastAPI,
    Response,
    status,
    HTTPException,
)  # 8 http ststus codes, 9 HTTPExceptions
from fastapi.params import Body  # post data lere
from pydantic import BaseModel  # schema Validation
from typing import Optional  # fully optional Value
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor

app = FastAPI()

# Extending Base model of pydantic (Validating The data we get from request)
class Post(BaseModel):  # 4
    title: str
    content: str
    published: bool = True  # optional Feild
    # rating: Optional[int] = None  # fully optional feild


while True:
    try:
        conn = psycopg2.connect(
            host="localhost",
            database="fastapi",
            user="postgres",
            password="12345$smARK",
            cursor_factory=RealDictCursor,
        )
        cursor = conn.cursor()
        print("connection to database was successful!!")
        break
    except Exception as error:
        print("connection failed!!")
        print("Error: ", error)


""" posts = [  # 5
    {
        "title": "Best calisthenics Exersisees 1",
        "content": "pushus, pullups, Bent-over Rows, Pike Pushups",
        "published": False,
        "rating": 5,
        "id": 1,
    },
    {
        "title": "Best calisthenics Exersisees 2",
        "content": "pushus, pullups, Bent-over Rows, Pike Pushups",
        "published": False,
        "rating": 5,
        "id": 2,
    },
] """


def find_post(id: int):  # 6 finding a post with matching id
    for p in posts:
        if p["id"] == id:
            return p


def find_index_of_post(id: int):
    for i, p in enumerate(posts):
        if p["id"] == id:
            return i


# Started here 1
@app.get("/")
def root():
    return {"message": "Hello ARK!"}


@app.get("/posts")  # 2
def get_posts():
    cursor.execute(""" SELECT * FROM posts """)
    posts = cursor.fetchall()
    return posts


@app.post(
    "/posts", status_code=status.HTTP_201_CREATED
)  # 3,10 Adding a 201 status code for created post
def create_posts(post: Post):
    # can be converted into dictionary
    cursor.execute(
        """INSERT INTO posts(title,content,published) VALUES(%s,%s,%s) RETURNING *""",
        (post.title, post.content, post.published),
    )
    created_post = cursor.fetchone()
    conn.commit()
    return created_post


@app.get("/posts/{id}")
def get_post(
    id: int, response: Response
):  # 7 get post using id (id is initially str and is converted to an int), 8.5 Added Response to parameter
    cursor.execute("""SELECT * FROM posts WHERE id = %s""", (str(id)))
    post = cursor.fetchone()
    if not post:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND, f"post with id:{id} was not found"
        )
        """ response.status_code = status.HTTP_404_NOT_FOUND
        return {"message": f"post with id:{id} was not found"} """
    return post


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    cursor.execute(""" DELETE FROM posts WHERE id = %s RETURNING * """, (str(id)))
    deleted_post = cursor.fetchone()
    conn.commit()
    if deleted_post == None:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND, f"No content with specified id:{id}"
        )
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    cursor.execute(
        """ UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""",
        (post.title, post.content, post.published, str(id)),
    )
    updated_post = cursor.fetchone()
    conn.commit()
    if updated_post == None:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND, f"No content with specified id:{id}"
        )
    return updated_post

{
        "post": {
            "id": 10,
            "content": "post-2 for sumeriamahi1906",
            "created_at": "2021-12-08T18:23:30.741497+05:30",
            "title": "sm 2",
            "published": false,
            "owner_id": 7
        },
        "votes": 0
    },

 "title": "ark2 post 1",
    "content": "post-1 for arkhangreat2",
    "published": true,
    "id": 5,
    "created_at": "2021-12-07T18:23:02.921370+05:30",
    "owner_id": 6,
    "owner": {
        "id": 6,
        "email": "arkhangreat2@gmail.com",
        "created_at": "2021-12-06T18:00:08.176702+05:30"
    }