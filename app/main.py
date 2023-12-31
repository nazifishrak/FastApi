# This imports fastAPI library
from email.policy import HTTP
from random import randrange
import time
from turtle import mode, pos
from typing import Optional, Tuple, List
from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi import Body
from pydantic import BaseModel
import psycopg2
from psycopg2.extras import RealDictCursor
from sqlalchemy.orm import Session
from app import models, schemas
from app.database import engine, get_db
from app.models import Post

app = FastAPI()

models.Base.metadata.create_all(bind= engine)








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
        


#TEST ONE: db.query(models.Post).all() ->
# Tapping into database object and query the Post table and get all posts
#returns the SQL query db.query(models.Post)

@app.get("/")
async def root():
    return {"message": "Hello world"} 

#If we go to the http://127.0.0.1:8000/posts we will see the json output
@app.get("/posts",response_model=List[schemas.PostResponse])
def get_posts(db: Session = Depends(get_db)):
    # cursor.execute("""SELECT * from posts""")
    # posts=cursor.fetchall()

    posts= db.query(models.Post).all()



    return posts

    # Fast api will auto serialize my_posts into JSON
    

@app.post("/post",status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse)  
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db)):
    # cursor.execute("""INSERT INTO posts (title, content, published)
    #                VALUES (%s, %s, %s) RETURNING * """, (post.title, post.content, post.published))
    # new_post = cursor.fetchone()

    # conn.commit()

    # new_post=models.Post(title=post.title, content=post.content, published=post.published)
    new_post=models.Post(**post.model_dump()) #Same as above, we unpacked

    db.add(new_post) #add to database
    db.commit()
    db.refresh(new_post) # When you call db.refresh(new_post),
    #SQLAlchemy issues a SELECT statement to re-query the current state of the new_post 
    # #instance from the database, and then it updates the object's attributes with the fresh data.

    return new_post

@app.get("/posts/latest",response_model=schemas.PostResponse)
def get_latest_post(db: Session = Depends(get_db)):
    post = my_posts[len(my_posts)-1]
    return {"detail": post}



@app.get("/posts/{id}", response_model=schemas.PostResponse)
def get_post(id:int, response: Response, db: Session = Depends(get_db)):
    # cursor.execute("""SELECT * FROM posts where id = %s""",(str(id)))
    # post=cursor.fetchone()
    # conn.commit()
# filter is equivalent of where
    post = db.query(models.Post).filter(models.Post.id==id).first()
    
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id {id} was not found")

    return post





@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)):

    """delete the post"""
    #find the index of the post in the array with the required ID
    # cursor.execute("""DELETE FROM posts WHERE id = %s returning *""", (str(id)))
    # deleted_post=cursor.fetchone()
    # conn.commit()

    post_query=db.query(models.Post).filter(models.Post.id == id)


    if post_query.first() ==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id {id} does not exist")
    
    post_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code= status.HTTP_204_NO_CONTENT)

@app.delete("/all",status_code=status.HTTP_204_NO_CONTENT)
def delete_all(db : Session= Depends(get_db)):
    post_query = db.query(models.Post)
    post_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code= status.HTTP_204_NO_CONTENT)



@app.put("/posts/{id}")
def update_post(id: int, post: schemas.PostCreate, db: Session = Depends(get_db)):
    # cursor.execute("""UPDATE posts SET title = %s, content =  %s, published = %s WHERE id = %s RETURNING *""", (post.title, post.content, post.published, (str(id))))
    # updated_post=cursor.fetchone()

    post_query= db.query(models.Post).filter(models.Post.id == id)

    post_inst=post_query.first()


    if post_inst==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id{id} does not exist")
    
    post_query.update({**post.model_dump()}, synchronize_session=False)
    db.commit()
    

    # conn.commit()
    return post_query.first()


