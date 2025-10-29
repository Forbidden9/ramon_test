from sqlalchemy import Column, String

from db.session import Base


class BlacklistToken(Base):
    __tablename__ = 'blacklist'

    token = Column(String(255), primary_key=True, unique=True)
    email = Column(String(100))
