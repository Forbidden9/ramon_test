from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from core.comment.model import Comment
from core.comment.repository import repository_comment
from core.comment.schema import CommentBaseSchema, CommentResponse
from db.session import get_db


comment = APIRouter()

@comment.get("/", status_code=status.HTTP_200_OK, name="Get all comments", description="List all comments")
async def getComments(db: Session = Depends(get_db), limit: int = 10, page: int = 1, search: str = ""):
    skip = (page - 1) * limit
    comments = db.query(Comment).group_by(Comment.id).filter(Comment.description.contains(search)).limit(limit).offset(skip).all()
    return {"results": len(comments), "comments": comments}

@comment.get("/inactive_comments", status_code=status.HTTP_200_OK, name="Get inactive comments", description="List inactive poscommentsts")
async def inactiveComments():
    comment = repository_comment.inactive_comments()
    return comment

@comment.post('/{post_id}', status_code=status.HTTP_201_CREATED, response_model=CommentResponse, name="Create a new comment", description="Create a comment")
async def createComment(data_comment: CommentBaseSchema, post_id: int, db: Session = Depends(get_db)):
    new_comment = repository_comment.create(db, obj_in=data_comment, post_id = post_id)
    return new_comment

@comment.put('/{comment_id}', status_code=status.HTTP_200_OK, response_model=CommentResponse, name="Update comment")
async def updateComment(comment_id: int, data_comment: CommentBaseSchema, db: Session = Depends(get_db)):
    update_comment = repository_comment.update(db=db, comment_id=comment_id, obj_in=data_comment)
    return update_comment

@comment.delete('/{comment_id}', status_code=status.HTTP_204_NO_CONTENT, name="Remove comment", description="Remove a comment")
async def deleteComment(comment_id: int, db: Session = Depends(get_db)):
    repository_comment.delete(db, comment_id)
    return JSONResponse(content={"message": "Comment removed successfully"})
