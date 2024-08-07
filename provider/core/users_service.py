import datetime
from typing import Any, Mapping

from provider.db.repositories.addresses_repository import AddressesRepository
from provider.db.repositories.users_repository import UsersRepository
from bson import ObjectId
from provider.utils.hash_service import HashService
from provider.constants.exceptions import Exceptions


class UsersService:
    def __init__(
        self,
        users_repository: UsersRepository,
        addresses_repository: AddressesRepository,
    ):
        self.users_repository = users_repository
        self.addresses_repository = addresses_repository

    def create_user(self, data: dict) -> ObjectId:
        try:
            self.users_repository.find_one({"email": data["email"]})
        except Exception:  # which error roles
            data["password"] = HashService.hash_password(data["password"]).decode()
            data.update(
                {
                    "refresh_token": None,
                    "expired_at": None,
                    "updated_at": datetime.datetime.utcnow(),
                }
            )
            if data["role"].value == "USER":
                data.update({"is_premium": False, "bindings_left": 1})
            else:
                data.update({"is_premium": None, "bindings_left": None})
            return self.create_user(data)
        else:
            raise Exceptions.EMAIL_ERROR.value

    def get_open_bindings_count(self, user_id: ObjectId) -> int:
        return self.users_repository.find_one({"_id": user_id})["bindings_left"]

    def create_binding(self, data: dict) -> ObjectId:
        user = self.users_repository.find_one({"_id": data["user_id"]})
        if user["bindings_left"] == 0:
            raise Exceptions.LIMIT_ERROR.value
        self.users_repository.update_one(
            {"_id": user["_id"]},
            {
                "$and": [
                    {"$set": {"updated_at": datetime.datetime.utcnow()}},
                    {"$inc": {"bindings_left": -1}},
                ]
            },
        )
        return self.addresses_repository.insert_one(data)

    def get_bindings(self, user_id: ObjectId) -> (dict, list):
        bindings = self.addresses_repository.find_many({"user_id": user_id})
        return bindings[0], bindings

    def delete_binding(self, binding_id: ObjectId) -> int:
        binding = self.addresses_repository.find_one({"_id": binding_id})
        user = self.users_repository.find_one({"_id": binding["user_id"]})
        self.users_repository.update_one(
            {"_id": user["_id"]},
            {
                "$and": [
                    {"$set": {"updated_at": datetime.datetime.utcnow()}},
                    {"$inc": {"bindings_left": 1}},
                ]
            },
        )
        return self.addresses_repository.delete_one({"_id": binding_id})

    def update_binding(self, binding_id: ObjectId, data: dict) -> Mapping[str, Any]:
        binding = self.addresses_repository.find_one({"_id": binding_id})
        user = self.users_repository.find_one({"_id": binding["user_id"]})
        self.users_repository.update_one(
            {"_id": user["_id"]}, {"$set": {"updated_at": datetime.datetime.utcnow()}}
        )
        return self.addresses_repository.update_one(
            {"_id": binding_id},
            {"$set": {"ip_address": data["ip_address"], "domain": data["domain"]}},
        )
