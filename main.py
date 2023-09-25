# This imports fastAPI library
from email.policy import HTTP
from random import randrange
from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException
from fastapi import Body
from pydantic import BaseModel

app = FastAPI()

class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int]= None

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
    # Fast api will auto serialize my_posts into JSON
    return {"data": my_posts}

@app.post("/post",status_code=status.HTTP_201_CREATED)  
def create_posts(new_post: Post):
    post_dict = new_post.model_dump()
    post_dict['id']= randrange(0,1000000)
    my_posts.append(post_dict)
    print(my_posts)
    # new_post.dict() -> returns the post as a dict
    return {"data": post_dict}

@app.get("/posts/latest")
def get_latest_post():
    post = my_posts[len(my_posts)-1]
    return {"detail": post}



@app.get("/posts/{id}")
def get_post(id, response: Response):
    post = find_post(id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} was not found")

    return {"post_detail": post}

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    """delete the post"""
    #find the index of the post in the array with the required ID
    index= find_post_index(id)
    if index==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id{id} does not exist")
    my_posts.pop(index)
    print(my_posts)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

