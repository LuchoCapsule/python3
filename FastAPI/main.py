from typing import Optional
from fastapi import FastAPI, HTTPException, Response, status
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange

app = FastAPI()

# Models to validate parameters using Pydantic module
class ModelPost(BaseModel):
    id: Optional[int] = None
    title: str
    content: str
    published: bool = True # default value
    rating: Optional[int] = None # optional value

# my_posts = [{"title": "Post 1", "content": "Content 1", "published": True, "rating": 5, "id": 1},
#            {"title": "Post 2", "content": "Content 2", "published": False, "rating": 4, "id": 2},
#            {"title": "Post 3", "content": "Content 3", "published": True, "rating": 3, "id": 3}]

my_posts = [
    ModelPost(title="Post 1", content="Content 1", published=True, rating=5, id=1),
    ModelPost(title="Post 2", content="Content 2", published=False, rating=4, id=2),
    ModelPost(title="Post 3", content="Content 3", published=True, rating=3, id=3)
]

async def get_post_by_id(post_id: int):
    post = None
    print("post_id is ", post_id)
    for item in my_posts:
        if item.id == post_id:
            post = item
    return  post

@app.get("/")
async def root():
    return {"message": "Hello World 4"}

@app.get("/posts", status_code=status.HTTP_200_OK)
async def get_posts():
     
    return {"data": my_posts}

# create a function to create a post
@app.post("/create_post")
async def create_post(payload: dict = Body(...)):
    print(payload)
    #return {"dataLucho": "Post created successfully"}  
    return {"data": f"Create as title {payload['title']}" }

# create a function to create a post using a model to validate the parameters
@app.post("/create_post_model", status_code=status.HTTP_201_CREATED)
async def create_post_mod (new_post: ModelPost):
    new_post.id = randrange(100000)
    print("title is " , new_post.title)
    my_posts.append(new_post)
    #return {"dataLucho": "Post created successfully"}  
    return {"data_your_model": new_post }

@app.get("/post_by_id/{post_id}")
async def get_post(post_id: int, response: Response):
    post = await get_post_by_id(post_id)
    if not post:
        #response.status_code = status.HTTP_404_NOT_FOUND
        return {"data": f"Post with id {post_id} not found"}
    return {"data": post}
    

@app.delete("/delete_post/{post_id}", status_code=status.HTTP_200_OK)
async def delete_post(post_id: int):
    post = await get_post_by_id(post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"data": f"Post with id {post_id} not found"}
    my_posts.remove(post)
    return {"data": f"Post with id {post_id} deleted successfully"}

@app.put("/update_post/{post_id}", status_code=status.HTTP_200_OK)
async def update_post(post_id: int, post: ModelPost):
    post_found = await get_post_by_id(post_id)
    if not post_found:
        raise HTTPException(status_code=404, detail="Post not found")
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"data": f"Post with id {post_id} not found"}
    post_found.title = post.title
    post_found.content = post.content
    post_found.published = post.published
    post_found.rating = post.rating
    return {"data": f"Post with id {post_id} updated successfully"}

