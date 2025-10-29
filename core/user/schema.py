from datetime import date, datetime
from pydantic import BaseModel, EmailStr, Field, validator


class UserBaseSchema(BaseModel):
    name: str = Field(..., max_length=50, min_length=3)
    email: EmailStr

class CreateUserSchema(UserBaseSchema):
    password: str
    phone_number: str
    username: str
    
    @validator('password')
    def password_length_validator(cls, value):
        if len(value) < 8:
            raise ValueError('El campo password no puede tener menos de 8 caracteres.')
        return value

class UpdateUserSchema(UserBaseSchema):
    phone_number: str | None

class UserResponse(UserBaseSchema):
    phone_number: str
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class ListUserResponse(BaseModel):
    results: int
    users: list[UserResponse]

class BaseUserTypeSchema(UpdateUserSchema):
    pass

class UserBasicInDB(BaseModel):
    id: int
    name: str 
    email: EmailStr
    phone_number: str | None
    
    class Config:
        from_attributes = True
