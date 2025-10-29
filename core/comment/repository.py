from sqlalchemy.orm import Session
from core.comment.exception import CommentNotFoundException
from core.comment.schema import CommentBaseSchema
from core.comment.model import Comment
from db.session import connect
from sqlalchemy import text

class RepositoryComment():

    def get_by_id_class(self, db: Session, *, id: int) -> Comment:
        return db.query(Comment).filter(Comment.id == id)

    def get_by_id(self, db: Session, *, id: int) -> Comment:
        return db.query(Comment).filter(Comment.id == id).first()
    
    def active_comments(self, db: Session):
        return db.query(Comment).execution_options(skip_visibility_filter = True).all()
    
    def inactive_comments(self):
        query = text("SELECT description, is_active FROM comment WHERE comment.is_active = false")
        return connect.execute(query).mappings().all()
    
    def create(self, db: Session, obj_in: CommentBaseSchema, post_id: int) -> Comment:
        dict_post = {'post_id': post_id}      
        db_obj = Comment(**obj_in.dict() | dict_post)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(self, db: Session, comment_id: int, *, obj_in: CommentBaseSchema) -> Comment:
        obj_comment = self.get_by_id(db=db, id=comment_id)
        comment = self.get_by_id_class(db, id=obj_comment.id)
        if not obj_comment:
            raise CommentNotFoundException
        comment.update(obj_in.dict(exclude_unset=True), synchronize_session=False)
        db.commit()
        return comment.first()
    
    def delete(self, db: Session, id):
        obj_comment = self.get_by_id_class(db, id=id)
        comment = self.get_by_id(db, id=id)        
        if not comment:
            raise CommentNotFoundException
        obj_comment.delete(synchronize_session=False)
        db.commit()


repository_comment = RepositoryComment()
