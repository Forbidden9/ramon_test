from datetime import timedelta
from fastapi import APIRouter, Depends, status
from fastapi.responses import RedirectResponse
from fastapi.security import OAuth2PasswordRequestForm
from jose import JWTError, jwt
from pydantic import ValidationError
import requests
from sqlalchemy.orm import Session
from config.config import settings
from core.oauth.exception import CredentialsException, IncorrectInputFieldsException
from core.oauth.repository import create_access_token
from core.oauth.schema import TokenData
from core.user.exception import UserInactiveException
from core.user.model import User
from core.user.repository import repository_user
from core.oauth.repository import oauth2_token

from db.session import get_db
from utils.jwt import get_by_token


oauth2 = APIRouter()


@oauth2.post("/login")
async def login(db: Session = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()):
    user = repository_user.authenticate(db, email=form_data.username, password=form_data.password)

    if not user:
        raise IncorrectInputFieldsException
    elif user.is_active is False:
        raise UserInactiveException
    
    access_token_expires = timedelta(minutes=int(settings.ACCESS_TOKEN_EXPIRES_IN))
    access_token = create_access_token(
        data={"sub": str(user.id), "email": user.email, "scopes": form_data.scopes}, expires_delta = access_token_expires)

    return {
        "access_token": access_token,
        "token_type": "bearer",
    }


async def get_current_user(db: Session = Depends(get_db), token: str = Depends(oauth2_token)):
    try:
        black_list = await get_by_token(db, token=token)
        payload = jwt.decode(token, str(settings.SECRET_KEY), algorithms=[str(settings.JWT_ALGORITHM)])
        
        payload_id = payload.get("sub", "")
        payload_email = payload.get("email", "")

        if payload_id is None:
            raise CredentialsException
        if black_list:
            raise CredentialsException
            
        token_data = TokenData(id=payload_id, email=payload_email)

    except (JWTError, ValidationError):
        raise CredentialsException
  
    user = repository_user.get_by_id(db, id=token_data.id)

    if not user:
        raise CredentialsException
    return user
