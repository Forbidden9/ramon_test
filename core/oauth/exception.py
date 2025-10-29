from fastapi import HTTPException, status


class IncorrectInputFieldsException(HTTPException):
    """Raised when the email or pasword field are incorrect in the form"""

    def __init__(self):
        details = "Incorrect email or password"
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail=details)


class CredentialsException(HTTPException):
    """Raised when the credentials are incorrect"""

    def __init__(self):
        details = "Could not validate credentials"
        super().__init__(status_code=status.HTTP_401_UNAUTHORIZED, detail=details)
