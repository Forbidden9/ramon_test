from datetime import datetime

from sqlalchemy import Column, ForeignKey, Integer, Sequence, String, ARRAY
from sqlalchemy.orm import relationship

from core.tag_post.model import TagPost
from db.session import Base
from utils.mixin import ActiveMixin, TimestampsMixin


class Post(Base, ActiveMixin, TimestampsMixin):
    __tablename__ = "post"

    id = Column(Integer, Sequence("post_id_seq"), primary_key=True, nullable=False, autoincrement=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    user_id = Column(Integer, ForeignKey("user.id", ondelete="CASCADE"), nullable=False)
    tags = relationship("Tag", secondary=TagPost.__tablename__, back_populates="posts")
