from enum import Enum
from fastapi.exceptions import HTTPException


class Exceptions(Enum):
    EMAIL_ERROR = HTTPException(status_code=400, detail="email already taken")
    AUTHENTICATION_ERROR = HTTPException(
        status_code=401, detail="Incorrect password or username"
    )
