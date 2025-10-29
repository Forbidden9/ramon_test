from sqlalchemy import Column, ForeignKey, BigInteger, Sequence

from db.session import Base


class TagPost(Base):
    __tablename__ = "tag_post"

    id = Column(BigInteger, Sequence('tag_post_id_seq'), primary_key=True, nullable=False)
    tag_id = Column('tag_id', ForeignKey("tag.id"))
    post_id = Column('post_id', ForeignKey("post.id"))
