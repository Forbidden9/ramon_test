from datetime import datetime, timedelta
from typing import Union
from fastapi.security import OAuth2PasswordBearer

from config.config import settings
from jose import jwt


oauth2_token = OAuth2PasswordBearer(tokenUrl="/api/oauth2/login")


def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, str(settings.SECRET_KEY), algorithm=str(settings.JWT_ALGORITHM))
    return encoded_jwt
