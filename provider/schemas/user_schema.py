from pydantic import BaseModel, EmailStr
from provider.constants.roles import Roles


class UseCreationDTO(BaseModel):
    name: str
    surname: str
    email: EmailStr
    role: Roles
    password: str
