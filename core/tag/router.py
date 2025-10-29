from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from core.post.schema import PostBaseSchema
from core.tag.model import Tag
from core.tag.repository import repository_tag
from core.tag.schema import TagBaseSchema, TagResponse
from db.session import get_db


tag = APIRouter()

@tag.get("/", status_code=status.HTTP_200_OK, name="Get all tags", description="List all tags")
async def getTags(db: Session = Depends(get_db), limit: int = 10, page: int = 1, search: str = ""):
    skip = (page - 1) * limit
    tags = db.query(Tag).group_by(Tag.id).filter(Tag.name.contains(search)).limit(limit).offset(skip).all()
    return {"results": len(tags), "tags": tags}

@tag.get("/getTagList", status_code=status.HTTP_200_OK, name="Get list of tags", description="List of active tags")
async def getTagList(db: Session = Depends(get_db)):
    tag = repository_tag.active_tags(db=db)
    return tag

@tag.get("/inactive_tags", status_code=status.HTTP_200_OK, name="Get inactive tags", description="List inactive tags")
async def inactiveTags():
    tag = repository_tag.inactive_tags()
    return tag

@tag.post('/', status_code=status.HTTP_201_CREATED, response_model=TagResponse, name="Create a new tag", description="Create a tag")
async def createTag(data_tag: TagBaseSchema, db: Session = Depends(get_db)):
    new_tag = repository_tag.create(db, obj_in=data_tag)
    return new_tag

@tag.put('/{tag_id}', status_code=status.HTTP_200_OK, response_model=TagResponse, name="Update tag")
async def updateTag(tag_id: int, data_tag: TagBaseSchema, db: Session = Depends(get_db)):
    update_tag = repository_tag.update(db=db, tag_id=tag_id, obj_in=data_tag)
    return update_tag

@tag.delete('/{tag_id}', status_code=status.HTTP_204_NO_CONTENT, name="Remove tag", description="Remove a tag")
async def deleteTag(tag_id: int, db: Session = Depends(get_db)):
    repository_tag.delete(db, tag_id)
    return JSONResponse(content={"message": "Tag removed successfully"})
