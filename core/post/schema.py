from datetime import datetime
from typing import List
from pydantic import BaseModel, Field, validator

from core.tag.schema import TagBaseSchema

class PostBaseSchema(BaseModel):
    name: str = Field(..., max_length=100, min_length=3)
    description: str
    tags: List[int]

    @validator('description')
    def name_length_validator(cls, value):
        if len(value) < 10:
            raise ValueError('El campo descripción no puede tener menos de 10 caracteres.')
        return value

class PostResponse(PostBaseSchema):
    id: int
    tags: List[TagBaseSchema] = []
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
