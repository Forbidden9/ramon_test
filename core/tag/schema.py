from datetime import datetime
from typing import List
from pydantic import BaseModel, Field


class TagBaseSchema(BaseModel):
    name: str = Field(..., max_length=100, min_length=3)

class TagResponse(TagBaseSchema):
    id: int
    posts: List[int] = []
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
