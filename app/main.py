# This imports fastAPI library
from email.policy import HTTP
from random import randrange
import time
from typing import Optional, Tuple
from fastapi import FastAPI, Response, status, HTTPException
from fastapi import Body
from pydantic import BaseModel
import psycopg2
from psycopg2.extras import RealDictCursor
import psycopg

from app import models
from app.database import SessionLocal, engine

app = FastAPI()

models.Base.metadata.create_all(bind= engine)

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int]= None


# with psycopg.connect(host="localhost",dbname="postgres", user="postgres", password="password") as conn:
#     with conn.cursor(row_factory=psycopg.AsyncCursor) as curr:
#         print("Database connection was successful")

while True:
    try:
        conn = psycopg2.connect(host='localhost', dbname='postgres', user='postgres', password = 'password', cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("Database connection successful")
        break
    except Exception as err:
        print("Connecting to database failed")
        print(err)
        time.sleep(2)



my_posts = [{"title": "Title1", "content": "Content1", "id":1}, {"title": "Title2", "content": "Content2", "id":2}]
def find_post(id: str):
    for post in my_posts:
        if post['id']==int(id):
            return post
        
def find_post_index(id: int)->int:
    """
    Returns the index of the post with given index"""
    for i in range(len(my_posts)):
        if my_posts[i]['id']==id:
            return i
        


@app.get("/")
async def root():
    return {"message": "Hello world"}

#If we go to the http://127.0.0.1:8000/posts we will see the json output
@app.get("/posts")
def get_posts():
    cursor.execute("""SELECT * from posts""")
    posts=cursor.fetchall()
    return {"data":posts}

    # Fast api will auto serialize my_posts into JSON
    

@app.post("/post",status_code=status.HTTP_201_CREATED)  
def create_posts(post: Post):
    cursor.execute("""INSERT INTO posts (title, content, published)
                   VALUES (%s, %s, %s) RETURNING * """, (post.title, post.content, post.published))
    new_post = cursor.fetchone()

    conn.commit()
    return {"data": new_post}

@app.get("/posts/latest")
def get_latest_post():
    post = my_posts[len(my_posts)-1]
    return {"detail": post}



@app.get("/posts/{id}")
def get_post(id:int, response: Response):
    cursor.execute("""SELECT * FROM posts where id = %s""",(str(id)))
    post=cursor.fetchone()
    conn.commit()

    return {"post_detail": post}

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):

    """delete the post"""
    #find the index of the post in the array with the required ID
    cursor.execute("""DELETE FROM posts WHERE id = %s returning *""", (str(id)))
    deleted_post=cursor.fetchone()
    conn.commit()

    if deleted_post ==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id {id} does not exist")
    return Response(status_code= status.HTTP_204_NO_CONTENT)



@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    cursor.execute("""UPDATE posts SET title = %s, content =  %s, published = %s WHERE id = %s RETURNING *""", (post.title, post.content, post.published, (str(id))))
    updated_post=cursor.fetchone()
    if updated_post==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id{id} does not exist")
    conn.commit()
    return {'data': updated_post}


