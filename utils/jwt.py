from sqlalchemy.orm import Session
from typing import Optional
from fastapi import Depends
from jose import jwt
from passlib.context import CryptContext
from core.oauth.model import BlacklistToken

from core.oauth.repository import oauth2_token

from config.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, password: str) -> bool:
    return pwd_context.verify(plain_password, password)


def verify_password_reset_token(token: str) -> Optional[str]:
    try:
        decoded_token = jwt.decode(token, str(settings.SECRET_KEY), algorithms=[str(settings.JWT_ALGORITHM)])
        return decoded_token["sub"]
    except jwt.JWTError:
        return None


def get_token_user(token: str = Depends(oauth2_token)):
    return token


async def get_by_token(db: Session, *, token: str):
    return db.query(BlacklistToken).filter(BlacklistToken.token == token).first()
