from fastapi import HTTPException, status


class TagPostNotFoundException(HTTPException):
    """Raised when a tag is not found in the post database"""

    def __init__(self):
        details = "Tag not found in the post"
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=details)

class DuplicateTagPostException(HTTPException):
    """Raised when a tag already exists in a job"""

    def __init__(self):
        details = "The tag already exists in the post"
        super().__init__(status_code=status.HTTP_409_CONFLICT, detail=details)


class TagPostCreateException(HTTPException):
    """Raised when there is an error creating a tag to a post in the database"""

    def __init__(self):
        details = "Error creating a tag to a post"
        super().__init__(status_code=status.HTTP_409_CONFLICT, detail=details)


class TagPostDeleteException(HTTPException):
    """Raised when there is an error deleting a tag with a post from the database"""

    def __init__(self):
        details = "Tag with a post not deleted"
        super().__init__(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=details)
