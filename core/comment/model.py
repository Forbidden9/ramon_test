from sqlalchemy import Column, ForeignKey, Integer, Sequence, Text

from db.session import Base
from utils.mixin import ActiveMixin, TimestampsMixin


class Comment(Base, ActiveMixin, TimestampsMixin):
    __tablename__ = "comment"

    id = Column(Integer, Sequence("comment_id_seq"), primary_key=True, nullable=False)
    description = Column(Text, nullable=True)
    post_id = Column(Integer, ForeignKey("post.id", ondelete="CASCADE"), nullable=False)