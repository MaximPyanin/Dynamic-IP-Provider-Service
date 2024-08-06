from typing import Any, Mapping

from bson import ObjectId
from pymongo.command_cursor import CommandCursor

from provider.db.repositories.addresses_repository import AddressesRepository
from provider.db.repositories.users_repository import UsersRepository


class AdminService:
    def __init__(
        self,
        users_repository: UsersRepository,
        addresses_repository: AddressesRepository,
    ):
        self.users_repository = users_repository
        self.addresses_repository = addresses_repository

    def update_account_type(
        self, user_id: ObjectId, new_data: dict
    ) -> Mapping[str, Any]:
        if new_data["is_premium"] is True:
            return self.users_repository.update_one(
                {"_id": user_id},
                {
                    "$and": [
                        {"$inc": {"bindings_left": 4}},
                        {"$set": {"is_premium": True}},
                    ]
                },
            )
        else:
            return self.users_repository.update_one(
                {"_id": user_id},
                {
                    "$and": [
                        {"$inc": {"bindings_left": -4}},
                        {"$set": {"is_premium": False}},
                    ]
                },
            )

    def delete_user(self, user_id: ObjectId) -> Mapping[str, Any]:
        return self.users_repository.delete_one({"_id": user_id})

    def get_user_info(self, user_id: ObjectId) -> tuple:
        return self.users_repository.find_one(
            {"_id": user_id}
        ), self.addresses_repository.find_many({"user_id": user_id})

    def get_all_users(
        self, sort: str | None, limit: int | None, skip: int | None
    ) -> CommandCursor[Mapping[str, Any] | Any]:
        query = []
        if sort:
            query.append(self.parse_sort(sort))
        if skip:
            query.append({"$skip": skip})
        if limit:
            query.append({"$limit": limit})
        return self.users_repository.aggragate(query)

    def parse_sort(self, sort: str) -> dict:
        direction, field = sort.split(",")
        if direction == "asc":
            return {"$sort": {field: 1}}
        return {"$sort": {field: -1}}
