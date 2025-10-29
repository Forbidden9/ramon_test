from fastapi import HTTPException, status


class PostNotFoundException(HTTPException):
    """Raised when a post is not found in the database"""

    def __init__(self):
        details = "Post not found"
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=details)

class DuplicatePostException(HTTPException):
    """Raised when a post with the same name already exists"""

    def __init__(self):
        details = "A post with that name already exists"
        super().__init__(status_code=status.HTTP_409_CONFLICT, detail=details)

        
class PostPermitionException(HTTPException):
    """Raised when a post with the same name already exists"""

    def __init__(self):
        details = "Only the user who created a post can edit it or delete it"
        super().__init__(status_code=status.HTTP_401_UNAUTHORIZED, detail=details)
