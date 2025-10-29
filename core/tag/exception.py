from fastapi import HTTPException, status


class TagNotFoundException(HTTPException):
    """Raised when a post is not found in the database"""

    def __init__(self):
        details = "Tag not found"
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=details)
