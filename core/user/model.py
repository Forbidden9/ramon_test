from sqlalchemy import Column, Integer, Sequence
from sqlalchemy.sql.sqltypes import String
from sqlalchemy.orm import Mapped, mapped_column
from utils.mixin import TimestampsMixin, ActiveMixin
from db.session import Base


class User(Base, ActiveMixin, TimestampsMixin):
    __tablename__ = "user"

    id = Column(Integer, Sequence("user_id_seq"), primary_key=True, nullable=False, autoincrement=True)
    name = Column(String(255), nullable=True)
    email = Column(String(100), unique=True, nullable=True)
    phone_number = Column(String(20), unique=True, index=True, nullable=True)
    username = Column(String(50), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String, nullable=True)
