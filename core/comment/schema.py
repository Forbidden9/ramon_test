from datetime import datetime
from pydantic import BaseModel


class CommentBaseSchema(BaseModel):
    description: str | None

class CommentResponse(CommentBaseSchema):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
