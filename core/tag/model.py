from sqlalchemy import Column, Integer, Sequence, Text
from sqlalchemy.orm import relationship

from core.tag_post.model import TagPost
from db.session import Base
from utils.mixin import ActiveMixin, TimestampsMixin


class Tag(Base, ActiveMixin, TimestampsMixin):
    __tablename__ = "tag"

    id = Column(Integer, Sequence("tag_id_seq"), primary_key=True, nullable=False)
    name = Column(Text, nullable=True)
    posts = relationship("Post", secondary=TagPost.__tablename__, back_populates="tags")