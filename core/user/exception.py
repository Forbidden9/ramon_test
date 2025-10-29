from fastapi import HTTPException, status


class DuplicatedEmailException(HTTPException):
    """Raised when a user with the same email already exists in the database"""

    def __init__(self):
        details = "Email already exists"
        super().__init__(status_code=status.HTTP_409_CONFLICT, detail=details)


class DuplicatedPhoneNumberException(HTTPException):
    """Raised when a user with the same phone number already exists in the database"""

    def __init__(self):
        details = "Phone number already exists"
        super().__init__(status_code=status.HTTP_409_CONFLICT, detail=details)


class DuplicatedUsernameException(HTTPException):
    """Raised when a user with the same username already exists in the database"""

    def __init__(self):
        details = "Username already exists"
        super().__init__(status_code=status.HTTP_409_CONFLICT, detail=details)


class NotFoundPhoneNumberException(HTTPException):
    """Raised when a phone number's user is not found in the database"""

    def __init__(self):
        details = "Phone number not found"
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=details)


class UserInactiveException(HTTPException):
    """Raised when the user are inactive"""

    def __init__(self):
        details = "Inactive user"
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail=details)


class UserNotFoundException(HTTPException):
    """Raised when the user not found"""

    def __init__(self):
        details = "User not found"
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail=details)


class CurrentPasswordException(HTTPException):
    """Raised when there is an error change a password from the database"""

    def __init__(self):
        details = "Current password is not match"
        super().__init__(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=details)


class NewPasswordNotMatchException(HTTPException):
    """Raised when the password not match"""

    def __init__(self):
        details = "New password is not match."
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=details)


class PasswordTokenException(HTTPException):
    """Raised when the password token has expired"""

    def __init__(self):
        details = "Reset password token has expired, please request a new one."
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail=details)

