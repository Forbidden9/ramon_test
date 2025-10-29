from typing import Optional
from fastapi import APIRouter, Depends, Query, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from core.post.model import Post
from core.post.repository import repository_post
from core.post.schema import PostBaseSchema, PostResponse
from core.user.router import get_current_active_user
from core.user.schema import UserBasicInDB
from db.session import get_db


post = APIRouter()

@post.get("/", status_code=status.HTTP_200_OK, name="Get active posts", description="List active posts")
async def getPosts(db: Session = Depends(get_db), limit: int = 10, page: int = 1, search: str = ""):
    skip = (page - 1) * limit
    posts = db.query(Post).group_by(Post.id).filter(Post.name.contains(search)).limit(limit).offset(skip).all()
    return {"results": len(posts), "posts": posts}

@post.get("/inactive_posts", status_code=status.HTTP_200_OK, name="Get inactive posts", description="List inactive posts")
async def inactivePosts(db: Session = Depends(get_db)):
    posts = repository_post.inactive_posts(db)
    return posts

@post.post('/', status_code=status.HTTP_201_CREATED, response_model=PostResponse, name="Create a new post", description="Create a post")
async def createPost(data_post: PostBaseSchema, current_user: UserBasicInDB = Depends(get_current_active_user), db: Session = Depends(get_db)):
    new_post = repository_post.create(db, obj_in=data_post, user_id=current_user.id)
    return new_post

@post.put('/{post_id}', status_code=status.HTTP_200_OK, response_model=PostResponse, name="Update posts")
async def updatePost(post_id: int, data_post: PostBaseSchema, current_user: UserBasicInDB = Depends(get_current_active_user), db: Session = Depends(get_db)):
    update_post = repository_post.update(db=db, post_id=post_id, obj_in=data_post, user_id=current_user.id)
    return update_post

@post.delete('/{post_id}', status_code=status.HTTP_204_NO_CONTENT, name="Remove posts", description="Remove a post")
async def deletePosty(post_id: int, current_user: UserBasicInDB = Depends(get_current_active_user), db: Session = Depends(get_db)):
    repository_post.delete(db, post_id, user_id=current_user.id)
    return JSONResponse(content={"message": "Post removed successfully"})
