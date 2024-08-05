from enum import Enum
from fastapi.exceptions import HTTPException


class Exceptions(Enum):
    EMAIL_ERROR = HTTPException(status_code=400, detail="email already taken")
    LOGIN_ERROR = HTTPException(
        status_code=400, detail="Incorrect password or username"
    )
    AUTHENTICATION_ERROR = HTTPException(
        status_code=401, detail="Invalid or expired token"
    )
    LIMIT_ERROR = HTTPException(
        status_code=400,
        detail="You have reached the maximum number of allowed IP address and domain bindings for your account.",
    )
