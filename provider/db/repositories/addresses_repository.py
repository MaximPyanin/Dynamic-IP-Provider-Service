from typing import Any, Mapping

from pymongo.cursor import Cursor

from provider.db.database import Database
from pymongo import DESCENDING
from bson import ObjectId


class AddressesRepository:
    def __init__(self, db: Database):
        self.db = db

    def find_one(self, data: dict) -> Mapping[str, Any]:
        return self.db.get_addresses_collection.find_one(data)

    def find_many(self, data: dict) -> Cursor[Mapping[str, Any] | Any]:
        return self.db.get_addresses_collection.find(data).sort(
            "created_at", DESCENDING
        )

    def insert_one(self, new_data: dict) -> ObjectId:
        return self.db.get_addresses_collection.insert_one(new_data).inserted_id

    def delete_one(self, data: dict) -> int:
        return self.db.get_addresses_collection.delete_one(data).deleted_count

    def update_one(self, filter: dict, new_data: dict) -> Mapping[str, Any]:
        return self.db.get_addresses_collection.update_one(filter, new_data).raw_result
