from sqlalchemy.orm import Session
from core.tag.exception import TagNotFoundException
from core.tag.schema import TagBaseSchema
from core.tag.model import Tag
from db.session import connect
from sqlalchemy import text

class RepositoryTag():

    def get_by_id_class(self, db: Session, *, id: int) -> Tag:
        return db.query(Tag).filter(Tag.id == id)

    def get_by_id(self, db: Session, *, id: int) -> Tag:
        return db.query(Tag).filter(Tag.id == id).first()
    
    def active_tags(self, db: Session):
        return db.query(Tag).execution_options(skip_visibility_filter = True).all()
    
    def inactive_tags(self):
        query = text("SELECT name, is_active FROM tag WHERE tag.is_active = false")
        return connect.execute(query).mappings().all()
    
    def create(self, db: Session, obj_in: TagBaseSchema) -> Tag:     
        db_obj = Tag(**obj_in.dict())
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(self, db: Session, tag_id: int, *, obj_in: TagBaseSchema) -> Tag:
        obj_tag = self.get_by_id(db=db, id=tag_id)
        tag = self.get_by_id_class(db, id=obj_tag.id)
        if not obj_tag:
            raise TagNotFoundException
        tag.update(obj_in.dict(exclude_unset=True), synchronize_session=False)
        db.commit()
        return tag.first()
    
    def delete(self, db: Session, id):
        obj_tag = self.get_by_id_class(db, id=id)
        tag = self.get_by_id(db, id=id)        
        if not tag:
            raise TagNotFoundException
        obj_tag.delete(synchronize_session=False)
        db.commit()


repository_tag = RepositoryTag()
