from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from core.oauth.router import get_current_user
from core.user.exception import UserInactiveException, UserNotFoundException
from core.user.model import User

from core.user.schema import CreateUserSchema, ListUserResponse, UpdateUserSchema, UserBasicInDB, UserResponse
from core.user.repository import repository_user
from db.session import get_db


user = APIRouter()

@user.get("/", response_model=ListUserResponse, description="Get all users")
async def get_users(db: Session = Depends(get_db), limit: int = 10, page: int = 1, search: str = ""):
    skip = (page - 1) * limit
    users = db.query(User).group_by(User.id).filter(User.email.contains(search)).limit(limit).offset(skip).all()
    return {"results": len(users), "users": users}


@user.post("/", status_code=status.HTTP_201_CREATED, response_model=UserResponse, description="Register a user")
async def create_user(data_user: CreateUserSchema, db: Session = Depends(get_db)):
    new_user = repository_user.create(db, obj_in=data_user)
    return new_user

@user.put('/{user_id}', status_code=status.HTTP_200_OK, response_model=UserResponse, description="Update a user")
async def update_user(user_id: int, data_user: UpdateUserSchema, db: Session = Depends(get_db)):
    current_user = repository_user.update(db, user_id, obj_in=data_user)
    return current_user

@user.get("/me", status_code=status.HTTP_200_OK, description="Get current user")
async def get_current_active_user(current_user: User = Depends(get_current_user)):
    if current_user.is_active is False:
        raise UserInactiveException
    return current_user

@user.get('/{user_id}', status_code=status.HTTP_200_OK, response_model=UserBasicInDB, description="Get a user")
async def get_user(user_id: int, db: Session = Depends(get_db)):
    current_user = repository_user.get_by_id(db, id=user_id)
    if current_user:
        return current_user
    else:
        UserNotFoundException()
