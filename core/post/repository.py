from sqlalchemy.orm import Session
from core.post.exception import PostNotFoundException, DuplicatePostException, PostPermitionException
from core.post.schema import PostBaseSchema
from core.post.model import Post
from core.tag.model import Tag
from core.tag_post.model import TagPost
from db.session import connect
from sqlalchemy import text


class RepositoryPost():

    def get_by_id_class(self, db: Session, *, id: int) -> Post:
        return db.query(Post).filter(Post.id == id)

    def get_by_id(self, db: Session, *, id: int) -> Post:
        return db.query(Post).filter(Post.id == id).first()
    
    def get_by_name(self, db: Session, *, name: str):
        return db.query(Post).filter(Post.name == name).first()
    
    def inactive_posts(self):
        query = text("SELECT name, description, tags, is_active FROM post WHERE post.is_active = false")
        return connect.execute(query).mappings().all()
    
    def create(self, db: Session, obj_in: PostBaseSchema, user_id: int) -> Post:
        name = self.get_by_name(db, name=obj_in.name)
        if name:
            raise DuplicatePostException
        
        db_obj = Post(name=obj_in.name, description=obj_in.description, user_id=user_id)
        
        for tag_id in obj_in.tags:
            tag = db.query(Tag).filter(Tag.id == tag_id).first()
            if tag:
                db_obj.tags.append(tag)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(self, db: Session, post_id: int, obj_in: PostBaseSchema, user_id: int) -> Post:
        db_post = self.get_by_id(db=db, id=post_id)
        if not db_post:
            raise PostNotFoundException
        if not db_post.user_id == user_id:
            raise PostPermitionException    
        
        db_post.name = obj_in.name
        db_post.description = obj_in.description

        db.query(TagPost).filter(TagPost.post_id == post_id).delete()

        for tag_id in obj_in.tags:
            tag = db.query(Tag).filter(Tag.id == tag_id).first()
            if tag:
                tag_post = TagPost(tag_id=tag.id, post_id=db_post.id)
                db.add(tag_post)

        db.commit()
        db.refresh(db_post)
        return db_post
    
    def delete(self, db: Session, id: int, user_id: int):
        obj_post = self.get_by_id_class(db, id=id)
        post = self.get_by_id(db, id=id)
        if not post:
            raise PostNotFoundException
        if not obj_post.user_id == user_id:
            raise PostPermitionException
        obj_post.delete(synchronize_session=False)
        db.commit()


repository_post = RepositoryPost()
