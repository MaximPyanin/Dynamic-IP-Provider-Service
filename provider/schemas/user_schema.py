from typing import Annotated

from pydantic import BaseModel, EmailStr, Field
from provider.constants.roles import Roles


class UseCreationDTO(BaseModel):
    name: str
    surname: str
    email: EmailStr
    role: Roles
    password: Annotated[str, Field(min_length=8, max_length=32)]


class UserUpdateDTO(BaseModel):
    is_premium: bool
