from netcore.models import Post, UpdatePost
from fastapi import APIRouter, Body, status, HTTPException
from fastapi.encoders import jsonable_encoder
from netcore.database import mongodb
from fastapi.responses import JSONResponse, Response
from typing import List

router = APIRouter(prefix="/posts", tags=["posts"])

@router.post("/", response_description="Add a post", response_model=Post)
async def create_post(post: Post = Body(...)):
    post = jsonable_encoder(post)
    new_post = await mongodb["posts"].insert_one(post)
    created_post = await mongodb["posts"].find_one({"_id": new_post.inserted_id})
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=created_post)

@router.get('/', response_description="List all posts", response_model=List[Post])
async def list_posts(limit: int = 1000):
    posts = await mongodb["posts"].find().to_list(limit)
    return posts

@router.get("/{id}", response_description="Get a single post", response_model=Post)
async def get_post(id: str):
    if (post := await mongodb["posts"].find_one({'_id': id})) is not None:
        return post
    raise HTTPException(status_code=404, detail=f"Post {id} not found")

@router.delete("/{id}", response_description="Delete a post")
async def delete_post(id: str):
    delete_result = await mongodb["posts"].delete_one({"_id": id})
    
    if delete_result.deleted_count == 1:
        return Response(status_code=status.HTTP_204_NO_CONTENT)

    raise HTTPException(status_code=404, detail=f"Post {id} not found")

@router.put("/{id}", response_description="Update a post", response_model=Post)
async def update_post(id: str, post: UpdatePost = Body(...)):
    # post = {k:v for k,v in post.dict().items() if v is not None}

    if len(post.dict()) >= 1:
        update_result = await mongodb["posts"].update_one({'_id': id}, {"$set": post.dict()})
        
        if update_result.modified_count == 1:
            if (updated_post := await mongodb["posts"].find_one({'_id': id})) is not None:
                return updated_post
    
    if (existing_post := await mongodb["posts"].find_one({"_id": id})) is not None:
        return existing_post
    
    raise HTTPException(status_code=404, detail=f"Post {id} not found")