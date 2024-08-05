import datetime

from pydantic import BaseModel
from bson import ObjectId


class BindingCreationDTO(BaseModel):
    ip_address: str
    domain: str
    user_id: ObjectId
    created_at: datetime.datetime


class BindingUpdateDTO(BaseModel):
    ip_address: str
    domain: str
