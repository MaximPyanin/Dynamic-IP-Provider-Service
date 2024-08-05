from typing import Any, Mapping

from bson import ObjectId
from provider.db.repositories.users_repository import UsersRepository


# add users
class AdminService:
    def __init__(self, users_repository: UsersRepository):
        self.users_repository = users_repository

    def update_account_type(
        self, user_id: ObjectId, new_data: dict
    ) -> Mapping[str, Any]:
        return self.users_repository.update_one({"_id": user_id}, new_data)

    def delete_user(self, user_id: ObjectId) -> Mapping[str, Any]:
        return self.users_repository.delete_one({"_id": user_id})
