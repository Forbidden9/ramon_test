from typing import Optional
from sqlalchemy.orm import Session
from core.tag.exception import TagNotFoundException
from core.tag.model import Tag
from core.tag.repository import repository_tag
from core.post.exception import PostNotFoundException
from core.post.model import Post
from core.post.repository import repository_post

from core.tag_post.exception import TagPostNotFoundException, DuplicateTagPostException
from core.tag_post.model import TagPost


class RepositoryTagPost():

    def get_by_id(self, db: Session, *, tag_id: int, post_id: int) -> Optional[TagPost]:
        return db.query(TagPost).filter(TagPost.tag_id == tag_id, TagPost.post_id == post_id).first()
    
    def add_tag_post(self, db: Session, *, tag_id: Tag.id, post_id: Post.id):
        post = repository_post.get_by_id(db, id=post_id)
        tag = repository_tag.get_by_id(db, id=tag_id)
        get_tag_post = self.get_by_id(db, tag_id=tag_id, post_id=post_id)

        if not tag:
            raise TagNotFoundException
        elif not post:
            raise PostNotFoundException
        elif get_tag_post:
            raise DuplicateTagPostException

        tag.posts.append(post)
        db.add(tag)
        db.commit()
        db.refresh(tag)

    def remove_tag_post(self, db: Session, *, tag_id: Tag.id, post_id: Post.id):
        tag = repository_tag.get_by_id(db, id=tag_id)
        post = repository_post.get_by_id(db, id=post_id)
        get_tag_post = self.get_by_id(db, tag_id=tag_id, post_id=post_id)
        
        if not tag:
            raise TagNotFoundException
        elif not post:
            raise PostNotFoundException
        elif not get_tag_post:
            raise TagPostNotFoundException
        
        post.tags.remove(tag)
        db.add(post)
        db.commit()
        db.refresh(post)


repository_tag_post = RepositoryTagPost()
